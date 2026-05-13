# How to initialise a new hardware feature

> Use this process when starting a brand-new hardware feature from scratch.

---

## When to use this

Use this process when you are creating a completely new hardware feature. For ongoing design work on an existing feature, see [design-workflow.md](design-workflow.md) instead.

---

## Prerequisites

- Write access to the repository
- KiCad 10.0.1 installed
- Repository cloned with submodules:
  ```bash
  git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
  ```

---

## Steps

### 1. Create your branch

```bash
git checkout -b init/<feature-name>
```

The branch name must match `init/<feature>` exactly — CI will reject any other format.

> 💡 Tip: Use lowercase letters and hyphens only in `<feature-name>` (e.g. `init/buck-converter-5v`). Underscores and uppercase letters will fail the branch name check.

---

### 2. Create the required files

Your PR must contain these files inside `features/<feature-name>/`:

| File | Requirement |
|---|---|
| `decisions/DDR-000-design-intent.md` | Real content describing the feature — not a placeholder |
| `decisions/DDR-000-decisions.md` | At least one decision entry — not placeholder |
| `requirements/feature-requirements.yaml` | Real REQ-IDs |
| `requirements/interface-requirements.yaml` | Real interface values |
| `requirements/verification-matrix.md` | REQ-IDs listed |

CI automatically updates `.github/commitlint.config.js` and `.github/release-please-config.json` when the `init/<feature>` branch is first pushed. Run `git pull` after your first push to get the scaffolded files.

> ⚠️ Warning: CI will reject an init PR that contains placeholder content in the required documents. The files must contain real information about the feature.

#### Document version and baseline fields

Each controlled document stub (`feature-requirements.yaml`, `interface-requirements.yaml`, `verification-matrix.md`, `DDR-000.md`) contains a metadata block at the top:

```yaml
document-version: "0.1"
baseline: DRAFT
approved-date: ""
approved-by: ""
```

**What to fill in at init:**
- `document-version`: Start at `"0.1"`. Increment the minor version (0.2, 0.3…) on every substantive change to the document content. Set to `"1.0"` when the document is approved at PDR.
- `baseline`: Set to `DRAFT` until PDR sign-off. Update to `PDR`, `CDR`, or `TRR` at each gate as the document is formally approved.
- `approved-date` and `approved-by`: Leave blank at init — filled in by the lead at gate sign-off.

These fields are the traceability record for the document. They answer: "which version of the requirements was reviewed at CDR?"

---

### 3. Open a draft PR

PR title format:

```
feat(<feature-name>): initialise feature
```

Open the PR as a **draft** immediately — this allows CI checks to start running while you are still working.

---

### 4. Merge

Once CI passes and you have the required approvals, merge the PR.

The scaffold (directories, KiCad templates, and stubs) is committed to your branch automatically by CI when the branch is first pushed — before the PR is opened. Run `git pull` after your first push to see the scaffolded files. On merge, CI does not run additional scaffolding.

The scaffold includes:

- `kicad/`, `simulations/models/`, `calculations/`
- `analysis/mtbf`, `analysis/stress`, `analysis/thermal`, `analysis/doe`
- `bom/`, `bring-up/scripts/`, `circuit-mods/`, `production/fptcs/`, `production/test-programs/`, `production/aoi/`
- `decisions/`, `ci-results/`, `reviews/`, `requirements/`, `datasheet/`
- KiCad project files (`kicad/<feature>.kicad_pro`, `kicad/<feature>.kicad_sch`, `kicad/<feature>.kicad_pcb`), `.kibot.yml`, `README.md`, datasheet stubs

You do not need to create any of these manually.

---

## After merge

Once the scaffold is in place, create a new branch `artifact/<feature-name>/<description>` and begin design work. See [design-workflow.md](design-workflow.md) for the day-to-day process.
