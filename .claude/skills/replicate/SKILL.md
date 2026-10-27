---
name: replicate
description: Verify the project reproduces from scratch and prepare an AEA-style replication package. Use before sharing results, submitting, or when the user asks whether everything reproduces.
---

# Replication check

1. Record environment: `python --version`, `pip freeze > output/environment.txt`.
2. Clean rebuild: delete `data/lake/*`, `data/clean/*`, `output/tables/*`, `output/figures/*` (never `data/raw/`),
   then run `pytask` and `pytest`. Report any failure verbatim.
3. Diff outputs vs. the last committed versions (`git diff --stat output/`). Any changed number must be explained.
4. Check: seeds fixed, no absolute paths, no hard-coded numbers in `paper/`, every raw file in `data/SOURCES.md`.
5. Write/refresh `REPLICATION.md` following the AEA Data Editor template: data availability statements, computational
   requirements, run time, and a table mapping each table/figure → producing task file.
