from ..Views import View
from ..Investors import InvestmentGroup
from ..Requests import Request
from ..Views.Menus import Menu
from ..Views.Menus.menu_manager import MenuManager

class Controller():
    _MAX_MENU_STACK = 5

    def __init__(self, view : View, group : InvestmentGroup):
        self._view = view
        self._group = group

        self._REQUESTS_RESPONSE : dict[Request, function] = {
            Request.MASS_INVESTMENT : lambda : self.group.mass_invest(),
        }

    @property
    def view(self) -> View:
        return(self._view)

    @property
    def group(self) -> InvestmentGroup:
        return(self._group)

    def run(self):
        request = self.view.show()
        self.proccess_request(request)

    def proccess_request(self, request : Request):
        self._REQUESTS_RESPONSE[request]()
