APP_NAME = "CipherVault"

AUTH_FILE = {
    "path": "./data/config.ini",
    "hash_key": "SIGNATURE",
    "salt": "DATA_TOKEN",
}

GEN_PASS_LENGTH = 12

WINDOW = {
    "bg": "#fff",
    "width": 860,
    "height": 720,
    "new-password": {
        "title": "Add Credentials",
        "heading": "New Account Information",
        "desc": "Store and organize passwords or sensitive data with ease.",
        "width": 600,
        "height": 510,
    },
    "export-import": {
        "title": "Export/Import",
        "heading": "Backup & Restore Data",
        "desc": "Export your saved entries for safekeeping or import from a backup file.",
        "width": 580,
        "height": 470,
    },
    "account-details": {
        "title": "Account Snapshot",
        "heading": "Account Snapshot",
        "desc": "Manage your stored credentials—view, modify, or remove them from the vault.",
        "width": 540,
        "height": 460,
    },
}

USER_OPTIONS = {
    "new": {
        "title": "Add Credentials",
        "icon": "add",
        "inputs": {
            "account": {
                "title": "Account",
                "placeholder": "Enter account name",
                "key": "account",
                "min_len": 3,
                "error": "Account must be at least 3 characters!",
                "save_failed": "Failed to save the account. Please try again.",
            },
            "url": {
                "title": "URL (optional)",
                "placeholder": "Enter the URL",
                "min_len": 0,
                "error": "",
            },
            "username": {
                "title": "Email/Username",
                "placeholder": "Enter email or username",
                "min_len": 3,
                "error": "Email or Username must be at least 3 characters!",
            },
            "password": {
                "title": "Password",
                "placeholder": "Enter or Create password",
                "show": "*",
                "command": {"title": "Generate Password"},
                "min_len": 3,
                "error": "Password must be at least 3 characters!",
            },
        },
    },
    "exp-imp": {
        "title": "Export/Import",
        "icon": "export-import",
    },
}


BUTTON = {
    "bg": "#191919",
    "hover-bg": "#2F2F2F",
    "bg-light": "#eaeaea",
    "hover-bg-l": "#dbdcde",
    "color": "#fff",
    "icon": {
        "password-show": "./static/password-show.png",
        "password-hide": "./static/password-hide.png",
    },
}

TEXT = {
    "dark": "#191919",
    "light": "#979797",
    "font": "Showcard Gothic",
    "bg": "#fff",
    "border": "#979797",
    "border-light": "#eaeaea",
    "border-light-hover": "#e1e1e1",
    "error": "#ff0000",
    "success": "#00b300",
}

AUTH_FIELDS = {
    "username": {
        "max_len": 12,
        "min_len": 3,
        "title": "Username",
        "placeholder": "Enter the username",
        "show": "",
        "error": {
            "empty": "Username cannot be left blank",
            "404": "Oops! We couldn't find the account. Why not create a new one?",
            "present": "Whoops! That account is already registered",
            "long": "Username must be 3-12 characters!",
            "invalid": "Username can only contain letters, digits, and spaces",
            "unknown": "Oops! Something went wrong. Try again",
        },
    },
    "password": {
        "max_len": 16,
        "min_len": 8,
        "title": "Password",
        "placeholder": "Enter the password",
        "show": "*",
        "error": {
            "empty": "Password cannot be empty",
            "incorrect": "The password you entered is incorrect. Please try again",
            "long": "Password must be 8-16 characters!",
        },
    },
}

TABLE = {
    "header": "#191919",
    "bg-hover": "#f1f8fb",
    "odd": "#f6f6f8",
    "even": "#fff",
}
