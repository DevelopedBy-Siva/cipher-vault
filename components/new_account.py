import customtkinter as ctk

import utility.toolkit as tool
from utility.constants import *
from components.top_level import TopLevel


class NewPassword(TopLevel):

    __KEY = "new-password"
    __password_hide_ico = tool.ctk_image("password-hide", (16, 16))
    __password_show_ico = tool.ctk_image("password-show", (16, 16))

    def __init__(self, parent) -> None:
        super().__init__(parent, key=self.__KEY, grid_y_size=4)
        self.__entries = {}
        self.__user_input()

    def __user_input(self) -> None:

        self.grid_columnconfigure(1, weight=1)

        for idx, entry in enumerate(USER_OPTIONS["new"]["inputs"]):
            row_idx = idx + 1
            gap_y = (0, 30)
            show = entry.get("show", "")

            entry_label = tool.create_label(
                self, title=f'{entry["title"]}:', font_size=13
            )
            entry_label.grid(
                column=0, row=row_idx, pady=gap_y, sticky="w", padx=(0, 25)
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
            self.__entries[entry["key"]] = entry_box
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
                generate_button.grid(column=3, row=row_idx, pady=gap_y, padx=(15, 0))
                entry_box_column_span = 1

            entry_box_container.grid(
                column=1,
                row=row_idx,
                columnspan=entry_box_column_span,
                sticky="we",
                pady=gap_y,
                ipady=5,
            )
            entry_box_container.grid_columnconfigure(0, weight=1)
            entry_box_container.grid_rowconfigure(0, weight=1)

        save_button = tool.create_button(
            self, command=self.__save_account, title="Save to Vault"
        )
        save_button.grid(column=1, columnspan=2, row=5, pady=(20, 0))

        self.grid_columnconfigure(1, weight=1)

    def __save_account(self) -> None:
        is_valid = True
        data = {}
        for key, entry in self.__entries.items():
            value = entry.get().strip()
            # Validation
            if key != "url" and isinstance(entry, ctk.CTkEntry):
                if len(value) == 0:
                    is_valid = False
            data[key] = value
        if not is_valid:
            return
        self.close_window()

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
        entry = self.__entries.get("password", None)
        if isinstance(entry, ctk.CTkEntry):
            entry.delete(0, "end")
            entry.insert(0, new_password)
