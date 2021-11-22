"""
The parser for /etc/group files
"""

from .constants import GROUP_HEADERS


def parse_group(group_file, delimiter=":"):
    """A parser for /etc/group files taking an open file objet as input"""
    lines = group_file.readlines()
    parsed_lines = []
    for line in lines:
        parsed = dict(zip(GROUP_HEADERS, line.strip().split(delimiter)))
        if parsed['group_name'] != '':
            parsed_lines.append(parsed)
    return parsed_lines
