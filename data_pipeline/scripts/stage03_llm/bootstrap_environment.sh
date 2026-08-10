#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
ENV_DIR="${RCB_PIPELINE_ENV_DIR:-$PIPELINE_ROOT/.envs/researchchem-data-pipeline}"
PYTHON_BIN="${STAGE03_LLM_BOOTSTRAP_PYTHON:-python3}"
PIP_INDEX_URL="${STAGE03_LLM_PIP_INDEX_URL:-http://mirrors.h.pjlab.org.cn/pypi/simple/}"
PIP_TRUSTED_HOST="${STAGE03_LLM_PIP_TRUSTED_HOST:-mirrors.h.pjlab.org.cn}"
TORCH_INDEX_URL="${RCB_GPU_TORCH_INDEX_URL:-https://download.pytorch.org/whl/cu128}"
VLLM_SOURCE="${STAGE03_LLM_VLLM_SOURCE:-/mnt/shared-storage-user/liyuqiang/vllm}"
MINERU_SOURCE="${STAGE04_MINERU_SOURCE:-$PIPELINE_ROOT/third_party/MinerU}"
TMP_ROOT="${RCB_RUNTIME_TMP_DIR:-/tmp/researchchem-runtime-${USER:-user}}"

if [[ ! -x "$ENV_DIR/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$ENV_DIR"
fi
mkdir -p "$TMP_ROOT"
export TMPDIR="$TMP_ROOT"

UV_BIN="${RCB_UV_BIN:-$(command -v uv || true)}"
if [[ -z "$UV_BIN" ]]; then
  PIP_CONFIG_FILE=/dev/null PIP_EXTRA_INDEX_URL="" "$ENV_DIR/bin/python" -m pip install \
    --index-url "$PIP_INDEX_URL" --trusted-host "$PIP_TRUSTED_HOST" \
    --timeout 300 --retries 10 uv
  UV_BIN="$ENV_DIR/bin/uv"
fi
install_packages() {
  local index_url=$1
  shift
  if [[ -n "$UV_BIN" ]]; then
    # uv resolves and downloads independent wheels concurrently; this is much
    # faster on the shared proxy than pip's serial downloader.
    UV_HTTP_TIMEOUT=300 UV_CONCURRENT_DOWNLOADS="${RCB_UV_CONCURRENT_DOWNLOADS:-16}" \
      UV_LINK_MODE=copy \
      "$UV_BIN" pip install --python "$ENV_DIR/bin/python" \
      --index-url "$index_url" \
      --allow-insecure-host "$PIP_TRUSTED_HOST" "$@"
  else
    PIP_CONFIG_FILE=/dev/null PIP_EXTRA_INDEX_URL="" "$ENV_DIR/bin/python" -m pip install \
      --index-url "$index_url" --trusted-host "$PIP_TRUSTED_HOST" \
      --timeout 300 --retries 10 "$@"
  fi
}

if ! "$ENV_DIR/bin/python" -m pip --version >/dev/null 2>&1; then
  "$ENV_DIR/bin/python" -m ensurepip --upgrade
fi
install_packages "$TORCH_INDEX_URL" \
  'torch==2.11.0' 'torchvision==0.26.0' 'torchaudio==2.11.0'
install_packages "$PIP_INDEX_URL" -r "$SCRIPT_DIR/requirements.txt"
if [[ -f "$VLLM_SOURCE/pyproject.toml" ]]; then
  install_packages "$PIP_INDEX_URL" setuptools-rust setuptools-scm semantic-version
  # The shared source tree already contains the validated precompiled CUDA
  # extensions. Install only editable metadata here and reuse those binaries.
  if [[ "${RCB_FORCE_RUNTIME_REINSTALL:-0}" == 1 ]] || \
    ! "$ENV_DIR/bin/python" - "$VLLM_SOURCE" <<'PY'
from importlib import metadata
import json
from pathlib import Path
import sys

try:
    direct_url = json.loads(metadata.distribution("vllm").read_text("direct_url.json"))
    installed_source = Path(direct_url["url"].removeprefix("file://")).resolve()
except (metadata.PackageNotFoundError, KeyError, TypeError, ValueError):
    raise SystemExit(1)
raise SystemExit(0 if installed_source == Path(sys.argv[1]).resolve() else 1)
PY
  then
    VLLM_TARGET_DEVICE=empty install_packages "$PIP_INDEX_URL" \
      --no-deps --no-build-isolation -e "$VLLM_SOURCE"
  fi
  VLLM_RUNTIME_REQUIREMENTS="$TMP_ROOT/vllm-runtime-requirements.txt"
  "$ENV_DIR/bin/python" - "$VLLM_RUNTIME_REQUIREMENTS" <<'PY'
from importlib import metadata
from pathlib import Path
import sys

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

protected = {
    "numpy",
    "opencv-python-headless",
    "protobuf",
    "torch",
    "torchaudio",
    "torchvision",
    "transformers",
}
missing = []
for raw in metadata.requires("vllm") or []:
    requirement = Requirement(raw)
    if requirement.marker and not requirement.marker.evaluate():
        continue
    name = canonicalize_name(requirement.name)
    if name in protected:
        continue
    try:
        installed = Version(metadata.version(requirement.name))
    except metadata.PackageNotFoundError:
        missing.append(raw)
        continue
    if requirement.specifier and installed not in requirement.specifier:
        missing.append(raw)
content = "\n".join(missing)
Path(sys.argv[1]).write_text(content + ("\n" if content else ""), encoding="utf-8")
PY
  if [[ -s "$VLLM_RUNTIME_REQUIREMENTS" ]]; then
    install_packages "$TORCH_INDEX_URL" \
      --extra-index-url "$PIP_INDEX_URL" --index-strategy unsafe-best-match \
      --constraint "$SCRIPT_DIR/unified_runtime_constraints.txt" \
      -r "$VLLM_RUNTIME_REQUIREMENTS"
  fi
  VLLM_CUDA_REQUIREMENTS="$TMP_ROOT/vllm-cuda-requirements.txt"
  "$ENV_DIR/bin/python" - "$VLLM_SOURCE/requirements/cuda.txt" \
    "$VLLM_CUDA_REQUIREMENTS" <<'PY'
from importlib import metadata
from pathlib import Path
import sys

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

protected = {"torch", "torchaudio", "torchvision"}
requirements = []
for raw in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    line = raw.split("#", 1)[0].strip()
    if not line or line.startswith("-r "):
        continue
    requirement = Requirement(line)
    if canonicalize_name(requirement.name) in protected:
        continue
    try:
        installed = Version(metadata.version(requirement.name))
    except metadata.PackageNotFoundError:
        requirements.append(line)
        continue
    if requirement.specifier and installed not in requirement.specifier:
        requirements.append(line)
content = "\n".join(requirements)
Path(sys.argv[2]).write_text(content + ("\n" if content else ""), encoding="utf-8")
PY
  if [[ -s "$VLLM_CUDA_REQUIREMENTS" ]]; then
    install_packages "$TORCH_INDEX_URL" \
      --extra-index-url "$PIP_INDEX_URL" --index-strategy unsafe-best-match \
      --constraint "$SCRIPT_DIR/unified_runtime_constraints.txt" \
      -r "$VLLM_CUDA_REQUIREMENTS"
  fi
else
  install_packages "$PIP_INDEX_URL" 'vllm>=0.8.5,<0.11'
fi
if [[ "${RCB_FORCE_RUNTIME_REINSTALL:-0}" == 1 ]] || \
  ! "$ENV_DIR/bin/python" - "$MINERU_SOURCE" <<'PY'
from importlib import metadata
import json
from pathlib import Path
import sys

try:
    direct_url = json.loads(metadata.distribution("mineru").read_text("direct_url.json"))
    installed_source = Path(direct_url["url"].removeprefix("file://")).resolve()
except (metadata.PackageNotFoundError, KeyError, TypeError, ValueError):
    raise SystemExit(1)
raise SystemExit(0 if installed_source == Path(sys.argv[1]).resolve() else 1)
PY
then
  install_packages "$PIP_INDEX_URL" \
    --constraint "$SCRIPT_DIR/unified_runtime_constraints.txt" \
    -e "$MINERU_SOURCE[pipeline]"
fi
if ! "$ENV_DIR/bin/python" - <<'PY'
try:
    import onnxruntime
    providers = onnxruntime.get_available_providers()
except (AttributeError, ImportError):
    providers = []

raise SystemExit(
    0 if "CUDAExecutionProvider" in providers else 1
)
PY
then
  "$ENV_DIR/bin/python" -m pip uninstall -y onnxruntime || true
  if [[ -n "$UV_BIN" ]]; then
    install_packages "$PIP_INDEX_URL" \
      --constraint "$SCRIPT_DIR/unified_runtime_constraints.txt" \
      --reinstall-package onnxruntime-gpu onnxruntime-gpu
  else
    install_packages "$PIP_INDEX_URL" \
      --constraint "$SCRIPT_DIR/unified_runtime_constraints.txt" \
      --force-reinstall onnxruntime-gpu
  fi
fi
"$ENV_DIR/bin/python" - <<'PY'
import fastapi
import httpx
import mineru
import onnxruntime
import torch
import uvloop
import vllm

print("torch", torch.__version__)
print("cuda_available", torch.cuda.is_available())
print("gpu_count", torch.cuda.device_count())
print("vllm", vllm.__version__)
print("mineru", mineru.__file__)
print("onnxruntime_providers", onnxruntime.get_available_providers())
print("fastapi", fastapi.__version__)
print("httpx", httpx.__version__)
print("uvloop", uvloop.__version__)
if torch.version.cuda is None:
    raise SystemExit("CUDA-enabled PyTorch was not installed")
if "CUDAExecutionProvider" not in onnxruntime.get_available_providers():
    raise SystemExit("onnxruntime CUDAExecutionProvider is unavailable")
PY
