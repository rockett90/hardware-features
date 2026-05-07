# Contributing

## 1. First-time setup

**KiCad version:** See [docs/versions.md](docs/versions.md) — do not upgrade individually, coordinate with the lead.

**Clone with SourceTree:**
File → New → Clone from URL → `https://github.com/rockett90/hardware-features.git` → tick **"Recurse submodules"** (essential — clones the component library at the same time) → Clone.

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
| Concept | `concept/<feature>` | Optional pre-PDR exploration. Not a controlled baseline. Outputs must be re-committed through controlled PRs before use as review evidence. |
| Init | `init/<feature>` | PDR baseline. Contains requirements, DDR-000, and feature scope registration. Triggers scaffold on merge. |
| Artifact | `artifact/<feature>/<desc>` | Any discrete design artefact during PDR→CDR or CDR→TRR: schematics, PCB, calculations, simulations, analysis, BOM, bring-up evidence. |
| Artifact with Jira | `artifact/<feature>/<desc-HW-123>` | Same as above with an optional Jira ticket key appended. |
| Finding | `finding/<feature>/<N>-<desc>` | IVV finding fix. N is the GitHub Issue number. Triggers automatic label updates on the linked issue. |
| CDR sign-off | `signoff/<feature>/cdr` | CDR gate sign-off. Document-only PR. Triggers CDR checklist posting and gate tag creation. |
| Re-CDR | `signoff/<feature>/cdr-N` | Re-CDR after a `finding: major` severity forces the design back to CDR. N starts at 1. Triggers the same CDR gate automation as the original CDR sign-off. |
| TRR sign-off | `signoff/<feature>/trr` | TRR gate sign-off. Document-only PR. Triggers TRR checklist, rc tag, and pre-release creation. |
| Re-TRR | `signoff/<feature>/trr-N` | Re-TRR after finding resolution. Triggers visual diff versus previous rc tag. |
| Release sign-off | `signoff/<feature>/release` | Final Release gate. Document-only PR. Triggers release gate checklist enforcement and `release/<feature>/approved` tag creation. Must be raised and merged before manufacturing outputs are considered authorised for production. |
| Library | `library/<desc>` | Changes to the hardware-library repository (raised in that repo, not here). |
| Chore | `chore/<desc>` | Repository housekeeping: CI changes, guideline updates, template changes, submodule pointer updates. Uses `library` scope in PR title by convention. |

> **PDR** is recorded via the `init/<feature>` PR — there is no separate `signoff/*/pdr` branch. The init PR IS the PDR baseline.
>
> **Final Release** is recorded via the `signoff/<feature>/release` PR. This must be merged before treating manufacturing outputs as authorised for production.

CI validates every PR branch. A non-matching branch fails "Validate branch name" and cannot merge until corrected.

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

Comment `/render` on the PR at any time to export schematic SVGs. Comment `/kicad-diff` to generate a visual diff of all changes vs the base branch.

When ready for review, click **"Ready for review"** at the bottom of the PR page (below the merge box) — this triggers AI review automatically.

Address all ⚠️ CRITICAL findings before requesting human review.

---

## 6a. Slash commands

Post a slash command as a PR comment to trigger CI actions. Commands require **write access** to the repository.

| Command | Action |
|---|---|
| `/render` | Export schematic as SVG — readable without KiCad |
| `/ai-review` | Run AI schematic review |
| `/kicad-diff` | Generate visual diff of schematic (and PCB) changes vs base branch |
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
| `decisions/DDR-000-feature-overview.md` | Real content — not placeholder |
| `requirements/feature-requirements.yaml` | Real REQ-IDs |
| `requirements/interface-requirements.yaml` | Real interface values |
| `requirements/verification-matrix.md` | REQ-IDs listed |

Your init PR must also update:
- `.github/commitlint.config.js` — add the new scope to `scope-enum`
- `.github/release-please-config.json` — add the package entry

CI scaffolds all remaining directories automatically on merge.

---

## 12. IVV findings

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

Labels are applied automatically by CI. **Prerequisite:** the labels `finding: in-progress` and `finding: resolved` must exist in the repository before the automation can apply them. Create them once via GitHub → Issues → Labels → New label.

---

## 13. release-please

Never close a Release PR manually. Let release-please manage it.

---

## 14. KiCad version

See [docs/versions.md](docs/versions.md). Do not upgrade individually — coordinate with the lead.

---

## 15. Bench scripts import path

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../bench'))
```

---

## 16. Review checklists

See `checklists/review/` for schematic, PCB, BOM, and general review checklists. Use during review. Not auto-posted.
