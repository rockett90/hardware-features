# templates

This directory contains KiCad project templates that are copied into each new feature directory when an `init/<feature>` PR merges and `init-feature.sh` runs.

Templates include:

- **Title block** (`.kicad_wks`) — copied into each feature at `features/<feature>/kicad/title-block.kicad_wks`; engineers can customize per feature as needed.
- **Schematic template** (`.kicad_sch`) — base schematic with title block wired up
- **PCB template** (`.kicad_pcb`) — base PCB with design rules and stackup
- **Project settings file** (`.kicad_pro`) — shared project preferences

> ℹ️ The title block template is copied into each new feature at init. Template changes affect only newly scaffolded features; existing features keep their local copy unless updated intentionally.

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
| `title-block.kicad_wks` | `features/<feature>/kicad/title-block.kicad_wks` |

The templates are minimal starters. The team's standard stackup, design rules, and approval fields will be added to `pcb-template.kicad_pcb` and `title-block.kicad_wks` as they are agreed. See [docs/versions.md](../docs/versions.md) for the KiCad version these templates target.

When updating a template, all existing features will be unaffected (the template was already copied). Only new features created after the update will use the new template.

---

## KiCad project structure notes

- The `.kicad_pro` and `.kicad_sch` template files are intended to live in `features/<feature>/kicad/` as `features/<feature>/kicad/<feature>.kicad_pro` and `features/<feature>/kicad/<feature>.kicad_sch`.
- KiCad's project panel may show parent directories when you open one of these feature projects. This is normal KiCad UI behaviour.
- The title block file is stored next to the feature KiCad files at `features/<feature>/kicad/title-block.kicad_wks`, and templates reference it as `title-block.kicad_wks`.
- These templates target KiCad 10.
