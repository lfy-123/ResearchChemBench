#!/usr/bin/env bash
# Run on the original server: finalize recorded Codex completion, then score.
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
if [[ $# != 1 ]]; then
  echo "Usage: bash scripts/finalize_small_molecules_gpt61.sh CASE_DIR" >&2
  exit 2
fi
PYTHON="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT/.envs}/researchchembench}/bin/python"
CASE_DIR=$(realpath "$1")
cd "$ROOT"
RUN_DIR=$("$PYTHON" - "$CASE_DIR" "$ROOT" <<'PY'
import sys
from pathlib import Path
case, root = map(Path, sys.argv[1:])
expected = (root / "workspaces/codex_gpt61_high_small_molecules_v3").resolve()
if case.parent != expected or not case.name.startswith("paper_") or not (case / "submission.json").is_file():
    raise SystemExit("Expected an existing GPT-6.1-sol v3 case directory")
runs = list(case.glob("runs/cli_runs/batch_*/autonomous_research-*-codex-*/_meta.json"))
if len(runs) != 1:
    raise SystemExit("Expected exactly one saved Codex run")
print(runs[0].parent)
PY
)
"$PYTHON" -m evaluation.execution.control finalize \
  --run-root "$RUN_DIR" --run-id "${RUN_DIR##*/}" \
  --apply --stop-completed-processes --no-score
# The completed-run resume branch only continues Judge, loading the existing API settings.
exec bash "$ROOT/scripts/run_small_molecules_gpt61_eval.sh" codex --resume "$CASE_DIR"
