#!/usr/bin/env bash
# Replace Intel's executable-stack format callback with equivalent standard Fortran formatting.
set -euo pipefail
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
sisso_dir="$project_dir/.software_cache/installations/sisso/3.5"
compiler_dir="$sisso_dir/toolchain/oneapi/compiler/2021.2.0/linux"
build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT
python3 - "$project_dir/.software_cache/sources/sisso/3.5/source/utilities/SISSO_predict.f90" "$build_dir/predict.f90" <<'PY'
import sys
from pathlib import Path
source = Path(sys.argv[1]).read_text()
assert source.count("'(<nd>e20.10)'") == 1
Path(sys.argv[2]).write_text(source.replace("'(<nd>e20.10)'", "'(*(e20.10))'"))
PY
LD_LIBRARY_PATH="$compiler_dir/compiler/lib/intel64_lin:${LD_LIBRARY_PATH:-}" \
  "$compiler_dir/bin/intel64/ifort" -O2 -static-intel "$build_dir/predict.f90" -o "$build_dir/SISSO_predict"
if [[ ! -f "$sisso_dir/bin/SISSO_predict.original" ]]; then
  cp -p "$sisso_dir/bin/SISSO_predict" "$sisso_dir/bin/SISSO_predict.original"
fi
install -m 755 "$build_dir/SISSO_predict" "$sisso_dir/bin/SISSO_predict"
