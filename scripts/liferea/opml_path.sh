#!/bin/sh

# Stdout: path to feed list OPML file if it exists, nothing otherwise
# Exit: 0 if it exists, >0 otherwise
#
# References:
# - XDG Spec: https://specifications.freedesktop.org/basedir/latest/#variables
# - Liferea man page: https://github.com/lwindolf/liferea/blob/main/data/man/liferea.1

# TODO request Liferea cmdline flag to print path to OPML file

set -o errexit -o nounset
realpath -e "${XDG_CONFIG_HOME:-"$HOME/.config"}/liferea/feedlist.opml"
