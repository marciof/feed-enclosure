#!/bin/sh

# Runs a Python module (useful for Liferea).
#
# Arguments: module arguments...

# TODO convert to Python script? to avoid shell scripts and Makefiles
# TODO error handling (eg. argument count)
# TODO add catchall logging wrapper
# TODO honor other Python's user environment variables

set -e -u

PYTHONPATH="${PYTHONPATH:-}:$(dirname "$(readlink -e "$0")")/../"
export PYTHONPATH

PYTHON3="${PYTHON3:-python3}"

module_name="$1"
shift

"$PYTHON3" -m "feed_enclosure.$module_name" "$@"
