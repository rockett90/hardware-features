# templates

This directory contains KiCad project templates that are copied into each new feature directory when an `init/<feature>` PR merges and `init-feature.sh` runs.

Templates include:

- **Title block** (`.kicad_wks`) — referenced by path from all feature schematics; not copied per feature. Changes take effect globally when engineers next open their schematics.
- **Schematic template** (`.kicad_sch`) — base schematic with title block wired up
- **PCB template** (`.kicad_pcb`) — base PCB with design rules and stackup
- **Project settings file** (`.kicad_pro`) — shared project preferences

> ⚠️ The title block is **referenced by path from all feature schematics** — it is not copied per feature. Any change to it takes effect for all features the next time an engineer opens their schematic.

---

## Protection

These files are CODEOWNERS-protected. Changes require a `chore/` PR with lead approval.

---

## Current status

All four template files are present and will be copied by `init-feature.sh` when an `init/<feature>` PR merges:

| File | Copied to |
|---|---|
| `kicad-project-template.kicad_pro` | `features/<feature>/<feature>.kicad_pro` |
| `schematic-template.kicad_sch` | `features/<feature>/<feature>.kicad_sch` |
| `pcb-template.kicad_pcb` | `features/<feature>/pcb/<feature>.kicad_pcb` |
| `title-block.kicad_wks` | Referenced by path — not copied per feature |

The templates are minimal starters. The team's standard stackup, design rules, and approval fields will be added to `pcb-template.kicad_pcb` and `title-block.kicad_wks` as they are agreed. See [docs/versions.md](../docs/versions.md) for the KiCad version these templates target.

When updating a template, all existing features will be unaffected (the template was already copied). Only new features created after the update will use the new template.
