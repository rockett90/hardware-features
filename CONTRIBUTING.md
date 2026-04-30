# Contributing

## Workflow overview
1. Raise an init PR (`init/<feature-name>`) — creates scaffold
2. Work in `artifact/<feature-name>/<description>` branches
3. Gate PRs (`signoff/<feature-name>/pdr`, `signoff/<feature-name>/cdr`, `signoff/<feature-name>/trr`)
4. Use `/render` comment to generate schematic SVG
5. Copilot AI review fires automatically on ready-for-review PRs

## Branch naming
| Type | Pattern |
|---|---|
| Init | `init/<feature-name>` |
| Artifact | `artifact/<feature-name>/<description>` |
| Gate | `signoff/<feature-name>/pdr` or `/cdr` or `/trr` |
| Finding | `finding/<feature-name>/<description>` |

## PR title format
Must follow: `type(scope): description`

Valid types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`

Scope must match a feature name defined in commitlint config.

## Commit message format
Same as PR title: `type(scope): description`

## Adding a new feature
1. Add the scope to `.github/commitlint.config.js`
2. Add the entry to `.github/release-please-config.json`
3. Raise an `init/<feature-name>` PR

## Guidelines
See `.github/guidelines/` for detailed guidance on:
- Schematic standards
- BOM standards  
- IVV standards
- Gate criteria
- Commit standards
