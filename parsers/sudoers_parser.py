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
    SUDO_ALIASES_PATTERN,
    SUDO_ALIASES_HEADERS,
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


def _parse_sudoers_aliases(lines, delim):
    aliases = []
    for line in lines:
        match = search(SUDO_ALIASES_PATTERN, line)
        if match is not None:
            alias = dict(zip(SUDO_ALIASES_HEADERS, match.groups()))
            alias_detail = f"{delim}".join(
                [detail.strip() for detail in alias["alias_detail"].split(",")]
            )
            alias["alias_detail"] = alias_detail
            aliases.append(alias)
    return aliases


def _parse_users_and_groups(lines, delim):
    entities = {
        "users": [],
        "groups": [],
    }
    for line in lines:
        if line.startswith("Defaults"):
            continue

        aliases = search(SUDO_ALIASES_PATTERN, line)
        if aliases is not None:
            continue

        users_match = search(SUDO_USERS_PATTERN, line)
        if users_match is not None:
            user = dict(zip(SUDO_USERS_HEADERS, users_match.groups()))
            commands = f"{delim}".join(
                [command.strip() for command in user["commands"].split(",")]
            )
            user["commands"] = commands
            entities["users"].append(user)
            continue

        groups_match = search(SUDO_GROUPS_PATTERN, line)
        if groups_match is not None:
            group = dict(zip(SUDO_GROUPS_HEADERS, groups_match.groups()))
            commands = f"{delim}".join(
                [command.strip() for command in group["commands"].split(",")]
            )
            group["commands"] = commands
            entities["groups"].append(group)
            continue

        print("CANNOT PARSE LINE:", line)

    return entities


def parse_sudoers(sudoers_file, delim="\n"):
    """A parser for /etc/passwd files taking an open file objet as input"""
    lines = sudoers_file.readlines()
    clean_lines = list(_get_relevant_sudoers_lines(lines))
    aliases = _parse_sudoers_aliases(clean_lines, delim)
    entities = _parse_users_and_groups(clean_lines, delim)
    return aliases, entities
