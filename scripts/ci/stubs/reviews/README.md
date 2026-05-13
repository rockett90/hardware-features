# reviews

> Review records and sign-off evidence for `FEATURE_NAME`.

---

## What belongs here

This directory contains **CI-managed review evidence only**. Do not manually create files here unless specified below.

| File / Pattern | Source | Notes |
|---|---|---|
| `gate-evidence-cdr.md` | Created automatically by CI when a `signoff/FEATURE_NAME/cdr` branch is pushed | Do not edit manually |
| `gate-evidence-trr.md` | Created automatically by CI when a `signoff/FEATURE_NAME/trr` branch is pushed | Do not edit manually |
| `gate-evidence-release.md` | Created automatically by CI when a `signoff/FEATURE_NAME/release` branch is pushed | Do not edit manually |
| `library.lock` | Committed manually at CDR and TRR — version-pins the shared library at gate sign-off | See [docs/how-to/library-lock.md](../../../docs/how-to/library-lock.md) |

---

## What does NOT belong here

- Review minutes — these should be stored in the project SharePoint area and linked from the feature README
- Completed review checklists — review checklists live in [`checklists/review/`](../../../checklists/review/) and are reference documents, not per-feature artefacts
- Informal notes or scratch files

---

## Gate evidence files

Gate evidence files (`gate-evidence-*.md`) are created automatically by the `signoff-branch-setup.yml` workflow when a sign-off branch is pushed. They record the SHA, date, and previous gate tag at the time of branch creation. Do not edit or delete them.

---

## External review records

Formal design review minutes and sign-off records are stored in SharePoint, not in this repository. Link to them from the feature README (`../README.md`) under the **External links** section.
