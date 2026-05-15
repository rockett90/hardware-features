# How to run a second design cycle

Use this guide when a released feature needs another round of design changes, review, and release. A second cycle uses the same process as the first cycle — there is no special branch naming, no cycle suffix, and no separate sign-off path.

---

## Process

1. Make the required design changes through the usual `artifact/<feature>/...` PRs.
2. When the design is ready for CDR again, go to **Actions → Gate Sign-Off → Run workflow** and select `cdr`.
3. After build and bring-up are complete, run **Gate Sign-Off** again and select `trr`.
4. After IVV evidence is updated and the design is ready for manufacture, run **Gate Sign-Off** again and select `release`.
5. Merge the release-please Release PR as normal to generate the next production version tag and manufacturing outputs.

---

## Tags

Gate tags are floating tags. Each time a new CDR, TRR, or Release sign-off PR merges, the existing `cdr/<feature>/approved`, `trr/<feature>/approved`, or `release/<feature>/approved` tag moves forward to the latest approved baseline automatically.

---

## Manual updates

After a new design cycle is complete, update the feature records that humans read:

- Update the gate history table in `features/<feature>/README.md`
- Update `requirements/verification-matrix.md` with the new cycle's evidence
- Increment the schematic title block revision (for example `A` → `B`)
- Update `datasheet/specs.yaml` if measured or released values changed

---

## Traceability

The gate evidence files (`gate-evidence-cdr.md`, `gate-evidence-trr.md`, `gate-evidence-release.md`) are overwritten on each new sign-off cycle because the workflow recreates the same gate branch names. That does not lose traceability: Git history keeps every previous gate merge commit, PR discussion, approval, checklist state, and tag movement for audit purposes.
