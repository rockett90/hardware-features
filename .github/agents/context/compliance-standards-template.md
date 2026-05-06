# Compliance Standards Template

> **This is a template.** Copy this file to `.github/agents/context/compliance-standards.md`
> (or a product-specific name), fill in the sections below, and add the filename to
> `.github/agents/context/company-standards.md` so that the AI reviewer applies it automatically.
>
> Keep this file free of confidential product information — it should contain standard names and
> requirement summaries only, not design details.

## How to use this template

1. Copy this file to `.github/agents/context/compliance-standards.md` (or a product-specific name)
2. Fill in each section for your product
3. Remove sections that do not apply
4. Add the filename to `.github/agents/context/company-standards.md` so AI review applies it automatically
5. Raise a `chore/` PR with lead approval

---

## Applicable regulatory directives

> EU/UK examples — add, remove, or modify rows to match your product.

| Directive | Scope | Applies to this product | Notes |
|---|---|---|---|
| Low Voltage Directive (LVD) 2014/35/EU / SI 2016/1101 | Electrical equipment 50–1000 V AC or 75–1500 V DC | Yes / No / Partial | |
| EMC Directive 2014/30/EU / SI 2016/1091 | Electromagnetic compatibility | Yes / No / Partial | |
| RoHS Directive 2011/65/EU | Restriction of hazardous substances | Yes / No / Partial | |
| REACH Regulation (EC) 1907/2006 | Chemical substances | Yes / No / Partial | |
| WEEE Directive 2012/19/EU | Waste electrical and electronic equipment | Yes / No / Partial | |
| Machinery Directive 2006/42/EC | Machinery incorporating electrical equipment | Yes / No / Partial | |
| [Add further directives as applicable] | | | |

---

## Applicable industry standards

> Placeholder rows — teams fill in their own standards and applicability.

| Standard | Title | Applies | Notes |
|---|---|---|---|
| IEC 61010-1 | Safety requirements for electrical equipment for measurement, control, and laboratory use | Yes / No | |
| IEC 62133 | Safety requirements for portable sealed secondary lithium cells and batteries | Yes / No | |
| ISO 26262 | Functional safety for road vehicles | Yes / No | |
| IEC 61508 | Functional safety of electrical/electronic/programmable electronic safety-related systems | Yes / No | |
| IEC 60601-1 | Medical electrical equipment — general requirements for basic safety | Yes / No | |
| [Add further standards as applicable] | | | |

---

## Certification targets

| Mark | Region | Target | Notes |
|---|---|---|---|
| CE | EU | Yes / No / TBD | Required for EU market — requires applicable directive conformity |
| UKCA | Great Britain | Yes / No / TBD | Required for GB market post-Brexit |
| UL | North America | Yes / No / TBD | |
| FCC Part 15 | USA | Yes / No / TBD | Required for intentional and unintentional radiators |
| [Add further marks as applicable] | | | |

---

## Key design constraints from standards

> Summarise the most important design rules that flow from the applicable standards.
> Delete the placeholder examples and replace with your product-specific constraints.

<!-- Examples (replace with your own):
- Creepage and clearance requirements (reference the applicable IEC 60664 category)
- Working voltage limits
- Temperature limits
- Insulation requirements
- Specific component approval requirements (e.g. safety-rated capacitors for mains filtering)
-->

---

## AI review instructions for this product

> Tell the AI reviewer what to check specifically for this product.
> Delete the placeholder examples and replace with your own instructions.

<!-- Examples (replace with your own):
- "Flag any component operating above X% of its rated voltage"
- "Check all mains-connected circuits for sufficient creepage per [standard]"
- "Verify all ESD protection paths on external connectors"
-->
