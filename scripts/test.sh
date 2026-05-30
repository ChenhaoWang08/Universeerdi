#!/usr/bin/env bash
set -euo pipefail

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  printf 'python interpreter not found\n' >&2
  exit 1
fi

printf '== tests ==\n'
"$PYTHON_BIN" -m pytest -p no:cacheprovider tests
