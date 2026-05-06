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

The KiCad templates in this directory are present but minimal. The team's standard stackup, design rules, and approval fields will be added as they are agreed. See [docs/versions.md](../docs/versions.md) for the KiCad version these templates target.
