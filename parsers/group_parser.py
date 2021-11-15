"""
The parser for /etc/group files
"""

HEADERS = (
    "group_name",
    "password",
    "group_id",
    "users",
)


def parse_group(group_file, delimiter=":"):
    """A parser for /etc/group files taking an open file objet as input"""
    lines = group_file.readlines()
    parsed_lines = []
    for line in lines:
        parsed = dict(zip(HEADERS, line.strip().split(delimiter)))
        parsed_lines.append(parsed)
    return parsed_lines