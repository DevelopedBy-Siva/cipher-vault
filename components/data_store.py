import pandas as pd
import cryptography.fernet as crypto
from typing import Union

import utility.toolkit as tool

_MODAL = {
    "UUID": [],
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
            DataStore.account_df = pd.read_csv(decrypted_data)
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

            # Remove 'Url' if empty
            url = data.get("Url", None)
            if isinstance(url, str) and len(url.strip()) == 0:
                data.pop("Url")

            # Form new data
            new_data = {key: [data.get(key, float("NAN"))] for key in _MODAL.keys()}

            new_df = pd.DataFrame(new_data)
            temp_df = pd.concat([new_df, DataStore.account_df], ignore_index=True)

            # Initialise 'Url' to empty if it's 'NaN'
            temp_df["Url"] = temp_df["Url"].fillna(" ")

            tool.encrypt(DataStore.cipher_key, DataStore.data_file_name, temp_df)
            DataStore.account_df = temp_df
            return True
        except:
            return False

    @staticmethod
    def update_account(data: dict, id: str) -> bool:
        """
        Update account and save to the vault
        Args:
            data (dict): Data to add
            id (str): unique id of the row
        Returns:
            bool: True when success, else False
        """
        try:

            # Remove 'Url' if empty
            url = data.get("Url", None)
            if isinstance(url, str) and len(url.strip()) == 0:
                data.pop("Url")

            temp_df = DataStore.account_df.copy()
            # Update values
            temp_df.loc[temp_df["UUID"] == id, list(data.keys())] = list(data.values())

            # Initialise Url to empty if it's NaN
            temp_df["Url"] = temp_df["Url"].fillna(" ")

            tool.encrypt(DataStore.cipher_key, DataStore.data_file_name, temp_df)
            DataStore.account_df = temp_df
            return True
        except:
            return False

    @staticmethod
    def delete_account(id: str) -> bool:
        try:
            # Delete the row
            temp_df = DataStore.account_df[DataStore.account_df["UUID"] != id]
            # Encrypt and store DataFrame after removing data
            tool.encrypt(DataStore.cipher_key, DataStore.data_file_name, temp_df)
            DataStore.account_df = temp_df
            return True
        except:
            return False

    @staticmethod
    def select_and_sort(ascending=False, search: str = "") -> pd.DataFrame:
        df = DataStore.account_df.sort_values(
            by=["Last Modified"], ascending=ascending, ignore_index=True
        )
        if df.size:
            df = df.loc[df["Account"].str.contains(search.strip())]
        return df

    @staticmethod
    def merge_datastore(new_datastore: pd.DataFrame) -> None:
        temp_df = pd.concat([DataStore.account_df, new_datastore], ignore_index=True)
        tool.encrypt(DataStore.cipher_key, DataStore.data_file_name, temp_df)
        DataStore.account_df = temp_df
