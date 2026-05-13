# PDR Checklist

> Reference document — the authoritative PDR checklist is embedded in the init PR body template (`.github/PULL_REQUEST_TEMPLATE/init.md`), which is pre-filled when a `signoff/<feature>/pdr` or `init/<feature>` PR is opened. This file is a standalone reference copy.

## Scope and requirements

- [ ] Feature name is descriptive and follows the naming convention (lowercase, hyphens, no spaces)
- [ ] `requirements/feature-requirements.yaml` contains real REQ-IDs (not just stub placeholder text)
- [ ] `requirements/interface-requirements.yaml` contains real interface definitions with voltage, current, and signal levels
- [ ] `requirements/verification-matrix.md` lists all REQ-IDs with a verification method for each

## Design intent

- [ ] `decisions/DDR-000-design-intent.md` and `decisions/DDR-000-decisions.md` contain real content — problem statement, design approach, key decisions (not stub text)
- [ ] Feature scope is clearly bounded — what this feature does and what it does not do

## Feature README

- [ ] `README.md` intent paragraph describes what this feature does and where it fits in the wider system
- [ ] External links section updated with Jira, SharePoint, or other relevant project links (or explicitly marked N/A)
- [ ] Contacts section populated with feature lead name

## Repository configuration

- [ ] Feature scope added to `commitlint.config.js` so PR titles with this feature's scope are valid
- [ ] Feature package added to `.github/release-please-config.json` so release automation works for this feature

## Sign-off

- [ ] PDR date recorded below
- [ ] Lead name recorded below

---

> ⚠️ CI will block merge until all checklist items above are ticked.
> Every item must be checked — items may not be deleted from this list.
> If an item does not apply, tick it and add a note below.

<!-- PDR date: -->
<!-- Lead: -->
<!-- Notes: -->
