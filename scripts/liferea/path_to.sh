#!/bin/sh

# Arguments: [path type]
# Stdout: path to a Liferea file/folder if it exists, nothing otherwise
# Exit: 0 if it exists, >0 otherwise
#
# References:
# - XDG Spec: https://specifications.freedesktop.org/basedir/latest/#variables
# - Liferea man page: https://github.com/lwindolf/liferea/blob/main/data/man/liferea.1

set -o errexit -o nounset

# TODO request Liferea cmdline flag to print paths
help_opt=h
opml_cmd=opml
plugins_cmd=plugins

while getopts "$help_opt" opt "$@"; do
    case "$opt" in
        \?)
            exit 1
            ;;
        "$help_opt")
            printf 'usage: %s [options] <path type>\n\n' \
                "$(basename "$(realpath -e "$0")")"
            printf 'options:\n'
            printf '  -%s \t\thelp\n' "$help_opt"
            echo
            printf 'path types:\n'
            printf '  %s \t\tfeed list OPML file\n' "$opml_cmd"
            printf '  %s \tplugins folder\n' "$plugins_cmd"
            exit 0
            ;;
    esac
done

shift "$((OPTIND - 1))"

case "${1:-}" in
    opml)
        realpath --canonicalize-existing \
            "${XDG_CONFIG_HOME:-"$HOME/.config"}/liferea/feedlist.opml"
        ;;
    plugins)
        realpath --canonicalize-existing \
            "${XDG_DATA_HOME:-"$HOME/.local/share"}/liferea/plugins/"
        ;;
    *)
        echo 'Invalid or missing required arguments' >&2
        printf "try '-%s' for help\n" "$help_opt" >&2
        exit 1
        ;;
esac
