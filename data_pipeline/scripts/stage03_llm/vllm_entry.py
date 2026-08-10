#!/usr/bin/env python3
"""Launch the vLLM FastAPI server with conservative Stage 03 defaults."""

from __future__ import annotations

import os
import runpy
import shlex
import sys


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default).strip()


def main() -> int:
    # Generic rlaunch GPU workers provide a CUDA runtime but not nvcc.  The
    # FlashInfer sampler tries to JIT CUDA sources during vLLM warm-up.
    os.environ.setdefault("VLLM_USE_FLASHINFER_SAMPLER", "0")
    os.environ.setdefault("VLLM_USE_DEEP_GEMM", "0")
    model_path = _env(
        "STAGE03_LLM_MODEL_DIR",
        "/mnt/shared-storage-user/liyuqiang/mdoels/Qwen3-30B-A3B-Instruct-2507",
    )
    argv = [
        "vllm.entrypoints.openai.api_server",
        "--model",
        model_path,
        "--served-model-name",
        _env("STAGE03_LLM_MODEL_NAME", "qwen3-30b-a3b-instruct-2507"),
        "--host",
        _env("STAGE03_LLM_VLLM_HOST", "127.0.0.1"),
        "--port",
        _env("STAGE03_LLM_VLLM_PORT", "18082"),
        "--dtype",
        "bfloat16",
        "--tensor-parallel-size",
        "1",
        "--gpu-memory-utilization",
        _env("STAGE03_LLM_GPU_MEMORY_UTILIZATION", "0.90"),
        "--max-model-len",
        _env("STAGE03_LLM_MAX_MODEL_LEN", "16384"),
        "--max-num-seqs",
        _env("STAGE03_LLM_MAX_NUM_SEQS", "64"),
        "--max-num-batched-tokens",
        _env("STAGE03_LLM_MAX_BATCHED_TOKENS", "32768"),
        "--moe-backend",
        _env("STAGE03_LLM_MOE_BACKEND", "triton"),
        "--no-enable-flashinfer-autotune",
        "--enable-prefix-caching",
        "--trust-remote-code",
    ]
    extra_args = os.environ.get("STAGE03_LLM_VLLM_EXTRA_ARGS", "").strip()
    if extra_args:
        argv.extend(shlex.split(extra_args))
    sys.argv = argv
    print("[stage03-vllm]", " ".join(shlex.quote(item) for item in argv), flush=True)
    runpy.run_module("vllm.entrypoints.openai.api_server", run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
