# -*- coding: UTF-8 -*-

"""
Wraps youtube-dl to add additional functionality.

Changes: (1) support for uGet as an external downloader, named "x-uget";
(2) support for an output download folder only template.
"""

# stdlib
import argparse
import asyncio
import os.path
import sys
from time import time
from typing import Any, List, Optional, Type

# external
from overrides import overrides
# FIXME missing type stubs for some external libraries
# TODO use yt-dlp? https://github.com/yt-dlp/yt-dlp
# TODO use pytube? https://github.com/pytube/pytube
import youtube_dl  # type: ignore
# FIXME plugin system API for youtube-dl external downloaders
from youtube_dl.downloader.external import _BY_NAME, ExternalFD  # type: ignore
from youtube_dl.utils import YoutubeDLError  # type: ignore

# internal
from . import log, os_api, uget


MODULE_DOC = __doc__.strip()


# TODO log to syslog as well using `log`
class UgetFD (ExternalFD):
    """
    https://github.com/ytdl-org/youtube-dl#mandatory-and-optional-metafields
    """

    AVAILABLE_OPT = '--version'

    def __init__(
            self,
            *args,
            download_progress_throttle_interval_secs: float = 1,
            **kwargs):

        super().__init__(*args, **kwargs)
        self.uget = uget.Uget()
        self.last_timestamp_secs = time()
        self.download_progress_throttle_interval_secs = \
            download_progress_throttle_interval_secs

    @classmethod
    @overrides
    def get_basename(cls) -> str:
        return uget.find_executable_name()

    def error(self, message: str, *args) -> None:
        self.report_error(('[%s] ' + message) % (self.get_basename(), *args))

    def info(self, message: str, *args) -> None:
        self.to_screen(('[%s] ' + message) % (self.get_basename(), *args))

    def warn(self, message: str, *args) -> None:
        self.report_warning(('[%s] ' + message) % (self.get_basename(), *args))

    def log_progress_throttled(
            self, current_size: int, expected_size: Optional[int]):

        timestamp_secs = time()
        should_log = ((timestamp_secs - self.last_timestamp_secs)
                      >= self.download_progress_throttle_interval_secs)

        if should_log:
            self.last_timestamp_secs = timestamp_secs
            self.info('Downloaded %s block bytes (%s)',
                      current_size,
                      self.calc_format_percent(current_size, expected_size))

    @overrides
    def temp_name(self, filename: str) -> str:
        return self.uget.clean_file_name(filename)

    def calc_format_percent(self, count: int, total: Optional[int]) -> str:
        return self.format_percent(self.calc_percent(count, total)).strip()

    # TODO honor youtube-dl's proxy option/value
    # TODO honor `external_downloader_args`
    def _make_cmd(self, tmpfilename: str, info_dict: dict) -> List[str]:
        (folder, file_name_only) = os.path.split(tmpfilename)

        # TODO use flag to wait for download?
        (command, file_path) = self.uget.make_command(
            url=info_dict['url'],
            file_name=file_name_only,
            folder=folder,
            quiet=True,
            http_user_agent=info_dict.get('http_headers', {})
                                     .get('User-Agent'))

        return command

    @overrides
    def _call_downloader(self, tmpfilename: str, info_dict: dict) -> int:
        # TODO use `filesize_approx` as well?
        expected_size = info_dict.get('filesize')

        if expected_size is None:
            self.warn('Unknown expected file size, using block size only.')
        else:
            self.info('Expected file size: %d bytes', expected_size)

        try:
            is_downloaded = self.uget.is_downloaded(tmpfilename, expected_size)
            return_code: Optional[int] = os_api.EXIT_SUCCESS
        except FileNotFoundError:
            is_downloaded = False
            return_code = None

        # TODO honor youtube-dl's continue/restart option
        if is_downloaded:
            self.report_file_already_downloaded(tmpfilename)
            return os_api.EXIT_SUCCESS

        if return_code is None:
            self.uget.ensure_running_background()
            return_code = super()._call_downloader(tmpfilename, info_dict)
            self.info('Return code: %s', return_code)
        else:
            self.info('File already exists, waiting for download.')

        asyncio.run(self.wait_for_download(tmpfilename, info_dict))
        return return_code

    async def wait_for_download(self, tmpfilename: str, info_dict: dict):
        expected_size = info_dict.get('filesize')

        await self.uget.wait_for_download(
            tmpfilename,
            expected_size,
            lambda current_size:
                self.log_progress_throttled(current_size, expected_size))


class YoutubeDl:

    def __init__(
            self,
            uget_external_downloader: Optional[str] = 'x-uget'):

        self.logger = log.create_logger('youtube_dl')
        self.uget_external_downloader = uget_external_downloader

        self.arg_parser = argparse.ArgumentParser(
            description=MODULE_DOC, add_help=False, allow_abbrev=False)
        self.arg_help = self.arg_parser.add_argument(
            '-h', '--help', action='store_true', help=argparse.SUPPRESS)
        self.arg_output = self.arg_parser.add_argument(
            '-o', '--output', help='Output template')

        if uget_external_downloader is not None:
            self.register_external_downloader(
                uget_external_downloader, UgetFD)

    def main(self, args: Optional[List[str]] = None) -> Any:
        parsed_args = self.parse_args(args)

        # FIXME expose function to use youtube-dl without exiting
        try:
            # TODO capture error output and log it
            return youtube_dl._real_main(parsed_args)
        except SystemExit as exit_error:
            return exit_error.code

    def register_external_downloader(
            self, name: str, klass: Type[ExternalFD]) \
            -> None:

        _BY_NAME[name] = klass

    def parse_args(self, args: Optional[List[str]]) -> List[str]:
        (parsed_args, rest_args) = self.arg_parser.parse_known_args(args)
        parsed_kwargs = vars(parsed_args)

        self.logger.debug('Parsed arguments: %s', parsed_args)
        self.logger.debug('Remaining arguments: %s', rest_args)

        if parsed_kwargs[self.arg_output.dest]:
            rest_args[0:0] = [
                self.arg_output.option_strings[0],
                self.parse_output_template_arg(
                    parsed_kwargs[self.arg_output.dest]),
            ]

        if parsed_kwargs[self.arg_help.dest]:
            rest_args.insert(0, self.arg_help.option_strings[0])
            self.arg_parser.print_help()
            print('\n---\n')

        self.logger.debug('Final arguments: %s', rest_args)
        return rest_args

    # https://github.com/ytdl-org/youtube-dl#output-template
    def parse_output_template_arg(self, output: str) -> str:
        (head, tail) = os.path.split(output)

        if not tail:
            # Directory only, eg. "xyz/"
            return os.path.join(output, youtube_dl.DEFAULT_OUTTMPL)

        if not head:
            if os.path.isdir(output):
                # Directory constant, eg. ".."
                return os.path.join(output, youtube_dl.DEFAULT_OUTTMPL)
            else:
                # File name only, eg. "xyz"
                return output

        if os.path.isdir(output):
            return os.path.join(output, youtube_dl.DEFAULT_OUTTMPL)
        else:
            return output

    # TODO avoid parsing arguments a second time?
    def download(
            self,
            url: str,
            external_downloader: Optional[str] = None,
            output: Optional[str] = None,
            format: Optional[str] = None,
            add_metadata: bool = False,
            verbose: bool = False) \
            -> None:

        argv = []

        if external_downloader is not None:
            argv.extend(['--external-downloader', external_downloader])

        if output is not None:
            argv.extend([self.arg_output.option_strings[0], output])

        if format is not None:
            argv.extend(['--format', format])

        # FIXME add `YoutubeDL` option for adding metadata
        #       https://github.com/ytdl-org/youtube-dl/#embedding-youtube-dl
        if add_metadata:
            argv.append('--add-metadata')

        if verbose:
            argv.append('--verbose')

        argv.extend(['--', url])
        exit_status = self.main(argv)

        if exit_status not in {None, os_api.EXIT_SUCCESS}:
            raise YoutubeDLError(exit_status)


# TODO tests
if __name__ == '__main__':
    sys.exit(YoutubeDl().main())
