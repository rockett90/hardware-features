# tests

> Tests for CI scripts and automation tooling.

---

## Status

Not yet populated. This directory is reserved for future unit tests of the scripts in `scripts/ci/`.

The `reference-designs/` subdirectory contains KiCad reference design files used as test fixtures.

---

## Running tests

```bash
pytest tests/
```

---

## Adding tests

- Use [pytest](https://docs.pytest.org/).
- One test file per script under test, named `test_<script_name>.py`.
- Place test files directly in `tests/`.
- Use files from `tests/reference-designs/` as test fixtures where KiCad files are needed.

| Script under test | Test file to create |
|---|---|
| `scripts/ci/kicad-visual-diff.py` | `tests/test_kicad_visual_diff.py` |
| `scripts/ci/validate-branch-name.sh` | `tests/test_validate_branch_name.py` |
| `scripts/ci/validate-dir-structure.py` | `tests/test_validate_dir_structure.py` |
| `scripts/ci/init-feature.sh` | `tests/test_init_feature.py` |

---

## `reference-designs/`

| Directory | Contents |
|---|---|
| `poc-test/` | A small proof-of-concept KiCad project used as a reference fixture for diff and render tests |
