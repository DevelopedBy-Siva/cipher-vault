import customtkinter as ctk

from utility.constants import BUTTON, TEXT


class Button(ctk.CTkButton):

    def __init__(self, master, command, **kwargs):
        """
        Custom Button Widget
        """
        text = kwargs.get("title", "Unknown")
        font_size = kwargs.get("font_size", 12)
        height = kwargs.get("height", 35)
        width = kwargs.get("width", 140)
        bg = kwargs.get("bg", BUTTON["bg"])
        hover_bg = kwargs.get("hover_bg", BUTTON["hover-bg"])
        text_color = kwargs.get("text_color", BUTTON["color"])
        icon = kwargs.get("icon", None)

        # Configure widget
        super().__init__(master)
        self.configure(
            text=text.title(),
            font=(TEXT["font"], font_size),
            fg_color=bg,
            bg_color=TEXT["bg"],
            hover_color=hover_bg,
            text_color=text_color,
            height=height,
            image=icon,
            state="normal",
            anchor="center",
            command=command,
            width=width,
        )
