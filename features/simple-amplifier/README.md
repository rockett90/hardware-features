# simple-amplifier

> **Status:** 🔵 In progress — PDR
>
> **📖 Reference example.** This feature is the canonical reference example for this repository. It demonstrates a correctly-populated feature directory at PDR stage. There is no real hardware — it exists so engineers can see what complete content looks like before starting their own feature. See [docs/how-to/worked-example.md](../../docs/how-to/worked-example.md) for the full lifecycle walkthrough.

---

## What is this feature?

The `simple-amplifier` is a fixed-gain non-inverting voltage amplifier. It conditions a low-level analogue sensor output (0–500 mV) to a full-scale ADC input range (0–3.3 V) on a single 3.3 V supply.

The design uses a rail-to-rail op-amp in a non-inverting configuration with a gain of 6.6×. It is intended for use wherever a sensor output needs to be scaled to match an ADC input range without inverting signal polarity and without loading the sensor source.

---

## Gate history

| Gate | Cycle | Date | Tag | Lead |
|---|---|---|---|---|
| PDR | 1 | <!-- date --> | `pdr/simple-amplifier/approved` | <!-- name --> |
| CDR | 1 | <!-- date --> | `cdr/simple-amplifier/approved` | <!-- name --> |
| TRR | 1 | <!-- date --> | `trr/simple-amplifier/approved` | <!-- name --> |
| Release | 1 | <!-- date --> | `release/simple-amplifier/approved` | <!-- name --> |

---

## Key design decisions

<!-- Link to DDR files in decisions/ — one line each with a brief summary of the decision. -->

- [DDR-000 — Design intent](decisions/DDR-000-design-intent.md) — problem statement, scope, and constraints
- [DDR-000 — Decisions](decisions/DDR-000-decisions.md) — op-amp selection, topology, gain setting

---

## Requirements and verification

| Document | Description |
|---|---|
| [Feature requirements](requirements/feature-requirements.yaml) | Functional requirements — what this feature must do |
| [Interface requirements](requirements/interface-requirements.yaml) | Interface definitions — connectors, voltages, signals |
| [Verification matrix](requirements/verification-matrix.md) | REQ-ID to evidence mapping |

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

<!-- Add links to external systems here. Examples below — replace or remove as needed. -->

| System | Link | Contents |
|---|---|---|
| Project tracking | <!-- Jira epic URL --> | Sprint board, backlog |
| Requirements / spec | <!-- SharePoint or Confluence URL --> | System-level requirements |
| Test plans / reports | <!-- SharePoint folder URL --> | IVV test plans and results |
| Supplier correspondence | <!-- SharePoint folder URL --> | Quotes, NDA, lead time |
| Reference datasheets | <!-- SharePoint folder URL --> | Component datasheets |

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
| Feature lead | Reference Example |
| Backup | — |
