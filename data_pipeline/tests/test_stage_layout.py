from __future__ import annotations

import json
import urllib.error
from pathlib import Path

import pytest

import src.pipeline as pipeline
import src.runtime as runtime
from src.model_client import RoleModelClient


def test_screening_start_command_reuses_external_worker(tmp_path: Path) -> None:
    manager = tmp_path / "manager.sh"
    state = tmp_path / "worker.json"
    target = "ws-existing.example@h.pjlab.org.cn"

    command = runtime._start_command(
        {"existing_worker": target, "skip_bootstrap": True, "skip_download": True},
        manager,
        state,
    )

    assert command[:3] == ["bash", str(manager), "start"]
    assert command[command.index("--existing-worker") + 1] == target
    assert "--skip-bootstrap" in command
    assert "--skip-download" in command


def test_managed_screening_worker_refuses_second_creation(tmp_path: Path) -> None:
    manager = tmp_path / "manager.sh"
    manager.write_text("#!/usr/bin/env bash\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="worker creation is disabled"):
        runtime.ensure_managed_screening_worker(
            {
                "managed_rlaunch": True,
                "manager_script": str(manager),
                "state_file": str(tmp_path / "missing-worker.json"),
                "allow_worker_creation": False,
            }
        )


def test_shared_worker_switch_adds_persistent_mineru_api(monkeypatch, tmp_path: Path) -> None:
    state = tmp_path / "worker.json"
    state.write_text(json.dumps({"base_url": "http://127.0.0.1:18084"}), encoding="utf-8")
    calls = []
    monkeypatch.setattr(runtime.subprocess, "run", lambda command, **kwargs: calls.append(command))
    updated = runtime.start_managed_mineru_service(
        {
            "managed_rlaunch": True,
            "manager_script": str(tmp_path / "manager.sh"),
            "state_file": str(state),
        },
        {
            "gpu_env_dir": "/shared/mineru-gpu",
            "environment": {"MINERU_TOOLS_CONFIG_JSON": "/shared/mineru.json"},
            "api_concurrency": 3,
            "request_batch_size": 2,
            "extra_args": ["--formula", "true"],
        },
    )

    assert "start-mineru" in calls[0]
    assert updated["execution"] == "managed_gpu"
    assert updated["api_url"] == "http://127.0.0.1:18084"
    assert updated["extra_args"][-2:] == ["--api-url", "http://127.0.0.1:18084"]


def test_managed_screening_guard_serializes_recovery(monkeypatch, tmp_path: Path) -> None:
    guard = runtime.ManagedScreeningServiceGuard(
        {
            "manager_script": str(tmp_path / "manager.sh"),
            "state_file": str(tmp_path / "state.json"),
            "base_url": "http://127.0.0.1:18083/v1",
        }
    )
    health = iter([False, True])
    monkeypatch.setattr(guard, "_healthy", lambda: next(health))
    calls = []

    class Result:
        returncode = 0
        stdout = "recovered"
        stderr = ""

    monkeypatch.setattr(
        runtime.subprocess,
        "run",
        lambda command, **kwargs: calls.append(command) or Result(),
    )

    guard.recover()

    assert calls[0][2] == "recover-screening"


def test_role_model_client_recovers_connection_and_retries(monkeypatch, tmp_path: Path) -> None:
    class Guard:
        def __init__(self):
            self.checks = 0
            self.recoveries = 0

        def ensure_healthy(self):
            self.checks += 1

        def recover(self):
            self.recoveries += 1

    guard = Guard()
    calls = []

    def caller(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise urllib.error.URLError(ConnectionRefusedError(111, "connection refused"))
        return {"decision": "pass"}, {"model_returned": "fixture"}

    monkeypatch.setenv("FIXTURE_KEY", "secret")
    client = RoleModelClient(
        role="screening",
        config={
            "model": "fixture",
            "base_url": "http://127.0.0.1:18083/v1",
            "api_key_env": "FIXTURE_KEY",
            "cache": False,
            "_managed_service_guard": guard,
        },
        cache_root=tmp_path,
        caller=caller,
    )

    response, _audit = client.call_json(
        namespace="test",
        record_id="paper-1",
        prompt_version="v1",
        system_prompt="system",
        user_content="user",
    )

    assert response == {"decision": "pass"}
    assert guard.checks == 1
    assert guard.recoveries == 1
    assert len(calls) == 2


def test_screening_connection_error_aborts_phase() -> None:
    with pytest.raises(runtime.ManagedScreeningServiceError, match="aborting"):
        pipeline._raise_on_screening_infrastructure_error(
            {
                "records": [
                    {
                        "processing_status": "failed",
                        "error": {
                            "error_type": "URLError",
                            "message": "<urlopen error [Errno 111] Connection refused>",
                        },
                    }
                ]
            },
            "stage02",
        )


def test_two_phase_scheduler_finishes_all_stage03_work_before_stage04(
    monkeypatch, tmp_path: Path
) -> None:
    events: list[str] = []
    papers = [{"paper_id": f"paper-{index}", "decision": "pass"} for index in range(4)]
    documents = [
        {
            "paper_id": row["paper_id"],
            "document_id": f"doc-{index}",
            "source_path": str(tmp_path / f"doc-{index}.pdf"),
            "sha256": str(index),
        }
        for index, row in enumerate(papers)
    ]
    for document in documents:
        Path(document["source_path"]).write_bytes(b"%PDF fixture")

    monkeypatch.setattr(pipeline, "run_stage00", lambda *_args: {"corpus_root": str(tmp_path)})
    monkeypatch.setattr(
        pipeline,
        "_load_or_run_package",
        lambda *_args: {"papers": papers, "documents": documents, "summary": {}},
    )
    monkeypatch.setattr(pipeline, "_grobid_service", lambda *_args: object())

    def normalize(**kwargs):
        rows = [
            {**row, "decision": "pass", "document_ids": [f"doc-{row['paper_id'].split('-')[-1]}"]}
            for row in kwargs["papers"]
        ]
        docs = [{**row, "decision": "pass"} for row in kwargs["documents"]]
        return {"papers": rows, "documents": docs, "attempts": [], "summary": {}}

    def content(**kwargs):
        events.append(f"stage02:{kwargs['papers'][0]['paper_id']}")
        return {
            "records": [{"paper_id": row["paper_id"], "passed": True} for row in kwargs["papers"]],
            "summary": {},
        }

    def gate(**kwargs):
        events.append(f"stage03:{kwargs['stage02_records'][0]['paper_id']}")
        return {"records": kwargs["stage02_records"], "summary": {}}

    def deep(**kwargs):
        events.append(f"stage04:{kwargs['stage03_records'][0]['paper_id']}")
        return {
            "records": kwargs["stage03_records"],
            "documents": kwargs["documents"],
            "deep_parse_attempts": [],
            "summary": {},
        }

    monkeypatch.setattr(pipeline, "run_document_normalization", normalize)
    monkeypatch.setattr(pipeline, "run_stage02", content)
    monkeypatch.setattr(pipeline, "run_stage03", gate)
    monkeypatch.setattr(pipeline, "run_stage04", deep)
    config = {
        "workspace": str(tmp_path / "run"),
        "run_id": "fixture",
        "stop_after": "stage04",
        "stage00": {},
        "stage01": {"package": {}, "normalization": {}},
        "stage02": {},
        "stage03": {},
        "stage04": {"mineru": {"enabled": True, "managed_gpu": False}},
        "stage05": {},
        "stage06": {},
        "stage07": {},
        "models": {
            role: {"enabled": True, "base_url": "http://fixture/v1", "model": role}
            for role in ("screening", "suitability", "builder", "judge")
        },
        "microbatch": {"enabled": True, "size": 1, "concurrency": 2, "resume": True},
    }

    result = pipeline._run_loaded_pipeline(config)

    assert result["status"] == "completed"
    last_gate = max(index for index, event in enumerate(events) if event.startswith("stage03:"))
    first_deep = min(index for index, event in enumerate(events) if event.startswith("stage04:"))
    assert last_gate < first_deep


def test_stage01_aggregate_keeps_package_holds_visible(tmp_path: Path) -> None:
    package_papers = [
        {"paper_id": "paper-pass", "decision": "pass", "package_status": "complete_with_si"},
        {
            "paper_id": "paper-hold",
            "decision": "hold",
            "package_status": "incomplete_si_unavailable",
        },
    ]
    normalized_paper = {
        "paper_id": "paper-pass",
        "decision": "pass",
        "document_ids": ["doc-pass"],
    }
    normalized_document = {
        "paper_id": "paper-pass",
        "document_id": "doc-pass",
        "decision": "pass",
        "selected_parser": "grobid",
    }

    result = pipeline._aggregate_phase1(
        [
            {
                "stage01": {
                    "papers": [normalized_paper],
                    "documents": [normalized_document],
                    "attempts": [],
                    "summary": {},
                }
            }
        ],
        {"papers": package_papers, "documents": [normalized_document]},
        tmp_path,
        "fixture",
        1,
    )

    summary = result["stage01"]["summary"]
    assert summary["papers"] == 2
    assert summary["package_passed_papers"] == 1
    assert summary["package_held_papers"] == 1
    assert summary["normalization_attempted_papers"] == 1
