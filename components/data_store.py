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
            new_data = {}
            for key, val in data.items():
                new_data[key] = [val]
            new_df = pd.DataFrame(new_data)
            temp_df = pd.concat([DataStore.account_df, new_df])

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
            columns_to_update = []
            updated_values = []
            for key, val in data.items():
                columns_to_update.append(key)
                updated_values.append(val)

            temp_df = DataStore.account_df.copy()
            temp_df.loc[temp_df[temp_df["UUID"] == id].index, columns_to_update] = (
                updated_values
            )

            tool.encrypt(DataStore.cipher_key, DataStore.data_file_name, temp_df)
            DataStore.account_df = temp_df
            return True
        except:
            return False

    @staticmethod
    def delete_account(id: str) -> bool:
        try:
            temp_df = DataStore.account_df.copy()
            # Delete the row
            temp_df = temp_df.drop(temp_df[temp_df["UUID"] == id].index)
            # Encrypt and store DataFrame after removing data
            tool.encrypt(DataStore.cipher_key, DataStore.data_file_name, temp_df)
            DataStore.account_df = temp_df
            return True
        except:
            return False

    @staticmethod
    def select_and_sort(ascending=False) -> pd.DataFrame:
        df = DataStore.account_df.sort_values(
            by=["Last Modified"], ascending=ascending, ignore_index=True
        )
        return df

    @staticmethod
    def merge_datastore(new_datastore: pd.DataFrame) -> None:
        DataStore.account_df = pd.concat([DataStore.account_df, new_datastore])
        DataStore.account_df.reset_index(drop=True, inplace=True)
        tool.encrypt(
            DataStore.cipher_key, DataStore.data_file_name, DataStore.account_df
        )
