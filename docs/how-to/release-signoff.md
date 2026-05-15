# How to perform a Final Release sign-off

## When to raise this PR

After TRR has passed and the IVV team has completed testing. All findings must be resolved or formally deferred before this gate can clear.

## Steps

1. Go to **Actions → Gate Sign-Off → Run workflow**, enter your feature name, and select `release`. The workflow creates `signoff/<feature>/release`, commits the gate evidence file, and opens the Release PR automatically.
2. Open the PR from the workflow summary link once the run completes. The release checklist is already filled into the PR body.
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

   Check the **Manufacturing Release** (`hw-release.yml`) workflow run triggered by the production tag for any ⛔ in the step summary — this means one or more manufacturing outputs are incomplete.

## After this gate

The `release/<feature>/approved` tag is the authorisation record for production manufacture.

The release-please Release PR (opened automatically) creates the final `<feature>-vX.Y.Z` version tag and updates the CHANGELOG. No manufacturing outputs are re-generated at that point — they were generated when this gate PR merged.
