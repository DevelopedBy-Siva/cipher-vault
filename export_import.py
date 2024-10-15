from customtkinter import *

from top_level import TopLevel
from constants import *


class ExportImport(TopLevel):

    __KEY = "export-import"

    def __init__(self, parent) -> None:
        super().__init__(parent, key=self.__KEY)
