import pandas as pd
import cryptography.fernet as crypto
from typing import Union

import utility.toolkit as tool

_MODAL = {"Account": [], "Username": [], "Password": [], "Last Modified": []}


class DataStore:

    # User details
    username = ""
    password = ""
    cipher_key = ""
    data_file_name = ""

    # All stored accounts
    account_df = pd.DataFrame(_MODAL)

    @staticmethod
    def initialize_account(username: str, password: str, salt: str) -> None:
        """_summary_
        Store the user data
        """
        DataStore.username = username
        DataStore.password = password
        DataStore.cipher_key = password + salt
        DataStore.data_file_name = f"{username}_{salt}"

    @staticmethod
    def fetch_accounts() -> Union[None, str]:
        """
        Get all saved accounts
        """
        try:
            decrypted_data = tool.decrypt(
                DataStore.cipher_key, DataStore.data_file_name
            )
            data_frame = pd.read_csv(decrypted_data)
            DataStore.account_df = data_frame
        except FileNotFoundError:
            return None
        except crypto.InvalidToken:
            return "Unable to retrieve accounts at the moment.\nThis may be due to mismatched account credentials or possible file corruption. Please restart the application and try again."
        except Exception:
            return "Something went wrong. Please restart the application and try again."
