# Requirements Schema

> This file defines the expected structure of hardware requirements attached to PRs and issues in this repository.

## Required fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique requirement identifier, e.g. `REQ-HW-001` |
| `title` | string | Short, imperative description |
| `rationale` | string | Why this requirement exists |
| `verification` | string | How compliance will be verified (analysis, test, inspection, simulation) |
| `priority` | enum | `shall` / `should` / `may` |
| `status` | enum | `draft` / `approved` / `deprecated` |

## Optional fields

| Field | Type | Description |
|---|---|---|
| `links` | array | Related requirement IDs or guideline paths |
| `notes` | string | Additional context |

## Example

```yaml
id: REQ-HW-001
title: All power inputs shall have reverse polarity protection
rationale: Prevents board damage during incorrect connector insertion
verification: inspection
priority: shall
status: approved
links:
  - guidelines/electrical/protection-circuits.md
```
