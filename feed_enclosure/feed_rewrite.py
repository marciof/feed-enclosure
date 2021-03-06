# -*- coding: UTF-8 -*-

"""
Rewrites RSS/Atom feeds (in stdin) into RSS (in stdout) so that the best
enclosures are chosen, and also rewritten to have the best quality possible.
Accepts whatever kinds of feed `feedparser` supports.

Enclosure URLs will also have their associated feed entry title saved in the
URL fragment part as a file name, so downloaders can use it if/when needed.
"""

# stdlib
import argparse
import os.path
import sys
from typing import Any, List, Optional
from urllib.parse import urldefrag, urlparse

# external
# FIXME missing type stubs for some external libraries
from feedgen import feed as feedgen  # type: ignore
import feedparser  # type: ignore
from pathvalidate import sanitize_filename

# internal
from . import url_rewrite, log, os_api


MODULE_DOC = __doc__.strip()


def list_parsed_feed_entry_enclosure_urls(
        feed_entry: feedparser.FeedParserDict) \
        -> List[str]:

    """
    List all feed entry enclosures found, ordered from "best" to "worst".
    """

    urls = []

    if 'feedburner_origenclosurelink' in feed_entry:
        urls.append(feed_entry.feedburner_origenclosurelink)

    for enclosure in feed_entry.enclosures:
        urls.append(enclosure['href'])

    for media in feed_entry.media_content:
        urls.append(media['url'])

    return urls


# TODO figure out a more "proper" way to attach meta-data
def add_title_filename_to_url(url: str, title: str) -> str:
    """
    Add a title in the URL fragment part for downloaders to use when the
    original URL file name isn't human readable (URL fragments are client-side
    only, so safe to remove).
    """

    (defrag_url, fragment) = urldefrag(url)
    path = urlparse(defrag_url).path
    (file_root, file_ext) = os.path.splitext(path)

    return defrag_url + '#' + sanitize_filename(title + file_ext)


def rebuild_parsed_feed_entry(
        feed_entry: feedparser.FeedParserDict,
        new_feed: feedgen.FeedGenerator) \
        -> feedgen.FeedEntry:

    new_feed_entry = new_feed.add_entry()
    new_feed_entry.title(feed_entry.title)

    if 'id' in feed_entry:
        new_feed_entry.id(feed_entry.id)
    if 'link' in feed_entry:
        new_feed_entry.link({'href': feed_entry.link})
    if 'published' in feed_entry:
        new_feed_entry.published(feed_entry.published)
    if 'updated' in feed_entry:
        new_feed_entry.updated(feed_entry.updated)
    if 'summary' in feed_entry:
        new_feed_entry.summary(feed_entry.summary)
    if 'description' in feed_entry:
        new_feed_entry.description(feed_entry.description)

    if ('content' in feed_entry) and (len(feed_entry.content) > 0):
        new_feed_entry.content(
            content=feed_entry.content[0]['value'],
            type='')

    return new_feed_entry


def rebuild_parsed_feed(
        feed: feedparser.FeedParserDict,
        logger: log.Logger) \
        -> feedgen.FeedGenerator:

    new_feed = feedgen.FeedGenerator()

    if 'id' in feed.feed:
        new_feed.id(feed.feed.id)
    if 'title' in feed.feed:
        new_feed.title(feed.feed.title)
    if 'link' in feed.feed:
        new_feed.link({'href': feed.feed.link})
    if 'published' in feed.feed:
        new_feed.pubDate(feed.feed.published)

    if 'description' in feed.feed:
        new_feed.description(feed.feed.description)
    else:
        # Description is mandatory for RSS feeds.
        # https://www.rssboard.org/rss-specification
        logger.debug('No feed description found, setting it anyway.')
        new_feed.description('-')

    return new_feed


# TODO feed handling errors don't indicate which feed it was on
def rebuild_feed(feed_xml: str, logger: log.Logger) -> str:
    # FIXME Liferea sends no data on stdin when it gets an HTTP 304
    #       https://github.com/lwindolf/liferea/issues/925#issuecomment-902992812
    if feed_xml.strip() == '':
        raise Exception('Feed XML is an empty string')

    parsed_feed = feedparser.parse(feed_xml)
    is_bozo = parsed_feed.get('bozo', False)
    bozo_exception = parsed_feed.get('bozo_exception')
    logger.debug('Feed bozo? %s', is_bozo)

    if is_bozo:
        logger.warning('Feed bozo exception:', bozo_exception)

    new_feed = rebuild_parsed_feed(parsed_feed, logger)

    for entry in parsed_feed.entries:
        new_entry = rebuild_parsed_feed_entry(entry, new_feed)
        urls = list_parsed_feed_entry_enclosure_urls(entry)

        if len(urls) > 0:
            url = url_rewrite.process_url(urls[0])
            titled_url = add_title_filename_to_url(url, entry.title)
            logger.debug('Enclosure URL for "%s": %s', entry.title, titled_url)
            new_entry.enclosure(url=titled_url, type='')
        else:
            logger.warning(
                'No enclosure URLs found in "%s".', entry.title)

    logger.info('Rebuilt feed: %s', new_feed.title())
    return new_feed.rss_str(pretty=True).decode()


def rebuild_feed_from_stdin_to_stdout(logger: log.Logger) -> None:
    # FIXME `feedparser` breaks on detecting the encoding of the input
    #       data when given a file object (eg `sys.stdin`) that when
    #       `read` gives a string-like object, since the regex is a bytes
    #       pattern (see `feedparser.encodings.RE_XML_PI_ENCODING`). As a
    #       workaround read `sys.stdin` to yield a string.
    print(rebuild_feed(sys.stdin.read(), logger))


def parse_args(args: Optional[List[str]], logger: log.Logger) -> None:
    parser = argparse.ArgumentParser(description=MODULE_DOC)
    parser.parse_args(args)

    if sys.stdin.isatty():
        logger.warning('Stdin is a terminal (possibly connected to keyboard)')
        logger.warning(parser.format_usage().strip())


def main(args: Optional[List[str]] = None) -> Any:
    logger = None

    try:
        logger = log.create_logger('feed_rewrite')
        parse_args(args, logger)
        rebuild_feed_from_stdin_to_stdout(logger)
        return os_api.EXIT_SUCCESS
    except SystemExit:
        raise
    except BaseException as error:
        if logger is None:
            raise
        else:
            logger.error('Failed to rewrite feed', exc_info=error)
        return os_api.EXIT_FAILURE


# TODO tests
if __name__ == '__main__':
    sys.exit(main())
