#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Converts a TVW Show page's HTML in `stdin` to an episodes RSS feed in `stdout`.

https://tvw.org/shows/
"""

# FIXME document (including dependencies and setup)
# FIXME test
# FIXME error handling
# FIXME proper logging (including to syslog)
# FIXME shebang pointing to venv's Python

# stdlib
import sys

# external
from bs4 import BeautifulSoup
import dateparser
from feedgen.feed import FeedGenerator

# FIXME avoid reading input all at once?
html = sys.stdin.read()

if len(html) == 0:
    # If the source page returns an HTTP 304 Not Modified, then Liferea
    # determines the source TVW page hasn't changed since the last update,
    # and then seems to still invoke this conversion filter with an empty stdin.
    # https://github.com/lwindolf/liferea/issues/925#issuecomment-902992812
    raise SystemExit('No HTML input provided on stdin')

soup = BeautifulSoup(html, 'html.parser')
title = soup.title.get_text()
url = soup.select_one('link[rel=canonical]')['href']

# FIXME <meta>'s description seems to be "The Impact is Sponsored by:"
description = soup.select_one('meta[name=description]')['content']

feed = FeedGenerator()
feed.title(title)
feed.link(href=url)
feed.description(description)

for ep_soup in soup.select('#episodes .video-preview'):
    ep_title = ep_soup.find('h3').get_text()
    ep_url = ep_soup.select_one('a')['href']

    # FIXME find/guess proper timezone
    ep_time_str = ' '.join([t['datetime'] for t in ep_soup.select('time')])
    ep_datetime = dateparser.parse(
        ep_time_str, settings={'RETURN_AS_TIMEZONE_AWARE': True})

    feed_entry = feed.add_entry()
    feed_entry.title(ep_title)
    feed_entry.link(href=ep_url)

    # FIXME should this use `application/x-shockwave-flash` like YouTube does?
    feed_entry.enclosure(url=ep_url, type='text/html', length='')

    feed_entry.published(ep_datetime)
    feed_entry.content(str(ep_soup))

# FIXME print directly to stdout?
print(feed.rss_str(pretty=True, encoding='unicode', xml_declaration=False))
