# How to perform a TRR sign-off

> Test Readiness Review (TRR) — a formal gate confirming the feature is ready for formal verification and validation testing.

---

## What is a TRR?

A Test Readiness Review is a formal checkpoint that confirms the hardware is built, brought up, and ready to enter formal verification testing. It is a gate — the `gate-check.yml` workflow validates that all required documentation is present and will block merge if anything is missing.

---

## Prerequisites

- CDR gate passed (`<feature>/cdr-v1` tag exists)
- Hardware built and basic bring-up complete
- ERC and DRC pass (run `/erc` and `/drc`)
- All required gate documents present (see gate-check below)

---

## Branch naming

First TRR:
```
signoff/<feature>/trr
```

Re-TRR (if the first TRR failed and a re-review is required):
```
signoff/<feature>/trr-2
signoff/<feature>/trr-3
```
(increment `N` for each re-TRR)

---

## Steps

### 1. Create the sign-off branch

```bash
git checkout main
git pull
git checkout -b signoff/<feature>/trr
```

### 2. Verify gate documents are present

The `gate-check.yml` workflow validates that all required documents exist inside `features/<feature>/`. Required documents are defined in [`.github/guidelines/gate-criteria.md`](../../.github/guidelines/gate-criteria.md).

> ⚠️ Warning: If any required document is missing, `gate-check.yml` will fail and block merge. Fix failures before requesting review.

### 3. Open a PR

PR title format:
```
chore(<feature>): TRR sign-off
```

For a re-TRR:
```
chore(<feature>): TRR-2 sign-off
```

### 4. Run `/render`

Post `/render` as a PR comment to generate current schematic SVGs for the record.

### 5. Obtain required approvals

Obtain the required number of reviewer approvals per CODEOWNERS.

### 6. Merge

On merge, `gate-tags.yml` automatically applies the git tag:

| Branch | Tag applied |
|---|---|
| `signoff/<feature>/trr` | `<feature>/trr-v1` |
| `signoff/<feature>/trr-2` | `<feature>/trr-v2` |
| `signoff/<feature>/trr-N` | `<feature>/trr-vN` |

---

## What gate-check validates

The `gate-check.yml` workflow checks that required design and test documents are present in the feature directory. See [`.github/guidelines/gate-criteria.md`](../../.github/guidelines/gate-criteria.md) for the full list of requirements.

---

## After TRR

Once TRR is merged and tagged, the feature is cleared to enter formal verification. Releases are managed automatically by release-please — do not create release tags manually.
