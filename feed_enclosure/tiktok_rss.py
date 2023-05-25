# -*- coding: UTF-8 -*-

"""
Outputs an RSS feed of up to 10 videos for a given TikTok user name.
"""

# stdlib
import argparse
import sys
from typing import Any, List, Optional

# external
# FIXME missing type stubs for some external libraries
from feedgen import feed as feedgen  # type: ignore
from tiktokapipy.api import TikTokAPI

# internal
from . import log, os_api


MODULE_DOC = __doc__.strip()


def build_feed(user_name: str, logger: log.Logger) -> feedgen.FeedGenerator:
    with TikTokAPI(navigation_retries=3, navigation_timeout=10) as tik_tok:
        # FIXME takes too long to build a feed and Liferea times out
        user = tik_tok.user(user_name, video_limit=1)
        user_url = 'https://www.tiktok.com/@' + user_name
        logger.info('TikTok user: %s', user)

        feed = feedgen.FeedGenerator()
        feed.id(str(user.id))
        feed.title(user.nickname)
        feed.link({'href': user_url})

        # FIXME add description from user's bio
        # Description is mandatory for RSS feeds.
        # https://www.rssboard.org/rss-specification
        feed.description('-')

        for video in user.videos:
            video_url = user_url + '/video/' + str(video.id)
            logger.info('TikTok video "%s": %s', video.desc, video_url)

            feed_entry = feed.add_entry()

            # FIXME are the title and description the same thing?
            feed_entry.title(video.desc)

            feed_entry.id(str(video.id))
            feed_entry.link({'href': video_url})
            feed_entry.published(video.create_time)
            feed_entry.enclosure(url=video_url, type='')

            # FIXME need to properly encode into HTML
            feed_entry.description('<img src="%s">' % video.video.cover)

        logger.info('Built feed: %s', feed)
        return feed


def build_feed_to_stdout(user_name: str, logger: log.Logger) -> None:
    print(build_feed(user_name, logger).rss_str(pretty=True).decode())


def parse_args(args: Optional[List[str]], logger: log.Logger) -> str:
    arg_parser = argparse.ArgumentParser(description=MODULE_DOC)
    arg_user_name = arg_parser.add_argument('user', help='user name')

    parsed_args = arg_parser.parse_args(args)
    logger.debug('Parsed arguments: %s', parsed_args)

    user_name = vars(parsed_args)[arg_user_name.dest]
    logger.debug('User name: %s', user_name)

    return user_name


def main(args: Optional[List[str]] = None) -> Any:
    logger = None

    try:
        logger = log.create_logger('tiktok_rss')
        build_feed_to_stdout(parse_args(args, logger), logger)
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
