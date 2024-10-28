import pyperclip
import customtkinter as ctk
import pandas as pd
from typing import Callable

import utility.toolkit as tool
from components.data_store import DataStore
from custom_widgets import Entry, Frame, TopLevel, Label, Button, Image

from utility.constants import *


class Account(TopLevel):

    __KEY = "account-details"

    def __init__(self, parent, data: pd.Series, refresh: Callable) -> None:
        super().__init__(parent, key=self.__KEY)
        self.__data_series = data.dropna()
        self.__entries = {}
        self.__refresh_table = refresh
        self.__content()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def __content(self) -> None:
        container = Frame(self)
        container.grid(column=0, row=1, sticky="news")
        container.grid_columnconfigure(0, weight=1)

        row_count = 0
        for idx, (key, val) in enumerate(ACCOUNT_EDIT.items()):

            item = self.__data_series.get(key, None)
            if not item:
                continue

            item_container = Frame(container)
            label = Label(
                item_container,
                title=f'{val["title"]}:',
                width=135,
                font_size=13,
                text_color=TEXT["light_2"],
            )
            label.grid(column=0, row=0, sticky="w")
            if not val["editable"]:
                non_editable_field = Label(
                    item_container,
                    title=item,
                    font_size=12,
                )
                non_editable_field.grid(
                    column=1,
                    row=0,
                    sticky="we",
                    columnspan=2,
                    padx=(3, 0),
                )
            else:
                editable_field = Entry(
                    item_container,
                    value=item.strip(),
                    placeholder=val["placeholder"],
                )
                editable_field.grid(column=1, row=0, sticky="we")

                copy_btn = Button(
                    item_container,
                    command=lambda text=str(item): self.__copy_to_clipboard(text),
                    width=40,
                    title="",
                    icon=Image("copy", (15, 15)),
                    bg=BUTTON["bg-light"],
                    hover_bg=BUTTON["hover-bg-l"],
                )
                copy_btn.grid(column=2, row=0, sticky="we", padx=(8, 0))

                if key == "Password":
                    generate_password_btn = Button(
                        item_container,
                        command=self.__generate_password,
                        title="Generate New",
                        text_color=TEXT["dark"],
                        bg=BUTTON["bg-light"],
                        hover_bg=BUTTON["hover-bg-l"],
                        width=110,
                    )
                    generate_password_btn.grid(
                        column=3, row=0, sticky="we", padx=(8, 0)
                    )

                error_field = Label(
                    item_container,
                    text_color=TEXT["error"],
                    title="",
                    font_size=11,
                )
                error_field.grid(column=1, row=1, sticky="we")
                self.__entries[key] = (editable_field, error_field)

            item_container.grid(column=0, row=idx, sticky="we", pady=(0, 4))
            item_container.grid_columnconfigure(1, weight=1)
            row_count += 1

        btn_container = Frame(container)
        btn_container.grid(column=0, row=row_count, sticky="we", pady=(25, 0))
        btn_container.grid_columnconfigure(0, weight=1, uniform="account_btn")
        btn_container.grid_columnconfigure(1, weight=1, uniform="account_btn")

        delete_btn = Button(
            btn_container,
            self.__delete_account,
            title="Delete",
            text_color=TEXT["bg"],
            bg=TEXT["error"],
            hover_bg=TEXT["error_light"],
            width=215,
        )
        delete_btn.grid(column=0, row=0, sticky="e", padx=(0, 5), pady=(5, 0))

        save_btn = Button(
            btn_container,
            self.__save_account,
            title="Save",
            width=215,
        )
        save_btn.grid(column=1, row=0, sticky="w", padx=(5, 0), pady=(5, 0))

    def __copy_to_clipboard(self, text: str) -> None:
        """
        Copy text to clipboard
        Args:
            text (str): Text to copy
        """
        pyperclip.copy(text)

    def __delete_account(self) -> None:
        try:
            success = DataStore.delete_account(id=self.__data_series["UUID"])
            if not success:
                raise Exception("Failed to delete")
            self.__refresh_table()  # Reload the table
            self.close_window()  # Close the window
        except:
            _, error = self.__entries["Account"]
            if isinstance(error, ctk.CTkLabel):
                error.configure(text="Oops! Couldn’t delete the account. Try again!")

    def __save_account(self) -> None:
        is_valid = True
        data = {}
        for key, item in self.__entries.items():
            input_entry, input_error = item
            value = input_entry.get().strip()
            # Validation
            if isinstance(input_entry, ctk.CTkEntry):
                if len(value) < ACCOUNT_EDIT[key]["min_len"]:
                    is_valid = False
                    error_msg = ACCOUNT_EDIT[key]["error"]
                    if isinstance(input_error, ctk.CTkLabel):
                        input_error.configure(text=error_msg)
                else:
                    if isinstance(input_error, ctk.CTkLabel):
                        input_error.configure(text="")
            data[key] = value
        if not is_valid:
            return
        # Get the current Date Time
        data["Last Modified"] = tool.current_datetime()
        # Update data
        success = DataStore.update_account(data, self.__data_series["UUID"])
        if success:
            self.__refresh_table()
            self.close_window()
        else:
            # Failed to update data
            error_msg = ACCOUNT_EDIT["Account"]["save_failed"]
            unknown_error = self.__entries["Account"][1]
            if isinstance(unknown_error, ctk.CTkLabel):
                unknown_error.configure(text=error_msg)

    def __generate_password(self) -> None:
        """
        Generates a random password
        """
        new_password = tool.generate_password()
        entry, error = self.__entries.get("Password", None)
        if isinstance(entry, ctk.CTkEntry) and isinstance(error, ctk.CTkLabel):
            entry.delete(0, "end")
            entry.insert(0, new_password)
            error.configure(text="")
