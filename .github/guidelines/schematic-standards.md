# Schematic Standards
## Net naming
- Power nets: VCC, GND, +3V3, +5V
- Signal nets: descriptive names, UPPER_SNAKE_CASE
- Buses: follow KiCad bus naming convention

## Component placement
- Place components logically by function block
- Group related components visually

## ERC
- Zero errors before any artifact PR merge
- Zero warnings unless formally accepted with comment

## Title block
- Title: feature name
- Revision: match git tag (e.g. v1.0.0)
- Date: date of last schematic change
