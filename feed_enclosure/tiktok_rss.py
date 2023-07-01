# -*- coding: UTF-8 -*-

"""
Rewrites a TikTok user's HTML page (in stdin) into RSS (in stdout).
"""

# stdlib
import argparse
from datetime import datetime, timezone
import html
import json
import sys
from typing import Any, List, Optional, TextIO

# external
# FIXME missing type stubs for some external libraries
import bs4
from feedgen import feed as feedgen  # type: ignore

# internal
from . import log, os_api


MODULE_DOC = __doc__.strip()


def build_feed_from_json(
        user_page_html: str | TextIO,
        logger: log.Logger) \
        -> str:

    page = bs4.BeautifulSoup(user_page_html, 'html5lib')
    state_element = page.find('script', attrs={'id': 'SIGI_STATE'})

    # TODO logging and proper exception
    if state_element is None:
        raise Exception('No state element found in user page HTML: %s' % page)

    state = json.loads(state_element.string)

    title = page.title.string
    url = page.find('link', attrs={'rel': 'canonical'})['href']
    description = page.find('meta', attrs={'property': 'og:description'})[
        'content']

    logger.info('User at <%s>: %s', url, title)

    feed = feedgen.FeedGenerator()
    feed.title(title)
    feed.link({'href': url})
    feed.description(description)

    for video_id, video_props in state['ItemModule'].items():
        video_url = url + '/video/' + video_id

        # FIXME some titles are very long (use ellipsis / summarize)
        video_title = video_props['desc']
        video_created_timestamp = int(video_props['createTime'])
        video_cover_url = video_props['video']['cover']

        logger.info('Video "%s": %s', video_title, video_url)
        feed_entry = feed.add_entry()

        feed_entry.id(video_url)
        feed_entry.title(video_title)
        feed_entry.link({'href': video_url})
        feed_entry.enclosure(url=video_url, type='')
        feed_entry.published(datetime.fromtimestamp(
            video_created_timestamp, tz=timezone.utc))

        feed_entry.description(
            '<img src="%s">' % html.escape(video_cover_url, quote=True))

    return feed.rss_str(pretty=True).decode()


def build_feed_to_stdout(logger: log.Logger) -> None:
    print(build_feed_from_json(sys.stdin, logger))


def parse_args(args: Optional[List[str]], logger: log.Logger) -> None:
    parser = argparse.ArgumentParser(description=MODULE_DOC)
    parser.parse_args(args)

    if sys.stdin.isatty():
        logger.warning('Stdin is a terminal (possibly connected to keyboard)')
        logger.warning(parser.format_usage().strip())


def main(args: Optional[List[str]] = None) -> Any:
    logger = None

    try:
        logger = log.create_logger('tiktok_rss')
        parse_args(args, logger)
        build_feed_to_stdout(logger)
        return os_api.EXIT_SUCCESS
    except SystemExit:
        raise
    except BaseException as error:
        if logger is None:
            raise
        else:
            logger.error('Failed to build feed', exc_info=error)
        return os_api.EXIT_FAILURE


# TODO tests
if __name__ == '__main__':
    sys.exit(main())
