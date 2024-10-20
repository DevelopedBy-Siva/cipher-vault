import pandas as pd

import utility.toolkit as tool
from utility.constants import DATA_PATH

_MODAL = {"Account": [], "Username": [], "Password": [], "Last Modified": []}


class DataStore:

    # User details
    username = ""
    password = ""
    cipher_key = ""

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

    @staticmethod
    def fetch_accounts() -> None:
        """
        Get all saved accounts
        """
        try:
            data_frame = pd.read_csv(DATA_PATH)
            data_frame["Password"] = data_frame["Password"].apply(
                lambda val: tool.decrypt(DataStore.cipher_key, val)
            )
            DataStore.account_df = data_frame
        except:
            return
