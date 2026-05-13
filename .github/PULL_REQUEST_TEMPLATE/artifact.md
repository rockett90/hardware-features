## Design Artifact

Use this template when raising a PR that delivers a design artifact (schematic, layout, BOM, simulation results, etc.).

### Summary

<!-- Describe what this artifact is and what design it belongs to -->

### Artifact type

- [ ] Schematic
- [ ] PCB layout
- [ ] BOM
- [ ] Simulation results
- [ ] Bring-up / test results
- [ ] Other (describe below)

### Review checklists

Use the relevant checklist(s) from [`checklists/review/`](../checklists/review/) before marking this PR ready for review:

| Artifact type | Checklist |
|---|---|
| Schematic | [`schematic-review.md`](../checklists/review/schematic-review.md) |
| PCB layout | [`pcb-review.md`](../checklists/review/pcb-review.md) |
| BOM | [`bom-review.md`](../checklists/review/bom-review.md) |
| Bring-up / test | [`bring-up-review.md`](../checklists/review/bring-up-review.md) |
| EMC | [`emc-review.md`](../checklists/review/emc-review.md) |
| Thermal | [`thermal-review.md`](../checklists/review/thermal-review.md) |
| Stress analysis | [`stress-analysis-review.md`](../checklists/review/stress-analysis-review.md) |
| FPTCS | [`fptcs-review.md`](../checklists/review/fptcs-review.md) |

### Checklist

- [ ] Relevant review checklist(s) above completed
- [ ] All review findings raised as GitHub issues or resolved
- [ ] Guideline compliance verified (see [`guidelines/`](../guidelines/))
- [ ] Simulation results attached (if applicable)
- [ ] FPTCS updated (if applicable)

### External review evidence

<!-- Optional: paste a link to SharePoint, meeting notes, or other external review records if a formal design review was held -->

**Review record:** <!-- SharePoint link or N/A -->

### Notes

<!-- Any additional context, assumptions, or known issues -->

---

> 📖 **New to this workflow?** See [docs/how-to/design-workflow.md](../docs/how-to/design-workflow.md) for the full day-to-day process guide, including branch naming, PR title format, and slash commands.
> PR title format: `feat(<feature>): description` — validated by CI.
