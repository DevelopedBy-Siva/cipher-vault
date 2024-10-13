APP_NAME = "Vault"
LOGO = "./static/logo.png"

WINDOW = {
    "bg": "#fff",
    "width": 860,
    "height": 720,
    "new-password": {
        "title": "Add Credentials",
        "heading": "New Account Information",
        "desc": "Store and organize passwords or sensitive data with ease.",
        "width": 600,
        "height": 420,
    },
    "export-import": {
        "title": "Export/Import",
        "heading": "Backup & Restore Data",
        "desc": "Export your saved entries for safekeeping or import from a backup file.",
        "width": 540,
        "height": 460,
    },
}

USER_OPTIONS = {
    "new": {
        "title": "Add Credentials",
        "icon": "add",
        "inputs": (
            {"title": "Account", "placeholder": "Enter account name"},
            {"title": "Email/Username", "placeholder": "Enter email or username"},
            {
                "title": "Password",
                "placeholder": "Enter or Create password",
                "show": "*",
                "command": {"title": "Generate Password"},
            },
        ),
    },
    "exp-imp": {
        "title": "Export/Import",
        "icon": "export-import",
    },
}

BUTTON = {
    "bg": "#0f172a",
    "hover-bg": "#262E3F",
    "bg-light": "#e7e7e9",
    "hover-bg-l": "#dbdcde",
    "color": "#fff",
    "icon": {
        "password-show": "./static/password-show.png",
        "password-hide": "./static/password-hide.png",
    },
}

TEXT = {
    "dark": "#0f172a",
    "light": "grey",
    "font": "Showcard Gothic",
    "bg": "#fff",
    "border": "grey",
}
