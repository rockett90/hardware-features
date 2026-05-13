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
| `kicad-project-template.kicad_pro` | `features/<feature>/kicad/<feature>.kicad_pro` |
| `schematic-template.kicad_sch` | `features/<feature>/kicad/<feature>.kicad_sch` |
| `pcb-template.kicad_pcb` | `features/<feature>/kicad/<feature>.kicad_pcb` |
| `title-block.kicad_wks` | Referenced by path — not copied per feature |

The templates are minimal starters. The team's standard stackup, design rules, and approval fields will be added to `pcb-template.kicad_pcb` and `title-block.kicad_wks` as they are agreed. See [docs/versions.md](../docs/versions.md) for the KiCad version these templates target.

When updating a template, all existing features will be unaffected (the template was already copied). Only new features created after the update will use the new template.

---

## KiCad project structure notes

- The `.kicad_pro` and `.kicad_sch` template files are intended to live in `features/<feature>/kicad/` as `features/<feature>/kicad/<feature>.kicad_pro` and `features/<feature>/kicad/<feature>.kicad_sch`.
- KiCad's project panel may show parent directories when you open one of these feature projects. This is normal KiCad UI behaviour.
- The title block is referenced from `templates/title-block.kicad_wks` relative to the repository root using `../../templates/title-block.kicad_wks` from the feature root. If the repository is moved or copied to a different relative location, that path may need updating.
- These templates target KiCad 10.
