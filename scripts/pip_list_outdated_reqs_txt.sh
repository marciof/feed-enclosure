#!/bin/sh

# List updates by checking PIP against files containing requirements.
# If no arguments are given, it searches recursively ignoring hidden paths.
#
# A file containing requirements is one of the following:
#
# - Filename ending in "requirements.txt" case-insensitive.
#   https://pip.pypa.io/en/stable/reference/requirements-file-format/
#
# - File containing inline script metadata.
#   https://packaging.python.org/en/latest/specifications/inline-script-metadata/#script-type
#
# Arguments: [file with requirements | directory ...]

# FIXME convert to Python so it's cross-platform
# FIXME list `pip` itself if outdated
# FIXME ensure `pip install` uses `--uploaded-prior-to` (since pip v26.1)
# FIXME ensure `pip install` uses `--require-virtualenv`
# FIXME detect brand new/empty venv to list all are required updates

set -o errexit -o nounset

if command -v mktemp >/dev/null; then
    alias mktemp_posix=mktemp
else
    mktemp_posix() {
        echo 'mkstemp(template)' | m4 --define="template=${TMPDIR:-/tmp}/"
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

# Arguments: <file with requirements>
# Stdout: packages, one name per line
list_pkgs_from_file_with_reqs() {
    if grep --quiet --line-regexp --fixed-strings '# /// script' -- "$1"; then
        echo --requirements-from-script "$1"
    else
        echo --requirement "$1"
    fi \
    | xargs pip install \
        --quiet --no-input --dry-run \
        --no-deps --ignore-installed --disable-pip-version-check \
        --report - \
    | python -c 'import sys, json; print("\n".join(p["metadata"]["name"] for p in json.load(sys.stdin)["install"]))' \
    | sort \
    | uniq
}

# Arguments: <pip list output file>
# Stdin: packages, one name per line
# Stdout: pip list filtered by matching packages
grep_for_pkgs() {
    xargs -I '{}' -- echo '--regexp={}' \
        | xargs grep "$1" --fixed-strings
}

# Arguments: <file with requirements> <pip list output file>
pretty_print_outdated_pkgs() {
    echo "$1"
    printf "%${#1}s\n" | tr ' ' '-'

    if ! list_pkgs_from_file_with_reqs "$1" | grep_for_pkgs "$2"; then
        echo '(N/A)'
    fi | indent_stdout
}

# Arguments: <file with requirements | directory> <pip list output file>
pretty_print_outdated_pkgs_or_dir() {
    if [ -d "$1" ]; then
        for file in $(list_files_with_reqs "$1"); do
            wait_for_pip_list
            echo
            pretty_print_outdated_pkgs "${file#./}" "$PIP_OUTDATED_PKGS_FILE"
        done
    else
        wait_for_pip_list
        echo
        pretty_print_outdated_pkgs "${1#./}" "$PIP_OUTDATED_PKGS_FILE"
    fi
}

# Arguments: <starting path>
list_files_with_reqs() {
    starting_path="$1"; shift

    find "$starting_path" -name '.*' \! -name '.' -prune -o -type f \( \
        -iname '*requirements.txt' \
        -o -exec grep --quiet --line-regexp --fixed-strings '# /// script' {} \; \
    \) -print
}

if [ $# -eq 0 ]; then
    set -- .
fi

for file_or_dir; do
    pretty_print_outdated_pkgs_or_dir "$file_or_dir"
done
