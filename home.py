import customtkinter as ctk

import toolkit as tool
from constants import *
from new_account import NewPassword
from export_import import ExportImport
from account_table import AccountTable


class Home(ctk.CTkFrame):

    def __init__(self, root: ctk.CTk) -> None:
        self.__root = root
        super().__init__(self.__root)
        self.__create_header()
        self.__show_account_details()
        self.configure(bg_color=WINDOW["bg"], fg_color=WINDOW["bg"])
        self.grid(column=0, row=0, sticky="news", padx=50, pady=30)
        self.grid_columnconfigure(0, weight=1)

    def __create_header(self) -> None:

        # Create a header wrapper
        container = tool.create_container(self)
        container.grid(column=0, row=1, sticky="ew", pady=(20, 0))

        # Create header and subheading wrapper
        label_container = tool.create_container(container)
        label_container.grid(column=0, row=0, sticky="w", pady=(0, 40))

        heading = tool.create_label(
            label_container,
            title="Your Secure Vault",
            text_color=TEXT["dark"],
            font_size=24,
        )
        heading.grid(column=0, row=0, sticky="w")

        subheading = tool.create_label(
            label_container,
            title="Easily manage and access all your passwords and sensitive information.",
            text_color=TEXT["light"],
        )
        subheading.grid(column=0, row=1, sticky="w")

        # Create search box
        search_box = tool.create_entry(container, placeholder="Search accounts...")
        search_box.grid(column=0, row=1, sticky="nwse")

        # Create user options
        for idx, (key, val) in enumerate(USER_OPTIONS.items()):
            button = tool.create_button(
                container,
                command=lambda key=key: self.__navigate_to(key),
                title=val["title"],
            )
            button.grid(column=idx + 1, row=1, sticky="e", padx=(10, 0))

        container.grid_columnconfigure(0, weight=1)

    def __show_account_details(self) -> None:

        table_container = tool.create_container(self)
        table_container.grid(column=0, row=2, sticky="news", pady=(40, 0))

        _ = AccountTable(table_container)

        table_container.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def __navigate_to(self, key: str) -> None:
        if key == "new":
            _ = NewPassword(self.__root)
        elif key == "exp-imp":
            _ = ExportImport(self.__root)
        else:
            pass
