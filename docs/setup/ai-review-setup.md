# AI Review Setup

This document explains how the automated AI schematic review works, what data it handles, and how to enable it.

---

## How it works

The AI review workflow (`ai-review.yml`) runs automatically when a PR is marked Ready for Review, and on demand via the `/ai-review` slash command.

It sends the following data to the GitHub Copilot API (`api.githubcopilot.com`):
- The schematic review instructions (`.github/agents/instructions/schematic-review.md`)
- The feature requirements YAML files (`requirements/feature-requirements.yaml`, `requirements/interface-requirements.yaml`)
- The company engineering standards (`.github/agents/context/company-standards.md`)
- The kicad-happy deterministic analysis report (generated locally in CI — not committed)

It does **not** send raw KiCad schematic files. The kicad-happy analysis report is a structured text summary of findings, not the schematic source.

---

## Data protection

All data is sent exclusively to `api.githubcopilot.com` — the GitHub Copilot inference endpoint.

| Endpoint used | Provider | Data protection |
|---|---|---|
| `api.githubcopilot.com` ✅ | GitHub (Microsoft Azure) | Covered by the GitHub Copilot Enterprise Data Protection Agreement — data is not used for model training, enterprise data boundary applies |

> ⚠️ The workflow does **not** use the GitHub Models marketplace (`models.github.com` or `api.github.com/models`). That endpoint routes to multiple third-party providers and is not covered by the Copilot Enterprise DPA. Do not change the endpoint without confirming data protection implications with the lead.

If your organisation has IP or confidentiality requirements, ensure the Copilot Enterprise DPA is in place before enabling this workflow on non-public repositories.

---

## Enabling AI review

### Organisation repository with Copilot Enterprise (recommended)

No token configuration is required for contributors. The standard `GITHUB_TOKEN` in GitHub Actions runners works automatically, provided the organisation owner has enabled the following setting:

1. Go to `https://github.com/organizations/<your-org>/settings/copilot`
2. Under **"Policies"**, enable **"Allow GitHub Actions to use Copilot"**

Once enabled, AI review works for all contributors with no per-user setup.

### Personal repository

The `GITHUB_TOKEN` in GitHub Actions on personal repositories does not have Copilot API access. To enable AI review on a personal repository:

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Create a new token from an account with an **active Copilot subscription**:
   - **Fine-grained PAT:** enable the `models: read` scope
   - **Classic PAT:** no specific scope is required, but the account must have Copilot
3. Go to `https://github.com/<your-username>/<repo>/settings/secrets/actions`
4. Add a new repository secret:
   - **Name:** `MODELS_TOKEN`
   - **Value:** the PAT you just created
5. AI review will now use this token in preference to the default `GITHUB_TOKEN`

> ℹ️ The `MODELS_TOKEN` secret, if set, takes precedence over `GITHUB_TOKEN`. On an organisation repo with Copilot Enterprise, you do not need to set `MODELS_TOKEN` — the default token is sufficient.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| HTTP 400 in AI review comment | `GITHUB_TOKEN` lacks Copilot API access | Org repo: enable "Allow GitHub Actions to use Copilot" in org settings. Personal repo: add `MODELS_TOKEN` secret |
| HTTP 401 | `MODELS_TOKEN` is invalid or expired | Regenerate the PAT and update the repository secret |
| HTTP 429 | Rate limit exceeded | Wait and re-run with `/ai-review` |
| "No KiCad files in diff" | PR has no `.kicad_sch` changes | Make a schematic change and re-run, or use `/ai-review` after adding a change |
| Review comment not posted | Workflow did not run | Check that the PR is not a draft — AI review only runs on Ready for Review PRs |

---

## Further reading

- [docs/tools.md](../tools.md) — GitHub Models API entry
- [docs/how-to/design-workflow.md](../how-to/design-workflow.md) — slash commands reference
- [GitHub Copilot Trust Center](https://resources.github.com/copilot-trust-center/) — data protection and privacy information
