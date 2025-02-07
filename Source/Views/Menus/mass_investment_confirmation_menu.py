from ...Requests import Request
from .menu import Menu

class MassInvestmentConfirmationMenu(Menu):
    _OPTIONS = {
        "Realizar inversión en masa." : Request.MASS_INVESTMENT
    }
    _NAME = "Menú de confirmación"