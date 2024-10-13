from customtkinter import *

import toolkit as tool
from top_level import TopLevel
from constants import *

_KEY = "new-password"
_PASSWORD_HIDE_KEY = "password-hide"
_PASSWORD_SHOW_KEY = "password-show"


class NewPassword(TopLevel):

    def __init__(self, parent) -> None:
        super().__init__(parent, key=_KEY, grid_y_size=4)
        self.__password_hide_ico = tool.ctk_image(_PASSWORD_HIDE_KEY, (16, 16))
        self.__password_show_ico = tool.ctk_image(_PASSWORD_SHOW_KEY, (16, 16))
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
                placeholder_text=entry["placeholder"],
                show=show,
                border=False,
                height=20,
            )
            entry_box.grid(column=0, row=0, sticky="nwse", padx=3, pady=3)
            entry_box_column_span = 3

            if show == "*":
                show_button = tool.create_button(
                    entry_box_container,
                    command=lambda: self.__toggle_password(entry_box, show_button),
                    title="",
                    bg=TEXT["bg"],
                    hover_bg=TEXT["bg"],
                    width=0,
                    height=0,
                    icon=self.__password_hide_ico,
                )
                show_button.grid(
                    column=1,
                    row=0,
                    padx=(0, 3),
                    sticky="e",
                )

            command = entry.get("command", None)
            if isinstance(command, dict):
                generate_button = tool.create_button(
                    self,
                    command=lambda: print("hello"),
                    title=entry["command"]["title"],
                    bg=BUTTON["bg-light"],
                    hover_bg=BUTTON["hover-bg-l"],
                    text_color=TEXT["dark"],
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
            self, command=self.__save_password, title="Save to Vault"
        )
        save_button.grid(column=1, columnspan=2, row=4, pady=(20, 0))

        self.grid_columnconfigure(1, weight=1)

    def __save_password(self):
        self.close_window()

    def __toggle_password(self, entry: CTkEntry, button: CTkButton) -> None:
        if entry.cget("show") == "":
            entry.configure(show="*")
            button.configure(image=self.__password_hide_ico)
        else:
            entry.configure(show="")
            button.configure(image=self.__password_show_ico)
