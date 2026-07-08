# -*- coding: UTF-8 -*-

# FIXME document (including deps)
# FIXME tests (including typing, mypy, pycodestyle)
# FIXME error handling
# FIXME how to disable built-in Download Manager and have that setting persist?
# TODO would be nice to optionally pass the feed article title to ext cmds

# stdlib
import logging
import os
from pathlib import Path
import subprocess

# internal
from gi.repository import GObject, Liferea


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


    def __init__(self):
        super().__init__()

        self.plugin_path: Path = Path(__file__)
        self.plugin_name: str = self.plugin_path.stem
        self.is_dbus_activatable: bool = 'DBUS_STARTER_ADDRESS' in os.environ

        logging.basicConfig()

        self.logger: logging.Logger = logging.getLogger(
            'plugin.' + self.plugin_name)
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug(
            '__init__: path=%s; name=%s; dbus=%s',
            self.plugin_path,
            self.plugin_name,
            self.is_dbus_activatable)


    def do_activate(self):
        self.logger.info('Activate')


    def do_deactivate(self):
        self.logger.info('Deactivate')


    def do_download(self, url):
        cmd = self.plugin_path.parent / 'on_enclosure_url'
        self.logger.info('Download: cmd=%s; url=%s', cmd, url)
        subprocess.Popen([cmd, url])
