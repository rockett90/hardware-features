# Versions

Single source of truth for all pinned tool and dependency versions used in this repository.

When a version changes, update this file and all inline references in the same PR.

---

## KiCad

| Tool | Version | Notes |
|---|---|---|
| KiCad | **10.0.1** | Do not upgrade individually — coordinate with the lead |
| KiBot Docker image | `ghcr.io/inti-cmnb/kicad10_auto_full@sha256:81621e501169e66dc051a65a0e575c0ab2854f69a121f1f9d97aad2b0d4c0257` | Pinned digest — update via `chore/` PR after regression testing |

---

## Python dependencies (kicad-visual-diff)

Pinned in `scripts/ci/requirements.txt`.

| Package | Version | Purpose |
|---|---|---|
| Pillow | 12.2.0 | Image processing and rasterisation |
| cairosvg | 2.7.1 | SVG to PNG conversion |
| lxml | 6.1.0 | XML and SVG parsing |
| sexpdata | 1.0.2 | KiCad S-expression file parsing |

---

## CI and automation tools

| Tool | Version | Notes |
|---|---|---|
| kicad-happy | v1.3.0 (pinned) | Deterministic schematic and PCB analysis |
| release-please | @v5 | Changelog and release automation |
| actions/checkout | @v4 | — |
| actions/upload-artifact | @v4 | — |
| actions/github-script | @v7 | — |
| actions/setup-node | @v4 | — |
| Node.js | 20 | Used for commitlint PR title validation |

---

## AI models

Model selection is handled automatically by the GitHub Copilot Models API — no specific model is pinned in the workflow. The model actually used is logged in the AI review comment on each PR under the **Model:** field.

To change the model, a specific `model` field can be added to the API request body in `.github/workflows/ai-review.yml`. Coordinate with the lead before doing this.

---

## Python runtime

Minimum version: **3.11+**

---

## How to upgrade a version

1. Test the upgrade locally where possible.
2. For KiCad or KiBot: re-run the KiCad regression tests inside the new Docker image first — see `tests/README.md` for instructions once a reference design is available.
3. Raise a `chore(library): upgrade <tool> to <version>` PR.
4. Update this file and all inline references in the same PR.
5. Lead approval required.
