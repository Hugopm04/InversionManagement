from .menu import Menu
from collections import deque


class MenuManager():
    def __init__(self, max_size : int = 5):
        self._max_size = max_size
        self._previous_menus : deque = deque(maxlen=max_size)
        self._future_menus : deque = deque(maxlen=max_size)
    
    def add_forward(self, menu : Menu) -> None:
        self._future_menus.append(menu)
    
    def add_backward(self, menu : Menu) -> None:
        self._previous_menus.append(menu)

    def go_back(self, current_menu : Menu) -> Menu:
        menu = self._previous_menus.pop()
        self._future_menus.append(current_menu)
        return(menu)
    
    def go_forward(self, current_menu : Menu) -> Menu:
        menu = self._future_menus.pop()
        self._previous_menus.append(current_menu)
        return(menu)
    
    def check_forward(self) -> Menu:
        if len(self._future_menus) > 0:
            return(self._future_menus[0])
        else:
            return(None)

    def check_backwards(self) -> Menu:
        if len(self._previous_menus) > 0:
            return(self._previous_menus[0])
        else:
            return(None)