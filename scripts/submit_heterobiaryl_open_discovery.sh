#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Submit the six Heterobiaryl P(V) open-discovery benchmark tasks.

Usage:
  bash scripts/submit_heterobiaryl_open_discovery.sh flash [OPTIONS]
  bash scripts/submit_heterobiaryl_open_discovery.sh pro [OPTIONS]
  bash scripts/submit_heterobiaryl_open_discovery.sh all [OPTIONS]
  bash scripts/submit_heterobiaryl_open_discovery.sh flash --task TASK_ID [OPTIONS]

Model settings:
  flash  Agent=deepseek-v4-flash, Judge=deepseek-v4-pro
  pro    Agent=deepseek-v4-pro,   Judge=deepseek-v4-pro
  all    Run flash and then pro sequentially.

Options:
  --stage all|subtasks|q6  Select all six tasks, Q1-Q5 only, or Q6 only.
                            Default: all.
  --task TASK_ID            Run exactly one open-discovery or reproduction task.
                            This bypasses --stage and is intended for serial audits.
  --judge-model MODEL       Override the scoring model. Default: deepseek-v4-pro.
  --live-progress           Record timestamped model/tool/judge progress (default).
  --no-live-progress        Disable the readable progress log.
  --progress-console        Also mirror detailed progress to the terminal.
  --no-progress-console     Keep detailed progress file-only (default).
  --progress-max-chars N    Truncate each logged progress field to N characters.
                             Default: 600; minimum: 80.
  --dry-run                 Validate and print planned runs without API calls.
  -h, --help                Show this help.

The script does not change API URLs or credentials. It uses config.local.env (or
RESEARCHCHEMBENCH_LOCAL_CONFIG) through scripts/run_agent_eval.sh.
EOF
}

log_info() {
  printf '[RCB][%s][SUBMIT] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*"
}

SETTING="${1:-}"
if [[ -z "$SETTING" || "$SETTING" == "-h" || "$SETTING" == "--help" ]]; then
  usage
  [[ -n "$SETTING" ]] && exit 0
  exit 2
fi
shift

STAGE="all"
SINGLE_TASK=""
JUDGE_MODEL="deepseek-v4-pro"
DRY_RUN=0
LIVE_PROGRESS_MODE=""
PROGRESS_CONSOLE_MODE=""
PROGRESS_MAX_CHARS=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --stage)
      if [[ $# -lt 2 ]]; then
        echo "Error: --stage requires all, subtasks, or q6." >&2
        exit 2
      fi
      STAGE="$2"
      shift 2
      ;;
    --task)
      if [[ $# -lt 2 ]]; then
        echo "Error: --task requires one task ID." >&2
        exit 2
      fi
      SINGLE_TASK="$2"
      shift 2
      ;;
    --judge-model)
      if [[ $# -lt 2 ]]; then
        echo "Error: --judge-model requires one model name." >&2
        exit 2
      fi
      JUDGE_MODEL="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --live-progress)
      LIVE_PROGRESS_MODE="--live-progress"
      shift
      ;;
    --no-live-progress)
      LIVE_PROGRESS_MODE="--no-live-progress"
      shift
      ;;
    --progress-console)
      PROGRESS_CONSOLE_MODE="--progress-console"
      shift
      ;;
    --no-progress-console)
      PROGRESS_CONSOLE_MODE="--no-progress-console"
      shift
      ;;
    --progress-max-chars)
      if [[ $# -lt 2 ]]; then
        echo "Error: --progress-max-chars requires an integer of at least 80." >&2
        exit 2
      fi
      if [[ ! "$2" =~ ^[1-9][0-9]*$ ]] || (( 10#$2 < 80 )); then
        echo "Error: --progress-max-chars requires an integer of at least 80." >&2
        exit 2
      fi
      PROGRESS_MAX_CHARS="$2"
      shift 2
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

if [[ "$SETTING" != "flash" && "$SETTING" != "pro" && "$SETTING" != "all" ]]; then
  echo "Error: model setting must be flash, pro, or all." >&2
  exit 2
fi
if [[ "$STAGE" != "all" && "$STAGE" != "subtasks" && "$STAGE" != "q6" ]]; then
  echo "Error: --stage must be all, subtasks, or q6." >&2
  exit 2
fi
if [[ -n "$SINGLE_TASK" && ! -f "$ROOT_DIR/tasks/$SINGLE_TASK/task_info.json" ]]; then
  echo "Error: task not found: $SINGLE_TASK" >&2
  exit 2
fi

SUBTASK_CONFIG="eval_configs/heterobiaryl_pv_open_discovery_subtasks.yaml"
Q6_CONFIG="eval_configs/heterobiaryl_pv_independent_discovery_q6.yaml"

run_single() {
  local agent_model="$1"
  local agent_slug="$2"
  local task_id="$3"
  local task_track="open_discovery"
  if [[ "$task_id" == Heterobiaryl_PV_Reproduction_* ]]; then
    task_track="reproduction"
  fi
  local judge_slug="${JUDGE_MODEL//\//_}"
  local output_root="$ROOT_DIR/workspaces/heterobiaryl_${task_track}/agent_${agent_slug}__judge_${judge_slug}"
  local command=(
    bash "$ROOT_DIR/scripts/run_agent_eval.sh"
    --agent opencode
    --task "$task_id"
    --opencode-model "$agent_model"
    --judge-model "$JUDGE_MODEL"
    --workspaces-dir "$output_root"
    --timeout-seconds 21600
    --max-turns 400
    --tool-discovery-mode progressive
  )
  if [[ -n "$LIVE_PROGRESS_MODE" ]]; then
    command+=("$LIVE_PROGRESS_MODE")
  fi
  if [[ -n "$PROGRESS_CONSOLE_MODE" ]]; then
    command+=("$PROGRESS_CONSOLE_MODE")
  fi
  if [[ -n "$PROGRESS_MAX_CHARS" ]]; then
    command+=(--progress-max-chars "$PROGRESS_MAX_CHARS")
  fi

  log_info "Heterobiaryl P(V) serial single-task submission"
  log_info "Task:            $task_id"
  log_info "Track:           $task_track"
  log_info "Agent model:     $agent_model"
  log_info "Judge model:     $JUDGE_MODEL"
  log_info "Output root:     $output_root"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    "${command[@]}" --dry-run
    return
  fi

  local log_dir="$output_root/logs"
  local timestamp
  timestamp="$(date -u +%Y%m%d_%H%M%S)"
  mkdir -p "$log_dir"
  "${command[@]}" 2>&1 | tee "$log_dir/${task_id}_${timestamp}.log"
}

run_batch() {
  local agent_model="$1"
  local agent_slug="$2"
  local stage_name="$3"
  local config_path="$4"
  local output_root="$ROOT_DIR/workspaces/heterobiaryl_open_discovery/agent_${agent_slug}__judge_deepseek-v4-pro"
  local command=(
    bash "$ROOT_DIR/scripts/run_agent_eval.sh"
    --config "$config_path"
    --opencode-model "$agent_model"
    --judge-model "$JUDGE_MODEL"
    --workspaces-dir "$output_root"
    --tool-discovery-mode progressive
  )
  if [[ -n "$LIVE_PROGRESS_MODE" ]]; then
    command+=("$LIVE_PROGRESS_MODE")
  fi
  if [[ -n "$PROGRESS_CONSOLE_MODE" ]]; then
    command+=("$PROGRESS_CONSOLE_MODE")
  fi
  if [[ -n "$PROGRESS_MAX_CHARS" ]]; then
    command+=(--progress-max-chars "$PROGRESS_MAX_CHARS")
  fi

  log_info "Heterobiaryl P(V) open-discovery submission"
  log_info "Stage:           $stage_name"
  log_info "Agent model:     $agent_model"
  log_info "Judge model:     $JUDGE_MODEL"
  log_info "Output root:     $output_root"
  log_info "Config:          $config_path"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    "${command[@]}" --dry-run
    return
  fi

  local log_dir="$output_root/logs"
  local timestamp
  timestamp="$(date -u +%Y%m%d_%H%M%S)"
  mkdir -p "$log_dir"
  "${command[@]}" 2>&1 | tee "$log_dir/${stage_name}_${timestamp}.log"
}

run_setting() {
  local name="$1"
  local model
  local slug
  case "$name" in
    flash)
      model="deepseek-v4-flash"
      slug="deepseek-v4-flash"
      ;;
    pro)
      model="deepseek-v4-pro"
      slug="deepseek-v4-pro"
      ;;
  esac

  if [[ -n "$SINGLE_TASK" ]]; then
    run_single "$model" "$slug" "$SINGLE_TASK"
    return
  fi

  if [[ "$STAGE" == "all" || "$STAGE" == "subtasks" ]]; then
    run_batch "$model" "$slug" "subtasks_q1_q5" "$SUBTASK_CONFIG"
  fi
  if [[ "$STAGE" == "all" || "$STAGE" == "q6" ]]; then
    run_batch "$model" "$slug" "q6_independent_open_discovery" "$Q6_CONFIG"
  fi
}

if [[ "$SETTING" == "all" ]]; then
  run_setting flash
  run_setting pro
else
  run_setting "$SETTING"
fi
