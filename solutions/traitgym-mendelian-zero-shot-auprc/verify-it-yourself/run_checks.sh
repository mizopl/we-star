#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -x ${PYTHON:-python3} ]; then
    ${PYTHON:-python3} "$DIR/verify.py"
else
    python3 "$DIR/verify.py"
fi
