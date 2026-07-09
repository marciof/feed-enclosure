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


# stdlib
from functools import partial
import logging
import os
from pathlib import Path
import subprocess
from threading import Thread
from typing import TextIO, Callable, List

# internal
from gi.repository import GObject, Liferea


# FIXME seems to be missing from outside the plugin
logging.basicConfig()


# FIXME tests (including typing, mypy, pycodestyle)
# FIXME disable built-in Download Manager?
# TODO see LibnotifyPlugin for QoL ideas to notify user of errors
#   https://github.com/lwindolf/liferea/blob/v1.16.7/plugins/libnotify.py
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


    # FIXME instantiated 2x
    def __init__(self):
        super().__init__()

        plugin_path: Path = Path(__file__)
        plugin_name: str = plugin_path.stem
        self.on_download_url_env_var: str = 'LIFEREA_ON_DOWNLOAD_URL'

        # See https://dbus.freedesktop.org/doc/dbus-specification.html
        self.is_dbus_activatable: bool = 'DBUS_STARTER_ADDRESS' in os.environ

        self.logger: logging.Logger = logging.getLogger('plugin.' + plugin_name)
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug(
            '__init__ path=%s; name=%s; dbus=%s',
            plugin_path,
            plugin_name,
            self.is_dbus_activatable)


    # inherit Liferea.Activatable
    def do_activate(self) -> None:
        self.logger.info('Activate')


    # inherit Liferea.Activatable
    def do_deactivate(self) -> None:
        self.logger.info('Deactivate')


    # inherit Liferea.DownloadActivatable
    def do_download(self, url: str) -> None:
        command: str = os.getenv(self.on_download_url_env_var, '')

        if command:
            self.logger.info('Download command=%s; url=%s', command, url)
            self.run_ext_cmd([command, url])
        else:
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


    # TODO would be nice to optionally pass the feed article title to ext cmds
    def run_ext_cmd(self, command: List[str]) -> None:
        process = subprocess.Popen(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.logger.info('Run pid=%s', process.pid)

        def log_output(pipe: TextIO, log: Callable[[str], None]) -> None:
            with pipe:
                for line in pipe:
                    log(line)

        def log_exit() -> None:
            code = process.wait()
            log = (self.logger.info if code == os.EX_OK else self.logger.error)
            log('Run pid=%s; exit=%s', process.pid, code)

        Thread(target=log_output, args=[
            process.stdout, partial(self.logger.info, f'[{process.pid}] %s'),
        ]).start()

        Thread(target=log_output, args=[
            process.stderr, partial(self.logger.error, f'[{process.pid}] %s'),
        ]).start()

        Thread(target=log_exit).start()
