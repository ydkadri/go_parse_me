"""CSV writer for /etc/passwd"""

import os
import csv

from .constants import SUDO_ALIASES_HEADERS, SUDO_USERS_HEADERS, SUDO_GROUPS_HEADERS
from .sudoers_parser import parse_sudoers


def write_sudoers_file(fpath_in: str, fpath_out: str):
    """
    Parse an /etc/sudoers file and write the output to csv

    The expected output file path is of the form /path/to/file.csv
    and will output three files:
        /path/to/alias_file.csv
        /path/to/users_file.csv
        /path/to/groups_file.csv
    """
    with open(fpath_in, "r", encoding="utf-8") as fin:
        aliases, entities = parse_sudoers(fin)

    # Get the directory and base filename
    dirname = os.path.dirname(fpath_out)
    basename = os.path.basename(fpath_out)

    alias_file = os.path.join(dirname, f"alias_{basename}")
    users_file = os.path.join(dirname, f"users_{basename}")
    groups_file = os.path.join(dirname, f"groups_{basename}")
    # Write Aliases file
    with open(alias_file, "w", newline="", encoding="utf-8") as alias_fout:
        alias_writer = csv.DictWriter(alias_fout, fieldnames=SUDO_ALIASES_HEADERS)
        alias_writer.writeheader()
        alias_writer.writerows(aliases)

    # Write Users file
    with open(users_file, "w", newline="", encoding="utf-8") as users_fout:
        alias_writer = csv.DictWriter(users_fout, fieldnames=SUDO_USERS_HEADERS)
        alias_writer.writeheader()
        alias_writer.writerows(entities["users"])

    # Write Groups file
    with open(groups_file, "w", newline="", encoding="utf-8") as groups_fout:
        alias_writer = csv.DictWriter(groups_fout, fieldnames=SUDO_GROUPS_HEADERS)
        alias_writer.writeheader()
        alias_writer.writerows(entities["groups"])
