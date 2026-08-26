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


def _late_stage_batch_workflow_module():
    path = Path(__file__).resolve().parents[1] / "scripts/workflows/run_stage06_07_gpt_batch.py"
    spec = importlib.util.spec_from_file_location("run_stage06_07_gpt_batch", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_late_stage_batch_treats_scientific_rejection_as_terminal_success(tmp_path) -> None:
    workflow = _late_stage_batch_workflow_module()
    summary = tmp_path / "late_stage_run_summary.json"
    summary.write_text(
        '{"stage06":{"provisional_not_constructible":1,"decisions":{"provisional_not_constructible":1}},"stage07":{"status":"not_run"}}',
        encoding="utf-8",
    )
    assert workflow._late_stage_outcome(summary) == {
        "state": "COMPLETED",
        "outcome": "scientific_rejection",
    }


def test_late_stage_batch_still_flags_unexplained_stage07_not_run(tmp_path) -> None:
    workflow = _late_stage_batch_workflow_module()
    summary = tmp_path / "late_stage_run_summary.json"
    summary.write_text(
        '{"stage06":{"provisional_constructed":1,"decisions":{"provisional_constructed":1}},"stage07":{"status":"not_run"}}',
        encoding="utf-8",
    )
    assert workflow._late_stage_outcome(summary) == {
        "state": "FAILED",
        "outcome": "technical_blocked",
        "failure_class": "stage07_not_run",
    }


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
        publication_date_from="2026-01-01",
        publication_index_path=str(tmp_path / "publication-index.jsonl"),
        credentials=str(tmp_path / "credentials"),
        seed=20260813,
        sandbox_cpu=64,
        sandbox_memory="128Gi",
        sandbox_startup_timeout_seconds=14400,
        sandbox_cleanup="stop",
        mineru_sandbox_count=32,
        mineru_sandbox_cpu=16,
        mineru_sandbox_memory="32Gi",
        mineru_sandbox_startup_concurrency=32,
        api_base_url="http://127.0.0.1:13000/v1",
        api_key_env="RCB_NEW_API_KEY",
        microbatch_size=10,
        microbatch_concurrency=8,
        stage02_workers=8,
        stage03_workers=8,
        stage04_microbatch_concurrency=2,
        stage04_api_concurrency=8,
        stage05_workers=8,
        stage05_auditor_max_tokens=8192,
        stage05_auditor_model="Nex-N2-Pro-w8a8",
        stage05_auditor_chat_template_kwargs={"enable_thinking": False},
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
    assert config["stage00"]["publication_date_from"] == "2026-01-01"
    assert config["execution"]["mineru_sandbox_pool"]["count"] == 32
    assert config["stage04"]["mineru"]["api_concurrency"] == 8
    assert config["microbatch"]["stage_concurrency"]["stage04"] == 2
    assert config["models"]["stage02_screening"]["model"] == "DeepSeek-V4-Pro"
    assert config["models"]["stage03_screening"]["model"] == "Nex-N2-Pro"
    assert config["stage02"]["classification_max_tokens"] == 12288
    assert config["stage02"]["pass_verification_max_tokens"] == 6144
    assert config["stage03"]["max_tokens"] == 12288
    assert config["models"]["stage02_screening"]["context_window_tokens"] == 32768
    assert config["models"]["stage03_screening"]["context_window_tokens"] == 32768
    assert config["models"]["stage02_screening"]["chat_template_kwargs"] == {
        "thinking": False
    }
    assert config["models"]["stage03_screening"]["chat_template_kwargs"] == {
        "enable_thinking": False
    }
    assert config["models"]["stage05_router"]["model"] == "DeepSeek-V4-Flash"
    assert config["execution"]["sandbox"]["cleanup"] == "stop"
    assert config["models"]["suitability"]["model"] == "Nex-N2-Pro-w8a8"
    assert config["models"]["suitability"]["max_tokens"] == 8192
    assert config["stage05"]["auditor_max_tokens"] == 8192
    assert config["models"]["stage05_router"]["base_url_env"] == "RCB_NEW_API_BASE_URL"
    assert config["models"]["suitability"]["model_env"] == (
        "RCB_RUN_SELECTED_STAGE05_AUDITOR_MODEL"
    )
    assert config["models"]["stage05_router"]["chat_template_kwargs"] == {"thinking": False}
    assert config["models"]["suitability"]["chat_template_kwargs"] is None


def test_stage05_auditor_selector_falls_back_to_first_stable_strong_model() -> None:
    batch_workflow = _api_batch_workflow_module()
    calls = []

    def caller(**kwargs):
        calls.append(kwargs["model"])
        if kwargs["model"] in {"DeepSeek-V4-Pro", "GLM-5.2"}:
            raise RuntimeError("upstream unavailable")
        return {"decision": "pass", "checks": ["workflow", "software", "cost"]}, {}

    selected, audit = batch_workflow._select_stage05_auditor(
        "http://127.0.0.1:13000/v1",
        "secret",
        ("DeepSeek-V4-Pro", "GLM-5.2", "Nex-N2-Pro"),
        attempts=3,
        caller=caller,
    )

    assert selected == "Nex-N2-Pro"
    assert calls == [
        "DeepSeek-V4-Pro",
        "GLM-5.2",
        "Nex-N2-Pro",
        "Nex-N2-Pro",
        "Nex-N2-Pro",
    ]
    assert audit[-1]["selected"] is True


def test_stage05_auditor_selector_never_falls_back_to_flash() -> None:
    batch_workflow = _api_batch_workflow_module()

    def caller(**_kwargs):
        raise RuntimeError("upstream unavailable")

    import pytest

    with pytest.raises(RuntimeError, match="no strong Stage05B auditor"):
        batch_workflow._select_stage05_auditor(
            "http://127.0.0.1:13000/v1",
            "secret",
            ("DeepSeek-V4-Pro", "GLM-5.2", "Nex-N2-Pro"),
            attempts=3,
            caller=caller,
        )
