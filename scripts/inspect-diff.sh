#!/usr/bin/env bash
set -euo pipefail

printf '== git status --short ==\n'

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --short
else
  printf 'git repository not initialized\n'
fi

printf '\n== git diff --stat ==\n'

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    git diff --stat
  else
    printf 'no commits yet; working tree is all untracked content\n'
  fi
else
  printf 'git repository not initialized\n'
fi

printf '\n== git diff --name-only ==\n'

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    git diff --name-only
  else
    git ls-files --others --exclude-standard
  fi
else
  printf 'git repository not initialized\n'
fi
