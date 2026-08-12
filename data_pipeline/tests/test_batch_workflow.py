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


def _api_batch_workflow_module():
    path = Path(__file__).resolve().parents[1] / "scripts/workflows/run_stage00_05_api_batches.py"
    spec = importlib.util.spec_from_file_location("run_stage00_05_api_batches", path)
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


def test_api_batch_config_uses_no_managed_worker_and_stops_after_stage05(tmp_path) -> None:
    batch_workflow = _api_batch_workflow_module()
    template = {
        "pipeline_contract": "researchchembench-data-pipeline/v2",
        "execution": {"backend": "local", "sandbox": {}},
        "stage01": {"package": {}, "normalization": {"grobid": {}}},
        "stage02": {},
        "stage03": {},
        "stage04": {"mineru": {}},
        "stage05": {},
        "models": {"screening": {}},
    }
    args = SimpleNamespace(
        dataset="en-paper-hzzj",
        credentials=str(tmp_path / "credentials"),
        seed=20260813,
        sandbox_cpu=64,
        sandbox_memory="128Gi",
        sandbox_startup_timeout_seconds=14400,
        api_base_url="http://127.0.0.1:13000/v1",
        api_key_env="RCB_NEW_API_KEY",
        microbatch_size=10,
        microbatch_concurrency=8,
        stage02_workers=8,
        stage03_workers=8,
        stage04_microbatch_concurrency=2,
        stage04_api_concurrency=8,
        stage05_workers=8,
    )
    config = batch_workflow._batch_config(
        template,
        args=args,
        run_root=tmp_path / "run",
        workspace=tmp_path / "run/batches/batch-0001",
        batch_index=0,
        count=1000,
        exclusions=[],
    )

    assert config["stop_after"] == "stage05"
    assert config["models"]["screening"]["managed_rlaunch"] is False
    assert config["models"]["screening"]["allow_worker_creation"] is False
    assert config["stage04"]["mineru"]["managed_gpu"] is False
    assert config["stage04"]["mineru"]["api_concurrency"] == 4
    assert config["microbatch"]["stage_concurrency"]["stage04"] == 2
    assert config["models"]["stage02_screening"]["model"] == "Qwen3.6-27B"
    assert config["models"]["stage03_screening"]["model"] == "DeepSeek-V4-Flash"
    assert config["models"]["stage05_router"]["model"] == "DeepSeek-V4-Flash-DSpark"
    assert config["models"]["suitability"]["model"] == "DeepSeek-V4-Flash"
    assert config["models"]["stage05_router"]["base_url_env"] == "RCB_NEW_API_BASE_URL"
    assert config["models"]["suitability"]["model_env"] == "RCB_NEW_STAGE05_AUDITOR_MODEL"
    assert config["models"]["stage05_router"]["chat_template_kwargs"] == {"thinking": False}
    assert config["models"]["suitability"]["chat_template_kwargs"] == {"thinking": False}
