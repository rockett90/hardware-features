# Company Standards

> **Status notice:** The `guidelines/` files referenced below are currently placeholder documents.
> Apply the general engineering principles described in each section as intent, not as team-ratified
> standards. When a guideline file is completed and reviewed, this notice will be removed for that section.

> This file is loaded automatically by Copilot during AI-assisted reviews. It summarises the non-negotiable engineering standards that apply to every design in this repository.

## Electrical

- All components must be derated per `guidelines/electrical/derating.md`. Key rules: capacitors ≤80% of rated voltage; semiconductors ≤75% of VMAX; resistors ≤70% of rated power at 25°C.
- ESD protection is required on all external-facing signals. Minimum IEC 61000-4-2 Level 3 (±2kV contact discharge). See `guidelines/electrical/esd-protection.md` for TVS selection and layout rules.
- Protection circuits (OVP, OCP, reverse polarity) are mandatory on all external DC power inputs. Soft-start required when bulk capacitance exceeds 47µF. See `guidelines/electrical/protection-circuits.md`.

## PCB

- Minimum trace widths and via rules defined in `guidelines/pcb/pcb-design-rules.md` must be respected. Use IPC-2221 current vs. width table with 10°C rise budget.
- Creepage and clearance must meet IEC 62368-1 for the applicable working voltage and pollution degree. See `guidelines/pcb/creepage-and-clearance.md`.
- All high-speed signals must follow `guidelines/pcb/signal-integrity.md` (impedance control: 50Ω single-ended, 90Ω USB differential, 100Ω Ethernet differential).

## Components

- Only components from the approved vendor list may be used.
- All passives must meet the tolerances specified in `guidelines/components/passive-guidelines.md`.

## Process

- A design review must be completed before layout begins and before release.
- Bring-up must follow `guidelines/process/bring-up-procedure.md`.

---

> **Note:** The guideline files referenced above contain industry-standard best practices based on IEC 62368-1, IPC-2221, IEC 61000-4-2, and JEDEC JS-001. Each file includes a review notice. The lead engineer should confirm project-specific applicability before the first design review.
