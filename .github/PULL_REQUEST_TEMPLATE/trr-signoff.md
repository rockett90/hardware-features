## Test Readiness Review (TRR) Sign-Off

**Feature:**
**Revision:**
**TRR date:**
**Lead:**
**External reference (if applicable):**
**Re-TRR number (if applicable — leave blank for first TRR):**

---

## Design Artefacts

<!-- 
  Before ticking the artefact items below, work through the relevant review checklists:
  - Schematic: checklists/review/schematic-review.md
  - PCB: checklists/review/pcb-review.md
  - BOM: checklists/review/bom-review.md
  - Bring-up: checklists/review/bring-up-review.md
  - Thermal: checklists/review/thermal-review.md
  - Stress: checklists/review/stress-analysis-review.md
  - FPTCS: checklists/review/fptcs-review.md
  - EMC: checklists/review/emc-review.md
  These checklists are engineer reference documents — they are not auto-posted to this PR.
-->

- [ ] ERC clean (zero errors)
- [ ] DRC clean (zero errors)
- [ ] Calculations complete and reviewed
- [ ] Simulations complete and reviewed

## Implementation

- [ ] Stress analysis complete
- [ ] Thermal analysis complete
- [ ] BOM MPNs all confirmed (no TBDs)
- [ ] Bring-up checklist complete
- [ ] Bring-up notes committed to `features/<feature>/bring-up/`
- [ ] `production/fptcs/fptcs.yaml` complete — all `[COMPLETE BEFORE TRR]` markers replaced, all TEST-IDs and CAL-IDs have pass/fail criteria, all REQ-IDs linked
- [ ] `production/fptcs/fptcs-notes.md` complete — operator instructions, failure handling, and fixturing documented
- [ ] Circuit mods documented in `features/<feature>/circuit-mods/`

## Verification

- [ ] All TRR-gate verification matrix items marked Verified
- [ ] All REQ-IDs evidenced
- [ ] `features/<feature>/reviews/external-references.md` populated with real SharePoint and IV&V links (or marked N/A with justification)

## Open Findings (re-TRR only — tick N/A if first TRR)

- [ ] All major findings resolved — N/A if first TRR
- [ ] All moderate findings resolved or formally deferred with lead sign-off — N/A if first TRR

## AI Review

- [ ] All CRITICAL findings resolved or explicitly dismissed with reasoning

## Linked PRs

<!-- List the finding PRs resolved since the previous TRR (if re-TRR), or the CDR baseline PRs (if first TRR) -->

## Sign-off

- [ ] TRR date recorded above
- [ ] Lead name recorded above
- [ ] External reference recorded above (or marked N/A)

---

> ⚠️ CI will block merge until all checklist items above are ticked.
> Every item must be checked — items may not be deleted from this list.
> If an item does not apply, tick it and add a note below.

<!-- Notes -->
