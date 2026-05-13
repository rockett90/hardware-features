# TRR Checklist

> Reference document — the CI-enforced checklist is in `.github/PULL_REQUEST_TEMPLATE/trr-signoff.md`.
> This file is for engineer reference and pre-review preparation.

## Design artefacts

- [ ] ERC clean (zero errors)
- [ ] DRC clean (zero errors)
- [ ] Calculations complete and reviewed
- [ ] Simulations complete and reviewed

## Implementation

- [ ] Stress analysis complete
- [ ] Thermal analysis complete
- [ ] BOM MPNs all confirmed (no TBDs)
- [ ] Bring-up checklist complete and notes committed to `features/<feature>/bring-up/`
- [ ] `production/fptcs/fptcs.yaml` complete — all `[COMPLETE BEFORE TRR]` markers replaced, all TEST-IDs and CAL-IDs have pass/fail criteria, all REQ-IDs linked
- [ ] `production/fptcs/fptcs-notes.md` complete — operator instructions, failure handling, and fixturing documented
- [ ] Circuit mods documented in `features/<feature>/circuit-mods/`

## Verification

- [ ] All TRR-gate verification matrix items marked Verified
- [ ] All REQ-IDs evidenced
- [ ] `features/<feature>/reviews/external-references.md` populated with real SharePoint and IV&V links (or marked N/A with justification)

## Datasheet

- [ ] `datasheet/specs.yaml` complete — all `[COMPLETE BEFORE TRR]` placeholders replaced with real characterised values
- [ ] `datasheet/application-notes.md` complete — typical application, configuration, and layout guidance written
- [ ] Datasheet Markdown and PDF committed and reviewed by lead — values consistent with test results and analysis

## Open findings (re-TRR only — tick N/A if first TRR)

- [ ] All `finding: major` findings resolved — N/A if first TRR
- [ ] All `finding: moderate` findings resolved or formally deferred with lead sign-off — N/A if first TRR

## AI review

- [ ] All CRITICAL findings resolved or explicitly dismissed with reasoning

## Sign-off

- [ ] TRR date recorded
- [ ] Lead name recorded
- [ ] External reference recorded (or marked N/A)

---

> **After merge:** CI automatically creates (or force-updates) the `trr/<feature>/approved` gate tag.
