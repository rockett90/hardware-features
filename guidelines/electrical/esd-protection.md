# ESD Protection

> **Review notice:** This document contains industry-standard best practices. It must be reviewed and approved by the lead engineer before being treated as team-authoritative for this project.

## ESD standards

### IEC 61000-4-2 — Electrostatic Discharge Immunity

The primary standard for ESD immunity testing on equipment. Contact discharge levels:

| Level | Contact discharge voltage | Air discharge voltage |
|---|---|---|
| Level 1 | ±0.5kV | ±2kV |
| Level 2 | ±1kV | ±4kV |
| Level 3 | ±2kV | ±8kV |
| Level 4 | ±4kV | ±15kV |

**Requirement for this project:** All external-facing connector pins must have ESD protection to at minimum **IEC 61000-4-2 Level 3 (±2kV contact discharge, ±8kV air discharge)**.

### IEC 61000-4-5 — Surge Immunity

Surge immunity testing (1.2/50µs voltage, 8/20µs current waveform). Relevant for power inputs and long cable interfaces. Coordinate TVS selection with surge current capability (I_PP).

### JEDEC JS-001 — Human Body Model (HBM)

Component-level ESD classification. A 100pF capacitor discharged through 1.5kΩ into the device under test. All ICs used in this design must be rated HBM Class 2 (±2kV) or better at the pin level.

---

## TVS diode selection

### Unidirectional vs. bidirectional

| Type | Use case |
|---|---|
| **Unidirectional** | Single-polarity signals (power rails, digital signals referenced to GND) |
| **Bidirectional** | AC-coupled signals, signals that can swing both positive and negative |

### Selection criteria

1. **V_RWM (Reverse Working Maximum Voltage):** must exceed the maximum signal voltage under normal operating conditions. For a 3.3V signal: V_RWM ≥ 3.3V — select V_RWM = 5V device.
2. **V_BR (Breakdown voltage):** the voltage at which the TVS begins to conduct. Must be above V_RWM.
3. **V_CL (Clamping voltage):** the peak voltage across the TVS at the specified test current (I_PP). Ensure V_CL is below the absolute maximum input voltage of the protected IC.
4. **I_PP (Peak pulse current):** must exceed the expected surge current (calculated from source impedance and V_CL).
5. **Capacitance:** TVS capacitance adds to the signal line. For high-speed interfaces, use low-capacitance TVS arrays:
   - USB 2.0: C < 1pF per line
   - Ethernet: C < 0.5pF per line (use dedicated Ethernet ESD arrays)
   - SPI / UART at <10MHz: C < 10pF acceptable
   - General I/O at low speed: C < 100pF acceptable

### ESD protection arrays for multi-channel interfaces

For interfaces with multiple signals in close proximity (USB, UART headers, CAN, SPI), use dedicated multi-channel ESD protection arrays rather than individual TVS diodes. This reduces BOM count, improves consistency, and saves PCB space.

---

## Connector protection matrix

| Connector / interface | Minimum ESD device example | Notes |
|---|---|---|
| USB 2.0 | PRTR5V0U2X (Nexperia) or equivalent | Dual-line, C < 1pF/line, V_RWM = 5V |
| CAN bus | NUP2105L (onsemi) or equivalent | Bidirectional, bus-rated V_RWM |
| General I/O header (3.3V/5V) | SP0503BAHTG (Littelfuse) or equivalent | Multi-channel array |
| RS-232 / UART to external connector | Rail-to-rail TVS, V_RWM ≥ supply | |
| Power input (DC jack / screw terminal) | SMAJ series TVS on V+ and TVS on each polarity | Coordinate with protection-circuits.md |
| Ethernet (RJ45) | Integrated magnetics + ESD combo or dedicated ESD array | C < 0.5pF/line |

> **Note:** "Or equivalent" means a device meeting the same V_RWM, I_PP, and capacitance requirements. Footprint equivalence is preferred but not mandatory — if the footprint differs, the PCB layout must accommodate the substitute device. Any substitution must be documented in the BOM with justification comparing the key parameters (V_RWM, V_CL, I_PP, capacitance).

---

## PCB layout rules for ESD protection

### Placement
- ESD protection devices **must be placed as close as possible to the connector pin** — on the same side of the board as the connector, before any series resistors, common-mode filters, ferrite beads, or the protected IC.
- Signal routing order: **Connector → ESD device → (series resistor/filter) → IC**.
- Never route the signal to the IC and loop back to the ESD device — this defeats the protection entirely.

### Guard rings
- High-sensitivity analogue inputs (ADC inputs, op-amp inputs) must have a guard ring connected to the appropriate reference (GND or signal common).
- Guard rings prevent surface leakage currents from coupling into high-impedance nodes.

### GND return path
- The ESD device GND connection must be short and direct to the local GND pour / plane.
- Do not route the ESD return current through a long trace or via chain — this adds inductance which reduces clamping effectiveness during fast ESD events.
- Place a dedicated via from the ESD device GND pad to the ground plane, as close as possible to the device.

### Trace widths
- Traces from connector to ESD device should be ≥0.25mm to handle ESD current without trace damage.
- Traces beyond the ESD device (to the IC) can follow normal signal width rules.

---

## Non-negotiable rules

- **All external-facing connector pins** must have ESD protection rated to minimum IEC 61000-4-2 Level 3 (±2kV contact discharge).
- **ESD device placement** must be before (connector-side of) any series resistors, filters, or the protected IC.
- **V_RWM** of the TVS must exceed the maximum normal signal voltage on the protected line.
- **V_CL** must be below the absolute maximum input voltage of the protected IC.
- **Low-capacitance arrays** must be used for USB, Ethernet, and any signal running above 10MHz.
- **GND return** from ESD device to ground plane must be short and direct.
- **ICs used in this design** must be rated JEDEC HBM Class 2 (±2kV) or better at each pin.
- Any deviation from the connector protection matrix above must be documented and approved in the design review.

---

## Related guidelines

- [Derating](derating.md)
- [Protection Circuits](protection-circuits.md)
- [PCB Design Rules](../pcb/pcb-design-rules.md)
- [EMC Guidelines](../pcb/emc-guidelines.md)
