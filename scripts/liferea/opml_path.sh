#!/bin/sh

# Stdout: path to feed list OPML file if it exists, nothing otherwise
# Exit: 0 if it exists, >0 otherwise
#
# References:
# - XDG Spec: https://specifications.freedesktop.org/basedir/latest/#variables
# - Liferea source: https://raw.githubusercontent.com/lwindolf/liferea/refs/heads/main/src/node_source.c#:~:text=feedlist.opml

set -o errexit -o nounset
realpath -e "${XDG_CONFIG_HOME:-"$HOME/.config"}/liferea/feedlist.opml"
