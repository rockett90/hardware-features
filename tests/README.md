# tests

> Regression fixtures and test infrastructure for CI scripts and automation tooling.

---

## `reference-designs/poc-test/`

This directory contains a simple KiCad schematic whose **only purpose is to prove the CI pipeline works end-to-end**.

It is **not** a hardware feature and must **never** be moved to `features/`. It is retained permanently as a regression fixture.

**Contents:**

| File | Purpose |
|---|---|
| `poc-test.kicad_sch` | Minimal schematic — a few components, no real circuit |
| `poc-test.kicad_pcb` | Minimal PCB — sufficient to exercise the PCB render path |
| `poc-test.kicad_pro` | KiCad project file |

**Why it is intentionally simple:** If a CI run fails against `poc-test/`, the failure is clearly a CI or tooling problem, not a design error. A complex reference design would make it harder to distinguish the two.

**Before upgrading KiCad or KiBot:** re-run the full CI pipeline against this design inside the new Docker image. See [docs/versions.md](../docs/versions.md) for the current versions and upgrade procedure.

---

## Unit tests

Unit tests for CI scripts are not yet written. When added, they should follow this convention:

| Script under test | Test file |
|---|---|
| `scripts/ci/kicad-visual-diff.py` | `tests/test_kicad_visual_diff.py` |
| `scripts/ci/validate-branch-name.sh` | `tests/test_validate_branch_name.py` |
| `scripts/ci/validate-dir-structure.py` | `tests/test_validate_dir_structure.py` |
| `scripts/ci/init-feature.sh` | `tests/test_init_feature.py` |

Use [pytest](https://docs.pytest.org/). Place test files directly in `tests/`. Use files from `tests/reference-designs/` as fixtures where KiCad files are needed.

```bash
pytest tests/
```
