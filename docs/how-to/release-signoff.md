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

## Documentation-only releases

A documentation-only change (typo fix, datasheet correction, application note update) does not require repeating PDR, CDR, TRR, or IV&V. The `release/<feature>/approved` gate tag is not re-created — it continues to point to the last hardware-authorised state.

### When to use this path

Use this path when **only** files under `datasheet/`, `requirements/`, or `decisions/` are changed, and no `.kicad_sch`, `.kicad_pcb`, or `datasheet/specs.yaml` files are modified.

### How to do it

1. Create an `artifact/<feature>/` branch and make the correction.
2. Use a `docs(<feature>):` commit message — e.g. `docs(simple-amplifier): correct output impedance value in datasheet`.
3. Open a PR, review, and merge normally.
4. Release-please will automatically queue a patch version bump and update `CHANGELOG.md`.
5. Merge the release-please Release PR when ready. This creates the `<feature>-vX.Y.Z` patch tag.
6. No manufacturing outputs are generated — `hw-release.yml` only triggers on `release/*/approved` tags.

### Changelog entry

The changelog will show:

```markdown
## [1.2.1] - 2026-05-13

### Documentation
- docs(simple-amplifier): correct output impedance value in datasheet
```

The patch version bump makes it clear no hardware design change occurred.
