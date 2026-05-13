---
document-version: "1.0"
baseline: PDR
approved-date: "2025-03-01"
approved-by: "Reference Example"
---

# DDR-000 — Design Decisions: simple-amplifier

**Date:** 2025-03-01 | **Owner:** Reference Example

## Decision log

| ID | Decision | Rationale | Alternatives considered | Date |
|---|---|---|---|---|
| DEC-001 | Use non-inverting topology | Preserves signal polarity; high input impedance avoids sensor loading | Inverting (rejected — inverts polarity, lower input impedance) | 2025-03-01 |
| DEC-002 | Select OPA2134 op-amp | Low noise (8 nV/√Hz), rail-to-rail I/O on 3.3 V, available in SOIC-8, known to library | MCP6001 (rejected — higher noise), LM358 (rejected — not rail-to-rail on 3.3 V) | 2025-03-01 |
| DEC-003 | Set gain to 6.6× using 56 kΩ / 10 kΩ resistor divider | Maps 0–500 mV to 0–3.3 V; E96 values, 0.1% tolerance for accuracy | Gain of 7× (rejected — over-ranges ADC at 500 mV input) | 2025-03-01 |
| DEC-004 | Add 100 Ω series output resistor | Protects op-amp from ADC input capacitance; negligible effect on bandwidth at 10 kHz | No output resistor (rejected — op-amp may oscillate driving capacitive ADC input) | 2025-03-01 |
