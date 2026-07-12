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
import configparser
from functools import partial
import logging
import os
from pathlib import Path
import subprocess
from threading import Thread
from typing import TextIO, Callable, List, Optional

# internal
from gi.repository import Gio, GObject, Liferea


# FIXME seems to be missing from outside the plugin
logging.basicConfig()


# FIXME tests (including mypy, pycodestyle)
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

        app: Optional[Gio.Application] = Gio.Application.get_default()
        app_flags: Optional[Gio.ApplicationFlags] = (
            None if app is None
            else app.get_flags())

        info = configparser.ConfigParser()
        info.read(plugin_path.parent / (plugin_name + '.plugin'))

        self.on_download_url_env_var: str \
            = info['Configuration']['OnDownloadUrlEnvVar']

        # See https://docs.gtk.org/gio/flags.ApplicationFlags.html#is_service
        # See https://dbus.freedesktop.org/doc/dbus-specification.html
        # See https://developer.gnome.org/documentation/guidelines/maintainer/integrating.html#d-bus-activation
        self.is_dbus_activatable: bool = (
            app_flags is not None
            and (app_flags & Gio.ApplicationFlags.IS_SERVICE) != 0)

        self.logger: logging.Logger = logging.getLogger('plugin.' + plugin_name)
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug(
            '__init__ path=%s; flags=%s; dbus=%s; $%s=%s',
            plugin_path,
            None if app_flags is None else bin(app_flags),
            self.is_dbus_activatable,
            self.on_download_url_env_var,
            self.on_download_url)


    @property
    def on_download_url(self) -> Optional[str]:
        return os.getenv(self.on_download_url_env_var)


    # inherit Liferea.Activatable
    def do_activate(self) -> None:
        self.logger.info('Activate')


    # inherit Liferea.Activatable
    def do_deactivate(self) -> None:
        self.logger.info('Deactivate')


    # inherit Liferea.DownloadActivatable
    def do_download(self, url: str) -> None:
        command = self.on_download_url

        if command is not None:
            self.logger.info('Download command=%s; url=%s', command, url)
            self.run_ext_cmd([command, url])
        else:
            self.logger.error(
                'Download aborted: $%s not set: looked in %s',
                self.on_download_url_env_var,
                sorted(os.environ.keys()))

            if self.is_dbus_activatable:
                self.logger.info(
                    'D-Bus Activatable detected. See README for help.',
                    self.on_download_url_env_var)


    # TODO would be nice to optionally pass the feed article title to ext cmds
    # TODO might be nice to use `shlex.split` and/or `os.path.expanduser/vars`
    def run_ext_cmd(self, command: List[str]) -> None:
        process = subprocess.Popen(command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

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
            process.stdout,
            partial(self.logger.info, f'[{process.pid}] %s'),
        ]).start()

        Thread(target=log_output, args=[
            process.stderr,
            partial(self.logger.error, f'[{process.pid}] %s'),
        ]).start()

        Thread(target=log_exit).start()
