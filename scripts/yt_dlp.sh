#!/bin/sh

# `yt-dlp` helper wrappers.
# Calls `yt_defaults` by default, unless sourced.
# https://github.com/yt-dlp/yt-dlp
#
# Arguments: [pass-through]

# FIXME document (including dependencies and setup)
# FIXME test (including shellcheck)
# FIXME error handling
# FIXME proper logging (including to syslog)
# TODO check https://github.com/TheFrenchGhosty/TheFrenchGhostys-Ultimate-YouTube-DL-Scripts-Collection

set -e -u

yt() {
    yt-dlp "$@"
}

# Arguments: URL
# Exit: 0 if live, 1 otherwise
yt_is_livestream() {
    # Some upcoming livestreams don't have a video format available yet,
    # so ignore related warnings and errors.
    # https://github.com/jmbannon/ytdl-sub/issues/1323
    yt \
        --no-warnings \
        --ignore-no-formats-error \
        --output-na-placeholder not_live \
        --print live_status \
        "$1" \
    | grep --quiet --invert-match --ignore-case -F not_live
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

if [ "$(basename "$(readlink -e "$0")")" = 'yt_dlp.sh' ]; then
    yt_defaults "$@"
fi
