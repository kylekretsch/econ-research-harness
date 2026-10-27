"""Project paths, seed, and the registry of raw data sources."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW = DATA / "raw"
LAKE = DATA / "lake"
CLEAN = DATA / "clean"
TABLES = ROOT / "output" / "tables"
FIGURES = ROOT / "output" / "figures"

SEED = 20261027

# name -> path relative to data/raw. Each becomes data/lake/<name>.parquet via task_ingest.py.
RAW_SOURCES: dict[str, str] = {
    "example_panel": "example/example_panel.csv",
}
