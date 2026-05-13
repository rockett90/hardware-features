# How to work on a hardware feature

> Day-to-day workflow for making schematic and PCB changes on an existing feature.

---

## Prerequisites

- The feature must already exist in `features/` — if it does not, see [init-feature.md](init-feature.md) first.
- KiCad 10.0.1 installed.
- Repository cloned with submodules.

---

## Branch naming

```
artifact/<feature>/<description>
artifact/<feature>/<description-HW-123>    ← include ticket number if you have one
```

Examples:
```
artifact/buck-converter-5v/add-output-filter
artifact/buck-converter-5v/fix-input-cap-HW-42
```

---

## Workflow

### 1. Create your branch and push immediately

```bash
git checkout -b artifact/<feature>/<description>
git push -u origin artifact/<feature>/<description>
```

### 2. Open a draft PR immediately

Open a draft PR after your first push. This starts CI running and makes your work visible to the team.

GitHub → "Compare & pull request" → dropdown arrow on the green button → **"Create draft pull request"**.

PR title format:
```
feat(<feature>): description of change
```

### 3. Work on the design in KiCad

Open `features/<feature>/kicad/<feature>.kicad_pro` in KiCad 10.0.1.

Push at the end of every working session.

---

## Slash commands during design

Post these as PR comments at any time to trigger CI actions. You must have **write access** to use them.

| Command | When to use |
|---|---|
| `/render` | Export schematic as SVG — do this after significant schematic changes so reviewers can see the design without opening KiCad |
| `/kicad-diff` | Generate a four-column visual diff showing exactly what changed vs the base branch |
| `/ai-review` | Run AI analysis of your schematic changes — check for issues before requesting human review |
| `/erc` | Run Electrical Rules Check — informational, does not block merge |
| `/drc` | Run Design Rules Check — informational, does not block merge |

> 💡 **One command per comment:** The dispatcher processes only the first slash command in each comment. Post each command as a separate comment if you want to run multiple.
>
> 💡 Tip: Run `/render` before marking your PR ready for review. Reviewers can then see schematic images directly in the PR without installing KiCad.

---

## Ready for review

1. Run `/render` to generate up-to-date schematic SVGs.
2. Run `/ai-review` and address all ⚠️ CRITICAL findings.
3. Click **"Ready for review"** on the PR — this automatically triggers AI review.
4. Request reviewers.

---

## The one-feature rule

> ⚠️ Warning: Never open a PR that touches KiCad files (`.kicad_sch`, `.kicad_pcb`, `.kicad_pro`) in more than one feature directory. CI will reject it.

Check that no other open PR is modifying the same KiCad files before starting work. If there is a conflict, coordinate with the author of the other PR — **never manually resolve conflicts in `.kicad_sch` or `.kicad_pcb` files**. KiCad files will be silently corrupted by a standard git merge.

---

## Merging

Once CI passes and you have the required approvals, merge using "Squash and merge" or "Merge commit" — do not use "Rebase and merge" on KiCad file changes.
