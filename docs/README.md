# docs

> Reference documentation and guides for working with this repository.

---

## Structure

| Directory / File | Contents |
|---|---|
| `setup/` | Environment and tooling setup guides |
| `how-to/` | Step-by-step process guides for specific workflow tasks |
| `tools.md` | Toolchain reference — what each tool does and why it was chosen |
| `versions.md` | Single source of truth for all pinned tool and dependency versions |

---

## Setup guides

| Guide | Description |
|---|---|
| [setup/tool-setup.md](setup/tool-setup.md) | Installing Git tooling (GitHub Desktop or GitHub CLI) and cloning the repository |
| [setup/kicad-setup.md](setup/kicad-setup.md) | Installing KiCad and configuring the symbol and footprint libraries |
| [setup/ai-review-setup.md](setup/ai-review-setup.md) | Enabling AI schematic review — token setup, data protection, troubleshooting |

---

## How-to guides

| Guide | Description |
|---|---|
| [how-to/worked-example.md](how-to/worked-example.md) | Complete worked example — hardware feature from idea to release |
| [how-to/init-feature.md](how-to/init-feature.md) | How to initialise a brand-new hardware feature |
| [how-to/design-workflow.md](how-to/design-workflow.md) | Day-to-day workflow for working on a hardware feature |
| [how-to/cdr-signoff.md](how-to/cdr-signoff.md) | How to perform a Critical Design Review (CDR) sign-off |
| [how-to/library-submodule.md](how-to/library-submodule.md) | How to initialise, update, and work with the hardware library submodule |
| [how-to/library-lock.md](how-to/library-lock.md) | What library.lock is and how to use it for design traceability |
| [how-to/trr-signoff.md](how-to/trr-signoff.md) | How to perform a Test Readiness Review (TRR) sign-off |
| [how-to/release-signoff.md](how-to/release-signoff.md) | How to perform a Final Release sign-off |

---

## Reference

| Document | Description |
|---|---|
| [tools.md](tools.md) | Toolchain reference for new engineers |
| [versions.md](versions.md) | All pinned tool and dependency versions |

---

## Adding documentation

- Add new setup guides to `docs/setup/` as Markdown files.
- Add new how-to guides to `docs/how-to/` as Markdown files.
- Add the new file to the relevant table above.
- Raise a `chore/` PR.
