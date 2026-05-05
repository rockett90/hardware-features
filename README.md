# hardware-features

> A KiCad hardware design repository with automated CI for schematic rendering, visual diffing, ERC/DRC, AI review, and release management.

---

## Quick start

1. **Clone with submodules** — the shared component library is a git submodule and must be checked out at the same time:
   ```bash
   git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
   ```
2. **Open in KiCad 10.0.1** — open `features/<feature-name>/<feature-name>.kicad_pro`.
3. **Create a branch and open a draft PR** — CI runs on every push. Open the PR as a draft immediately after your first push so checks can start running.
4. **Use slash commands** during review to trigger CI actions — see [Slash commands](#slash-commands) below.

---

## Toolchain & versions

| Tool | Version | Notes |
|---|---|---|
| KiCad | 10.0.1 | **Pinned. Do not upgrade individually — coordinate with the team.** |
| KiBot | via Docker (`kicad10_auto_full`, pinned SHA) | Used in CI only — no local install needed |
| kicad-happy | latest (cloned in CI) | Design analysis and derating checks |
| Python | 3.9+ | Required for local script use |
| Pillow | latest | Required for `kicad-visual-diff` locally |
| cairosvg | latest | Required for `kicad-visual-diff` locally |
| sexpdata | latest | Required for semantic diff locally |
| release-please | v4 | Manages `CHANGELOG.md` and GitHub Releases automatically |

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

The dispatcher reacts with 👀 immediately on receipt, ✅ on success, ❌ on failure.

---

## Branch naming

| Type | Pattern |
|---|---|
| Concept exploration | `concept/<feature>` |
| Initialise new feature | `init/<feature>` |
| Design work | `artifact/<feature>/<desc>` |
| Design work with ticket | `artifact/<feature>/<desc-HW-123>` |
| IVV finding | `finding/<feature>/<N>-<desc>` |
| CDR sign-off | `signoff/<feature>/cdr` |
| TRR sign-off | `signoff/<feature>/trr` |
| Re-TRR | `signoff/<feature>/trr-N` |
| Library change | `library/<desc>` |
| Tooling / docs | `chore/<desc>` |

CI validates every PR branch name. A non-matching name fails the "Validate branch name" check and cannot merge until corrected.

---

## Feature lifecycle (overview)

1. **Init PR** (`init/<feature>`) — scaffolds the full feature directory structure automatically on merge.
2. **Design work** (`artifact/<feature>/...` PRs) — schematic and PCB changes, one feature per PR.
3. **Use slash commands** during review: `/render`, `/kicad-diff`, `/ai-review`, `/erc`, `/drc`.
4. **CDR sign-off** (`signoff/<feature>/cdr`) — gate-check CI must pass before merge.
5. **TRR sign-off** (`signoff/<feature>/trr`) — gate-check CI must pass before merge.
6. **Release** — managed automatically by release-please; never close a Release PR manually.

---

## Further reading

- [CONTRIBUTING.md](CONTRIBUTING.md) — full contributor guide
- [docs/how-to/init-feature.md](docs/how-to/init-feature.md) — how to initialise a new feature
- [docs/how-to/design-workflow.md](docs/how-to/design-workflow.md) — day-to-day design workflow
- [docs/how-to/cdr-signoff.md](docs/how-to/cdr-signoff.md) — how to perform a CDR sign-off
- [docs/how-to/trr-signoff.md](docs/how-to/trr-signoff.md) — how to perform a TRR sign-off
- [scripts/ci/README.md](scripts/ci/README.md) — CI script reference
- [kicad-visual-diff/README.md](kicad-visual-diff/README.md) — visual diff action reference
