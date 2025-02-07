from .transaction import Transaction
from datetime import datetime
from typing import Self
import os
import json

class Investment(Transaction):
    _FILENAME = '-investment.json'
    def __init__(self, savings : float, purchase_price:float, quantity:float, date:datetime=datetime.now(), fee:float=0) -> None:
        super().__init__(purchase_price * quantity, date, fee)
        self._purchase_price = purchase_price
        self._stock_quantity = quantity
    
    @property
    def purchase_price(self) -> float:
        return(self._purchase_price)
    
    @property
    def stock_quantity(self) -> float:
        return(self._stock_quantity)

    def current_value(self, current_price:float) -> float:
        value = self._stock_quantity * current_price
        return(value)
    
    def initial_value(self) -> float:
        value = self._purchase_price * self._stock_quantity
        return(value)
        
    def benefit(self, current_price:float) -> float:
        benefit = self.current_value(current_price) - self.initial_value() - self._fee
        return(benefit)
    
    def __str__(self) -> str:
        output = "Fecha compra: " + str(self.date) + ", "
        output += "Precio de compra: " + str(self._purchase_price) + ", "
        output += "Nº de acciones: " + str(self._stock_quantity) + ", "
        output += "Comisión: " + str(self._fee)
        
        return(output)

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        inversion = cls(data["Precio de compra"], data["Nº de acciones"], data["Fecha"], data["Comisión"])
        return(inversion)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["Precio de compra"] = self._purchase_price
        data["Nº de acciones"] = self._stock_quantity
        return(data)
    
    def filename(self):
        f = str(self.date) + Investment._FILENAME
        return(f)