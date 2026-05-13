---
document-version: "1.0"
baseline: PDR
approved-date: "2025-03-01"
approved-by: "Reference Example"
---

# Verification Matrix — simple-amplifier

| REQ ID  | Description                                      | Method   | Gate | Evidence                                        | Status      |
|---------|--------------------------------------------------|----------|------|-------------------------------------------------|-------------|
| REQ-001 | Gain 0–500 mV → 0–3.3 V, error < ±1%            | Test     | TRR  | `bring-up/measurements/gain-accuracy.csv`       | ⏳ Pending  |
| REQ-002 | Input impedance > 100 kΩ at DC                  | Analysis | CDR  | `calculations/input-impedance.md`               | ⏳ Pending  |
| REQ-003 | Operates from 3.3 V ± 5% single supply          | Test     | TRR  | `bring-up/measurements/supply-variation.csv`    | ⏳ Pending  |
| REQ-004 | Bandwidth > 10 kHz (−3 dB)                      | Test     | TRR  | `bring-up/measurements/frequency-response.csv` | ⏳ Pending  |
| REQ-005 | Operates −20 °C to +70 °C                       | Test     | TRR  | `bring-up/measurements/temperature-sweep.csv`  | ⏳ Pending  |
