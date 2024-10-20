import datetime
import random
import string
import hashlib
import configparser as parser
import customtkinter as ctk
from PIL import Image
from typing import Union

from utility.constants import *


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


def create_button(master, command, **kwargs) -> ctk.CTkButton:

    text = kwargs.get("title", "Unknown")
    font_size = kwargs.get("font_size", 12)
    height = kwargs.get("height", 35)
    width = kwargs.get("width", 140)
    bg = kwargs.get("bg", BUTTON["bg"])
    hover_bg = kwargs.get("hover_bg", BUTTON["hover-bg"])
    text_color = kwargs.get("text_color", BUTTON["color"])
    icon = kwargs.get("icon", None)

    button = ctk.CTkButton(
        master,
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
    return button


def create_label(master, **kwargs) -> ctk.CTkLabel:

    text = kwargs.get("title", "Unknown")
    font_size = kwargs.get("font_size", 12)
    text_color = kwargs.get("text_color", TEXT["dark"])
    height = kwargs.get("height", 25)
    bg = kwargs.get("bg", TEXT["bg"])
    width = kwargs.get("width", 0)

    label = ctk.CTkLabel(
        master,
        text=text,
        text_color=text_color,
        font=(TEXT["font"], font_size),
        fg_color=bg,
        bg_color=bg,
        anchor="w",
        height=height,
        width=width,
        wraplength=width,
    )
    return label


def create_container(master, **kwargs) -> ctk.CTkFrame:
    bg = kwargs.get("bg", WINDOW["bg"])
    fg = kwargs.get("fg", WINDOW["bg"])
    border_width = kwargs.get("border_width", 0)
    border_color = kwargs.get("border_color", TEXT["bg"])
    height = kwargs.get("height", 0)
    return ctk.CTkFrame(
        master,
        bg_color=fg,
        fg_color=bg,
        border_color=border_color,
        border_width=border_width,
        height=height,
    )


def create_entry(master, **kwargs) -> ctk.CTkEntry:

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

    entry = ctk.CTkEntry(
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


def ctk_image(icon_name: str, size: tuple = (10, 10)) -> ctk.CTkImage:
    icon_img = Image.open(BUTTON["icon"][icon_name])
    icon = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=size)
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


def username_valid(value: str) -> bool:
    valid = True
    for char in value:
        if not (char in string.ascii_letters or char in string.digits or char == " "):
            valid = False
    return valid


def hash_password(password: str) -> str:
    hash_obj = hashlib.sha256(password.encode())
    return hash_obj.hexdigest()


def auth_info(account: str) -> Union[tuple, None]:
    """
    If auth info present, retrieves it
    Returns:
        Union[tuple, None]: Auth data (username, hash password) or None
    """
    try:
        config = parser.ConfigParser()
        config.read(AUTH_FILE["path"])
        password = config.get(account, AUTH_FILE["hash_key"])
        return (account, password)
    except:
        return None


def save_auth_info(info: dict) -> bool:
    """
    Save auth info to file
    Args:
        info (dict): username & password

    Returns:
        bool: True if Success, else False
    """
    try:
        config = parser.ConfigParser()
        account = info["username"]
        config[account] = {}
        config[account][AUTH_FILE["hash_key"]] = info["password"]
        # Write to file
        with open(AUTH_FILE["path"], mode="a") as file:
            config.write(file)
        return True
    except:
        return False
