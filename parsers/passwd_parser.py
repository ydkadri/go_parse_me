"""
The parser for /etc/passwd files
"""

from .constants import PASSWD_HEADERS


def parse_passwd(passwd_file, delimiter=":"):
    """A parser for /etc/passwd files taking an open file objet as input"""
    lines = passwd_file.readlines()
    parsed_lines = []
    for line in lines:
        parsed = dict(zip(PASSWD_HEADERS, line.strip().split(delimiter)))
        if parsed['user_name'] != '':
            parsed_lines.append(parsed)
    return parsed_lines
