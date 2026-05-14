#!/usr/bin/env bash
set -euo pipefail
# Phase 1 of the init flow — runs on branch push via init-branch-setup.yml.
# Idempotently scaffolds the full feature directory tree (.gitkeep placeholders),
# all feature stubs/templates (cp -n, no-clobber), and patches
# commitlint.config.js and release-please-config.json.
# Phase 2 (post-merge) is handled by init-feature.yml and only creates the PDR tag.

FEATURE="${1:?Usage: init-branch-setup.sh <feature-name>}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

FEATURE_DIR="features/$FEATURE"

for dir in kicad simulations/models calculations \
            analysis/mtbf analysis/stress analysis/thermal analysis/doe \
            bom bring-up/scripts circuit-mods \
            production/fptcs production/test-programs production/aoi \
            decisions ci-results reviews requirements datasheet; do
  mkdir -p "$FEATURE_DIR/$dir"
  touch "$FEATURE_DIR/$dir/.gitkeep"
done

cp -n "scripts/ci/stubs/DDR-000-design-intent.md"    "$FEATURE_DIR/decisions/DDR-000-design-intent.md"
cp -n "scripts/ci/stubs/DDR-000-decisions.md"         "$FEATURE_DIR/decisions/DDR-000-decisions.md"
cp -n "scripts/ci/stubs/feature-requirements.yaml"   "$FEATURE_DIR/requirements/feature-requirements.yaml"
cp -n "scripts/ci/stubs/interface-requirements.yaml" "$FEATURE_DIR/requirements/interface-requirements.yaml"
cp -n "scripts/ci/stubs/verification-matrix.md"      "$FEATURE_DIR/requirements/verification-matrix.md"
cp -n "scripts/ci/stubs/fptcs.yaml"                  "$FEATURE_DIR/production/fptcs/fptcs.yaml"
cp -n "scripts/ci/stubs/fptcs-notes.md"              "$FEATURE_DIR/production/fptcs/fptcs-notes.md"
cp -n "scripts/ci/stubs/README.md"                   "$FEATURE_DIR/README.md"
cp -n "scripts/ci/stubs/specs.yaml"                  "$FEATURE_DIR/datasheet/specs.yaml"
cp -n "scripts/ci/stubs/application-notes.md"        "$FEATURE_DIR/datasheet/application-notes.md"
cp -n "scripts/ci/stubs/errata.md"                   "$FEATURE_DIR/datasheet/errata.md"
cp -n "scripts/ci/stubs/reviews/README.md"           "$FEATURE_DIR/reviews/README.md"
cp -n "scripts/ci/stubs/ci-results/README.md"       "$FEATURE_DIR/ci-results/README.md"

cp_template() {
  if [[ -f "$1" ]]; then
    cp -n "$1" "$2"
  else
    echo "⚠️  Template not found, skipping: $1"
  fi
}
cp_template "templates/kicad-project-template.kicad_pro" "$FEATURE_DIR/kicad/$FEATURE.kicad_pro"
cp_template "templates/schematic-template.kicad_sch"     "$FEATURE_DIR/kicad/$FEATURE.kicad_sch"
cp_template "templates/pcb-template.kicad_pcb"           "$FEATURE_DIR/kicad/$FEATURE.kicad_pcb"
cp_template "templates/title-block.kicad_wks"            "$FEATURE_DIR/kicad/title-block.kicad_wks"
cp_template "config/kibot/base-feature.kibot.yml"        "$FEATURE_DIR/.kibot.yml"

for file in \
  "$FEATURE_DIR/decisions/DDR-000-design-intent.md" \
  "$FEATURE_DIR/decisions/DDR-000-decisions.md" \
  "$FEATURE_DIR/requirements/feature-requirements.yaml" \
  "$FEATURE_DIR/requirements/interface-requirements.yaml" \
  "$FEATURE_DIR/requirements/verification-matrix.md" \
  "$FEATURE_DIR/production/fptcs/fptcs.yaml" \
  "$FEATURE_DIR/production/fptcs/fptcs-notes.md" \
  "$FEATURE_DIR/README.md" \
  "$FEATURE_DIR/datasheet/specs.yaml" \
  "$FEATURE_DIR/datasheet/application-notes.md" \
  "$FEATURE_DIR/datasheet/errata.md" \
  "$FEATURE_DIR/reviews/README.md" \
  "$FEATURE_DIR/ci-results/README.md"; do
  if [[ -f "$file" ]]; then
    sed -i "s/FEATURE_NAME/$FEATURE/g" "$file"
  fi
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
