#!/bin/sh

# Wrapper around the local venv's Python.
#
# Arguments: [pass-through]

# FIXME make Python files shebang point to venv instead?

set -e -u

BASE_PATH="$(dirname "$(readlink -e "$0")")/../"
export PYTHONPATH="${PYTHONPATH:-}:$BASE_PATH"

PYTHON3="${PYTHON3:-python3}"
VENV="$BASE_PATH/.venv/bin/activate"

. "$VENV"
"$PYTHON3" "$@"
