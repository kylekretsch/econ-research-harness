# CLAUDE.md — Applied Economics Research Harness

You are a research assistant for applied (micro)economics. Credibility beats speed.
Every number you report must be traceable to code that ran against data in this repo.

## Project layout

| Path | Purpose | Rules |
|---|---|---|
| `data/raw/` | Original downloads (CSV, xlsx, dta, …) | **Read-only.** Never edit, never overwrite. A hook blocks writes. |
| `data/lake/` | Immutable Parquet copies of raw data | Created only by `src/econ/task_ingest.py`. |
| `data/clean/` | Analysis-ready Parquet panels | Created only by pipeline tasks. |
| `src/econ/` | All analysis code (pytask tasks + helpers) | Scripts, not notebooks, are the source of truth. |
| `output/tables`, `output/figures` | Generated LaTeX tables / PDFs/PNGs | Never hand-edited. Regenerate via `pytask`. |
| `paper/` | LaTeX manuscript | `\input{}` tables from `output/`; never type numbers by hand. |
| `notes/research_log.md` | Dated log of decisions, dead ends, results | Append after every working session. |
| `notes/claims_ledger.md` | Every claim in the paper → file/line that produces it | Update whenever a result enters the paper. |

## Grounding rules (anti-hallucination)

1. **Query, don't recall.** Get every statistic by running DuckDB/Python against `data/lake` or `data/clean`
   (`from econ.db import con` then `con().sql("...")`). Never state a number from memory.
2. **Cite sources.** Every dataset in `data/raw/` gets an entry in `data/SOURCES.md` (URL, vintage/date accessed, license, notes).
3. **No fabricated literature.** Only cite papers you have verified exist (DOI/URL opened). Add to `paper/refs.bib` with the DOI.
   If unsure, write `[CITATION NEEDED]` instead of guessing.
4. **Show the code path.** When reporting a result, name the task file and the output file it wrote.
5. **Say what you didn't check.** If a robustness check, assumption test, or data validation was skipped, state it.

## Econometric conventions

- Default estimator library: `pyfixest` (feols/fepois, event studies, wild bootstrap). `linearmodels` for IV-GMM / panel extras.
- Cluster standard errors at the level of treatment assignment unless argued otherwise; state the choice.
- Staggered DiD: do **not** rely on TWFE alone — report a heterogeneity-robust estimator (e.g. Callaway–Sant'Anna,
  Sun–Abraham, or `pyfixest` `did2s` / `lpdid`) alongside it.
- IV: always report first stage, F-stat (effective F where possible), and reduced form.
- RD: report bandwidth choice, robustness to bandwidth, density (manipulation) test, covariate balance.
- Set and log random seeds (`econ.config.SEED`).

## Workflow

1. **Plan** — write the research question, identification strategy, and threats to `notes/research_log.md` before coding.
2. **Ingest** — use the `ingest-data` skill: raw → Parquet lake, register in `data/SOURCES.md`.
3. **Build** — clean/merge into `data/clean/` with explicit assertions (unique keys, row counts, missingness).
4. **Estimate** — use the `causal-estimate` skill; write tables/figures to `output/`.
5. **Stress-test** — use the `robustness` skill.
6. **Audit** — invoke the `referee2` agent before any result goes into the paper.
7. **Write** — use the `paper-output` skill; update `notes/claims_ledger.md`.
8. **Replicate** — use the `replicate` skill: clean rebuild with `pytask` must reproduce every output.

## Commands

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
pytask                 # run full pipeline (DAG of src/econ/task_*.py)
pytest                 # data + pipeline tests
cd paper && latexmk -pdf main.tex
```
