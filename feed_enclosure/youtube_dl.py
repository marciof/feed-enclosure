# -*- coding: UTF-8 -*-

# FIXME remove yt-dlp wrapper as it's no longer needed
"""
Wraps yt-dlp.
"""

# stdlib
import argparse
import os.path
import sys
from typing import Any, List, Optional

# external
# FIXME missing type stubs for some external libraries
# Preferred over youtube-dl due to being more up-to-date.
import yt_dlp  # type: ignore
# FIXME use plugin API for external downloaders
#       https://github.com/yt-dlp/yt-dlp#developing-plugins
from yt_dlp.utils import YoutubeDLError  # type: ignore

# internal
from . import log, os_api


MODULE_DOC = __doc__.strip()


class YoutubeDl:

    def __init__(self):

        self.PATHS_ARG_NAME = '--paths'
        self.logger = log.create_logger('youtube_dl')

        self.arg_parser = argparse.ArgumentParser(
            description=MODULE_DOC, add_help=False, allow_abbrev=False)
        self.arg_help = self.arg_parser.add_argument(
            '-h', '--help', action='store_true', help=argparse.SUPPRESS)
        self.arg_output = self.arg_parser.add_argument(
            '-o', '--output', help='Output template')

    def main(self, args: Optional[List[str]] = None) -> Any:
        parsed_args = self.parse_args(args)

        # FIXME expose function without exiting
        try:
            # TODO capture error output and log it
            return yt_dlp._real_main(parsed_args)
        except SystemExit as exit_error:
            return exit_error.code

    def parse_args(self, args: Optional[List[str]]) -> List[str]:
        (parsed_args, rest_args) = self.arg_parser.parse_known_args(args)
        parsed_kwargs = vars(parsed_args)

        self.logger.debug('Parsed arguments: %s', parsed_args)
        self.logger.debug('Remaining arguments: %s', rest_args)

        if parsed_kwargs[self.arg_output.dest]:
            rest_args[0:0] = self.parse_output_template_arg(
                parsed_kwargs[self.arg_output.dest])

        if parsed_kwargs[self.arg_help.dest]:
            rest_args.insert(0, self.arg_help.option_strings[0])
            self.arg_parser.print_help()
            print('\n---\n')

        self.logger.debug('Final arguments: %s', rest_args)
        return rest_args

    # https://github.com/yt-dlp/yt-dlp#output-template
    def parse_output_template_arg(self, output: str) -> List[str]:
        (head, tail) = os.path.split(output)

        if not tail:
            # Directory only, eg. "xyz/"
            return [self.PATHS_ARG_NAME, output]

        if not head:
            if os.path.isdir(output):
                # Directory constant, eg. ".."
                return [self.PATHS_ARG_NAME, output]
            else:
                # File name only, eg. "xyz"
                return [self.arg_output.option_strings[0], output]

        if os.path.isdir(output):
            return [self.PATHS_ARG_NAME, output]
        else:
            return [self.arg_output.option_strings[0], output]

    # TODO avoid parsing arguments a second time?
    def download(
            self,
            url: str,
            output: Optional[str] = None,
            format: Optional[str] = None,
            match_filters: Optional[str] = None,
            add_metadata: bool = False,
            verbose: bool = False) \
            -> None:

        argv = []

        if output is not None:
            argv.extend([self.arg_output.option_strings[0], output])

        if format is not None:
            argv.extend(['--format', format])

        if match_filters is not None:
            argv.extend(['--match-filters', match_filters])

        # FIXME add option for adding metadata
        if add_metadata:
            argv.append('--add-metadata')

        if verbose:
            argv.append('--verbose')

        argv.extend([
            # FIXME add fallback https://github.com/yt-dlp/yt-dlp/issues/14680
            # '--extractor-args', 'youtube:player_js_version=actual',
            '--',
            url,
        ])
        exit_status = self.main(argv)

        if exit_status not in {None, os_api.EXIT_SUCCESS}:
            raise YoutubeDLError(exit_status)


# TODO tests
if __name__ == '__main__':
    sys.exit(YoutubeDl().main())
