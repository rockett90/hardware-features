# checklists

> Review and gate checklists used during the hardware design lifecycle.

---

## What is this directory?

This directory contains Markdown checklists used at different stages of the design process. They serve as structured prompts for reviewers — they are **not** automated gates.

> 💡 Tip: The `post-checklist.yml` workflow automatically posts the appropriate checklist as a PR comment when a PR is opened or converted from draft, so reviewers see the relevant checklist without having to find it manually.

---

## Structure

| Directory | Contents | When used |
|---|---|---|
| `gates/` | Checklists for formal design gate sign-offs (CDR, TRR, release) | When raising a `signoff/<feature>/cdr` or `signoff/<feature>/trr` PR |
| `review/` | Checklists for general design reviews (schematic, PCB, BOM, general) | During artifact PR review |
| `library/` | Checklist for adding a new component to the shared library | When raising a `library/<desc>` PR |

---

## Gates (`gates/`)

| File | Purpose |
|---|---|
| `cdr-checklist.md` | Critical Design Review gate checklist |
| `trr-checklist.md` | Test Readiness Review gate checklist |
| `release-checklist.md` | Release readiness checklist |

## Review (`review/`)

| File | Purpose |
|---|---|
| `schematic-review.md` | Schematic design review checklist |
| `pcb-review.md` | PCB layout review checklist |
| `bom-review.md` | Bill of Materials review checklist |
| `general-review.md` | General design review checklist |

## Library (`library/`)

| File | Purpose |
|---|---|
| `component-addition.md` | Checklist for adding a new component to the shared library |

---

## Important notes

- Checklists are informational prompts — they do not block merge automatically.
- The formal gate **does** block merge: `gate-check.yml` validates that required documents are present on `signoff/` PRs. See [`.github/guidelines/gate-criteria.md`](../.github/guidelines/gate-criteria.md) for what the gate checks.
- Do not delete checklist items without raising a `chore/` PR for discussion.
