import pyperclip
from typing import Callable

import utility.toolkit as tool
from components.top_level import TopLevel
from components.data_store import DataStore
from utility.constants import *


class Account(TopLevel):

    __KEY = "account-details"

    def __init__(self, parent, index: int, refresh: Callable) -> None:
        super().__init__(parent, key=self.__KEY)
        self.__df_index = index
        self.__df = DataStore.account_df.iloc[self.__df_index].dropna()
        self.__entries = {}
        self.__refresh_table = refresh
        self.__content()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def __content(self) -> None:
        container = tool.create_container(self)
        container.grid(column=0, row=1, sticky="news")
        container.grid_columnconfigure(0, weight=1)

        row_count = 0
        for idx, (name, value) in enumerate(self.__df.items()):
            item = ACCOUNT_EDIT[str(name)]
            item_container = tool.create_container(container)
            label = tool.create_label(
                item_container,
                title=f'{item["title"]}:',
                width=160,
                font_size=13,
            )
            label.grid(column=0, row=0, sticky="w")
            gap_y = (0, 8)
            if not item["editable"]:
                non_editable_field = tool.create_label(
                    item_container,
                    title=str(value),
                    font_size=12,
                    font_weight="bold",
                )
                non_editable_field.grid(
                    column=1,
                    row=0,
                    sticky="we",
                    columnspan=2,
                    padx=(3, 0),
                )
                gap_y = (0, 20)
            else:
                editable_field = tool.create_entry(
                    item_container,
                    value=value.strip(),
                    placeholder=item["placeholder"],
                )
                editable_field.grid(column=1, row=0, sticky="we")

                copy_btn = tool.create_button(
                    item_container,
                    command=lambda text=str(value): self.__copy_to_clipboard(text),
                    width=20,
                    title="",
                    icon=tool.ctk_image("copy", (15, 15)),
                    bg=BUTTON["bg-light"],
                    hover_bg=BUTTON["hover-bg-l"],
                )
                copy_btn.grid(column=2, row=0, sticky="we", padx=(8, 0))

                error_field = tool.create_label(
                    item_container,
                    text_color=TEXT["error"],
                    title="",
                    font_size=12,
                )
                error_field.grid(column=1, row=1, sticky="we")
                self.__entries[str(name)] = (editable_field, error_field)

            item_container.grid(column=0, row=idx, sticky="we", pady=gap_y)
            item_container.grid_columnconfigure(1, weight=1)
            row_count += 1

        btn_container = tool.create_container(container)
        btn_container.grid(column=0, row=row_count, sticky="we", pady=(25, 0))
        btn_container.grid_columnconfigure(0, weight=1, uniform="account_btn")
        btn_container.grid_columnconfigure(1, weight=1, uniform="account_btn")

        delete_btn = tool.create_button(
            btn_container,
            self.__delete_account,
            title="Delete",
            text_color=TEXT["bg"],
            bg=TEXT["error"],
            hover_bg=TEXT["error_light"],
        )
        delete_btn.grid(column=0, row=0, sticky="e", padx=(0, 20))

        save_btn = tool.create_button(btn_container, self.__save_account, title="Save")
        save_btn.grid(column=1, row=0, sticky="w", padx=(20, 0))

    def __copy_to_clipboard(self, text: str) -> None:
        """
        Copy text to clipboard
        Args:
            text (str): Text to copy
        """
        pyperclip.copy(text)

    def __delete_account(self) -> bool:
        # TODO
        return True

    def __save_account(self) -> bool:
        # TODO
        self.__refresh_table()
        return True
