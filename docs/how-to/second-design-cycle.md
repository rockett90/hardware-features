# How to run a second design cycle

Use this guide when a feature has completed its first full release and a design change requires going back through PDR/CDR/TRR and re-releasing.

---

## Branch naming

Second-cycle branches use the `-rN` suffix where `N` is the cycle number (starting at 2):

| Gate | First cycle | Second cycle | Third cycle |
|---|---|---|---|
| PDR | `init/<feature>` | Not repeated — use `artifact/<feature>/` for design changes | — |
| CDR | `signoff/<feature>/cdr` | `signoff/<feature>/cdr-r2` | `signoff/<feature>/cdr-r3` |
| TRR | `signoff/<feature>/trr` | `signoff/<feature>/trr-r2` | `signoff/<feature>/trr-r3` |
| Release | `signoff/<feature>/release` | `signoff/<feature>/release-r2` | `signoff/<feature>/release-r3` |

Re-attempts within the same cycle (e.g. re-TRR after a finding) continue to use `-2`, `-3`:
- `signoff/<feature>/trr-2` — second attempt at TRR within cycle 1
- `signoff/<feature>/trr-r2-2` — second attempt at TRR within cycle 2

---

## Tags created

| Event | Tag |
|---|---|
| CDR cycle 1 | `cdr/<feature>/approved` (floating — always points to latest CDR) |
| CDR cycle 2 | `cdr/<feature>/r2/approved` (permanent) + floating updated |
| TRR cycle 1 | `trr/<feature>/approved` (floating) |
| TRR cycle 2 | `trr/<feature>/r2/approved` (permanent) + floating updated |
| Release cycle 1 | `release/<feature>/approved` (floating) |
| Release cycle 2 | `release/<feature>/r2/approved` (permanent) + floating updated |

---

## Gate history table

Update the gate history table in `features/<feature>/README.md` to add a Cycle column and new rows for the second cycle:

```markdown
| Gate | Cycle | Date | Tag | Owner |
|---|---|---|---|---|
| CDR | 1 | 2025-03-10 | `cdr/<feature>/approved` | Alice |
| TRR | 1 | 2025-04-15 | `trr/<feature>/approved` | Alice |
| Release | 1 | 2025-05-01 | `release/<feature>/approved` | Alice |
| CDR | 2 | 2026-02-12 | `cdr/<feature>/r2/approved` | Bob |
| TRR | 2 | 2026-03-20 | `trr/<feature>/r2/approved` | Bob |
| Release | 2 | 2026-04-01 | `release/<feature>/r2/approved` | Bob |
```

---

## What CI does automatically

- `signoff-branch-setup.yml` recognises the `-rN` suffix and sets the correct previous gate tag in the evidence file
- `gate-tags.yml` creates both the cycle-namespaced tag (`r2/approved`) and updates the floating `approved` tag
- `hw-release.yml` triggers on `release/<feature>/r2/approved` and generates a new manufacturing release
- The manufacturing ZIP is named `<feature>-cycle2-manufacturing.zip`

---

## What the engineer does manually

- Update the gate history table in `features/<feature>/README.md`
- Update `requirements/verification-matrix.md` with the new cycle's evidence
- Increment the schematic title block `rev` field (e.g. A → B)
- Update `datasheet/specs.yaml` if performance values have changed
