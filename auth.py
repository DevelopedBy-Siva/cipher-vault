import os
from typing import Union
from customtkinter import *

from constants import *
import toolkit as tool
import home


class Authentication(CTkFrame):

    def __init__(self, root: CTk) -> None:
        super().__init__(root, bg_color=WINDOW["bg"], fg_color=WINDOW["bg"])
        self.__root = root
        self.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.__entries = {}
        self.__paint_ui()

    def __paint_ui(self) -> None:
        """
        Create the auth screen
        """
        title = tool.create_label(self, title="Access Your Secure Vault", font_size=32)
        title.grid(column=0, row=0, columnspan=2)
        description = tool.create_label(
            self,
            title="Access your vault with CipherVault credentials or create a new\naccount in seconds. Your data is encrypted and stored locally,\n so make sure to back it up before creating a new account, as\nthis will replace any existing vault.",
            text_color=TEXT["light"],
        )
        description.grid(column=0, row=1, pady=(10, 20), columnspan=2)

        row = 1
        for key, value in AUTH_FIELDS.items():
            row += 1
            entry_label = tool.create_label(self, title=value["title"], font_size=13)
            entry_label.grid(column=0, row=row, sticky="w", pady=(2, 2), columnspan=2)

            row += 1
            entry = tool.create_entry(
                self,
                width=365,
                height=40,
                placeholder=value["placeholder"],
                show=value["show"],
            )
            entry.grid(column=0, row=row, sticky="w", columnspan=2)

            row += 1
            entry_error = tool.create_label(
                self,
                title="",
                font_size=12,
                text_color=TEXT["error"],
            )
            entry_error.grid(column=0, row=row, sticky="w", padx=(2, 0), columnspan=2)

            self.__entries[key] = (entry, entry_error)

        row += 1
        new_account_btn = tool.create_button(
            self, command=lambda: self.__submit(True), title="Create Account"
        )
        new_account_btn.grid(column=0, row=row, sticky="w", pady=(20, 5))

        login_btn = tool.create_button(
            self, command=self.__submit, title="Unlock Vault"
        )
        login_btn.grid(column=1, row=row, sticky="e", pady=(20, 5))

    def __submit(self, new_account: bool = False) -> None:
        """_summary_
        Create or validate login and redirect to 'Home'
        Args:
            new_account (bool, optional): Creates new account if 'True', else login. Defaults to False.
        """
        account_data = {
            key: entry[0].get().strip() for key, entry in self.__entries.items()
        }
        # Input details validation
        if not self.__input_valid(account_data):
            return

        account_data["username"] = account_data["username"].lower()
        # Login
        if not new_account:
            # Check account is present
            if self.__env_data("username") == account_data["username"]:
                # validate password
                if self.__env_data("username") != account_data["password"]:
                    error_msg = AUTH_FIELDS["password"]["error"]["incorrect"]
                    self.__entries["username"][1].configure(text=error_msg)
                    return
            else:
                error_msg = AUTH_FIELDS["username"]["error"]["404"]
                self.__entries["username"][1].configure(text=error_msg)
                return
        # New account creation
        else:
            # Cannot create if new username matches with previous username
            if self.__env_data("username") == account_data["username"]:
                error_msg = AUTH_FIELDS["username"]["error"]["present"]
                self.__entries["username"][1].configure(text=error_msg)
                return
            # Create Account
            else:
                user_env_name = AUTH_FIELDS["username"]["env"]
                os.environ[user_env_name] = account_data["username"]
                pass_env_name = AUTH_FIELDS["username"]["env"]
                os.environ[pass_env_name] = account_data["password"]
                self.__cleanup()

        self.destroy()  # Destroy the auth widget

        # Change APP window title
        self.__root.title(f"{account_data['username'].title()}'s {APP_NAME}")
        # Create the Home UI
        _ = home.Home(self.__root)
        self.__root.update_idletasks()

    def __env_data(self, key: str) -> Union[str, None]:
        """
        Retrieve env data
        Args:
            key (str): Env variable identifier suffix
        Returns:
            Union[str, None]: Returns env data if found, else returns None
        """
        env_name = AUTH_FIELDS[key]["env"]
        try:
            value = os.environ[env_name]
            return value
        except:
            return None

    def __input_valid(self, data: dict) -> bool:
        """
        Valid user auth input
        Args:
            data (dict): Auth input data which needs to be validated
        Returns:
            bool: returns True if valid, else False
        """
        is_valid = True
        for key, value in data.items():
            if len(value) == 0:
                is_valid = False
                error_msg = AUTH_FIELDS[key]["error"]["empty"]
                self.__entries[key][1].configure(text=error_msg)
            elif (
                len(value) < AUTH_FIELDS[key]["min_len"]
                or len(value) > AUTH_FIELDS[key]["max_len"]
            ):
                is_valid = False
                error_msg = AUTH_FIELDS[key]["error"]["long"]
                self.__entries[key][1].configure(text=error_msg)
            else:
                self.__entries[key][1].configure(text="")
        return is_valid

    def __cleanup(self):
        # TODO
        pass
