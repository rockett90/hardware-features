---
document-version: "1.0"
baseline: PDR
approved-date: "2025-03-01"
approved-by: "Reference Example"
---

# DDR-000 — Design Intent: simple-amplifier

**Date:** 2025-03-01 | **Owner:** Reference Example

## Problem statement

The system requires a fixed-gain voltage amplifier to condition a low-level analogue sensor output (0–500 mV) to a full-scale ADC input range (0–3.3 V). The amplifier must operate from the system 3.3 V single supply, introduce minimal noise, and present a high input impedance to avoid loading the sensor.

## Design approach

A non-inverting op-amp configuration is used. The gain is set by a resistor divider on the inverting input. A rail-to-rail input/output op-amp is selected to maximise dynamic range on the single supply. The gain is fixed at approximately 6.6×, mapping 0–500 mV input to 0–3.3 V output.

## Feature scope

**In scope:**
- Fixed-gain non-inverting amplifier stage
- Input protection resistor
- Output series resistor for driving ADC input capacitance
- Decoupling on the supply pin

**Out of scope:**
- Variable gain
- Anti-aliasing filter (handled upstream)
- ADC interface circuitry

## Constraints and drivers

| Constraint | Value / Description | Source |
|---|---|---|
| Supply voltage | 3.3 V single supply | System power architecture |
| Input range | 0–500 mV | Sensor specification |
| Output range | 0–3.3 V | ADC full-scale input |
| Input impedance | > 100 kΩ | Sensor loading requirement |
| Bandwidth | > 10 kHz | Signal bandwidth requirement |
| PCB area | < 10 × 10 mm | Mechanical constraint |

## Key interfaces

| Interface | Direction | Connected to |
|---|---|---|
| VIN | Input | Sensor output |
| VOUT | Output | ADC input |
| VCC | Power | 3.3 V system rail |
| GND | Power | System ground |
