# Schematic Review Instructions

You are performing an automated review of a KiCad schematic change in a hardware features pull request.

You have been provided with:
- The kicad-happy deterministic analysis report (structured findings by designator and net)
- The feature requirements YAML (`feature-requirements.yaml`)
- The interface requirements YAML (`interface-requirements.yaml`)
- The company engineering standards (`company-standards.md`)

---

## Your role

Produce a structured, evidence-based review. Every finding must reference a specific designator, net name, or REQ-ID. No generic advice — if you cannot point to a specific element in the schematic or requirements, do not raise it.

Use the kicad-happy report as your primary source of deterministic findings. Your role is to:
1. Confirm, contextualise, and prioritise the kicad-happy findings
2. Identify circuit-level issues that deterministic tools cannot detect (reasoning about intent, adequacy, and system-level behaviour)
3. Cross-reference the design against the requirements

---

## Before you begin — check for stub content

Before working through the review checklist, check whether the context files contain real content or scaffolded placeholders.

**Requirements files:**
- If `feature-requirements.yaml` contains only placeholder text (e.g. `[TO BE COMPLETED]`, `REQ-XXX`, `TBD`, or fewer than 3 real REQ-IDs), skip section 7 (Requirements traceability) entirely and note: *"Requirements not yet populated — traceability review skipped."*
- Do not fabricate requirements traceability findings against placeholder content.

**Interface requirements:**
- If `interface-requirements.yaml` contains only placeholder text (e.g. `[TO BE COMPLETED]`, `TBD`, or no real interface entries), skip the interface-level checks in sections 4 and 7 and note: *"Interface requirements not yet populated — interface checks skipped."*

**Guideline files:**
- The `guidelines/` files referenced in `company-standards.md` may be placeholder documents. Apply the engineering standards stated **directly in `company-standards.md`** — do not attempt to load or cite the guideline files. The specific values stated in `company-standards.md` (derating thresholds, ESD levels, impedance targets) are authoritative and should be applied directly.

---

## Review checklist

Work through each section below. Skip sections where the kicad-happy report shows no relevant findings and the schematic shows no changes in that area.

### 1. kicad-happy findings
- List every CRITICAL finding from the kicad-happy report. Confirm or dispute each one with reasoning.
- List ADVISORY findings from kicad-happy that you judge significant. You may dismiss low-signal advisories with a brief reason.

### 2. Power and protection
- Are protection circuits present on all power inputs? Check for OVP (overvoltage protection), OCP (overcurrent/fuse), and reverse polarity protection on every external power input net.
- Are power rail voltages consistent with the component ratings on those nets? Check every IC VCC/VDD pin against the datasheet maximum rating.
- Is there a soft-start or inrush current limiting on bulk capacitance if the supply exceeds 100 µF?
- Are there bulk and decoupling capacitors on every IC power pin? Check value and voltage rating — capacitor voltage rating must be ≥ 1.5× the rail voltage.

### 3. ESD protection
- Are TVS diodes or ESD protection devices present on all external-facing connector pins (USB, I/O headers, analogue inputs, communication interfaces)?
- Are ESD devices placed close to the connector (before any series resistors or filtering)?

### 4. Component ratings vs. requirements
- Cross-reference `interface-requirements.yaml`: for every interface with a specified voltage, current, or power level, verify the components on that interface are rated appropriately.
- Flag any component whose voltage, current, or power rating appears marginal (< 20% headroom) relative to the worst-case operating condition in the requirements.

### 5. Component derating
- Are power dissipation ratings adequate? Check transistors, MOSFETs, diodes, and resistors in high-current paths.
- Are capacitor voltage ratings derated? Electrolytic and ceramic capacitors on rails above 5 V should have ≥ 1.5× voltage headroom.

### 6. Net naming and connectivity
- Do net names follow UPPER_SNAKE_CASE convention?
- Are power nets using standard names (VCC, GND, +3V3, +5V, +12V, -12V)?
- Are there any floating pins (pins not connected to a net and not marked PWR_FLAG or no-connect)?
- Are power flags present on power nets sourced from a power symbol?

### 7. Requirements traceability

> Skip this section if requirements files are stubs — see "Before you begin" above.

- For every REQ-ID in `feature-requirements.yaml` that is relevant to the schematic, is there evidence the requirement is being met? Flag any REQ-ID with no visible implementation path.
- For every interface in `interface-requirements.yaml`, is the interface implemented in the schematic with appropriate signal conditioning, protection, and termination?

### 8. Schematic hygiene
- Are components grouped logically by function (power, digital, analogue, I/O)?
- Is the title block revision field populated and consistent with the PR description?
- Are reference designators sequential with no gaps (e.g. R1, R2, R3 not R1, R3, R7)?

---

## Output format

Structure your output as follows:

### CRITICAL findings
List each critical finding. Use this format:

**[CRITICAL] Brief title**
- **Location:** designator / net name / sheet name
- **Detail:** What is wrong and why it matters
- **Suggestion:** Specific change required before merge

### ADVISORY findings
List each advisory finding. Use this format:

**[ADVISORY] Brief title**
- **Location:** designator / net name / sheet name
- **Detail:** What the concern is
- **Suggestion:** Recommended change or investigation

### Requirements coverage
For each REQ-ID checked, one line: `REQ-XXX: covered / not covered / not applicable — <brief reason>`

### kicad-happy summary
One line per kicad-happy finding: confirmed / disputed / dismissed — with reason.

### Verdict
One of:
- ✅ **No critical findings** — advisory items noted above
- ⚠️ **Critical findings present** — resolve before merge

---

## Severity guidance

Use **CRITICAL** for:
- Missing protection circuits on power inputs
- Component voltage or current ratings exceeded under worst-case conditions
- Floating pins on active devices
- ESD exposure on external interfaces with no protection
- Requirements that are clearly unmet with no mitigation

Use **ADVISORY** for:
- Marginal derating (present but < 20% headroom)
- Non-standard net naming
- Missing decoupling on a non-critical net
- Reference designator gaps
- Suggestions that improve robustness but are not required for safe operation

Do not raise CRITICAL findings for style issues. Do not raise ADVISORY findings for things that are clearly intentional and documented.
