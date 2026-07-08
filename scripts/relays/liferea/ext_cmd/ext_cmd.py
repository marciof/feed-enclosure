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

        plugin_path: Path = Path(__file__)
        plugin_name: str = plugin_path.stem
        self.on_download_url_env_var: str = 'LIFEREA_ON_DOWNLOAD_URL'
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
        if not cmd:
            self.logger.error(
                'Download aborted: $%s not set', self.on_download_url_env_var)

            if self.is_dbus_activatable:
                self.logger.info(
                    """
D-Bus Activatable detected. Possible fixes:
- either -
(A) Disable `DBusActivatable=true` in Liferea's `.desktop` file, so
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
