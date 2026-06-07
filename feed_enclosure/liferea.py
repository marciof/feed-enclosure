# -*- coding: UTF-8 -*-

"""
Wraps Liferea adding a command to get the path to the feed list OPML file.
"""

# FIXME document (including dependencies and setup)
# FIXME test
# FIXME error handling
# FIXME proper logging (including to syslog)

# stdlib
import argparse
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# external
# FIXME missing type stubs for some external libraries
from xdg_base_dirs import xdg_config_home  # type: ignore

# internal
from . import log


EXIT_FAILURE = 1

try:
    EXIT_SUCCESS = os.EX_OK
except AttributeError:
    EXIT_SUCCESS = 0


# FIXME fix flag `--mainwindow-state`
#       https://github.com/lwindolf/liferea/issues/447
# FIXME add command for setting encAutoDownload=true
# FIXME add command for setting filtercmd
class Liferea:

    def __init__(self):
        self.logger = log.create_logger('liferea')

        # FIXME add options/commands to Liferea app
        self.FEED_LIST_COMMAND = 'feed-list'

        self.arg_parser = argparse.ArgumentParser(
            description=__doc__.strip(), add_help=False)
        self.arg_help = self.arg_parser.add_argument(
            '-h', '--help', action='store_true', help=argparse.SUPPRESS)

        self.cmd_arg_parser = self.arg_parser.add_subparsers(
            dest='command_arg')

        self.cmd_arg_parser.add_parser(
            self.FEED_LIST_COMMAND, help='print feedlist OPML file path')

    def main(self, args: Optional[List[str]] = None) -> Any:
        (parsed_kwargs, rest_args) = self.parse_args(args)
        command = parsed_kwargs[self.cmd_arg_parser.dest]

        if command is None:
            return subprocess.run(['liferea'] + rest_args).returncode

        try:
            if command == self.FEED_LIST_COMMAND:
                print(self.find_feed_list_opml())
            else:
                raise Exception('Unknown command: ' + command)

            return EXIT_SUCCESS
        except SystemExit:
            raise
        except BaseException as error:
            self.logger.error('Failed to interface Liferea', exc_info=error)
            return EXIT_FAILURE

    def parse_args(self, args: Optional[List[str]]) \
            -> Tuple[Dict[str, Any], List[str]]:

        (parsed_args, rest_args) = self.arg_parser.parse_known_args(args)
        parsed_kwargs = vars(parsed_args)

        self.logger.debug('Parsed arguments: %s', parsed_args)
        self.logger.debug('Remaining arguments: %s', rest_args)

        if parsed_kwargs[self.arg_help.dest]:
            rest_args.insert(0, self.arg_help.option_strings[0])
            self.arg_parser.print_help()
            print('\n---\n')

        self.logger.debug('Final arguments: %s', rest_args)
        return (parsed_kwargs, rest_args)

    def find_feed_list_opml(self) -> Path:
        return xdg_config_home().joinpath('liferea', 'feedlist.opml')


if __name__ == '__main__':
    sys.exit(Liferea().main())
