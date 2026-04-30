# Review Rubric

> This file is loaded automatically by Copilot during PR reviews to guide the depth and focus of feedback.

## Severity levels

| Level | Label | Meaning |
|---|---|---|
| 1 | `blocking` | Must be resolved before merge. Safety, reliability, or correctness risk. |
| 2 | `major` | Should be resolved before merge. Significant deviation from guidelines. |
| 3 | `minor` | Recommended improvement. Low risk if deferred. |
| 4 | `nit` | Style or consistency. Author's discretion. |

## Review focus areas

1. **Safety** — derating, protection circuits, creepage/clearance
2. **Reliability** — component selection, thermal management, ESD
3. **Signal/power integrity** — routing, decoupling, impedance
4. **EMC** — shielding, filtering, layout
5. **Process compliance** — design review checklist completed, simulation results attached

## What reviewers must check

- Every blocking issue must include a reference to the relevant guideline.
- Simulation results must be present in the PR artifact if required by `guidelines/simulation/design-verification.md`.
