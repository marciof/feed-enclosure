"""
"""

# FIXME document
# FIXME test
# FIXME error handling
# FIXME logging
# FIXME typing
#   https://github.com/lwindolf/liferea/blob/main/src/plugins/liferea_activatable.h
#   https://github.com/lwindolf/liferea/blob/main/src/plugins/download_activatable.h

import os
from pathlib import Path
import subprocess

# FIXME requirements.txt PyGObject
from gi.repository import GObject, Liferea


# FIXME ensure correct paths for config and plugin (broken website links too?)
#   https://lzone.de/liferea/blog/Writing-Liferea-Plugins-Tutorial-Part-1.html
#   ~/.config/liferea/plugins/
#   ~/.local/share/liferea/plugins/
# FIXME avoid hardcoding paths, use `xdg_base_dirs`?
PLUGIN_NAME = os.path.basename(os.path.dirname(__file__))
CONFIG_HOME = Path(os.getenv('XDG_CONFIG_HOME', str(Path.home() / '.config')))
CONFIG_DIR = CONFIG_HOME / 'liferea' / 'plugins' / PLUGIN_NAME
ENCLOSURE_URL_CMD = CONFIG_DIR / 'enclosure_url'


# FIXME use ShellActivatable and listen for new feed items?
class ExtCmdPlugin (GObject.Object, Liferea.Activatable, Liferea.DownloadActivatable):
    __gtype_name__ = 'ExtCmdPlugin'
    shell = GObject.property(type=Liferea.Shell)


    def __init__(self):
        super(ExtCmdPlugin, self).__init__()
        self.enclosure_url_cmd = None


    def do_activate(self):
        try:
            self.enclosure_url_cmd = ENCLOSURE_URL_CMD.read_text()
        except FileNotFoundError:
            pass


    def do_deactivate(self):
        self.enclosure_url_cmd = None


    def do_download(self, url):
        if self.enclosure_url_cmd is None:
            return

        try:
            # FIXME don't use the shell?
            subprocess.Popen(
                self.enclosure_url_cmd.replace('%s', url), shell=True)
        except OSError:
            pass
