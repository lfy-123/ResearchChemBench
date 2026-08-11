from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

from src.sandbox.manager import DEFAULT_IMAGE, SandboxRunOptions


def _batch_workflow_module():
    path = Path(__file__).resolve().parents[1] / "scripts/workflows/run_stage00_04_batches.py"
    spec = importlib.util.spec_from_file_location("run_stage00_04_batches", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_batch_sandbox_prewarm_uses_default_image_and_configured_timeout(
    tmp_path, monkeypatch
) -> None:
    batch_workflow = _batch_workflow_module()
    monkeypatch.setattr(batch_workflow, "SandboxManager", lambda options: options)
    args = SimpleNamespace(
        sandbox_cpu=64,
        sandbox_memory="128Gi",
        sandbox_startup_timeout_seconds=14400,
    )

    options = batch_workflow._sandbox_manager(
        tmp_path,
        {"execution": {"sandbox": {}}},
        args,
        cleanup="keep",
    )

    assert isinstance(options, SandboxRunOptions)
    assert options.image == DEFAULT_IMAGE
    assert options.startup_timeout_seconds == 14400
    assert options.cleanup == "keep"
