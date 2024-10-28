import customtkinter as ctk

from utility.constants import TEXT


class Label(ctk.CTkLabel):

    def __init__(self, master, **kwargs):
        """
        Custom Label Widget
        """

        text = kwargs.get("title", "Unknown")
        font_size = kwargs.get("font_size", 12)
        font_weight = kwargs.get("font_weight", "normal")
        text_color = kwargs.get("text_color", TEXT["dark"])
        height = kwargs.get("height", 25)
        bg = kwargs.get("bg", TEXT["bg"])
        width = kwargs.get("width", 0)
        justify = kwargs.get("justify", "left")

        # Configure widget
        super().__init__(master)
        self.configure(
            text=text,
            text_color=text_color,
            font=(TEXT["font"], font_size, font_weight),
            fg_color=bg,
            bg_color=bg,
            anchor="w",
            height=height,
            width=width,
            wraplength=width,
            justify=justify,
        )
