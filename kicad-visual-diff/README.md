# kicad-visual-diff

This directory contains the KiCad visual diff tooling used by `kicad-diff.yml` to produce four-column visual diffs of schematic and PCB changes on pull requests.

## Location

This tooling lives at the repository root rather than in `scripts/` intentionally — it is self-contained and is planned to be extracted as a submodule shared across multiple hardware repositories in future. When that happens, this directory becomes a submodule pointer and nothing else in the repository changes.

## Usage

Triggered via the `/kicad-diff` slash command on any PR. See `docs/how-to/design-workflow.md` for usage instructions.
