# How to raise and resolve an IVV finding

## Overview

An IVV finding is a defect raised during Integration, Verification and Validation. Findings are tracked as GitHub Issues and resolved via `finding/` branches.

The same process applies whether the finding is raised by the designer during bring-up (Stage 4) or by the IVV team after TRR (Stage 6).

---

## Prerequisites

The following labels must exist in the repository before this process can be used:

- `finding: minor`
- `finding: moderate`
- `finding: major`
- `finding: in-progress`
- `finding: resolved`

A lead should verify these exist before the first IVV cycle. Go to **github.com → Issues → Labels** to check.

---

## Step 1 — Raise a GitHub Issue

1. Go to the **Issues** tab on GitHub.
2. Click **New issue**.
3. Select the **IVV Finding** issue template.
4. Fill in:
   - Title: `[FEATURE] Brief description of the finding`
   - Body: complete the template fields — observed behaviour, expected behaviour, evidence, affected requirement(s)
5. Submit the issue. Note the issue number (e.g. `#42`).

---

## Step 2 — Assign severity

The lead reviews the finding and applies the correct severity label:

| Label | Meaning | Gate re-entry |
|---|---|---|
| `finding: minor` | Does not affect form, fit, or function | None, unless lead decides otherwise |
| `finding: moderate` | Affects function but not safety-critical | Re-TRR required |
| `finding: major` | Affects safety, compliance, or system interface | Re-CDR then re-TRR required |

---

## Step 3 — Create a finding branch and PR

#### GitHub Desktop

1. Click **Current branch** → **New branch**.
2. Name the branch: `finding/<feature>/<issue-number>-<short-desc>`
   - Example: `finding/simple-amplifier/42-gain-error-at-low-temp`
3. Confirm **From** shows `main` → **Create branch** → **Publish branch**.

#### Command line

```bash
git checkout main && git pull
git checkout -b finding/simple-amplifier/42-gain-error-at-low-temp
git push -u origin finding/simple-amplifier/42-gain-error-at-low-temp
```

Open a PR:
- Title: `fix(<feature>): <description> — finding #<N>`
  - Example: `fix(simple-amplifier): correct gain resistor value — finding #42`
- Body: include `Resolves #42` on its own line in the PR description body (not the title)

> ⚠️ `Resolves #N` must be in the **PR body**, not the title. CI reads the body to link the finding issue.

**What CI does automatically when the PR is opened:**
- Adds `finding: in-progress` label to the linked issue
- Posts a comment on the issue linking to the PR

---

## Step 4 — Fix, review, and merge

Work through the fix on the `finding/` branch. Follow the same commit and review process as an `artifact/` PR.

**What CI does automatically when the PR is merged:**
- Adds `finding: resolved` label to the linked issue
- Posts a comment on the issue with the merge commit SHA

---

## Step 5 — Gate re-entry (if required)

| Severity | Action |
|---|---|
| `finding: minor` | No gate re-entry. Proceed to next stage. |
| `finding: moderate` | Re-TRR required — run **Actions → Gate Sign-Off → trr** |
| `finding: major` | Re-CDR then re-TRR — run **Actions → Gate Sign-Off → cdr** then **→ trr** |

For re-TRR and re-CDR, follow the same process as the original CDR/TRR sign-off — see [cdr-signoff.md](cdr-signoff.md) and [trr-signoff.md](trr-signoff.md).

---

## Quick reference

```text
Branch:   finding/<feature>/<issue-number>-<short-desc>
PR title: fix(<feature>): <description> — finding #<N>
PR body:  Resolves #<N>
Labels:   finding: minor | finding: moderate | finding: major
CI adds:  finding: in-progress (PR opened), finding: resolved (PR merged)
```
