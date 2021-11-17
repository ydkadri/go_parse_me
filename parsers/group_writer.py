"""CSV writer for /etc/group"""

import csv

from .constants import GROUP_HEADERS
from .group_parser import parse_group


def write_groups_file(fpath_in: str, fpath_out: str, delimiter=":"):
    """Parse an /etc/group file and write the output to csv"""
    with open(fpath_in, "r", encoding="utf-8") as fin:
        data = parse_group(fin, delimiter=delimiter)
    with open(fpath_out, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=GROUP_HEADERS)
        writer.writeheader()
        writer.writerows(data)
