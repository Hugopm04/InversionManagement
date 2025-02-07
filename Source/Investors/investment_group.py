from .investor import Investor
from .transfer import Transfer
from .periodic_registry import PeriodicRegistry
from .value_distribution import ValueDistribution
import yfinance as yf
from typing import Self
import json
import os

class InvestmentGroup():
    _FILENAME = 'InvestmentGroup.json'
    _TRANSACTIONS_DIR = 'Transactions'
    
    def __init__(self):
        '''
        Creates a new InvestmentGroup object.
        _balance (float): _description_ When clients contribute money to the group, it is stored here. When money is taken for investments or savings, it is taken from here. So:
            - If the balance is positive, there is remaining money to be invested or saved.
            - If the balance is negative, someone in the group is in debt.
        _investors (list): _description_ List of investors in the group.
        _investment_rate (float): _description_ Percentage of the adjusted contribution to be invested. That means, after balancing the savings and investments of the investor.
        '''
        self._balance : float = 0
        self._investors : list[Investor] = []
        self._periodic_fee : float = 1
        self._investment_rate : float = 1
        self._prices_updated : bool = False
        self._current_prices : dict[str, float] = {}


    @property
    def balance(self) -> float:
        '''
        Returns the balance of the group.
        '''
        return self._balance

    @property
    def current_prices(self) -> dict[str, float]:
        if not self._prices_updated:
            self.update_stock_prices()
            self._prices_updated = True
        return self._current_prices
        
            

    def total_profit(self) -> float:
        '''
        Returns the total profit of the group.
        '''
        return sum([investor.profit() for investor in self._investors])

    def total_savings(self) -> float:
        '''
        Returns the total savings of the group.
        '''
        return sum([investor.savings() for investor in self._investors])
    
    def total_investments_value (self) -> float:
        '''
        Returns the total value of the investments of the group.
        '''
        return sum([investor.investments_current_value() for investor in self._investors])

    def _get_current_prices(self, tickers : set[str]) -> dict[str, float]:
        '''
        Returns a dictionary with the current prices of the tickers in the set 'tickers'.
        It has to access the Yahoo Finance API to get the current prices so take in mind is an inefficient operation.
        '''
        current_prices = {}
        for ticker in tickers:
            current_prices[ticker] = yf.Ticker(ticker).history(period='1d', interval='1m')['Close'].iloc[-1]
        return current_prices

    def update_stock_prices(self) -> None:
        '''
        Updates the variable self._current_prices with the current value of the stocks the group is investing in.
        '''
        tickers = set()
        for investor in self._investors:
            tickers.update(investor.investments.keys())
        
        self._current_prices = self._get_current_prices(tickers)

    def value_to_invest(self) -> float:
        '''
        If an investment was considered to be mande now, how much would the group invest.
        '''
        value = 0
        for investor in self._investors:
            value += investor.value_distribution(self.current_prices, self._investment_rate).investment
        return value

    def pay_debt(self, name : str, amount : float) -> None:
        '''
        Pays x amount of money of the debt of the investor with the name 'name'.
        Saves a Transfer object with the transaction.
        '''
        for investor in self._investors:
            if investor.name == name:
                investor.pay_debt(amount)
                self._balance += amount
                break
        
        transfer = Transfer(amount, name, 'Group')
        os.makedirs(InvestmentGroup._TRANSACTIONS_DIR, exist_ok=True)
        transfer.save(os.path.join(InvestmentGroup._TRANSACTIONS_DIR, transfer.filename()))


    def withdraw(self, name : str, amount : float) -> None:
        '''
        Withdraws x amount of money from the savings of the investor with the name 'name'.
        Saves a Transfer object with the transaction.
        
        Precondition: The investor must have enough money in savings to withdraw the amount.
        '''
        for investor in self._investors:
            if investor.name == name:
                investor.withdraw(amount)
                break
        
        transfer = Transfer(amount, 'Group', name)
        os.makedirs(InvestmentGroup._TRANSACTIONS_DIR, exist_ok=True)
        transfer.save(os.path.join(InvestmentGroup._TRANSACTIONS_DIR, transfer.filename()))

    def mass_invest(self, fee : float) -> None:
        '''
        Iterates through all the investors in the group and invests their corresponding periodic contribution respecting
        the percentage of investments and saving of each investor. Saves all the investments as Investment objects.
        '''
        current_prices = self.get_stocks_value()
        for investor in self._investors:
            registry = investor.add_investment(current_prices, fee)
            self._balance -= registry.total_contribution
            registry.save(investor.name)

    @classmethod
    def from_dict(cls, data : dict) -> Self:
        '''
        Creates a new InvestmentGroup object from a dictionary.
        '''
        group = cls()
        group._balance = data['Balance']
        return(group)

    def load(self, dir : str):
        '''
        Loads the InvestmentGroup object and all of it's investors from a directory.
        '''
        os.chdir(dir)
        with open(self._FILENAME, 'r') as file:
            data = json.load(file)
            self = InvestmentGroup.from_dict(data)
        
        for investor in os.listdir():
            if os.path.isdir(investor):
                new_investor = Investor()
                new_investor.load(os.path.join(dir, investor + Investor.filename()))
                self._investors.append(new_investor)

    def to_dict(self) -> dict:
        '''
        Returns a dictionary with the data of the InvestmentGroup object.
        '''
        data = {
            'Balance': self._balance,
        }
        return data

    def save(self, dirname : str):
        '''
        Saves the InvestmentGroup object and all of it's investors to a file.
        '''
        os.makedirs(dirname, exist_ok=True)
        with open(os.path.join(dirname, self._FILENAME), 'w') as file:
            json.dump(self.to_dict(), file)
        
        for investor in self._investors:
            os.makedirs(os.path.join(dirname, investor.name), exist_ok=True)
            investor.save(os.path.join(dirname, investor.name + Investor.filename()))
            os.chdir(dirname)

    def investment_confirmation(self) -> None:
        '''
        Displays usefult data to chekc before confirming the investment.
        '''
        print("La cantidad a invertir (teniendo en cuenta el porcentage) es: " + str(self.value_to_invest()))
        print("El procentaje de reducción de inversión es de: " + str(self._investment_rate))
        print("La comisión establecida es de: " + str(self._periodic_fee))
        print("Los precios actuales son:")
        current_prices = self.get_stocks_value()
        for ticker, price in current_prices.items():
            print("\t-" + ticker + ": " + str(price))

            