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

Your PR must contain these four files inside `features/<feature-name>/`:

| File | Requirement |
|---|---|
| `decisions/DDR-000-feature-overview.md` | Real content describing the feature — not a placeholder |
| `requirements/feature-requirements.yaml` | Real REQ-IDs |
| `requirements/interface-requirements.yaml` | Real interface values |
| `requirements/verification-matrix.md` | REQ-IDs listed |

Your PR must also update these two repository-level files:

| File | Change required |
|---|---|
| `.github/commitlint.config.js` | Add the new feature name to `scope-enum` |
| `.github/release-please-config.json` | Add the new package entry |

> ⚠️ Warning: CI will reject an init PR that contains placeholder content in the required documents. The files must contain real information about the feature.

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

On merge, the `init-feature.yml` workflow automatically scaffolds all remaining directories inside `features/<feature-name>/`, including:

- `schematics/`, `pcb/`, `simulations/`, `calculations/`
- `analysis/mtbf`, `analysis/stress`, `analysis/thermal`, `analysis/doe`
- `bom/`, `bring-up/`, `circuit-mods/`, `production/`, `reviews/`
- KiCad project files copied from `templates/`

You do not need to create any of these manually.

---

## After merge

Once the scaffold is in place, create a new branch `artifact/<feature-name>/<description>` and begin design work. See [design-workflow.md](design-workflow.md) for the day-to-day process.
