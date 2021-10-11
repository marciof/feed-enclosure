# -*- coding: UTF-8 -*-

"""
Wraps the various download tools to pick the most appropriate for downloading
feed enclosures.
"""

# stdlib
import argparse
import os
import sys
from typing import Any, List, Optional

# internal
from . import log, uget, youtube_dl


MODULE_DOC = __doc__.strip()


class Downloader:

    def __init__(self):
        self.logger = log.create_logger('download')

        self.arg_parser = argparse.ArgumentParser(description=MODULE_DOC)
        self.arg_url = self.arg_parser.add_argument(
            'url', help='URL to download')
        self.arg_folder = self.arg_parser.add_argument(
            '-f', '--folder', metavar='PATH', help='download save location')

        self.uget = uget.Uget()
        self.youtube_dl = youtube_dl.YoutubeDl()

    def main(self, args: Optional[List[str]] = None) -> Any:
        parsed_args = self.arg_parser.parse_args(args)
        self.logger.debug('Parsed arguments: %s', parsed_args)

        parsed_kwargs = vars(parsed_args)
        url = parsed_kwargs[self.arg_url.dest]
        folder = parsed_kwargs[self.arg_folder.dest]

        self.download(url, folder=folder)

    # TODO add filename option
    def download(self, url: str, folder: Optional[str] = None) -> None:
        if folder is None:
            folder = os.curdir

        try:
            # FIXME youtube URL support detection
            #       https://github.com/ytdl-org/youtube-dl/#how-can-i-detect-whether-a-given-url-is-supported-by-youtube-dl
            self.youtube_dl.download(
                url,
                external_downloader='x-uget',
                output=folder,
                format='bestvideo+bestaudio',
                add_metadata=True,
                verbose=True)
        except youtube_dl.YoutubeDLError as error:
            self.logger.debug(
                'Failed to download using YouTube DL (attempting with uGet)',
                exc_info=error)
            # TODO use same parameters as `enclosure_download.sh`
            self.uget.download(url, folder=folder)


# TODO tests
# TODO GUI?
#      https://github.com/chriskiehl/Gooey
#      https://github.com/PySimpleGUI/PySimpleGUI
#      https://github.com/alfiopuglisi/guietta
if __name__ == '__main__':
    sys.exit(Downloader().main())
