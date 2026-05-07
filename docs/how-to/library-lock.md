# How to use `library.lock` for traceability

`library.lock` is a small YAML text file created automatically by CI when a CDR sign-off PR merges. It records the exact git SHA of the component library submodule and the feature directory at the moment CDR was approved.

---

## Where to find it

`library.lock` is created at:

```
features/<feature>/reviews/library.lock
```

The `reviews/` directory is scaffolded automatically at feature init. CI drops `library.lock` into that directory when CDR merges.

You will see it appear in a commit with this message:

```
chore(<feature>): create library.lock at CDR gate [skip ci]
```

---

## What it contains

Example:

```yaml
# Created automatically by CI at CDR gate. Do not edit manually.
library-submodule-url: https://github.com/rockett90/hardware-library.git
library-submodule-commit: a3f9c1d8e2b4f6a9c1d3e5b7f2a4c6e8d0b2f4a6
feature-commit: 8b2e44f1c3d5e7a9b1c3d5e7f9a1b3c5d7e9f1a3
locked-at-gate: cdr
locked-date: 2026-05-07
```

---

## Why it exists

The hardware component library is a git submodule and can be updated independently at any time. Without `library.lock`, there is no explicit record of which library version your design was reviewed against.

With `library.lock`, you can answer: **which exact footprint and symbol was approved at CDR?**

---

## How to use it

If you need to reconstruct the exact CDR design state later (audit, dispute, or reopening a design after a long gap), check out the locked library commit:

```bash
cd library
git checkout a3f9c1d8e2b4f6a9c1d3e5b7f2a4c6e8d0b2f4a6
```

This gives you the library exactly as it was on CDR approval day — every symbol, footprint, and 3D model. Open the KiCad project from that state to see what was reviewed.

---

## What it does **not** do

`library.lock` does **not** freeze the library and does not prevent other features from using newer library versions. It is purely a traceability record.

The library submodule pointer in the repository can still move forward; `library.lock` only records what was approved at the gate.

---

## Re-CDR behaviour

If a `finding: major` sends the design back to re-CDR, CI overwrites `library.lock` with a new file reflecting the library and feature SHAs at that later re-CDR approval.

This is expected and correct: the newest lock file reflects what was reviewed at the most recent CDR approval.

---

## Final Release checklist link

The Final Release sign-off checklist requires `library.lock` to be present before manufacturing outputs are authorised. This ensures every released design has a traceable library baseline.
