#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TASKS=(
  Electron_Isodensity_Reproduction_01_Method_Selection
  Electron_Isodensity_Reproduction_02_Conformer_Effects
  Electron_Isodensity_Reproduction_03_Cutoff_Calibration
  Electron_Isodensity_Reproduction_04_Blind_Prediction
  Electron_Isodensity_Reproduction_05_End_to_End
)

usage() {
  cat <<'EOF'
Run one Electron Isodensity guided-reproduction benchmark task.

Usage:
  bash scripts/submit_electron_isodensity_reproduction.sh --task TASK_ID [OPTIONS]

Options:
  --task TASK_ID            Required; one Electron_Isodensity_Reproduction_01..05 task.
  --agent-model MODEL       Default: deepseek-v4-flash.
  --judge-model MODEL       Default: deepseek-v4-flash.
  --timeout-seconds N       Default: 21600.
  --max-turns N             Default: 400.
  --dry-run                 Validate and print the planned run without API calls.
  -h, --help                Show this help.

Credentials and API endpoints are loaded by scripts/run_agent_eval.sh from
config.local.env or RESEARCHCHEMBENCH_LOCAL_CONFIG.
EOF
}

log_info() {
  printf '[RCB][%s][EIS-REPRO] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*"
}

TASK_ID=""
AGENT_MODEL="deepseek-v4-flash"
JUDGE_MODEL="deepseek-v4-flash"
TIMEOUT_SECONDS=21600
MAX_TURNS=400
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task)
      TASK_ID="${2:-}"
      shift 2
      ;;
    --agent-model)
      AGENT_MODEL="${2:-}"
      shift 2
      ;;
    --judge-model)
      JUDGE_MODEL="${2:-}"
      shift 2
      ;;
    --timeout-seconds)
      TIMEOUT_SECONDS="${2:-}"
      shift 2
      ;;
    --max-turns)
      MAX_TURNS="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown option '$1'." >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$TASK_ID" ]]; then
  echo "Error: --task is required." >&2
  usage >&2
  exit 2
fi
valid=0
for candidate in "${TASKS[@]}"; do
  if [[ "$TASK_ID" == "$candidate" ]]; then
    valid=1
    break
  fi
done
if [[ "$valid" -ne 1 ]]; then
  echo "Error: unsupported Electron Isodensity reproduction task: $TASK_ID" >&2
  exit 2
fi
if [[ ! "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ || ! "$MAX_TURNS" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: timeout and max turns must be positive integers." >&2
  exit 2
fi

agent_slug="${AGENT_MODEL//\//_}"
judge_slug="${JUDGE_MODEL//\//_}"
output_root="$ROOT_DIR/workspaces/electron_isodensity_reproduction/agent_${agent_slug}__judge_${judge_slug}"
timestamp="$(date -u +%Y%m%d_%H%M%S)"
log_dir="$output_root/logs"
mkdir -p "$log_dir"

command=(
  bash "$ROOT_DIR/scripts/run_agent_eval.sh"
  --agent opencode
  --task "$TASK_ID"
  --opencode-model "$AGENT_MODEL"
  --judge-model "$JUDGE_MODEL"
  --workspaces-dir "$output_root"
  --timeout-seconds "$TIMEOUT_SECONDS"
  --max-turns "$MAX_TURNS"
  --tool-discovery-mode progressive
  --live-progress
  --no-progress-console
  --progress-max-chars 1200
)

log_info "Task:        $TASK_ID"
log_info "Agent:       $AGENT_MODEL"
log_info "Judge:       $JUDGE_MODEL"
log_info "Output root: $output_root"
log_info "Timeout:     $TIMEOUT_SECONDS seconds"
log_info "Max turns:   $MAX_TURNS"

if [[ "$DRY_RUN" -eq 1 ]]; then
  "${command[@]}" --dry-run
  exit 0
fi

"${command[@]}" 2>&1 | tee "$log_dir/${TASK_ID}_${timestamp}.log"
