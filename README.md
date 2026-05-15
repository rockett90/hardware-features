# hardware-features

> A KiCad hardware design repository with automated CI for schematic rendering, visual diffing, ERC/DRC, AI review, and release management.

---

## Quick start

1. **Clone with submodules** — the shared component library is a git submodule and must be checked out at the same time:
   ```bash
   git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
   ```
2. **Open in KiCad** — open `features/<feature-name>/kicad/<feature-name>.kicad_pro`. See [docs/versions.md](docs/versions.md) for the required KiCad version.
3. **Create a branch and open a draft PR** — CI runs on every push. Open the PR as a draft immediately after your first push so checks can start running.
4. **Use slash commands** during review to trigger CI actions — see [Slash commands](#slash-commands) below.

---

## Toolchain & versions

See [docs/versions.md](docs/versions.md) for all pinned tool and dependency versions.

| Tool | Notes |
|---|---|
| KiCad | Pinned — do not upgrade individually, coordinate with the lead |
| KiBot | Via Docker (pinned SHA) — used in CI only, no local install needed |
| kicad-happy | Deterministic schematic and PCB analysis |
| Python | Required for local script use — minimum version in [docs/versions.md](docs/versions.md) |
| Pillow / cairosvg / sexpdata | Required for `kicad-visual-diff` locally — pinned in `scripts/ci/requirements.txt` |
| release-please | Manages `CHANGELOG.md` and GitHub Releases automatically |

---

## Repository structure

```
.github/          — Workflows, templates, guidelines, agent instructions
assets/           — Static assets (logos, images used in docs)
bench/            — Bench instrument drivers for automated hardware test
checklists/       — Gate and design review checklists
config/           — KiBot render configs, kicad-happy rules
docs/             — Guides, how-tos, and reference documentation
features/         — One directory per hardware feature (KiCad projects live here)
guidelines/       — Engineering and design guidelines
kicad-visual-diff/— Reusable GitHub Action for schematic/PCB visual diffing
library/          — Shared KiCad component library (git submodule)
scripts/          — CI automation scripts (also runnable locally)
templates/        — KiCad project templates used when scaffolding a new feature
tests/            — Tests for CI scripts and tooling
```

---

## Slash commands

Post a slash command as a PR comment to trigger CI actions. Commands require **write access** to the repository.

| Command | Action |
|---|---|
| `/render` | Export schematic as SVG — readable without KiCad |
| `/kicad-diff` | Generate a four-column visual diff of schematic (and PCB) changes vs base branch |
| `/ai-review` | Run AI schematic review — posts findings as a PR comment |
| `/erc` | Run Electrical Rules Check — informational, does not block merge |
| `/drc` | Run Design Rules Check — informational, does not block merge |
| `/datasheet` | Regenerate the feature datasheet from `datasheet/specs.yaml` and `datasheet/application-notes.md` |

The dispatcher reacts with 👀 immediately on receipt, ✅ on success, ❌ on failure.

---

## Branch naming

| Type | Pattern |
|---|---|
| Initialise new feature | `init/<feature>` |
| Design work | `artifact/<feature>/<desc>` |
| Design work with ticket | `artifact/<feature>/<desc-HW-123>` |
| IVV finding | `finding/<feature>/<N>-<desc>` |
| CDR sign-off | `signoff/<feature>/cdr` |
| TRR sign-off | `signoff/<feature>/trr` |
| Release sign-off | `signoff/<feature>/release` |
| Library change | `library/<desc>` |
| Tooling / docs | `chore/<desc>` |

CI validates every PR branch name. A non-matching name fails the "Validate branch name" check and cannot merge until corrected.
Sign-off branches are created automatically by running **Actions → Gate Sign-Off → Run workflow**.

> **Sign-off branches:** `signoff/<feature>/cdr`, `signoff/<feature>/trr`, and `signoff/<feature>/release` are created by the **Actions → Gate Sign-Off** workflow. Do not create these branches manually.

---

## Feature lifecycle (overview)

1. **Init PR** (`init/<feature>`) — scaffolds the full feature directory structure automatically on merge.
2. **Design work** (`artifact/<feature>/...` PRs) — schematic and PCB changes, one feature per PR.
3. **Use slash commands** during review: `/render`, `/kicad-diff`, `/ai-review`, `/erc`, `/drc`, `/datasheet`.
4. **CDR sign-off** — run the **Gate Sign-Off** workflow from the Actions tab, select `cdr`, and let CI create the sign-off branch and PR automatically. Gate-check CI must pass before merge.
5. **TRR sign-off** — run the **Gate Sign-Off** workflow from the Actions tab, select `trr`, and let CI create the sign-off branch and PR automatically. Gate-check CI must pass before merge; creates the `trr/<feature>/approved` tag.
6. **Final Release sign-off** — run the **Gate Sign-Off** workflow from the Actions tab, select `release`, and let CI create the sign-off branch and PR automatically. Gate-check CI must pass before merge; creates the `release/<feature>/approved` tag. See [docs/how-to/release-signoff.md](docs/how-to/release-signoff.md).
7. **Release** — merge the release-please Release PR; never close it manually. Manufacturing outputs are generated automatically from the `release/<feature>/approved` gate tag.

---

## Further reading

**Setup**
- [docs/versions.md](docs/versions.md) — all pinned tool and dependency versions
- [docs/tools.md](docs/tools.md) — toolchain reference for new engineers
- [docs/setup/kicad-setup.md](docs/setup/kicad-setup.md) — KiCad installation and library setup
- [docs/setup/tool-setup.md](docs/setup/tool-setup.md) — Git tooling setup (GitHub Desktop or GitHub CLI)

**Contributor reference**
- [CONTRIBUTING.md](CONTRIBUTING.md) — full contributor guide including branch naming, commit format, CI failure fixes, and IVV finding loop

**How-to guides**
- [docs/how-to/README.md](docs/how-to/README.md) — index of all how-to guides
- [docs/how-to/worked-example.md](docs/how-to/worked-example.md) — complete worked example from idea to release
- [docs/how-to/init-feature.md](docs/how-to/init-feature.md) — how to initialise a new feature
- [docs/how-to/design-workflow.md](docs/how-to/design-workflow.md) — day-to-day design workflow

**Gate sign-offs**
- [docs/how-to/cdr-signoff.md](docs/how-to/cdr-signoff.md) — how to perform a CDR sign-off
- [docs/how-to/trr-signoff.md](docs/how-to/trr-signoff.md) — how to perform a TRR sign-off
- [docs/how-to/release-signoff.md](docs/how-to/release-signoff.md) — how to perform a Final Release sign-off

**CI and tooling**
- [scripts/ci/README.md](scripts/ci/README.md) — CI script reference
- [kicad-visual-diff/README.md](kicad-visual-diff/README.md) — visual diff action reference
