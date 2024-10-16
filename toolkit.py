import datetime
import random
import string
from customtkinter import *
from PIL import Image

from constants import *


def screen_size(window, width: int, height: int):

    # width & height of the screen
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    w = width
    h = height

    # x and y coordinates for the window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # Screen dimension and position
    screen_dp = "%dx%d+%d+%d" % (w, h, x, y)

    return (screen_dp, w, h)


def current_datetime() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_button(master, command, **kwargs) -> CTkButton:

    text = kwargs.get("title", "Unknown")
    font_size = kwargs.get("font_size", 12)
    height = kwargs.get("height", 35)
    width = kwargs.get("width", 140)
    bg = kwargs.get("bg", BUTTON["bg"])
    hover_bg = kwargs.get("hover_bg", BUTTON["hover-bg"])
    text_color = kwargs.get("text_color", BUTTON["color"])
    icon = kwargs.get("icon", None)

    button = CTkButton(
        master,
        text=text.title(),
        font=(TEXT["font"], font_size),
        fg_color=bg,
        bg_color=TEXT["bg"],
        hover_color=hover_bg,
        text_color=text_color,
        height=height,
        image=icon,
        state=NORMAL,
        anchor="center",
        command=command,
        width=width,
    )
    return button


def create_label(master, **kwargs) -> CTkLabel:

    text = kwargs.get("title", "Unknown")
    font_size = kwargs.get("font_size", 12)
    text_color = kwargs.get("text_color", TEXT["dark"])
    height = kwargs.get("height", 25)
    bg = kwargs.get("bg", TEXT["bg"])

    label = CTkLabel(
        master,
        text=text,
        text_color=text_color,
        font=(TEXT["font"], font_size),
        fg_color=bg,
        bg_color=bg,
        anchor="w",
        height=height,
        width=100,
    )
    return label


def create_container(master, **kwargs) -> CTkFrame:
    bg = kwargs.get("bg", WINDOW["bg"])
    border_width = kwargs.get("border_width", 0)
    border_color = kwargs.get("border_color", TEXT["bg"])
    height = kwargs.get("height", 0)
    return CTkFrame(
        master,
        bg_color=WINDOW["bg"],
        fg_color=bg,
        border_color=border_color,
        border_width=border_width,
        height=height,
    )


def create_entry(master, **kwargs) -> CTkEntry:

    placeholder = kwargs.get("placeholder", "Enter input...")
    height = kwargs.get("height", 35)
    show = kwargs.get("show", "")
    value = kwargs.get("value", None)
    width = kwargs.get("width", 0)

    border = kwargs.get("border", True)
    border_width = 0
    border_color = TEXT["bg"]
    if border:
        border_width = 1
        border_color = TEXT["border"]

    entry = CTkEntry(
        master,
        bg_color=TEXT["bg"],
        fg_color=TEXT["bg"],
        border_color=border_color,
        border_width=border_width,
        text_color=TEXT["dark"],
        placeholder_text=placeholder,
        placeholder_text_color=TEXT["light"],
        height=height,
        show=show,
        width=width,
    )
    if value:
        entry.insert(0, value)
    return entry


def ctk_image(icon_name: str, size: tuple = (10, 10)) -> CTkImage:
    icon_img = Image.open(BUTTON["icon"][icon_name])
    icon = CTkImage(light_image=icon_img, dark_image=icon_img, size=size)
    return icon


def generate_password() -> str:
    rules = (
        string.ascii_lowercase,
        string.ascii_uppercase,
        range(0, 10),
        ("!", "#", "$", "%", "&", "(", ")", "*", "+"),
    )
    new_password = ""
    # Make sure a character is generated from each rule
    for rule in rules:
        new_password += str(random.choice(rule))
    # Generate random characters
    for _ in range(0, GEN_PASS_LENGTH - len(new_password)):
        rule = random.choice(rules)
        new_password += str(random.choice(rule))

    # Shuffle the letters
    new_password = list(new_password)
    random.shuffle(new_password)
    new_password = "".join(new_password)
    return new_password
