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

    def __init__(
            self,
            default_folder: str = os.curdir,
            default_livestreams: bool = True):

        self.logger = log.create_logger('download')
        self.default_folder = default_folder
        self.default_livestreams = default_livestreams

        self.arg_parser = argparse.ArgumentParser(description=MODULE_DOC)
        self.arg_url = self.arg_parser.add_argument(
            'url', help='URL to download')
        self.arg_path = self.arg_parser.add_argument(
            '-p', '--path',
            default=self.default_folder,
            help='download save location (default: %s)' % self.default_folder)
        self.arg_livestreams = self.arg_parser.add_argument(
            '--livestreams',
            action=argparse.BooleanOptionalAction,
            default=self.default_livestreams,
            help='allow live streams')

        self.uget = uget.Uget()
        self.youtube_dl = youtube_dl.YoutubeDl()

    def main(self, args: Optional[List[str]] = None) -> Any:
        parsed_args = self.arg_parser.parse_args(args)
        self.logger.debug('Parsed arguments: %s', parsed_args)

        parsed_kwargs = vars(parsed_args)
        url = parsed_kwargs[self.arg_url.dest]
        path = parsed_kwargs[self.arg_path.dest]
        livestreams = parsed_kwargs[self.arg_livestreams.dest]

        self.download(url, path=path, livestreams=livestreams)

    # FIXME filenames with emojis/Unicode break Dropbox upload?
    # FIXME fails on TikTok videos with very long titles
    # FIXME output from yt-dlp isn't logged
    # TODO ensure downloads can be paused and resumed
    # TODO normalize file names? https://github.com/woodgern/confusables
    def download(
            self,
            url: str,
            path: Optional[str] = None,
            livestreams: Optional[bool] = None) \
            -> None:

        if path is None:
            path = self.default_folder

        match_filters = None

        if livestreams is not None and not livestreams:
            match_filters = '!is_live'

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
                match_filters=match_filters,
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
# TODO GUI notification of download errors or significant events?
#      eg. ffmpeg muxing start/end, error "downloading" livestreams, etc
if __name__ == '__main__':
    sys.exit(Downloader().main())
