import uuid
import customtkinter as ctk
from typing import Callable

import utility.toolkit as tool
from utility.constants import *
from components.top_level import TopLevel
from components.data_store import DataStore


class NewAccount(TopLevel):

    __KEY = "new-password"
    __password_hide_ico = tool.ctk_image("password-hide", (16, 16))
    __password_show_ico = tool.ctk_image("password-show", (16, 16))

    def __init__(self, parent, refresh_table: Callable) -> None:
        super().__init__(parent, key=self.__KEY, grid_y_size=4)
        self.__entries = {}
        self.__user_input()
        self.__refresh_table = refresh_table

    def __user_input(self) -> None:

        self.grid_columnconfigure(1, weight=1)

        row_idx = 0
        for key, entry in dict(USER_OPTIONS["new"]["inputs"]).items():
            show = entry.get("show", "")

            row_idx += 1
            entry_label = tool.create_label(
                self,
                title=f'{entry["title"]}:',
                font_size=13,
                text_color=TEXT["light_2"],
            )
            entry_label.grid(
                column=0,
                row=row_idx,
                sticky="w",
                padx=(0, 25),
            )

            entry_box_container = tool.create_container(
                self, border_color=TEXT["border"], border_width=1
            )
            entry_box = tool.create_entry(
                entry_box_container,
                placeholder=entry["placeholder"],
                show=show,
                border=False,
                height=20,
            )
            entry_box.grid(column=0, row=0, sticky="nwse", padx=3, pady=3)
            entry_box_column_span = 3

            if show == "*":
                password_toggle_btn = tool.create_button(
                    entry_box_container,
                    command=lambda: self.__toggle_password(
                        entry_box, password_toggle_btn
                    ),
                    title="",
                    bg=TEXT["bg"],
                    hover_bg=TEXT["bg"],
                    width=0,
                    height=0,
                    icon=self.__password_hide_ico,
                )
                password_toggle_btn.grid(
                    column=1,
                    row=0,
                    padx=(0, 3),
                    sticky="e",
                )

            command = entry.get("command", None)
            if isinstance(command, dict):
                generate_button = tool.create_button(
                    self,
                    command=self.__generate_password,
                    title=entry["command"]["title"],
                    bg=BUTTON["bg-light"],
                    hover_bg=BUTTON["hover-bg-l"],
                    text_color=TEXT["dark"],
                    height=37,
                )
                generate_button.grid(
                    column=3,
                    row=row_idx,
                    padx=(15, 0),
                )
                entry_box_column_span = 1

            entry_box_container.grid(
                column=1,
                row=row_idx,
                columnspan=entry_box_column_span,
                sticky="we",
                ipady=5,
            )
            entry_box_container.grid_columnconfigure(0, weight=1)
            entry_box_container.grid_rowconfigure(0, weight=1)

            # Render Error
            row_idx += 1
            entry_error = tool.create_label(
                self, title="", font_size=12, text_color=TEXT["error"]
            )
            entry_error.grid(
                column=1,
                row=row_idx,
                sticky="w",
                columnspan=3,
                pady=(0, 8),
                padx=(2, 0),
            )
            self.__entries[key] = (entry_box, entry_error)

        save_button = tool.create_button(
            self, command=self.__save_account, title="Save to Vault"
        )
        save_button.grid(column=1, columnspan=2, row=row_idx + 1, pady=(20, 0))

        self.grid_columnconfigure(1, weight=1)

    def __save_account(self) -> None:
        is_valid = True
        data = {}
        for key, item in self.__entries.items():
            input_entry, input_error = item
            value = input_entry.get().strip()
            # Validation
            if isinstance(input_entry, ctk.CTkEntry):
                if len(value) < USER_OPTIONS["new"]["inputs"][key]["min_len"]:
                    is_valid = False
                    error_msg = USER_OPTIONS["new"]["inputs"][key]["error"]
                    if isinstance(input_error, ctk.CTkLabel):
                        input_error.configure(text=error_msg)
                else:
                    if isinstance(input_error, ctk.CTkLabel):
                        input_error.configure(text="")
            # Initialise empty value to URL
            if key == "url" and len(value) == 0:
                value = " "
            data[str(key).title()] = value
        if not is_valid:
            return
        # Get the current Date Time
        data["Last Modified"] = tool.current_datetime()
        data["UUID"] = uuid.uuid4()
        # Add data
        success = DataStore.add_account(data)
        if success:
            self.__refresh_table()
            self.close_window()
        else:
            # Failed to save data
            error_msg = USER_OPTIONS["new"]["inputs"]["account"]["save_failed"]
            unknown_error = self.__entries["account"][1]
            if isinstance(unknown_error, ctk.CTkLabel):
                unknown_error.configure(text=error_msg)

    def __toggle_password(self, entry: ctk.CTkEntry, button: ctk.CTkButton) -> None:
        if entry.cget("show") == "":
            entry.configure(show="*")
            button.configure(image=self.__password_hide_ico)
        else:
            entry.configure(show="")
            button.configure(image=self.__password_show_ico)

    def __generate_password(self) -> None:
        # Generates a random password
        new_password = tool.generate_password()
        entry, error = self.__entries.get("password", None)
        if isinstance(entry, ctk.CTkEntry) and isinstance(error, ctk.CTkLabel):
            entry.delete(0, "end")
            entry.insert(0, new_password)
            error.configure(text="")
