#!/bin/sh

# `yt-dlp` helper wrappers.
# https://github.com/yt-dlp/yt-dlp

# FIXME document (including dependencies and setup)
# FIXME test (including shellcheck)
# FIXME error handling
# FIXME proper logging (including to syslog)
# TODO check https://github.com/TheFrenchGhosty/TheFrenchGhostys-Ultimate-YouTube-DL-Scripts-Collection

set -o errexit -o nounset

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
        --format 'bestvideo[height<=?720]+bestaudio/best' \
        "$@"
}

yt_non_live() {
    yt_defaults \
        --output-na-placeholder not_live \
        --match-filter live_status=not_live \
        "$@"
}

# Arguments: URL
# Exit: 0 if live, 1 otherwise
# FIXME merge into `yt_defaults` using post-processing filters?
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
    | grep --quiet --invert-match --ignore-case --fixed-strings not_live
}
