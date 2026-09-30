#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

LOCAL_CONFIG_FILE="${RESEARCHCHEMBENCH_LOCAL_CONFIG:-$ROOT_DIR/config.local.env}"
if [[ -f "$LOCAL_CONFIG_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$LOCAL_CONFIG_FILE"
  set +a
fi

ENV_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT_DIR/.envs}"
FRAMEWORK_ENV="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-$ENV_ROOT/researchchembench}"
PYTHON="$FRAMEWORK_ENV/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  echo "ResearchChemBench framework environment is missing: $FRAMEWORK_ENV" >&2
  echo "Build it with: bash chemistry_toolbox/scripts/setup_toolbox_env.sh" >&2
  exit 2
fi

export RESEARCHCHEMBENCH_ENV_ROOT="$ENV_ROOT"
# Match the pilot launcher: these paths are part of the frozen MCP runtime
# environment and must be identical when an existing run is resumed.
export PATH="$FRAMEWORK_ENV/bin:$PATH"
export LD_LIBRARY_PATH="$FRAMEWORK_ENV/lib:${LD_LIBRARY_PATH:-}"

usage() {
  cat <<'EOF'
ResearchChemBench persistent evaluation submission

Usage:
  bash scripts/submit_evaluation.sh submit [OPTIONS] TASK_TYPE/PAPER_ID [TASK_TYPE/PAPER_ID ...]
  bash scripts/submit_evaluation.sh status  --run-root PATH
  bash scripts/submit_evaluation.sh follow  --run-root PATH [--interval SECONDS]
  bash scripts/submit_evaluation.sh summary --run-root PATH
  bash scripts/submit_evaluation.sh attach  --session NAME
  bash scripts/submit_evaluation.sh stop    --session NAME

Submit options:
  --recovery                    Legacy persistence flag (Codex local saves by default).
  --resume / --no-resume         Enable/disable bounded automatic session recovery.
  --agent NAME                  Agent framework preset. Default: opencode.
  --model MODEL                 Agent model. Default: deepseek-v4-flash.
  --judge-model MODEL           Judge model. Default: same as --model.
  --timeout-seconds N           Per-task Agent wall time. Default: 90000.
  --compute-action-timeout-seconds N
                                Fixed timeout for compute Actions/jobs. Default: 86400.
  --fast-action-timeout-seconds N
                                Fixed timeout for fast/data Actions. Default: 86400.
  --mcp-tool-timeout-seconds N  MCP client deadline per tool call. Default: 86700.
  --job-event-settle-seconds N  Stable notification window after job events. Default: 60.
  --available-cpu-cores N       CPU cores available to each task. Default: 48.
  --available-memory-mb N       Memory available to each task, in MiB. Default: 204800.
  --available-gpu-count N       GPUs available to each task. Default: 0.
  --max-turns N                 Maximum Agent turns. Default: 600.
  --max-concurrent-runs N       Concurrent task runs. Default: 1.
  --repeats N                   Repetitions per task. Default: 1.
  --workspaces-dir PATH         Submission root. Default: workspaces/submissions/<UTC>.
  --session NAME                tmux session name. Default: derived from UTC time.
  --tool-discovery-mode MODE    progressive or full. Default: progressive.
  --execution-mode MODE         local or distributed. Default: local.
  --distributed-transport TYPE  ssh or sandbox. Default: ssh.
  --distributed-inventory PATH  Inventory for the selected distributed transport.
  --progress-max-chars N        Per-field live-log truncation. Default: 600.
  --progress-console            Mirror detailed progress into launcher.log.
  --no-score                    Do not call the Judge.
  --foreground                  Run in this terminal instead of tmux.
  --follow                      After tmux submission, display compact live progress.
  --dry-run                     Validate and print the planned runs without execution.

Status/follow/summary options:
  --run-root PATH               Submission root printed by the submit command.
  --interval N                  Follow refresh interval. Default: 10 seconds.

Examples:
  bash scripts/submit_evaluation.sh submit autonomous_research/paper_2aca1dd116799b28

  bash scripts/submit_evaluation.sh submit \
    --model deepseek-v4-flash \
    --judge-model deepseek-v4-flash \
    --timeout-seconds 90000 \
    --max-turns 600 \
    --follow \
    autonomous_research/paper_A paper_reproduction/paper_A

  bash scripts/submit_evaluation.sh status --run-root workspaces/submissions/20260727_120000
  bash scripts/submit_evaluation.sh attach --session rcb_20260727_120000
EOF
}

require_value() {
  local option="$1"
  local value="${2:-}"
  if [[ -z "$value" ]]; then
    echo "Error: $option requires a value." >&2
    exit 2
  fi
}

require_positive_integer() {
  local option="$1"
  local value="$2"
  if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: $option must be a positive integer; received '$value'." >&2
    exit 2
  fi
}

require_nonnegative_integer() {
  local option="$1"
  local value="$2"
  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    echo "Error: $option must be a non-negative integer; received '$value'." >&2
    exit 2
  fi
}

latest_batch_dir() {
  local run_root="$1"
  if [[ ! -d "$run_root/runs/cli_runs" ]]; then
    return 0
  fi
  find "$run_root/runs/cli_runs" -mindepth 1 -maxdepth 1 -type d -name 'batch_*' \
    -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-
}

print_status() {
  local run_root="$1"
  local batch_dir
  batch_dir="$(latest_batch_dir "$run_root")"
  "$PYTHON" - "$run_root" "$batch_dir" <<'PY'
import json
import os
import sys
from pathlib import Path

from evaluation.provenance.progress_snapshot import build_progress_snapshot, format_progress_summary

run_root = Path(sys.argv[1]).resolve()
batch_dir = Path(sys.argv[2]).resolve() if sys.argv[2] else None
submission = {}
submission_path = run_root / "submission.json"
if submission_path.is_file():
    submission = json.loads(submission_path.read_text(encoding="utf-8"))
if submission.get("error"):
    print("Submission failure: " + json.dumps(submission["error"], ensure_ascii=False))
tasks = list(submission.get("tasks") or [])
records = {}
if batch_dir and batch_dir.is_dir():
    for workspace in sorted(path for path in batch_dir.iterdir() if path.is_dir()):
        meta_path = workspace / "_meta.json"
        if not meta_path.is_file():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        task_key = f"{meta.get('task_type', '')}/{meta.get('paper_id', '')}"
        score = {}
        if (workspace / "_score.json").is_file():
            score = json.loads((workspace / "_score.json").read_text(encoding="utf-8"))
        try:
            progress = build_progress_snapshot(workspace)
            tokens = progress["usage"]
            accounting_status = tokens.get("accounting_status", "unavailable")
        except Exception:
            tokens = {}
            progress = None
            accounting_status = "unavailable"
        records.setdefault(task_key, []).append(
            {
                "status": progress.get("run_status") if progress else meta.get("status", "unknown"),
                "run_id": meta.get("run_id"), "workspace": str(workspace),
                "duration": meta.get("duration_seconds"),
                "score": score.get("score"),
                "score_max": score.get("score_max"),
                "tools": progress.get("tool_call_count") if progress else None,
                "failed_tools": meta.get("failed_tool_calls"),
                "tokens": None if accounting_status == "unavailable" else tokens.get("total_tokens"),
                "progress": progress,
                "accounting_status": accounting_status,
            }
        )
if batch_dir and (batch_dir / "eval_report.json").is_file():
    for row in json.loads((batch_dir / "eval_report.json").read_text()).get("runs", []):
        if not row.get("workspace"):
            key = f"{row['task_type']}/{row['paper_id']}"
            records.setdefault(key, []).append(row)
            if row.get("error"):
                print("Startup failure: " + json.dumps(row["error"], ensure_ascii=False))
ordered = [
    f"{task['task_type']}/{task['paper_id']}" if isinstance(task, dict) else str(task)
    for task in tasks
] or sorted(records)
print(f"Run root: {run_root}")
print(f"Batch: {batch_dir if batch_dir else 'not created yet'}")
print("Task                                                   Status       Duration     Score       Tools  Failed       Tokens")
print("-" * 122)
for task in ordered:
    values = records.get(task) or []
    repeats = max(1, int(submission.get("repeats") or 1))
    for repeat in range(repeats):
        row = values[repeat] if repeat < len(values) else {}
        status = str(row.get("status") or (submission.get("status") if not batch_dir else None) or "pending")
        duration = row.get("duration")
        duration_text = "-" if duration is None else f"{float(duration):.1f}s"
        score = row.get("score")
        score_text = "-" if score is None else f"{score}/{row.get('score_max')}"
        label = task if repeats == 1 else f"{task} [repeat {repeat + 1}]"
        token_text = "unavailable" if row.get("tokens") is None else format(row["tokens"], ",")
        tools_text = "?" if row.get("tools") is None else str(row["tools"])
        failures_text = "?" if row.get("failed_tools") is None else str(row["failed_tools"])
        print(
            f"{label[:54]:54} {status[:12]:12} {duration_text:12} "
            f"{score_text:11} {tools_text:>5} "
            f"{failures_text:>7} {token_text:>12}"
        )
import shlex
for task_records in records.values():
    for record in task_records:
        if record.get("run_id"):
            print("Workspace: " + record["workspace"])
            if record.get("progress"):
                print(format_progress_summary(record["progress"]))
            for operation in ("status", "cancel", "resume"):
                print(operation + ": " + shlex.join(["bash", "scripts/submit_evaluation.sh", operation,
                    "--run-root", str(run_root), "--run-id", record["run_id"]]))
results_path = batch_dir / "results.json" if batch_dir else None
if results_path and results_path.is_file():
    result = json.loads(results_path.read_text(encoding="utf-8"))
    summary = result.get("summary") or {}
    print("\nSaved batch summary (current controller status shown above):")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
PY
}

command="${1:-}"
if [[ -z "$command" || "$command" == "-h" || "$command" == "--help" ]]; then
  usage
  exit 0
fi
shift

if [[ "$command" =~ ^(status|resume|pause|cancel|reconcile)$ && " $* " == *" --run-id "* ]]; then
  exec "$PYTHON" "$ROOT_DIR/scripts/manage_evaluation_run.py" "$command" "$@"
fi

case "$command" in
  submit|create)
    agent="opencode"
    model="deepseek-v4-flash"
    model_explicit=false
    judge_model=""
    timeout_seconds=90000
    compute_action_timeout_seconds=86400
    fast_action_timeout_seconds=86400
    mcp_tool_timeout_seconds=86700
    job_event_settle_seconds="${RESEARCHCHEMBENCH_JOB_EVENT_SETTLE_SECONDS:-60}"
    job_event_max_batch_seconds="${RESEARCHCHEMBENCH_JOB_EVENT_MAX_BATCH_SECONDS:-300}"
    job_wait_heartbeat_seconds="${RESEARCHCHEMBENCH_JOB_WAIT_HEARTBEAT_SECONDS:-}"
    job_internal_poll_interval_seconds="${RESEARCHCHEMBENCH_JOB_INTERNAL_POLL_INTERVAL_SECONDS:-2}"
    job_failure_tail_chars="${RESEARCHCHEMBENCH_JOB_FAILURE_TAIL_CHARS:-2000}"
    available_cpu_cores=48
    available_memory_mb=204800
    available_gpu_count=0
    max_turns=600
    max_concurrent_runs=1
    repeats=1
    run_root=""
    session_name=""
    discovery_mode="progressive"
    execution_mode="local"
    distributed_transport="${RCB_DISTRIBUTED_TRANSPORT:-ssh}"
    distributed_inventory=""
    progress_max_chars=600
    progress_console=false
    score_enabled=true
    foreground=false
    follow=false
    dry_run=false
    tasks=()
    resume_option=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --resume|--no-resume)
          if [[ -n "$resume_option" && "$resume_option" != "$1" ]]; then
            echo "Error: --resume and --no-resume are mutually exclusive." >&2
            exit 2
          fi
          resume_option="$1"; shift ;;
        --recovery)
          export RESEARCHCHEMBENCH_RECOVERY_ENABLED=1; shift ;;
        --agent)
          require_value "$1" "${2:-}"; agent="$2"; shift 2 ;;
        --model)
          require_value "$1" "${2:-}"; model="$2"; model_explicit=true; shift 2 ;;
        --judge-model)
          require_value "$1" "${2:-}"; judge_model="$2"; shift 2 ;;
        --timeout-seconds)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          timeout_seconds="$2"; shift 2 ;;
        --compute-action-timeout-seconds)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          compute_action_timeout_seconds="$2"; shift 2 ;;
        --fast-action-timeout-seconds)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          fast_action_timeout_seconds="$2"; shift 2 ;;
        --mcp-tool-timeout-seconds)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          mcp_tool_timeout_seconds="$2"; shift 2 ;;
        --job-event-settle-seconds)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          job_event_settle_seconds="$2"; shift 2 ;;
        --available-cpu-cores)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          available_cpu_cores="$2"; shift 2 ;;
        --available-memory-mb)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          available_memory_mb="$2"; shift 2 ;;
        --available-gpu-count)
          require_value "$1" "${2:-}"; require_nonnegative_integer "$1" "$2"
          available_gpu_count="$2"; shift 2 ;;
        --max-turns)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          max_turns="$2"; shift 2 ;;
        --max-concurrent-runs)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          max_concurrent_runs="$2"; shift 2 ;;
        --repeats)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          repeats="$2"; shift 2 ;;
        --workspaces-dir)
          require_value "$1" "${2:-}"; run_root="$2"; shift 2 ;;
        --session)
          require_value "$1" "${2:-}"; session_name="$2"; shift 2 ;;
        --tool-discovery-mode)
          require_value "$1" "${2:-}"; discovery_mode="$2"; shift 2 ;;
        --execution-mode)
          require_value "$1" "${2:-}"; execution_mode="$2"; shift 2 ;;
        --distributed-transport)
          require_value "$1" "${2:-}"; distributed_transport="$2"; shift 2 ;;
        --distributed-inventory)
          require_value "$1" "${2:-}"; distributed_inventory="$2"; shift 2 ;;
        --progress-max-chars)
          require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"
          progress_max_chars="$2"; shift 2 ;;
        --progress-console) progress_console=true; shift ;;
        --no-score) score_enabled=false; shift ;;
        --foreground) foreground=true; shift ;;
        --follow) follow=true; shift ;;
        --dry-run) dry_run=true; foreground=true; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; tasks+=("$@"); break ;;
        -*) echo "Error: unknown submit option '$1'." >&2; exit 2 ;;
        *) tasks+=("$1"); shift ;;
      esac
    done
    if [[ "$agent" == "codex" && "$model_explicit" == false ]]; then
      model="${RCB_CODEX_MODEL:-gpt-5.6-sol}"
    fi
    if [[ ${#tasks[@]} -eq 0 ]]; then
      echo "Error: provide at least one TASK_TYPE/PAPER_ID." >&2
      exit 2
    fi
    if [[ "$discovery_mode" != "progressive" && "$discovery_mode" != "full" ]]; then
      echo "Error: --tool-discovery-mode must be progressive or full." >&2
      exit 2
    fi
    if [[ "$execution_mode" != "local" && "$execution_mode" != "distributed" ]]; then
      echo "Error: --execution-mode must be local or distributed." >&2
      exit 2
    fi
    if [[ "$distributed_transport" == "opensandbox" ]]; then
      distributed_transport="sandbox"
    fi
    if [[ "$distributed_transport" != "ssh" && "$distributed_transport" != "sandbox" ]]; then
      echo "Error: --distributed-transport must be ssh or sandbox." >&2
      exit 2
    fi
    if [[ "$execution_mode" == "distributed" ]]; then
      if [[ -z "$distributed_inventory" ]]; then
        if [[ "$distributed_transport" == "sandbox" ]]; then
          distributed_inventory="${RCB_DISTRIBUTED_SANDBOX_INVENTORY:-}"
        else
          distributed_inventory="${RCB_DISTRIBUTED_WORKER_INVENTORY:-}"
        fi
      fi
      if [[ -z "$distributed_inventory" ]]; then
        echo "Error: distributed mode requires an inventory for transport=$distributed_transport." >&2
        exit 2
      fi
      export RCB_DISTRIBUTED_TRANSPORT="$distributed_transport"
      export RCB_DISTRIBUTED_INVENTORY="$distributed_inventory"
    fi
    if (( fast_action_timeout_seconds > compute_action_timeout_seconds )); then
      echo "Error: --fast-action-timeout-seconds cannot exceed --compute-action-timeout-seconds." >&2
      exit 2
    fi
    if (( mcp_tool_timeout_seconds <= compute_action_timeout_seconds )); then
      echo "Error: --mcp-tool-timeout-seconds must exceed --compute-action-timeout-seconds." >&2
      exit 2
    fi
    if [[ -z "$job_wait_heartbeat_seconds" ]]; then
      job_wait_heartbeat_seconds=3600
      if (( job_wait_heartbeat_seconds >= mcp_tool_timeout_seconds )); then
        job_wait_heartbeat_seconds=$((mcp_tool_timeout_seconds - 1))
      fi
    fi
    for supervision_value in \
      "$job_event_settle_seconds" \
      "$job_event_max_batch_seconds" \
      "$job_wait_heartbeat_seconds" \
      "$job_internal_poll_interval_seconds" \
      "$job_failure_tail_chars"; do
      require_positive_integer "job supervision setting" "$supervision_value"
    done
    if (( job_event_max_batch_seconds < job_event_settle_seconds )); then
      echo "Error: job event max batch seconds must be >= settle seconds." >&2
      exit 2
    fi
    if (( job_wait_heartbeat_seconds < job_event_max_batch_seconds )); then
      echo "Error: job wait heartbeat seconds must be >= max batch seconds." >&2
      exit 2
    fi
    if (( mcp_tool_timeout_seconds <= job_wait_heartbeat_seconds )); then
      echo "Error: --mcp-tool-timeout-seconds must exceed the job wait heartbeat." >&2
      exit 2
    fi
    if (( available_memory_mb < 128 )); then
      echo "Error: --available-memory-mb must be at least 128 MiB." >&2
      exit 2
    fi
    for task in "${tasks[@]}"; do
      task_type="${task%%/*}"
      paper_id="${task#*/}"
      if [[ "$task_type" == "$task" || "$paper_id" == *"/"* || ! -f "$ROOT_DIR/tasks/$task_type/$paper_id/task_info.json" ]]; then
        echo "Error: unknown task '$task'; expected TASK_TYPE/PAPER_ID." >&2
        exit 2
      fi
    done
    judge_model="${judge_model:-$model}"
    timestamp="$(date -u +'%Y%m%d_%H%M%S')"
    run_root="${run_root:-$ROOT_DIR/workspaces/submissions/$timestamp}"
    mkdir -p "$run_root"
    run_root="$(cd "$run_root" && pwd)"
    session_name="${session_name:-rcb_$timestamp}"
    if [[ ! "$session_name" =~ ^[A-Za-z0-9_.-]+$ ]]; then
      echo "Error: tmux session may contain only letters, digits, dot, underscore, and dash." >&2
      exit 2
    fi
    config_path="$run_root/evaluation_config.yaml"
    submission_path="$run_root/submission.json"
    launcher_log="$run_root/launcher.log"
    "$PYTHON" - "$config_path" "$submission_path" "$run_root" "$session_name" \
      "$agent" "$model" "$judge_model" "$timeout_seconds" "$max_turns" \
      "$max_concurrent_runs" "$repeats" "$discovery_mode" "$progress_max_chars" \
      "$progress_console" "$score_enabled" "$compute_action_timeout_seconds" \
      "$fast_action_timeout_seconds" "$mcp_tool_timeout_seconds" \
      "$available_cpu_cores" "$available_memory_mb" "$available_gpu_count" \
      "$job_event_settle_seconds" "$job_event_max_batch_seconds" \
      "$job_wait_heartbeat_seconds" "$job_internal_poll_interval_seconds" \
      "$job_failure_tail_chars" \
      "$execution_mode" "$distributed_transport" "$resume_option" \
      "${tasks[@]}" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

(
    config_path, submission_path, run_root, session_name, agent, model,
    judge_model, timeout_seconds, max_turns, max_concurrent_runs, repeats,
    discovery_mode, progress_max_chars, progress_console, score_enabled,
    compute_action_timeout_seconds, fast_action_timeout_seconds,
    mcp_tool_timeout_seconds, available_cpu_cores, available_memory_mb,
    available_gpu_count, job_event_settle_seconds, job_event_max_batch_seconds,
    job_wait_heartbeat_seconds, job_internal_poll_interval_seconds,
    job_failure_tail_chars, execution_mode, distributed_transport, resume_option, *tasks
) = sys.argv[1:]
def flag(value):
    return value.casefold() == "true"
config = {
    "name": f"submission_{Path(run_root).name}",
    "agents": [agent],
    **({"recovery_enabled": True} if os.environ.get("RESEARCHCHEMBENCH_RECOVERY_ENABLED") == "1" else {}),
    "resume": resume_option == "--resume",
    "codex_model": model if agent == "codex" else None,
    "tasks": [
        {"task_type": value.split("/", 1)[0], "paper_id": value.split("/", 1)[1]}
        for value in tasks
    ],
    "repeats": int(repeats),
    "max_concurrent_runs": int(max_concurrent_runs),
    "timeout_seconds": int(timeout_seconds),
    "compute_action_timeout_seconds": int(compute_action_timeout_seconds),
    "fast_action_timeout_seconds": int(fast_action_timeout_seconds),
    "mcp_tool_timeout_seconds": int(mcp_tool_timeout_seconds),
    "available_cpu_cores": int(available_cpu_cores),
    "available_memory_mb": int(available_memory_mb),
    "available_gpu_count": int(available_gpu_count),
    "job_event_settle_seconds": int(job_event_settle_seconds),
    "job_event_max_batch_seconds": int(job_event_max_batch_seconds),
    "job_wait_heartbeat_seconds": int(job_wait_heartbeat_seconds),
    "job_internal_poll_interval_seconds": int(job_internal_poll_interval_seconds),
    "job_failure_tail_chars": int(job_failure_tail_chars),
    "max_turns": int(max_turns),
    "tool_discovery_mode": discovery_mode,
    "execution_mode": execution_mode,
    "distributed_transport": distributed_transport if execution_mode == "distributed" else None,
    "live_progress": True,
    "progress_console": flag(progress_console),
    "progress_max_chars": int(progress_max_chars),
    "judge": {"enabled": flag(score_enabled)},
}
Path(config_path).write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
if execution_mode == "distributed":
    os.environ["RESEARCHCHEMBENCH_EXECUTION_MODE"] = "distributed"
    from chemistry_toolbox.src.distributed_pool import pool_snapshot
    pool = pool_snapshot()
    resource_budget = {
        "cpu_cores": pool["maximum_cpu_cores_per_job"],
        "memory_mb": pool["maximum_memory_mb_per_job"],
        "gpu_count": max(
            (worker["capacity"]["gpu_count"] for worker in pool["workers"]),
            default=0,
        ),
        "total_cpu_cores": pool["total_cpu_cores"],
        "total_memory_mb": pool["total_memory_mb"],
        "worker_count": pool["worker_count"],
        "scope": "per_job_on_one_compute_worker",
    }
else:
    resource_budget = {
        "cpu_cores": int(available_cpu_cores),
        "memory_mb": int(available_memory_mb),
        "gpu_count": int(available_gpu_count),
        "scope": "per_task",
    }
submission = {
    "schema_version": 1,
    "submitted_at": datetime.now(timezone.utc).isoformat(),
    "run_root": run_root,
    "tmux_session": session_name,
    "agent": agent,
    "agent_model": model,
    "judge_model": judge_model,
    "tasks": [
        {"task_type": value.split("/", 1)[0], "paper_id": value.split("/", 1)[1]}
        for value in tasks
    ],
    "repeats": int(repeats),
    "max_concurrent_runs": int(max_concurrent_runs),
    "timeout_seconds": int(timeout_seconds),
    "compute_action_timeout_seconds": int(compute_action_timeout_seconds),
    "fast_action_timeout_seconds": int(fast_action_timeout_seconds),
    "mcp_tool_timeout_seconds": int(mcp_tool_timeout_seconds),
    "job_supervision_policy": {
        "event_settle_seconds": int(job_event_settle_seconds),
        "event_max_batch_seconds": int(job_event_max_batch_seconds),
        "wait_heartbeat_seconds": int(job_wait_heartbeat_seconds),
        "internal_poll_interval_seconds": int(job_internal_poll_interval_seconds),
        "failure_tail_chars": int(job_failure_tail_chars),
        "agent_controllable": False,
    },
    "resource_budget": resource_budget,
    "execution_mode": execution_mode,
    "distributed_transport": distributed_transport if execution_mode == "distributed" else None,
    "max_turns": int(max_turns),
    "tool_discovery_mode": discovery_mode,
    "score_enabled": flag(score_enabled),
}
Path(submission_path).write_text(
    json.dumps(submission, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
PY
    eval_command=(
      bash "$ROOT_DIR/scripts/run_agent_eval.sh"
      --config "$config_path"
      --workspaces-dir "$run_root/runs"
      --opencode-model "$model"
      --judge-model "$judge_model"
      --execution-mode "$execution_mode"
    )
    if [[ "$execution_mode" == "distributed" ]]; then
      eval_command+=(--distributed-transport "$distributed_transport")
    fi
    if [[ "$score_enabled" == false ]]; then eval_command+=(--no-score); fi
    if [[ "$dry_run" == true ]]; then eval_command+=(--dry-run); fi
    echo "Submission root: $run_root"
    echo "Tasks: ${tasks[*]}"
    echo "Agent: $agent model=$model"
    echo "Judge: enabled=$score_enabled model=$judge_model"
    echo "Limits: agent=${timeout_seconds}s mcp=${mcp_tool_timeout_seconds}s compute_action=${compute_action_timeout_seconds}s fast_action=${fast_action_timeout_seconds}s max_turns=$max_turns concurrency=$max_concurrent_runs repeats=$repeats"
    echo "Job supervision: settle=${job_event_settle_seconds}s max_batch=${job_event_max_batch_seconds}s heartbeat=${job_wait_heartbeat_seconds}s poll=${job_internal_poll_interval_seconds}s failure_tail=${job_failure_tail_chars}chars"
    if [[ "$execution_mode" == "distributed" ]]; then
      echo "Compute resources: transport=$distributed_transport inventory=$RCB_DISTRIBUTED_INVENTORY"
    else
      echo "Per-task resources: cpu=${available_cpu_cores} memory=${available_memory_mb}MiB gpu=${available_gpu_count}"
    fi
    echo "Execution mode: $execution_mode"
    if [[ "$foreground" == true ]]; then
      "${eval_command[@]}" 2>&1 | tee "$launcher_log"
      exit "${PIPESTATUS[0]}"
    fi
    if tmux has-session -t "$session_name" 2>/dev/null; then
      echo "Error: tmux session already exists: $session_name" >&2
      exit 2
    fi
    printf -v quoted_command '%q ' "${eval_command[@]}"
    printf -v quoted_root '%q' "$ROOT_DIR"
    printf -v quoted_log '%q' "$launcher_log"
    tmux new-session -d -s "$session_name" \
      "cd $quoted_root && exec $quoted_command >> $quoted_log 2>&1"
    echo "Submission accepted; evaluation completion is reported separately."
    echo "tmux session: $session_name"
    echo "Launcher log: $launcher_log"
    echo "Status: bash scripts/submit_evaluation.sh status --run-root '$run_root'"
    echo "Attach: tmux attach -t '$session_name'"
    if [[ "$follow" == true ]]; then
      "$0" follow --run-root "$run_root"
    fi
    ;;

  status|follow|summary)
    run_root=""
    interval=10
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --run-root) require_value "$1" "${2:-}"; run_root="$2"; shift 2 ;;
        --interval) require_value "$1" "${2:-}"; require_positive_integer "$1" "$2"; interval="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Error: unknown $command option '$1'." >&2; exit 2 ;;
      esac
    done
    if [[ -z "$run_root" || ! -d "$run_root" ]]; then
      echo "Error: --run-root must name an existing submission directory." >&2
      exit 2
    fi
    run_root="$(cd "$run_root" && pwd)"
    if [[ "$command" == "status" ]]; then
      print_status "$run_root"
      exit 0
    fi
    if [[ "$command" == "summary" ]]; then
      batch_dir="$(latest_batch_dir "$run_root")"
      if [[ -z "$batch_dir" || ! -f "$batch_dir/results.json" ]]; then
        echo "Batch results are not available yet; showing current status."
        print_status "$run_root"
        exit 1
      fi
      "$PYTHON" -m json.tool "$batch_dir/results.json"
      exit 0
    fi
    while true; do
      printf '\n[%s]\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
      print_status "$run_root"
      batch_dir="$(latest_batch_dir "$run_root")"
      if [[ -n "$batch_dir" ]]; then
        if "$PYTHON" - "$batch_dir" <<'PYFOLLOW'
import sys
from evaluation.provenance.progress_snapshot import batch_is_active
raise SystemExit(1 if batch_is_active(sys.argv[1]) else 0)
PYFOLLOW
        then
          break
        fi
      fi
      sleep "$interval"
    done
    ;;

  attach|stop)
    session_name=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --session) require_value "$1" "${2:-}"; session_name="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Error: unknown $command option '$1'." >&2; exit 2 ;;
      esac
    done
    if [[ -z "$session_name" ]]; then
      echo "Error: --session is required." >&2
      exit 2
    fi
    if ! tmux has-session -t "$session_name" 2>/dev/null; then
      echo "Error: tmux session does not exist: $session_name" >&2
      exit 1
    fi
    if [[ "$command" == "attach" ]]; then
      exec tmux attach -t "$session_name"
    fi
    tmux send-keys -t "$session_name" C-c
    echo "SIGINT sent to tmux session $session_name; the evaluator will stop active jobs and write final metadata."
    ;;

  *)
    echo "Error: unknown command '$command'." >&2
    usage >&2
    exit 2
    ;;
esac
