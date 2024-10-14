from customtkinter import *
from tkinter import Scrollbar

import toolkit as tool
from constants import *

_DATA_COLUMNS = ("Account", "Username", "Last Modified")


class AccountTable:
    def __init__(self, master: CTkFrame) -> None:
        self.__master = master
        self.__create_columns()
        self.__create_rows()

    def __create_columns(self) -> None:
        frame = tool.create_container(self.__master, bg=BUTTON["bg-light"])
        for idx, col in enumerate(_DATA_COLUMNS):
            column = tool.create_label(frame, title=col, font_size=12, bg="transparent")
            column.grid(column=idx, row=0, sticky="nsew", pady=12, padx=(12, 0))
            frame.grid_columnconfigure(idx, weight=1)
        frame.grid(column=0, row=0, sticky="we", pady=(0, 5))

    def __create_rows(self) -> None:
        scrollable_container = tool.create_container(self.__master, bg="transparent")
        scrollable_container.grid(row=1, column=0, sticky="nsew")

        scrollable_container.grid_columnconfigure(0, weight=1)
        scrollable_container.grid_rowconfigure(1, weight=1)

        for i in range(3):
            each_row = tool.create_container(scrollable_container, bg="red", height=50)
            each_row.grid(column=0, row=i, sticky="ew")
            for idx in range(0, 3):
                data_column = tool.create_label(
                    each_row,
                    title=f"    Row {i+1} Col {idx+1}",
                    font_size=12,
                )
                data_column.grid(column=idx, row=0, sticky="we", ipady=15)
                each_row.grid_columnconfigure(idx, weight=1)
            self.__draw_border_bottom(each_row)

    def __draw_border_bottom(self, master: CTkFrame) -> None:
        bottom_border = tool.create_container(master, bg=TEXT["border-light"], height=1)
        bottom_border.grid(column=0, row=1, columnspan=len(_DATA_COLUMNS), sticky="we")
