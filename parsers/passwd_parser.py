"""
The parser for /etc/passwd files
"""

HEADERS = (
    "user_name",
    "password",
    "user_id",
    "primary_group_id",
    "comment",
    "home_directory",
    "user_shell",
)


def parse_passwd(passwd_file, delimiter=":"):
    """A parser for /etc/passwd files taking an open file objet as input"""
    lines = passwd_file.readlines()
    parsed_lines = []
    for line in lines:
        parsed = dict(zip(HEADERS, line.strip().split(delimiter)))
        parsed_lines.append(parsed)
    return parsed_lines
