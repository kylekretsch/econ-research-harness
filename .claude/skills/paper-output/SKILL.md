---
name: paper-output
description: Write or update the LaTeX paper (paper/main.tex) from generated tables and figures, keeping every number traceable. Use when drafting sections, adding tables/figures to the paper, or writing up results.
---

# Paper output

- Tables/figures enter the paper only via `\input{../output/tables/<name>.tex}` and
  `\includegraphics{../output/figures/<name>.pdf}`. Never retype numbers into tables.
- Numbers quoted in prose: generate them as LaTeX macros in a task (write `output/tables/numbers.tex` with
  `\newcommand{\mainEffect}{0.123}`) and use the macro, so text updates with the pipeline.
- For every quantitative sentence, add a row to `notes/claims_ledger.md`:
  `| claim | macro/table | producing file | date verified |`
- Style: concise economics prose; state magnitudes relative to the mean/SD of the outcome; interpret, don't just report
  significance stars; describe identification before results.
- Only `\cite{}` keys present in `paper/refs.bib` (verified via the `lit-review` skill).
- Build with `cd paper && latexmk -pdf main.tex` and fix all warnings about undefined references.
