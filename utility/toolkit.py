import random
import string
import hashlib
import base64
import io
import os
import pandas as pd
import configparser as parser
import customtkinter as ctk
import cryptography.fernet as crypto
from PIL import Image
from typing import Union
from datetime import datetime

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
    return datetime.now().strftime("%d %B %Y, %I:%M %p")


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
    font_weight = kwargs.get("font_weight", "normal")
    text_color = kwargs.get("text_color", TEXT["dark"])
    height = kwargs.get("height", 25)
    bg = kwargs.get("bg", TEXT["bg"])
    width = kwargs.get("width", 0)
    justify = kwargs.get("justify", "left")

    label = ctk.CTkLabel(
        master,
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
    text_variable = kwargs.get("text_variable", None)
    text_color = kwargs.get("text_color", TEXT["dark"])

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
        text_color=text_color,
        placeholder_text=placeholder,
        placeholder_text_color=TEXT["light"],
        height=height,
        show=show,
        width=width,
        textvariable=text_variable,
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
        salt = config.get(account, AUTH_FILE["salt"])
        return (account, password, salt)
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
        password = info["password"]
        config[account] = {}
        config[account][AUTH_FILE["hash_key"]] = hash_password(password)
        config[account][AUTH_FILE["salt"]] = generate_salt(password)

        # Check dir exists, else create a new one
        os.makedirs(os.path.dirname(AUTH_FILE["path"]), exist_ok=True)

        # Write to file
        with open(AUTH_FILE["path"], mode="a") as file:
            config.write(file)
        return True
    except Exception:
        return False


def generate_salt(password: str) -> str:
    """
    Generates a random string which is used in encrypting and decrypting data
    """
    salt_len = 32 - len(password)
    characters = string.ascii_lowercase + string.digits
    salt = "".join(random.choices(characters, k=salt_len))
    return salt


def encrypt(key: str, file_name: str, data: pd.DataFrame) -> None:
    """
    Encrypt the data using the key
    """
    try:
        key_bytes = base64.urlsafe_b64encode((key).encode())
        fernet = crypto.Fernet(key_bytes)
        data_byte = data.to_csv(index=False).encode()
        encrypted = fernet.encrypt(data_byte)
        # # writing the encrypted data
        with open(f"data/{file_name}", "wb") as encrypted_file:
            encrypted_file.write(encrypted)
    except Exception as ex:
        raise ex


def decrypt(key: str, file_name: str, encrypted_data=None) -> io.BytesIO:
    """
    Decrypt the data using the key
    """
    try:
        key_bytes = base64.urlsafe_b64encode((key).encode())
        fernet = crypto.Fernet(key_bytes)
        if encrypted_data:
            encrypted = encrypted_data
        else:
            # opening the encrypted file
            with open(f"data/{file_name}", "rb") as enc_file:
                encrypted = enc_file.read()
        # decrypting the file
        decrypted = fernet.decrypt(encrypted)
        return io.BytesIO(decrypted)
    except Exception as ex:
        raise ex
