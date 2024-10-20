import customtkinter as ctk

import utility.toolkit as tool
from utility.constants import *
from components.home import Home
from components.data_store import DataStore


class Authentication(ctk.CTkFrame):

    def __init__(self, root: ctk.CTk) -> None:
        super().__init__(root, bg_color=WINDOW["bg"], fg_color=WINDOW["bg"])
        self.__root = root
        self.place(relx=0.5, rely=0.5, anchor="center")
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
            title="Access your vault with CipherVault credentials or quickly set up a new account. Your data is encrypted and stored locally.",
            text_color=TEXT["light"],
            width=365,
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
            self,
            command=lambda: self.__submit(True),
            title="Create Account",
            bg=BUTTON["bg-light"],
            hover_bg=BUTTON["hover-bg-l"],
            text_color=TEXT["dark"],
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

        auth_info = tool.auth_info(account_data["username"])
        # Login
        if not new_account:
            # Check account is present
            if auth_info != None and (auth_info[0] == account_data["username"]):
                # validate password
                hashed_password = tool.hash_password(account_data["password"])
                if auth_info[1] != hashed_password:
                    error_msg = AUTH_FIELDS["password"]["error"]["incorrect"]
                    self.__entries["password"][1].configure(text=error_msg)
                    return
            else:
                error_msg = AUTH_FIELDS["username"]["error"]["404"]
                self.__entries["username"][1].configure(text=error_msg)
                return
        # New account creation
        else:
            # Cannot create if new username matches with previous username
            if auth_info != None and (auth_info[0] == account_data["username"]):
                error_msg = AUTH_FIELDS["username"]["error"]["present"]
                self.__entries["username"][1].configure(text=error_msg)
                return
            # Create Account
            else:
                if tool.save_auth_info(account_data):
                    # Account created
                    self.__cleanup()
                else:
                    # Something went wrong while saving files
                    error_msg = AUTH_FIELDS["username"]["error"]["unknown"]
                    self.__entries["username"][1].configure(text=error_msg)
                    return

        # Store user data
        if auth_info:
            DataStore.initialize_account(
                username=auth_info[0],
                password=account_data["password"],
                salt=auth_info[2],
            )

        self.destroy()  # Destroy the auth widget

        # Change APP window title
        self.__root.title(f"{account_data['username'].title()}'s {APP_NAME}")
        # Create the Home UI
        _ = Home(self.__root)
        self.__root.update_idletasks()

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
            elif key == "username" and not tool.username_valid(value):
                is_valid = False
                error_msg = AUTH_FIELDS[key]["error"]["invalid"]
                self.__entries[key][1].configure(text=error_msg)
                pass
            else:
                self.__entries[key][1].configure(text="")
        return is_valid

    def __cleanup(self):
        # TODO
        pass
