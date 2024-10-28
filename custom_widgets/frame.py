import customtkinter as ctk

from utility.constants import WINDOW, TEXT


class Frame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        """
        Custom Entry Widget
        """

        bg = kwargs.get("bg", WINDOW["bg"])
        fg = kwargs.get("fg", WINDOW["bg"])
        border_width = kwargs.get("border_width", 0)
        border_color = kwargs.get("border_color", TEXT["bg"])
        height = kwargs.get("height", 0)

        # Configure widget
        super().__init__(master)
        self.configure(
            bg_color=fg,
            fg_color=bg,
            border_color=border_color,
            border_width=border_width,
            height=height,
        )
