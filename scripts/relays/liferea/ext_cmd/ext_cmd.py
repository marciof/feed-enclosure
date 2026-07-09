# -*- coding: UTF-8 -*-

"""
Plugin that runs external commands on various events.

Supported Events
================

Enclosure Download
------------------

Reinstates the external downloader tool functionality that was removed in
`v1.15.9 <https://github.com/lwindolf/liferea/releases/tag/v1.15.9>`_, by using
an environment variable to specify what command to run with an enclosure URL.

Why
^^^

- Symlinks aren't cross-platform and aren't portable.
- Not all VCS' support symlinks.
- Avoids polluting `$PATH`, and it's also too implicit.
- Environment variables can be VCS-ed as "Configuration as Code".
- Protocol handler registration (eg. `extcmd://`) is too involved.
"""


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

    - https://github.com/lwindolf/liferea/blob/v1.16.7/plugins/README.md#plugin-tutorial
    - https://github.com/lwindolf/liferea/blob/v1.16.7/plugins/download-manager.py
    - https://github.com/lwindolf/liferea/blob/v1.16.7/src/plugins/download_activatable.c
    - https://github.com/mozbugbox/liferea-plugin-studio
    """

    __gtype_name__ = __qualname__

    # Required by `DownloadActivatable`, even if not used:
    #   gi/types.py: Warning: Object class [PLUGIN] doesn't implement property
    #   'shell' from interface 'LifereaDownloadActivatable'
    shell = GObject.property(type=Liferea.Shell)


    def __init__(self):
        super().__init__()

        plugin_path: Path = Path(__file__)
        plugin_name: str = plugin_path.stem
        self.on_download_url_env_var: str = 'LIFEREA_ON_DOWNLOAD_URL'

        # See https://dbus.freedesktop.org/doc/dbus-specification.html
        self.is_dbus_activatable: bool = 'DBUS_STARTER_ADDRESS' in os.environ

        logging.basicConfig()
        self.logger: logging.Logger = logging.getLogger('plugin.' + plugin_name)
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug(
            '__init__ path=%s; name=%s; dbus=%s',
            plugin_path,
            plugin_name,
            self.is_dbus_activatable)


    def do_activate(self) -> None:
        self.logger.info('Activate')


    def do_deactivate(self) -> None:
        self.logger.info('Deactivate')


    def do_download(self, url: str) -> None:
        cmd: str = os.getenv(self.on_download_url_env_var, '')

        # TODO see LibnotifyPlugin for QoL ideas to notify user of errors
        #   https://github.com/lwindolf/liferea/blob/v1.16.7/plugins/libnotify.py
        if not cmd:
            self.logger.error(
                'Download aborted: $%s not set', self.on_download_url_env_var)

            if self.is_dbus_activatable:
                self.logger.info(
                    """
D-Bus Activatable detected. Possible fixes:
- either -
(A) Set `DBusActivatable=false` in Liferea's `.desktop` file, so
    that environment variables are passed to it.
    https://developer.gnome.org/documentation/guidelines/maintainer/integrating.html#d-bus-activation
- or -
(B) Run command: dbus-update-activation-environment %s=PATH_TO_EXECUTABLE
- then -
    Restart Liferea.
                    """.lstrip(),
                    self.on_download_url_env_var)

            return

        self.logger.info('Download cmd=%s; url=%s', cmd, url)
        subprocess.Popen([cmd, url])
