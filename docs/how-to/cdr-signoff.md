# How to perform a CDR sign-off

> **Opening the CDR PR:** Use the following URL to open your PR with the CDR template pre-loaded (replace `<branch>` with your branch name):
> ```
> https://github.com/rockett90/hardware-features/compare/main...<branch>?template=cdr-signoff.md
> ```
> Do not open the PR from the GitHub branch page directly — it will load the default template instead of the CDR template.
>
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

## Branch naming

```
signoff/<feature>/cdr
```

---

## Steps

### 1. Create the sign-off branch

```bash
git checkout main
git pull
git checkout -b signoff/<feature>/cdr
```

### 2. Verify gate documents are present

The `gate-check.yml` workflow validates that all required documents exist inside `features/<feature>/`. Required documents are defined in [`.github/guidelines/gate-criteria.md`](../../.github/guidelines/gate-criteria.md).

> ⚠️ Warning: If any required document is missing, `gate-check.yml` will fail and block merge. The check runs automatically on push — fix any failures before requesting review.

### 3. Open a PR

PR title format:
```
chore(<feature>): CDR sign-off
```

Open the PR as a **draft** initially, then convert to ready-for-review once CI passes.

### 4. Run `/render`

Post `/render` as a PR comment. This generates current schematic SVGs that are stored as part of the review record.

### 5. Obtain required approvals

Obtain the required number of reviewer approvals per CODEOWNERS.

### 6. Merge

Once CI passes and approvals are in place, merge the PR.

On merge, `gate-tags.yml` automatically applies the git tag `<feature>/cdr-v1`.

---

## What gate-check validates

The `gate-check.yml` workflow checks that required design documents are present in the feature directory. It does not validate the content of those documents — that is the responsibility of the human reviewers.

See [`.github/guidelines/gate-criteria.md`](../../.github/guidelines/gate-criteria.md) for the full list of requirements.

---

## After CDR

Once CDR is merged and tagged, the feature is cleared to proceed to build and bring-up. For the next formal gate, see [trr-signoff.md](trr-signoff.md).
