"""
The parser for /etc/sudoers file

sudoers user syntax
User    Host=(RunAsUser:Group)  [NOPASSWD:]Commands

sudoers group syntax
%Group  Host=(RunAsUser)        [NOPASSWD:]Commands

aliases
User_Alias  ALIAS_NAME = user,user,...
Runas_Alias ALIAS_NAME = user,user,...
Host_Alias  ALIAS_NAME = host,host,... OR ip/mask,ipnetwork
Cmnd_Alias  ALIAS_NAME = cmnd,cmnd,...

Exceptions are achieved with an exclamation mark "!"

e.g.
User_Alias  EXCEPT_ROOT = ALL,!root
"""

from re import search

from .constants import (
    COMMENT_CHAR,
    EMPTY_LINE,
    SUDO_ALIASES,
    SUDO_ALIASES_PATTERN,
    SUDO_USERS_PATTERN,
    SUDO_USERS_HEADERS,
    SUDO_GROUPS_PATTERN,
    SUDO_GROUPS_HEADERS,
)


def _get_relevant_sudoers_lines(lines):
    prev_line = ""
    for line in lines:
        line = prev_line + line.strip()
        if line.startswith(COMMENT_CHAR):
            continue
        if search(EMPTY_LINE, line) is not None:
            continue
        if line.endswith("\\"):
            prev_line = line
        else:
            prev_line = ""
            yield line


def _parse_sudoers_aliases(lines):
    aliases = {alias: [] for alias in SUDO_ALIASES}
    for line in lines:
        match = search(SUDO_ALIASES_PATTERN, line)
        if match is not None:
            name, detail = line[match.end() :].strip().split("=")
            aliases[match.group()].append(
                {"name": name.strip(), "detail": detail.strip()}
            )
    return aliases


def _parse_users_and_groups(lines):
    entities = {
        "users": [],
        "groups": [],
    }
    for line in lines:
        aliases = search(SUDO_ALIASES_PATTERN, line)
        if aliases is not None:
            continue
        if line.startswith("Defaults"):
            continue
        users_match = search(SUDO_USERS_PATTERN, line)
        if users_match is not None:
            entities["users"].append(
                dict(zip(SUDO_USERS_HEADERS, users_match.groups()))
            )
        else:
            groups_match = search(SUDO_GROUPS_PATTERN, line)
            if groups_match is not None:
                entities["groups"].append(
                    dict(zip(SUDO_GROUPS_HEADERS, groups_match.groups()))
                )
            else:
                print("CANNOT PARSE LINE:", line)

    return entities


def parse_sudoers(sudoers_file, delimiter="\W "):
    """A parser for /etc/passwd files taking an open file objet as input"""
    lines = sudoers_file.readlines()
    clean_lines = [line for line in _get_relevant_sudoers_lines(lines)]
    aliases = _parse_sudoers_aliases(clean_lines)
    entities = _parse_users_and_groups(clean_lines)
    return aliases, entities
