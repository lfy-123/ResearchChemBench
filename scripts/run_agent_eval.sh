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

if [[ -x "$ROOT_DIR/.toolbox_env/bin/python" ]]; then
  export PATH="$ROOT_DIR/.toolbox_env/bin:$PATH"
  export LD_LIBRARY_PATH="$ROOT_DIR/.toolbox_env/lib:${LD_LIBRARY_PATH:-}"
elif [[ -f "$ROOT_DIR/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/.venv/bin/activate"
fi

usage() {
  cat <<'EOF'
ResearchChemBench Agent evaluation

Single-task mode:
  bash scripts/run_agent_eval.sh --agent AGENT --task TASK [OPTIONS]

Batch-config mode:
  bash scripts/run_agent_eval.sh --config FILE [OPTIONS]

Backward-compatible positional mode:
  bash scripts/run_agent_eval.sh AGENT TASK [--no-score|--dry-run]

Main options:
  -a, --agent NAME              Agent preset: mock, codex, claude, opencode.
                                Default: mock.
  -t, --task TASK_ID           Task to run, for example ChemGraph_001.
                                Default: ChemGraph_001.
  -c, --config FILE            Run all Agent/task combinations from a YAML file.
                                Cannot be combined with --agent or --task.
      --no-score               Do not call the LLM judge after the Agent finishes.
      --dry-run                Validate and print planned runs without executing them.

Runtime options:
      --timeout-seconds N      Maximum wall time for one Agent process.
                                In batch mode, a YAML timeout_seconds value wins.
      --max-turns N            Claude maximum turns and shared Agent turn setting.
                                In batch mode, a YAML max_turns value wins.
      --workspaces-dir PATH    Override the output workspace root.
      --tasks-dir PATH         Override the task directory.
      --chemgraph-root PATH    Override the ChemGraph checkout.
      --chemgraph-python PATH  Python executable used by the Chemistry MCP server.
      --mcp-tools VALUE       Compatibility option; only `all` is accepted. Every
                               task can discover the complete Action catalog.
      --tool-discovery-mode MODE
                              `progressive` (default) loads Action schemas on demand;
                               `full` preserves one MCP tool per Action for regression.
      --mcp-profiles CSV      Select runtimes for installation/probe validation only:
                               core, services, quantum, psi4, reaction, qe, cp2k,
                               periodic, phonons, md, mlip, docking. This never
                               changes the public tool catalog.

OpenCode/OpenAI-compatible options:
      --opencode-model MODEL   Example: deepseek/deepseek-v4-flash.
      --opencode-base-url URL  Example: https://api.deepseek.com/v1.
                                Supply the API credential through OPENAI_API_KEY.
      --judge-model MODEL      Override only the scoring model for this run.
                                Judge URL and key still come from local environment.

Discovery/help:
      --list-agents            Print available Agent presets and exit.
      --list-tasks             Print available tasks grouped by category and exit.
  -h, --help                   Show this help text and exit.

Scoring URL and credentials are read from environment variables:
  JUDGE_API_KEY, JUDGE_API_BASE
The default scoring model comes from JUDGE_MODEL_NAME and may be overridden with
--judge-model for one submission.

Local credentials and environment variables can be placed in:
  config.local.env
This file is automatically loaded and is excluded from version control.

Examples:
  # Local no-API harness smoke test
  bash scripts/run_agent_eval.sh --agent mock --task ChemGraph_001 --no-score

  # Real OpenCode/DeepSeek lookup task
  export OPENAI_API_KEY=...
  bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_003 --no-score

  # Validate selected backend runtimes; the Agent still sees the full toolbox
  bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_003 \
    --mcp-profiles core,services --no-score

  # Codex task with a 30-minute timeout
  bash scripts/run_agent_eval.sh --agent codex --task ChemGraph_005 \
    --timeout-seconds 1800 --no-score

  # Preview a batch without running it
  bash scripts/run_agent_eval.sh --config eval_configs/quick_opencode.yaml \
    --dry-run --no-score

  # Run all tasks described by a custom YAML configuration
  bash scripts/run_agent_eval.sh --config eval_configs/full.yaml
EOF
}

require_value() {
  local option="$1"
  local value="${2:-}"
  if [[ -z "$value" ]]; then
    echo "Error: $option requires a value." >&2
    usage >&2
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

AGENT=""
TASK=""
CONFIG=""
DRY_RUN=0
NO_SCORE=0
LIST_AGENTS=0
LIST_TASKS=0
TIMEOUT_SECONDS=""
MAX_TURNS=""
WORKSPACES_DIR=""
TASKS_DIR=""
CHEMGRAPH_ROOT_VALUE=""
CHEMGRAPH_PYTHON_VALUE=""
# Preserve values loaded from config.local.env. Command-line flags below may
# still override them, but an omitted flag must not silently discard the local
# provider/model configuration and fall back to evaluation.config defaults.
OPENCODE_MODEL_VALUE="${OPENCODE_MODEL_VALUE:-}"
OPENCODE_BASE_URL_VALUE="${OPENCODE_BASE_URL_VALUE:-}"
JUDGE_MODEL_VALUE="${JUDGE_MODEL_NAME:-}"
MCP_TOOLS_VALUE="${RESEARCHCHEMBENCH_MCP_TOOLS:-all}"
MCP_PROFILES_VALUE="${RESEARCHCHEMBENCH_MCP_PROFILES:-}"
TOOL_DISCOVERY_MODE_VALUE="${RESEARCHCHEM_TOOL_DISCOVERY_MODE:-progressive}"
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -a|--agent)
      require_value "$1" "${2:-}"
      AGENT="$2"
      shift 2
      ;;
    -t|--task)
      require_value "$1" "${2:-}"
      TASK="$2"
      shift 2
      ;;
    -c|--config)
      require_value "$1" "${2:-}"
      CONFIG="$2"
      shift 2
      ;;
    --no-score)
      NO_SCORE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --timeout-seconds)
      require_value "$1" "${2:-}"
      require_positive_integer "$1" "$2"
      TIMEOUT_SECONDS="$2"
      shift 2
      ;;
    --max-turns)
      require_value "$1" "${2:-}"
      require_positive_integer "$1" "$2"
      MAX_TURNS="$2"
      shift 2
      ;;
    --workspaces-dir)
      require_value "$1" "${2:-}"
      WORKSPACES_DIR="$2"
      shift 2
      ;;
    --tasks-dir)
      require_value "$1" "${2:-}"
      TASKS_DIR="$2"
      shift 2
      ;;
    --chemgraph-root)
      require_value "$1" "${2:-}"
      CHEMGRAPH_ROOT_VALUE="$2"
      shift 2
      ;;
    --chemgraph-python)
      require_value "$1" "${2:-}"
      CHEMGRAPH_PYTHON_VALUE="$2"
      shift 2
      ;;
    --opencode-model)
      require_value "$1" "${2:-}"
      OPENCODE_MODEL_VALUE="$2"
      shift 2
      ;;
    --opencode-base-url)
      require_value "$1" "${2:-}"
      OPENCODE_BASE_URL_VALUE="$2"
      shift 2
      ;;
    --judge-model)
      require_value "$1" "${2:-}"
      JUDGE_MODEL_VALUE="$2"
      shift 2
      ;;
    --mcp-tools)
      require_value "$1" "${2:-}"
      MCP_TOOLS_VALUE="$2"
      shift 2
      ;;
    --mcp-profiles)
      require_value "$1" "${2:-}"
      MCP_PROFILES_VALUE="$2"
      shift 2
      ;;
    --tool-discovery-mode)
      require_value "$1" "${2:-}"
      TOOL_DISCOVERY_MODE_VALUE="$2"
      shift 2
      ;;
    --list-agents)
      LIST_AGENTS=1
      shift
      ;;
    --list-tasks)
      LIST_TASKS=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        POSITIONAL+=("$1")
        shift
      done
      ;;
    -*)
      echo "Error: unknown option '$1'." >&2
      usage >&2
      exit 2
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [[ ${#POSITIONAL[@]} -gt 2 ]]; then
  echo "Error: at most two positional arguments are allowed: AGENT TASK." >&2
  exit 2
fi
if [[ -n "$CONFIG" && ( -n "$AGENT" || -n "$TASK" || ${#POSITIONAL[@]} -gt 0 ) ]]; then
  echo "Error: --config cannot be combined with --agent, --task, or positional arguments." >&2
  exit 2
fi

if [[ -z "$CONFIG" ]]; then
  AGENT="${AGENT:-${POSITIONAL[0]:-mock}}"
  TASK="${TASK:-${POSITIONAL[1]:-ChemGraph_001}}"
fi

export CHEMGRAPH_ROOT="${CHEMGRAPH_ROOT_VALUE:-${CHEMGRAPH_ROOT:-$ROOT_DIR/../ChemGraph}}"
export CHEMGRAPH_PYTHON="${CHEMGRAPH_PYTHON_VALUE:-${CHEMGRAPH_PYTHON:-$(command -v python)}}"

if [[ -n "$TIMEOUT_SECONDS" ]]; then
  export RESEARCHCHEMBENCH_AGENT_TIMEOUT_SECONDS="$TIMEOUT_SECONDS"
fi
if [[ -n "$MAX_TURNS" ]]; then
  export RESEARCHCHEMBENCH_MAX_TURNS="$MAX_TURNS"
fi
if [[ -n "$WORKSPACES_DIR" ]]; then
  export RESEARCHCHEMBENCH_WORKSPACES_DIR="$WORKSPACES_DIR"
fi
if [[ -n "$TASKS_DIR" ]]; then
  export RESEARCHCHEMBENCH_TASKS_DIR="$TASKS_DIR"
fi
if [[ -n "$OPENCODE_MODEL_VALUE" ]]; then
  export RESEARCHCHEMBENCH_OPENCODE_MODEL="$OPENCODE_MODEL_VALUE"
fi
if [[ -n "$OPENCODE_BASE_URL_VALUE" ]]; then
  export RESEARCHCHEMBENCH_OPENCODE_BASE_URL="$OPENCODE_BASE_URL_VALUE"
fi
if [[ -n "$JUDGE_MODEL_VALUE" ]]; then
  export JUDGE_MODEL_NAME="$JUDGE_MODEL_VALUE"
fi

if [[ "$MCP_TOOLS_VALUE" != "all" ]]; then
  echo "Error: --mcp-tools only accepts 'all'; task-specific tool filtering is disabled for this benchmark." >&2
  exit 2
fi
unset RESEARCHCHEM_MCP_ENABLED_TOOLS RESEARCHCHEM_MCP_DISABLED_TOOLS
if [[ "$TOOL_DISCOVERY_MODE_VALUE" != "progressive" && "$TOOL_DISCOVERY_MODE_VALUE" != "full" ]]; then
  echo "Error: --tool-discovery-mode must be 'progressive' or 'full'." >&2
  exit 2
fi
export RESEARCHCHEM_TOOL_DISCOVERY_MODE="$TOOL_DISCOVERY_MODE_VALUE"
if [[ -n "$MCP_PROFILES_VALUE" ]]; then
  export RESEARCHCHEMBENCH_MCP_PROFILES="$MCP_PROFILES_VALUE"
  python - <<'PY'
from chemistry_toolbox.mcp.profiles import selected_profile_names
selected_profile_names()
PY
fi

if [[ "$LIST_AGENTS" -eq 1 ]]; then
  python - <<'PY'
from evaluation.config import AGENT_PRESETS
for key, value in sorted(AGENT_PRESETS.items()):
    print(f"{key:10s} {value.get('label', key)}")
PY
  exit 0
fi

if [[ "$LIST_TASKS" -eq 1 ]]; then
  python - <<'PY'
from evaluation.utils import list_tasks_grouped
for category, task_ids in list_tasks_grouped().items():
    print(f"[{category}]")
    for task_id in task_ids:
        print(f"  {task_id}")
PY
  exit 0
fi

CLI_ARGS=()
if [[ "$DRY_RUN" -eq 1 ]]; then
  CLI_ARGS+=("--dry-run")
fi
if [[ "$NO_SCORE" -eq 1 ]]; then
  CLI_ARGS+=("--no-score")
fi

if [[ -n "$CONFIG" ]]; then
  echo "ResearchChemBench batch evaluation"
  echo "  Config:          $CONFIG"
  echo "  ChemGraph root:  $CHEMGRAPH_ROOT"
  echo "  MCP Python:      $CHEMGRAPH_PYTHON"
  echo "  MCP tools:       $MCP_TOOLS_VALUE"
  echo "  Tool discovery:  $TOOL_DISCOVERY_MODE_VALUE"
  echo "  Backend runtimes:${MCP_PROFILES_VALUE:-all catalog entries; one public server}"
  echo "  Workspaces root: ${RESEARCHCHEMBENCH_WORKSPACES_DIR:-$ROOT_DIR/workspaces}"
  echo "  Judge model:     ${JUDGE_MODEL_NAME:-<not configured>}"
  exec python -m evaluation.cli_eval "$CONFIG" "${CLI_ARGS[@]}"
fi

echo "ResearchChemBench single-task evaluation"
echo "  Agent:           $AGENT"
echo "  Task:            $TASK"
echo "  ChemGraph root:  $CHEMGRAPH_ROOT"
echo "  MCP Python:      $CHEMGRAPH_PYTHON"
echo "  MCP tools:       $MCP_TOOLS_VALUE"
echo "  Tool discovery:  $TOOL_DISCOVERY_MODE_VALUE"
echo "  Backend runtimes:${MCP_PROFILES_VALUE:-all catalog entries; one public server}"
echo "  Timeout seconds: ${RESEARCHCHEMBENCH_AGENT_TIMEOUT_SECONDS:-7200}"
echo "  Max turns:       ${RESEARCHCHEMBENCH_MAX_TURNS:-200}"
echo "  Workspaces root: ${RESEARCHCHEMBENCH_WORKSPACES_DIR:-$ROOT_DIR/workspaces}"
echo "  Judge model:     ${JUDGE_MODEL_NAME:-<not configured>}"

exec python -m evaluation.cli_eval \
  --agent "$AGENT" \
  --task "$TASK" \
  "${CLI_ARGS[@]}"
