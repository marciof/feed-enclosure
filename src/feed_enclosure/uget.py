# -*- coding: UTF-8 -*-

"""
Wraps uGet to add additional functionality and workaround certain issues.

Changes: (1) transliterates Unicode characters in filenames to ASCII;
(2) ensures multiple consecutive calls to uGet don't block by making it run
in the background; (3) can optionally wait on a download for completion;
(4) ensures relative folder paths are made absolute.
"""

# stdlib
import argparse
import asyncio
import os
import os.path
import subprocess
import sys
from typing import Callable, List, Optional, Tuple

# external
# FIXME missing type stubs for some external libraries
from asyncinotify import Inotify, Mask  # type: ignore
from unidecode import unidecode

# internal
from . import logging


MODULE_DOC = __doc__.strip()


def find_executable_name() -> str:
    return 'uget-gtk'


class Uget:

    def __init__(self):
        self.executable_name = find_executable_name()
        self.logger = logging.create_logger('uget')

        self.arg_parser = argparse.ArgumentParser(
            description=MODULE_DOC, add_help=False, allow_abbrev=False)

        self.arg_parser.add_argument(
            '-?', '-h', '--help', action='store_true', help=argparse.SUPPRESS)
        self.arg_parser.add_argument(
            '--quiet', action='store_true', help=argparse.SUPPRESS)

        self.arg_url = self.arg_parser.add_argument(
            'url', nargs='?', default=None, help=argparse.SUPPRESS)
        self.arg_file_name = self.arg_parser.add_argument(
            '--filename', dest='file_name', help=argparse.SUPPRESS)
        self.arg_folder = self.arg_parser.add_argument(
            '--folder', help=argparse.SUPPRESS)

        self.arg_parser.add_argument(
            '--http-user-agent',
            dest='http_user_agent',
            help=argparse.SUPPRESS)

        self.arg_wait_for_download = self.arg_parser.add_argument(
            '--x-wait-download',
            dest='wait_download',
            help='Wait for download to finish (requires folder and file name)',
            action='store_true')

    # FIXME uGet doesn't handle filenames with Unicode characters on the CLI
    def clean_file_name(self, file_name: str) -> str:
        return unidecode(file_name)

    def run(self, args: Optional[List[str]] = None) -> int:
        (parsed_args, rest_args) = self.arg_parser.parse_known_args(args)
        self.logger.debug('Parsed arguments: %s', parsed_args)
        self.logger.debug('Remaining arguments: %s', rest_args)

        kwargs = vars(parsed_args)
        wait_for_download = kwargs.pop(self.arg_wait_for_download.dest)

        # TODO attempt to figure out folder and file name?
        # TODO honor default folder and file name from uget
        if wait_for_download:
            has_folder = kwargs[self.arg_folder.dest] is not None
            has_file_name = kwargs[self.arg_file_name.dest] is not None

            if not has_folder or not has_file_name:
                raise Exception(
                    'Waiting for a download requires folder and file name')

        if parsed_args.help:
            self.arg_parser.print_help()
            print('\n---')

        self.ensure_running()
        (command, file_path) = self.make_command(args=rest_args, **kwargs)

        self.logger.info('Running command: %s', command)
        return_code = subprocess.run(args=command).returncode

        if wait_for_download and file_path is not None:
            self.logger.info('Waiting for download to finish')
            asyncio.run(self.wait_for_download(file_path))

        return return_code

    def ensure_running(self) -> None:
        """
        If uGet isn't already running, then starting it up will block execution
        until it exits. To avoid that, ensure it's always running already in
        the background.
        """

        # TODO detect existence of `start_new_session` (it's POSIX specific)
        subprocess.Popen([self.executable_name, '--quiet'],
                         start_new_session=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)

    def get_file_disk_sizes(
            self,
            file_path: str,
            block_size_bytes: int = 512) \
            -> Tuple[int, int]:

        """
        Get the reported file size, as well as the actual total block size
        on disk.
        """

        stat = os.stat(file_path)

        # TODO detect availability of `st_blocks` (it's Unix specific)
        block_size = stat.st_blocks * block_size_bytes

        return (stat.st_size, block_size)

    def is_downloaded(
            self,
            file_path: str,
            file_size: Optional[int],
            progress_cb: Optional[Callable[[int], None]] = None) \
            -> bool:

        # If the file to be downloaded has been already reserved
        # space on disk, then its apparent size will already be the
        # final size. In that case use the disk block size to get
        # an idea for when its download is complete.
        (actual_size, block_size) = self.get_file_disk_sizes(file_path)

        if progress_cb is not None:
            progress_cb(block_size)

        return ((block_size >= actual_size)
                and ((file_size is None) or (actual_size == file_size)))

    def make_command(
            self,
            args: Optional[List[str]] = None,
            url: Optional[str] = None,
            file_name: Optional[str] = None,
            folder: Optional[str] = None,
            http_user_agent: Optional[str] = None,
            help: bool = False,
            quiet: bool = False) \
            -> Tuple[List[str], Optional[str]]:

        command = [self.executable_name]
        file_path = None

        if help:
            command += ['--help']

        if quiet:
            command += ['--quiet']

        # FIXME uGet doesn't seem to interpret relative folder paths correctly,
        #       so as a workaround make it absolute
        if folder is not None:
            abs_folder = os.path.abspath(folder)
            command += ['--folder=' + abs_folder]
            file_path = abs_folder

        if file_name is not None:
            clean_file_name = self.clean_file_name(file_name)
            command += ['--filename=' + clean_file_name]
            if file_path is None:
                file_path = clean_file_name
            else:
                file_path = os.path.join(file_path, clean_file_name)

        if http_user_agent is not None:
            command += ['--http-user-agent=' + http_user_agent]

        if args is not None:
            command += args

        return (command + (['--', url] if url else []), file_path)

    async def wait_for_download(
            self,
            file_path: str,
            file_size: Optional[int] = None,
            progress_cb: Optional[Callable[[int], None]] = None) \
            -> None:

        (folder, file_name) = os.path.split(file_path)

        if folder == '':
            folder = os.getcwd()

        # TODO use the `watchdog` package to be platform agnostic?
        with Inotify() as inotify:
            # TODO watch target file only for performance (measure first)
            inotify.add_watch(folder, Mask.ONLYDIR | Mask.CLOSE | Mask.CREATE
                              | Mask.MODIFY | Mask.MOVED_TO)

            # TODO add an optional check, if after starting uGet there's no
            #      inotify event for the target filename then it's
            #      suspicious and flag it?
            async for event in inotify:
                if event.path.name != file_name:
                    continue
                if self.is_downloaded(file_path, file_size, progress_cb):
                    break


def main(args: Optional[List[str]] = None) -> None:
    sys.exit(Uget().run(args))


if __name__ == '__main__':
    main()
