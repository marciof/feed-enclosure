# -*- coding: UTF-8 -*-

# FIXME document (including deps and setup ~/.local/share/liferea/plugins/)
# FIXME tests (including typing, mypy, pycodestyle)
# FIXME error handling
# FIXME proper logging (including to syslog)
# FIXME how to disable built-in Download Manager and have that setting persist?
# FIXME confirm this is API compliant
# FIXME use ShellActivatable and listen for new feed items?
# TODO would be nice to optionally pass the feed article title

# stdlib
from pathlib import Path
import subprocess
import sys

# internal
from gi.repository import GObject, Liferea

PLUGIN_PATH = Path(__file__)
PLUGIN_NAME = PLUGIN_PATH.stem
ENCLOSURE_URL_CMD = PLUGIN_PATH.parent / 'on_enclosure_url'

class ExtCmdPlugin (
        GObject.Object,
        Liferea.Activatable, # Required by `DownloadActivatable`.
        Liferea.DownloadActivatable):

    """
    References:

    - https://github.com/lwindolf/liferea/blob/main/plugins/README.md#plugin-tutorial
    - https://github.com/lwindolf/liferea/blob/main/plugins/download-manager.py
    - https://github.com/lwindolf/liferea/blob/main/src/plugins/download_activatable.c
    - https://github.com/mozbugbox/liferea-plugin-studio
    """

    __gtype_name__ = __qualname__

    # Required by `DownloadActivatable`, even if not used:
    #   gi/types.py: Warning: Object class [PLUGIN] doesn't implement property
    #   'shell' from interface 'LifereaDownloadActivatable'
    shell = GObject.property(type=Liferea.Shell)

    def do_activate(self):
        print('%s.%s' % (PLUGIN_NAME, self.do_activate.__name__),
            file=sys.stderr)

    def do_deactivate(self):
        print('%s.%s' % (PLUGIN_NAME, self.do_deactivate.__name__),
            file=sys.stderr)

    def do_download(self, url):
        print('%s.%s: %s %s'
            % (PLUGIN_NAME, self.do_download.__name__, ENCLOSURE_URL_CMD, url),
            file=sys.stderr)

        subprocess.Popen([ENCLOSURE_URL_CMD, url])
