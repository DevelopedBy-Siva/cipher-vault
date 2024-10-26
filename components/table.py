import customtkinter as ctk
import pandas as pd

import utility.toolkit as tool
from utility.constants import *
from components.account import Account
from components.data_store import DataStore


class Table(ctk.CTkFrame):

    __DATA_COLUMNS = ("Account", "Username", "Last Modified")

    def __init__(self, root: ctk.CTk, parent):
        self.__root = root
        self.__parent = parent
        self.__content_container = None
        super().__init__(self.__parent, fg_color=WINDOW["bg"], bg_color=WINDOW["bg"])
        self.__render_data()  # render rows and columns
        self.grid(column=0, row=0, sticky="news")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def __render_data(self):
        """
        Render rows and columns
        """
        # column names
        self.__heading()
        # Fetch Data
        error = DataStore.fetch_accounts()
        if not error:
            self.__content()
        else:
            self.__notify(error)

    def __heading(self) -> None:
        """
        Table columns
        """
        column_wrapper = tool.create_container(self, bg=BUTTON["bg-light"])
        column_wrapper.grid(column=0, row=0, sticky="we", pady=(0, 5), ipady=2)
        column_wrapper.grid_rowconfigure(0, weight=1)
        container = tool.create_container(
            column_wrapper, fg=BUTTON["bg-light"], bg=BUTTON["bg-light"]
        )
        container.grid(column=0, row=0, padx=(5, 110), sticky="we")
        for idx, col in enumerate(self.__DATA_COLUMNS):
            column = tool.create_label(
                container, title=col, font_size=12, bg="transparent"
            )
            column.grid(column=idx, row=0, sticky="we", pady=12, padx=(15, 0))
            container.grid_columnconfigure(idx, weight=1, uniform="header")

        column_wrapper.grid_columnconfigure(0, weight=1)

    def __content(self) -> None:
        """
        Table rows
        """
        # If vault is empty, display message
        if DataStore.account_df.size == 0:
            self.__notify("No accounts stored in your vault.")
            return

        self.__content_container = ctk.CTkScrollableFrame(
            self,
            bg_color="transparent",
            fg_color="transparent",
            scrollbar_fg_color=TEXT["bg"],
            scrollbar_button_color=TEXT["border-light"],
            scrollbar_button_hover_color=TEXT["border-light-hover"],
        )
        self.__content_container.grid(row=1, column=0, sticky="nsew")
        self.__content_container.grid_columnconfigure(0, weight=1)
        self.__content_container.grid_rowconfigure(1, weight=1)

        # Filter and render data
        data_frame = DataStore.select_and_sort()
        for row_no, (_, row) in enumerate(data_frame.iterrows()):
            each_row_container = tool.create_container(
                self.__content_container, bg="transparent"
            )
            each_row_container.grid(column=0, row=row_no, sticky="ew")
            # Render each row
            for idx, col_name in enumerate(self.__DATA_COLUMNS):

                col_value = str(row[col_name]).capitalize()
                data_column = tool.create_label(
                    each_row_container,
                    title=col_value,
                    font_size=12,
                    bg="transparent",
                )
                data_column.grid(column=idx, row=0, sticky="we", padx=(15, 0), ipady=20)
                each_row_container.grid_columnconfigure(
                    idx, weight=1, uniform="content"
                )

            # open button for each row
            open_btn = tool.create_button(
                each_row_container,
                title="",
                width=30,
                bg=BUTTON["color"],
                hover_bg=BUTTON["color"],
                icon=tool.ctk_image("open", (18, 18)),
                command=lambda data=row: self.__open_account(data),
            )
            open_btn.grid(column=3, row=0, sticky="e", padx=(20, 40))
            # Draw a border line after every row
            self.__draw_border_bottom(each_row_container)

    def __notify(self, msg) -> None:
        """
        Render message (if any)
        """
        error = tool.create_label(self, title=msg, text_color=TEXT["light"])
        error.grid(column=0, row=1, sticky="n", pady=(25, 0))

    def refresh(self) -> None:
        """
        Refresh table content
        """
        if self.__content_container:
            self.__content_container.destroy()
        self.__content()

    def __draw_border_bottom(self, master: ctk.CTkFrame) -> None:
        """
        Creates a border that act as a row separator
        """
        bottom_border = tool.create_container(master, bg=TEXT["border-light"], height=1)
        bottom_border.grid(
            column=0, row=1, columnspan=len(self.__DATA_COLUMNS) + 1, sticky="we"
        )

    def __open_account(self, data: pd.Series) -> None:
        """_summary_
        Render the account details when a selection is made
        """
        Account(self.__root, data, self.refresh)
