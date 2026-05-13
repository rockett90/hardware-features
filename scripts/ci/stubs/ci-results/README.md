# ci-results

> CI-generated evidence and release records for this feature.

---

## What belongs here

Files are written here automatically by CI workflows. Do not create or edit files in this directory manually unless specified below.

| File | Written by | When |
|---|---|---|
| `erc-report.txt` | `erc-drc.yml` | On every PR that changes `.kicad_sch` files, and on `/erc` command |
| `drc-report.txt` | `erc-drc.yml` | On every PR that changes `.kicad_pcb` files, and on `/drc` command |
| `erc-report-release.txt` | `hw-release.yml` | When a production release tag is pushed |
| `release-manifest.txt` | `hw-release.yml` | When a production release tag is pushed — records tag, version, date, and file list |

---

## What does NOT belong here

- Schematic renders (SVGs, PDFs) — these are uploaded as workflow artefacts and not committed
- Manufacturing outputs (Gerbers, BOM, CPL) — these go to `../fab/release/` and are uploaded to GitHub Releases
- Manually written notes or documents
