---
name: causal-estimate
description: Estimate a causal effect with a standard applied-micro design (DiD / event study, staggered DiD, IV, RD, panel FE, synthetic control) in Python with pyfixest/linearmodels, writing LaTeX tables and figures to output/. Use when the user asks to estimate, regress, or test a treatment effect.
---

# Causal estimation

Before coding, write in `notes/research_log.md`: estimand, unit, treatment, outcome, identifying assumption, clustering level.

Implement as a pytask task in `src/econ/task_<topic>.py` reading from `data/clean/` and producing files in `output/`
(see `task_analysis.py` for the pattern). Use `econ.config.SEED` for any randomness.

## Design checklists

**DiD / event study** (`pyfixest`)
- `pf.feols("y ~ treat_post | unit+time", data, vcov={"CRV1": "unit"})`
- Event study: `pf.feols("y ~ i(rel_time, ref=-1) | unit+time", ...)` → plot with `.iplot()`; report joint pre-trend test.
- Staggered adoption: also report a robust estimator — `pf.did2s(...)`, `pf.lpdid(...)`, or `pf.event_study(..., estimator="did2s")`.
  Compare to TWFE and explain differences.

**IV** (`pyfixest` `y ~ exog | fe | endog ~ instr`, or `linearmodels.iv.IV2SLS`)
- Report first stage, reduced form, 2SLS; first-stage F (`fit.IV_Diag()` / effective F). Discuss exclusion restriction in prose.

**RD**
- Local linear with triangular kernel; data-driven bandwidth (`rdrobust` Python package if installed). Show binned scatter,
  bandwidth sensitivity (½×, 2×), density test, placebo cutoffs, covariate balance.

**Panel FE / OLS**
- State the comparison that identifies the coefficient. Use `pf.etable([...], type="tex")` for tables.

**Few clusters (< ~40)**: add wild cluster bootstrap (`fit.wildboottest(param=..., reps=9999, seed=SEED)`).

## Output
- Tables: `pf.etable(models, type="tex", file=...)` → `output/tables/<name>.tex` (booktabs).
- Figures: matplotlib → `output/figures/<name>.pdf`, labeled axes with units, no chart junk.
- Log the headline estimate, SE, N, clusters in `notes/research_log.md` with the producing file.
