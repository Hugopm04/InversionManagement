from .View import View
from ..Requests import Request
from .Menus import Menu, MainMenu
from .Menus.exit_menu import ExitMenu

class CMDView(View):
    _INPUT_PROMPT = '-> '
    _EXIT_MENU = ExitMenu

    def __init__(self):
        super().__init__(CMDView._EXIT_MENU)
        self._menus.add_backward(self.menu)
        self.menu = MainMenu()
     

    def print_options(self):
        ASCII_CODE_FOR_A = 97
        
        if self.menu.header:
            print(self.menu.header)

        options = self.menu.str_options
        current_char = ASCII_CODE_FOR_A
        for option in options:
            print(type(self)._indexation(current_char) + option)
            current_char += 1
        self.print_return_back(current_char)


    def ask(self) -> Request:
        ASCII_CODE_FOR_A = 97
        
        options = self.menu.options

        self.print_options()
        answer = input(CMDView._INPUT_PROMPT)
        if len(answer) > 0:
            answer = ord(answer) - ASCII_CODE_FOR_A
        else:
            answer = -1
        
        while answer not in range(len(options) + 1):
            print("Opción no válida.")
            answer = input(CMDView._INPUT_PROMPT)
            if len(answer) > 0:
                answer = ord(answer) - ASCII_CODE_FOR_A
            else:
                answer = -1

        if answer < len(options):
            option = self.menu.str_options[answer]
            option = options[option]
            if (type(option) == Request):
                return(option)
            else: #Moving forward to another menu:
                if type(self._menus.check_forward()) == option: #Already existing menu.
                    self._menus.go_forward(self.menu)
                else: #Creating the new menu
                    self._menus.add_backward(self.menu)

                return(option())
        else: #Moving to previous menu:
            return(self._menus.go_back(self.menu))


    def show(self) -> Request:
        answer = self.ask()
        if type(answer) == Request:
            return(answer)
        else:
            self.menu = answer
            return(self.show())

    @staticmethod
    def _indexation(current_char : int) -> str:
        s = chr(current_char) + ') '
        return(s)

    def print_return_back(self, char : str) -> None:
        if not type(self.menu) == CMDView._EXIT_MENU:
            print(CMDView._indexation(char) + self.menu.return_back)