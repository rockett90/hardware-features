# .github/guidelines

> Detailed guidelines for CI tooling, AI review, and repository conventions — referenced by workflows and Copilot agents.

---

## What is this directory?

This directory contains guidelines that supplement `CONTRIBUTING.md`. They are used in two ways:

1. **Referenced by CI workflows** — for example, `gate-check.yml` uses `gate-criteria.md` to determine what constitutes a passing gate.
2. **Loaded by the AI review agent** — the Copilot coding agent reads these files as context when performing schematic review and other analysis tasks.

> 💡 Tip: For engineering guidelines (derating, PCB design rules, component selection), see [`guidelines/`](../../guidelines/README.md) at the repository root instead.

---

## Files

| File | Purpose |
|---|---|
| `bom-standards.md` | Standards and conventions for BOM entries — component fields, manufacturer part numbers, approved supplier rules |
| `commit-standards.md` | Conventional Commits format requirements and valid type/scope combinations |
| `gate-criteria.md` | What must be present and correct for a CDR or TRR gate to pass — used by `gate-check.yml` |
| `ivv-standards.md` | Standards for IVV (Integration, Verification and Validation) findings — branch naming, severity classification, resolution requirements |
| `schematic-standards.md` | KiCad schematic drawing standards — net naming, power symbols, hierarchical sheet conventions, annotation rules |

---

## Editing these files

- Raise a `chore/` PR with lead approval.
- Changes to `gate-criteria.md` directly affect what `gate-check.yml` accepts — verify the workflow still passes on a known-good gate PR after editing.
- Changes to `schematic-standards.md` are picked up by the AI review agent automatically on the next run — no workflow changes needed.
