from customtkinter import *

from top_level import TopLevel
from constants import *

_KEY = "export-import"


class ExportImport(TopLevel):

    def __init__(self, parent) -> None:
        super().__init__(parent, key=_KEY)
