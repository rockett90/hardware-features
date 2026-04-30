#!/usr/bin/env bash
set -euo pipefail

FEATURE="${1:?Usage: init-feature.sh <feature-name>}"
FEATURE_DIR="features/$FEATURE"

for dir in schematics pcb simulations/models calculations \
            analysis/mtbf analysis/stress analysis/thermal analysis/doe \
            bom bring-up/scripts circuit-mods \
            production/fptcs production/test-programs production/aoi \
            decisions ci-results reviews requirements; do
  mkdir -p "$FEATURE_DIR/$dir"
done

# Copy KiCad templates — skip gracefully if not yet created.
cp_template() {
  if [[ -f "$1" ]]; then cp "$1" "$2"
  else echo "⚠️  Template not found, skipping: $1"; fi
}
cp_template "templates/kicad-project-template.kicad_pro" "$FEATURE_DIR/$FEATURE.kicad_pro"
cp_template "templates/schematic-template.kicad_sch"     "$FEATURE_DIR/schematics/$FEATURE.kicad_sch"
cp_template "templates/pcb-template.kicad_pcb"           "$FEATURE_DIR/pcb/$FEATURE.kicad_pcb"
cp_template "config/kibot/base-feature.kibot.yml"        "$FEATURE_DIR/.kibot.yml"

# -n = no-clobber: skip if destination already exists,
# preserving files the engineer placed in the init PR.
cp -n "scripts/ci/stubs/feature-requirements.yaml"   "$FEATURE_DIR/requirements/feature-requirements.yaml"
cp -n "scripts/ci/stubs/interface-requirements.yaml" "$FEATURE_DIR/requirements/interface-requirements.yaml"
cp -n "scripts/ci/stubs/verification-matrix.md"      "$FEATURE_DIR/requirements/verification-matrix.md"
cp -n "scripts/ci/stubs/DDR-000.md"                  "$FEATURE_DIR/decisions/DDR-000-feature-overview.md"

echo "✅ Scaffolded: $FEATURE_DIR"
