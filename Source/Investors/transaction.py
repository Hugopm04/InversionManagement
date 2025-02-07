from abc import ABC, abstractmethod
from typing import Self
import json
import datetime


class Transaction(ABC):
    def __init__(self, amount : float, date : datetime = datetime.datetime.now(), fee : float = 0) -> None:
        self._amount = amount
        self._date = date
        self._fee = fee
    
    @property
    def amount(self) -> float:
        return(self._amount)
    
    @property
    def date(self) -> datetime:
        return(self._date)
    
    @property
    def fee(self) -> float:
        return(self._fee)
    
    def to_dict(self) -> dict:
        data = {
            "amount" : self.amount,
            "date" : self.date,
            "fee" : self.fee
        }
        return(data)
    
    @abstractmethod
    def __str__(self) -> str:
        pass

    def save(self) -> None:
        '''Saves the transaction in a file in the current dir.'''
        with open(self.filename(), 'a') as file:
            file.write(json.dump(self.to_dict()) + "\n")

    @classmethod
    @abstractmethod
    def from_dict(cls : Self, data : dict) -> Self:
        pass

    @abstractmethod
    def filename(self) -> str:
        pass

    

