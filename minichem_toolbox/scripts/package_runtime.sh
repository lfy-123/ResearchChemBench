#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.mini_software_cache/runtimes/minichem"
OUTPUT="$ROOT/.mini_software_cache/runtime_packs/minichem.tar.gz"

if [[ ! -x "$RUNTIME/bin/python" ]]; then
  echo "MiniChem runtime is missing; run scripts/bootstrap.sh first" >&2
  exit 1
fi

if ! "$RUNTIME/bin/python" -c 'import conda_pack' 2>/dev/null; then
  "$RUNTIME/bin/python" -m pip install conda-pack
fi
mkdir -p "$(dirname "$OUTPUT")"
"$RUNTIME/bin/conda-pack" \
  -p "$RUNTIME" \
  -o "$OUTPUT" \
  --ignore-editable-packages \
  --ignore-missing-files \
  --force
echo "Created portable runtime pack: $OUTPUT"
