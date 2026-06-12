#!/bin/sh

# List updates by checking PIP against a requirements file.
#
# Arguments: [requirements.txt]

# FIXME find all the requirements.txt
# FIXME document
# FIXME error handling
# FIXME proper logging

set -o errexit -o nounset

if command -v mktemp >/dev/null; then
    alias mktemp_posix=mktemp
else
    mktemp_posix() {
        echo 'mkstemp(template)' | m4 --define= "template=${TMPDIR:-/tmp}/"
    }
fi

pip_list_outdated_pkgs() {
    pip list --outdated | tail --lines +3
}

find_reqs_txt_files() {
    find "$@" \
        -type d -name '.*' \! -path "$1" -prune \
        -o \
        -type f -iname '*requirements.txt' -print
}

list_pkgs_from_reqs_txt() {
    grep --no-filename --invert-match --extended-regexp '^$|^#' -- "$@" \
        | cut --delimiter '=' --fields 1 \
        | sort \
        | uniq
}

grep_for_pkgs() {
    xargs -I '{}' -- echo --regexp='{}' | xargs grep "$1" --fixed-strings
}

pretty_print_outdated_pkgs() {
    echo "* $1 *"
    printf "  %${#1}s  \n" | tr ' ' '-'

    if ! list_pkgs_from_reqs_txt "$1" | grep_for_pkgs "$2"; then
        echo '(N/A)'
    fi
}

pretty_print_outdated_pkgs_or_dir() {
    if [ -d "$1" ]; then
        for reqs_txt_file in $(find_reqs_txt_files "$1"); do
            echo
            pretty_print_outdated_pkgs "$reqs_txt_file" "$2"
        done
    else
        echo
        pretty_print_outdated_pkgs "$1" "$2"
    fi
}

outdated_pkgs_file="$(mktemp_posix)"
echo "(Downloading list of outdated packages... $outdated_pkgs_file)"
pip_list_outdated_pkgs > "$outdated_pkgs_file"

if [ $# -eq 0 ]; then
    set -- .
fi

for arg; do
    pretty_print_outdated_pkgs_or_dir "$arg" "$outdated_pkgs_file"
done
