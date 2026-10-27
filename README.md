# econ-research-harness

A [Claude Code](https://claude.com/claude-code) harness for **applied economics research** in Python + LaTeX.
It combines the practices applied economists have converged on for AI-assisted empirical work:

- **Rules file** (`CLAUDE.md`): grounding rules, econometric conventions, and an 8-step research workflow.
- **Grounded data layer**: immutable raw files → DuckDB-queryable **Parquet lake**, so every number comes from a query, not memory
  (after Matt Clancy's [anti-hallucination setup](https://homeeconomics.substack.com/p/claude-code-for-research-preventing)).
- **Referee 2 audit agent**: an independent skeptic that re-derives headline numbers and checks identification
  (after Scott Cunningham's MixtapeTools "Referee 2" protocol).
- **Skills** in the open SKILL.md format (as in [awesome-econ-ai-stuff](https://github.com/meleantonio/awesome-econ-ai-stuff)).
- **Reproducible pipeline**: a [pytask](https://pytask-dev.readthedocs.io) DAG, as in
  [econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
- **Guardrail hook**: Claude cannot write to `data/raw/` or hand-edit generated `output/`.

## What's inside

```
CLAUDE.md                     rules + workflow Claude follows
.claude/
  settings.json               permissions + PreToolUse hook
  hooks/protect_raw.sh        blocks edits to data/raw and output/
  agents/referee2.md          audit subagent
  skills/
    ingest-data/              raw → Parquet lake → SOURCES.md
    causal-estimate/          DiD/event study, staggered DiD, IV, RD, FE (pyfixest)
    robustness/               spec curve, placebos, wild bootstrap, RI
    lit-review/               verified citations only → refs.bib
    paper-output/             LaTeX with auto-generated number macros
    replicate/                clean rebuild + AEA-style REPLICATION.md
src/econ/                     pytask tasks: ingest → clean → analysis
data/{raw,lake,clean}/        + SOURCES.md registry
output/{tables,figures}/      generated, never hand-edited
paper/                        main.tex, refs.bib
notes/                        research_log, claims_ledger, referee2 reports
```

## Quick start

```bash
git clone https://github.com/kylekretsch/econ-research-harness && cd econ-research-harness
python3 -m venv .venv && source .venv/bin/activate   # Python >= 3.10; tested on 3.14
pip install -e ".[dev]"
pytask          # runs the example staggered-DiD pipeline
pytest
claude          # start Claude Code in the project
```

The bundled example is a synthetic 50-state staggered DiD with a true effect of **2.0**. TWFE and Gardner's `did2s`
both recover ≈1.93 (SE ≈0.13). Replace it with your own data via the `ingest-data` skill.

## Typical session

> "Pull state unemployment from BLS LAUS 2000–2024 and minimum wage changes, build a state-year panel, and estimate an event study.
> Then run robustness and have referee2 audit it."

Claude will ingest → register sources → build with assertions → estimate → robustness → audit → write LaTeX, logging every step in `notes/`.

## Further reading
- Paul Goldsmith-Pinkham, [Claude Code for Applied Economists](https://markusacademy.substack.com/p/claude-code-for-applied-economists) (Markus Academy)
- Scott Cunningham, [Claude Code series](https://causalinf.substack.com/s/claude-code/archive?sort=new) (Causal Inference Mixtape)
- [Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) (formerly Awesome-Agent-Skills-for-Empirical-Research): 23,000+ agent skills for empirical social science, by Stanford REAP / CoPaper.AI
