#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THIRD_PARTY="$ROOT/third_party"
SOFTCITE="$THIRD_PARTY/software-mentions"
QUANTITIES="$THIRD_PARTY/grobid-quantities"
DELFT="$THIRD_PARTY/delft"
GROBID_HOME="$THIRD_PARTY/grobid-home"
PYTHON="${PIPELINE_PYTHON:-python}"
SOFTCITE_COMMIT="c7c83852a3cad8f2d9d07ce3de6fbe852e23c19a"
QUANTITIES_COMMIT="d0d55592f4d0ddbe6a549e06613349adaa2d1cd7"
DELFT_COMMIT="d8505592c38058b9b0abbde14d4ddedff3ad7d0f"

if [[ -n "${GROBID_JAVA_HOME:-}" ]]; then
  JAVA_HOME="$GROBID_JAVA_HOME"
elif [[ -n "${JAVA_HOME:-}" ]]; then
  JAVA_HOME="$JAVA_HOME"
elif command -v conda >/dev/null; then
  JAVA_HOME="$(conda info --base)"
else
  echo "OpenJDK 21 is required. Set GROBID_JAVA_HOME or JAVA_HOME." >&2
  exit 1
fi
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$JAVA_HOME/lib/server:${LD_LIBRARY_PATH:-}"
export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"

java_version="$(java -version 2>&1 | sed -n '1s/.*version "\([0-9][0-9]*\).*/\1/p')"
if [[ -z "$java_version" || "$java_version" -lt 21 ]]; then
  echo "OpenJDK 21 or newer is required; found: $(java -version 2>&1 | head -1)" >&2
  exit 1
fi

mkdir -p "$THIRD_PARTY"
clone_at_commit() {
  local url="$1" path="$2" commit="$3"
  if [[ ! -d "$path/.git" ]]; then
    git clone "$url" "$path"
  fi
  git -C "$path" fetch origin "$commit"
  git -C "$path" checkout --detach "$commit"
}

apply_patch_once() {
  local checkout="$1" patch_file="$2"
  if git -C "$checkout" apply --reverse --check "$patch_file" >/dev/null 2>&1; then
    return
  fi
  git -C "$checkout" apply --check "$patch_file"
  git -C "$checkout" apply "$patch_file"
}

clone_at_commit https://github.com/softcite/software-mentions.git "$SOFTCITE" "$SOFTCITE_COMMIT"
clone_at_commit https://github.com/lfoppiano/grobid-quantities.git "$QUANTITIES" "$QUANTITIES_COMMIT"
clone_at_commit https://github.com/kermitt2/delft.git "$DELFT" "$DELFT_COMMIT"
apply_patch_once "$SOFTCITE" "$ROOT/scripts/patches/software-mentions-c7c83852.patch"
apply_patch_once "$QUANTITIES" "$ROOT/scripts/patches/grobid-quantities-d0d5559.patch"

ln -sfn grobid/grobid-home "$GROBID_HOME"

"$PYTHON" -m pip install \
  "transformers==4.57.3" \
  "tensorflow==2.17.1" \
  "tf_keras==2.17.0" \
  "tfa-nightly==0.23.0.dev20240415222534" \
  "h5py==3.11.0" \
  "scikit-learn==1.6.1" \
  "unidecode==1.3.2" \
  "pydot==1.4.0" \
  "lmdb==2.1.1" \
  truecase blingfire2 "jep==4.3.1"
"$PYTHON" -m pip install --no-deps -e "$DELFT"

(cd "$SOFTCITE" && ./gradlew copyModels)
(cd "$QUANTITIES" && ./gradlew copyModels)

"$PYTHON" - "$GROBID_HOME/models" <<'PY'
import sys
from pathlib import Path

import h5py
from huggingface_hub import snapshot_download

root = Path(sys.argv[1])
models = [
    "context_bert",
    "context_creation_bert",
    "context_shared_bert",
    "context_used_bert",
    "software-BERT",
]
snapshot_download(
    repo_id="sciencialab/software-mentions-models",
    allow_patterns=[f"{name}/**" for name in models],
    local_dir=root,
)
for name in models:
    path = root / name / "model_weights.hdf5"
    try:
        with h5py.File(path, "r") as handle:
            if not handle.keys():
                raise RuntimeError("empty HDF5 root")
    except Exception as exc:
        raise SystemExit(f"Invalid Softcite model {path}: {exc}") from exc
PY

jep_library="$($PYTHON - <<'PY'
from pathlib import Path
import jep
print(Path(jep.__file__).with_name("libjep.so"))
PY
)"
mkdir -p "$GROBID_HOME/lib/lin-64/jep"
ln -sfn "$jep_library" "$GROBID_HOME/lib/lin-64/jep/libjep.so"

(cd "$SOFTCITE" && ./gradlew classes)
(cd "$QUANTITIES" && ./gradlew classes)

echo "Stage 03-05 services are ready."
echo "Softcite: $SOFTCITE_COMMIT"
echo "GROBID Quantities: $QUANTITIES_COMMIT"
echo "DeLFT: $DELFT_COMMIT"
