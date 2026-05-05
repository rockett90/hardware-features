# Contributing

## 1. First-time setup

**KiCad version:** 10.0.1 — do not upgrade individually, coordinate with the lead.

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

| Type | Pattern |
|---|---|
| Concept | `concept/<feature>` |
| Init | `init/<feature>` |
| Artifact | `artifact/<feature>/<desc>` |
| Artifact with Jira | `artifact/<feature>/<desc-HW-123>` |
| Finding | `finding/<feature>/<N>-<desc>` |
| CDR sign-off | `signoff/<feature>/cdr` |
| TRR sign-off | `signoff/<feature>/trr` |
| Re-TRR | `signoff/<feature>/trr-N` |
| Library | `library/<desc>` |
| Chore | `chore/<desc>` |

CI validates every PR branch. A non-matching branch fails "Validate branch name" and cannot merge until corrected.

---

## 4. PR title format

Conventional Commits on the title only. Commits are freeform.

Format: `type(scope): description`

Valid types: `feat`, `fix`, `docs`, `test`, `chore`

Scope must be a feature name or `library`. Jira key never in the title.

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

Branch as `finding/<feature>/<N>-<desc>` where `N` is the GitHub issue number.

Include `Resolves #N` in the PR description body.

Labels are applied automatically by CI.

---

## 13. release-please

Never close a Release PR manually. Let release-please manage it.

---

## 14. KiCad version

**10.0.1.** Do not upgrade individually — coordinate with the lead.

---

## 15. Bench scripts import path

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../bench'))
```

---

## 16. Review checklists

See `checklists/review/` for schematic, PCB, BOM, and general review checklists. Use during review. Not auto-posted.
