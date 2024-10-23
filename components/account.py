from typing import Callable

from components.top_level import TopLevel


class Account(TopLevel):

    __KEY = "account-details"

    def __init__(self, parent, index: int, refresh: Callable) -> None:
        super().__init__(parent, key=self.__KEY)
        self.__df_index = index
        self.__refresh_table = refresh
