# EMC Review Checklist

> Engineer reference checklist — not auto-posted. Consult during schematic and PCB review for EMC-relevant designs.

## Schematic — filtering and protection

- [ ] Mains or high-frequency power rails have appropriate common-mode and differential-mode filtering
- [ ] ESD protection devices on all external-facing signal and power pins
- [ ] TVS diodes or MOVs on power inputs where transient protection is required
- [ ] Ferrite beads or pi-filters on power supply rails where emissions are a concern
- [ ] Decoupling capacitors placed on all IC power pins — values appropriate for operating frequencies
- [ ] Crystal circuit has load capacitors sized correctly and guard ring noted for PCB
- [ ] Clock signals are buffered close to source and do not fan out across the board unnecessarily

## Schematic — grounding

- [ ] Single-point or split-plane ground strategy documented in a DDR
- [ ] Chassis ground / protective earth connection present where required
- [ ] Shield ground connections defined — floating or connected, with reason recorded
- [ ] Connector shell grounds specified

## PCB — layout

- [ ] High-frequency return paths are short and direct — no splits in ground plane under high-speed signals
- [ ] Decoupling capacitors placed as close as possible to IC power pins
- [ ] Crystal and oscillator circuits have tight layout with guard ring or ground pour
- [ ] Clock traces are short, routed away from sensitive analogue signals, and have ground reference underneath
- [ ] Switching regulator layout follows manufacturer recommended layout
- [ ] Filter components form a clean signal path — no re-radiation via long trace loops
- [ ] Board edge has unbroken ground pour where chassis contact or gasket is intended

## PCB — cable and connector management

- [ ] Cable entry points have filtering and/or ESD protection close to the connector
- [ ] Cable grounds are connected at the correct point (shield termination reviewed)
- [ ] Differential pairs are matched in length and have continuous ground reference

## Compliance

- [ ] Creepage and clearance distances meet the applicable standard for working voltage and pollution degree
- [ ] Isolation barriers (galvanic, optical, transformer) meet the applicable standard
- [ ] Any intentional radiators (Bluetooth, Wi-Fi, cellular) are noted and appropriate regulatory approvals identified

## References

- [ ] Applicable EMC directive or standard identified and referenced in the design record
- [ ] EMC test plan or approach documented in a DDR or requirements document
