# Derating

> **Review notice:** This document contains industry-standard best practices. It must be reviewed and approved by the lead engineer before being treated as team-authoritative for this project.

## What is derating and why is it required?

Derating is the practice of operating a component below its rated maximum to improve long-term reliability. The Arrhenius model demonstrates that failure rate increases exponentially with temperature; the same relationship applies to voltage and current stress. By reducing stress, mean time between failures (MTBF) increases significantly.

The rule of thumb from MIL-HDBK-217 and similar reliability handbooks is that every 10°C reduction in junction temperature roughly halves the failure rate for semiconductor devices. Derate all components unless explicitly justified in the design review record.

---

## Voltage derating

| Component type | Maximum operating voltage | Rule |
|---|---|---|
| Capacitors (electrolytic, ceramic, film) | ≤80% of rated voltage | A 10V rail requires ≥12.5V rated cap; a 12V rail requires ≥15V rated cap |
| BJT (VCE, VCB, VEB) | ≤75% of V_MAX | |
| MOSFET (VDS) | ≤75% of V_DS_MAX | |
| Diode (PIV / V_RRM) | ≤75% of V_MAX | |
| Zener / TVS (clamping) | ≤80% of V_Z or V_RWM | |

**Worked example — capacitor on a 12V rail:**
- Rail voltage: 12V
- Allowed ripple: assume +5% worst-case transient → 12.6V peak
- Derate to 80%: required rated voltage ≥ 12.6V ÷ 0.80 = 15.75V
- **Select: 25V rated capacitor** — this gives 12.6V / 25V = 50.4% stress, well within spec and provides headroom for transients.

---

## Current derating

### Resistors
- Derate to **≤70% of rated power** at 25°C ambient.
- Apply linear derating from 70% at 25°C to 0% at the maximum rated temperature (typically 70°C or 125°C per manufacturer datasheet).
- Example: a 0.25W resistor dissipates a maximum of 0.25W × 0.70 = 0.175W at 25°C.

### PCB traces
- Size traces per **IPC-2221** for a 10°C temperature rise budget.
- See `guidelines/pcb/pcb-design-rules.md` for the current vs. width table.
- Derate further for high-temperature environments or internal layers.

### Connector pins
- Derate to **≤80% of rated current** per pin.
- Account for multi-pin connectors where adjacent pins share thermal path (de-rate further if all pins are loaded simultaneously — consult manufacturer's derating curve).

---

## Temperature derating

### Junction temperature budget
- Junction temperature **must not exceed T_J_MAX − 25°C** under any operating condition.
- For commercial-grade parts (T_J_MAX = 125°C): maximum T_J in use ≤ 100°C.
- For industrial-grade parts (T_J_MAX = 150°C): maximum T_J in use ≤ 125°C.

### Thermal resistance calculations

```
T_J = T_A + P_D × Rθ_JA                  (free-air, no heatsink)
T_J = T_C + P_D × Rθ_JC                  (case temperature known)
T_J = T_A + P_D × (Rθ_JC + Rθ_CS + Rθ_SA)  (with heatsink)
```

Where:
- T_J = junction temperature (°C)
- T_A = ambient temperature (°C)
- T_C = case temperature (°C)
- P_D = power dissipated (W)
- Rθ_JA = junction-to-ambient thermal resistance (°C/W)
- Rθ_JC = junction-to-case thermal resistance (°C/W)
- Rθ_CS = case-to-heatsink thermal resistance (°C/W)
- Rθ_SA = heatsink-to-ambient thermal resistance (°C/W)

### Worked example — linear regulator

Conditions: LDO regulator, V_IN = 12V, V_OUT = 5V, I_OUT = 500mA, T_A = 50°C, Rθ_JA = 50°C/W (SOT-223).

```
P_D = (V_IN − V_OUT) × I_OUT = (12 − 5) × 0.5 = 3.5W
T_J = T_A + P_D × Rθ_JA = 50 + 3.5 × 50 = 50 + 175 = 225°C
```

225°C far exceeds the 100°C limit. **This design requires a heatsink or forced airflow, or the input voltage must be reduced, or the load current must be reduced.** Add a pre-regulator or switch to a switching regulator.

Revised with heatsink (Rθ_SA = 10°C/W, Rθ_JC = 5°C/W, Rθ_CS = 1°C/W):
```
T_J = 50 + 3.5 × (5 + 1 + 10) = 50 + 56 = 106°C  → still exceeds 100°C budget
```
Reduce to I_OUT = 300mA:
```
P_D = 7 × 0.3 = 2.1W
T_J = 50 + 2.1 × 16 = 50 + 33.6 = 83.6°C  → passes
```

*(where 2.1W × 16°C/W = 33.6°C rise)*

---

## Operating temperature categories

| Category | Ambient temperature range | Applies to this project |
|---|---|---|
| Commercial | 0°C to 70°C | *(team to confirm)* |
| Industrial | −40°C to 85°C | *(team to confirm)* |
| Mil-spec | −55°C to 125°C | *(team to confirm)* |

> **Action required:** The lead engineer must confirm which temperature category applies before the first design review and record it in the DDR.

---

## Worked example — power MOSFET carrying 3A at 50°C ambient

Device: IRF7328 (dual P-FET), Rθ_JA = 50°C/W, R_DS(on) = 25mΩ at 25°C.

```
P_D = I²× R_DS(on) = 3² × 0.025 = 0.225W
T_J = T_A + P_D × Rθ_JA = 50 + 0.225 × 50 = 50 + 11.25 = 61.25°C
```

61.25°C is well below T_J_MAX − 25°C = 125 − 25 = 100°C. **Passes.** Note that R_DS(on) increases with temperature; for conservatism, use the value at 100°C from the datasheet graph (typically ~1.5–2× the 25°C value) and recheck.

---

## Non-negotiable rules

- **Capacitors:** never exceed 80% of rated voltage, including transients.
- **Semiconductors (BJT, MOSFET, diode):** never exceed 75% of maximum voltage rating.
- **Zener / TVS:** never exceed 80% of rated clamping / standoff voltage.
- **Resistors:** never exceed 70% of rated power at 25°C; derate linearly to 0 at T_MAX.
- **PCB traces:** size per IPC-2221 with 10°C rise budget; see `pcb-design-rules.md`.
- **Connector pins:** never exceed 80% of rated current per pin.
- **Junction temperature:** T_J must not exceed T_J_MAX − 25°C under any operating condition.
- **Thermal calculations:** must be documented in the DDR for every power-dissipating device dissipating >0.5W.
- **Temperature category:** must be confirmed by lead engineer and recorded before first design review.

---

## Related guidelines

- [ESD Protection](esd-protection.md)
- [Protection Circuits](protection-circuits.md)
- [Thermal Derating](../components/thermal-derating.md)
- [PCB Design Rules](../pcb/pcb-design-rules.md)
