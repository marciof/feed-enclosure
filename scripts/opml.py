#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
OPML parsing and handling helpers.

http://opml.org/spec2.opml
"""

# FIXME document
# FIXME test
# FIXME error handling
# FIXME proper logging (including to syslog)
# FIXME add command for setting encAutoDownload=true?
# FIXME add command for setting filtercmd?

# stdlib
import argparse
from pathlib import Path
import sys
from typing import Iterator, List, Optional, TextIO, NoReturn
from xml.etree.ElementTree import Element

# external
# FIXME missing type stubs for some external libraries
import defusedxml.ElementTree as ElementTree  # type: ignore


class Opml:
    def __init__(self, data: TextIO):
        self.types = {'rss', 'atom'}
        self.data = data
        self.root = None

    def iter_feed_outline(self) -> Iterator[Element]:
        for (event, el) in ElementTree.iterparse(self.data, list({'start'})):
            if self.root is None:
                self.root = el
            elif el.tag == 'outline' and el.attrib.get('type') in self.types:
                yield el

    def set_feed_outline_attr(self, name: str, value: str) -> None:
        for feed in self.iter_feed_outline():
            feed.attrib[name] = value

    def to_string(self) -> str:
        return ElementTree.tostring(self.root, encoding='unicode')


def OpmlAttrNameArgType(arg: str) -> str:
    if len(arg) == 0:
        raise ValueError('Attribute name must not be empty')
    else:
        return arg


def TextIoArgType(arg: str) -> TextIO:
    return Path(arg).open()


def set_feed_attr_arg_cmd(
        opml: Opml, args: argparse.Namespace, output: TextIO = sys.stdout) \
        -> None:

    opml.set_feed_outline_attr(args.name, args.value)
    print(opml.to_string(), file=output)


def main(args: Optional[List[str]] = None) -> NoReturn:
    arg_parser = argparse.ArgumentParser(description=__doc__.strip())
    arg_parser.add_argument(
        '-p', '--path',
        type=TextIoArgType, default=sys.stdin,
        help='path to OPML file or stdin')
    cmd_arg_parser = arg_parser.add_subparsers(required=True)

    set_feed_attr_arg_parser = cmd_arg_parser.add_parser(
        'set-feed-attr', help="set an attribute on feed <outline>'s")
    set_feed_attr_arg_parser.set_defaults(func=set_feed_attr_arg_cmd)
    set_feed_attr_arg_parser.add_argument('name', type=OpmlAttrNameArgType)
    set_feed_attr_arg_parser.add_argument('value')

    parsed_args = arg_parser.parse_args(args)

    with parsed_args.path:
        opml = Opml(parsed_args.path)
        parsed_args.func(opml, parsed_args)
        raise SystemExit()


if __name__ == '__main__':
    main()
