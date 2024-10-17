import customtkinter as ctk
import pandas as pd

import toolkit as tool
from constants import *


class AccountTable:

    __DATA_COLUMNS = ("Account", "Username", "Last Modified")

    def __init__(self, master: ctk.CTkFrame) -> None:
        self.__master = master
        self.__create_columns()
        self.__create_rows()

    def __create_columns(self) -> None:
        column_wrapper = tool.create_container(self.__master, bg=BUTTON["bg-light"])
        column_wrapper.grid(column=0, row=0, sticky="we", pady=(0, 5), ipady=2)
        column_wrapper.grid_rowconfigure(0, weight=1)
        container = tool.create_container(
            column_wrapper, fg=BUTTON["bg-light"], bg=BUTTON["bg-light"]
        )
        container.grid(column=0, row=0, padx=(4, 15), sticky="we")
        for idx, col in enumerate(self.__DATA_COLUMNS):
            column = tool.create_label(
                container, title=col, font_size=12, bg="transparent", width=200
            )
            column.grid(column=idx, row=0, sticky="w", pady=12, padx=(15, 0))
            container.grid_columnconfigure(idx, weight=1)
        column_wrapper.grid_columnconfigure(0, weight=1)

    def __create_rows(self) -> None:
        scrollable_container = ctk.CTkScrollableFrame(
            self.__master,
            bg_color="transparent",
            fg_color="transparent",
            scrollbar_fg_color=TEXT["bg"],
            scrollbar_button_color=TEXT["border-light"],
            scrollbar_button_hover_color=TEXT["border-light-hover"],
        )
        scrollable_container.grid(row=1, column=0, sticky="nsew")

        scrollable_container.grid_columnconfigure(0, weight=1)
        scrollable_container.grid_rowconfigure(1, weight=1)
        # Retrieve and render data
        data_frame = pd.read_csv(DATA_PATH)
        for col_no, row in data_frame.iterrows():
            each_row_container = tool.create_container(
                scrollable_container, bg="transparent"
            )
            each_row_container.grid(column=0, row=col_no, sticky="ew", padx=(0, 0))
            for idx, col_name in enumerate(self.__DATA_COLUMNS):
                data_column = tool.create_label(
                    each_row_container,
                    title=row[col_name].title(),
                    font_size=12,
                    bg="transparent",
                    width=200,
                )
                data_column.grid(column=idx, row=0, sticky="w", ipady=15, padx=(15, 0))
                each_row_container.grid_columnconfigure(idx, weight=1)
            self.__draw_border_bottom(each_row_container)

    def __draw_border_bottom(self, master: ctk.CTkFrame) -> None:
        bottom_border = tool.create_container(master, bg=TEXT["border-light"], height=1)
        bottom_border.grid(
            column=0, row=1, columnspan=len(self.__DATA_COLUMNS), sticky="we"
        )

    def retrieve_data(self) -> pd.DataFrame:
        data_frame = pd.read_csv(DATA_PATH)
        return data_frame
