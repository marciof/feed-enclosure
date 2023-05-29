# -*- coding: UTF-8 -*-

"""
Rewrites a TikTok user's HTML page (in stdin) into RSS (in stdout).
"""

# stdlib
import argparse
from datetime import datetime, timezone
import json
import sys
from typing import Any, List, Optional

# external
# FIXME missing type stubs for some external libraries
import bs4
from feedgen import feed as feedgen  # type: ignore

# internal
from . import log, os_api


MODULE_DOC = __doc__.strip()


# TODO refactor duplicate parsing of feed properties?
def build_feed_from_html(user_page_html: str, logger: log.Logger) -> str:
    page = bs4.BeautifulSoup(user_page_html, 'html5lib')

    title = page.title.string
    url = page.find('link', attrs={'rel': 'canonical'})['href']
    description = page.find('meta', attrs={'property': 'og:description'})[
        'content']

    logger.info('TikTok user: %s', url)

    feed = feedgen.FeedGenerator()
    feed.title(title)
    feed.link({'href': url})
    feed.description(description)

    for video in page.find_all(attrs={'data-e2e': 'user-post-item'}):
        link_tag = video.find('a')
        cover_tag = link_tag.find('img')

        video_url = link_tag['href']
        video_title = cover_tag['alt']
        video_cover_url = cover_tag['src']

        # FIXME add date
        logger.info('TikTok video "%s": %s', video_title, video_url)
        feed_entry = feed.add_entry()

        feed_entry.id(video_url)
        feed_entry.title(video_title)
        feed_entry.link({'href': video_url})
        feed_entry.enclosure(url=video_url, type='')

        # FIXME encode safely into HTML
        feed_entry.description('<img src="%s">' % video_cover_url)

    return feed.rss_str(pretty=True).decode()


def build_feed_from_json(user_page_html: str, logger: log.Logger) -> str:
    page = bs4.BeautifulSoup(user_page_html, 'html5lib')
    state = json.loads(page.find('script', attrs={'id': 'SIGI_STATE'}).string)

    title = page.title.string
    url = page.find('link', attrs={'rel': 'canonical'})['href']
    description = page.find('meta', attrs={'property': 'og:description'})[
        'content']

    logger.info('TikTok user: %s', url)

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

        logger.info('TikTok video "%s": %s', video_title, video_url)
        feed_entry = feed.add_entry()

        feed_entry.id(video_url)
        feed_entry.title(video_title)
        feed_entry.link({'href': video_url})
        feed_entry.enclosure(url=video_url, type='')
        feed_entry.published(datetime.fromtimestamp(video_created_timestamp,
            tz=timezone.utc))

        # FIXME encode safely into HTML
        feed_entry.description('<img src="%s">' % video_cover_url)

    return feed.rss_str(pretty=True).decode()


# FIXME resort to parsing HTML if JSON fails
def build_feed_to_stdout(logger: log.Logger) -> None:
    # FIXME `feedparser` breaks on detecting the encoding of the input
    #       data when given a file object (eg `sys.stdin`) that when
    #       `read` gives a string-like object, since the regex is a bytes
    #       pattern (see `feedparser.encodings.RE_XML_PI_ENCODING`). As a
    #       workaround read `sys.stdin` to yield a string.
    print(build_feed_from_json(sys.stdin.read(), logger))


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
