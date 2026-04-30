# Commit Standards

## Format
```
type(scope): short description

Optional longer body.
```

## Types
| Type | Use for |
|---|---|
| feat | New design content |
| fix | Correction to existing content |
| chore | Tooling, config, admin |
| docs | Documentation only |
| test | IVV / test content |
| refactor | Restructure without functional change |

## Scope
Must match a feature name in commitlint config.
One scope per commit — commits must not span features.
