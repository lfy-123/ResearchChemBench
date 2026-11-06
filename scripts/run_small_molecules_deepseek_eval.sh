#!/usr/bin/env bash
# One selected small-molecule task, using the existing ARCHE / Codex entrypoints.
# Usage: bash scripts/run_small_molecules_deepseek_eval.sh arche|codex PAPER_ID [--dry-run]
# Resume: bash scripts/run_small_molecules_deepseek_eval.sh arche|codex --resume CASE_DIR
# CASE_DIR is the original paper_* result directory; resume on its original host.
# Agent and Judge: deepseek-v4.1-flash, model-default reasoning and sampling.
# Credentials/API/model: config.local.deepseek_v41.env (gitignored, permissions 0600).
# ARCHE: 3 queries x 2 candidates = 6; Top 2 investigated sequentially; one batch.
# Both harnesses: 48 CPU / 204800 MiB per task; paper search disabled; science V2.
# Model/harness-specific result directories are independent of previous GPT runs.
# Resume keeps the original run's frozen model and judge configuration.
# --dry-run validates configuration/packages only: no model, chemistry, or QEMU run.
set +x
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
usage() {
  echo "Usage: bash scripts/run_small_molecules_deepseek_eval.sh arche|codex PAPER_ID [--dry-run]"
  echo "       bash scripts/run_small_molecules_deepseek_eval.sh arche|codex --resume CASE_DIR"
}
if [[ ${1:-} == --help || ${1:-} == -h ]]; then usage; exit 0; fi
if [[ $# -lt 2 || $# -gt 3 || ( $1 != arche && $1 != codex ) ]]; then usage >&2; exit 2; fi
AGENT=$1
shift
RESUME_DIR=""
if [[ $1 == --resume ]]; then
  if [[ $# != 2 || ! -d $2 ]]; then usage >&2; exit 2; fi
  RESUME_DIR=$(cd "$2" && pwd -P)
  shift 2
else
  PAPER=$1
  shift
  if [[ $# -gt 0 && $1 != --dry-run ]]; then usage >&2; exit 2; fi
  SOURCE="$ROOT/tasks/small_molecules_verified_autonomous_research/$PAPER"
  if [[ ! $PAPER =~ ^paper_[A-Za-z0-9]+$ || ! -f $SOURCE/task_info.json ]]; then
    echo "Unknown small-molecule task: $PAPER" >&2; exit 2
  fi
fi

# Load only the dedicated provider config; do not import the depleted provider.
CONFIG="$ROOT/config.local.deepseek_v41.env"
set -a
if [[ -f $CONFIG ]]; then source "$CONFIG"; fi
set +a
if [[ -z ${RCB_CODEX_API_KEY:-} && ${1:-} != --dry-run ]]; then
  echo "Missing RCB_CODEX_API_KEY in config.local.deepseek_v41.env" >&2; exit 2
fi
export RCB_CODEX_BASE_URL="${RCB_CODEX_BASE_URL:-https://apicz.boyuerichdata.com/v1}"
export RCB_CODEX_MODEL="${RCB_CODEX_MODEL:-deepseek-v4.1-flash}"
export RCB_CODEX_REASONING_EFFORT=default
export JUDGE_REASONING_EFFORT=default
export RESEARCHCHEMBENCH_LOCAL_CONFIG=/dev/null
PYTHON="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT/.envs}/researchchembench}/bin/python"
if [[ ! -x $PYTHON ]]; then echo "Missing framework Python: $PYTHON" >&2; exit 2; fi
OUTPUT_ROOT="$ROOT/workspaces/${AGENT}_deepseek_v41_flash_small_molecules"
if [[ -n $RESUME_DIR ]]; then
  # Resolve exactly one existing run. Never stage inputs or select a newer run
  # while resuming; native launchers validate host, liveness and saved settings.
  RUN_DIR=$("$PYTHON" - "$RESUME_DIR" "$OUTPUT_ROOT" "$AGENT" <<'PY'
import sys
from pathlib import Path
case, root = (Path(p).resolve(strict=True) for p in sys.argv[1:3])
agent = sys.argv[3]
if case.parent != root or not case.name.startswith("paper_") or not (case / "submission.json").is_file():
    raise SystemExit("Resume requires an original paper_* result directory under " + str(root))
runs = [p.parent for p in case.glob("runs/cli_runs/batch_*/autonomous_research-*/_meta.json")]
if len(runs) != 1 or ("-" + agent + "-") not in runs[0].name:
    raise SystemExit("Resume requires exactly one saved run matching the selected agent")
print(runs[0])
PY
  )
  if [[ $AGENT == arche ]]; then
    export ARCHE_EVAL_ENV_FILE=/dev/null ARCHE_EVAL_API_KEY="$RCB_CODEX_API_KEY"
    exec bash "$ROOT/scripts/run_arche_gpt56_eval.sh" --resume "$RESUME_DIR"
  else
    exec bash "$ROOT/scripts/test_codex_gpt56.sh" --resume --run-root "$RUN_DIR" --run-id "${RUN_DIR##*/}"
  fi
fi
RUN_NAME="${PAPER}_$(date -u +%Y%m%d_%H%M%S)_$("$PYTHON" -c 'import uuid; print(uuid.uuid4().hex[:8])')"
TASKS_ROOT="$OUTPUT_ROOT/.runtime/task_sources/$RUN_NAME/tasks"
CASE_OUTPUT="$OUTPUT_ROOT/$RUN_NAME"
# Keep configuration-only Codex trials out of the actual results list.
if [[ ${1:-} == --dry-run ]]; then CASE_OUTPUT="$OUTPUT_ROOT/.runtime/preflight/$RUN_NAME"; fi

# Both original launchers require a canonical parent directory. Copy only this
# task byte-for-byte; keep the source package, manifests and private/public split.
# Each invocation has an independent input copy and result directory.
"$PYTHON" - "$SOURCE" "$TASKS_ROOT" <<'PY'
import json
import shutil
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
    "source_task": str(source), "staged_task": str(target),
    "package_content_sha256": json.loads((target / "package_manifest.json").read_text())["package_content_sha256"],
}, ensure_ascii=False, indent=2) + "\n")
PY

if [[ $AGENT == arche ]]; then
  export ARCHE_EVAL_ENV_FILE=/dev/null ARCHE_EVAL_API_KEY="$RCB_CODEX_API_KEY"
  export ARCHE_EVAL_MODEL="$RCB_CODEX_MODEL" ARCHE_EVAL_BASE_URL="$RCB_CODEX_BASE_URL" ARCHE_EVAL_REASONING=default
  export ARCHE_EVAL_HYPOTHESIS_PROVIDER=codex ARCHE_EVAL_JUDGE_MODEL="$RCB_CODEX_MODEL" ARCHE_EVAL_JUDGE_REASONING=default
  export ARCHE_EVAL_JUDGE_ENABLED=true ARCHE_EVAL_JUDGE_WIRE_API=responses
  export ARCHE_EVAL_TASKS_ROOT="$TASKS_ROOT" ARCHE_EVAL_PAPERS="$PAPER"
  export ARCHE_EVAL_OUTPUT_ROOT="$OUTPUT_ROOT" ARCHE_EVAL_STATE_DIR="$OUTPUT_ROOT/.runtime"
  export ARCHE_EVAL_PROFILE=standard ARCHE_EVAL_REPEATS=1 ARCHE_EVAL_RESUME_DIR=""
  # Initial candidates = 3 x 2 = 6; investigate Top 2 sequentially, one batch.
  export ARCHE_EVAL_NUM_QUERIES=3 ARCHE_EVAL_HYPOTHESES_PER_QUERY=2
  export ARCHE_EVAL_TOP_N=2 ARCHE_EVAL_PARALLEL_INVESTIGATIONS=1 ARCHE_EVAL_HYPOTHESIS_BATCHES=1
  export ARCHE_EVAL_MAX_CALLS=2000 ARCHE_EVAL_MAX_TOKENS=null ARCHE_EVAL_TOOL_RESPONSE_PROFILE=compact_v1
  # Keep the task's no-search protocol. Some packages lack source-exclusion metadata.
  export ARCHE_EVAL_PAPER_SEARCH=false
  export ARCHE_EVAL_CPU_CORES=48 ARCHE_EVAL_MEMORY_MB=204800 ARCHE_EVAL_GPU_COUNT=0
  export ARCHE_EVAL_TIMEOUT=345600 ARCHE_EVAL_COMPUTE_TIMEOUT=86400 ARCHE_EVAL_FAST_TIMEOUT=86400 ARCHE_EVAL_MCP_TIMEOUT=345660
  export ARCHE_EVAL_EVENT_SETTLE=60 ARCHE_EVAL_EVENT_BATCH=300 ARCHE_EVAL_WAIT_HEARTBEAT=3600
  export ARCHE_EVAL_HTTP2=false ARCHE_EVAL_JSON_OBJECT=false
  exec bash "$ROOT/scripts/run_arche_gpt56_eval.sh" --paper "$PAPER" "$@"
else
  exec bash "$ROOT/scripts/test_codex_gpt56.sh" "$PAPER" --tasks-root "$TASKS_ROOT" \
    --output-dir "$CASE_OUTPUT" --no-resume --judge-model "$RCB_CODEX_MODEL" "$@"
fi
