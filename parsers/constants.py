"""
Constants for file parsers
"""

# General use
COMMENT_CHAR = "#"
EMPTY_LINE = "^$"

# /etc/passwd headers
PASSWD_HEADERS = (
    "user_name",
    "password",
    "user_id",
    "primary_group_id",
    "comment",
    "home_directory",
    "user_shell",
)

# /etc/group headers
GROUP_HEADERS = (
    "group_name",
    "password",
    "group_id",
    "users",
)

# /etc/sudoers aliases and headers
SUDO_ALIASES_HEADERS = ("alias", "alias_type", "alias_name", "alias_detail")

SUDO_USERS_HEADERS = (
    "user",
    "group",
    "as",
    "run_as_user",
    "run_as_group",
    "no_pass",
    "commands",
)

SUDO_GROUPS_HEADERS = ("user", "group", "as", "run_as_user", "no_pass", "commands")

# /etc/sudoers RegEx patterns
SUDO_ALIASES_PATTERN = (
    r"^((User|Runas|Host|Cmnd)_Alias)\s+"
    r"([a-zA-Z0-9_]+)\s*="
    r"\s*(.*)"
)

SUDO_USERS_PATTERN = (
    r"^([a-zA-Z0-9_]+)\s+"
    r"([a-zA-Z0-9_]+)\s*="
    r"\s*(\(([a-zA-Z]+):?([a-zA-Z]*)\))?\s*"
    r"(NOPASSWD:)?\s*"
    r"(.*)"
)

SUDO_GROUPS_PATTERN = (
    r"^%([a-zA-Z0-9_]+)\s+"
    r"([a-zA-Z0-9_]+)\s*="
    r"\s*(\(([a-zA-Z_]+)\))?\s*"
    r"(NOPASSWD:)?\s*"
    r"(.*)"
)
