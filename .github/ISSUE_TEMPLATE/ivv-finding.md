---
name: IVV Finding
about: Record an independent verification and validation finding against a hardware feature
title: 'IVV Finding — [feature-name]: [brief description]'
labels: ''
assignees: ''
---

## Finding details

**Feature:**
**Severity:** <!-- Minor / Moderate / Major — lead confirms label after submission -->
**Found by:**
**Date found:**
**TRR gate tag:** <!-- e.g. trr/<feature>/approved -->

---

## Description

<!-- Clear description of the finding. What is wrong? -->

---

## Expected behaviour

<!-- What should happen? Reference the relevant REQ-ID if applicable. -->

---

## Observed behaviour

<!-- What actually happens? Include measurements, screenshots, or test results where relevant. -->

---

## Affected artefacts

<!-- List the files, schematics, PCB layers, or documents that are affected. -->

---

## Requirements affected

<!-- List any REQ-IDs that this finding impacts. -->
<!-- Example: REQ-001, REQ-004 -->

---

## Gate re-entry required

- [ ] None — minor correction only, no gate re-entry (lead must confirm)
- [ ] Re-TRR required — moderate finding
- [ ] Re-CDR then re-TRR required — major finding

---

## Notes

<!-- Any additional context, measurements, photographs, or links. -->

<!-- -----------------------------------------------------------------------
PROCESS NOTES (not visible in rendered issue)

- The lead will confirm the severity label after submission.
- The engineer picks up this finding by creating a `finding/<feature>/<N>-<desc>`
  branch where N is this issue number.
- The PR must include `Resolves #N` in the description body.
- See CONTRIBUTING.md section 12 for the full IVV finding workflow.
----------------------------------------------------------------------- -->
