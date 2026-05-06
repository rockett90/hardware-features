# Protection Circuits

> **Review notice:** This document contains industry-standard best practices. It must be reviewed and approved by the lead engineer before being treated as team-authoritative for this project.

## Overvoltage protection (OVP)

### Topologies

#### 1. Zener clamp
A Zener diode placed across the supply rail. When voltage exceeds the Zener breakdown voltage, current is shunted to GND.

- **Pros:** Simple, passive, no latching.
- **Cons:** Continuous power dissipation if voltage stays elevated; Zener must handle the full fault current; response is soft (not a hard clamp).
- **Use when:** low-energy transients; the supply impedance is high enough to limit fault current.

#### 2. TVS clamp
A TVS diode across the supply rail. Faster response than a Zener (sub-nanosecond), higher peak power capability.

- **Pros:** Very fast; available in high I_PP ratings; bidirectional options.
- **Cons:** Not suitable for sustained overvoltage (thermal damage); capacitance adds to power rail.
- **TVS selection for OVP:** V_RWM must be set just above the nominal rail voltage plus the maximum expected tolerance:
  - 12V rail ±5% → V peak = 12.6V → choose V_RWM = 13.3V or 15V TVS (next standard value above 12.6V with margin).
  - V_CL must be below the maximum input voltage of downstream ICs.
- **Use when:** transient suppression on power inputs, coordinated with a series fuse or polyfuse.

#### 3. Active crowbar (SCR / thyristor)
A voltage comparator monitors the rail. On overvoltage, it fires an SCR (thyristor) which latches low, short-circuiting the supply and blowing the upstream fuse.

- **Pros:** Crowbar responds in µs; after tripping the rail is held near zero, protecting all downstream loads; can be reset by removing power.
- **Cons:** Latching — power must be cycled to reset; SCR must be rated for full fault current until fuse clears; comparator adds complexity.
- **Crowbar set point:** set ~10–15% above nominal rail. Example: 12V rail → trip at 13.5V.
- **Coordination:** the upstream fuse must blow before the SCR's I²t rating is exceeded. Size the fuse accordingly.
- **Use when:** high-energy OVP required; load must be protected from any prolonged overvoltage (e.g. if a boost converter malfunctions).

### Response time
- Zener: µs to ms (passive)
- TVS: sub-nanosecond to nanoseconds
- Active crowbar: 1–10µs (comparator + gate drive delay)

---

## Overcurrent protection (OCP)

### Placement
OCP devices must always be placed on the **hot side of the supply** (between the supply source and the load), not on the GND return path.

### Topologies

#### 1. Resettable polyfuse (PTC)
A PTC (positive temperature coefficient) polymer fuse that increases resistance dramatically when it heats up past its trip temperature.

- **Selection:** hold current (I_HOLD) must exceed maximum normal operating current; trip current (I_TRIP) must be below the minimum fault current expected. Note: I_TRIP ≈ 2× I_HOLD is typical.
- **Pros:** Resettable (auto-reset on power removal); no manual intervention required.
- **Cons:** Slow trip time (tens to hundreds of ms); does not protect against fast inrush or very low impedance faults; resistance in normal operation causes voltage drop.
- **Use when:** USB port protection, low-power auxiliary rails, user-accessible connectors.

#### 2. Ideal diode / eFuse IC (e.g. TPS2596 family)
An integrated circuit that uses a power FET to implement a low-dropout current limiter with adjustable current limit, fast over-current response, and thermal shutdown.

- **Selection:** set current limit via external resistor: I_LIM = V_ILIM / R_ILIM (see IC datasheet).
- **Inrush limiting:** most eFuse ICs include programmable soft-start (slew rate control on V_OUT) to prevent inrush current during power-up.
- **Pros:** Precise current limit; fast response (µs); programmable; includes status/fault output; low on-resistance.
- **Cons:** Requires more PCB area and cost than a polyfuse; active device (requires correct supply to operate).
- **Use when:** main system power input, any rail where precise current limiting and fast fault response are required.

#### 3. Fuse + P-FET
A traditional fuse in series with the hot rail, optionally combined with a P-FET for soft-start or reverse polarity protection.

- **Hold/trip selection:** fuse hold current ≥ 1.25× maximum normal load current; fuse interrupt rating must exceed the available fault current.
- **Inrush:** fuses must not blow on normal inrush current during power-up — check the I²t of inrush event vs. the fuse's melting I²t curve.
- **Pros:** Simple; well-understood; very low cost.
- **Cons:** Single-use (must be replaced after trip); no current limiting — full fault current flows until fuse clears.

---

## Reverse polarity protection

### P-FET gate-to-source clamp topology (preferred)
A P-channel MOSFET with the source connected to V_IN and the drain to the load. A Zener clamp between gate and source ensures the FET turns on at the correct supply voltage and off if polarity is reversed.

```
V_IN (+) ─── [P-FET Source] ──── [P-FET Drain] ─── V_OUT to load
                   │
               [Zener / gate resistor to GND]
                   │
                  GND
```

- When polarity is correct: gate is pulled below source by the Zener reference, FET turns on, nearly zero voltage drop (I × R_DS(on)).
- When polarity is reversed: V_GS becomes positive, FET turns off, load is disconnected.
- **Preferred topology** because V_F drop is very low (I × R_DS(on) vs. ~0.3–0.6V for a Schottky diode).
- **Gate clamp:** use a Zener rated at V_GS(th) + margin. Ensure V_GS clamp voltage does not exceed the MOSFET's absolute maximum V_GS.

### Schottky diode (simple but lossy)
A Schottky diode in series with the supply rail, forward-biased when polarity is correct, reverse-biased when polarity is reversed.

- **Pros:** Simple; one component; inherently limits inrush if forward-biased.
- **Cons:** 0.3–0.6V forward voltage drop at full load current — significant power loss at high currents (e.g. 5A × 0.5V = 2.5W); Schottky must be rated for full load current.
- **Use when:** low-current auxiliary circuits where the voltage drop is acceptable.

### P-FET + Zener gate clamp (full description)
Extend the P-FET topology by adding a resistor (R_G) between V_IN and the gate, and a Zener (D_Z) between gate and GND:

- R_G limits gate drive current and prevents oscillation.
- D_Z sets the gate voltage, ensuring V_GS = −V_Z (regulated) when supply is present.
- Choose V_Z = 5.1V or 10V to keep V_GS well within the FET's safe operating area and ensure full enhancement at minimum supply voltage.

---

## Soft-start

### Why soft-start is required
At power-up, bulk capacitance (electrolytic, ceramic output capacitors) presents a near-short-circuit load. The inrush current can be several amperes for tens of milliseconds, causing voltage droop on the supply, nuisance tripping of fuses, and mechanical / thermal stress on connectors and components.

**Soft-start is required when bulk capacitance on any rail exceeds 47µF.**

### RC soft-start on enable pin
Many regulators and load switches have an enable pin. Adding an RC network (R in series, C to GND) on the enable pin delays the turn-on ramp, effectively controlling inrush.

```
V_CTRL ──[R]──┬── EN (regulator enable)
              │
             [C]
              │
             GND
```

Approximate inrush limiting: I_inrush ≈ C_BULK × dV/dt, where dV/dt is set by the soft-start ramp.

### Dedicated eFuse with adjustable soft-start
The preferred method for main power rails. eFuse ICs (e.g. TPS2596, TPS2660 family) allow programming of the output slew rate via a capacitor on the dV/dt pin. See the eFuse section under OCP above.

### Inrush limiting resistor calculation
For a resistor-based inrush limiter (NTC thermistor at room temperature):
```
I_peak = V_IN / R_NTC_cold
```
Choose R_NTC such that I_peak ≤ the fuse hold current × 5 (typical inrush allowance for fuses — check manufacturer's time-current curve).

---

## Crowbar circuits

### Over-voltage crowbar using TL431 + SCR
The TL431 precision shunt regulator is used as a comparator. When the monitored voltage exceeds the set point, the TL431 cathode current increases, triggering the SCR gate.

```
                 R_TOP
V_RAIL ──[R_TOP]──┬──── SCR Anode
                  │     SCR Cathode ── GND
               [R_BOT]  SCR Gate ──┐
                  │                │
                 GND   [R_G] ──── TL431 Cathode
                                  TL431 Anode ── GND
                                  TL431 Ref ──[R_TOP / R_BOT divider tap]
```

**Set point selection:**
```
V_TRIP = V_REF × (1 + R_TOP / R_BOT)   (V_REF = 2.495V for TL431)
```
Choose R_TOP and R_BOT to set V_TRIP approximately 10–15% above nominal rail. R_G (gate resistor) limits SCR gate drive current and is typically 100–470Ω.

### Coordination with upstream fuse
- The SCR crowbar creates a near-short circuit. The upstream fuse must clear before the SCR's I²t limit is exceeded.
- Calculate the available fault current: I_fault = V_IN / (R_source + R_crowbar).
- Check the fuse's melting I²t (from datasheet) vs. the SCR's single-pulse I²t rating.
- Size the fuse so it always clears within the SCR's rating.

---

## Mandatory requirements

- **OVP + OCP + reverse polarity protection** are required on all external DC power inputs.
- **Soft-start** is required when bulk capacitance exceeds **47µF** on any rail.
- **OCP placement:** always on the hot side of the supply (not the GND return).
- **Fuse coordination** must be verified when using a crowbar topology (fuse I²t > crowbar I²t).
- **Inrush analysis** must be documented in the DDR for any rail with bulk capacitance > 47µF.

---

## Non-negotiable rules

- OVP, OCP, and reverse polarity protection required on every external DC power input — no exceptions.
- Soft-start required when C_BULK > 47µF on any rail.
- OCP device (fuse, PTC, eFuse) must be on the hot side of the supply.
- TVS V_RWM on a power rail must be set above nominal + tolerance, and V_CL must be below the downstream IC absolute maximum supply voltage.
- Crowbar trip point must be set 10–15% above nominal rail voltage; fuse coordination must be verified.
- All protection circuit calculations and topology choices must be documented in the DDR.

---

## Related guidelines

- [ESD Protection](esd-protection.md)
- [Derating](derating.md)
- [PCB Design Rules](../pcb/pcb-design-rules.md)
