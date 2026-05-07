# Worked example — hardware feature from idea to release

> This guide walks through the complete hardware feature lifecycle using `buck-converter-5v` as the example. Every step shown here maps directly to the automated CI and branch conventions in this repository.

---

## Overview

A hardware feature passes through seven stages before production-authorised manufacturing outputs are available:

| Stage | Branch | Gate |
|---|---|---|
| 1. Init (PDR) | `init/buck-converter-5v` | All PDR checklist items ticked |
| 2. Design work | `artifact/buck-converter-5v/<desc>` | CI checks on every push |
| 3. CDR sign-off | `signoff/buck-converter-5v/cdr` | All CDR checklist items ticked |
| 4. Post-CDR work | `artifact/buck-converter-5v/<desc>` | CI checks on every push |
| 5. TRR sign-off | `signoff/buck-converter-5v/trr` | All TRR checklist items ticked |
| 6. Final Release sign-off | `signoff/buck-converter-5v/release` | All Release checklist items ticked |
| 7. Release PR | (opened by release-please) | `release/buck-converter-5v/approved` tag must exist |

---

## Stage 1 — Init PR (PDR baseline)

### What this stage achieves

The Init PR registers the feature in the repository. On merge, CI scaffolds the full directory structure automatically and creates the `pdr/buck-converter-5v/approved` git tag.

### 1.1 Create the branch

```bash
git checkout main
git pull
git checkout -b init/buck-converter-5v
```

The branch name must match `init/<feature>` exactly. CI will fail the "Validate branch name" check if it does not.

### 1.2 Create the required files

Create the following files inside `features/buck-converter-5v/`:

| File | What to write |
|---|---|
| `decisions/DDR-000-feature-overview.md` | Problem statement, design approach, key decisions — real content, not a placeholder |
| `requirements/feature-requirements.yaml` | Real REQ-IDs with descriptions and acceptance criteria |
| `requirements/interface-requirements.yaml` | Real interface definitions: voltage, current, signal levels |
| `requirements/verification-matrix.md` | All REQ-IDs with a verification method for each |

> ⚠️ Warning: CI checks that these files contain real content. Placeholder text will cause the init PR to fail.

### 1.3 Update repository-level configuration

Two repository-level files must be updated in the same PR:

**`.github/commitlint.config.js`** — add `buck-converter-5v` to the `scope-enum` array so that PR titles using this feature as a scope are accepted by commitlint CI.

**`.github/release-please-config.json`** — add a package entry for the feature. Copy the `_example-feature` block, rename the key, and update `package-name` and `changelog-path`:

```json
"buck-converter-5v": {
  "release-type": "simple",
  "package-name": "buck-converter-5v",
  "changelog-path": "features/buck-converter-5v/CHANGELOG.md",
  "bump-minor-pre-major": true
}
```

CI will fail the init PR with a clear error if the `release-please-config.json` entry is missing.

### 1.4 Open a draft PR using the init template

Open the PR using this URL (replace `<branch>` with `init/buck-converter-5v`):

```
https://github.com/rockett90/hardware-features/compare/main...init/buck-converter-5v?template=init.md
```

PR title format:
```
feat(buck-converter-5v): initialise feature
```

Open as a **draft** immediately — CI starts running on the first push.

### 1.5 Tick all PDR checklist items

The PR description contains the PDR gate checklist. Tick every item:

- Feature naming convention followed
- `feature-requirements.yaml` contains real REQ-IDs
- `interface-requirements.yaml` contains real interface definitions
- `verification-matrix.md` lists all REQ-IDs
- `DDR-000-feature-overview.md` contains real content
- Feature scope added to `commitlint.config.js`
- Feature package added to `release-please-config.json`
- PDR date and lead name recorded

`gate-check.yml` runs on every push and **blocks merge** if any `- [ ]` item remains unchecked.

### 1.6 Merge

Once CI passes and approvals are in place, merge the PR.

**On merge, `init-feature.yml` automatically:**
- Scaffolds all directories inside `features/buck-converter-5v/` — `schematics/`, `pcb/`, `simulations/`, `calculations/`, `analysis/mtbf`, `analysis/stress`, `analysis/thermal`, `analysis/doe`, `bom/`, `bring-up/`, `circuit-mods/`, `production/`, `reviews/`
- Copies KiCad project files from `templates/`
- Creates the git tag `pdr/buck-converter-5v/approved`

You do not create any of these directories or files manually.

---

## Stage 2 — Design work (PDR → CDR)

### What this stage achieves

Design artefacts are committed through one or more `artifact/` PRs — one PR per discrete artefact. This keeps the review history clean and makes it clear what changed in each review.

### Example artefacts for a buck converter

| Artefact | Branch | PR title |
|---|---|---|
| Initial schematic | `artifact/buck-converter-5v/initial-schematic` | `feat(buck-converter-5v): add initial schematic` |
| PCB layout | `artifact/buck-converter-5v/pcb-layout` | `feat(buck-converter-5v): add PCB layout` |
| Inductor calculations | `artifact/buck-converter-5v/inductor-calculations` | `docs(buck-converter-5v): add inductor ripple current calculations` |
| Stress analysis | `artifact/buck-converter-5v/stress-analysis` | `docs(buck-converter-5v): add component stress analysis` |
| BOM | `artifact/buck-converter-5v/bom` | `feat(buck-converter-5v): add initial BOM` |

### Workflow for each artifact PR

```bash
git checkout main
git pull
git checkout -b artifact/buck-converter-5v/initial-schematic
git push -u origin artifact/buck-converter-5v/initial-schematic
```

Open a **draft PR** immediately after the first push. PR title format:
```
feat(buck-converter-5v): add initial schematic
```

### Slash commands during design

Post these as PR comments to trigger CI actions. Write access is required.

| Command | When to use |
|---|---|
| `/render` | After significant schematic changes — exports schematic as SVG so reviewers can read it without KiCad |
| `/kicad-diff` | Shows a four-column visual diff of what changed vs the base branch |
| `/ai-review` | AI analysis of schematic changes against company engineering standards (derating, ESD, protection) — run before requesting human review |
| `/erc` | Electrical Rules Check — informational, does not block merge |
| `/drc` | Design Rules Check — informational, does not block merge |

The dispatcher reacts 👀 on receipt, ✅ on success, ❌ on failure.

### Before marking ready for review

1. Post `/render` to generate current schematic SVGs for reviewers.
2. Post `/ai-review` and resolve all ⚠️ CRITICAL findings before requesting human review.
3. Click **"Ready for review"** on the PR.

---

## Stage 3 — CDR sign-off

### What this stage achieves

CDR is a formal gate confirming the design is complete and reviewed before proceeding to build. The `gate-check.yml` workflow blocks merge until all checklist items are ticked.

### 3.1 Create the CDR branch

```bash
git checkout main
git pull
git checkout -b signoff/buck-converter-5v/cdr
```

This is a **document-only branch** — no KiCad file changes. The CDR sign-off PR records the gate evidence; the design artefacts are already on `main` via the artifact PRs.

### 3.2 Open the CDR PR using the CDR template

```
https://github.com/rockett90/hardware-features/compare/main...signoff/buck-converter-5v/cdr?template=cdr-signoff.md
```

PR title format:
```
chore(buck-converter-5v): CDR sign-off
```

### 3.3 Post `/render`

Post `/render` as a PR comment to generate current schematic SVGs. These are stored as part of the CDR review record.

### 3.4 Tick all CDR checklist items

The CDR template checklist includes:

- ERC clean (zero errors, zero warnings unless formally accepted)
- Calculations complete and reviewed
- Simulations complete and reviewed
- PCB reviewed
- BOM has no TBDs
- MTBF confirmed
- All components derated per derating guidelines
- ESD protection in place on all external-facing signals
- Protection circuits reviewed (OVP, OCP, reverse polarity)
- PCB design rules met
- Creepage and clearance checked against IEC 62368
- Verification matrix CDR-gate column complete
- All REQ-IDs have evidence or a documented plan
- DDR-000 complete and reviewed
- All CRITICAL AI review findings resolved
- CDR date and lead name recorded

`gate-check.yml` blocks merge if any `- [ ]` item remains unchecked.

### 3.5 Merge

Once CI passes and approvals are in place, merge the PR.

**On merge, CI automatically:**
- Creates the git tag `cdr/buck-converter-5v/approved`
- Commits `reviews/library.lock` to `main` (records the exact component library revision used at CDR)
- Generates the datasheet stub at `features/buck-converter-5v/datasheet/buck-converter-5v-datasheet.md` — only if it does not already exist

---

## Stage 4 — Post-CDR work (CDR → TRR)

### What this stage achieves

The physical hardware is built and brought up. Verification evidence is committed. The datasheet is filled in.

### 4.1 Bring-up and test evidence PRs

Continue using `artifact/` branches for discrete artefacts:

| Artefact | Branch | PR title |
|---|---|---|
| Bring-up checklist and notes | `artifact/buck-converter-5v/bring-up` | `test(buck-converter-5v): add bring-up checklist and notes` |
| Measurement data | `artifact/buck-converter-5v/efficiency-measurements` | `test(buck-converter-5v): add efficiency measurement data` |
| Thermal images | `artifact/buck-converter-5v/thermal-evidence` | `test(buck-converter-5v): add thermal characterisation evidence` |

### 4.2 Fill in the datasheet source files

During this phase, fill in the source files in `features/buck-converter-5v/datasheet/`:

| File | What to fill in |
|---|---|
| `datasheet/specs.yaml` | Characterised min/nom/max values for all interfaces and performance parameters |
| `datasheet/application-notes.md` | Typical application, configuration guidance, layout recommendations |
| `datasheet/errata.md` | Known issues against specific hardware revisions |

> ⚠️ Do not edit `buck-converter-5v-datasheet.md` directly — it is a generated file. Edit the source files above and run `/datasheet` to regenerate it.

### 4.3 Run `/datasheet` to regenerate the output

Post `/datasheet` as a PR comment to regenerate `buck-converter-5v-datasheet.md` from the source files. The updated file is committed to `main` automatically.

The TRR checklist requires all `[COMPLETE BEFORE TRR]` placeholders to be replaced and the datasheet committed before TRR can merge.

### 4.4 Finding PRs (if defects are found during bring-up)

If a defect is found:

1. Raise a GitHub Issue using the IVV Finding issue template.
2. The lead confirms the severity label: `finding: minor`, `finding: moderate`, or `finding: major`.
3. Create a `finding/<feature>/<N>-<desc>` branch where `N` is the GitHub Issue number:

```bash
git checkout -b finding/buck-converter-5v/42-output-voltage-low
```

4. Open the PR with `Resolves #42` in the **body** (not the title). PR title format:
```
fix(buck-converter-5v): correct feedback resistor divider — IVV finding #42
```

CI automatically adds `finding: in-progress` to the issue when the PR opens, and `finding: resolved` plus the merge commit SHA when it merges.

---

## Stage 5 — TRR sign-off

### What this stage achieves

TRR is a formal gate confirming the hardware is built, brought up, and ready to enter formal verification. On merge, CI creates an rc pre-release automatically.

### 5.1 Create the TRR branch

```bash
git checkout main
git pull
git checkout -b signoff/buck-converter-5v/trr
```

This is a **document-only branch**.

### 5.2 Open the TRR PR using the TRR template

```
https://github.com/rockett90/hardware-features/compare/main...signoff/buck-converter-5v/trr?template=trr-signoff.md
```

PR title format:
```
chore(buck-converter-5v): TRR sign-off
```

### 5.3 Post `/render`

Post `/render` as a PR comment to generate current schematic SVGs for the record.

### 5.4 Tick all TRR checklist items

The TRR template checklist includes:

- ERC clean (zero errors)
- DRC clean (zero errors)
- Calculations complete and reviewed
- Simulations complete and reviewed
- Stress analysis complete
- Thermal analysis complete
- BOM MPNs all confirmed (no TBDs)
- Bring-up checklist complete and notes committed to `features/buck-converter-5v/bring-up/`
- FPTCS complete
- Circuit mods documented in `features/buck-converter-5v/circuit-mods/`
- All TRR-gate verification matrix items marked Verified
- All REQ-IDs evidenced
- All CRITICAL AI review findings resolved
- TRR date and lead name recorded

`gate-check.yml` blocks merge if any `- [ ]` item remains unchecked.

### 5.5 Merge

Once CI passes and approvals are in place, merge the PR.

**On merge, CI automatically:**
- Creates the rc git tag, e.g. `buck-converter-5v-v1.0.0-rc.1`
- Creates a GitHub pre-release at that tag
- Triggers KiBot to generate manufacturing outputs (Gerbers, drill, BOM, CPL, schematic PDF) and attach them to the pre-release

> 💡 Check the Actions workflow run for the rc tag. Any ⛔ in the step summary means manufacturing outputs are incomplete.

---

## Stage 6 — Final Release sign-off

### What this stage achieves

This gate formally authorises the manufacturing outputs for production. The `release/buck-converter-5v/approved` tag is the authorisation record.

### 6.1 Verify pre-conditions

Before raising the release sign-off PR, confirm:
- `pdr/buck-converter-5v/approved` tag exists in the repository
- `cdr/buck-converter-5v/approved` tag exists in the repository
- `buck-converter-5v-v1.0.0-rc.1` (or the latest rc tag) exists
- Manufacturing outputs from the rc tag generated cleanly

### 6.2 Create the release sign-off branch

```bash
git checkout main
git pull
git checkout -b signoff/buck-converter-5v/release
```

This is a **document-only branch**.

### 6.3 Open the release sign-off PR using the release template

```
https://github.com/rockett90/hardware-features/compare/main...signoff/buck-converter-5v/release?template=release-signoff.md
```

PR title format:
```
chore(buck-converter-5v): final release sign-off
```

### 6.4 Tick all Release checklist items

The release sign-off template checklist includes:

- `pdr/buck-converter-5v/approved` tag present
- `cdr/buck-converter-5v/approved` tag present
- `buck-converter-5v-vX.Y.Z-rc.N` tag present
- `features/buck-converter-5v/reviews/library.lock` committed
- ERC report clean
- All CDR-gate checklist items remain satisfied
- All TRR-gate checklist items remain satisfied
- All P1 and P2 findings resolved or formally deferred with lead sign-off
- Manufacturing outputs generated by CI without errors
- Gerbers visually verified against PCB layout
- DRC confirmed clean
- BOM has no TBDs — all MPNs confirmed and available
- CPL file verified against placement drawing
- CHANGELOG reviewed and accurate
- Version number correct
- Release date and lead name recorded

`gate-check.yml` blocks merge if any `- [ ]` item remains unchecked.

### 6.5 Merge

Once CI passes and approvals are in place, merge the PR.

**On merge, CI automatically creates the git tag `release/buck-converter-5v/approved`.**

---

## Stage 7 — Release PR

### What this stage achieves

The production tag and final GitHub Release are created. Manufacturing outputs are attached to the release and are ready for the PCB manufacturer.

### 7.1 Merge the release-please Release PR

Release-please automatically opens a Release PR after the TRR merge. It tracks conventional commits from the merged artifact PRs and generates `CHANGELOG.md` content.

The Release PR appears in the repository's open PRs as something like:
```
chore(buck-converter-5v): release 1.0.0
```

**Merge this PR — never close it manually.** Closing it prevents the production tag from being created.

### 7.2 What happens on merge

**On merge, CI automatically:**
- Creates the production git tag, e.g. `buck-converter-5v-v1.0.0`
- Creates the final GitHub Release at that tag
- Checks that `release/buck-converter-5v/approved` exists before running manufacturing outputs — if the tag is missing the manufacturing CI stops immediately
- Runs KiBot to generate Gerbers, drill files, BOM, CPL, and schematic PDF
- Attaches all manufacturing outputs to the GitHub Release

The manufacturing outputs attached to the `buck-converter-5v-v1.0.0` release are the production-authorised files.

---

## Tag summary

After completing all seven stages, the following tags exist in the repository:

| Tag | Created by | Meaning |
|---|---|---|
| `pdr/buck-converter-5v/approved` | Init PR merge | PDR gate passed |
| `cdr/buck-converter-5v/approved` | CDR sign-off merge | CDR gate passed |
| `buck-converter-5v-v1.0.0-rc.1` | TRR sign-off merge | Pre-release candidate |
| `release/buck-converter-5v/approved` | Release sign-off merge | Manufacturing authorised |
| `buck-converter-5v-v1.0.0` | Release PR merge | Production release |

---

## Quick reference

**Branch names (CI-validated):**
```
init/buck-converter-5v
artifact/buck-converter-5v/<desc>
signoff/buck-converter-5v/cdr
signoff/buck-converter-5v/trr
signoff/buck-converter-5v/release
finding/buck-converter-5v/<N>-<desc>
```

**PR title format:**
```
type(buck-converter-5v): description
```
Types: `feat`, `fix`, `docs`, `test`, `chore`

**Slash commands (post as PR comment):**
```
/render         — export schematic SVG
/kicad-diff     — four-column visual diff vs base branch
/ai-review      — AI schematic review
/erc            — Electrical Rules Check (informational)
/drc            — Design Rules Check (informational)
/datasheet      — regenerate datasheet from specs.yaml and application-notes.md
```

---

## See also

- [init-feature.md](init-feature.md) — detailed steps for the Init PR
- [design-workflow.md](design-workflow.md) — day-to-day workflow for artifact PRs
- [cdr-signoff.md](cdr-signoff.md) — detailed steps for CDR sign-off
- [trr-signoff.md](trr-signoff.md) — detailed steps for TRR sign-off
- [release-signoff.md](release-signoff.md) — detailed steps for Final Release sign-off
- [datasheet.md](datasheet.md) — how to generate the feature datasheet
