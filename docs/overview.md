# Hardware Design Control Repository — Engineer Overview

*A plain-English guide for engineers working with KiCad hardware designs in `hardware-features`.*

---

## Why this exists

Hardware design has always involved reviews, controlled releases, and traceability — but in practice these often rely on informal messages, local folders, email threads, and memory. When something goes wrong six months later, it is hard to find the approved schematic, understand what decision was made, or reproduce the manufacturing outputs.

This repository provides a structured, version-controlled home for hardware design work. It is not a replacement for good engineering judgement — it is a system that makes that judgement visible and retrievable.

---

## What the repository provides

- A single, auditable location for KiCad schematics, PCB layouts, calculations, simulations, BOM, bring-up evidence, and design decisions.
- Structured gate points (PDR, CDR, TRR, Release) with checklists and sign-off records.
- Automated artefact generation — schematic renders, visual diffs, ERC/DRC reports, datasheets, and manufacturing outputs.
- A clear design history: every change is recorded, linked to a reason, and traceable to a review.
- A shared component library (`hardware-library`) with controlled symbols, footprints, 3D models, and SPICE models — referenced as a submodule and locked at the CDR gate.
- Automatic release records — version tags, changelogs, and manufacturing packs created without manual effort.

---

## How the process works

Each hardware design lives in its own directory inside `features/`. The lifecycle follows these stages:

| Stage | Branch type | What happens |
|---|---|---|
| **1. Init (PDR)** | `init/<feature>` | Feature is registered. CI scaffolds the full directory structure and generates the initial datasheet stub. Requirements and design intent are defined. |
| **2. Design work** | `artifact/<feature>/...` | Schematic and PCB changes are made, one PR per artefact. Slash commands trigger renders, visual diffs, ERC/DRC, AI review, and datasheet regeneration. |
| **3. CDR sign-off** | `signoff/<feature>/cdr` | CI posts the CDR checklist into the PR. All items must be ticked before merge. A `cdr/.../approved` tag and a `library.lock` file are created automatically on merge. |
| **4. Build and bring-up** | `artifact/<feature>/...` | Hardware is built. Bring-up notes, measurements, and verified design values are committed. The datasheet is completed with measured data. |
| **5. TRR sign-off** | `signoff/<feature>/trr` | CI posts the TRR checklist. A `trr/.../approved` tag is created automatically on merge. Hardware is now ready for independent IVV. |
| **6. IVV** | `artifact/<feature>/...` | Independent test is performed externally. Findings are tracked as GitHub Issues and resolved via `finding/` branches. The verification matrix is updated with result references. |
| **7. Release sign-off** | `signoff/<feature>/release` | CI validates gate traceability, generates a PDF document pack, and creates a GitHub Release at the `release/.../approved` tag on merge. Manufacturing is now authorised. |
| **8. Production release** | (CI-managed Release PR) | An automatically raised Release PR finalises the version number, runs KiBot to generate manufacturing outputs (Gerbers, BOM, CPL, schematic PDF), and attaches them to the GitHub Release. Merge it — do not close it manually. |

If an IVV finding is raised, its severity determines whether a gate re-entry is required: minor findings may proceed without one; moderate findings require a re-TRR; major findings require a re-CDR then re-TRR.

---

## What gate reviews are for

A gate review is a structured pause point. Before moving from one design phase to the next, the relevant checklist must be completed and sign-off recorded.

- **PDR gate** — design intent and requirements are defined before detailed design begins. Captured via the `init/` PR.
- **CDR gate** — schematic is complete, ERC is clean, all components are specified, calculations and BOM are reviewed, and the design is ready for layout and test planning.
- **TRR gate** — test readiness is confirmed; the design is ready for build and IVV.
- **Release gate** — IVV is complete, all findings are resolved or formally deferred, manufacturing outputs are verified, and the design is authorised for production.

Gate reviews are not bureaucracy for their own sake. They are the point where evidence is collected and a record is created that the design was ready to proceed. Without them, a future investigation has no baseline to work from.

---

## What engineers need to do

The following discipline is expected from everyone working in the repository:

- **Branch naming** — use the correct pattern (e.g. `artifact/buck-converter-5v/add-schematic`). CI rejects a PR with a non-matching branch name and it cannot merge until corrected.
- **PR titles** — follow the format `type(scope): description` (e.g. `feat(buck-converter-5v): add initial schematic`). CI validates this automatically.
- **File location** — KiCad files live in `features/<feature>/kicad/`. Do not put them elsewhere.
- **One feature per PR** — a single PR must only change KiCad files in one feature directory. CI enforces this.
- **Checklists** — complete the relevant review checklist before requesting sign-off. Gate PRs will not merge until all checklist items are ticked.
- **Push regularly** — push at the end of every working session. Local-only changes are invisible to everyone else and have no design history.
- **Do not manually resolve KiCad file conflicts** — `.kicad_sch` and `.kicad_pcb` files are not safe to merge by hand. Speak to the lead.
- **Do not bypass the release process** — manufacturing outputs are generated at the Release gate. Do not use outputs generated informally outside this process.
- **Check generated outputs** — automation can fail or produce unexpected results. You remain responsible for confirming that rendered schematics, ERC reports, manufacturing files, and datasheets are correct before relying on them.

---

## How much GitHub do I need to know?

Not a great deal to start. Here are the essential terms:

| Term | What it means |
|---|---|
| **Branch** | A controlled working area for a change. Your design work happens here, separate from the main copy until it is reviewed and approved. |
| **Commit** | A saved checkpoint — a record of what changed and when. Individual commit messages are freeform; it is the PR title that is validated. |
| **Pull request (PR)** | A request to merge your change into the main copy. It is also where review happens, comments are made, CI results appear, and sign-off is given. |
| **Issue** | A record of a task, problem, or IVV finding. Used to track work and link evidence together. |
| **Tag / Release** | A fixed, permanent record of an approved design state at a point in time. Gate tags and version releases are created automatically by CI — you do not need to create them manually. |
| **Draft PR** | A PR that is not yet ready for review. Open one immediately after your first push so CI starts running. When ready, click "Ready for review" to trigger the AI review and the full review process. |

For setup guidance, see `docs/setup/` in the repository. GitHub Desktop is supported for those who prefer not to use the command line.

---

## What automation does

CI runs automatically on every push and pull request. It handles the mechanical parts so you do not have to.

| What CI does automatically | When |
|---|---|
| Scaffolds the full feature directory structure | When an `init/` branch is first pushed |
| Commits a gate evidence file to the branch | When a `signoff/` branch is first pushed |
| Generates the initial datasheet stub | When an `init/` PR is opened |
| Fills the PR body with the correct checklist or template | When any PR is opened or converted from draft |
| Validates branch name format and single-feature rule | On every PR update |
| Runs AI schematic review and posts findings | When a PR is marked "Ready for review" |
| Runs ERC / DRC and posts results | Via `/erc` or `/drc` (informational — does not block merge) |
| Generates schematic renders (SVG and PDF) | Via `/render` |
| Generates a visual diff of schematic and PCB changes | Via `/kicad-diff` |
| Regenerates the datasheet from source files | Via `/datasheet` |
| Validates gate checklist completion | On `signoff/` PRs — blocks merge until all items are ticked |
| Creates gate tags (`cdr/.../approved`, `trr/.../approved`, etc.) | When a gate PR merges |
| Creates `library.lock` recording the library commit at CDR | When the CDR gate PR merges |
| Generates a PDF document pack and creates a GitHub Release | When the release gate PR merges |
| Runs KiBot to generate manufacturing outputs and attaches them to the release | When the release-please Release PR merges |
| Manages the changelog and creates the production version tag | On merge of the release-please Release PR |
| Tracks IVV finding labels automatically | When a `finding/` PR is opened or merged |

**Slash commands** — post as a comment on a PR (write access required):

| Command | What it does |
|---|---|
| `/render` | Export schematic as SVG and PDF |
| `/kicad-diff` | Four-column visual diff of schematic and PCB changes vs base branch |
| `/ai-review` | AI schematic review — posts CRITICAL and ADVISORY findings |
| `/erc` | Electrical Rules Check — informational, does not block merge |
| `/drc` | Design Rules Check — informational, does not block merge |
| `/datasheet` | Regenerate the feature datasheet from `datasheet/specs.yaml` and `datasheet/application-notes.md` |

The dispatcher reacts 👀 when it receives a command, ✅ on success, and ❌ on failure.

ERC and DRC violations are reported as informational comments and do not block merge. Genuine errors should be fixed; intentional exceptions should be suppressed inside KiCad with a note. ERC evidence is formally reviewed at CDR; DRC evidence at TRR.

---

## What should stay outside the repository

The following are excluded by design:

- **Generated manufacturing outputs** (Gerbers, drill files, render PDFs and PNGs) — produced by CI and attached to GitHub Releases. Do not commit them manually.
- **KiCad local state and lock files** (`.kicad_prl`, `.lck`) — machine-specific; ignored automatically.
- **KiCad backup files** (`.bak`, `-backups/` directories) — local KiCad artefacts; not design content.
- **SPICE simulation output files** (`.raw`, `.op`, `.dc`, `.ac`, `.tran`, `.log`) — source models are committed; simulation run outputs are not.
- **Python virtual environments and caches** (`.venv/`, `__pycache__/`) — tooling, not design content.
- **Documents controlled in other systems** — if a document (e.g. a test report or project specification) is formally controlled in SharePoint or another system, a reference link belongs in `features/<feature>/reviews/external-references.md`, not a copy of the file itself.

If you are unsure whether a file belongs in the repository, ask the lead before committing it.

---

## What happens when a released design changes

A released design must not be modified informally. Once the `release/.../approved` tag exists, that is the authorised design baseline.

If a change is needed — whether a correction, an improvement, or a finding resolution — a new design cycle begins. This follows the same process: branch sequence, checklists, gate sign-offs, and a new release record. Each cycle is separately tagged (e.g. `cdr/.../r2/approved`), so the full history of every design cycle remains available and traceable.

Do not overwrite or silently update a released design. If someone later needs to understand what was built and when, the records need to be there.

---

## If something goes wrong

- **CI check fails** — read the error message on the PR. The most common failures (branch name, PR title, gate checklist items) are quick to fix. `CONTRIBUTING.md` section 6a has step-by-step fixes for every common failure.
- **Gate checklist blocks merge** — open the PR on GitHub, scroll to the PR description, and tick the remaining checklist items by clicking the checkboxes. The check re-runs automatically.
- **KiCad file conflict** — do not attempt to resolve it manually. Speak to the lead. KiCad's file format is not safe to merge by hand; a silently corrupted schematic is worse than a delay.
- **Slash command appears to do nothing** — check that you have write access to the repository. Read-only access is not sufficient to trigger CI commands.
- **Something is unclear** — ask. The repository has detailed documentation in `docs/`, `CONTRIBUTING.md`, and the checklist files. If the documentation does not cover your situation, raise it with the lead rather than improvising.

---

## Why this helps us

In practice, this process addresses problems that hardware teams commonly experience:

- **"Which version was actually built?"** — every release is tagged and its manufacturing outputs are attached to a GitHub Release record.
- **"Why was that decision made?"** — design decision records (DDRs) live alongside the design files, linked to the PR that introduced the change.
- **"Has the schematic been reviewed?"** — the CDR gate record and AI review comment are permanently attached to the PR history.
- **"What changed between builds?"** — the visual diff (`/kicad-diff`) shows exactly what changed, page by page, in a format reviewers can read without opening KiCad.
- **"Who approved this?"** — PR approvals, gate checklist completion, and sign-off records are all captured and do not rely on email threads or memory.
- **Handover** — a new engineer can open the repository and read the design history, requirements, decisions, and review evidence without needing to ask anyone.

---

## Getting started

1. **Read** `docs/setup/kicad-setup.md` and `docs/setup/tool-setup.md` — KiCad installation, library configuration, and GitHub tooling setup.
2. **Clone with submodules** — the shared component library must be checked out at the same time. See `CONTRIBUTING.md` section 1.
3. **Read** `CONTRIBUTING.md` — the full contributor guide. Keep it open for your first few PRs.
4. **Work through** `docs/how-to/worked-example.md` — a complete step-by-step walkthrough from initialising a feature to production release, using GitHub Desktop.
5. **Look at an existing feature** — browse `features/` to see what a real feature directory looks like.
6. **Raise your first `init/` PR** — follow `docs/how-to/init-feature.md` step by step.
7. **Ask if anything is unclear** — the process is more approachable than it first appears.

---

## Key message

> This process is deliberately disciplined, but the aim is to make hardware design easier to review, easier to release, easier to maintain, and easier to understand later — not to create unnecessary admin.
