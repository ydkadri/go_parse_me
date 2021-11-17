"""CSV writer for /etc/passwd"""

import csv

from .constants import PASSWD_HEADERS
from .passwd_parser import parse_passwd


def write_passwd_file(fpath_in: str, fpath_out: str, delimiter=":"):
    """Parse an /etc/passwd file and write the output to csv"""
    with open(fpath_in, "r", encoding="utf-8") as fin:
        data = parse_passwd(fin, delimiter=delimiter)
    with open(fpath_out, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=PASSWD_HEADERS)
        writer.writeheader()
        writer.writerows(data)
