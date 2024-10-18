import pandas as pd
import customtkinter as ctk
from tkinter import ttk

import toolkit as tool
from account import Account
from constants import *


class Table(ctk.CTkFrame):

    def __init__(self, root: ctk.CTk, parent, columns: tuple, data: pd.DataFrame):
        self.__root = root
        self.__parent = parent
        self.__columns = columns
        self.__data = data
        self.__tree = None
        super().__init__(self.__parent, fg_color=WINDOW["bg"], bg_color=WINDOW["bg"])
        self.__style()
        self.__heading()
        self.__content()
        self.grid(column=0, row=0, sticky="news")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def __heading(self) -> None:
        heading_container = tool.create_container(self, bg=TABLE["header"])
        heading_container.grid(column=0, row=0, sticky="ew")
        heading_container.grid_columnconfigure(0, weight=1)

        wrapper = tool.create_container(
            heading_container, bg=TABLE["header"], fg="transparent"
        )
        wrapper.grid(column=0, row=0, sticky="ew", padx=(5, 15), pady=5)
        for idx, val in enumerate(self.__columns):
            col_name = tool.create_label(
                wrapper,
                title=f"    {val}",
                width=100,
                height=40,
                bg=TABLE["header"],
                text_color=TEXT["bg"],
            )
            col_name.grid(column=idx, row=0, sticky="w", pady=4)
            wrapper.grid_columnconfigure(idx, weight=1)

    def __content(self) -> None:
        container = ctk.CTkScrollableFrame(
            self,
            bg_color="transparent",
            fg_color="transparent",
            scrollbar_fg_color=TEXT["bg"],
            scrollbar_button_color=TEXT["border-light"],
            scrollbar_button_hover_color=TEXT["border-light-hover"],
        )
        container.grid(column=0, row=1, sticky="news")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.__tree = ttk.Treeview(container, columns=self.__columns, show="")
        self.__tree.grid(column=0, row=0, sticky="news")

        # Handle row selection
        self.__tree.bind("<<TreeviewSelect>>", self.__open_account)

        # Handle row hover
        self.__tree.tag_configure("highlight", background=TABLE["bg-hover"])
        self.__tree.bind("<Motion>", self.__highlight_row)

        # Create columns
        for col in self.__columns:
            self.__tree.column(col, anchor="w")

        # Insert data to columns
        data = self.__data[list(self.__columns)]
        for idx, (_, row) in enumerate(data.iterrows()):
            row_tag = "odd_row"
            if idx % 2 == 0:
                row_tag = "even_row"
            self.__tree.insert(
                "", "end", values=[f"   {val}".title() for val in row], tags=(row_tag,)
            )
            self.__tree.tag_configure("odd_row", background=TABLE["odd"])
            self.__tree.tag_configure("even_row", background=TABLE["even"])

    def __style(self) -> None:
        style = ttk.Style()
        style.configure(
            "Treeview",
            rowheight=60,
            background=WINDOW["bg"],
            foreground=TEXT["dark"],
            fieldbackground=WINDOW["bg"],
            font=(TEXT["font"], 12),
        )
        style.map(
            "Treeview",
            background=[("selected", TABLE["bg-hover"])],
            foreground=[("selected", TEXT["dark"])],
        )

    def __open_account(self, _) -> None:
        # Render the account details when a selection is made
        if self.__tree and self.__tree.selection():
            Account(self.__root, self.__tree)

    def __highlight_row(self, event) -> None:
        # Handle table row hover event
        tree = event.widget
        item = tree.identify_row(event.y)
        tree.tk.call(tree, "tag", "remove", "highlight")
        tree.tk.call(tree, "tag", "add", "highlight", item)
