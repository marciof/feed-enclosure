# -*- coding: UTF-8 -*-

"""
Wraps the various download tools to pick the most appropriate for downloading
feed enclosures.
"""

# stdlib
import argparse
import os
import os.path
import sys
from typing import Any, List, Optional

# internal
from . import log, uget, youtube_dl


MODULE_DOC = __doc__.strip()


class Downloader:

    def __init__(self, default_folder: str = os.curdir):
        self.logger = log.create_logger('download')
        self.default_folder = default_folder

        self.arg_parser = argparse.ArgumentParser(description=MODULE_DOC)
        self.arg_url = self.arg_parser.add_argument(
            'url', help='URL to download')
        self.arg_path = self.arg_parser.add_argument(
            '-p', '--path', metavar='PATH', help='download save location')

        self.uget = uget.Uget()
        self.youtube_dl = youtube_dl.YoutubeDl()

    def main(self, args: Optional[List[str]] = None) -> Any:
        parsed_args = self.arg_parser.parse_args(args)
        self.logger.debug('Parsed arguments: %s', parsed_args)

        parsed_kwargs = vars(parsed_args)
        url = parsed_kwargs[self.arg_url.dest]
        path = parsed_kwargs[self.arg_path.dest]

        self.download(url, path=path)

    def download(self, url: str, path: Optional[str] = None) -> None:
        if path is None:
            path = self.default_folder

        try:
            if path == '-':
                path = os.path.join(self.default_folder, path)

            # FIXME youtube URL support detection
            #       https://github.com/ytdl-org/youtube-dl/#how-can-i-detect-whether-a-given-url-is-supported-by-youtube-dl
            self.youtube_dl.download(
                url,
                external_downloader=self.youtube_dl.uget_external_downloader,
                output=path.replace('%', '%%'),
                # TODO expose format?
                # TODO option to pick best quality using `url_rewrite`?
                format='bestvideo[height<=?1080]+bestaudio/best[height<=?1080]/best',
                add_metadata=True,
                verbose=True)
        except youtube_dl.YoutubeDLError as error:
            # TODO hide Youtube DL error log when it's unsupported
            self.logger.debug(
                'Failed to download using YouTube DL (attempting with uGet)',
                exc_info=error)

            self.uget.download(url, path=path, quiet=True, wait=True)


# TODO tests
# TODO GUI?
#      https://github.com/chriskiehl/Gooey
#      https://github.com/PySimpleGUI/PySimpleGUI
#      https://github.com/alfiopuglisi/guietta
if __name__ == '__main__':
    sys.exit(Downloader().main())
