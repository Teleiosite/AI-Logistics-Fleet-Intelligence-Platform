#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./tools/resolve_conflicts.sh <target-branch>
# Example:
#   ./tools/resolve_conflicts.sh main

TARGET_BRANCH="${1:-main}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not inside a git repository" >&2
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current)"

echo "Current branch: ${CURRENT_BRANCH}"
echo "Target branch: ${TARGET_BRANCH}"

echo "Fetching latest refs..."
git fetch --all --prune

echo "Merging ${TARGET_BRANCH} into ${CURRENT_BRANCH}..."
if ! git merge "origin/${TARGET_BRANCH}"; then
  echo
  echo "Merge reported conflicts. Files with markers:"
  git diff --name-only --diff-filter=U || true
  echo
  echo "Open each conflicted file and resolve markers:"
  echo "  <<<<<<<"
  echo "  ======="
  echo "  >>>>>>>"
  echo
  echo "After resolving files, run:"
  echo "  git add <resolved-files>"
  echo "  git commit -m 'Resolve merge conflicts with ${TARGET_BRANCH}'"
  exit 2
fi

echo "Merge completed without conflicts."
