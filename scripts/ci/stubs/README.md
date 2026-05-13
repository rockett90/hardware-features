# FEATURE_NAME

> **Status:** 🔵 In progress — PDR

---

## What is this feature?

<!-- Describe the purpose and function of this feature in 1–3 paragraphs.
     What problem does it solve? Where does it fit in the wider system?
     Written for someone picking this up for the first time. -->

[COMPLETE AT PDR]

---

## Gate history

| Gate | Cycle | Date | Tag | Owner |
|---|---|---|---|---|
| PDR | 1 | <!-- date --> | `pdr/FEATURE_NAME/approved` | <!-- name --> |
| CDR | 1 | <!-- date --> | `cdr/FEATURE_NAME/approved` | <!-- name --> |
| TRR | 1 | <!-- date --> | `FEATURE_NAME-vX.Y.Z-rc.N` | <!-- name --> |
| Release | 1 | <!-- date --> | `release/FEATURE_NAME/approved` | <!-- name --> |

---

## Key design decisions

<!-- Link to DDR files in decisions/ — one line each with a brief summary of the decision. -->

- [DDR-000 — Design intent](decisions/DDR-000-design-intent.md)
- [DDR-000 — Engineering decisions log](decisions/DDR-000-decisions.md)

---

## Requirements and verification

| Document | Description |
|---|---|
| [Feature requirements](requirements/feature-requirements.yaml) | Functional requirements — what this feature must do |
| [Interface requirements](requirements/interface-requirements.yaml) | Interface definitions — connectors, voltages, signals |
| [Verification matrix](requirements/verification-matrix.md) | REQ-ID to evidence mapping |
| [FPTCS](production/fptcs/fptcs.yaml) | Feature Production Test and Calibration Specification — test items, calibration steps, pass/fail criteria |

---

## Datasheet

The feature datasheet (for integration team handover) lives in [`datasheet/`](datasheet/).
It is generated from [`datasheet/specs.yaml`](datasheet/specs.yaml) using the `/datasheet` slash command.

| Document | Description |
|---|---|
| [specs.yaml](datasheet/specs.yaml) | Characterised performance — actual min/nom/max values |
| [application-notes.md](datasheet/application-notes.md) | Application guidance for integration engineers |
| [errata.md](datasheet/errata.md) | Known issues against specific hardware revisions |

---

## External links

<!-- 
  Populate this table with links to external project systems at PDR.
  SharePoint folder structure may change — update these links if they become stale.
  Use N/A for rows that do not apply to this feature.
  Formal design review minutes and sign-off records should be stored in SharePoint
  and linked here — they are not committed to the repository.
-->

| System | Link | Contents |
|---|---|---|
| Project tracking | <!-- Jira epic URL --> | Sprint board, backlog |
| Requirements / spec | <!-- SharePoint or Confluence URL --> | System-level requirements |
| Test plans / reports | <!-- SharePoint folder URL --> | IVV test plans and results |
| Supplier correspondence | <!-- SharePoint folder URL --> | Quotes, NDA, lead time |
| Reference datasheets | <!-- SharePoint folder URL --> | Component datasheets |
| Design review records | <!-- SharePoint folder URL --> | Review minutes and sign-off records |

---

## Open issues and risks

<!-- Link to open finding/ PRs or Jira tickets. Remove this section when there are none. -->

| ID | Description | Severity | Status |
|---|---|---|---|
| — | — | — | — |

---

## Contacts

| Role | Name |
|---|---|
| Feature owner | <!-- name --> |
| Backup | <!-- name --> |
