#!/usr/bin/env bash
# Run one final V2 task with Codex and Judge gpt-6.1-sol/high.
set +x
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
usage() {
  echo "Usage: bash scripts/run_codex_gpt61_v2_eval.sh PAPER_ID [--dry-run]"
  echo "       bash scripts/run_codex_gpt61_v2_eval.sh --resume CASE_DIR [--repair-history] [--timeout-seconds TOTAL_SEC]"
}
if [[ ${1:-} == --help || ${1:-} == -h ]]; then usage; exit 0; fi
if [[ $# -eq 0 ]]; then usage >&2; exit 2; fi
RESUME_DIR=""
RESUME_OPTIONS=()
if [[ $1 == --resume ]]; then
  [[ $# -ge 2 && -d $2 ]] || { usage >&2; exit 2; }
  RESUME_DIR=$(cd "$2" && pwd -P)
  shift 2
  while (($#)); do
    case "$1" in
      --repair-history) RESUME_OPTIONS+=("$1"); shift ;;
      --timeout-seconds)
        [[ $# -ge 2 && $2 =~ ^[1-9][0-9]*$ ]] || { usage >&2; exit 2; }
        RESUME_OPTIONS+=("$1" "$2"); shift 2 ;;
      *) usage >&2; exit 2 ;;
    esac
  done
else
  PAPER=$1
  shift
  if [[ $# -gt 1 || ( $# -gt 0 && $1 != --dry-run ) ]]; then usage >&2; exit 2; fi
  SOURCE="$ROOT/tasks/final_v2_verified_autonomous_research/$PAPER"
  if [[ ! $PAPER =~ ^paper_[A-Za-z0-9]+$ || ! -f $SOURCE/task_info.json ]]; then
    echo "Unknown final V2 task: $PAPER" >&2; exit 2
  fi
fi

# Match the existing gpt61 deployment; set model choices after local config.
set -a
if [[ -f $ROOT/config.local.env ]]; then source "$ROOT/config.local.env"; fi
if [[ -f $ROOT/custom_agents/Arche-Harness/benchmark_adapter/gpt_test2.local.env ]]; then
  source "$ROOT/custom_agents/Arche-Harness/benchmark_adapter/gpt_test2.local.env"
fi
set +a
export RCB_CODEX_API_KEY="${ARCHE_EVAL_API_KEY:-${RCB_CODEX_API_KEY:-}}"
if [[ -z $RCB_CODEX_API_KEY && ${1:-} != --dry-run ]]; then
  echo "Missing saved API key in config.local.env or gpt_test2.local.env" >&2; exit 2
fi
export RCB_CODEX_BASE_URL="${RCB_CODEX_BASE_URL:-http://35.220.164.252:3888/v1}"
export RCB_CODEX_MODEL=gpt-6.1-sol RCB_CODEX_REASONING_EFFORT=high
export JUDGE_REASONING_EFFORT=high RESEARCHCHEMBENCH_LOCAL_CONFIG=/dev/null
PYTHON="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT/.envs}/researchchembench}/bin/python"
[[ -x $PYTHON ]] || { echo "Missing framework Python: $PYTHON" >&2; exit 2; }
OUTPUT_ROOT="$ROOT/workspaces/codex_gpt61_v2"

if [[ -n $RESUME_DIR ]]; then
  # Resume exactly the selected checkpoint, including its frozen task/model.
  RUN_DIR=$("$PYTHON" - "$RESUME_DIR" "$OUTPUT_ROOT" <<'PY'
import sys
from pathlib import Path
case, root = (Path(p).resolve(strict=True) for p in sys.argv[1:])
if case.parent != root or not case.name.startswith("paper_") or not (case / "submission.json").is_file():
    raise SystemExit("Resume requires an original paper_* result directory under " + str(root))
runs = [p.parent for p in case.glob("runs/cli_runs/batch_*/autonomous_research-*/_meta.json")]
if len(runs) != 1 or "-codex-" not in runs[0].name:
    raise SystemExit("Resume requires exactly one saved Codex run")
print(runs[0])
PY
  )
  exec bash "$ROOT/scripts/test_codex_gpt56.sh" --resume \
    --run-root "$RUN_DIR" --run-id "${RUN_DIR##*/}" "${RESUME_OPTIONS[@]}"
fi

RUN_NAME="${PAPER}_$(date -u +%Y%m%d_%H%M%S)_$("$PYTHON" -c 'import uuid; print(uuid.uuid4().hex[:8])')"
TASKS_ROOT="$OUTPUT_ROOT/.runtime/task_sources/$RUN_NAME/tasks"
# The shared runner expects final_verified_autonomous_research as its parent.
# Copy only this V2 package without rewriting any scientific/scoring content.
"$PYTHON" - "$SOURCE" "$TASKS_ROOT" <<'PY'
import json
import shutil
import socket
import sys
from pathlib import Path
from evaluation.contracts import validate_task_package
source, root = map(Path, sys.argv[1:])
target = root / "final_verified_autonomous_research" / source.name
shutil.copytree(source, target)
validation = validate_task_package(target)
if validation.status != "passed":
    raise SystemExit(f"Invalid task package: {source}: {validation.findings}")
(root.parent / "source.json").write_text(json.dumps({
    "source_task": str(source), "staged_task": str(target), "host": socket.gethostname(),
    "package_content_sha256": json.loads((target / "package_manifest.json").read_text())["package_content_sha256"],
}, ensure_ascii=False, indent=2) + "\n")
PY

# An explicit fresh output directory prevents accidental selection of old runs.
# --resume enables the runner's bounded automatic recovery within this new run.
exec bash "$ROOT/scripts/test_codex_gpt56.sh" "$PAPER" --tasks-root "$TASKS_ROOT" \
  --output-dir "$OUTPUT_ROOT/$RUN_NAME" --resume --judge-model gpt-6.1-sol "$@"
