#!/usr/bin/env bash
# Shared-storage setup: install host OS tools only; never modify shared envs.
set +x
set -euo pipefail
umask 077
ARCHE_SETUP_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec /usr/bin/python3 "$ARCHE_SETUP_ROOT/custom_agents/Arche-Harness/benchmark_adapter/deploy/setup_shared_host.py" "$@"
