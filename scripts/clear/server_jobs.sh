#!/usr/bin/env bash
# Default: read-only CPU/process status. See README.md for explicit stop commands.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/server_jobs.py" "$@"
