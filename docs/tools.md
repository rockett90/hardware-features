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

**What it does:** Custom tool in this repository (`kicad-visual-diff/kicad-visual-diff.py`, packaged as a GitHub Action in `kicad-visual-diff/`). Generates a four-column HTML visual diff report (Old / Diff / New per schematic sheet or PCB layer) when triggered by the `/kicad-diff` slash command.

**Why it was chosen:** Reviewers need to see exactly what changed in a schematic or PCB, not just a raw text diff of S-expression files. The self-contained HTML report with zoom/pan makes this accessible without KiCad installed.

**Documentation:** [kicad-visual-diff/README.md](../kicad-visual-diff/README.md)

---

## GitHub Models API

**What it does:** Provides access to AI models (Claude, GPT-4) via a standard GitHub token. Used by `ai-review.yml` to run automated schematic review on every PR.

**Why it was chosen:** No separate API key or billing required with a Copilot licence. The standard `GITHUB_TOKEN` is sufficient, making it straightforward to enable across all PRs without additional secrets management.

**Documentation:** [models.github.com](https://models.github.com)

**Setup:** [docs/setup/ai-review-setup.md](setup/ai-review-setup.md)

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

## GitHub Desktop

**What it does:** Recommended Git GUI client. Handles submodule cloning natively via the **"Recurse submodules"** option in the clone dialog, making it the easiest way for engineers to set up the repository with the component library intact.

**Why it was chosen:** Free, no Atlassian account required, and runs on Windows and macOS. Supports submodule cloning, branch creation, commit, and push — covers all day-to-day operations without a terminal.

**Documentation:** [desktop.github.com](https://desktop.github.com) · [Setup guide](setup/tool-setup.md)

---

## GitHub Actions

**What it does:** CI/CD platform. All automation in this repository runs here — rendering, AI review, gate checks, visual diff, finding label management, release automation, and more.

**Why it was chosen:** Native to GitHub, no separate service to maintain, and the `GITHUB_TOKEN` is available automatically for all workflows.

**Documentation:** [github.com/features/actions](https://github.com/features/actions)

---

## GitHub Copilot PR Review

**What it does:** Automatic code and documentation review on every PR. Provides a second pass on top of the AI schematic review to catch documentation issues, workflow errors, and general code quality problems.

**Why it was chosen:** Available as part of the Copilot licence at no additional cost. Complements the domain-specific AI schematic review with general-purpose review coverage.

---

## KiCad SPICE Simulator

**What it does:** Built-in SPICE simulation environment inside KiCad. Used for circuit-level simulation (AC analysis, transient, DC operating point). Simulation files live in `features/<feature>/simulations/`.

**Why it was chosen:** Bundled with KiCad — no separate tool to install. Simulation files integrate directly with the schematic and component library. ngspice (the underlying engine) is also installed in CI for automated simulation runs.

**Documentation:** [KiCad Simulator docs](https://docs.kicad.org/8.0/en/eeschema/eeschema.html#simulation)

---

## Tool categories

| Category | Tools |
|---|---|
| **Local — required** | KiCad |
| **Local — recommended** | GitHub Desktop |
| **Local — optional** | GitHub CLI |
| **CI-only** | KiBot (Docker), kicad-happy, kicad-visual-diff, release-please, commitlint, ngspice |
| **CI + local** | Python 3.11+ (scripts are also runnable locally) |

---

## Supported operating systems

| OS | KiCad | GitHub Desktop | GitHub CLI | CI scripts (local) |
|---|---|---|---|---|
| Windows 10/11 | ✅ | ✅ | ✅ | ⚠️ See note below |
| macOS (Intel/Apple Silicon) | ✅ | ✅ | ✅ | ✅ |
| Linux | ✅ | ❌ | ✅ | ✅ |

> ⚠️ **Windows note:** CI automation scripts (`.sh` files in `scripts/ci/`) run in GitHub Actions on Ubuntu. They are not designed or tested for local execution on Windows. Engineers on Windows should use CI to run all automation — use slash commands (`/render`, `/kicad-diff`, `/ai-review`, `/erc`, `/drc`) in PR comments instead of running scripts locally.
> Python scripts in `scripts/ci/` can be run locally on Windows with Python 3.11+ if needed, but this is not required for normal workflow.
