#!/bin/sh

# Wrapper around the local venv's Python.
#
# Arguments: [pass-through]

# FIXME make Python files shebang point to venv instead?

set -o errexit -o nounset

BASE_PATH="$(dirname "$(realpath -e "$0")")/../"
export PYTHONPATH="${PYTHONPATH:-}:$BASE_PATH"

PYTHON3="${PYTHON3:-python3}"
VENV="$BASE_PATH/.venv/bin/activate"

# shellcheck disable=SC1090
. "$VENV"
"$PYTHON3" "$@"
