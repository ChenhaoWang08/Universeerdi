#!/usr/bin/env bash
set -euo pipefail

printf '== check ==\n'

if [ -f scripts/test.sh ] && [ -s scripts/test.sh ]; then
  printf 'Running scripts/test.sh\n'
  bash scripts/test.sh
else
  printf 'tests are not yet available\n'
fi

printf '\n== git status ==\n'

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --short
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    printf '\n== git branch ==\n'
    git branch --show-current
  else
    printf '\nno commits yet in this repository\n'
  fi
else
  printf 'git repository not initialized\n'
fi
