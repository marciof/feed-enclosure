#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Converts a TVW Show page's HTML in `stdin` to an episodes RSS feed in `stdout`.

https://tvw.org/shows/
"""

# /// script
# dependencies = [
#   "beautifulsoup4==4.12.3", # parse/search show's HTML for show/episode's info
#   "dateparser==1.4.0", # parse/search episode's published date
#   "feedgen==1.0.0", # generate show's RSS feed
# ]
# ///

# FIXME document
# FIXME test
# FIXME error handling
# FIXME proper logging (including to syslog)

# stdlib
from datetime import datetime as DateTime
import sys

# external
from bs4 import BeautifulSoup, Tag
from dateparser.search import search_dates
from feedgen.feed import FeedGenerator


def find_show_description(soup: Tag) -> str:
    # Prioritize description on the page, as some shows have the `meta`
    # description as "The Impact is Sponsored by:", which isn't useful.
    details = soup.select_one('#show-details h3 + p')

    if details:
        return details.get_text()

    return soup.select_one('meta[name=description]')['content']


def find_episode_published_date(ep_soup: Tag) -> DateTime:
    # FIXME find/guess proper timezone
    dates = search_dates(
        ' '.join(map(Tag.get_text, ep_soup.select('time'))),
        settings={'RETURN_AS_TIMEZONE_AWARE': True})

    return dates[0][1]


def convert_html_to_feed(html: str) -> FeedGenerator:
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.get_text()
    url = soup.select_one('link[rel=canonical]')['href']
    description = find_show_description(soup)

    feed = FeedGenerator()
    feed.title(title)
    feed.link(href=url)
    feed.description(description)

    for ep_soup in soup.select('#episodes .video-preview'):
        ep_title = ep_soup.find('h3').get_text()
        ep_url = ep_soup.select_one('a')['href']
        ep_datetime = find_episode_published_date(ep_soup)

        feed_entry = feed.add_entry()
        feed_entry.title(ep_title)
        feed_entry.link(href=ep_url)

        # FIXME should this use `application/x-shockwave-flash` like YouTube does?
        feed_entry.enclosure(url=ep_url, type='text/html', length='')

        feed_entry.published(ep_datetime)
        feed_entry.content(str(ep_soup))

    return feed


if __name__ == '__main__':
    # FIXME avoid reading input all at once?
    html = sys.stdin.read()

    # FIXME move to the liferea module
    if len(html) == 0:
        # FIXME have Liferea not call a converter with no data
        # If the source page returns an HTTP 304 Not Modified, then Liferea
        # determines the source TVW page hasn't changed since the last update,
        # and then seems to still invoke this conversion filter with an empty stdin.
        # https://github.com/lwindolf/liferea/issues/925#issuecomment-902992812
        raise SystemExit()

    feed = convert_html_to_feed(html)

    # FIXME print directly to stdout?
    print(feed.rss_str(pretty=True, encoding='unicode', xml_declaration=False))
