#!/usr/bin/env bash
# Read-only; only Python 3 standard library is required.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/check_eval_status.py" "$@"
