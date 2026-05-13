# CDR Checklist

> Reference document — the CI-enforced checklist is in `.github/PULL_REQUEST_TEMPLATE/cdr-signoff.md`.
> This file is for engineer reference and pre-review preparation.

## Artefacts

- [ ] ERC clean (zero errors, zero warnings unless formally accepted and documented)
- [ ] Calculations complete and reviewed
- [ ] Simulations complete and reviewed (where applicable)
- [ ] PCB reviewed
- [ ] BOM has no TBDs — all MPNs specified
- [ ] FPTCS draft present in `features/<feature>/production/fptcs/` — test points defined for all interfaces and all functional requirements
- [ ] MTBF confirmed

## Design quality

- [ ] All components derated per derating guidelines
- [ ] ESD protection in place on all external-facing signals
- [ ] Protection circuits reviewed (OVP, OCP, reverse polarity)
- [ ] PCB design rules met
- [ ] Creepage and clearance checked against IEC 62368 for working voltage

## Requirements

- [ ] Verification matrix CDR-gate column complete
- [ ] All REQ-IDs have evidence or a documented plan
- [ ] DDR-000 complete and reviewed

## AI review

- [ ] All CRITICAL findings resolved or explicitly dismissed with reasoning

## Sign-off

- [ ] CDR date recorded
- [ ] Lead name recorded
- [ ] External reference recorded (or marked N/A)

---

> **After merge:** CI automatically creates the `cdr/<feature>/approved` gate tag and commits `features/<feature>/reviews/library.lock` recording the library submodule commit at this gate.
