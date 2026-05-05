# .github/agents

> Instruction files for GitHub Copilot coding agents working in this repository.

---

## What is this directory?

This directory contains instruction files that tell Copilot coding agents how to behave when working in this repository. The files define:

- Coding conventions and patterns to follow
- Patterns to avoid
- Which tools to use and how to structure PRs
- Repository-specific context (standards, schemas, review rubrics)

Engineers do not need to read or edit these files in normal day-to-day work. They are consumed automatically by the agent.

---

## Structure

| Path | Contents |
|---|---|
| `context/` | Background context files the agent reads to understand this repository's standards |
| `instructions/` | Task-specific instruction files for common agent-driven operations |

### `context/`

| File | Purpose |
|---|---|
| `company-standards.md` | Design and engineering standards applied during AI review |
| `requirements-schema.md` | Schema and conventions for requirements YAML files |
| `review-rubric.md` | Scoring rubric used by the AI review workflow |

### `instructions/`

| File | Purpose |
|---|---|
| `bom-review.md` | Instructions for AI-assisted BOM review |
| `datasheet-generation.md` | Instructions for generating datasheet summaries |
| `doe-generation.md` | Instructions for generating design-of-experiments documents |
| `fptcs-generation.md` | Instructions for generating functional performance test case specifications |
| `mtbf-generation.md` | Instructions for generating MTBF analysis documents |
| `schematic-review.md` | Instructions for AI schematic review (used by `ai-review.yml`) |
| `stress-generation.md` | Instructions for generating component stress analysis documents |

---

## Editing these files

Changes to agent instructions affect the behaviour of all future agent-assisted operations in this repository.

- Raise a `chore/` PR with lead approval for any changes.
- After updating `context/company-standards.md`, verify that `ai-review.yml` still produces sensible output on a known-good schematic.

> ⚠️ Warning: Removing a file from `context/` will silently reduce the quality of AI review output — the agent will no longer apply those standards without any error or warning.
