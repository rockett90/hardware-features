# guidelines

> Engineering and design guidelines organised by discipline — referenced during design review and by the AI review agent.

---

## What is this directory?

This directory contains engineering guidelines for hardware development. They supplement the process described in `CONTRIBUTING.md` and define the standards that designs are expected to meet.

> 💡 Tip: For CI and AI tooling guidelines (schematic standards, BOM standards, gate criteria), see [`.github/guidelines/`](../.github/guidelines/README.md) instead. That directory contains guidelines consumed directly by workflows and the AI review agent.

---

## Structure

| Directory | Contents |
|---|---|
| `electrical/` | Electrical design guidelines — derating, protection circuits, grounding, ESD |
| `pcb/` | PCB layout guidelines — design rules, component placement, signal and power integrity, EMC, thermal management |
| `components/` | Component selection guidelines — selection criteria, connector rules, passive guidelines, thermal derating |
| `simulation/` | Simulation guidelines — SPICE usage, design verification |
| `process/` | Process guidelines — bring-up procedure, design review process |

---

## Electrical (`electrical/`)

| File | Contents |
|---|---|
| `derating.md` | Voltage and temperature derating rules |
| `esd-protection.md` | ESD protection design requirements |
| `grounding-and-shielding.md` | Grounding and shielding guidelines |
| `protection-circuits.md` | Overcurrent, overvoltage, and reverse polarity protection |

## PCB (`pcb/`)

| File | Contents |
|---|---|
| `pcb-design-rules.md` | Track widths, clearances, via rules |
| `component-placement.md` | Component placement conventions |
| `signal-integrity.md` | Signal integrity guidelines |
| `power-integrity.md` | Power distribution and decoupling guidelines |
| `emc-guidelines.md` | EMC design guidelines |
| `thermal-management.md` | Thermal management guidelines |
| `creepage-and-clearance.md` | Creepage and clearance requirements |

## Components (`components/`)

| File | Contents |
|---|---|
| `component-selection.md` | How to select components — approved sources, preferred parts |
| `connector-selection.md` | Connector selection and mating requirements |
| `passive-guidelines.md` | Resistor, capacitor, and inductor selection |
| `thermal-derating.md` | Thermal derating requirements for components |

## Simulation (`simulation/`)

| File | Contents |
|---|---|
| `spice-guidelines.md` | SPICE simulation conventions and file organisation |
| `design-verification.md` | Simulation-based design verification requirements |

## Process (`process/`)

| File | Contents |
|---|---|
| `bring-up-procedure.md` | Standard bring-up procedure for new hardware |
| `design-review-process.md` | Design review process — roles, inputs, outputs, criteria |

---

## Adding or updating a guideline

1. Raise a `chore/` PR with the new or updated content.
2. Once the guideline is complete, consider adding it to `.github/agents/context/company-standards.md` so it is applied automatically during AI review.

