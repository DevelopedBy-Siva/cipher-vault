import pandas as pd
import customtkinter as ctk
import cryptography.fernet as crypto
from typing import Callable

import utility.toolkit as tool
from components.data_store import DataStore
from components.top_level import TopLevel
from utility.constants import *


class ExportImport(TopLevel):

    __KEY = "export-import"

    def __init__(self, parent, refresh_table: Callable) -> None:
        super().__init__(parent, key=self.__KEY)
        self.__import()
        self.__export()
        self.grid_columnconfigure(0, weight=1)
        self.__temp_vault = None
        self.__refresh_table = refresh_table

    def __import(self) -> None:
        """
        Import block
        """
        self.__import_container = self.__wrapper(
            heading="# Import your vault",
            description="Import a vault from a previous account. To successfully complete the process, you’ll need to enter the password linked to the vault being imported.",
        )
        # Select button
        self.__selection_import_btn = tool.create_button(
            self.__import_container,
            title="Select Vault",
            command=self.__import_file_selection,
        )
        self.__selection_import_btn.grid(column=0, row=2, sticky="w", pady=(15, 0))
        # Import button
        self.__import_btn = tool.create_button(
            self.__import_container, title="Import", command=self.__import_action
        )
        # Password entry
        self.__import_password_entry = tool.create_entry(
            self.__import_container,
            placeholder="Enter the password for the vault you're importing...",
            show="*",
        )
        # Display messages
        self.__import_notify = tool.create_label(
            self.__import_container, title="", text_color=TEXT["error"], width=500
        )
        self.__import_notify.grid(
            column=0, row=3, sticky="we", padx=(3, 0), pady=(5, 0), columnspan=2
        )

        self.__import_container.grid(column=0, row=1, sticky="we")
        self.__import_container.grid_columnconfigure(1, weight=1)

    def __import_file_selection(self) -> None:
        """
        Handle vault file selection
        """
        try:
            filename = ctk.filedialog.askopenfilename(
                title="Select a vault to import",
                defaultextension=".bytes",
                filetypes=[("Bytes files", "*.bytes")],
            )
            if filename:
                # Open Vault
                with open(filename) as file:
                    self.__temp_vault = (self.__filename(filename), file.read())

                # Show password entry box
                self.__import_password_entry.grid(
                    column=1, row=2, sticky="we", pady=(15, 0), padx=(15, 0)
                )
                # Show import button
                self.__import_btn.grid(column=0, row=2, sticky="w", pady=(15, 0))
                # Remove file selection button
                self.__selection_import_btn.grid_remove()
                # Show 1st success message
                self.__import_notify.configure(
                    text=f"'{self.__filename(filename)}' vault is ready to import.\nPlease enter the vault password to initiate import.",
                    text_color=TEXT["success"],
                )
            else:
                self.__import_cleanup()
        except:
            self.__import_cleanup()
            self.__import_notify.configure(
                text="Something went wrong. Failed to import vault."
            )

    def __import_action(self) -> None:
        """
        Handle vault import
        """
        try:
            vault = self.__temp_vault
            if not isinstance(vault, tuple):
                raise FileNotFoundError("No vault found")

            password = self.__import_password_entry.get().strip()
            if len(password) == 0:
                self.__import_notify.configure(
                    text="Please enter the password", text_color=TEXT["error"]
                )
                return
            # Get the key name
            password_with_salt = password + vault[0].split("__")[1]
            # Decrypt the vault
            decrypted_data = tool.decrypt(
                key=password_with_salt, encrypted_data=vault[1], file_name=""
            )
            # Convert vault to data frame
            data_frame = pd.read_csv(decrypted_data)
            data_frame["Imported On"] = tool.current_datetime()
            # Merge Datastore
            DataStore.merge_datastore(data_frame)
            # Refresh the table
            self.__refresh_table()
            # Clean up the container and show success message
            self.__import_cleanup()
            self.__import_notify.configure(
                text="Vault is imported successfully", text_color=TEXT["success"]
            )
        except (crypto.InvalidToken, ValueError):
            self.__import_notify.configure(
                text="Incorrect vault password. Please try again.",
                text_color=TEXT["error"],
            )
        except Exception:
            self.__import_cleanup()
            self.__import_notify.configure(
                text="Something went wrong. Failed to import vault.",
                text_color=TEXT["error"],
            )

    def __export(self) -> None:
        """
        Export block
        """
        export_container = self.__wrapper(
            heading="# Export your vault",
            description="Export your vault as an encrypted file. Do not rename or modify the file, as this will corrupt it and prevent decryption. Your current account credentials are used for encryption and will be required to import the file back into the app.",
        )
        # Export button
        export_btn = tool.create_button(
            export_container, title="Export", command=self.__export_action
        )
        export_btn.grid(column=0, row=2, sticky="w", pady=15)
        # Display messages
        self.__export_notify = tool.create_label(
            export_container, title="", text_color=TEXT["error"]
        )
        self.__export_notify.grid(column=1, row=2, sticky="w", padx=(15, 0), pady=15)

        export_container.grid(column=0, row=2, sticky="we", pady=(25, 0))
        export_container.grid_columnconfigure(1, weight=1)

    def __export_action(self):
        """
        Handle vault export
        """
        try:
            self.__export_notify.configure(text="", text_color=TEXT["error"])
            # If Vault is empty, don't initiate export
            if DataStore.account_df.size == 0:
                self.__export_notify.configure(
                    text="Vault is empty. Nothing to export."
                )
                return
            # Path to save the file
            path = ctk.filedialog.asksaveasfilename(
                initialfile=DataStore.data_file_name,
                title="Select vault destination",
                defaultextension=".bytes",
                filetypes=[("Bytes files", "*.bytes")],
            )
            if path:
                # Read the file to export
                with open(f"data/{DataStore.data_file_name}", "rb") as file:
                    file_content = file.read()
                # Save the file to the path
                with open(path, "wb") as file:
                    file.write(file_content)
                self.__export_notify.configure(
                    text="Your vault is exported successfully.",
                    text_color=TEXT["success"],
                )
        except:
            self.__export_notify.configure(
                text="Something went wrong. Failed to export vault."
            )

    def __wrapper(self, heading: str, description: str) -> ctk.CTkFrame:
        """
        Create a wrapper for import and export blocks
        """
        container = tool.create_container(self)
        # Container heading
        title = tool.create_label(container, title=heading, font_size=15)
        title.grid(column=0, row=0, sticky="we", columnspan=3)
        # Container Description
        desc = tool.create_label(
            container, title=description, text_color=TEXT["light"], width=500
        )
        desc.grid(column=0, row=1, sticky="we", pady=(2, 0), columnspan=3)
        return container

    def __filename(self, name: str) -> str:
        """
        Get file name from the path
        """
        names = name.split("/")
        if len(names) > 0:
            return names[-1]
        return name

    def __import_cleanup(self) -> None:
        """
        Reinitialize import container
        """
        self.__temp_vault = None
        self.__import_container.destroy()
        self.__import()
