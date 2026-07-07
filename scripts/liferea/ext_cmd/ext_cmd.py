# -*- coding: UTF-8 -*-

"""
https://github.com/lwindolf/liferea/tree/main/plugins
https://github.com/mozbugbox/liferea-plugin-studio
"""

# FIXME document (including dependencies and setup)
#   https://github.com/lwindolf/liferea/blob/main/plugins/README.md#plugin-tutorial
#   ~/.local/share/liferea/plugins/
# FIXME tests (including typing, mypy, pycodestyle)
# FIXME error handling
# FIXME proper logging (including to syslog)

# stdlib
from pathlib import Path
import subprocess
import sys

# FIXME requirements.txt PyGObject
from gi.repository import GObject, Liferea

PLUGIN_PATH = Path(__file__)
PLUGIN_NAME = PLUGIN_PATH.stem
ENCLOSURE_URL_CMD = PLUGIN_PATH.parent / 'on_enclosure_url'

# FIXME how to disable built-in Download Manager and have that setting persist?
# FIXME confirm with author so this is API compliant
# FIXME use ShellActivatable and listen for new feed items?
class ExtCmdPlugin (GObject.Object, Liferea.Activatable, Liferea.DownloadActivatable):
    __gtype_name__ = __qualname__
    shell = GObject.property(type=Liferea.Shell)

    def do_activate(self):
        print(f'{PLUGIN_NAME}.activate', file=sys.stderr)

    def do_deactivate(self):
        print(f'{PLUGIN_NAME}.deactivate', file=sys.stderr)

    def do_download(self, url):
        # TODO would be nice to optionally pass the feed article title
        print(f"{PLUGIN_NAME}.download: {ENCLOSURE_URL_CMD} '{url}'", file=sys.stderr)
        subprocess.Popen([ENCLOSURE_URL_CMD, url])
