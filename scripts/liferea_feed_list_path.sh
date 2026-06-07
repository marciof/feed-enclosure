#!/bin/sh

# Stdout: path to Liferea's feed list OPML file
# https://lzone.de/liferea/

# FIXME add command for setting encAutoDownload=true
# FIXME add command for setting filtercmd

set -e -u

# https://specifications.freedesktop.org/basedir/latest/#variables
echo "${XDG_CONFIG_HOME:-"$HOME/.config"}/liferea/feedlist.opml"
