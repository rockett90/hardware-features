## Critical Design Review (CDR) Sign-Off

**Feature:**
**Revision:**
**CDR date:**
**Lead:**
**External reference (if applicable):**

---

## Artefacts

<!-- 
  Before ticking the artefact items below, work through the relevant review checklists:
  - Schematic: checklists/review/schematic-review.md
  - PCB: checklists/review/pcb-review.md
  - BOM: checklists/review/bom-review.md
  - Thermal / stress: checklists/review/thermal-review.md, checklists/review/stress-analysis-review.md
  These checklists are engineer reference documents — they are not auto-posted to this PR.
-->

- [ ] ERC clean (zero errors, zero warnings unless formally accepted)
- [ ] Calculations complete and reviewed
- [ ] Simulations complete and reviewed
- [ ] PCB reviewed
- [ ] BOM has no TBDs
- [ ] MTBF confirmed

## Design Quality

- [ ] All components derated per derating guidelines
- [ ] ESD protection in place on all external-facing signals
- [ ] Protection circuits reviewed (OVP, OCP, reverse polarity)
- [ ] PCB design rules met
- [ ] Creepage and clearance checked against IEC 62368 for working voltage

## Requirements

- [ ] Verification matrix CDR-gate column complete
- [ ] All REQ-IDs have evidence or a documented plan

## Decisions

- [ ] DDR-000 complete and reviewed

## AI Review

- [ ] All CRITICAL findings resolved or explicitly dismissed with reasoning

## Linked artefact PRs

<!-- List the artifact PR numbers that form the CDR baseline, e.g. #12, #15, #18 -->

## Sign-off

- [ ] CDR date recorded above
- [ ] Lead name recorded above
- [ ] External reference recorded above (or marked N/A)

---

> ⚠️ CI will block merge until all checklist items above are ticked.
> Every item must be checked — items may not be deleted from this list.
> If an item does not apply, tick it and add a note in the linked artefact PR or below.

<!-- Notes -->
