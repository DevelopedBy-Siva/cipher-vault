APP_NAME = "Vault"
LOGO = "./static/logo.png"

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
        "height": 490,
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
            {
                "title": "Account",
                "placeholder": "Enter account name",
                "key": "account",
            },
            {
                "title": "URL (optional)",
                "placeholder": "Enter the URL",
                "key": "url",
            },
            {
                "title": "Email/Username",
                "placeholder": "Enter email or username",
                "key": "username",
            },
            {
                "title": "Password",
                "placeholder": "Enter or Create password",
                "show": "*",
                "command": {"title": "Generate Password"},
                "key": "password",
            },
        ),
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
}
