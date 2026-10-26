#!/bin/sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -x ${PYTHON:-python3} ]; then
    PY=${PYTHON:-python3}
else
    PY=python3
fi
"$PY" -B "$DIR/verify.py"
