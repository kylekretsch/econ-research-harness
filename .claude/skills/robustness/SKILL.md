---
name: robustness
description: Build a robustness/sensitivity suite for an existing main estimate (alternative samples, specs, controls, clustering, placebo, pre-trends, randomization inference, specification curve). Use after a main result exists, or when the user asks "is this robust?".
---

# Robustness suite

Create `src/econ/task_robustness_<topic>.py` producing `output/tables/robustness_<topic>.tex` and, where useful,
`output/figures/speccurve_<topic>.pdf`.

Pick the checks that match the design — and say which ones you skipped and why:

- **Specification:** add/remove controls; alternative FE structures; functional form (logs, IHS, Poisson via `pf.fepois`).
- **Sample:** drop outliers/top 1%; balanced panel only; exclude early/late adopters; drop each large unit/state (leave-one-out).
- **Inference:** alternative clustering (two-way, coarser level); wild cluster bootstrap; randomization inference (permute treatment, seed fixed).
- **Placebos:** fake treatment timing; unaffected outcomes; untreated groups.
- **Design-specific:** pre-trend tests and HonestDiD-style sensitivity (DiD); weak-IV robust CIs (IV); bandwidth/kernel/donut (RD).
- **Specification curve:** loop over the defensible choices, plot sorted estimates with CIs.

Summarize in `notes/research_log.md`: which checks moved the estimate, by how much, and the interpretation.
Do not drop checks that "fail" — report them.
