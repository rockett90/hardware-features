# .github/workflows

> GitHub Actions workflow files that power CI for every PR in this repository.

---

## Workflow reference

| Workflow | Trigger | Purpose |
|---|---|---|
| `ai-review.yml` | PR ready-for-review, `/ai-review` slash command | Runs AI analysis of schematic changes and posts findings as a PR comment |
| `commitlint.yml` | PR opened/updated | Validates that the PR title follows Conventional Commits format (`type(scope): description`) |
| `erc-drc.yml` | `/erc` or `/drc` slash command | Runs KiCad Electrical Rules Check / Design Rules Check via `kicad-cli` inside Docker — informational, does not block merge |
| `finding-labels.yml` | PR opened/updated | Automatically applies labels to `finding/<feature>/...` branches |
| `gate-check.yml` | PR opened/updated on `signoff/` branches | Validates that required gate documents and checklists are present for CDR/TRR sign-off PRs |
| `gate-tags.yml` | PR merged on a `signoff/` branch | Applies a git tag when a gate PR merges (e.g. `<feature>/cdr-v1`) |
| `hw-comment-dispatch.yml` | Issue comment created | Central slash command dispatcher — checks commenter permissions, routes commands to the correct workflow |
| `init-feature.yml` | PR merged on `init/<feature>` | Scaffolds the full feature directory structure automatically on merge |
| `kicad-diff.yml` | `/kicad-diff` slash command | Generates a four-column HTML visual diff of schematic and PCB changes vs the base branch |
| `post-checklist.yml` | PR opened/converted from draft | Posts the appropriate review checklist as a PR comment |
| `pr-checks.yml` | PR opened/updated | Validates branch name format and that the PR only touches one feature directory |
| `release-please.yml` | Push to `main` | Manages `CHANGELOG.md` and GitHub Releases automatically |
| `render.yml` | `/render` slash command | Exports schematic SVGs via KiBot, runs kicad-happy design analysis, posts results as a PR comment |
| `stale-drafts.yml` | Scheduled (weekly) | Marks draft PRs stale after 30 days of inactivity |

---

## How slash commands work

1. An engineer posts a comment on a PR containing a slash command (e.g. `/render`).
2. `hw-comment-dispatch.yml` fires on `issue_comment: created`.
3. The dispatcher checks that the commenter has **write access** to the repository. Comments from users without write access are silently ignored.
4. The dispatcher routes the command to the correct workflow via `workflow_dispatch`.
5. The target workflow runs and posts its results as a new PR comment.
6. The dispatcher reacts to the original comment:
   - 👀 immediately on receipt
   - ✅ on success
   - ❌ on failure

> 💡 Tip: If a slash command appears to do nothing, check that you have write access to the repository. Read-only access is not sufficient.

> ⚠️ Warning: The dispatcher does not validate that the command is being used on the correct branch type. Running `/erc` on an `init/` branch will attempt to run ERC on a feature that has not yet been scaffolded.

---

## Adding a new workflow

1. Add the workflow YAML file to this directory.
2. If the workflow is triggered by a slash command, add the command to `hw-comment-dispatch.yml` and document it in `CONTRIBUTING.md` section 6a.
3. Raise a `chore/` PR with lead approval.
