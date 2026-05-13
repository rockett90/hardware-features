# How to work with the hardware library submodule

The shared hardware component library is included in this repository as a git submodule at `library/`. This document explains how to initialise it, update it, and understand how the library version is tracked against each feature.

---

## Initial setup

When you clone this repository, initialise the submodule:

```bash
git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
```

Or if you have already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

---

## Using the library in KiCad

The library is located at `library/` relative to the repository root. In KiCad, paths are configured relative to `${KIPRJMOD}` (the project file location). Feature KiCad projects are at `features/<feature>/kicad/`, so the library path in KiCad settings should be:

```
${KIPRJMOD}/../../../library/symbols/
${KIPRJMOD}/../../../library/footprints/
```

These paths are set up automatically in the KiCad project template — you should not need to configure them manually.

---

## Updating the submodule to get new library components

When new components are added to `hardware-library`, update the submodule pointer in your feature branch:

```bash
cd library
git fetch
git checkout main
git pull
cd ..
git add library
git commit -m "chore(library): update submodule to latest main"
```

Then push your branch and open a PR as normal.

> ⚠️ Warning: Do not update the library submodule on a `signoff/` branch. Library updates should be made on an `artifact/` branch and merged before raising a sign-off PR.

---

## Checking the current library version

To see which commit of the library is currently checked out:

```bash
git submodule status
```

This prints the commit SHA, path, and description for each submodule. A `-` prefix means the submodule has not been initialised yet.

To inspect the library commit history:

```bash
cd library
git log --oneline
```

---

## Relationship to library.lock

At CDR sign-off, CI automatically records the exact library commit in `features/<feature>/reviews/library.lock`. This provides a traceable record of which library version was reviewed and approved at CDR.

Updating the submodule after CDR does not invalidate `library.lock` — the lock file is a point-in-time snapshot, not a constraint on future updates.

See [library-lock.md](library-lock.md) for details.
