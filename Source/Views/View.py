from abc import ABC, abstractmethod
from ..Requests import Request
from .Menus.menu_manager import MenuManager
from .Menus import Menu

class View(ABC):
    _MAX_MENU_STACK = 5

    @classmethod
    def max_menu_stack(cls) -> int:
        return(cls._MAX_MENU_STACK)

    def __init__(self, starting_menu : Menu):
        self._menus = MenuManager(type(self).max_menu_stack())
        self._current_menu = starting_menu()

    @property
    def menu(self) -> Menu:
        return(self._current_menu)
    
    @property
    def previous_menu_name(self) -> str:
        return(self._menus.check_backwards().__class__._NAME)

    @menu.setter
    def menu(self, menu : Menu) -> None:
        self._current_menu = menu

    @abstractmethod
    def show(self, data) -> Request:
        pass