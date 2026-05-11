# Worked example — hardware feature from idea to release

> **No prior experience needed.** This guide walks through the complete hardware feature lifecycle step by step, using **GitHub Desktop** as the primary tool. GitHub CLI alternatives are shown after each step for users comfortable with the command line.
>
> The example feature is `buck-converter-5v`. Replace this name with your own feature name throughout.

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

## Before you start — clone the repository

> **Do this once only.** If you have already cloned the repository, skip to Stage 1.

### Using GitHub Desktop

1. Open **GitHub Desktop**.
2. Click **File → Clone repository…** (or press `Ctrl+Shift+O` / `⇧⌘O`).
3. Select the **GitHub.com** tab.
4. Search for `hardware-features` and select `rockett90/hardware-features`.
5. Choose a **Local path** on your computer (e.g. `Documents/hardware-features`).
6. Expand **Advanced options** and tick **"Recurse submodules"** — this is essential to download the shared component library.
7. Click the blue **Clone** button.

<!-- screenshot: Clone repository dialog, Recurse submodules ticked, Clone button highlighted -->

> ⚠️ If you skip "Recurse submodules", KiCad will open files with empty symbol boxes. Fix with `git submodule update --init` in a terminal.

### Alternative: GitHub CLI

```bash
git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
cd hardware-features
```

---

## Stage 1 — Init PR (PDR baseline)

### What this stage achieves

The Init PR registers the feature in the repository. On first push to `init/<feature>`, CI scaffolds the full directory structure and stubs onto your branch. On merge, the `pdr/buck-converter-5v/approved` gate record is created.

---

### Step 1.1 — Create the init branch

#### GitHub Desktop

1. In GitHub Desktop, click **Current branch** (the dropdown in the top centre of the window).
2. Click **New branch**.
3. In the **Name** field, type: `init/buck-converter-5v`
4. Make sure **From** shows `main`. If it does not, click the dropdown and select `main`.
5. Click the blue **Create branch** button.

<!-- screenshot: New branch dialog with "init/buck-converter-5v" typed and Create branch highlighted -->

#### Alternative: GitHub CLI

```bash
git checkout main
git pull
git checkout -b init/buck-converter-5v
```

---

### Step 1.2 — Publish the branch immediately

Publishing (pushing) the branch triggers the `Init branch setup` CI workflow, which scaffolds all required directories and stubs automatically. Do this immediately — before making any manual file edits.

#### GitHub Desktop

1. Click the blue **Publish branch** button in the top-right corner of GitHub Desktop.

<!-- screenshot: GitHub Desktop toolbar showing the Publish branch button highlighted -->

#### Alternative: GitHub CLI

```bash
git push -u origin init/buck-converter-5v
```

> ⏱️ **Wait for CI.** The `Init branch setup` workflow runs in under 30 seconds. You can watch it at **github.com → Actions** tab. Do not continue until it completes.

---

### Step 1.3 — Pull the scaffolded files

CI has committed the full directory scaffold directly to your branch. Pull these changes before editing anything.

#### GitHub Desktop

1. In GitHub Desktop, click **Fetch origin** in the top-right corner.
2. If the button changes to **Pull origin**, click it to download the CI commit.

<!-- screenshot: GitHub Desktop toolbar showing Pull origin button -->

#### Alternative: GitHub CLI

```bash
git pull
```

The scaffold includes all required directories and stub files. Open each stub in a text editor and replace the placeholder content with real content for your feature.

> ⚠️ CI checks that stub files contain real content. Placeholder text will cause the init PR to fail gate-check.

---

### Step 1.4 — Edit the stub files

Open each file and fill in real content:

| File | What to fill in |
|---|---|
| `features/buck-converter-5v/requirements/feature-requirements.yaml` | Real REQ-IDs and requirement statements |
| `features/buck-converter-5v/requirements/interface-requirements.yaml` | Interface definitions (voltage, current, connector) |
| `features/buck-converter-5v/requirements/verification-matrix.md` | All REQ-IDs listed with verification method |
| `features/buck-converter-5v/decisions/DDR-000-design-intent.md` | Problem statement, scope, and constraints |
| `features/buck-converter-5v/decisions/DDR-000-decisions.md` | At least one decision entry |
| `features/buck-converter-5v/README.md` | Feature description (1–3 paragraphs) |

---

### Step 1.5 — Commit and push

#### GitHub Desktop

1. After editing files, switch to GitHub Desktop. Changed files appear in the **Changes** panel on the left.
2. All changed files should be ticked. Verify the list looks correct.
3. In the **Summary** box at the bottom-left, type a commit message. Example:
   ```
   feat(buck-converter-5v): fill in PDR stubs
   ```
4. Click the blue **Commit to `init/buck-converter-5v`** button.
5. Click **Push origin** in the top-right corner.

<!-- screenshot: GitHub Desktop Changes panel with commit summary filled in and Commit button highlighted -->

#### Alternative: GitHub CLI

```bash
git add features/buck-converter-5v/
git commit -m "feat(buck-converter-5v): fill in PDR stubs"
git push
```

---

### Step 1.6 — Open the init PR

#### GitHub Desktop

1. In GitHub Desktop, click **Branch → Create pull request** in the menu bar.
   Your browser opens to the GitHub PR creation page.

<!-- screenshot: GitHub Desktop Branch menu with Create pull request highlighted -->

#### Alternative: GitHub CLI

```bash
gh pr create --web
```

On the PR creation page:

1. Set the **title** to:
   ```
   feat(buck-converter-5v): initialise feature
   ```
2. Click the **dropdown arrow** on the green button (do not click the button itself yet).
3. Select **Create draft pull request**.
4. Click **Create draft pull request**.

<!-- screenshot: PR creation page showing the dropdown arrow on the green button and "Create draft pull request" option -->

> 💡 **Template autofill:** Within a few seconds, the `PR template autofill` workflow fills the correct checklist into the PR body automatically. If the body is blank, wait a moment and refresh the page. **Do not type in the body before it fills in.**

---

### Step 1.7 — Tick all PDR checklist items

The PR body contains the PDR gate checklist. Tick every item by clicking the `[ ]` boxes on the GitHub PR page:

- Feature naming convention followed
- `feature-requirements.yaml` contains real REQ-IDs
- `interface-requirements.yaml` contains real interface definitions
- `verification-matrix.md` lists all REQ-IDs
- `DDR-000-design-intent.md` captures the problem statement, scope, and constraints
- `DDR-000-decisions.md` contains at least one decision entry
- Feature scope present in `commitlint.config.js` (added automatically by CI — open `.github/commitlint.config.js` and verify that `buck-converter-5v` appears in the `scopes` array)
- Feature package present in `release-please-config.json` (added automatically by CI)
- PDR date and owner name recorded

`gate-check.yml` **blocks merge** if any `- [ ]` item remains unchecked.

---

### Step 1.8 — Mark ready for review and merge

1. On the PR page, click **"Ready for review"** once all checklist items are ticked and CI is green.
2. Request lead approval.
3. Once approved and CI passes, click **Squash and merge**.
4. Confirm the merge commit title matches the PR title format.
5. Click **Confirm squash and merge**.

> **After merge, CI creates the `pdr/buck-converter-5v/approved` gate record.**

---

## Stage 2 — Design work (PDR → CDR)

### What this stage achieves

Design artefacts are committed through one or more `artifact/` PRs — one PR per discrete artefact. This keeps the review history clean and makes it clear what changed in each review.

### Step 2.1 — Create an artifact branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type the branch name, e.g.: `artifact/buck-converter-5v/initial-schematic`
3. Confirm **From** shows `main`, then click **Create branch**.
4. Click **Publish branch** in the top-right corner.

<!-- screenshot: New branch dialog with artifact branch name typed -->

#### Alternative: GitHub CLI

```bash
git checkout main && git pull
git checkout -b artifact/buck-converter-5v/initial-schematic
git push -u origin artifact/buck-converter-5v/initial-schematic
```

### Step 2.2 — Open a draft PR immediately

Open a draft PR right after the first push so CI checks can start running.

#### GitHub Desktop

Click **Branch → Create pull request**. Set the title, select **Create draft pull request**, and submit.

#### Alternative: GitHub CLI

```bash
gh pr create --draft --title "feat(buck-converter-5v): add initial schematic"
```

> The PR body auto-fills within seconds. Wait for it before typing.

### Step 2.3 — Design, commit, and push

Work in KiCad. After each meaningful change:

#### GitHub Desktop

1. Switch to GitHub Desktop — changed files appear in **Changes**.
2. Tick the files to include, type a commit message, and click **Commit to `artifact/...`**.
3. Click **Push origin**.

#### Alternative: GitHub CLI

```bash
git add features/buck-converter-5v/
git commit -m "feat(buck-converter-5v): add initial schematic"
git push
```

### Step 2.4 — Use slash commands during review

Post these as comments on the PR (write access required):

| Command | When to use |
|---|---|
| `/render` | After significant schematic changes — exports SVG so reviewers can read it without KiCad |
| `/kicad-diff` | Four-column visual diff of what changed vs base branch |
| `/ai-review` | AI schematic analysis — run before requesting human review |
| `/erc` | Electrical Rules Check (informational, does not block merge) |
| `/drc` | Design Rules Check (informational, does not block merge) |

> The dispatcher reacts 👀 on receipt, ✅ on success, ❌ on failure.

### Step 2.5 — Mark ready for review and merge

1. Post `/render` to generate fresh SVGs.
2. Post `/ai-review` and resolve all CRITICAL findings.
3. Click **"Ready for review"** on the PR.
4. Request lead approval and merge once approved and CI is green.

Repeat for each subsequent artefact (PCB layout, calculations, BOM, etc.).

---

## Stage 3 — CDR sign-off

### What this stage achieves

CDR is a formal gate confirming the design is complete and reviewed. The `gate-check.yml` workflow blocks merge until all checklist items are ticked. On merge, CI creates the `cdr/buck-converter-5v/approved` gate tag and commits `library.lock`.

### Step 3.1 — Create the CDR branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type: `signoff/buck-converter-5v/cdr`
3. Confirm **From** shows `main`, then click **Create branch**.
4. Click **Publish branch** immediately.

<!-- screenshot: New branch dialog with signoff branch name -->

#### Alternative: GitHub CLI

```bash
git checkout main && git pull
git checkout -b signoff/buck-converter-5v/cdr
git push -u origin signoff/buck-converter-5v/cdr
```

> ⏱️ Wait for the `Signoff branch setup` workflow to complete (usually under 30 seconds) before opening the PR. It commits `gate-evidence.md` to your branch automatically.

### Step 3.2 — Pull the auto-committed gate evidence file

#### GitHub Desktop

1. Click **Fetch origin**, then **Pull origin** when it appears.

#### Alternative: GitHub CLI

```bash
git pull
```

### Step 3.3 — Open the CDR PR

#### GitHub Desktop

Click **Branch → Create pull request**. Your browser opens.

#### Alternative: GitHub CLI

```bash
gh pr create --web
```

Set the title:
```
chore(buck-converter-5v): CDR sign-off
```

> **Do not use Draft for signoff PRs.** Open it as a regular PR straight away. The checklist auto-fills within seconds — refresh if it is blank.

### Step 3.4 — Post `/render`

Post `/render` as a PR comment. This generates SVGs for the review record.

### Step 3.5 — Tick all CDR checklist items

Tick every item in the PR body. The CDR checklist includes:

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
- CDR date and owner name recorded

`gate-check.yml` blocks merge if any `- [ ]` item remains unchecked.

### Step 3.6 — Merge

Request lead approval. Once approved and CI is green, click **Squash and merge**.

> **After merge, CI automatically:**
> - Creates the `cdr/buck-converter-5v/approved` gate tag
> - Commits `reviews/library.lock` to `main`
> - Generates the datasheet stub (if it does not already exist)

---

## Stage 4 — Post-CDR work (CDR → TRR)

### What this stage achieves

The physical hardware is built and brought up. Verification evidence is committed. The datasheet is filled in.

### Step 4.1 — Bring-up and test evidence PRs

Continue using `artifact/` branches. Examples:

| Artefact | Branch | PR title |
|---|---|---|
| Bring-up notes | `artifact/buck-converter-5v/bring-up` | `test(buck-converter-5v): add bring-up checklist and notes` |
| Measurement data | `artifact/buck-converter-5v/efficiency-measurements` | `test(buck-converter-5v): add efficiency measurement data` |
| Thermal images | `artifact/buck-converter-5v/thermal-evidence` | `test(buck-converter-5v): add thermal characterisation evidence` |

Follow the same branch → push → draft PR → commit → merge process as Stage 2.

### Step 4.2 — Fill in the datasheet source files

Edit these files using KiCad or a text editor, then commit them via an `artifact/` PR:

| File | What to fill in |
|---|---|
| `features/buck-converter-5v/datasheet/specs.yaml` | Characterised min/nom/max values — actual achieved values, not requirements |
| `features/buck-converter-5v/datasheet/application-notes.md` | Typical application, configuration guidance, layout recommendations |
| `features/buck-converter-5v/datasheet/errata.md` | Known issues against specific hardware revisions |

> ⚠️ Do not edit `buck-converter-5v-datasheet.md` directly — it is generated. Edit the source files above and run `/datasheet` to regenerate.

### Step 4.3 — Run `/datasheet` to regenerate the output

Post `/datasheet` as a PR comment. The updated files are committed automatically.

### Step 4.4 — Finding PRs (if defects are found)

If a defect is found during bring-up:

1. Raise a GitHub Issue using the IVV Finding issue template.
2. The owner confirms the severity label (`finding: minor`, `finding: moderate`, or `finding: major`).
3. Create a finding branch:

   **GitHub Desktop:** New branch → `finding/buck-converter-5v/42-output-voltage-low` → Publish.

   **Alternative: GitHub CLI:**
   ```bash
   git checkout main && git pull
   git checkout -b finding/buck-converter-5v/42-output-voltage-low
   git push -u origin finding/buck-converter-5v/42-output-voltage-low
   ```

4. Open a PR with `Resolves #42` in the **body**. PR title:
   ```
   fix(buck-converter-5v): correct feedback resistor divider — IVV finding #42
   ```

**Severity and gate re-entry:**
- `finding: minor` — no gate re-entry required unless the owner decides otherwise
- `finding: moderate` — re-TRR required (`signoff/buck-converter-5v/trr-1`)
- `finding: major` — re-CDR then re-TRR required (`signoff/buck-converter-5v/cdr-1` then `signoff/buck-converter-5v/trr-1`)

---

## Stage 5 — TRR sign-off

### What this stage achieves

TRR confirms the hardware is built, brought up, and ready for formal verification. On merge, CI creates the `trr/buck-converter-5v/approved` tag.

### Step 5.1 — Create the TRR branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type: `signoff/buck-converter-5v/trr`
3. From `main` → **Create branch** → **Publish branch** immediately.

#### Alternative: GitHub CLI

```bash
git checkout main && git pull
git checkout -b signoff/buck-converter-5v/trr
git push -u origin signoff/buck-converter-5v/trr
```

> ⏱️ Wait for `Signoff branch setup` to complete and commit `gate-evidence.md` before opening the PR.

### Step 5.2 — Pull and open the TRR PR

#### GitHub Desktop

1. **Fetch origin** → **Pull origin**.
2. **Branch → Create pull request**.

#### Alternative: GitHub CLI

```bash
git pull
gh pr create --web
```

PR title:
```
chore(buck-converter-5v): TRR sign-off
```

> The checklist auto-fills within seconds — refresh if blank.

### Step 5.3 — Post `/render`

Post `/render` as a PR comment for the record.

### Step 5.4 — Tick all TRR checklist items

- ERC clean (zero errors)
- DRC clean (zero errors)
- Calculations complete and reviewed
- Simulations complete and reviewed
- Stress analysis complete
- Thermal analysis complete
- BOM MPNs all confirmed (no TBDs)
- Bring-up checklist complete and notes committed
- FPTCS complete
- Circuit mods documented
- All TRR-gate verification matrix items marked Verified
- All REQ-IDs evidenced
- `datasheet/specs.yaml` complete — no `[COMPLETE BEFORE TRR]` placeholders
- Datasheet committed and reviewed by owner
- All CRITICAL AI review findings resolved
- TRR date and owner name recorded

### Step 5.5 — Merge

Request lead approval. Once CI is green and approval is in, click **Squash and merge**.

> **After merge, CI creates the `trr/buck-converter-5v/approved` tag.**

---

## Stage 6 — Final Release sign-off

### What this stage achieves

This gate formally authorises the manufacturing outputs for production. On merge, CI creates `release/buck-converter-5v/approved` and attaches release documents to a GitHub Release.

### Step 6.1 — Verify pre-conditions

Before raising this PR, confirm these tags exist by checking **github.com → your repo → Releases** or by running:

```bash
git fetch --tags
git tag -l "*/buck-converter-5v/*"
```

Required tags:
- `cdr/buck-converter-5v/approved`
- `trr/buck-converter-5v/approved`

Also confirm all P1 and P2 IVV findings are resolved or formally deferred.

### Step 6.2 — Create the release sign-off branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type: `signoff/buck-converter-5v/release`
3. From `main` → **Create branch** → **Publish branch** immediately.

#### Alternative: GitHub CLI

```bash
git checkout main && git pull
git checkout -b signoff/buck-converter-5v/release
git push -u origin signoff/buck-converter-5v/release
```

> ⏱️ Wait for `Signoff branch setup` to complete before opening the PR.

### Step 6.3 — Pull and open the release sign-off PR

#### GitHub Desktop

1. **Fetch origin** → **Pull origin**.
2. **Branch → Create pull request**.

#### Alternative: GitHub CLI

```bash
git pull
gh pr create --web
```

PR title:
```
chore(buck-converter-5v): final release sign-off
```

### Step 6.4 — Tick all Release checklist items

- `cdr/buck-converter-5v/approved` tag present
- `trr/buck-converter-5v/approved` tag present
- `features/buck-converter-5v/reviews/library.lock` committed
- ERC report clean
- All CDR-gate checklist items remain satisfied
- All TRR-gate checklist items remain satisfied
- All P1 and P2 findings resolved or formally deferred with owner sign-off
- Manufacturing outputs generated by CI without errors
- Gerbers visually verified against PCB layout
- DRC confirmed clean
- BOM has no TBDs — all MPNs confirmed and available
- CPL file verified against placement drawing
- CHANGELOG reviewed and accurate
- Version number correct
- Release date and owner name recorded

### Step 6.5 — Merge

Request lead approval. Once CI is green and approval is in, click **Squash and merge**.

> **After merge, CI:**
> - Creates the `release/buck-converter-5v/approved` tag
> - Collects and converts release documents to PDF
> - Creates a GitHub Release at the tag with all release documents attached

---

## Stage 7 — Release PR

### What this stage achieves

The production tag and final GitHub Release are created. Manufacturing outputs are attached and ready for the PCB manufacturer.

### Step 7.1 — Merge the release-please Release PR

Release-please automatically maintains a Release PR. It opens after the first conventional commit merges to `main` and updates on every subsequent push. Merge it after the Final Release sign-off is complete.

The Release PR title looks like:
```
chore(buck-converter-5v): release 1.0.0
```

**Merge this PR — never close it manually.** Closing prevents the production tag from being created.

To merge it:

1. Go to the **Pull requests** tab on GitHub.
2. Find the release-please Release PR (it is labelled `autorelease: pending`).
3. Click **Squash and merge**.

### Step 7.2 — What happens on merge

**On merge, CI automatically:**
- Creates the production tag, e.g. `buck-converter-5v-v1.0.0`
- Checks that `release/buck-converter-5v/approved` exists — if the tag is absent, manufacturing CI fails immediately
- Runs KiBot to generate Gerbers, drill files, BOM, CPL, and schematic PDF
- Attaches all manufacturing outputs to the GitHub Release as a ZIP

> 💡 Check the `Manufacturing Release` Actions run triggered by the production tag. Any ⛔ in the step summary means outputs are incomplete — do not send to the manufacturer until resolved.

---

## Tag summary

After completing all seven stages, these tags exist in the repository:

| Tag | Created by | Meaning |
|---|---|---|
| `cdr/buck-converter-5v/approved` | CDR sign-off merge | CDR gate passed |
| `trr/buck-converter-5v/approved` | TRR sign-off merge | TRR gate passed |
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

> **Signoff branches** (`signoff/**`) are scaffolded automatically on first push — same as `init/**` branches. Publish the branch immediately and wait for `Signoff branch setup` to commit `gate-evidence.md` before opening your PR.

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

**CI that runs automatically (no command needed):**

| Event | What CI does |
|---|---|
| Init branch push (`init/**`) | Scaffold directories, copy stubs/templates, patch commitlint and release-please config |
| Signoff branch push (`signoff/**`) | Commit `gate-evidence.md` to the branch |
| Any PR opened | `PR template autofill` fills the correct checklist into the PR body |
| Artifact PR with `.kicad_sch` or `.kicad_pcb` change | ERC/DRC runs automatically and posts a comment |
| Artifact PR marked Ready for Review | AI schematic review runs and posts CRITICAL/ADVISORY findings |
| CDR merge | Create `cdr/.../approved` tag, commit `library.lock`, generate datasheet stub |
| TRR merge | Create `trr/.../approved` tag |
| Release sign-off merge | Create `release/.../approved` tag, attach release documents to GitHub Release |
| Release PR merge | Create production tag, run KiBot, attach manufacturing outputs to GitHub Release |

---

## See also

- [docs/tool-setup.md](../tool-setup.md) — installing GitHub Desktop and GitHub CLI
- [docs/how-to/init-feature.md](init-feature.md) — detailed steps for the Init PR
- [docs/how-to/design-workflow.md](design-workflow.md) — day-to-day workflow for artifact PRs
- [docs/how-to/cdr-signoff.md](cdr-signoff.md) — detailed steps for CDR sign-off
- [docs/how-to/trr-signoff.md](trr-signoff.md) — detailed steps for TRR sign-off
- [docs/how-to/release-signoff.md](release-signoff.md) — detailed steps for Final Release sign-off
- [docs/how-to/datasheet.md](datasheet.md) — how to generate the feature datasheet

