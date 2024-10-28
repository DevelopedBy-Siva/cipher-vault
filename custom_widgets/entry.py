import customtkinter as ctk

from utility.constants import TEXT


class Entry(ctk.CTkEntry):

    def __init__(self, master, **kwargs):
        """
        Custom Entry Widget
        """
        placeholder = kwargs.get("placeholder", "Enter input...")
        height = kwargs.get("height", 35)
        show = kwargs.get("show", "")
        value = kwargs.get("value", None)
        width = kwargs.get("width", 0)
        text_variable = kwargs.get("text_variable", None)
        text_color = kwargs.get("text_color", TEXT["dark"])

        border = kwargs.get("border", True)
        border_width = 0
        border_color = TEXT["bg"]
        if border:
            border_width = 1
            border_color = TEXT["border"]

        # Configure widget
        super().__init__(master)
        self.configure(
            bg_color=TEXT["bg"],
            fg_color=TEXT["bg"],
            border_color=border_color,
            border_width=border_width,
            text_color=text_color,
            placeholder_text=placeholder,
            placeholder_text_color=TEXT["light"],
            height=height,
            show=show,
            width=width,
            textvariable=text_variable,
        )

        if value:
            self.insert(0, value)
