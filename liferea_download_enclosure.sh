#!/bin/sh

# Download handler for Liferea's feed enclosures.
#
# Arguments: URL path
# Input: none
# Output: download progress
#
# Runtime dependencies:
#   python3 -m pip install youtube_dl # download Youtube videos
#   apt install uget # Version: 2.2.3-2 # download non-YouTube URLs
#   apt install ffmpeg # Version: 7:4.3.1-4ubuntu1 # merge video/audio
#
# Test dependencies:
#   apt install shellcheck # Version: 0.7.1-1build1

set -e -u

YOUTUBE_DL_BIN="${YOUTUBE_DL_BIN:-youtube-dl}"
UGET_BIN="${UGET_BIN:-uget-gtk}"

is_ign_daily_fix_url() {
    echo "$1" | grep -q -P '://assets\d*\.ign\.com/videos/'
}

prepare_ign_daily_fix_url() {
    ign_width='[[:digit:]]+'
    ign_hash='[[:xdigit:]]+'
    ign_bitrate='[[:digit:]]+'

    echo "$1" \
        | sed -r "s#/$ign_width(/$ign_hash-)$ign_bitrate-#/1920\\13906000-#"
}

extract_nice_filename_from_url() {
    if echo "$1" | grep -q -F '#'; then
        # Also convert percent-encoded spaces since Liferea seems to add those
        # even when the URL doesn't have them.
        echo "$1" | sed -r 's/^[^#]+#//' | sed -r 's/%20/ /g'
    fi
}

download_via_uget() {
    uget_url="$1"
    uget_path="$2"
    uget_filename="$(extract_nice_filename_from_url "$uget_url")"

    if [ -n "$uget_filename" ]; then
        set -- "--filename=$uget_filename"
        # Remove the URL fragment since uGet seems to break when given it
        # in the command line.
        uget_url="$(echo "$uget_url" | sed -r 's/#.+$//')"
    else
        set --
    fi

    # Make the folder path absolute since uGet doesn't seem to interpret it
    # correctly when invoked in the command line.
    "$UGET_BIN" --quiet "--folder=$(readlink -e "$uget_path")" "$@" "$uget_url"
}

main() {
    if ! command -v "$YOUTUBE_DL_BIN" >/dev/null; then
        echo "Error: $YOUTUBE_DL_BIN not found (override \$YOUTUBE_DL_BIN)" >&2
        return 1
    fi

    if [ $# -ne 2 ]; then
        cat <<'EOT' >&2
Arguments: url path
Note: if the URL has a URL fragment then it's an optional filename
EOT
        return 1
    fi

    url="$1"
    path="$2"
    shift 2

    if is_ign_daily_fix_url "$url"; then
        download_via_uget "$(prepare_ign_daily_fix_url "$url")" "$path"
    else
        (
            # Navigate to where the file should be downloaded to since
            # youtube-dl doesn't have an option for the output directory.
            cd "$path"
            "$YOUTUBE_DL_BIN" --add-metadata -f 'bestvideo+bestaudio' "$url"
        )
    fi
}

if [ -t 0 ]; then
    main "$@"
else
    # Tailor output with logging for when run under Liferea.
    main "$@" 2>&1 | logger --stderr --tag "$0 $*"
fi