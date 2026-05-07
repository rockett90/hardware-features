# bench

> Python drivers for bench instruments used in automated hardware test — PSU, DMM, oscilloscope, and similar.

---

## What is this directory?

This directory contains reusable Python drivers for bench instruments. Bring-up scripts inside `features/<feature>/bring-up/scripts/` import from here to control hardware during automated test.

---

## Import path

Bring-up scripts should add `bench/` to the Python path using this convention (from CONTRIBUTING.md section 15):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'bench'))
```

---

## Structure

| Directory | Contents |
|---|---|
| `drivers/` | Instrument driver modules — one file per instrument family |
| `utils/` | Shared utility functions used by multiple drivers |

> 💡 Tip: `drivers/` and `utils/` are currently empty placeholders. Drivers will be added here as they are developed.

---

## Status

Not yet populated. This directory is reserved for future instrument drivers.

---

## Adding a driver

When adding a new instrument driver:

1. Create one file per instrument family in `drivers/`, named `<manufacturer>-<model>.py` (e.g. `keysight-e3631a.py`).
2. Expose a class with at minimum: `connect()`, `measure()`, `disconnect()`.
3. Add any shared helper code to `utils/`.
4. Raise a `chore/` PR with a brief description of the instrument and the test it supports.

```python
class KeysightE3631A:
    def connect(self, address: str) -> None: ...
    def measure(self) -> float: ...
    def disconnect(self) -> None: ...
```
