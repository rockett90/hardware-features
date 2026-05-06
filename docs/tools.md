# Tools Reference

A map of every tool in the platform for new engineers. This is not a how-to guide — it explains what each tool does, why it was chosen, and where to find more information.

For pinned versions of all tools listed here, see [docs/versions.md](versions.md).

---

## KiCad

**What it does:** Schematic capture, PCB layout, and BOM generation.

**Why it was chosen:** Open-source EDA tool with a strong community, native git-friendly file formats (text-based S-expression), and a command-line interface (`kicad-cli`) that enables full CI automation without a GUI.

**Documentation:** [kicad.org](https://www.kicad.org)

---

## KiBot

**What it does:** Automated export of schematics, PCB layouts, BOMs, and Gerber files from the command line. Used in CI for SVG renders and ERC/DRC checks.

**Why it was chosen:** Mature, well-maintained tool with a declarative YAML configuration format. Runs inside a pinned Docker image so CI output is reproducible regardless of local KiCad version.

**Documentation:** [github.com/INTI-CMNB/KiBot](https://github.com/INTI-CMNB/KiBot)

---

## kicad-happy

**What it does:** Deterministic schematic and PCB analysis — IC pinout checks, voltage derating, and change diff. Runs before AI review to provide structured, machine-readable findings.

**Why it was chosen:** Produces structured output that can be fed directly to the AI review step, giving the AI reviewer grounded findings rather than asking it to infer issues from raw files.

**Documentation:** [github.com/aklofas/kicad-happy](https://github.com/aklofas/kicad-happy)

---

## kicad-visual-diff

**What it does:** Custom tool in this repository (`scripts/ci/kicad-visual-diff.py`, packaged as a GitHub Action in `kicad-visual-diff/`). Generates a four-column HTML visual diff report (Old / Diff / New per schematic sheet or PCB layer) when triggered by the `/kicad-diff` slash command.

**Why it was chosen:** Reviewers need to see exactly what changed in a schematic or PCB, not just a raw text diff of S-expression files. The self-contained HTML report with zoom/pan makes this accessible without KiCad installed.

**Documentation:** [kicad-visual-diff/README.md](../kicad-visual-diff/README.md)

---

## GitHub Models API

**What it does:** Provides access to AI models (Claude, GPT-4) via a standard GitHub token. Used by `ai-review.yml` to run automated schematic review on every PR.

**Why it was chosen:** No separate API key or billing required with a Copilot licence. The standard `GITHUB_TOKEN` is sufficient, making it straightforward to enable across all PRs without additional secrets management.

**Documentation:** [models.github.com](https://models.github.com)

---

## release-please

**What it does:** Automates changelog generation and release PRs from Conventional Commit PR titles. Creates and maintains `CHANGELOG.md` per feature automatically.

**Why it was chosen:** Turns the PR title discipline (which CI already enforces) into an automatic release record. Engineers do not write changelogs manually.

**Documentation:** [github.com/googleapis/release-please](https://github.com/googleapis/release-please)

---

## commitlint

**What it does:** Validates PR titles against the Conventional Commits format. Prevents malformed release notes from entering the changelog.

**Why it was chosen:** Lightweight, zero-configuration for basic usage, and integrates directly with GitHub Actions. Enforces the discipline that release-please depends on.

**Documentation:** [commitlint.js.org](https://commitlint.js.org)

---

## SourceTree

**What it does:** Recommended Git GUI client. Handles submodule cloning natively, making it the easiest way for engineers to clone the repository with the component library intact.

**Why it was chosen:** The repository uses a git submodule for the component library. SourceTree has a "Recurse submodules" tick-box on the clone dialog, which prevents the most common setup mistake.

**Documentation:** [sourcetreeapp.com](https://www.sourcetreeapp.com) · [Setup guide](setup/sourcetree-setup.md)

---

## GitHub Actions

**What it does:** CI/CD platform. All automation in this repository runs here — rendering, AI review, gate checks, visual diff, finding label management, release automation, and more.

**Why it was chosen:** Native to GitHub, no separate service to maintain, and the `GITHUB_TOKEN` is available automatically for all workflows.

**Documentation:** [github.com/features/actions](https://github.com/features/actions)

---

## GitHub Copilot PR Review

**What it does:** Automatic code and documentation review on every PR. Provides a second pass on top of the AI schematic review to catch documentation issues, workflow errors, and general code quality problems.

**Why it was chosen:** Available as part of the Copilot licence at no additional cost. Complements the domain-specific AI schematic review with general-purpose review coverage.
