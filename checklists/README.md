# checklists

> Review and gate checklists used during the hardware design lifecycle.

---

## What is this directory?

This directory contains Markdown checklists used at different stages of the design process. They serve as structured prompts for reviewers — they are **not** automated gates.

> 💡 Tip: The `post-checklist.yml` workflow posts a short orientation comment on relevant PRs, pointing reviewers to the checklist in the PR description or template — it does not post the full checklist content as a comment.

---

## Structure

| Directory | Contents | When used |
|---|---|---|
| `gates/` | Checklists for formal design gate sign-offs (PDR, CDR, TRR, release) | When raising an `init/<feature>` PR or a `signoff/<feature>/...` PR |
| `review/` | Checklists for general design reviews (schematic, PCB, BOM, bring-up, EMC, FPTCS, stress, thermal, general) | During artifact PR review |
| `library/` | Checklist for adding a new component to the shared library | When raising a `library/<desc>` PR |

---

## Gates (`gates/`)

| File | Purpose |
|---|---|
| `cdr-checklist.md` | Critical Design Review gate checklist |
| `pdr-checklist.md` | Preliminary Design Review gate checklist |
| `trr-checklist.md` | Test Readiness Review gate checklist |
| `release-checklist.md` | Release readiness checklist |

## Review (`review/`)

| File | Purpose |
|---|---|
| `schematic-review.md` | Schematic design review checklist |
| `pcb-review.md` | PCB layout review checklist |
| `bom-review.md` | Bill of Materials review checklist |
| `bring-up-review.md` | Bring-up review checklist |
| `emc-review.md` | EMC review checklist |
| `fptcs-review.md` | Functional performance test case specification review checklist |
| `general-review.md` | General design review checklist |
| `stress-analysis-review.md` | Stress analysis review checklist |
| `thermal-review.md` | Thermal review checklist |

## Library (`library/`)

| File | Purpose |
|---|---|
| `component-addition.md` | Checklist for adding a new component to the shared library |

---

## Important notes

- Checklists are informational prompts — they do not block merge automatically.
- The formal gate **does** block merge: `gate-check.yml` validates that required documents are present on `signoff/` PRs. See [`.github/guidelines/gate-criteria.md`](../.github/guidelines/gate-criteria.md) for what the gate checks.
- Do not delete checklist items without raising a `chore/` PR for discussion.
