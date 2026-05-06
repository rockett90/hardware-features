# KiCad Setup Guide

For the required KiCad version and all other tool versions, see [docs/versions.md](../versions.md).

---

## Installation

1. Download KiCad from [kicad.org](https://www.kicad.org).
2. Install the version listed in [docs/versions.md](../versions.md). Do not install a different version without coordinating with the lead — the CI pipeline uses a pinned KiBot Docker image that matches this version, and mismatches cause file format divergence.

---

## Cloning with the component library

The component library is a git submodule. If you clone without submodules, KiCad will open schematics with empty symbol boxes.

**Using SourceTree (recommended):**

See [docs/setup/sourcetree-setup.md](sourcetree-setup.md) for the full SourceTree guide. When cloning, tick **"Recurse submodules"**.

**Using the terminal:**

```bash
git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
```

**If you have already cloned without submodules:**

```bash
git submodule update --init
```

**Verify the submodule is populated:**

Check that `library/symbols/` contains `.kicad_sym` files. If the directory is empty, the submodule did not initialise correctly — re-run the command above.

---

## Configuring the symbol library

1. Open KiCad and open any feature project.
2. Go to **Preferences → Manage Symbol Libraries**.
3. Select the **Project Specific Libraries** tab.
4. Click **Add existing library to table** (folder icon).
5. Add the path: `${KIPRJMOD}/../../library/symbols/company.kicad_sym`

This path uses KiCad's `${KIPRJMOD}` variable, which resolves to the directory containing the `.kicad_pro` file. Because every feature project lives at `features/<feature-name>/`, the path `../../library/` always resolves to the shared `library/` directory at the repository root — so a single path works for all features without reconfiguration.

---

## Configuring the footprint library

1. Go to **Preferences → Manage Footprint Libraries**.
2. Select the **Project Specific Libraries** tab.
3. Add the path: `${KIPRJMOD}/../../library/footprints/FamilyName.pretty`

Replace `FamilyName` with the actual footprint library folder name. The same `${KIPRJMOD}` logic applies.

---

## Verifying the setup

- Open a schematic. Symbols should appear with their correct graphics, not as empty boxes.
- If symbols show as empty boxes, the library path is not configured correctly or the submodule is not populated.
- Run `git submodule status` in the terminal. If any line has a `-` prefix, run `git submodule update --init` to populate it.

---

## KiCad version upgrades

Coordinate with the lead before upgrading. The steps are:

1. Test the new version locally against `tests/reference-designs/poc-test/`.
2. Re-run the CI pipeline against `poc-test/` inside the new KiBot Docker image.
3. Update the Docker image digest in `config/kibot/`.
4. Update [docs/versions.md](../versions.md) with the new KiCad version and Docker digest.
5. Raise a `chore(library): upgrade KiCad to <version>` PR with lead approval.
