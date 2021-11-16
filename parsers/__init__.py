"""
A collection of parsers for system files found on Linux machines

These parsers will output the data content as a dictionary
"""
from .group_parser import parse_group
from .passwd_parser import parse_passwd
from .sudoers_parser import parse_sudoers
