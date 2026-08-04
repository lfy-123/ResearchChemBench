#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIPELINE_PYTHON="${PIPELINE_PYTHON:-python}"
PIPELINE_CONFIG="${1:-$ROOT/config.json}"
PIPELINE_SUMMARY="${2:-$ROOT/runs/current/outputs/stage_02_run_summary.json}"
CONFIG_DIR="$(cd "$(dirname "$PIPELINE_CONFIG")" && pwd)"
TEMP_CONFIG="$(mktemp "$CONFIG_DIR/.stage02-config.XXXXXX.json")"

cleanup() {
  rm -f "$TEMP_CONFIG"
}
trap cleanup EXIT

"$PIPELINE_PYTHON" - "$PIPELINE_CONFIG" "$TEMP_CONFIG" <<'PY'
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2]).resolve()
config = json.loads(source.read_text(encoding="utf-8"))
config["stop_after"] = "grobid_extract"
target.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

cd "$ROOT"
"$PIPELINE_PYTHON" -m src run \
  --config "$TEMP_CONFIG" \
  --output "$PIPELINE_SUMMARY"
