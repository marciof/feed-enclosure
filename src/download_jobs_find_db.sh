#!/bin/sh

# Prints the path to the download jobs recfile database (may not exist).
# https://www.gnu.org/software/recutils/
#
# Arguments: none
# Stdin: none
# Stdout: path to download jobs recfile
#
# Test dependencies:
#   ../tst/lint_shell.sh

set -e -u

USER_CONFIG_PATH="${XDG_CONFIG_HOME:-$HOME/.config}"
FEED_ENCLOSURE_CONFIG_PATH="$USER_CONFIG_PATH/feed-enclosure"

printf '%s\n' "$FEED_ENCLOSURE_CONFIG_PATH/download-jobs.rec"