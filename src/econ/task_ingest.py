"""Raw files -> immutable Parquet lake. One task per entry in config.RAW_SOURCES."""

from pathlib import Path

import duckdb
from pytask import task

from econ.config import LAKE, RAW, RAW_SOURCES

READERS = {
    ".csv": "read_csv_auto('{p}')",
    ".parquet": "read_parquet('{p}')",
    ".json": "read_json_auto('{p}')",
}


def _read_expr(path: Path) -> str:
    if path.suffix in READERS:
        return READERS[path.suffix].format(p=path.as_posix())
    # xlsx / dta: go through pandas
    return "df"


for name, rel in RAW_SOURCES.items():

    @task(id=name, kwargs={"src": RAW / rel, "produces": LAKE / f"{name}.parquet"})
    def task_ingest(src: Path, produces: Path) -> None:
        expr = _read_expr(src)
        if expr == "df":
            import pandas as pd

            df = pd.read_stata(src) if src.suffix == ".dta" else pd.read_excel(src)  # noqa: F841
        duckdb.sql(f"COPY (SELECT * FROM {expr}) TO '{produces.as_posix()}' (FORMAT PARQUET)")
