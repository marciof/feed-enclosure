# -*- coding: UTF-8 -*-

# FIXME document
# FIXME test
# FIXME error handling
# FIXME proper logging (including to syslog)
# FIXME typing
#   https://github.com/lwindolf/liferea/blob/main/src/plugins/liferea_activatable.h
#   https://github.com/lwindolf/liferea/blob/main/src/plugins/download_activatable.h

# stdlib
import os
from pathlib import Path
import subprocess
import sys

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

# FIXME confirm with author so this is API compliant
# FIXME use ShellActivatable and listen for new feed items?
#   https://github.com/mozbugbox/liferea-plugin-studio
#   https://github.com/lwindolf/liferea/tree/main/plugins
class ExtCmdPlugin (GObject.Object, Liferea.Activatable, Liferea.DownloadActivatable):
    __gtype_name__ = 'ExtCmdPlugin'
    shell = GObject.property(type=Liferea.Shell)

    def do_activate(self):
        print(f'{PLUGIN_NAME}/activate', file=sys.stderr)

    def do_deactivate(self):
        print(f'{PLUGIN_NAME}/deactivate', file=sys.stderr)

    def do_download(self, url):
        print(f"{PLUGIN_NAME}/download: {ENCLOSURE_URL_CMD} '{url}'", file=sys.stderr)
        subprocess.Popen([ENCLOSURE_URL_CMD, url])
