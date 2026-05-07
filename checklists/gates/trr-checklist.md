# TRR Checklist

> Posted automatically when a TRR sign-off PR opens.

## Design Artifacts
- [ ] ERC clean (zero errors)
- [ ] DRC clean (zero errors)
- [ ] Calculations complete and reviewed
- [ ] Simulations complete and reviewed

## Implementation
- [ ] Stress analysis complete
- [ ] Thermal analysis complete
- [ ] BOM MPNs all confirmed
- [ ] Bring-up checklist complete
- [ ] Bring-up notes committed
- [ ] FPTCS complete
- [ ] Circuit mods documented

## Verification
- [ ] All TRR-gate items Verified
- [ ] All REQ-IDs evidenced

## Datasheet

- [ ] `datasheet/specs.yaml` complete — all `[COMPLETE BEFORE TRR]` placeholders replaced with real values
- [ ] `datasheet/application-notes.md` complete — typical application, configuration, and layout guidance written
- [ ] `datasheet/<feature>-datasheet.md` committed and up to date — run `/datasheet` to regenerate if needed
- [ ] Datasheet reviewed by lead — values consistent with test results and analysis

## Open Findings for re-TRR
> Only relevant for re-TRR PRs
- [ ] All P1 findings resolved
- [ ] All P2 findings resolved or formally deferred

## AI Review
- [ ] All critical findings resolved or dismissed with reasoning

## Sign-off
- [ ] TRR date recorded
- [ ] Lead name recorded
- [ ] External reference recorded
