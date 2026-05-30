#!/usr/bin/env bash
set -euo pipefail

printf '== current git status ==\n'

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --short
else
  printf 'git repository not initialized\n'
fi

printf '\nSuggested rollback commands:\n'
printf '  git restore .\n'
printf '  git clean -fd\n'

printf '\nWarning: these commands discard uncommitted changes.\n'
printf 'Review the diff before running them.\n'
