import json
import subprocess
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "protect_raw.sh"


def run(path: str) -> int:
    payload = json.dumps({"tool_input": {"file_path": path}})
    return subprocess.run([str(HOOK)], input=payload, text=True, capture_output=True).returncode


def test_blocks_raw():
    assert run("/proj/data/raw/x.csv") == 2


def test_blocks_output():
    assert run("/proj/output/tables/t.tex") == 2


def test_allows_src():
    assert run("/proj/src/econ/task_x.py") == 0
