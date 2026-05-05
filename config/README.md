# config

> Configuration files for CI tooling — KiBot render configs and kicad-happy analysis rules.

---

## What is this directory?

This directory contains configuration files consumed by CI workflows. Engineers editing these files should test their changes against the pinned Docker image before merging.

> ⚠️ Warning: The KiBot Docker image is pinned by SHA digest in all workflows. If you update a KiBot config, verify it produces correct output against the **pinned** image, not the latest tag. Using a different image version may produce different output or fail silently.

---

## Structure

| Directory | Contents | Used by |
|---|---|---|
| `kibot/` | KiBot YAML configs for SVG export, BOM generation, and Gerber export | `render.yml` |

---

## `kibot/`

| File | Purpose |
|---|---|
| `base.kibot.yml` | Base KiBot configuration — shared settings inherited by feature-specific configs |
| `base-feature.kibot.yml` | Per-feature KiBot config template — copied into each feature directory on init as `.kibot.yml` |

> 💡 Tip: Each feature directory contains its own `.kibot.yml` (created by `init-feature.sh`). That file references the base config here using a relative path. If you need to change render settings for a single feature only, edit that feature's `.kibot.yml` directly.

---

## Pinned Docker image

All KiBot workflows use a pinned Docker image digest. The current pinned digest is recorded in the workflow files under `.github/workflows/`. Do not change the digest without coordinating with the team and testing the full render pipeline.
