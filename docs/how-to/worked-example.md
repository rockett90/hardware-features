# Worked example — hardware feature from idea to release

> **No prior experience needed.** This guide walks through the complete hardware feature lifecycle step by step, using **GitHub Desktop** as the primary tool. GitHub CLI alternatives are shown where the steps differ meaningfully.
>
> The example feature is `buck-converter-5v`. Replace this name with your own feature name throughout.

---

## Overview

A hardware feature passes through eight stages before production-authorised manufacturing outputs are available:

| Stage | Branch | Exit criteria |
|---|---|---|
| 1. Init (PDR) | `init/buck-converter-5v` | All PDR checklist items ticked and PR merged |
| 2. Design work | `artifact/buck-converter-5v/<desc>` | One or more artifact PRs merged |
| 3. CDR sign-off | `signoff/buck-converter-5v/cdr` | All CDR checklist items ticked and PR merged |
| 4. Build, bring-up, and designer testing | `artifact/buck-converter-5v/<desc>` | Bring-up notes, measurements, and tweaks committed; all designer findings resolved |
| 5. TRR sign-off | `signoff/buck-converter-5v/trr` | Hardware built and brought up; ready to hand to IVV |
| 6. IVV | `artifact/buck-converter-5v/<desc>` | IVV tests complete externally; verification matrix updated with result links |
| 7. Final Release sign-off | `signoff/buck-converter-5v/release` | All IVV requirements evidenced; manufacturing authorised |
| 8. Production release | (release PR opened by CI) | Release PR merged, manufacturing outputs generated |

---

---

## Before you start — clone the repository

> **Do this once only.** If you have already cloned the repository, skip to Stage 1.

### GitHub Desktop

1. Open **GitHub Desktop**.
2. Click **File → Clone repository…** (or press `Ctrl+Shift+O` on Windows / `⇧⌘O` on Mac).
3. Select the **GitHub.com** tab.
4. Search for `hardware-features` and select `rockett90/hardware-features`.
5. Choose a **Local path** on your computer (e.g. `Documents/hardware-features`).
6. Expand **Advanced options** and tick **"Recurse submodules"** — this is essential to download the shared component library.
7. Click the blue **Clone** button and wait for the download to complete.

<!-- screenshot: Clone repository dialog, Recurse submodules ticked, Clone button highlighted -->

> ⚠️ **If you skip "Recurse submodules"**, KiCad will open project files with empty symbol boxes. You can fix this later by opening a terminal in the repository folder and running `git submodule update --init`.

### Alternative: command line

```bash
git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
cd hardware-features
```

---

## Stage 1 — Init PR (PDR baseline)

### What this stage achieves

The Init PR registers the feature in the repository and establishes the PDR baseline. You create a branch named `init/<feature>`, publish it, and CI automatically scaffolds all required directories and stub files onto your branch. When you open the PR, CI also generates the initial datasheet stub. You fill in the stubs, tick the PDR checklist, and merge.

---

### Step 1.1 — Create the init branch

#### GitHub Desktop

1. In GitHub Desktop, click the **Current branch** dropdown in the top centre of the window.
2. Click **New branch**.
3. In the **Name** field, type: `init/buck-converter-5v`
4. Make sure **From** shows `main`. If it does not, click the dropdown and select `main`.
5. Click the blue **Create branch** button.

<!-- screenshot: New branch dialog with "init/buck-converter-5v" typed and Create branch button highlighted -->

#### Alternative: command line

```bash
git checkout main
git pull
git checkout -b init/buck-converter-5v
```

---

### Step 1.2 — Publish the branch immediately

Publishing (pushing) the branch triggers the `Init branch setup` CI workflow, which scaffolds all required directories and stub files automatically. **Do this before making any manual file edits.**

#### GitHub Desktop

1. Click the blue **Publish branch** button in the top-right corner.

<!-- screenshot: GitHub Desktop toolbar showing the Publish branch button highlighted -->

#### Alternative: command line

```bash
git push -u origin init/buck-converter-5v
```

> ⏱️ **Wait for CI.** The `Init branch setup` workflow takes under 30 seconds. You can monitor it at **github.com → your repository → Actions tab**. Do not continue to the next step until it shows a green tick.

---

### Step 1.3 — Pull the scaffolded files

CI has committed the full directory scaffold directly to your branch. Pull these changes before editing anything.

#### GitHub Desktop

1. Click **Fetch origin** in the top-right corner.
2. If the button changes to **Pull origin**, click it to download the CI commit.

<!-- screenshot: GitHub Desktop toolbar showing Pull origin button -->

#### Alternative: command line

```bash
git pull
```

**What was committed by CI:**

- `features/buck-converter-5v/` — full directory structure with all required stubs
- `.github/commitlint.config.js` — updated to include `buck-converter-5v` as a valid commit scope
- `.github/release-please-config.json` — updated to register the new feature

Open any of the stub files in a text editor to see their placeholder content. You will fill these in next.

---

### Step 1.4 — Edit the stub files

Open each file and replace the placeholder content with real content for your feature:

| File | What to fill in |
|---|---|
| `features/buck-converter-5v/requirements/feature-requirements.yaml` | Real REQ-IDs and requirement statements |
| `features/buck-converter-5v/requirements/interface-requirements.yaml` | Interface definitions (voltage, current, connector type) |
| `features/buck-converter-5v/requirements/verification-matrix.md` | All REQ-IDs listed, each with a verification method |
| `features/buck-converter-5v/decisions/DDR-000-design-intent.md` | Problem statement, scope, and constraints |
| `features/buck-converter-5v/decisions/DDR-000-decisions.md` | At least one decision entry |
| `features/buck-converter-5v/README.md` | Feature description (1–3 paragraphs) |

> ⚠️ **Do not leave placeholder text in stub files.** Each checklist item in the PDR gate corresponds to content that must exist in a stub file. If a file still contains placeholder text the work is not done, and you will not be able to tick that item honestly. `gate-check` blocks merge while any item is unchecked.

---

### Step 1.5 — Commit and push

#### GitHub Desktop

1. Switch to GitHub Desktop. Changed files appear in the **Changes** panel on the left.
2. Confirm all the files you edited are ticked.
3. In the **Summary** box at the bottom-left, type a commit message. For example:
   ```
   feat(buck-converter-5v): fill in PDR stubs
   ```
4. Click the blue **Commit to `init/buck-converter-5v`** button.
5. Click **Push origin** in the top-right corner.

<!-- screenshot: GitHub Desktop Changes panel with commit summary filled in and Commit button highlighted -->

#### Alternative: command line

```bash
git add features/buck-converter-5v/
git commit -m "feat(buck-converter-5v): fill in PDR stubs"
git push
```

---

### Step 1.6 — Open the init PR

#### GitHub Desktop

1. Click **Branch** in the menu bar.
2. Click **Create pull request**. Your browser opens to the GitHub PR creation page.

<!-- screenshot: GitHub Desktop Branch menu with Create pull request highlighted -->

#### Alternative: command line

```bash
gh pr create --web
```

On the GitHub PR creation page:

1. Set the **title** to:
   ```
   feat(buck-converter-5v): initialise feature
   ```
2. Click the **dropdown arrow** on the green button (do **not** click the button itself yet).
3. Select **Create draft pull request**.
4. Click **Create draft pull request**.

<!-- screenshot: PR creation page showing the dropdown arrow and "Create draft pull request" option -->

---

### Step 1.7 — Wait for CI to run on the PR

After the PR is opened, three things happen automatically within about 30 seconds:

1. **PR template autofill** fills the correct checklist into the PR body. The body will appear blank for a moment, then fill in. Do not type anything in the body before this happens.

2. **Post gate checklist** posts a comment on the PR with orientation notes for the PDR gate.

3. **Generate datasheet** generates the initial datasheet stub and commits it directly to your `init/buck-converter-5v` branch. You will see a new commit appear on the branch from `github-actions[bot]`.

> ⏱️ **Watch the Actions tab.** Go to **github.com → Actions** and wait for the `Generate datasheet` workflow run to show a green tick. This confirms the stub has been committed.

---

### Step 1.8 — Pull the datasheet stub commit

CI has committed the datasheet stub to your branch. Pull before doing anything else.

#### GitHub Desktop

1. Click **Fetch origin**, then **Pull origin** when it appears.

#### Alternative: command line

```bash
git pull
```

**What was committed:**

- `features/buck-converter-5v/datasheet/buck-converter-5v-datasheet.md` — the datasheet stub in Markdown (always created)
- `features/buck-converter-5v/datasheet/buck-converter-5v-datasheet.pdf` — an initial PDF, if PDF tools were available in the CI runner; if not, only the Markdown file is created

> ℹ️ Do not edit `buck-converter-5v-datasheet.md` directly. It is regenerated from source files (`datasheet/specs.yaml`, `datasheet/application-notes.md`, `datasheet/errata.md`) when you run `/datasheet` during Stage 4 (build, bring-up, and designer testing). The source files are the ones to edit.

---

### Step 1.9 — Tick all PDR checklist items

On the GitHub PR page, read the checklist in the PR body carefully. Tick every item by clicking the `[ ]` boxes:

- Feature naming convention followed
- `feature-requirements.yaml` contains real REQ-IDs
- `interface-requirements.yaml` contains real interface definitions
- `verification-matrix.md` lists all REQ-IDs with verification methods
- `DDR-000-design-intent.md` captures the problem statement, scope, and constraints
- `DDR-000-decisions.md` contains at least one decision entry
- Feature scope is present in `.github/commitlint.config.js` (added automatically by CI — open the file and confirm `buck-converter-5v` appears in the `scopes` array)
- Feature package is present in `.github/release-please-config.json` (added automatically by CI)
- PDR date and owner name recorded

> **CI enforcement:** `gate-check` blocks merge while any `- [ ]` item remains unchecked in the PR body. You will see a red ✕ on the PR until all items are ticked.

---

### Step 1.10 — Mark ready for review and merge

1. On the PR page, click **"Ready for review"** once all checklist items are ticked and CI is green.
2. Request lead approval.
3. Once approved and all checks pass, click **Squash and merge**.
4. Confirm the merge commit title matches the PR title format.
5. Click **Confirm squash and merge**.

> **After merge:** No automated CI action is triggered by the init PR merge itself. The PDR baseline is now established. Move on to Stage 2.

---

## Stage 2 — Design work (PDR → CDR)

### What this stage achieves

Design artefacts are committed through one or more `artifact/` PRs — one PR per discrete artefact (schematic, PCB, calculations, BOM, etc.). This keeps the review history clean and makes it clear what changed at each review.

---

### Step 2.1 — Create an artifact branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type the branch name, e.g.: `artifact/buck-converter-5v/initial-schematic`
3. Confirm **From** shows `main`, then click **Create branch**.
4. Click **Publish branch** in the top-right corner immediately.

<!-- screenshot: New branch dialog with artifact branch name typed -->

#### Alternative: command line

```bash
git checkout main && git pull
git checkout -b artifact/buck-converter-5v/initial-schematic
git push -u origin artifact/buck-converter-5v/initial-schematic
```

---

### Step 2.2 — Open a draft PR immediately

Open a draft PR right after the first push so CI checks begin running as you work.

#### GitHub Desktop

1. Click **Branch → Create pull request**.
2. In your browser, set the title (e.g. `feat(buck-converter-5v): add initial schematic`).
3. Use the dropdown arrow on the green button to select **Create draft pull request**.
4. Click **Create draft pull request**.

#### Alternative: command line

```bash
gh pr create --draft --title "feat(buck-converter-5v): add initial schematic"
```

> **What CI does automatically:**
> - **PR template autofill** fills the artifact PR checklist into the PR body within seconds. Wait for it before typing.

---

### Step 2.3 — Design, commit, and push

Work in KiCad or a text editor. After each meaningful change:

#### GitHub Desktop

1. Switch to GitHub Desktop — changed files appear in the **Changes** panel.
2. Tick the files to include.
3. Type a commit message in the **Summary** box, e.g.:
   ```
   feat(buck-converter-5v): add power stage schematic
   ```
4. Click **Commit to `artifact/...`**.
5. Click **Push origin**.

#### Alternative: command line

```bash
git add features/buck-converter-5v/
git commit -m "feat(buck-converter-5v): add power stage schematic"
git push
```

**What CI does automatically on push:**

- If your PR contains changes to `.kicad_sch` or `.kicad_pcb` files, the **ERC/DRC** workflow runs automatically and posts a comment with any electrical rules check or design rules check violations. These results are **informational only** — they do not block merge.

---

### Step 2.4 — Use slash commands during review

Post these as comments on the PR. You must have write access to the repository.

| Command | What it does | When to use |
|---|---|---|
| `/render` | Exports schematic as SVG and PDF, posts a download link | After significant schematic changes — allows reviewers to read it without KiCad |
| `/kicad-diff` | Generates a four-column visual diff of schematic changes vs base branch | When you want to show exactly what changed |
| `/ai-review` | Runs an AI schematic analysis, posts CRITICAL and ADVISORY findings | Before requesting human review |
| `/erc` | Runs ERC on demand (informational, does not block merge) | On demand |
| `/drc` | Runs DRC on demand (informational, does not block merge) | On demand |

**What the dispatcher does:**

- Reacts 👀 on your comment when it receives the command.
- Reacts ✅ when the workflow is successfully dispatched.
- Reacts ❌ and posts a failure comment if dispatch fails.
- Posts a comment with available commands if you post a comment with no recognised command.

---

### Step 2.5 — AI review runs automatically on ready for review

When you click **"Ready for review"** on any non-draft PR (for non-`init/` branches), the **AI schematic review** workflow runs automatically. It posts a comment with any CRITICAL or ADVISORY findings.

Resolve all CRITICAL findings before requesting lead approval.

---

### Step 2.6 — Mark ready for review and merge

1. Post `/render` to generate fresh SVG renders for the review record.
2. Post `/ai-review` if you want a fresh AI review before the automatic one triggered by "Ready for review".
3. Click **"Ready for review"** on the PR.
4. Request lead approval.
5. Once approved and all checks pass, click **Squash and merge**.

Repeat Steps 2.1–2.6 for each subsequent artefact (PCB layout, calculations, BOM, bring-up notes, etc.).

---

## Stage 3 — CDR sign-off

### What this stage achieves

CDR (Critical Design Review) is a formal gate confirming the design is complete and fully reviewed. You create a `signoff/<feature>/cdr` branch, publish it, and CI automatically commits a gate evidence file. You open the PR, tick all CDR checklist items, get lead approval, and merge. **On merge, CI creates the `cdr/buck-converter-5v/approved` tag and commits `reviews/library.lock` to `main`.**

---

### Step 3.1 — Create the CDR branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type: `signoff/buck-converter-5v/cdr`
3. Confirm **From** shows `main`, then click **Create branch**.
4. Click **Publish branch** immediately.

<!-- screenshot: New branch dialog with signoff branch name -->

#### Alternative: command line

```bash
git checkout main && git pull
git checkout -b signoff/buck-converter-5v/cdr
git push -u origin signoff/buck-converter-5v/cdr
```

> ⏱️ **Wait for CI.** The `Signoff branch setup` workflow takes under 30 seconds. It commits `gate-evidence-cdr.md` to your branch automatically. Do not open the PR until this completes (green tick on the Actions tab).

---

### Step 3.2 — Pull the auto-committed gate evidence file

#### GitHub Desktop

1. Click **Fetch origin**, then **Pull origin** when it appears.

#### Alternative: command line

```bash
git pull
```

**What was committed by CI:**

- `features/buck-converter-5v/reviews/gate-evidence-cdr.md` — a pre-filled table recording the branch, date, previous gate, and commit SHA at the time the branch was created. Do not edit this file.

---

### Step 3.3 — Open the CDR PR

#### GitHub Desktop

1. Click **Branch → Create pull request**. Your browser opens.

#### Alternative: command line

```bash
gh pr create --web
```

Set the title:
```
chore(buck-converter-5v): CDR sign-off
```

> **Do not open this as a draft.** Open it as a regular PR straight away. The CDR checklist auto-fills into the PR body within seconds — refresh the page if it appears blank.

**What CI does automatically on opening:**

- **PR template autofill** fills the CDR sign-off checklist into the PR body.
- **Post gate checklist** posts a CDR orientation comment with instructions.
- **Gate check** starts checking the PR body for unticked items.

---

### Step 3.4 — Post `/render` for the review record

Post `/render` as a PR comment. The renders will be attached as a workflow artifact and linked in a PR comment. This gives reviewers a readable schematic without needing KiCad.

---

### Step 3.5 — Tick all CDR checklist items

Read each item in the PR body and tick it once satisfied. The CDR checklist includes:

- ERC clean (zero errors, zero warnings unless formally accepted and documented)
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

> **CI enforcement:** `gate-check` blocks merge while any `- [ ]` item remains unchecked in the PR body. You will see a failing check on the PR until all items are ticked.

---

### Step 3.6 — Merge

1. Request lead approval.
2. Once approved and all checks pass, click **Squash and merge** → **Confirm squash and merge**.

> **After merge, CI automatically:**
> - Creates the `cdr/buck-converter-5v/approved` gate tag
> - Creates `features/buck-converter-5v/reviews/library.lock` recording the library submodule commit and feature commit SHA at this gate, then commits it to `main`
>
> You do not need to do anything. These happen within about a minute of merge. You can confirm by checking the **Tags** page on GitHub (`Code → Tags`).

---

## Stage 4 — Build, bring-up, and designer testing

### What this stage achieves

The physical hardware is built and brought up. Bring-up notes, measurement data, and verification evidence are committed via `artifact/` PRs. The datasheet source files are filled in with actual measured values. Any defects found by the designer are raised as finding PRs and resolved. This stage ends when the hardware is stable and ready to be handed to the independent IVV team.

---

### Step 4.1 — Bring-up and test evidence PRs

Continue using `artifact/` branches, following the same process as Stage 2. Examples:

| Artefact | Branch | PR title |
|---|---|---|
| Bring-up notes | `artifact/buck-converter-5v/bring-up` | `test(buck-converter-5v): add bring-up checklist and notes` |
| Measurement data | `artifact/buck-converter-5v/efficiency-measurements` | `test(buck-converter-5v): add efficiency measurement data` |
| Thermal images | `artifact/buck-converter-5v/thermal-evidence` | `test(buck-converter-5v): add thermal characterisation evidence` |

Follow the same branch → push → draft PR → commit → merge process as Stage 2.

---

### Step 4.2 — Fill in the datasheet source files

The datasheet stub was generated when you opened the init PR in Stage 1. During this stage, fill in the source files with actual measured values. Edit these files and commit them via an `artifact/` PR:

| File | What to fill in |
|---|---|
| `features/buck-converter-5v/datasheet/specs.yaml` | Characterised min/nom/max values — actual achieved values from measurement, not requirements |
| `features/buck-converter-5v/datasheet/application-notes.md` | Typical application circuit, configuration guidance, layout recommendations |
| `features/buck-converter-5v/datasheet/errata.md` | Known issues against specific hardware revisions |

> ⚠️ Do not edit `buck-converter-5v-datasheet.md` directly — it is generated from the source files above. Edit the source files and then run `/datasheet` (Step 4.3) to regenerate.

---

### Step 4.3 — Regenerate the datasheet with `/datasheet`

Post `/datasheet` as a comment on an open artifact PR. CI regenerates the Markdown and PDF datasheet from the updated source files and commits the result directly to your branch.

> ℹ️ The `/datasheet` command requires write access to the repository. The dispatcher reacts 👀 when it receives the command and ✅ when dispatched successfully. After the workflow completes, pull the new commit.

---

### Step 4.4 — Finding PRs (if defects are found during designer testing)

If a defect is found:

1. Raise a GitHub Issue using the appropriate finding issue template.
2. The owner assigns the severity label: `finding: minor`, `finding: moderate`, or `finding: major`.
3. Create a finding branch and open a PR:

   **GitHub Desktop:** Click **Current branch** → **New branch** → type `finding/buck-converter-5v/42-output-voltage-low` → **Create branch** → **Publish branch**.

   **Alternative: command line:**
   ```bash
   git checkout main && git pull
   git checkout -b finding/buck-converter-5v/42-output-voltage-low
   git push -u origin finding/buck-converter-5v/42-output-voltage-low
   ```

4. Open the PR and include `Resolves #42` in the **body**. PR title:
   ```
   fix(buck-converter-5v): correct feedback resistor divider — finding #42
   ```

**Severity and gate re-entry:**

| Severity | Gate re-entry required |
|---|---|
| `finding: minor` | None, unless the owner decides otherwise |
| `finding: moderate` | Re-TRR (`signoff/buck-converter-5v/trr-1`) |
| `finding: major` | Re-CDR then re-TRR (`signoff/buck-converter-5v/cdr-1`, then `signoff/buck-converter-5v/trr-1`) |

---

## Stage 5 — TRR sign-off

### What this stage achieves

TRR (Test Readiness Review) confirms the hardware is built, brought up by the designer, and stable enough to hand to the independent IVV team. It does not confirm that IVV has passed — that happens in Stage 6. **On merge, CI creates the `trr/buck-converter-5v/approved` tag.**

---

### Step 5.1 — Create the TRR branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type: `signoff/buck-converter-5v/trr`
3. Confirm **From** shows `main` → **Create branch** → **Publish branch** immediately.

#### Alternative: command line

```bash
git checkout main && git pull
git checkout -b signoff/buck-converter-5v/trr
git push -u origin signoff/buck-converter-5v/trr
```

> ⏱️ Wait for the `Signoff branch setup` workflow to complete and commit `gate-evidence-trr.md` to your branch before opening the PR.

---

### Step 5.2 — Pull the gate evidence file and open the PR

#### GitHub Desktop

1. Click **Fetch origin** → **Pull origin**.
2. Click **Branch → Create pull request**.

#### Alternative: command line

```bash
git pull
gh pr create --web
```

PR title:
```
chore(buck-converter-5v): TRR sign-off
```

> **Do not open this as a draft.** The TRR checklist auto-fills within seconds — refresh if it appears blank.

**What CI does automatically on opening:**

- **PR template autofill** fills the TRR sign-off checklist into the PR body.
- **Post gate checklist** posts a TRR orientation comment.
- **Gate check** starts enforcing the checklist.

---

### Step 5.3 — Post `/render` for the review record

Post `/render` as a PR comment to generate fresh schematic renders for the record.

---

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
- `datasheet/specs.yaml` complete — no `[COMPLETE BEFORE TRR]` placeholders remaining
- Datasheet Markdown and PDF committed and reviewed by owner
- All CRITICAL AI review findings resolved
- TRR date and owner name recorded

---

### Step 5.5 — Merge

1. Request lead approval.
2. Once approved and all checks pass, click **Squash and merge** → **Confirm squash and merge**.

> **After merge, CI creates the `trr/buck-converter-5v/approved` tag.** This tag is force-pushed, so if you run a re-TRR the tag will be updated to point to the new merge commit. Confirm the tag exists under **Code → Tags** on GitHub.

---

## Stage 6 — IVV

### What this stage achieves

The independent IVV (Integration, Verification and Validation) team runs their tests using their own test systems and tooling. Test evidence and results are stored in the IVV team's own systems — not in this repository. The only update made here is to `requirements/verification-matrix.md`, which is updated with links to the IVV test results so there is a traceable pointer from each REQ-ID to its evidence.

This stage uses the same `artifact/` PR process as Stage 2 and Stage 4. There is no dedicated branch type or gate PR for IVV itself.

---

### Step 6.1 — IVV team runs tests externally

The IVV team works independently using their own test equipment and management systems. You do not need to create any branches or PRs during this phase — wait for IVV to complete their testing.

If IVV finds defects, they raise GitHub Issues using the IVV Finding issue template. Handle these the same way as designer findings in Stage 4: create a `finding/` branch, fix the defect, and merge. Severity determines whether gate re-entry is required:

| Severity | Gate re-entry |
|---|---|
| `finding: minor` | None, unless the owner decides otherwise |
| `finding: moderate` | Re-TRR (`signoff/buck-converter-5v/trr-1`) |
| `finding: major` | Re-CDR then re-TRR |

---

### Step 6.2 — Update the verification matrix with IVV result links

Once IVV is complete and all requirements are evidenced, update `requirements/verification-matrix.md` with links to the IVV test results. Each REQ-ID should reference where its verification evidence lives in the IVV system.

Create an `artifact/` PR for this update:

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type: `artifact/buck-converter-5v/ivv-evidence`
3. Confirm **From** shows `main` → **Create branch** → **Publish branch**.
4. Edit `features/buck-converter-5v/requirements/verification-matrix.md` — add result links or references against each REQ-ID.
5. Commit and push. Open a PR titled:
   ```
   docs(buck-converter-5v): update verification matrix with IVV result references
   ```
6. Get lead review and merge.

#### Alternative: command line

```bash
git checkout main && git pull
git checkout -b artifact/buck-converter-5v/ivv-evidence
git push -u origin artifact/buck-converter-5v/ivv-evidence
# Edit verification-matrix.md, then:
git add features/buck-converter-5v/requirements/verification-matrix.md
git commit -m "docs(buck-converter-5v): update verification matrix with IVV result references"
git push
```

Once this PR is merged, move on to Stage 7 — Final Release sign-off.

---

## Stage 7 — Final Release sign-off

### What this stage achieves

This gate formally authorises the manufacturing outputs for production. **On merge, CI:**
- Creates the `release/buck-converter-5v/approved` tag
- Collects all release documents from `features/buck-converter-5v/`, converts them to PDF
- Creates a **GitHub Release** at the tag with all release documents attached as PDF assets

---

### Step 7.1 — Verify pre-conditions

Before raising this PR, confirm that both gate tags exist. On GitHub, go to **Code → Tags** and check for:

- `cdr/buck-converter-5v/approved`
- `trr/buck-converter-5v/approved`

#### Alternative: command line

```bash
git fetch --tags
git tag -l "*/buck-converter-5v/*"
```

Also confirm all `finding: major` and `finding: moderate` IVV findings are resolved or formally deferred with owner sign-off.

---

### Step 7.2 — Create the release sign-off branch

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Type: `signoff/buck-converter-5v/release`
3. Confirm **From** shows `main` → **Create branch** → **Publish branch** immediately.

#### Alternative: command line

```bash
git checkout main && git pull
git checkout -b signoff/buck-converter-5v/release
git push -u origin signoff/buck-converter-5v/release
```

> ⏱️ Wait for `Signoff branch setup` to complete and commit `gate-evidence-release.md` before opening the PR.

---

### Step 7.3 — Pull the gate evidence file and open the PR

#### GitHub Desktop

1. Click **Fetch origin** → **Pull origin**.
2. Click **Branch → Create pull request**.

#### Alternative: command line

```bash
git pull
gh pr create --web
```

PR title:
```
chore(buck-converter-5v): final release sign-off
```

> **Do not open this as a draft.** The Release checklist auto-fills within seconds.

---

### Step 7.4 — Tick all Release checklist items

- `cdr/buck-converter-5v/approved` tag present
- `trr/buck-converter-5v/approved` tag present
- `features/buck-converter-5v/reviews/library.lock` committed to `main`
- ERC report clean
- All CDR-gate checklist items remain satisfied
- All TRR-gate checklist items remain satisfied
- All `finding: major` and `finding: moderate` findings resolved or formally deferred
- Manufacturing outputs generated by CI without errors
- Gerbers visually verified against PCB layout
- DRC confirmed clean
- BOM has no TBDs — all MPNs confirmed and available
- CPL file verified against placement drawing
- CHANGELOG reviewed and accurate
- Version number correct
- Release date and owner name recorded

---

### Step 7.5 — Merge

1. Request lead approval.
2. Once approved and all checks pass, click **Squash and merge** → **Confirm squash and merge**.

> **After merge, CI automatically:**
> 1. Creates the `release/buck-converter-5v/approved` tag
> 2. Installs PDF conversion tools (Inkscape, img2pdf, Ghostscript)
> 3. Collects all files from `features/buck-converter-5v/` — PDFs are attached as-is, SVGs are converted to PDF, images (PNG/JPG) are converted to PDF
> 4. Creates a **GitHub Release** at the `release/buck-converter-5v/approved` tag with all collected PDFs attached
>
> The GitHub Release will appear under **Releases** on the repository home page within a few minutes of merge.

---

## Stage 8 — Production release

### What this stage achieves

Release-please automatically maintains a **Release PR** that tracks all conventional commits merged to `main`. Merging this PR creates the production version tag (e.g. `buck-converter-5v-v1.0.0`) and triggers the **Manufacturing Release** CI workflow, which generates Gerbers, BOM, CPL, and all other manufacturing outputs.

---

### Step 8.1 — Find the release-please Release PR

1. Go to the **Pull requests** tab on GitHub.
2. Look for a PR titled something like `chore(buck-converter-5v): release 1.0.0`. It will have the label `autorelease: pending`.

This PR is created and updated automatically — you do not create it. It accumulates changes from every conventional commit merged since the last release.

---

### Step 8.2 — Merge the Release PR

1. Open the release-please PR.
2. Review the automatically generated CHANGELOG in the PR body.
3. Click **Merge pull request** — **not** squash. Release-please requires a true merge commit to record which commits were included in the release. Squashing would cause it to re-open the same PR on the next push.
4. Click **Confirm merge**.

> **Never close this PR manually.** Closing it prevents the production tag from being created and will cause release-please to open a new PR.

---

### Step 8.3 — What happens on merge

**CI runs automatically:**

1. **Release-please** creates the production tag `buck-converter-5v-v1.0.0` and updates the GitHub Release with the CHANGELOG.

2. The **Manufacturing Release** workflow (`hw-release.yml`) is triggered by the production tag. It:
   - Verifies that the `release/buck-converter-5v/approved` gate tag exists — if it is absent, the workflow fails immediately with a clear error message
   - Checks out the repository with all submodules
   - Runs KiBot to generate Gerbers, drill files, assembly drawings, BOM, CPL, and schematic PDF
   - Attaches all manufacturing outputs as a ZIP to the GitHub Release

> 💡 **Check the Actions tab** for the `Manufacturing Release` workflow run triggered by the production tag. Any ⛔ in the step summary means one or more outputs failed to generate. Do not send files to the manufacturer until all steps show ✅.

---

## Tag summary

After completing all eight stages, these tags exist in the repository:

| Tag | Created by | Meaning |
|---|---|---|
| `cdr/buck-converter-5v/approved` | CDR sign-off PR merged | CDR gate passed |
| `trr/buck-converter-5v/approved` | TRR sign-off PR merged | TRR gate passed |
| `release/buck-converter-5v/approved` | Final Release sign-off PR merged | Manufacturing authorised |
| `buck-converter-5v-v1.0.0` | Release PR merged | Production release |

---

## Quick reference

**Branch names (validated by CI):**
```
init/buck-converter-5v
artifact/buck-converter-5v/<desc>
signoff/buck-converter-5v/cdr
signoff/buck-converter-5v/trr
signoff/buck-converter-5v/release
finding/buck-converter-5v/<issue-number>-<desc>
```

> **Signoff branches** (`signoff/**`) are scaffolded automatically on first push — same as `init/**` branches. Publish the branch immediately and wait for `Signoff branch setup` to commit the gate evidence file before opening the PR.

**PR title format:**
```
type(buck-converter-5v): description
```
Types: `feat`, `fix`, `docs`, `test`, `chore`

**Slash commands (post as a PR comment — write access required):**
```
/render         — export schematic as SVG and PDF
/kicad-diff     — four-column visual diff vs base branch
/ai-review      — AI schematic review (CRITICAL / ADVISORY findings)
/erc            — Electrical Rules Check (informational, does not block merge)
/drc            — Design Rules Check (informational, does not block merge)
/datasheet      — regenerate datasheet from specs.yaml and application-notes.md
```

**CI that runs automatically (no command needed):**

| Event | What CI does |
|---|---|
| Push to `init/**` branch | Scaffolds feature directory, stubs, and config files; commits back to branch |
| Push to `signoff/**` branch | Commits gate evidence file to branch |
| Any PR opened | Fills PR body with the correct template for the branch type |
| Init PR opened | Generates datasheet stub and commits it to the init branch |
| Artifact PR with `.kicad_sch` or `.kicad_pcb` changes | ERC/DRC runs and posts a comment (informational) |
| PR marked Ready for Review (non-`init/`, non-draft) | AI schematic review runs and posts findings |
| CDR sign-off PR merged | Creates `cdr/.../approved` tag; commits `library.lock` to `main` |
| TRR sign-off PR merged | Creates (or updates) `trr/.../approved` tag |
| Release sign-off PR merged | Creates `release/.../approved` tag; creates GitHub Release with PDF document pack |
| Release PR merged | Creates production tag; runs KiBot; attaches manufacturing outputs to GitHub Release |

---

## See also

- [docs/tool-setup.md](../tool-setup.md) — installing GitHub Desktop and GitHub CLI
- [docs/how-to/init-feature.md](init-feature.md) — detailed steps for the Init PR
- [docs/how-to/design-workflow.md](design-workflow.md) — day-to-day workflow for artifact PRs
- [docs/how-to/cdr-signoff.md](cdr-signoff.md) — detailed steps for CDR sign-off
- [docs/how-to/trr-signoff.md](trr-signoff.md) — detailed steps for TRR sign-off
- [docs/how-to/release-signoff.md](release-signoff.md) — detailed steps for Final Release sign-off
- [docs/how-to/datasheet.md](datasheet.md) — how to generate the feature datasheet
