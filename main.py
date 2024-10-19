import customtkinter as ctk

import utility.toolkit as tool
from components.auth import Authentication
from utility.constants import APP_NAME, WINDOW


def main():
    # Init the window
    root = ctk.CTk()
    root.title(APP_NAME)
    root.config(background=WINDOW["bg"])

    # Set the position and dimensions of the window
    dimension, width, height = tool.screen_size(
        root, width=WINDOW["width"], height=WINDOW["height"]
    )
    root.geometry(dimension)
    root.minsize(width=width, height=height)

    # Paint the auth screen
    _ = Authentication(root)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()


if __name__ == "__main__":
    main()
