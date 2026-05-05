# scripts/ci — CI Automation Scripts

All scripts here run both in CI and locally. No CI-only dependencies.

## kicad-visual-diff.py

**Purpose:** Generates a four-column HTML visual diff report comparing KiCad schematic sheets between two git refs.

**Dependencies:** Python 3.9+, Pillow (`pip install Pillow`), cairosvg (`pip install cairosvg`). The KiCad Docker image includes both.

**CLI usage:**
```bash
python3 scripts/ci/kicad-visual-diff.py \
  --base-dir /tmp/base \
  --head-dir /tmp/head \
  --feature my-feature \
  --output-dir /tmp/diff-output
```

**Local run (outside Docker):**
```bash
# Extract base ref
git archive origin/main | tar -x -C /tmp/base
# Extract head ref
git archive HEAD | tar -x -C /tmp/head
# Run
python3 scripts/ci/kicad-visual-diff.py --base-dir /tmp/base --head-dir /tmp/head --feature my-feature --output-dir /tmp/diff-output
```

**Outputs:** `diff-report.html`, `metadata.json`, `comment.md` in `--output-dir`.

## init-feature.sh
Scaffolds a new feature directory when an `init/<feature>` PR merges. Called by `init-feature.yml`.

## validate-branch-name.sh
Validates PR branch names against allowed patterns. Called by `pr-checks.yml` as a required check.

## validate-dir-structure.py
Validates that a PR touches only one feature directory. Called by `pr-checks.yml` as a required check.
