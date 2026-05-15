# Contributing

## 1. First-time setup

**KiCad version:** See [docs/versions.md](docs/versions.md) — do not upgrade individually, coordinate with the lead.

**Clone with GitHub Desktop:**
File → Clone repository → GitHub.com tab → select `rockett90/hardware-features` → expand Advanced options → tick **"Recurse submodules"** (essential — clones the component library at the same time) → Clone. See [docs/setup/tool-setup.md](docs/setup/tool-setup.md) for a full step-by-step guide.

**Clone with Terminal:**
```bash
git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
```

**KiCad library setup:**
Preferences → Manage Symbol Libraries → add `library/symbols/` using `${KIPRJMOD}` relative paths.

---

## 2. Repository structure

| Path | Contents |
|---|---|
| `features/` | One directory per feature |
| `library/` | Shared KiCad component library (git submodule) |
| `config/kibot/` | KiBot render and BOM config |
| `checklists/` | Gate and review checklists |
| `scripts/ci/` | CI scripts (init-feature, validators) |
| `templates/` | KiCad project templates |
| `docs/` | Guides and reference documentation |
| `.github/` | Workflows, templates, guidelines, agent instructions |

---

## 3. Branch naming

| Type | Pattern | When to use |
|---|---|---|
| Init | `init/<feature>` | PDR baseline. Contains requirements, DDR-000, and feature scope registration. Triggers scaffold on merge. |
| Artifact | `artifact/<feature>/<desc>` | Any discrete design artefact during PDR→CDR or CDR→TRR: schematics, PCB, calculations, simulations, analysis, BOM, bring-up evidence. |
| Artifact with Jira | `artifact/<feature>/<desc-HW-123>` | Same as above with an optional Jira ticket key appended. |
| Finding | `finding/<feature>/<N>-<desc>` | IVV finding fix. N is the GitHub Issue number. Triggers automatic label updates on the linked issue. |
| CDR sign-off | `signoff/<feature>/cdr` | CDR gate sign-off. Created by the **Actions → Gate Sign-Off** workflow, which opens the PR with the CDR checklist already filled in. |
| TRR sign-off | `signoff/<feature>/trr` | TRR gate sign-off. Created by the **Actions → Gate Sign-Off** workflow, which checks the CDR tag before opening the PR. |
| Release sign-off | `signoff/<feature>/release` | Final Release gate. Created by the **Actions → Gate Sign-Off** workflow, which opens the PR with the release checklist already filled in. Must be raised and merged before manufacturing outputs are considered authorised for production. |
| Library | `library/<desc>` | Changes to the hardware-library repository (raised in that repo, not here). |
| Chore | `chore/<desc>` | Repository housekeeping: CI changes, guideline updates, template changes, submodule pointer updates. Uses `library` scope in PR title by convention. |

> **PDR** is recorded via the `init/<feature>` PR — there is no separate `signoff/*/pdr` branch. The init PR IS the PDR baseline.
>
> **Final Release** is recorded via the `signoff/<feature>/release` PR. This must be merged before treating manufacturing outputs as authorised for production.

CI validates every PR branch. A non-matching branch fails "Validate branch name" and cannot merge until corrected.

> **Sign-off branches are workflow-managed.** Do not create or rename `signoff/*` branches manually — use **Actions → Gate Sign-Off** and let CI create the branch and PR for you.

> **Where does the changelog live?** release-please automatically creates and maintains `features/<feature-name>/CHANGELOG.md` when the first release PR for that feature is raised and merged. Engineers do not write the changelog manually — it is generated from PR titles.

---

## 4. PR title format

Format: `type(scope): description`

Follows the [Conventional Commits](https://www.conventionalcommits.org/) specification. The PR title is validated by CI — individual commit messages are freeform.

**Valid types:**

| Type | Hardware usage |
|---|---|
| `feat` | New design capability or artefact (new schematic, new PCB, new analysis document) |
| `fix` | Correction to an existing artefact or IVV finding resolution |
| `docs` | Documentation, analysis documents, DDRs, calculations |
| `test` | Simulations, bring-up scripts, verification evidence |
| `chore` | Gate sign-offs, CI configuration, template updates, submodule pointer updates |

Scope must be a feature name or `library`. Jira key never in the title.

**`library` scope convention:** Repository-level housekeeping PRs that do not belong to a specific feature use `library` as the scope by convention. This includes CI changes, template updates, submodule pointer bumps, and guideline updates.

**Good examples:**

```
feat(buck-converter-5v): add initial schematic
fix(buck-converter-5v): correct feedback resistor values — IVV finding #42
docs(buck-converter-5v): add DDR-003 thermal analysis
chore(library): upgrade KiCad to 10.0.2
feat(motor-driver): add PCB layout for H-bridge
```

**Bad examples and why:**

```
updated schematic                      ← missing type and scope
feat: add schematic                    ← missing scope
feat(buck-converter-5v): HW-123        ← Jira key in title — put it in the branch name instead
fix(buck-converter-5v): fixed stuff    ← description is not meaningful for the changelog
FEAT(buck-converter-5v): add layout    ← type must be lowercase
```

---

## 5. Jira (optional)

Add a Jira key to the branch name and PR description if you have a ticket. Leave blank if not. Both pass CI.

---

## 6. Draft PR workflow

Open a Draft PR immediately after your first push:
GitHub → "Compare & pull request" → dropdown arrow on the green button → "Create draft pull request".

When ready for review, click **"Ready for review"** at the bottom of the PR page (below the merge box) — this triggers AI review automatically.

Address all ⚠️ CRITICAL findings before requesting human review.

---

## 6a. What to do when CI fails

CI runs automatically on every push and PR update. Most failures are quick to fix. Here are the most common ones:

---

**Branch name check fails (`Validate branch name`)**

The branch name does not match the required format.

Fix:
- For `signoff/*` PRs, do **not** rename the branch manually. Close the malformed PR if one was opened, delete the malformed branch if needed, then go to **Actions → Gate Sign-Off → Run workflow** and create a fresh `cdr`, `trr`, or `release` PR from the workflow form.
- For all other branch types, rename your branch to match the convention in section 3, then push the corrected branch:

```bash
git branch -m old-branch-name artifact/my-feature/correct-name
git push origin -u artifact/my-feature/correct-name
git push origin --delete old-branch-name
```

Open a new PR from the corrected branch if needed.

---

**PR title check fails (`Validate PR title`)**

The PR title does not follow `type(scope): description` format, or the scope is not registered.

Fix: Edit the PR title directly on GitHub — click the pencil icon next to the title on the PR page. You do not need to push any new commits; the check re-runs automatically when the title changes.

Common mistakes:
- Missing scope: `feat: add schematic` → should be `feat(buck-converter-5v): add schematic`
- Wrong type casing: `FEAT` → must be lowercase `feat`
- Scope not registered: the feature name must be in `.github/commitlint.config.js` — this is added automatically when the `init/` branch is pushed. If you are on an `artifact/` branch and the scope is missing, the init PR may not have merged yet.

---

**Gate check fails (`Gate Check`)**

The gate PR has unchecked items in the PR description checklist.

Fix: Open the PR on GitHub, scroll to the PR description, and tick each checklist item (`- [ ]` → `- [x]`). You can tick items directly in the GitHub web editor by clicking the checkbox. The check re-runs automatically when the PR description is updated.

If an item does not apply, tick it and add a comment or note below the checklist explaining why.

---

**ERC / DRC shows violations (informational only)**

ERC and DRC results are **informational** — they do not block merge. A violation does not automatically prevent you from merging.

What to do:
- Review the violations in the PR comment posted by CI.
- Fix genuine errors (unconnected pins, missing power flags, DRC clearance violations).
- Accept known/intentional violations by adding them to the KiCad ERC/DRC suppression list inside KiCad, then push again.
- ERC evidence is reviewed formally at CDR; DRC evidence at TRR.

---

**Release-please config check fails (`Validate release-please config`)**

This only fires on `init/` PRs. It means the feature was not registered in `.github/release-please-config.json`.

In normal flow, `init-branch-setup.yml` adds this automatically when the branch is first pushed. If the check fails:
1. Pull the latest commits from your branch (`git pull`) — the scaffold commit may not have landed yet.
2. If the scaffold commit is present and the check still fails, check whether `.github/release-please-config.json` contains your feature name under `packages`.
3. If missing, the scaffold workflow may have failed — check the Actions tab for errors on the `Init branch setup` run.

---

### Slash commands

Post a slash command as a PR comment to trigger CI actions. Commands require **write access** to the repository.

| Command | Action |
|---|---|
| `/render` | Export schematic as SVG — readable without KiCad |
| `/ai-review` | Run AI schematic review |
| `/kicad-diff` | Generate visual diff of schematic (and PCB) changes vs base branch |
| `/datasheet` | Regenerate the feature datasheet from `datasheet/specs.yaml` and `datasheet/application-notes.md` |
| `/erc` | Run ERC (Electrical Rules Check) — informational, does not block merge |
| `/drc` | Run DRC (Design Rules Check) — informational, does not block merge |
| `/emc-check` | *(coming soon)* |
| `/spice` | *(coming soon)* |
| `/bom-check` | *(coming soon)* |
| `/fab-check` | *(coming soon)* |

The dispatcher reacts with 👀 immediately on receipt. On success it reacts with ✅; on failure with ❌.

---

## 7. One-file-at-a-time rule

Check open PRs before starting work. If another PR is open for a KiCad file you need, speak to the lead first.

**Never manually resolve conflicts in `.kicad_sch` or `.kicad_pcb` files — they will be silently corrupted.**

---

## 8. Pushing

Push at the end of every working session.

---

## 9. Library changes

Raise a PR in the library repo first. After merge, open a `chore/` PR in the features repo to advance the submodule pointer:

```bash
cd library && git pull && cd .. && git add library
```

Then commit and push.

---

## 10. Template changes

Raise a `chore/` PR. Lead approval required.

---

## 11. Raising an init PR

Your init PR must contain the following files inside `features/<name>/`:

| File | Requirement |
|---|---|
| `decisions/DDR-000-design-intent.md` | Real content — not placeholder |
| `decisions/DDR-000-decisions.md` | At least one decision entry — not placeholder |
| `requirements/feature-requirements.yaml` | Real REQ-IDs |
| `requirements/interface-requirements.yaml` | Real interface values |
| `requirements/verification-matrix.md` | REQ-IDs listed |

CI automatically patches both `.github/commitlint.config.js` and `.github/release-please-config.json` when the `init/<feature>` branch is first pushed. After your first push, run `git pull` to get the scaffolded files, which include these updates. The entry added to `release-please-config.json` looks like:

```json
"buck-converter-5v": {
  "release-type": "simple",
  "package-name": "buck-converter-5v",
  "changelog-path": "features/buck-converter-5v/CHANGELOG.md",
  "bump-minor-pre-major": true
}
```

> The `validate-release-please-config` CI check will fail if the feature is not registered. This should not happen in normal flow — if it does, pull the branch and check whether the scaffold commit landed.

CI scaffolds all remaining directories when the `init/<feature>` branch is first pushed.

---

## 12. IVV findings

> **Prerequisites:** The following labels must exist in the repository before the first finding PR is opened: `finding: minor`, `finding: moderate`, `finding: major`, `finding: in-progress`, `finding: resolved`. A lead should verify these labels exist before the first IVV cycle begins. If the labels are missing, CI will fail silently when it tries to apply them. Labels can be created at: **github.com → Issues → Labels → New label**.

The full IVV finding loop:

1. A finding is raised as a GitHub Issue using the IVV Finding issue template (by the IVV team or by the engineering team). The template is at `.github/ISSUE_TEMPLATE/ivv-finding.md`.
2. The lead reviews and confirms the severity label: `finding: minor`, `finding: moderate`, or `finding: major`.
3. An engineer creates a `finding/<feature>/<N>-<desc>` branch where `N` is the GitHub Issue number.
4. A PR is raised with `Resolves #N` in the **description body** (not the title).
5. CI automatically adds `finding: in-progress` to the issue and posts a link comment when the PR is opened, and `finding: resolved` plus the merge commit SHA when the PR merges.
6. Severity determines gate re-entry:
   - `finding: minor` — no gate re-entry unless the lead requires it
   - `finding: moderate` — re-TRR required (`signoff/<feature>/trr-N` branch)
   - `finding: major` — re-CDR then re-TRR required

---

## 13. release-please

Never close a Release PR manually. Let release-please manage it.

---

## 14. KiCad version

See [docs/versions.md](docs/versions.md). Do not upgrade individually — coordinate with the lead.

---

## 15. Bench scripts import path

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'bench'))
```

`parents[4]` navigates from the script file up through `scripts/`, `bring-up/`, `<feature>/`, `features/`, to the repository root where `bench/` lives. Using `Path.resolve()` makes this independent of the working directory the script is run from.

---

## 16. Review checklists

See `checklists/review/` for the full set of review checklists. Use during review. Not auto-posted.
