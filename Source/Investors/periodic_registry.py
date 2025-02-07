from .investment import Investment
from typing import Self
from Source.Investors.savings import Savings
import datetime
import json
import os

class PeriodicRegistry():
    def __init__(self, investment : Investment, savings : Savings):
        self._investment = investment
        self._savings = savings
    
    @property
    def date(self) -> datetime:
        return(self._investment.date)
    
    @property
    def amount_saved(self) -> float:
        return(self._savings.amount)

    @property
    def total_contribution(self) -> float:
        return(self._investment.amount + self._savings.amount)


    def __str__(self) -> str:
        pass

    def save(self, dir:str) -> None:
        os.makedirs(dir, exist_ok=True)
        self._investment.save()
        self._savings.save()

    @classmethod
    def from_dir(cls, dir:str) -> Self:
        pass