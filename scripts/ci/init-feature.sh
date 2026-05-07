#!/usr/bin/env bash
set -euo pipefail

FEATURE="${1:?Usage: init-feature.sh <feature-name>}"
FEATURE_DIR="features/$FEATURE"

for dir in schematics pcb simulations/models calculations \
            analysis/mtbf analysis/stress analysis/thermal analysis/doe \
            bom bring-up/scripts circuit-mods \
            production/fptcs production/test-programs production/aoi \
            decisions ci-results reviews requirements datasheet; do
  mkdir -p "$FEATURE_DIR/$dir"
done

# Copy KiCad templates — skip gracefully if not yet created.
cp_template() {
  if [[ -f "$1" ]]; then cp "$1" "$2"
  else echo "⚠️  Template not found, skipping: $1"; fi
}
cp_template "templates/kicad-project-template.kicad_pro" "$FEATURE_DIR/$FEATURE.kicad_pro"
cp_template "templates/schematic-template.kicad_sch"     "$FEATURE_DIR/$FEATURE.kicad_sch"
cp_template "templates/pcb-template.kicad_pcb"           "$FEATURE_DIR/pcb/$FEATURE.kicad_pcb"
cp_template "config/kibot/base-feature.kibot.yml"        "$FEATURE_DIR/.kibot.yml"

# -n = no-clobber: skip if destination already exists,
# preserving files the engineer placed in the init PR.
cp -n "scripts/ci/stubs/feature-requirements.yaml"   "$FEATURE_DIR/requirements/feature-requirements.yaml"
cp -n "scripts/ci/stubs/interface-requirements.yaml" "$FEATURE_DIR/requirements/interface-requirements.yaml"
cp -n "scripts/ci/stubs/verification-matrix.md"      "$FEATURE_DIR/requirements/verification-matrix.md"
cp -n "scripts/ci/stubs/DDR-000.md"                  "$FEATURE_DIR/decisions/DDR-000-feature-overview.md"

# Feature README — navigation hub for the feature directory
cp -n "scripts/ci/stubs/README.md"               "$FEATURE_DIR/README.md"

# Datasheet source stubs — engineer fills these in between CDR and TRR
mkdir -p "$FEATURE_DIR/datasheet"
cp -n "scripts/ci/stubs/specs.yaml"              "$FEATURE_DIR/datasheet/specs.yaml"
cp -n "scripts/ci/stubs/application-notes.md"    "$FEATURE_DIR/datasheet/application-notes.md"
cp -n "scripts/ci/stubs/errata.md"               "$FEATURE_DIR/datasheet/errata.md"

# Replace FEATURE_NAME placeholder in scaffolded files
for f in \
  "$FEATURE_DIR/README.md" \
  "$FEATURE_DIR/datasheet/specs.yaml" \
  "$FEATURE_DIR/datasheet/application-notes.md" \
  "$FEATURE_DIR/datasheet/errata.md"; do
  if [[ -f "$f" ]]; then
    sed -i "s/FEATURE_NAME/$FEATURE/g" "$f"
  fi
done

echo "✅ Scaffolded: $FEATURE_DIR"
