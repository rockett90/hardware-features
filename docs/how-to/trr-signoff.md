# How to perform a TRR sign-off

> Test Readiness Review (TRR) — a formal gate confirming the feature is ready for formal verification and validation testing.

---

## What is a TRR?

A Test Readiness Review is a formal checkpoint that confirms the hardware is built, brought up, and ready to enter formal verification testing. It is a gate — the `gate-check.yml` workflow validates that all required documentation is present and will block merge if anything is missing.

---

## Prerequisites

- CDR gate passed (`cdr/<feature>/approved` tag exists)
- Hardware built and basic bring-up complete
- ERC and DRC pass (run `/erc` and `/drc`)
- All required gate documents present (see gate-check below)

---

## Steps

### 1. Run the Gate Sign-Off workflow

Go to **Actions → Gate Sign-Off → Run workflow**, enter your feature name, and select `trr`. The workflow checks that `cdr/<feature>/approved` already exists before it creates `signoff/<feature>/trr`, commits the gate evidence file, and opens the TRR PR automatically.

### 2. Open the PR from the workflow summary link

When the workflow completes, open its summary page and click the PR link that it created. The PR title should be `chore(<feature>): TRR sign-off` and the TRR checklist is already filled into the PR body.

### 3. Run `/render`

Post `/render` as a PR comment to generate current schematic SVGs for the record.

### 4. Tick the checklist

Read the TRR checklist in the PR body and tick every item once the evidence is complete. If `gate-check.yml` fails, fix the missing evidence or update the checklist before requesting review.

### 5. Obtain required approvals

Obtain the required number of reviewer approvals per CODEOWNERS.

### 6. Merge

Once CI passes and approvals are in place, merge the PR.

On merge, `gate-tags.yml` automatically creates the git tag `trr/<feature>/approved`.

---

## What gate-check validates

The `gate-check.yml` workflow checks that required design and test documents are present in the feature directory. See [`.github/guidelines/gate-criteria.md`](../../.github/guidelines/gate-criteria.md) for the full list of requirements.

---

## After TRR

Once TRR is merged and tagged, the feature is cleared to enter formal verification. Releases are managed automatically by release-please — do not create release tags manually.
