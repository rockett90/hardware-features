# Stress Analysis Review Checklist

> Engineer reference checklist — not auto-posted. Consult when reviewing a stress analysis artefact.

## Coverage

- [ ] All active components included (ICs, transistors, diodes)
- [ ] All passive components operating above 50% rated voltage or current included
- [ ] All components on power rails included
- [ ] All components at thermal extremes included
- [ ] Components on external-facing interfaces included

## Voltage stress

- [ ] Worst-case supply voltage used (maximum input or regulation tolerance)
- [ ] Transient and start-up voltages considered
- [ ] All components derate to ≤70% rated voltage under worst-case conditions (or deviation recorded)
- [ ] Capacitor voltage ratings include derating for temperature and DC bias (ceramic capacitors particularly)

## Current stress

- [ ] Peak currents calculated, not just steady-state
- [ ] Inrush currents considered for capacitors and inductors
- [ ] All components derate to ≤70% rated current under worst-case conditions (or deviation recorded)

## Power stress

- [ ] Worst-case power dissipation calculated for all power-dissipating components
- [ ] Thermal resistance chain calculated where power dissipation is significant
- [ ] Components derate to ≤70% rated power under worst-case conditions (or deviation recorded)

## Temperature stress

- [ ] Worst-case ambient temperature used
- [ ] Junction temperature calculated for semiconductors
- [ ] All components within operating temperature range at worst-case junction temperature

## Sign-off

- [ ] Derating policy referenced (see `guidelines/electrical/derating.md`)
- [ ] All deviations from derating policy recorded with justification
- [ ] Analysis document includes component reference, rated value, operating value, and margin
