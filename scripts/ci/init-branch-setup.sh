#!/usr/bin/env bash
set -euo pipefail

FEATURE="${1:?Usage: init-branch-setup.sh <feature-name>}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

FEATURE_DIR="features/$FEATURE"

mkdir -p "$FEATURE_DIR/decisions" "$FEATURE_DIR/requirements"

cp -n "scripts/ci/stubs/DDR-000.md"                  "$FEATURE_DIR/decisions/DDR-000-feature-overview.md"
cp -n "scripts/ci/stubs/feature-requirements.yaml"   "$FEATURE_DIR/requirements/feature-requirements.yaml"
cp -n "scripts/ci/stubs/interface-requirements.yaml" "$FEATURE_DIR/requirements/interface-requirements.yaml"
cp -n "scripts/ci/stubs/verification-matrix.md"      "$FEATURE_DIR/requirements/verification-matrix.md"

for file in \
  "$FEATURE_DIR/decisions/DDR-000-feature-overview.md" \
  "$FEATURE_DIR/requirements/feature-requirements.yaml" \
  "$FEATURE_DIR/requirements/interface-requirements.yaml" \
  "$FEATURE_DIR/requirements/verification-matrix.md"; do
  sed -i "s/FEATURE_NAME/$FEATURE/g" "$file"
done

COMMITLINT_CONFIG=".github/commitlint.config.js"
if ! grep -qF "'$FEATURE'" "$COMMITLINT_CONFIG"; then
  python3 - "$FEATURE" "$COMMITLINT_CONFIG" <<'PY'
import re
import sys

feature, path = sys.argv[1:]

with open(path, encoding="utf-8") as fh:
    text = fh.read()

match = re.search(r"('scope-enum': \[2, 'always', \[\n)(.*?)(\n\s+\]\],)", text, re.S)
if match is None:
    raise SystemExit("Could not find scope-enum array in commitlint config")

entries = [line.strip().rstrip(",") for line in match.group(2).splitlines() if line.strip()]
entry = f"'{feature}'"
if entry not in entries:
    entries.append(entry)

body = "\n".join(
    f"      {value}{',' if index < len(entries) - 1 else ''}"
    for index, value in enumerate(entries)
)
updated = text[:match.start()] + match.group(1) + body + match.group(3) + text[match.end():]

with open(path, "w", encoding="utf-8") as fh:
    fh.write(updated)
PY
fi

RELEASE_PLEASE_CONFIG=".github/release-please-config.json"
python3 - "$FEATURE" "$RELEASE_PLEASE_CONFIG" <<'PY'
import json
import sys

feature, path = sys.argv[1:]

with open(path, encoding="utf-8") as fh:
    data = json.load(fh)

packages = data.setdefault("packages", {})
if feature in packages:
    raise SystemExit(0)

packages[feature] = {
    "release-type": "simple",
    "package-name": feature,
    "changelog-path": f"features/{feature}/CHANGELOG.md",
    "bump-minor-pre-major": True,
}

with open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")
PY
