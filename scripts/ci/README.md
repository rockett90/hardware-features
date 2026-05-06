# scripts/ci — CI Automation Scripts

> All scripts in this directory run both in CI and locally. There are no CI-only dependencies.

---

## Scripts

| Script | Called by | Also runnable locally |
|---|---|---|
| `kicad-visual-diff.py` | `kicad-diff.yml` | Yes |
| `init-feature.sh` | `init-feature.yml` | Not recommended |
| `validate-branch-name.sh` | `pr-checks.yml` | Yes |
| `validate-dir-structure.py` | `pr-checks.yml` | Yes |

---

## `kicad-visual-diff.py`

**Purpose:** Generates a four-column HTML visual diff report comparing KiCad schematic sheets (and optionally PCB layers) between two git refs.

**Dependencies:**

| Dependency | Version | Install |
|---|---|---|
| Python | 3.11+ | System package or pyenv |
| Pillow | 10.3.0 | `pip install -r scripts/ci/requirements.txt` |
| cairosvg | 2.7.1 | `pip install -r scripts/ci/requirements.txt` |
| lxml | 5.2.2 | `pip install -r scripts/ci/requirements.txt` |
| sexpdata | 1.0.2 | `pip install -r scripts/ci/requirements.txt` |
| kicad-cli | pinned via Docker | Included in the KiCad Docker image |

Dependency versions are pinned in `scripts/ci/requirements.txt`. See [docs/versions.md](../../docs/versions.md) for the full version reference.

> 💡 Tip: The KiCad Docker image includes all Python dependencies and `kicad-cli`. Running inside Docker is the easiest way to reproduce CI output locally.

**CLI reference:**

```
python3 scripts/ci/kicad-visual-diff.py \
  --base-dir <path>      Base directory containing the feature at the base ref
  --head-dir <path>      Head directory containing the feature at the head ref
  --feature <name>       Feature name (e.g. buck-converter-5v)
  --output-dir <path>    Output directory for generated files
  [--pcb]                Also diff PCB layers (optional flag)
```

**Local run (outside Docker):**

```bash
# Extract base ref into /tmp/base
git archive origin/main -- features/buck-converter-5v/ | tar -x -C /tmp/base

# Extract head ref into /tmp/head
git archive HEAD -- features/buck-converter-5v/ | tar -x -C /tmp/head

# Run
python3 scripts/ci/kicad-visual-diff.py \
  --base-dir /tmp/base \
  --head-dir /tmp/head \
  --feature buck-converter-5v \
  --output-dir /tmp/diff-output

# Open the report
open /tmp/diff-output/diff-report.html
```

**Docker run:**

```bash
docker run --rm \
  -v "$(pwd)/scripts:/scripts" \
  -v "/tmp/base:/kv-base" \
  -v "/tmp/head:/kv-head" \
  -v "/tmp/diff-output:/kv-out" \
  "ghcr.io/inti-cmnb/kicad10_auto_full@sha256:81621e501169e66dc051a65a0e575c0ab2854f69a121f1f9d97aad2b0d4c0257" \
  python3 /scripts/ci/kicad-visual-diff.py \
    --base-dir /kv-base \
    --head-dir /kv-head \
    --feature buck-converter-5v \
    --output-dir /kv-out
```

**Outputs:**

| File | Description |
|---|---|
| `diff-report.html` | Fully self-contained HTML report with zoom/pan on each image |
| `metadata.json` | Feature name, SHAs, sheet counts, warnings |
| `comment.md` | Markdown summary suitable for a PR comment |
| `changes.json` | Structured change list from the semantic diff step |

---

## `init-feature.sh`

**Purpose:** Scaffolds the full feature directory structure when an `init/<feature>` PR merges.

**Called by:** `init-feature.yml` — triggered automatically on merge of any `init/<feature>` branch.

**Not for manual use.** Running this script manually will overwrite files in the target feature directory. If you need to re-scaffold a feature directory, coordinate with the team first.

**What it does:**

1. Creates all standard subdirectories (`schematics/`, `pcb/`, `simulations/`, `calculations/`, `analysis/`, `bom/`, `bring-up/`, `production/`, `decisions/`, `requirements/`, `reviews/`, `ci-results/`).
2. Copies KiCad project templates from `templates/` into the feature directory.
3. Copies stub requirement and decision files from `scripts/ci/stubs/` into the feature directory (using `cp -n` — existing files are not overwritten).

---

## `validate-branch-name.sh`

**Purpose:** Validates a PR branch name against the allowed patterns defined in `CONTRIBUTING.md`.

**Called by:** `pr-checks.yml` — runs as a required check on every PR.

**Local use** (to pre-validate before pushing):

```bash
bash scripts/ci/validate-branch-name.sh artifact/buck-converter-5v/add-output-filter
```

Exit code 0 = valid. Non-zero = invalid, with an error message.

**Allowed patterns:**

| Pattern | Example |
|---|---|
| `main` | `main` |
| `concept/<feature>` | `concept/power-module` |
| `init/<feature>` | `init/buck-converter-5v` |
| `artifact/<feature>/<desc>` | `artifact/buck-converter-5v/add-filter` |
| `artifact/<feature>/<desc-HW-N>` | `artifact/buck-converter-5v/add-filter-HW-42` |
| `finding/<feature>/<N>-<desc>` | `finding/buck-converter-5v/7-wrong-footprint` |
| `signoff/<feature>/cdr` | `signoff/buck-converter-5v/cdr` |
| `signoff/<feature>/trr` | `signoff/buck-converter-5v/trr` |
| `signoff/<feature>/trr-N` | `signoff/buck-converter-5v/trr-2` |
| `library/<desc>` | `library/add-ldo-symbol` |
| `chore/<desc>` | `chore/update-kibot-config` |
| `release-please--*` | (managed automatically) |

---

## `validate-dir-structure.py`

**Purpose:** Validates that a PR touches only one feature directory and only allowed top-level paths.

**Called by:** `pr-checks.yml` — runs as a required check on every PR.

**Local use:**

```bash
git diff --name-only origin/main...HEAD | python3 scripts/ci/validate-dir-structure.py
```

Exit code 0 = valid. Non-zero = invalid, with an error message describing the violation.

**What it checks:**

1. All changed paths are under allowed top-level directories (rejects unexpected paths).
2. No more than one `features/<feature>` directory is touched in a single PR.

> ⚠️ Warning: This check applies to all file types, not just KiCad files. A PR that modifies `features/feature-a/requirements/` and `features/feature-b/requirements/` will also fail.

