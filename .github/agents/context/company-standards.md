# Company Standards

> **Status notice:** The `guidelines/` files referenced below are currently placeholder documents.
> Apply the general engineering principles described in each section as intent, not as team-ratified
> standards. When a guideline file is completed and reviewed, this notice will be removed for that section.

> This file is loaded automatically by Copilot during AI-assisted reviews. It summarises the non-negotiable engineering standards that apply to every design in this repository.

## Electrical

- All components must be derated per `guidelines/electrical/derating.md`.
- ESD protection is required on all external-facing signals.
- Protection circuits (OVP, OCP, reverse polarity) are mandatory on all power inputs.

## PCB

- Minimum trace/space and via rules defined in `guidelines/pcb/pcb-design-rules.md` must be respected.
- Creepage and clearance must meet IEC 62368 for the applicable working voltage.
- All high-speed signals must follow `guidelines/pcb/signal-integrity.md`.

## Components

- Only components from the approved vendor list may be used.
- All passives must meet the tolerances specified in `guidelines/components/passive-guidelines.md`.

## Process

- A design review must be completed before layout begins and before release.
- Bring-up must follow `guidelines/process/bring-up-procedure.md`.
