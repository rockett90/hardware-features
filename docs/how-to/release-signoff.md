# How to perform a Final Release sign-off

## When to raise this PR

After TRR has passed and the IVV team has completed testing. All findings must be resolved or formally deferred before this gate can clear.

## Steps

1. Create a branch `signoff/<feature>/release`.
2. Open a PR using the release sign-off template:
   ```
   https://github.com/rockett90/hardware-features/compare/main...<branch>?template=release-signoff.md
   ```
3. Verify all gate tags exist in the repository:
   - `pdr/<feature>/approved`
   - `cdr/<feature>/approved`
   - `<feature>-vX.Y.Z-rc.N`
4. Confirm the manufacturing pack was generated cleanly — check the `hw-release.yml` Actions run for the rc tag. Any ⛔ in the step summary means outputs are incomplete.
5. Tick every checklist item in the PR description.
6. Request lead review and approval.
7. On merge, CI creates the `release/<feature>/approved` tag automatically.

## After this gate

The `release/<feature>/approved` tag is the authorisation record for production manufacture. The release-please Release PR can then be merged to create the final `<feature>-vX.Y.Z` production tag.
