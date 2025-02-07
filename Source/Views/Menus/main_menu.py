from .mass_investment_confirmation_menu import MassInvestmentConfirmationMenu
from .menu import Menu

class MainMenu(Menu):
    '''
    '''
    _OPTIONS = {
        "Invertir en masa." : MassInvestmentConfirmationMenu,
    }
    _NAME = "Menú principal"
    _RETURN_BACK = "Salir del programa."