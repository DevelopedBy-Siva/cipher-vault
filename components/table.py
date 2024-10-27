import customtkinter as ctk
import pandas as pd

import utility.toolkit as tool
from utility.constants import *
from components.account import Account
from components.data_store import DataStore

_DATA_COLUMNS = ("Account", "Username", "Last Modified")


class Table(ctk.CTkFrame):

    show_search_placeholder = True

    def __init__(self, root: ctk.CTk, parent, search_var: ctk.StringVar):
        self.__root = root
        self.__parent = parent
        self.__content_container = None
        super().__init__(self.__parent, fg_color=WINDOW["bg"], bg_color=WINDOW["bg"])
        # Handle search
        self.__search = self.__bind_search(search_var)
        # render rows and columns
        self.__render_data()

        self.grid(column=0, row=0, sticky="news")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def __bind_search(self, search_var: ctk.StringVar):
        """
        Bind and handle user search
        Args:
            search_var (ctk.StringVar): Search variable to detect on change event
        """

        def handle_search(sv: ctk.StringVar):
            if not Table.show_search_placeholder:
                search = sv.get().strip().lower()
                print(search)
                if search != self.__search:
                    self.__search = search
                    self.refresh()

        search_var.trace_add("write", lambda i, j, k, sv=search_var: handle_search(sv))
        return ""

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
        for idx, col in enumerate(_DATA_COLUMNS):
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
            self.__notify("Nothing here yet! Add some accounts to get started.")
            return

        # Filter and render data
        data_frame = DataStore.select_and_sort(search=self.__search)
        if data_frame.size == 0:
            self.__notify(
                f"Hmm... couldn’t find '{self.__search}' in your vault. Time to add it?"
            )
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

        for row_no, (_, row) in enumerate(data_frame.iterrows()):
            each_row_container = tool.create_container(
                self.__content_container, bg="transparent"
            )
            each_row_container.grid(column=0, row=row_no, sticky="ew")
            # Render each row
            for idx, col_name in enumerate(_DATA_COLUMNS):

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
            column=0, row=1, columnspan=len(_DATA_COLUMNS) + 1, sticky="we"
        )

    def __open_account(self, data: pd.Series) -> None:
        """_summary_
        Render the account details when a selection is made
        """
        Account(self.__root, data, self.refresh)
