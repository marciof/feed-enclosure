#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Prints the path to a Liferea file/folder.

Folders always end with the OS' path separator.

References:

- XDG Spec: https://specifications.freedesktop.org/basedir/latest/#variables
- Liferea man page: https://github.com/lwindolf/liferea/blob/v1.16.7/man/liferea.1
"""


# /// script
# dependencies = [
# ]
# ///


# stdlib
import argparse
import os
from pathlib import Path
from typing import List, Optional, NoReturn, Callable


def get_env_var_path(name: str, default: Callable[[], Path]) -> Path:
    value = os.getenv(name)
    return Path(value) if value is not None else default()


def get_feed_list_opml_path(app_name: str) -> Path:
    config_home = get_env_var_path('XDG_CONFIG_HOME',
        default=lambda: Path.home() / '.config')
    return config_home / app_name / 'feedlist.opml'


def get_plugins_path(app_name: str) -> Path:
    data_home = get_env_var_path('XDG_DATA_HOME',
        default=lambda: Path.home() / '.local' / 'share')
    return data_home / app_name / 'plugins'


# TODO request Liferea cmdline flag to print paths
# FIXME tests (including mypy, pycodestyle)
# FIXME error handling
def main(args: Optional[List[str]] = None) -> NoReturn:
    arg_parser = argparse.ArgumentParser(description=__doc__.strip())
    cmd_parser = arg_parser.add_subparsers(required=True)

    opml_cmd = cmd_parser.add_parser('opml', help='feed list OPML file')
    opml_cmd.set_defaults(func=get_feed_list_opml_path)

    plugins_cmd = cmd_parser.add_parser('plugins', help='plugins folder')
    plugins_cmd.set_defaults(func=get_plugins_path)

    parsed_args = arg_parser.parse_args(args)
    path = parsed_args.func(app_name='liferea')

    if path.is_dir():
        path = str(path) + os.sep

    print(path)
    raise SystemExit()


if __name__ == '__main__':
    main()
