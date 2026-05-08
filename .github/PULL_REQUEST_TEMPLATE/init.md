## Preliminary Design Review (PDR) — Feature Init

**Feature name:**
**PDR date:**
**Owner:**

---

## Scope and requirements

- [ ] Feature name is descriptive and follows the naming convention (lowercase, hyphens, no spaces)
- [ ] `requirements/feature-requirements.yaml` contains real REQ-IDs (not just stub placeholder text)
- [ ] `requirements/interface-requirements.yaml` contains real interface definitions with voltage, current, and signal levels
- [ ] `requirements/verification-matrix.md` lists all REQ-IDs with a verification method for each
- [ ] `document-version` and `baseline` fields populated in `feature-requirements.yaml`, `interface-requirements.yaml`, `verification-matrix.md`, `DDR-000-design-intent.md`, and `DDR-000-decisions.md`

## Design intent

- [ ] `decisions/DDR-000-design-intent.md` contains real content — problem statement, design approach, feature scope, and constraints (not stub text)
- [ ] Feature scope is clearly bounded — what this feature does and what it explicitly does not do

## Engineering decisions

- [ ] `decisions/DDR-000-decisions.md` has at least one decision entry — even if only the initial topology or approach decision
- [ ] Each decision entry has a rationale and alternatives considered

## Repository configuration

- [ ] Feature scope added to `commitlint.config.js` so PR titles with this feature's scope are valid
- [ ] Feature package added to `.github/release-please-config.json` so release automation works for this feature

## Scaffolded files

- [ ] KiCad project files are present in `features/<feature>/` and `features/<feature>/pcb/`
- [ ] `features/<feature>/README.md` stub is present
- [ ] Datasheet stubs are present in `features/<feature>/datasheet/`

## Sign-off

- [ ] PDR date recorded above
- [ ] Owner name recorded above

---

> ⚠️ CI will block merge until all checklist items above are ticked.
> Every item must be checked — items may not be deleted from this list.
> If an item does not apply, tick it and add a note below.

## Feature overview

<!-- Briefly describe what this feature is, what problem it solves, and its key interfaces -->

## Key design decisions (summary)

<!-- Summarise the main design choices captured in DDR-000-design-intent.md and DDR-000-decisions.md -->

## Linked requirements

<!-- List the top-level REQ-IDs from feature-requirements.yaml, e.g. REQ-001, REQ-002 -->

<!-- Notes -->
