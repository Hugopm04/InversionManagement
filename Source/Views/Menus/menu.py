from abc import ABC, abstractmethod
from ...Requests import Request
from typing import Self, Union


class Menu():
    '''
    All menus should have their own static attribute containing their options without the indexing.
    '''
    _HEADER = None
    _OPTIONS = None
    _RETURN_BACK = "Volver al menú anterior: "


    @classmethod
    def _str_options(cls) -> list[str]:
        return(list(cls._options().keys()))

    @classmethod
    def _options(cls) -> dict[str, Union[Request, Self]]:
        return(cls._OPTIONS)

    @classmethod
    def _name(cls) -> str:
        return(cls._NAME)

    @classmethod
    def _n_options(cls) -> int:
        return(len(cls._OPTIONS))

    @classmethod
    def _return_back(cls) -> str:
        return(cls._RETURN_BACK)

    @classmethod
    def _header(cls) -> str:
        return(cls._HEADER)

    def __init__(self):
        pass

    @property
    def previous_menu(self) -> Self:
        return(self._previous_menu)

    @property
    def str_options(self) -> list[str]:
        return(self.__class__._str_options())

    @property
    def options(self) -> dict[str, Union[Request, Self]]:
        return(self.__class__._options())

    @property
    def name(self) -> str:
        return(self.__class__._NAME)

    @property
    def n_options(self) -> int:
        return(self.__class__._n_options())

    @property
    def return_back(self) -> str:
        return(self.__class__._return_back())

    @property
    def header(self) -> str:
        return(self.__class__._header())



    

    