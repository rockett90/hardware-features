# PCB Design Rules

> **Review notice:** This document contains industry-standard best practices. It must be reviewed and approved by the lead engineer before being treated as team-authoritative for this project.

## Minimum track widths by current (IPC-2221)

The table below gives minimum track widths for external copper layers (1oz copper, 35µm) with a 10°C temperature rise budget above ambient, per IPC-2221.

| Current (A) | Min. width — external layer, 1oz Cu (mm) | Min. width — internal layer, 1oz Cu (mm) |
|---|---|---|
| 0.5 | 0.25 | 0.35 |
| 1 | 0.50 | 0.70 |
| 2 | 0.90 | 1.26 |
| 3 | 1.20 | 1.68 |
| 5 | 2.00 | 2.80 |
| 10 | 3.50 | 4.90 |

> **Internal layer note:** Internal layers have less convective cooling. Use approximately **1.4× the external layer width** for the same temperature rise on an internal layer. Values in the table above are pre-calculated at 1.4×.

> **Derating reminder:** These widths assume 10°C rise and clean, flat traces. For elevated ambient temperatures, high-density boards, or partially covered traces, apply additional margin. See `guidelines/electrical/derating.md`.

---

## Clearance rules

### Low-voltage signals and power (≤50V)
- Minimum clearance between any two conductors: **0.15mm** (conductor edge to conductor edge).
- This applies to signal tracks, power tracks, pads, and copper pours.

### Higher voltages
- For working voltages above 50V, clearance must meet **IEC 62368-1**. Cross-reference `creepage-and-clearance.md`.

### Mains-connected designs
Per IEC 62368-1 for 230Vac (325Vpeak):

| Insulation type | Minimum clearance |
|---|---|
| Basic insulation | ≥4mm |
| Reinforced insulation | ≥8mm |

> **Warning:** Mains-connected PCBs require a formal creepage and clearance review against the applicable IEC 62368-1 table before layout sign-off. See `creepage-and-clearance.md`.

---

## Via sizes

| Via type | Min. drill diameter (mm) | Min. pad diameter (mm) | Notes |
|---|---|---|---|
| Signal via | 0.2 | 0.4 | Standard signal routing |
| Power via | 0.4 | 0.8 | Use multiple vias in parallel for high current |
| Thermal via | 0.3 | 0.6 | Array under power components; see thermal via section |
| Press-fit / through-hole | Per component datasheet | Per IPC-7251 | |

### Thermal vias
- Use an array of **0.3mm drill / 0.6mm pad** vias under power components dissipating >0.5W (e.g. buck converter, linear regulator, power FET) to transfer heat to internal copper layers or the opposite-side copper pour.
- Via array pitch: 0.6–0.8mm centre-to-centre.
- Fill thermal vias with conductive or non-conductive epoxy if component is soldered to exposed pad — unfilled vias cause solder wicking in reflow.
- Apply thermal relief to power pads on through-hole components (4-spoke, 0.25mm spoke width) for wave soldering; solid connection preferred for SMD power components in reflow.

---

## Copper pours

- **Ground pour on all layers:** every layer should have a GND copper pour to minimise impedance and provide a return path close to every signal trace.
- **Stitching vias:** connect GND pours on adjacent layers with vias every ≤5mm in power areas, and at least every 10mm elsewhere. This prevents resonant cavities at high frequencies.
- **Pour clearance:** maintain 0.3mm clearance from the pour edge to all tracks, pads, and other copper features.
- **No orphaned copper islands:** every island of copper must be connected to the net it is assigned to, or removed. Floating copper causes manufacturing uncertainty and potential ESD charging.
- **Pour connection:** use solid fill for GND/power pours; thermal relief spokes are acceptable on through-hole component pads only.

---

## Impedance control

Controlled impedance traces must be specified on the fabrication drawing with the target impedance class.

| Signal type | Target impedance | Notes |
|---|---|---|
| RF / general single-ended | 50Ω | Microstrip or stripline |
| USB 2.0 differential pair | 90Ω differential | Route as matched-length pair |
| Ethernet (100BASE-TX) | 100Ω differential | Route as matched-length pair through magnetics |
| High-speed single-ended (SPI, LVDS) | 50Ω | |

### Reference layer requirements
- The reference layer (GND or power) **must be continuous and unbroken** under all controlled-impedance tracks.
- Do not route controlled-impedance tracks across plane splits, slots, or gaps in the reference layer.
- Indicate reference layers on the fabrication drawing.

### Specifying on fab drawing
- Include a note such as: "Controlled impedance: 50Ω ±10% single-ended (Class 1), 90Ω ±10% differential (Class 2). Stackup as specified. Test coupon required."
- Confirm the board manufacturer's stackup against the impedance model used in the layout tool before ordering.

---

## Silkscreen

- All components must have a **visible reference designator** on the silkscreen layer.
- Minimum text height: **0.8mm** for reference designators and component values.
- Do **not** place silkscreen text or lines over exposed copper (pads, vias, test points). Silkscreen ink on copper causes solderability issues.
- Silkscreen must not overlap onto adjacent component landing areas.
- Pin 1 indicators must be visible for all ICs and polarised components.

---

## Non-negotiable rules

- Track widths must meet or exceed the IPC-2221 table values for the applicable current and layer — no exceptions.
- Internal layer tracks must use 1.4× the external layer minimum width.
- Minimum clearance between conductors: 0.15mm at ≤50V; comply with IEC 62368-1 above 50V.
- Mains-isolated designs: ≥4mm clearance (basic), ≥8mm clearance (reinforced) — see `creepage-and-clearance.md`.
- Signal vias: minimum 0.2mm drill / 0.4mm pad; power vias: minimum 0.4mm drill / 0.8mm pad.
- Thermal vias required under any power component dissipating >0.5W.
- GND copper pour required on all layers; stitched with vias every ≤5mm in power areas.
- No orphaned copper islands.
- Controlled impedance reference layer must be unbroken under the controlled impedance track.
- All component reference designators must appear on silkscreen with minimum 0.8mm text height.
- No silkscreen over exposed copper.

---

## Related guidelines

- [Creepage and Clearance](creepage-and-clearance.md)
- [Component Placement](component-placement.md)
- [Signal Integrity](signal-integrity.md)
- [Power Integrity](power-integrity.md)
- [Derating](../electrical/derating.md)
