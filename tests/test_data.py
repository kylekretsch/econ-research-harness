import pandas as pd
import pytest

from econ.config import CLEAN

PANEL = CLEAN / "panel.parquet"


@pytest.mark.skipif(not PANEL.exists(), reason="run pytask first")
def test_panel_keys_unique():
    df = pd.read_parquet(PANEL)
    assert not df.duplicated(["state", "year"]).any()


@pytest.mark.skipif(not PANEL.exists(), reason="run pytask first")
def test_panel_balanced():
    df = pd.read_parquet(PANEL)
    assert df.groupby("state").size().nunique() == 1
