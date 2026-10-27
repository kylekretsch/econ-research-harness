---
name: ingest-data
description: Bring a new dataset into the project (download or user-supplied file → data/raw → Parquet lake → registered source). Use when the user mentions a new data source, FRED/BLS/Census/World Bank/IPUMS series, or drops a CSV/xlsx/dta file in.
---

# Ingest data

1. **Acquire.** Save the original file unchanged to `data/raw/<source>/<name>.<ext>` using Bash (`curl -L -o ...`),
   or confirm the user placed it there. Prefer official APIs (FRED, BLS, Census, World Bank WDI, OECD).
   Never synthesize or "fill in" data.
2. **Register.** Append to `data/SOURCES.md`:
   `| file | publisher | URL | accessed (YYYY-MM-DD) | vintage | license | notes |`
3. **Add to the lake.** Add an entry to `RAW_SOURCES` in `src/econ/config.py` (`name -> relative raw path`).
   `task_ingest.py` converts every registered file to `data/lake/<name>.parquet` with DuckDB. Run `pytask`.
4. **Profile.** Run and paste the output into `notes/research_log.md`:
   ```python
   from econ.db import con
   c = con()
   c.sql("DESCRIBE <name>").show()
   c.sql("SUMMARIZE <name>").show()
   ```
   Note: key columns, unit of observation, time coverage, missingness, obvious coding (e.g. -99 = missing).
5. **Test.** Add a test in `tests/test_data.py` asserting the primary key is unique and row count is in the expected range.
