from .transaction import Transaction
from typing import Self
import datetime
import json

class Transfer(Transaction):
    def __init__(self, amount:float, source:str, destination:str, date:datetime=datetime.datetime.now(), fee:float=0) -> None:
        super().__init__(amount, date, fee)
        self._source = source
        self._destination = destination
    
    @property
    def source(self) -> str:
        return(self._source)
    
    @property
    def destination(self) -> str:
        return(self._destination)
    
    def __str__(self) -> str:
        output = "Fecha: " + str(self.date) + ", "
        output += "Cantidad: " + str(self.amount) + ", "
        output += "Origen: " + self._source + ", "
        output += "Destino: " + self._destination + ", "
        output += "Comisión: " + str(self.fee)
        
        return(output)

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        transfer = cls(data["Cantidad"], data["Origen"], data["Destino"], data["Fecha"], data["Comisión"])
        return(transfer)
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["Origen"] = self._source
        data["Destino"] = self._destination
        return(data)
    
    def filename(self) -> str:
        f = self.source
        f += "-" + self.destination
        f += "-" + str(self.date)
        return(f)