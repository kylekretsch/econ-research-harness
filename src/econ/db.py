"""DuckDB connection with every Parquet file in data/lake and data/clean exposed as a view.

    from econ.db import con
    con().sql("SELECT state, AVG(y) FROM example_panel GROUP BY 1").show()
"""

import duckdb

from econ.config import CLEAN, LAKE


def con() -> duckdb.DuckDBPyConnection:
    c = duckdb.connect()
    for folder in (LAKE, CLEAN):
        for f in sorted(folder.glob("*.parquet")):
            c.execute(f"CREATE OR REPLACE VIEW {f.stem} AS SELECT * FROM read_parquet('{f.as_posix()}')")
    return c
