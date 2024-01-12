#!/bin/sh

# List updates by checking PIP against a requirements file.
#
# Arguments: [requirements.txt]

set -e -u

if command -v mktemp >/dev/null; then
    mktemp_posix() {
        mktemp
    }
else
    mktemp_posix() {
        echo 'mkstemp(template)' | m4 -D "template=${TMPDIR:-/tmp}/"
    }
fi

if [ $# -eq 0 ]; then
    REQS_TXT="$(dirname "$(readlink -e "$0")")/../requirements.txt"
else
    REQS_TXT="$1"
fi

reqs_txt_patterns="$(mktemp_posix)"

grep -vE '^$|^#' "$REQS_TXT" | cut -d'~' -f1 > "$reqs_txt_patterns"
pip list --outdated | grep -Ff "$reqs_txt_patterns" -
