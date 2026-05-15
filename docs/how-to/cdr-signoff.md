# How to perform a CDR sign-off

> Critical Design Review (CDR) — a formal gate in the hardware feature lifecycle that must be passed before a design moves to build.

---

## What is a CDR?

A Critical Design Review is a formal checkpoint that confirms the design is complete, reviewed, and ready to proceed. It is a gate — the `gate-check.yml` workflow validates that all required documentation is present and will block merge if anything is missing.

---

## Prerequisites

- All ⚠️ CRITICAL AI review findings resolved
- ERC passes (run `/erc` and review the output)
- Schematic reviewed and approved by a second engineer
- All required gate documents present (see gate-check below)

---

## Steps

### 1. Run the Gate Sign-Off workflow

Go to **Actions → Gate Sign-Off → Run workflow**, enter your feature name, and select `cdr`. The workflow creates `signoff/<feature>/cdr`, commits the gate evidence file, and opens the CDR PR automatically.

### 2. Open the PR from the workflow summary link

When the workflow completes, open its summary page and click the PR link that it created. The PR title should be `chore(<feature>): CDR sign-off` and the CDR checklist is already filled into the PR body.

### 3. Run `/render`

Post `/render` as a PR comment. This generates current schematic SVGs that are stored as part of the review record.

### 4. Tick the checklist

Read the CDR checklist in the PR body and tick every item once the evidence is complete. If `gate-check.yml` fails, fix the missing evidence or update the checklist before requesting review.

### 5. Obtain required approvals

Obtain the required number of reviewer approvals per CODEOWNERS.

### 6. Merge

Once CI passes and approvals are in place, merge the PR.

On merge, `gate-tags.yml` automatically creates the git tag `cdr/<feature>/approved`.

---

## What gate-check validates

The `gate-check.yml` workflow checks that required design documents are present in the feature directory. It does not validate the content of those documents — that is the responsibility of the human reviewers.

See [`.github/guidelines/gate-criteria.md`](../../.github/guidelines/gate-criteria.md) for the full list of requirements.

---

## After CDR

Once CDR is merged and tagged, the feature is cleared to proceed to build and bring-up. For the next formal gate, see [trr-signoff.md](trr-signoff.md).

CI also creates `features/<feature>/reviews/library.lock` recording the exact library and feature commit SHAs at this gate. See [library-lock.md](library-lock.md) for what this file is and how to use it for traceability.
