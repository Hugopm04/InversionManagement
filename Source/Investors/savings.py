from .transaction import Transaction
from typing import Self
import datetime
import json

class Savings(Transaction):
    _FILENAME = '-savings.json'

    def __init__(self, amount:float, date:datetime=datetime.datetime.now()) -> None:
        super().__init__(amount, date, 0)
    
    def __str__(self) -> str:
        output = "Fecha: " + str(self.date) + ", "
        output += "Cantidad: " + str(self.amount) + ", "
        output += "Comisión: " + str(self.fee)
        
        return(output)

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        savings = cls(data["Cantidad"], data["Fecha"], data["Comisión"])
        return(savings)
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        return(data)
    
    def filename(self) -> str:
        f = str(self.date) + Savings._FILENAME
        return(f)