#!/usr/bin/env bash
# Block Claude from writing to data/raw/ or hand-editing generated outputs.
input=$(cat)
path=$(printf '%s' "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin).get("tool_input",{}); print(d.get("file_path") or d.get("notebook_path") or "")')

case "$path" in
  */data/raw/*)
    echo "Blocked: data/raw/ is read-only. Ingest into data/lake/ via src/econ/task_ingest.py instead." >&2
    exit 2 ;;
  */output/tables/*|*/output/figures/*)
    echo "Blocked: output/ is generated. Change the pytask task that produces it and rerun pytask." >&2
    exit 2 ;;
esac
exit 0
