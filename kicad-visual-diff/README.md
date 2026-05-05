# kicad-visual-diff

A GitHub Action (and standalone CLI) that generates a fully self-contained, four-column HTML visual diff report comparing KiCad schematic (and optionally PCB) files between two git refs.

The report embeds all images as base64 PNGs and includes an interactive **zoom/pan** control for each image (powered by [panzoom v4.5.1](https://github.com/timmywil/panzoom), MIT licence, hardcoded in the script — no CDN, no network calls).

> **Docker image used:** `ghcr.io/inti-cmnb/kicad10_auto_full@sha256:81621e501169e66dc051a65a0e575c0ab2854f69a121f1f9d97aad2b0d4c0257` (pinned digest)

---

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `feature` | ✅ | — | Feature name (e.g. `buck-converter-5v`) |
| `base-ref` | ❌ | `main` | Base git ref to compare against |
| `output-dir` | ❌ | `/tmp/kicad-visual-diff` | Output directory for diff report files |
| `pcb` | ❌ | `false` | Also diff PCB layers (`true`/`false`) |

## Outputs

| Output | Description |
|---|---|
| `report-path` | Path to the generated `diff-report.html` |
| `comment-path` | Path to the generated `comment.md` |
| `changes-path` | Path to the generated `changes.json` |
| `metadata-path` | Path to the generated `metadata.json` |

---

## Example workflow usage

```yaml
name: KiCad Visual Diff on PR

on:
  pull_request:
    paths:
      - 'features/**'

jobs:
  visual-diff:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run KiCad Visual Diff
        id: diff
        uses: rockett90/hardware-features/kicad-visual-diff@main
        with:
          feature: buck-converter-5v
          base-ref: main
          output-dir: /tmp/kicad-diff-output
          pcb: 'false'

      - name: Upload diff report
        uses: actions/upload-artifact@v4
        with:
          name: visual-diff-report
          path: ${{ steps.diff.outputs.report-path }}
          retention-days: 90

      - name: Post PR comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const comment = fs.readFileSync('${{ steps.diff.outputs.comment-path }}', 'utf8');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: comment,
            });
```

---

## Standalone CLI usage

The underlying script (`scripts/ci/kicad-visual-diff.py`) can be run directly outside CI.

**Dependencies:** Python 3.9+, [Pillow](https://pillow.readthedocs.io/), [cairosvg](https://cairosvg.org/), and `kicad-cli` on PATH (or run inside the KiCad Docker image).

```bash
# Extract base ref into /tmp/base
git archive origin/main -- features/buck-converter-5v/ | tar -x -C /tmp/base

# Extract head into /tmp/head
git archive HEAD -- features/buck-converter-5v/ | tar -x -C /tmp/head

# Run the diff
python3 scripts/ci/kicad-visual-diff.py \
  --base-dir /tmp/base \
  --head-dir /tmp/head \
  --feature buck-converter-5v \
  --output-dir /tmp/diff-output

# Open the report
open /tmp/diff-output/diff-report.html
```

Or using the pinned KiCad Docker image:

```bash
docker run --rm \
  -v "$(pwd)/scripts:/scripts" \
  -v "/tmp/base:/kv-base" \
  -v "/tmp/head:/kv-head" \
  -v "/tmp/diff-output:/kv-out" \
  -e BASE_SHA="$(git rev-parse origin/main)" \
  -e HEAD_SHA="$(git rev-parse HEAD)" \
  "ghcr.io/inti-cmnb/kicad10_auto_full@sha256:81621e501169e66dc051a65a0e575c0ab2854f69a121f1f9d97aad2b0d4c0257" \
  python3 /scripts/ci/kicad-visual-diff.py \
    --base-dir /kv-base \
    --head-dir /kv-head \
    --feature buck-converter-5v \
    --output-dir /kv-out
```

### Outputs

| File | Description |
|---|---|
| `diff-report.html` | Fully self-contained HTML report with zoom/pan on each image |
| `metadata.json` | Feature name, SHAs, sheet counts, warnings |
| `comment.md` | Markdown summary suitable for a PR comment |
| `changes.json` | Structured change list (populated by the semantic diff step) |
