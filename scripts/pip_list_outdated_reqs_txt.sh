#!/bin/sh

# List updates by checking PIP against a requirements file.
# If no arguments are given, it searches recursively for requirements files.
#
# Arguments: [requirements.txt | directory] ...

# FIXME list `pip` itself if outdated
# FIXME ensure `pip install` uses `--uploaded-prior-to` (since pip v26.1)
# FIXMe ensure `pip install` uses `--require-virtualenv`

set -o errexit -o nounset

if command -v mktemp >/dev/null; then
    alias mktemp_posix=mktemp
else
    mktemp_posix() {
        echo 'mkstemp(template)' | m4 -D "template=${TMPDIR:-/tmp}/"
    }
fi

PIP_OUTDATED_PKGS_FILE="$(mktemp_posix)"
pip list --outdated | tail --lines +3 > "$PIP_OUTDATED_PKGS_FILE" &
PIP_LIST_PID="$!"

wait_for_pip_list() {
    if [ -n "$PIP_LIST_PID" ]; then
        echo "(Downloading outdated package list... $PIP_OUTDATED_PKGS_FILE)"
        wait "$PIP_LIST_PID"
        PIP_LIST_PID=
    fi
}

indent_stdout() {
    sed 's/^/    /'
}

# Arguments: <requirements.txt file>
# Stdout: packages, one name per line
list_pkgs_from_reqs_txt() {
    grep --no-filename --invert-match --extended-regexp '^$|^#' -- "$@" \
        | cut --delimiter '=' --fields 1 \
        | sort \
        | uniq
}

# Arguments: <pip list output file>
# Stdin: packages, one name per line
# Stdout: pip list filtered by matching packages
grep_for_pkgs() {
    xargs -I '{}' -- echo --regexp='{}' \
        | xargs grep "$1" --fixed-strings
}

# Arguments: <requirements.txt file> <pip list output file>
pretty_print_outdated_pkgs() {
    echo "$1"
    printf "%${#1}s\n" | tr ' ' '-'

    if ! list_pkgs_from_reqs_txt "$1" | grep_for_pkgs "$2"; then
        echo '(N/A)'
    fi | indent_stdout
}

# Arguments: <requirements.txt file | directory> <pip list output file>
pretty_print_outdated_pkgs_or_dir() {
    if [ -d "$1" ]; then
        for file in "${1%%/}/"*requirements.txt; do
            # Skip verbatim glob pattern when no files are found.
            if [ -r "$file" ]; then
                wait_for_pip_list
                echo
                pretty_print_outdated_pkgs "$file" "$PIP_OUTDATED_PKGS_FILE"
            fi
        done
    else
        wait_for_pip_list
        echo
        pretty_print_outdated_pkgs "$1" "$PIP_OUTDATED_PKGS_FILE"
    fi
}

if [ $# -eq 0 ]; then
    set -- **/*requirements.txt
fi

for file_or_dir; do
    pretty_print_outdated_pkgs_or_dir "$file_or_dir"
done
