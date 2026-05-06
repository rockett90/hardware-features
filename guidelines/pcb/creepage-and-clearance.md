# Creepage and Clearance

> **Review notice:** This document contains industry-standard best practices. It must be reviewed and approved by the lead engineer before being treated as team-authoritative for this project.

## Definitions

- **Clearance:** the shortest distance through air between two conductive parts.
- **Creepage:** the shortest distance along the surface of an insulating material between two conductive parts.
- **Working voltage (V_RMS or V_peak):** the highest voltage that can appear between two conductors under normal operating conditions, including normal transients. Use V_peak for DC rails; use V_RMS for AC mains with V_peak = V_RMS × √2 (e.g. 230V_RMS = 325V_peak).
- **Pollution degree (PD):** a measure of the environmental contamination expected during use — affects the required creepage distance.

---

## Pollution degrees

| Pollution degree | Description | Typical environments |
|---|---|---|
| **PD1** | No pollution or only dry, non-conductive pollution | Clean rooms, hermetically sealed equipment |
| **PD2** | Only non-conductive pollution; occasionally temporary condensation | Normal office / home / laboratory environment — **most consumer and industrial products default to PD2** |
| **PD3** | Conductive pollution, or dry non-conductive pollution that may become conductive due to expected condensation | Industrial / outdoor / high-humidity environments |

> **Default assumption:** Use **PD2** unless the product's intended use environment requires PD3. Record the pollution degree assumption in the DDR.

---

## IEC 62368-1 creepage and clearance requirements

Values below are for **basic insulation** at the stated pollution degree. Working voltage is the higher of V_peak (DC) or V_peak (AC).

| Working voltage (V_peak or V_dc) | Clearance (mm) | Creepage — PD2 (mm) |
|---|---|---|
| ≤50V | 0.2 | 0.6 |
| ≤150V | 0.5 | 1.5 |
| ≤300V | 1.5 | 3.0 |
| ≤600V | 3.0 | 6.0 |

### Reinforced insulation
Multiply both clearance and creepage values by **2**:

| Working voltage (V_peak or V_dc) | Clearance — reinforced (mm) | Creepage — PD2, reinforced (mm) |
|---|---|---|
| ≤50V | 0.4 | 1.2 |
| ≤150V | 1.0 | 3.0 |
| ≤300V | 3.0 | 6.0 |
| ≤600V | 6.0 | 12.0 |

> **Supplementary insulation** = same as basic insulation. **Reinforced insulation** = basic + supplementary combined (×2 factor).

---

## How to determine working voltage

1. Identify all pairs of conductors that could have a voltage between them (live-to-neutral, live-to-PE, primary-to-secondary of isolated supply, etc.).
2. For each pair, determine the maximum voltage that can appear under **normal operating conditions** — this includes normal transients (e.g. switching spikes in normal operation) but excludes abnormal fault conditions.
3. For sinusoidal AC mains: working voltage = V_RMS × √2 = V_peak (e.g. 230V_RMS → 325V_peak → use ≥300V row minimum). Non-sinusoidal waveforms must use the actual measured peak voltage.
4. For DC rails: working voltage = V_DC_MAX (including ripple and regulation tolerance).
5. Select the appropriate row from the table. Add margin: always round up to the next table row.

---

## Mains-connected products (230Vac / 115Vac)

**230Vac mains:**
- V_peak = 230 × √2 ≈ 325V
- Minimum row: ≤300V → clearance 1.5mm basic, creepage 3.0mm PD2 basic
- **Recommended minimum with margin:** ≥4mm clearance, ≥6mm creepage (PD2, basic insulation)
- For **reinforced insulation** (live conductors to accessible conductive parts / user-touchable): ≥8mm clearance, ≥12mm creepage

**115Vac mains:**
- V_peak = 115 × √2 ≈ 163V
- Minimum row: ≤150V → clearance 0.5mm basic, creepage 1.5mm PD2 basic
- Recommended with margin: ≥1.5mm clearance, ≥3.0mm creepage (PD2, basic); double for reinforced

> **Important:** These are IEC 62368-1 electrical minimums. Many products are also subject to national regulations (e.g. BS EN 62368-1 in the UK, UL 62368-1 in North America) which may impose additional requirements. Consult the compliance engineer.

---

## Measurement procedure

### Creepage (surface distance)
Measure the shortest path along the surface of the PCB (or other insulating material) between the two conductors. If there is a slot cut in the PCB, the measurement must go down one side of the slot and up the other (the slot does not create air clearance — it creates a longer creepage path).

Steps:
1. Identify both conductors (track edges, pad edges, or exposed metal).
2. Trace the shortest path along the PCB surface, following contours, slots, and grooves.
3. The measured distance must equal or exceed the required creepage value.

### Clearance (through-air distance)
Measure the shortest straight-line distance through air between the two conductors.

Steps:
1. Identify both conductors.
2. If conductors are on the same surface, clearance = distance between nearest edges.
3. If conductors are on opposite sides or in 3D space, measure the shortest through-air straight line.
4. A physical barrier (moulding rib, slot ≥1mm depth) can be used to extend the effective clearance path if needed.

---

## Non-negotiable rules

- **Working voltage** must be calculated for every conductor pair where a potential difference exists; record in the DDR.
- **Pollution degree** must be declared and justified in the DDR before layout begins.
- **Clearance and creepage values** must equal or exceed the IEC 62368-1 table for the declared working voltage and pollution degree.
- **Reinforced insulation** is required wherever a user can touch a conductive part that is separated from live conductors only by that insulation path.
- **Mains-connected designs:** minimum ≥4mm clearance, ≥6mm creepage at PD2 (basic) for 230Vac. Reinforced: ≥8mm clearance, ≥12mm creepage.
- **PCB slots** must be used where the required creepage distance cannot be achieved by conductor spacing alone.
- **Post-layout verification:** creepage and clearance must be measured on the final Gerber files and confirmed before fab release.

---

## Related guidelines

- [PCB Design Rules](pcb-design-rules.md)
- [EMC Guidelines](emc-guidelines.md)
- [Protection Circuits](../electrical/protection-circuits.md)
