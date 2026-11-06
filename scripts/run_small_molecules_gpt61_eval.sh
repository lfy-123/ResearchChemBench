#!/usr/bin/env bash
# One selected small-molecule task, using the existing ARCHE / Codex entrypoints.
# Usage: bash scripts/run_small_molecules_gpt61_eval.sh arche|codex PAPER_ID [--dry-run]
# Resume: bash scripts/run_small_molecules_gpt61_eval.sh arche|codex --resume CASE_DIR
# CASE_DIR is the original paper_* result directory; cross-host recovery
# requires --migrate-from-host ORIGINAL_HOST after the original host has stopped.
# New runs use model-default sampling and gpt-6.1-sol / high judging.
# Resume keeps the saved task/model and uses the current API for execution/judging.
# --dry-run validates configuration/packages only: no model, chemistry, or QEMU run.
# Prefix --v3 to require paper_science_v3 and isolate results in *_small_molecules_v3.
# New ARCHE runs use predownloaded local papers. RETRIEVAL_MODE=online restores
# guarded online search; off uses only the original public task inputs.
set +x
set -euo pipefail
umask 077
readonly CODEX_CLI_VERSION=0.165.0
readonly CLAUDE_CODE_VERSION=2.1.312
readonly GEMINI_CLI_VERSION=0.66.0
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
usage() {
  echo "Usage: bash scripts/run_small_molecules_gpt61_eval.sh [--v3] arche|codex PAPER_ID [--dry-run]"
  echo "       bash scripts/run_small_molecules_gpt61_eval.sh [--v3] arche|codex --resume CASE_DIR"
  echo "       --v3 requires V3 scoring for new runs and uses separate *_small_molecules_v3 output roots."
  echo "       Resume also accepts [--migrate-from-host ORIGINAL_HOST] [--check]"
  echo "       Resume automatically uses the configured API for execution and judging."
  echo "       --check previews API/host migration without starting the evaluation."
  echo "       Codex resume also accepts --resume-cancelled to explicitly reopen a cancelled run."
}
OUTPUT_SUFFIX=""
REQUIRED_SCORING_POLICY=""
CODEX_RECOVERY=--no-resume
ARCHE_TOP_N=2
if [[ ${1:-} == --v3 ]]; then
  OUTPUT_SUFFIX=_v3
  REQUIRED_SCORING_POLICY=paper_science_v3
  CODEX_RECOVERY=--resume
  ARCHE_TOP_N=1
  shift
fi
if [[ ${1:-} == --help || ${1:-} == -h ]]; then usage; exit 0; fi
if [[ $# -lt 2 || ( $1 != arche && $1 != codex ) ]]; then usage >&2; exit 2; fi
AGENT=$1
shift
RESUME_DIR=""
RESUME_OPTIONS=()
CODEX_RESUME_OPTIONS=()
MIGRATE_FROM_HOST=""
CHECK_MIGRATION=false
if [[ $1 == --resume ]]; then
  if [[ $# -lt 2 || ! -d $2 ]]; then usage >&2; exit 2; fi
  RESUME_DIR=$(cd "$2" && pwd -P)
  shift 2
  while (($#)); do
    case "$1" in
      --use-current-api) shift ;;  # Accepted for previously issued commands; now the default.
      --check) CHECK_MIGRATION=true; RESUME_OPTIONS+=("$1"); shift ;;
      --resume-cancelled)
        [[ $AGENT == codex ]] || { usage >&2; exit 2; }
        CODEX_RESUME_OPTIONS+=("$1"); shift ;;
      --resume-max-attempts|--resume-max-wait-seconds)
        [[ $AGENT == codex && $# -ge 2 && $2 =~ ^[0-9]+$ ]] || { usage >&2; exit 2; }
        CODEX_RESUME_OPTIONS+=("$1" "$2"); shift 2 ;;
      --migrate-from-host)
        [[ $# -ge 2 && -n $2 ]] || { usage >&2; exit 2; }
        MIGRATE_FROM_HOST=$2; RESUME_OPTIONS+=("$1" "$2"); shift 2 ;;
      *) usage >&2; exit 2 ;;
    esac
  done
else
  PAPER=$1
  shift
  if [[ $# -gt 1 || ( $# -gt 0 && $1 != --dry-run ) ]]; then usage >&2; exit 2; fi
  SOURCE="$ROOT/tasks/small_molecules_verified_autonomous_research/$PAPER"
  if [[ ! $PAPER =~ ^paper_[A-Za-z0-9]+$ || ! -f $SOURCE/task_info.json ]]; then
    echo "Unknown small-molecule task: $PAPER" >&2; exit 2
  fi
fi

# Reuse saved credentials; override model settings after loading local config.
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
export RCB_CODEX_BASE_URL="${RCB_CODEX_BASE_URL:-https://api.tensoris.ai/v1}"
export RCB_CODEX_MODEL=gpt-6.1-sol
export RCB_CODEX_REASONING_EFFORT=high
# 上下文窗口 / 自动压缩触发 token 数。仅用于 Codex 新运行；resume 沿用保存值。
if [[ $AGENT == codex ]]; then
  export RCB_CONTEXT_WINDOW_TOKENS="${RCB_CONTEXT_WINDOW_TOKENS:-500000}"
  export RCB_AUTO_COMPACT_TOKEN_LIMIT="${RCB_AUTO_COMPACT_TOKEN_LIMIT:-400000}"
fi
# This evaluation uses the same provider for execution and judging, including
# when an independent Judge was configured by another launch script.
export RCB_JUDGE_API_KEY="$RCB_CODEX_API_KEY" RCB_JUDGE_BASE_URL="$RCB_CODEX_BASE_URL"
export JUDGE_API_KEY="$RCB_CODEX_API_KEY" JUDGE_API_BASE="$RCB_CODEX_BASE_URL"
export JUDGE_MODEL_NAME="$RCB_CODEX_MODEL" JUDGE_WIRE_API=responses
export ARCHE_EVAL_JUDGE_API_KEY="$RCB_CODEX_API_KEY" ARCHE_EVAL_JUDGE_BASE_URL="$RCB_CODEX_BASE_URL"
export ARCHE_EVAL_JUDGE_MODEL="$RCB_CODEX_MODEL" ARCHE_EVAL_JUDGE_REASONING=high
export JUDGE_REASONING_EFFORT=high
export RESEARCHCHEMBENCH_LOCAL_CONFIG=/dev/null
PYTHON="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT/.envs}/researchchembench}/bin/python"
if [[ ! -x $PYTHON ]]; then echo "Missing framework Python: $PYTHON" >&2; exit 2; fi
# Preview commands do not install CLIs. Every actual run/resume must pass.
if [[ ${1:-} != --dry-run && $CHECK_MIGRATION == false ]]; then
  source "$ROOT/scripts/ensure_eval_cli_versions.sh"
  ensure_eval_cli_versions
  bash "$ROOT/scripts/install_runsc.sh"
fi
OUTPUT_ROOT="$ROOT/workspaces/${AGENT}_gpt61_high_small_molecules${OUTPUT_SUFFIX}"
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
  API_OPTIONS=()
  if [[ $CHECK_MIGRATION == false ]]; then API_OPTIONS+=(--apply); fi
  if [[ -n $MIGRATE_FROM_HOST ]]; then API_OPTIONS+=(--from-host "$MIGRATE_FROM_HOST"); fi
  for option in "${CODEX_RESUME_OPTIONS[@]}"; do
    if [[ $option == --resume-cancelled ]]; then API_OPTIONS+=(--resume-cancelled); fi
  done
  "$PYTHON" -m evaluation.execution.provider_migration --case "$RESUME_DIR" \
    --base-url "$RCB_CODEX_BASE_URL" --model "$RCB_CODEX_MODEL" "${API_OPTIONS[@]}"
  if [[ $CHECK_MIGRATION == true && -z $MIGRATE_FROM_HOST ]]; then exit 0; fi
  if [[ $AGENT == arche ]]; then
    # Completed science only needs Judge recovery; do not restart its deployment.
    if [[ $CHECK_MIGRATION == false ]] && "$PYTHON" -c \
      'import json,sys; from pathlib import Path; sys.exit(0 if json.loads((Path(sys.argv[1])/"_meta.json").read_text()).get("status")=="completed" else 1)' "$RUN_DIR"; then
      exec "$PYTHON" - "$RUN_DIR" <<'PY'
import json, sys
from pathlib import Path
from evaluation.execution.control import resume_scoring
result = resume_scoring(Path(sys.argv[1]), {}, resume_enabled=False)
print(json.dumps({k: result.get(k) for k in ("status", "evaluation_status", "score", "score_max", "error")}, ensure_ascii=False))
raise SystemExit(0 if result.get("evaluation_status") == "scored" else 2)
PY
    fi
    export ARCHE_EVAL_ENV_FILE=/dev/null ARCHE_EVAL_API_KEY="$RCB_CODEX_API_KEY"
    exec bash "$ROOT/scripts/run_arche_gpt56_eval.sh" --resume "$RESUME_DIR" "${RESUME_OPTIONS[@]}"
  else
    if [[ -n $MIGRATE_FROM_HOST ]]; then
      MIGRATION_OPTIONS=()
      if [[ $CHECK_MIGRATION == false ]]; then MIGRATION_OPTIONS+=(--apply); fi
      PATH="$(dirname "$PYTHON"):$PATH" \
      LD_LIBRARY_PATH="$(dirname "$(dirname "$PYTHON")")/lib:${LD_LIBRARY_PATH:-}" \
      "$PYTHON" -m evaluation.execution.host_migration --workspace "$RUN_DIR" \
        --from-host "$MIGRATE_FROM_HOST" "${MIGRATION_OPTIONS[@]}"
      if [[ $CHECK_MIGRATION == true ]]; then exit 0; fi
    fi
    exec bash "$ROOT/scripts/test_codex_gpt56.sh" --resume --run-root "$RUN_DIR" --run-id "${RUN_DIR##*/}" "${CODEX_RESUME_OPTIONS[@]}"
  fi
fi
RUN_NAME="${PAPER}_$(date -u +%Y%m%d_%H%M%S)_$("$PYTHON" -c 'import uuid; print(uuid.uuid4().hex[:8])')"
TASKS_ROOT="$OUTPUT_ROOT/.runtime/task_sources/$RUN_NAME/tasks"

# Both original launchers require a canonical parent directory. Copy only this
# task byte-for-byte; keep the source package, manifests and private/public split.
# Each invocation has an independent input copy and result directory.
"$PYTHON" - "$SOURCE" "$TASKS_ROOT" "$REQUIRED_SCORING_POLICY" <<'PY'
import json
import shutil
import sys
from pathlib import Path
from evaluation.contracts import validate_task_package
source, root = map(Path, sys.argv[1:3])
policy = json.loads((source / "evaluation/scoring_rules.json").read_text()).get("scoring_policy")
if sys.argv[3] and policy != sys.argv[3]:
    raise SystemExit(f"Expected {sys.argv[3]}, found {policy!r}: {source}")
target = root / "final_verified_autonomous_research" / source.name
shutil.copytree(source, target)
validation = validate_task_package(target)
if validation.status != "passed":
    raise SystemExit(f"Invalid task package: {source}: {validation.findings}")
(root.parent / "source.json").write_text(json.dumps({
    "source_task": str(source), "staged_task": str(target),
    "scoring_policy": policy,
    "package_content_sha256": json.loads((target / "package_manifest.json").read_text())["package_content_sha256"],
}, ensure_ascii=False, indent=2) + "\n")
PY

if [[ $AGENT == arche ]]; then
  export ARCHE_EVAL_ENV_FILE=/dev/null ARCHE_EVAL_API_KEY="$RCB_CODEX_API_KEY"
  export ARCHE_EVAL_MODEL="$RCB_CODEX_MODEL" ARCHE_EVAL_BASE_URL="$RCB_CODEX_BASE_URL" ARCHE_EVAL_REASONING=high
  export ARCHE_EVAL_HYPOTHESIS_PROVIDER=codex ARCHE_EVAL_JUDGE_MODEL=gpt-6.1-sol ARCHE_EVAL_JUDGE_REASONING=high
  export ARCHE_EVAL_JUDGE_ENABLED=true ARCHE_EVAL_JUDGE_WIRE_API=responses
  export ARCHE_EVAL_TASKS_ROOT="$TASKS_ROOT" ARCHE_EVAL_PAPERS="$PAPER"
  export ARCHE_EVAL_OUTPUT_ROOT="$OUTPUT_ROOT" ARCHE_EVAL_STATE_DIR="$OUTPUT_ROOT/.runtime"
  export ARCHE_EVAL_PROFILE=standard ARCHE_EVAL_REPEATS=1 ARCHE_EVAL_RESUME_DIR=""
  # Initial candidates = 3 x 2 = 6; V3 investigates Top 1, legacy Top 2.
  export ARCHE_EVAL_NUM_QUERIES=3 ARCHE_EVAL_HYPOTHESES_PER_QUERY=2
  export ARCHE_EVAL_TOP_N="$ARCHE_TOP_N" ARCHE_EVAL_PARALLEL_INVESTIGATIONS=1 ARCHE_EVAL_HYPOTHESIS_BATCHES=1
  export ARCHE_EVAL_MAX_CALLS=2000 ARCHE_EVAL_MAX_TOKENS=null ARCHE_EVAL_TOOL_RESPONSE_PROFILE=compact_v1
  export ARCHE_EVAL_RETRIEVAL_MODE="${ARCHE_EVAL_RETRIEVAL_MODE:-local}"  # 将 local 改成 online 即可开启原有网络搜索；off 表示仅使用任务公开输入。旧运行 resume 沿用原配置。
  export ARCHE_EVAL_LOCAL_CORPUS_ROOT="${ARCHE_EVAL_LOCAL_CORPUS_ROOT:-$ROOT/workspaces/arche_local_literature_20261028}"
  export ARCHE_EVAL_PAPER_SEARCH=false
  export ARCHE_EVAL_PAPER_SEARCH_TARGET="${ARCHE_EVAL_PAPER_SEARCH_TARGET:-10}"
  export ARCHE_EVAL_CPU_CORES=48 ARCHE_EVAL_MEMORY_MB=204800 ARCHE_EVAL_GPU_COUNT=0
  export ARCHE_EVAL_TIMEOUT=345600 ARCHE_EVAL_COMPUTE_TIMEOUT=86400 ARCHE_EVAL_FAST_TIMEOUT=86400 ARCHE_EVAL_MCP_TIMEOUT=345660
  export ARCHE_EVAL_EVENT_SETTLE=60 ARCHE_EVAL_EVENT_BATCH=300 ARCHE_EVAL_WAIT_HEARTBEAT=3600
  export ARCHE_EVAL_HTTP2=false ARCHE_EVAL_JSON_OBJECT=false
  export ARCHE_EVAL_INVESTIGATION_REPAIRS=1  # 返修多少次
  exec bash "$ROOT/scripts/run_arche_gpt56_eval.sh" --paper "$PAPER" "$@"
else
  # V3 gets bounded automatic recovery; an explicit unique output directory
  # still starts a fresh run and cannot auto-select an older evaluation.
  exec bash "$ROOT/scripts/test_codex_gpt56.sh" "$PAPER" --tasks-root "$TASKS_ROOT" \
    --output-dir "$OUTPUT_ROOT/$RUN_NAME" "$CODEX_RECOVERY" --judge-model gpt-6.1-sol "$@"
fi
