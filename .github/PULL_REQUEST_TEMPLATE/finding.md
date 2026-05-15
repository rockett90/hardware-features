## IVV Finding Fix

**Feature:**
**Finding issue:** #
**Severity:** <!-- minor / moderate / major -->
**Fix date:**
**Lead:**

---

## Summary of finding

<!-- Describe the defect found during IVV. Reference the GitHub Issue number above. -->

## Root cause

<!-- What caused the defect? -->

## Fix description

<!-- What was changed to resolve it? -->

## Verification

- [ ] Fix implemented and committed to this branch
- [ ] Fix verified on hardware (or justified as verifiable by re-test at TRR)
- [ ] `Resolves #<issue-number>` included in this PR body (required for automatic issue label update)
- [ ] Severity label confirmed on the linked issue (`finding: minor`, `finding: moderate`, or `finding: major`)

## Gate re-entry (tick one)

- [ ] `finding: minor` — no gate re-entry required
- [ ] `finding: moderate` — re-TRR required; run **Actions → Gate Sign-Off → trr** after this merges
- [ ] `finding: major` — re-CDR then re-TRR required; run **Actions → Gate Sign-Off → cdr** then **→ trr** after this merges

## Sign-off

- [ ] Fix date recorded above
- [ ] Lead name recorded above

---

> ⚠️ CI will block merge until all checklist items above are ticked.
> Every item must be checked — items may not be deleted from this list.
> If an item does not apply, tick it and add a note below.

<!-- Notes -->

Resolves #

---

> 📖 See [CONTRIBUTING.md](../CONTRIBUTING.md#12-ivv-findings) for the full IVV findings process.
> PR title format: `fix(<feature>): description` — validated by CI.
