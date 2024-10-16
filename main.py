import customtkinter as ctk

import toolkit as tool
from auth import Authentication
from constants import APP_NAME, WINDOW

# Init the window
root = ctk.CTk()
root.title(APP_NAME)
root.config(background=WINDOW["bg"], padx=50, pady=30)

# Set the position and dimensions of the window
dimension, width, height = tool.screen_size(
    root, width=WINDOW["width"], height=WINDOW["height"]
)
root.geometry(dimension)
root.minsize(width=width, height=height)


# Paint the auth screen
_ = Authentication(root)

root.grid_columnconfigure(0, weight=1)
root.mainloop()
