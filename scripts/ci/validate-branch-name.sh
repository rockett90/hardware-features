#!/usr/bin/env bash
set -euo pipefail
BRANCH="${1:?Usage: validate-branch-name.sh <branch>}"
PATTERNS=(
  "^main$"
  "^concept/[a-z0-9][a-z0-9-]*$"
  "^init/[a-z0-9][a-z0-9-]*$"
  "^artifact/[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9A-Z_-]*$"
  "^finding/[a-z0-9][a-z0-9-]*/[0-9]+-[a-z0-9][a-z0-9-]*$"
  "^signoff/[a-z0-9][a-z0-9-]*/(cdr|cdr-[0-9]+|trr|trr-[0-9]+|release)$"
  "^library/[a-z0-9][a-z0-9-]*$"
  "^chore/[a-z0-9][a-z0-9-]*$"
  "^release-please--.*$"
)
for p in "${PATTERNS[@]}"; do
  if [[ "$BRANCH" =~ $p ]]; then echo "✅ Valid: $BRANCH"; exit 0; fi
done
echo "❌ Invalid branch name: $BRANCH"
echo "Allowed patterns:"
for p in "${PATTERNS[@]}"; do echo "  $p"; done
exit 1
