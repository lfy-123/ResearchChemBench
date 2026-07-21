#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
PYTHON_BIN="${RESEARCHCHEM_INSTALL_PYTHON:-python}"
WITH_CHEMISTRY=0
INSTALLER_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-chemistry-deps)
      WITH_CHEMISTRY=1
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Install the portable ResearchChem MCP tool package and configure Agent CLIs.

Usage:
  bash install.sh [--with-chemistry-deps] [installer options]

Examples:
  bash install.sh --agent all --chemgraph-root /path/to/ChemGraph --scope user
  bash install.sh --with-chemistry-deps --agent codex --chemgraph-root /path/to/ChemGraph
  bash install.sh --agent opencode --scope project --project-dir /path/to/project
  bash install.sh --agent all --chemgraph-root /path/to/ChemGraph --dry-run

Important installer options passed through:
  --agent all|codex|claude|opencode   Repeatable; default all installed Agents.
  --name NAME                         MCP server name; default researchchem-tools.
  --chemgraph-root PATH               ChemGraph checkout containing src/chemgraph.
  --workspace PATH                    Optional fixed workspace; default Agent process cwd.
  --python PATH                       Python used to start the installed MCP server.
  --scope local|project|user          Claude/OpenCode scope; default user.
  --project-dir PATH                  OpenCode project config directory.
  --uninstall                         Remove Agent MCP registrations.
  --dry-run                           Print config changes without applying them.

Set RESEARCHCHEM_INSTALL_PYTHON to choose the Python used for pip installation.
EOF
      exit 0
      ;;
    *)
      INSTALLER_ARGS+=("$1")
      shift
      ;;
  esac
done

PACKAGE_SPEC="$ROOT_DIR"
if [[ "$WITH_CHEMISTRY" -eq 1 ]]; then
  PACKAGE_SPEC="$ROOT_DIR[chemistry]"
fi

echo "Installing Python package: $PACKAGE_SPEC"
"$PYTHON_BIN" -m pip install "$PACKAGE_SPEC"

exec "$PYTHON_BIN" -m researchchem_mcp_tools.installer "${INSTALLER_ARGS[@]}"
