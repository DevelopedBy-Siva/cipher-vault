import customtkinter as ctk

import utility.toolkit as tool
from custom_widgets.frame import Frame
from custom_widgets.label import Label
from utility.constants import WINDOW, TEXT


class TopLevel(ctk.CTkToplevel):

    def __init__(self, master: ctk.CTk, key: str, **kwargs) -> None:
        """
        CustomTKinter TopLevel component extension
        Args:
            master (CTk): Root window
            key (str): Modal window identifier
            m_heading (str): Modal window main heading
            s_heading (str): Modal window sub heading
        """
        self.__parent = master
        self.__key = key
        super().__init__(self.__parent)

        # Set the position and dimensions of the window
        dimension, width, height = tool.screen_size(
            self, WINDOW[key]["width"], WINDOW[key]["height"]
        )
        self.geometry(dimension)
        self.minsize(width=width, height=height)
        self.resizable(False, False)

        self.title(WINDOW[key]["title"])
        self.config(background=WINDOW["bg"], padx=40, pady=40)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Column span size
        self.__grid_y_size = kwargs.get("grid_y_size", 2)

        # Activate only modal
        self.transient(self.__parent)
        self.grab_set()
        self.focus_set()

        # Create header and subheading wrapper
        self.__create_header()

    def __create_header(self) -> None:
        """
        Create the heading component
        """
        label_container = Frame(self)
        label_container.grid(
            column=0, row=0, columnspan=self.__grid_y_size, sticky="w", pady=(0, 40)
        )

        heading = Label(
            label_container,
            title=WINDOW[self.__key]["heading"],
            text_color=TEXT["dark"],
            font_size=18,
        )
        heading.grid(column=0, row=0, sticky="w")

        subheading = Label(
            label_container,
            title=WINDOW[self.__key]["desc"],
            text_color=TEXT["light"],
            height=18,
        )
        subheading.grid(column=0, row=1, sticky="w")

    def close_window(self) -> None:
        """
        Close window
        """
        self.grab_release()
        self.master.focus_set()
        self.destroy()
