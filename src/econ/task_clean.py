"""Build the analysis panel from the lake. Assertions document what we believe about the data."""

from pathlib import Path

from econ.config import CLEAN, LAKE
from econ.db import con


def task_clean_example_panel(
    src: Path = LAKE / "example_panel.parquet",
    produces: Path = CLEAN / "panel.parquet",
) -> None:
    df = con().sql("""
        SELECT
            state, year, y,
            first_treat,
            (first_treat > 0 AND year >= first_treat)::INT AS treat_post,
            CASE WHEN first_treat > 0 THEN year - first_treat ELSE -1000 END AS rel_time
        FROM example_panel
        ORDER BY state, year
    """).df()

    assert not df.duplicated(["state", "year"]).any(), "state-year must be unique"
    assert df["y"].notna().all(), "outcome has missing values"
    df.to_parquet(produces, index=False)
