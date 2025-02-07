from .investment import Investment
from .savings import Savings
from .periodic_registry import PeriodicRegistry
from .value_distribution import ValueDistribution
from typing import Self
import os
import json

class Investor():
    _DEFAULT_RELATION_SAVINGS_INVERSION = 0.5
    _FILENAME = '-info.json'

    @staticmethod
    def filename() -> str:
        return(Investor._FILENAME)

    def __init__(self, name:str) -> None:
        """_summary_
        Investor serves as a database for individual users.
        Args:
            name (str): _description_ Name of the inversor.
            _investments (dict): _description_ Dictionary with ticker as key and quantity as value.
            _savings (float): _description_ Total quantity of money saved.
            _debt (float): _description_ Money owed by the user to the fund.
            _total_contribution (float): _description_ Total quantity of money contributed by the user.
            _relation_savings_inversion (float, optional): _description_ Desired relationship between the total savings and the total inverted value. Defaults to 0.5.
        """
        self._name : str = name
        self._savings :float = 0
        self._debt : float = 0
        self._investments : dict[str, float] = {}
        self._periodic_contribution : float = 0
        self._total_contribution :float = 0

        self._relation_savings_inversion = Investor._DEFAULT_RELATION_SAVINGS_INVERSION
    
    @property
    def name(self) -> str:
        return(self._name)
    
    @property
    def savings(self) -> float:
        return(self._savings)
    
    @property
    def investments(self) -> dict:
        return(self._investments)

    @property
    def debt(self) -> float:
        return(self._debt)

    @property
    def total_contribution(self) -> float:
        return(self._total_contribution)

    @property
    def periodic_contribution(self) -> float:
        return(self._periodic_contribution)

    def withdraw(self, amount:float) -> None:
        """_summary_
        Withdraws money from the savings of the user.
    
        Args:
            amount (float): _description_ Quantity of money to withdraw.

        Preconditions:
            - The amount to withdraw must be less or equal than the total savings of the user.

        """
        self._savings -= amount

    def value_distribution(self, current_prices : dict[str, float], inversion_percent:float=1) -> ValueDistribution:
        '''
        Returns the distribution of the value of the user between savings and investments if it was to make an ivestment.
        Args:
            current_prices (dict): _description_ Dictionary with the ticker as key and the current price as value.
            inversion_percent (float, optional): _description_ For cases when a full inversion is not desired, instead of investing the usual quantity only a percentaje will be used. Deafults to 1.
        
        Returns:
            list[float]: _description_ List with the savings and the investments value. 
                - [0] Value to invest.
                - [1] Value to save.
        '''
        inversion_size = self.periodic_contribution
        amount_to_save = min([ self.difference(current_prices), inversion_size ])
        
        if (self._savings - amount_to_save < 0):
            amount_to_save = - self._savings
        
        amount_to_invest = (inversion_size - amount_to_save) * inversion_percent
        amount_to_save += (inversion_size - amount_to_save) * (1 - inversion_percent)
        distribution = ValueDistribution(amount_to_invest, amount_to_save)
        return(distribution)

    def add_investment(self, current_prices:float, ticker:str, fee:float=0, inversion_percent:float=1) -> PeriodicRegistry:
        """_summary_
        Given the periodic contribution, splits it into the inversion and the savings mounts. Creates and saves the new inversion of the user.
        Also increases it's debt by the inversion size and updates the total contribution by the same amount.

    
        Args:
            current_price (float): _description_ Current price of the action to buy.
            fee (float, optional): _description_ Fee of the movement. Defaults to 0.
            inversion_percent (float, optional): _description_ For cases when a full inversion is not desired, instead of investing the usual quantity only a percentaje will be used. Deafults to 1.    
        """
        inversion_size = self.periodic_contribution
        self._total_contribution += inversion_size
        self._debt += inversion_size

        distribution = self.value_distribution(current_prices, inversion_percent)
        amount_to_invest = distribution.investment
        amount_to_save = distribution.savings

        quantity = amount_to_invest / current_prices[ticker]
        inversion = Investment(current_prices[ticker], quantity, fee)
        savings = Savings(amount_to_save)
        registry = PeriodicRegistry(inversion, savings)

        self._investments[ticker] += quantity
        self._savings += amount_to_save

        return(registry)

    def pay_debt(self, amount:float) -> None:
        self._debt -= amount

    def difference(self, current_prices : dict[str, float]) -> float:
        """_summary_
        Returns the neccesary quantity to achieve the desired relationship between the savings value and the invested ones.
        """
        total = self.investments_current_value(current_prices) + self.savings
        savings_percentage = self.savings / total
        needed_quantity = 0
        displacement = self._relation_savings_inversion - savings_percentage
        
        needed_quantity = displacement * total
        
        return(needed_quantity)
    
    def investments_current_value(self, current_prices:dict) -> float:
        """_summary_
        Returns the current value of all the investments of the user.
    
        Args:
            current_prices (dict): _description_ Dictionary with the ticker as key and the current price as value.
    
        Returns:
            float: _description_ Total value of the investments.
        """
        value = 0
        for ticker in self._investments:
            value += self._investments[ticker] * current_prices[ticker]
        return(value)
    
    
    def profit(self, current_prices:dict) -> float:
        """_summary_
        Returns the total profit of the user.
    
        Args:
            current_prices (dict): _description_ Dictionary with the ticker as key and the current price as value.
    
        Returns:
            float: _description_ Total profit of the user.
        """
        profit = self.investments_current_value(current_prices) - self._total_contribution
        return(profit)

    def __str__(self) -> str:
        s = "Datos de " + self._name + ":\n"
        s += "\t- Ahorros: " + str(self._savings) + "\n"
        s += "\t- Deuda: " + str(self._debt) + "\n"
        s += "Contribución total: " + str(self.total_contribution) + "\n"
        s += "Valor actual: " + str(self.investments_current_value()) + "\n"
        s += "Beneficio total: " + str(self.profit()) + "\n"
        s += "Valor a invertir cada mes: " + str(self.periodic_contribution) + "\n"
        s += "Relación ahorros-inversiones: " + str(self._relation_savings_inversion) + "\n"
        s+= "\t- Inversiones: \n"
        for ticker in self._investments:
            s += "\t\t- " + ticker + " : " + str(self._investments[ticker]) + "\n"
        return(s)

    def to_dict(self) -> dict:
        data = {
            "Nombre": self._name,
            "Ahorros": self._savings,
            "Inversiones": self._investments,
            "Deuda": self._debt,
            "Contribución total": self._total_contribution,
            "Contribución periódica": self._periodic_contribution,
            "Relación ahorros-inversiones": self._relation_savings_inversion
        }
        return(data)

    def save(self, dir:str) -> None:
        with open(os.path.join(dir, self.name), 'w') as file:
            json.dump(self.to_dict(), file)
    
    @classmethod
    def from_dict(cls, data:dict) -> Self:
        investor = cls(data["Nombre"])
        investor._savings = data["Ahorros"]
        investor._investments = data["Inversiones"]
        investor._debt = data["Deuda"]
        investor._total_contribution = data["Contribución total"]
        investor._periodic_contribution = data["Contribución periódica"]
        investor._relation_savings_inversion = data["Relación ahorros-inversiones"]
        return(investor)
    
    def load(self, filename:str) -> None:
        with open(filename, 'r') as file:
            data = json.load(file)
            self = Investor.from_dict(data)
        