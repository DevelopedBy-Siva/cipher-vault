from tkinter import ttk

from components.top_level import TopLevel


class Account(TopLevel):

    __KEY = "account-details"

    def __init__(self, parent, tree: ttk.Treeview) -> None:
        super().__init__(parent, key=self.__KEY)
        self.__tree = tree

    def close_window(self):
        # Clear table selection when closing window
        selection = self.__tree.selection()
        self.__tree.selection_remove(selection)
        super().close_window()
