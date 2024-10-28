import random
import string
import hashlib
import base64
import io
import os
import pandas as pd
import configparser as parser
import cryptography.fernet as crypto
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
