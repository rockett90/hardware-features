# How to perform a Final Release sign-off

## When to raise this PR

After TRR has passed and the IVV team has completed testing. All findings must be resolved or formally deferred before this gate can clear.

## Steps

1. Create a branch `signoff/<feature>/release`.
2. Open a PR — the release sign-off checklist auto-fills into the PR body within seconds.
3. Verify all gate tags exist in the repository:
   - `cdr/<feature>/approved`
   - `trr/<feature>/approved`
4. Tick every checklist item in the PR description.
5. Request lead review and approval.
6. On merge, CI automatically:
   - Creates the `release/<feature>/approved` tag
   - Generates the datasheet PDF and FPTCS notes PDF
   - Collects all release documents and creates a GitHub Release at the tag
   - Runs KiBot to generate manufacturing outputs (gerbers, drill, BOM, CPL, schematic PDF)

   Check the `gate-tags.yml` Actions run (release-gate job) for any ⛔ in the step summary — this means one or more outputs are incomplete.

## After this gate

The `release/<feature>/approved` tag is the authorisation record for production manufacture.

The release-please Release PR (opened automatically) creates the final `<feature>-vX.Y.Z` version tag and updates the CHANGELOG. No manufacturing outputs are re-generated at that point — they were generated when this gate PR merged.

## Documentation-only releases

A documentation-only change (datasheet correction, typo fix) does not require repeating PDR, CDR, TRR, or IV&V. See [docs/how-to/second-design-cycle.md](second-design-cycle.md) for the documentation-only release path.
