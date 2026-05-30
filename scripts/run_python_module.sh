#!/bin/sh

# Runs a Python module (useful for Liferea).
#
# Arguments: module arguments...

# TODO convert to Python script? to avoid shell scripts and Makefiles
# TODO error handling (eg. argument count)
# TODO add catchall logging wrapper
# TODO honor other Python's user environment variables

set -e -u

BASE_PATH="$(dirname "$(readlink -e "$0")")/../"

PYTHONPATH="${PYTHONPATH:-}:$BASE_PATH"
export PYTHONPATH

PYTHON3="${PYTHON3:-python3}"
VENV="$BASE_PATH/.venv/bin/activate"

module_name="$1"
shift

. "$VENV"
"$PYTHON3" -m "feed_enclosure.$module_name" "$@"
