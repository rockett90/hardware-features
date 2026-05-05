# assets

> Static assets used across documentation — logos, diagrams, and images referenced from READMEs and docs.

---

## What belongs here

Files in this directory are referenced from READMEs and documentation using relative paths. Use this directory for:

- Logos and brand assets
- Architecture diagrams
- Screenshots used in documentation

> ⚠️ Warning: Do not put KiCad project files here. Schematics, PCB layouts, and project files belong in `features/<feature-name>/`.

---

## Structure

| Directory | Contents |
|---|---|
| `brand/` | Logo files and brand assets |
| `templates/` | Image templates used when generating documentation |

---

## Usage

Reference assets from a README using a relative path:

```markdown
![Logo](../../assets/brand/logo.png)
```

Adjust the relative path depth to match the location of the file you are editing.

---

## Adding assets

- Commit assets via a `chore/` or `docs/` PR.
- Prefer SVG over PNG for diagrams where possible — SVGs scale cleanly in GitHub Markdown.
- Keep file sizes reasonable — avoid committing large uncompressed images.
