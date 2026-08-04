#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
PYTHON_BIN="${MINICHEM_INSTALL_PYTHON:-$ROOT_DIR/.mini_software_cache/runtimes/minichem/bin/python}"
INSTALLER_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      cat <<'EOF'
Install the portable MiniChem MCP package and configure Agent CLIs.

Usage:
  bash mcp/install.sh [installer options]

Examples:
  bash mcp/install.sh --agent all --scope user
  bash mcp/install.sh --agent opencode --scope project --project-dir /path/to/project
  bash mcp/install.sh --agent all --dry-run

Important installer options passed through:
  --agent all|codex|claude|opencode   Repeatable; default all installed Agents.
  --name NAME                         MCP server name; default minichem-toolbox.
  --workspace PATH                    Optional fixed workspace; default Agent process cwd.
  --python PATH                       Python used to start the installed MCP server.
  --scope local|project|user          Claude/OpenCode scope; default user.
  --project-dir PATH                  OpenCode project config directory.
  --uninstall                         Remove Agent MCP registrations.
  --dry-run                           Print config changes without applying them.

Run `bash scripts/bootstrap.sh` first. Set MINICHEM_INSTALL_PYTHON to override the runtime Python.
EOF
      exit 0
      ;;
    *)
      INSTALLER_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "MiniChem runtime is missing; run bash scripts/bootstrap.sh first" >&2
  exit 1
fi

echo "Installing Python package: $ROOT_DIR"
"$PYTHON_BIN" -m pip install -e "$ROOT_DIR"

exec "$PYTHON_BIN" -m minichem_mcp_tools.installer "${INSTALLER_ARGS[@]}"
