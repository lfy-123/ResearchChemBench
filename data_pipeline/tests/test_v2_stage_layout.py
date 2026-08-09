from __future__ import annotations

import json
from pathlib import Path

import src.v2.pipeline as pipeline
import src.v2.runtime as runtime
from src.v2.config import load_v2_config


def test_legacy_layout_is_mapped_without_changing_screening_rules(tmp_path: Path) -> None:
    profile = tmp_path / "profile.json"
    aliases = tmp_path / "aliases.json"
    profile.write_text('{"backends": {}}', encoding="utf-8")
    aliases.write_text("{}", encoding="utf-8")
    models = {
        role: {"enabled": True, "base_url": "http://fixture/v1", "model": role}
        for role in ("screening", "suitability", "builder", "judge")
    }
    config = {
        "pipeline_contract": "researchchembench-data-pipeline/v2",
        "workspace": "run",
        "stop_after": "stage05",
        "policy": "strict",
        "models": models,
        "stage01": {"enable_network": False},
        "stage02": {"grobid": {"workers": 2}},
        "stage03": {"model_role": "screening", "workers": 4},
        "stage04": {
            "model_role": "screening",
            "toolbox_capabilities": str(profile),
            "software_aliases": str(aliases),
            "mineru": {"enabled": True},
        },
        "stage05": {"model_role": "suitability"},
        "stage06": {"model_role": "builder"},
        "stage07": {"model_role": "judge"},
        "microbatch": {"size": 10, "concurrency": 2},
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    loaded = load_v2_config(path)

    assert loaded["stage_layout"] == "v2.1-split-normalization"
    assert loaded["stage01"]["package"]["enable_network"] is False
    assert loaded["stage01"]["normalization"]["grobid"]["workers"] == 2
    assert loaded["stage02"]["workers"] == 4
    assert loaded["stage03"]["toolbox_capabilities"] == str(profile)
    assert loaded["stage04"]["mineru"]["enabled"] is True
    assert loaded["models"]["screening"]["use_proxy"] is False
    assert loaded["models"]["suitability"]["use_proxy"] is True
    assert loaded["models"]["builder"]["use_proxy"] is True
    assert loaded["models"]["judge"]["use_proxy"] is True


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
            "extra_args": ["--formula", "true"],
        },
    )

    assert "start-mineru" in calls[0]
    assert updated["execution"] == "managed_gpu"
    assert updated["api_url"] == "http://127.0.0.1:18084"
    assert updated["extra_args"][-2:] == ["--api-url", "http://127.0.0.1:18084"]


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

    result = pipeline._run_loaded_pipeline_v2(config)

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
