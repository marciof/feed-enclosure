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

    # FIXME filenames with emojis/Unicode break Dropbox upload?
    # FIXME fails on TikTok videos with very long titles
    # TODO ensure downloads can be paused and resumed
    def download(self, url: str, path: Optional[str] = None) -> None:
        if path is None:
            path = self.default_folder

        try:
            if path == '-':
                path = os.path.join(self.default_folder, path)

            # FIXME youtube URL support detection
            self.youtube_dl.download(
                url,
                output=path.replace('%', '%%'),
                # TODO expose format?
                # TODO option to pick best quality using `url_rewrite`?
                format='bestvideo+bestaudio/best',
                add_metadata=True,
                verbose=True)
        except youtube_dl.YoutubeDLError as error:
            # TODO hide Youtube DL error log when it's unsupported
            # TODO attempt to extract metadata from IGN Daily Fix videos?
            self.logger.debug(
                'Failed to download using YouTube DL (attempting with uGet)',
                exc_info=error)

            self.uget.download(url, path=path, quiet=True, wait=True)


# TODO tests
# TODO GUI?
#      https://github.com/chriskiehl/Gooey
#      https://github.com/PySimpleGUI/PySimpleGUI
#      https://github.com/alfiopuglisi/guietta
# TODO GUI notification of download errors or significant events?
#      eg. ffmpeg muxing start/end, error "downloading" livestreams, etc
if __name__ == '__main__':
    sys.exit(Downloader().main())
