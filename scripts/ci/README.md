# scripts/ci — CI Automation Scripts

> All scripts in this directory run both in CI and locally. There are no CI-only dependencies.

---

## Scripts

| Script | Called by | Also runnable locally |
|---|---|---|
| `init-feature.sh` | `init-feature.yml` | Not recommended |
| `validate-branch-name.sh` | `pr-checks.yml` | Yes |
| `validate-dir-structure.py` | `pr-checks.yml` | Yes |

---

## kicad-visual-diff

The visual diff tool lives in `kicad-visual-diff/` at the repository root, not here. It is the reusable GitHub Action copy and is the canonical source. `kicad-diff.yml` calls it from there.

Do not add a copy of `kicad-visual-diff.py` to this directory.

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
| `init/<feature>` | `init/buck-converter-5v` |
| `artifact/<feature>/<desc>` | `artifact/buck-converter-5v/add-filter` |
| `artifact/<feature>/<desc-HW-N>` | `artifact/buck-converter-5v/add-filter-HW-42` |
| `finding/<feature>/<N>-<desc>` | `finding/buck-converter-5v/7-wrong-footprint` |
| `signoff/<feature>/cdr` | `signoff/buck-converter-5v/cdr` |
| `signoff/<feature>/cdr-rN` | `signoff/buck-converter-5v/cdr-r2` |
| `signoff/<feature>/trr` | `signoff/buck-converter-5v/trr` |
| `signoff/<feature>/trr-N` | `signoff/buck-converter-5v/trr-2` |
| `signoff/<feature>/trr-rN` | `signoff/buck-converter-5v/trr-r2` |
| `signoff/<feature>/release` | `signoff/buck-converter-5v/release` |
| `signoff/<feature>/release-rN` | `signoff/buck-converter-5v/release-r2` |
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
