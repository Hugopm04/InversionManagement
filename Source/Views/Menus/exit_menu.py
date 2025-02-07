from .menu import Menu
from typing import Self, Union
from ...Requests import Request
from .main_menu import MainMenu

class ExitMenu(Menu):
    _HEADER = "¿Estás seguro de que quieres salir?"
    _OPTIONS = {
        "Salir." : Request.EXIT,
        "Volver al menú principal." : MainMenu
    }

    def ask(self) -> Union[Request,Self] :
        return(Request.EXIT)