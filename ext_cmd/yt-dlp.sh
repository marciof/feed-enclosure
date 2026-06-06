#!/bin/sh

# Helper wrappers around `yt-dlp`.
# https://github.com/yt-dlp/yt-dlp

# FIXME document (including dependencies and setup)
# FIXME test (including shellcheck)
# FIXME error handling
# FIXME proper logging (including to syslog)
# TODO check https://github.com/TheFrenchGhosty/TheFrenchGhostys-Ultimate-YouTube-DL-Scripts-Collection

set -e -u

yt() {
    yt-dlp "$@"
}

yt_defaults() {
    # https://github.com/yt-dlp/yt-dlp#filtering-formats
    yt \
        --mtime \
        --no-part \
        --windows-filenames \
        --embed-subs \
        --embed-metadata \
        --embed-thumbnail \
        --output-na-placeholder not_live \
        --match-filter live_status=not_live \
        --format 'bestvideo[height<=?720]+bestaudio/best' \
        "$@"
}

if [ $# -gt 0 ]; then
    yt_defaults "$@"
fi
