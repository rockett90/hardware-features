# FPTCS Review Checklist

> Engineer reference checklist — not auto-posted. Consult when reviewing the Feature Product Test and Calibration Specification (FPTCS) before TRR.

## Coverage

- [ ] Every functional requirement in `feature-requirements.yaml` is addressed by at least one test
- [ ] Every interface parameter in `interface-requirements.yaml` is tested at its limit values
- [ ] All calibration steps are documented with tolerances
- [ ] Power-on self-test requirements captured where applicable

## Test steps

- [ ] Each test step has unambiguous pass/fail criteria
- [ ] Test steps are in a logical order — no step depends on a later step's result
- [ ] Any required test equipment is specified with acceptable substitutes noted
- [ ] Any required calibrated equipment is identified

## Calibration

- [ ] Calibration procedure is separate from functional test where applicable
- [ ] Calibration tolerance is consistent with the requirements
- [ ] Calibration constants or trim values are stored in a defined location (EEPROM, test record, label)

## Production suitability

- [ ] Test time per unit estimated and acceptable for production rate
- [ ] Test fixturing requirements documented
- [ ] Any manual steps that are error-prone have been flagged for review
- [ ] Failure modes and operator responses defined for each failure type

## Traceability

- [ ] FPTCS references the REQ-IDs it covers
- [ ] FPTCS version is recorded
- [ ] FPTCS review is documented — who reviewed, what version, what date
