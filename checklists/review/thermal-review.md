# Thermal Review Checklist

> Engineer reference checklist — not auto-posted. Consult when reviewing thermal analysis or before TRR gate.

## Analysis completeness

- [ ] All power-dissipating components identified
- [ ] Power dissipation calculated at worst-case operating conditions
- [ ] Thermal resistance chain defined for each significant heat source (junction → case → heatsink → ambient)
- [ ] Worst-case ambient temperature defined and documented

## Junction temperatures

- [ ] Maximum junction temperature calculated for all semiconductors
- [ ] Junction temperatures are within the component's absolute maximum rating
- [ ] Junction temperatures include derating margin (typically ≤80% of absolute maximum)
- [ ] Calculations reference component datasheet thermal resistance values

## Heatsinking and cooling

- [ ] Heatsink sizing calculation present where heatsink is used
- [ ] Thermal interface material specified (where applicable)
- [ ] Forced-air cooling dependencies documented — failure mode considered if airflow is lost
- [ ] Passive convection path is unobstructed in the enclosure design

## PCB thermal management

- [ ] Thermal relief connections reviewed — appropriate for rework but not causing thermal issues
- [ ] Copper pours used to spread heat from high-dissipation components where appropriate
- [ ] Thermal vias under exposed pads sized and spaced per manufacturer recommendation
- [ ] Component placement allows for convection (hot components not directly above cool components)

## Testing

- [ ] Thermal analysis approach referenced in verification matrix
- [ ] Temperature measurement points defined for test
- [ ] Pass/fail criteria for junction temperatures documented
