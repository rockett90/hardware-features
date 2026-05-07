# tests

This directory will contain regression tests for CI scripts and KiCad tooling.

## KiCad regression tests

A reference design for regression-testing KiCad and KiBot version upgrades will be added here once a suitable feature has been completed. Until then, KiCad/KiBot upgrades should be validated manually against the Docker image before updating the pinned SHA in `docs/versions.md`.

## CI script tests

Unit tests for scripts in `scripts/ci/` (e.g. `validate-branch-name.sh`, `validate-dir-structure.py`) will live in `tests/ci/`.
