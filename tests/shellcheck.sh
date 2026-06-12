#!/bin/sh

# FIXME document (including dependencies)

set -e -u

BASE_PATH="$(dirname "$(realpath -e "$0")")/../"

grep \
    --exclude-dir .git \
    --exclude-dir .venv \
    --exclude-dir .idea \
    --recursive \
    --files-with-matches '#!/bin/sh' \
    "$BASE_PATH" \
| xargs shellcheck
