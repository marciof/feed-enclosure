#!/bin/sh

# Runs a Python module (useful for Liferea).
#
# Arguments: module arguments...

# TODO add catchall logging wrapper
# TODO honor other Python's user environment variables
# TODO convert to Python script? to avoid shell scripts and Makefiles

set -e -u

PYTHONPATH="${PYTHONPATH:-}:$(dirname "$(readlink -e "$0")")/../"
PYTHON3="${PYTHON3:-python3}"

export PYTHONPATH

main() {
    module_name="$1"
    shift
    "$PYTHON3" -m "feed_enclosure.$module_name" "$@"
}

if [ -t 0 ]; then
    main "$@"
else
    # Format output with logging for when run outside the terminal.
    {
        echo "Command line arguments: $0 $*"
        main "$@"
    } 2>&1 | logger --stderr --tag "feed_enclosure.run_module [PID $$]"
fi
