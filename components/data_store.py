import pandas as pd
import cryptography.fernet as crypto
from typing import Union

import utility.toolkit as tool

_MODAL = {
    "Account": [],
    "Username": [],
    "Url": [],
    "Password": [],
    "Last Modified": [],
    "Imported On": [],
}


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
        DataStore.data_file_name = f"{username}__{salt}__.bytes"

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
            DataStore.account_df = data_frame.sort_values(
                by=["Last Modified"], ascending=False
            )

        except FileNotFoundError:
            return None
        except crypto.InvalidToken:
            return "Unable to retrieve accounts at the moment.\nThis may be due to mismatched account credentials or possible file corruption. Please restart the application and try again."
        except Exception:
            return "Something went wrong. Please restart the application and try again."

    @staticmethod
    def add_account(data: dict) -> bool:
        """
        Add new account to the vault
        Args:
            data (dict): Data to add
        Returns:
            bool: True when success, else False
        """
        try:
            new_data = {}
            for key, val in data.items():
                new_data[key] = [val]
            new_df = pd.DataFrame(new_data)
            DataStore.account_df = pd.concat([DataStore.account_df, new_df])
            DataStore.account_df.reset_index(drop=True, inplace=True)
            tool.encrypt(
                DataStore.cipher_key, DataStore.data_file_name, DataStore.account_df
            )
            return True
        except:
            return False

    @staticmethod
    def select_and_sort(columns: list, ascending=False) -> pd.DataFrame:
        df = DataStore.account_df[columns].sort_values(
            by=["Last Modified"], ascending=ascending
        )
        return df

    @staticmethod
    def merge_datastore(new_datastore: pd.DataFrame) -> None:
        DataStore.account_df = pd.concat([DataStore.account_df, new_datastore])
        DataStore.account_df.reset_index(drop=True, inplace=True)
        tool.encrypt(
            DataStore.cipher_key, DataStore.data_file_name, DataStore.account_df
        )
