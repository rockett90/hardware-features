# Bring-Up Review Checklist

> Engineer reference checklist — not auto-posted. Review before first power-on of new hardware.

## Before first power-on

- [ ] Schematic reviewed against PCB — no assembly errors suspected
- [ ] BOM verified against assembled board — correct components in correct positions
- [ ] Polarity of all polarised components verified (electrolytic capacitors, diodes, ICs with orientation markings)
- [ ] Short-circuit test performed on power rails with a multimeter before applying power
- [ ] Current limit set on bench power supply — appropriate for the expected start-up current
- [ ] Test points for key rails identified and accessible
- [ ] Bring-up procedure documented and reviewed before starting

## Power sequencing

- [ ] Power sequencing requirements documented and understood
- [ ] Sequencing is achievable with bench supply setup
- [ ] Any enable pins or soft-start mechanisms understood

## First power-on

- [ ] Apply power with current limit — observe current draw before any other measurement
- [ ] Check all power rails at the correct voltage before enabling downstream circuits
- [ ] Check for unexpected heat — power down immediately if any component is hot to the touch

## Bring-up checklist in repository

- [ ] Bring-up checklist document is in `features/<feature>/bring-up/bring-up-checklist.md`
- [ ] Each step has a clear pass/fail criterion
- [ ] Checklist is committed progressively as steps are completed — not as a single commit at the end
- [ ] Bring-up notes (`bring-up-notes.md`) are being updated with any anomalies

## Circuit modifications

- [ ] Any physical circuit modifications are recorded in `features/<feature>/circuit-mods/` immediately
- [ ] Each modification record includes: date, board serial, description, reason, and schematic update status
