#!/bin/sh

# List updates by matching a PIP list against `requirements.txt` files.
#
# Arguments: [requirements.txt] ...

set -o errexit -o nounset

list_pkgs_from_reqs_txt() {
    grep --no-filename --invert-match --extended-regexp '^$|^#' -- "$@" \
        | cut --delimiter '=' --fields 1
}

match_pkg_names_regexp() {
    printf '(%s)' "$(sort | uniq | paste --serial --delimiters '|')"
}

grep_for_pkgs() {
    if [ $# -eq 0 ]; then
        cat
    else
        grep \
            --extended-regexp \
            --regexp "$(list_pkgs_from_reqs_txt "$@" | match_pkg_names_regexp)"
    fi
}

filter_out_pip_list_header() {
    tail --lines +3
}

filter_out_pip_list_header | grep_for_pkgs "$@"
