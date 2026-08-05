from __future__ import annotations

import contextlib
import threading
import time
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src.core.io import read_json, read_jsonl, write_jsonl
from src.orchestration import microbatch
from src.orchestration.microbatch import MicrobatchOptions
from src.sandbox.manager import service_instance_ports
from src.sandbox.runtime import SandboxPipelineRuntime


def _options(*, concurrency: int = 2, end_stage: int = 7) -> MicrobatchOptions:
    return MicrobatchOptions.from_config(
        {
            "microbatch": {
                "size": 1,
                "concurrency": concurrency,
                "stage_limits": {str(stage): concurrency for stage in range(2, end_stage + 1)},
                "softcite_instances": "auto",
            }
        },
        end_stage,
    )


def test_options_use_stage03_limit_for_automatic_softcite_pool():
    options = MicrobatchOptions.from_config(
        {
            "microbatch": {
                "size": 10,
                "concurrency": 5,
                "stage_limits": {"3": 3, "stage_06": 2},
                "softcite_instances": "auto",
            }
        },
        7,
    )

    assert options.size == 10
    assert options.concurrency == 5
    assert options.stage_limits[3] == 3
    assert options.stage_limits[6] == 2
    assert options.softcite_instances == 3


def test_scheduler_refills_a_fixed_number_of_microbatch_workers(tmp_path, monkeypatch):
    active = 0
    maximum = 0
    lock = threading.Lock()

    def fake_batch(*, batch_number, root, **_kwargs):
        nonlocal active, maximum
        with lock:
            active += 1
            maximum = max(maximum, active)
        time.sleep(0.02)
        with lock:
            active -= 1
        return {"batch": batch_number, "root": root}

    monkeypatch.setattr(microbatch, "_run_one_batch", fake_batch)
    batches = [[{"document_id": str(index)}] for index in range(6)]
    options = _options(concurrency=2)

    results = microbatch._run_batches(
        batches=batches,
        root=tmp_path,
        config={},
        base=tmp_path,
        toolbox={},
        options=options,
        end_stage=7,
        semaphores={stage: threading.BoundedSemaphore(2) for stage in range(2, 8)},
        clients={},
    )

    assert maximum == 2
    assert [item["batch"] for item in results] == [1, 2, 3, 4, 5, 6]


def test_one_microbatch_runs_stages_in_order_and_resumes(tmp_path, monkeypatch):
    calls = []

    def fake_execute(stage, previous, *, stage_root, **_kwargs):
        calls.append(stage)
        if stage == 2:
            write_jsonl(stage_root / "documents.jsonl", previous)
            return previous
        if stage == 3:
            write_jsonl(stage_root / "software_coverage_documents.jsonl", previous)
            return previous
        raise AssertionError(stage)

    monkeypatch.setattr(microbatch, "_execute_stage", fake_execute)
    documents = [{"document_id": "doc-1", "source_path": "/paper.pdf", "sha256": "abc"}]
    options = _options(concurrency=1, end_stage=3)
    kwargs = {
        "batch_number": 1,
        "documents": documents,
        "root": tmp_path / "batch_000001",
        "config": {},
        "base": tmp_path,
        "toolbox": {},
        "options": options,
        "end_stage": 3,
        "semaphores": {stage: threading.BoundedSemaphore(1) for stage in range(2, 4)},
        "clients": {},
    }

    microbatch._run_one_batch(**kwargs)
    assert calls == [2, 3]
    assert read_json(kwargs["root"] / "state.json")["completed_stages"] == [2, 3]

    calls.clear()
    resumed = microbatch._run_one_batch(**kwargs)
    assert calls == []
    assert resumed["stage02"] == documents
    assert resumed["stage03"] == documents


def test_one_microbatch_runs_stage02_through_stage07_in_order(tmp_path, monkeypatch):
    calls = []

    def fake_execute(stage, previous, **_kwargs):
        calls.append(stage)
        return previous

    monkeypatch.setattr(microbatch, "_execute_stage", fake_execute)
    documents = [{"document_id": "doc-1", "source_path": "/paper.pdf", "sha256": "abc"}]
    options = _options(concurrency=1, end_stage=7)
    root = tmp_path / "batch_000001"

    microbatch._run_one_batch(
        batch_number=1,
        documents=documents,
        root=root,
        config={},
        base=tmp_path,
        toolbox={},
        options=options,
        end_stage=7,
        semaphores={stage: threading.BoundedSemaphore(1) for stage in range(2, 8)},
        clients={},
    )

    assert calls == [2, 3, 4, 5, 6, 7]
    assert read_json(root / "state.json")["completed_stages"] == [2, 3, 4, 5, 6, 7]


def test_softcite_instances_have_non_conflicting_ports():
    assert service_instance_ports("softcite", 0) == (8060, 8061)
    assert service_instance_ports("softcite", 1) == (8160, 8161)
    assert service_instance_ports("softcite", 3) == (8164, 8165)
    with pytest.raises(ValueError, match="at most 16"):
        service_instance_ports("softcite", 16)


def test_sandbox_service_context_does_not_stop_at_stage_exit():
    runtime = object.__new__(SandboxPipelineRuntime)
    runtime._service_references = {}
    runtime._started_services = set()
    runtime._service_lock = threading.RLock()
    runtime.start_service = Mock(return_value={"healthy": True})
    runtime.stop_service = Mock()
    runtime._mirror_service_log = Mock()

    with runtime.service("softcite", {"_sandbox_instance": 2}):
        pass

    runtime.start_service.assert_called_once()
    runtime._mirror_service_log.assert_called_once()
    runtime.stop_service.assert_not_called()


def test_keep_lifecycle_leaves_services_running_between_pipeline_invocations():
    runtime = object.__new__(SandboxPipelineRuntime)
    runtime.options = SimpleNamespace(cleanup="keep")
    runtime._started_services = {("softcite", 0)}
    runtime._service_configs = {("softcite", 0): {"service_log": "/tmp/softcite.log"}}
    runtime.proxies = {}
    runtime.manager = SimpleNamespace(cleanup=Mock())
    runtime._mirror_service_log = Mock()
    runtime.stop_service = Mock()
    runtime._release_lock = Mock()

    runtime.__exit__(None, None, None)

    runtime._mirror_service_log.assert_called_once()
    runtime.stop_service.assert_not_called()
    runtime.manager.cleanup.assert_called_once()


def test_pipeline_clients_start_all_required_services_before_work(monkeypatch):
    entered = []
    exited = []

    @contextlib.contextmanager
    def service(name):
        entered.append(name)
        try:
            yield name
        finally:
            exited.append(name)

    monkeypatch.setattr(microbatch, "grobid_service", lambda _config: service("grobid"))
    monkeypatch.setattr(microbatch, "softcite_service", lambda _config: service("softcite"))
    monkeypatch.setattr(
        microbatch, "grobid_quantities_service", lambda _config: service("quantities")
    )
    options = _options(concurrency=2, end_stage=4)
    config = {
        "grobid_extract": {},
        "software_coverage": {},
        "grobid_quantities": {},
        "stage04": {"enabled": True},
    }

    with microbatch._pipeline_clients(config, options, 4):
        assert entered == ["grobid", "softcite", "quantities"]
        assert exited == []

    assert exited == ["quantities", "softcite", "grobid"]


def test_stage02_microbatches_merge_in_original_order(tmp_path, monkeypatch):
    @contextlib.contextmanager
    def fake_clients(_config, _options, _end_stage):
        yield {"grobid": object()}

    def fake_extract(documents, _client, **_kwargs):
        time.sleep(0.01 if documents[0]["document_id"] == "doc-1" else 0)
        return [
            {**item, "grobid_extract_status": "success", "grobid_request_attempted": True}
            for item in documents
        ]

    monkeypatch.setattr(microbatch, "_pipeline_clients", fake_clients)
    monkeypatch.setattr(microbatch, "extract_documents_with_grobid", fake_extract)
    documents = [
        {
            "document_id": f"doc-{index}",
            "paper_id": f"doc-{index}",
            "source_path": str(tmp_path / f"paper-{index}.pdf"),
            "sha256": str(index),
        }
        for index in range(1, 6)
    ]
    workspace = tmp_path / "outputs"
    config = {
        "stop_after": "grobid_extract",
        "source": {"exclude_supplementary": True},
        "microbatch": {"enabled": True, "size": 2, "concurrency": 2},
        "grobid_extract": {
            "tei_dir": str(workspace / "stage_02_grobid_extract" / "tei"),
            "text_dir": str(workspace / "stage_02_grobid_extract" / "text"),
            "fallback": {},
        },
    }

    summary = microbatch.run_microbatch_stages(
        config_path=tmp_path / "config.json",
        config=config,
        base=tmp_path,
        workspace=workspace,
        corpus_root=tmp_path,
        inventory=documents,
        canonical_inventory=documents,
        duplicate_inventory=[],
        supplementary_inventory=[],
        exclude_supplementary=True,
    )

    merged = read_jsonl(workspace / "stage_02_grobid_extract" / "documents.jsonl")
    assert [item["document_id"] for item in merged] == [f"doc-{index}" for index in range(1, 6)]
    assert summary["microbatch"]["batches"] == 3
    assert summary["stage_02_grobid_extract"]["documents"] == 5
    assert all(
        read_json(workspace / "microbatches" / f"batch_{index:06d}" / "state.json")[
            "completed_stages"
        ]
        == [2]
        for index in range(1, 4)
    )

    @contextlib.contextmanager
    def forbidden_clients(*_args, **_kwargs):
        raise AssertionError("a fully completed resume must not start services")
        yield

    monkeypatch.setattr(microbatch, "_pipeline_clients", forbidden_clients)
    resumed = microbatch.run_microbatch_stages(
        config_path=tmp_path / "config.json",
        config=config,
        base=tmp_path,
        workspace=workspace,
        corpus_root=tmp_path,
        inventory=documents,
        canonical_inventory=documents,
        duplicate_inventory=[],
        supplementary_inventory=[],
        exclude_supplementary=True,
    )
    assert resumed["stage_02_grobid_extract"]["documents"] == 5


def test_aggregation_keeps_stage05_through_stage07_outputs_compatible(tmp_path):
    batch_root = tmp_path / "microbatches" / "batch_000001"
    source = tmp_path / "paper.pdf"
    source.write_bytes(b"pdf")
    document = {
        "document_id": "doc-1",
        "paper_id": "paper-1",
        "source_path": str(source),
        "grobid_extract_status": "success",
        "software_coverage": {"decision": "direct_covered"},
        "resource_limits": {"decision": "no_explicit_resource", "passed": True},
    }
    for stage, child in ((5, "papers/paper-1"), (6, "paper-1"), (7, "task-1")):
        (batch_root / microbatch.STAGE_NAMES[stage] / child).mkdir(parents=True)
    write_jsonl(
        batch_root / microbatch.STAGE_NAMES[4] / "recalled_contexts.jsonl",
        [{"document_id": "doc-1", "contexts": []}],
    )
    write_jsonl(
        batch_root / microbatch.STAGE_NAMES[4] / "structured_resource_documents.jsonl",
        [{"document_id": "doc-1", "resource_records": []}],
    )
    results = [
        {
            "batch": 1,
            "root": batch_root,
            "stage02": [document],
            "stage03": [document],
            "stage04": [document],
            "stage05": {
                "assets": [{"paper_id": "paper-1", "role": "primary_pdf"}],
                "clues": [{"paper_id": "paper-1", "status": "resolved"}],
                "events": [{"paper_id": "paper-1", "event": "registered"}],
                "papers": [{"paper_id": "paper-1", "status": "success"}],
            },
            "stage06": {"records": [{"paper_id": "paper-1", "status": "candidate_ready"}]},
            "stage07": {
                "records": [{"paper_id": "paper-1", "task_id": "task-1", "status": "pass"}]
            },
        }
    ]
    workspace = tmp_path / "outputs"

    summaries = microbatch._aggregate_outputs(
        results=results,
        workspace=workspace,
        config={"stage04": {"enabled": True}, "stage05": {"enabled": True}},
        inventory=[document],
        duplicate_inventory=[],
        supplementary_inventory=[],
        exclude_supplementary=True,
        end_stage=7,
    )

    assert summaries["stage_05"]["papers"] == 1
    assert summaries["stage_06"]["statuses"] == {"candidate_ready": 1}
    assert summaries["stage_07"]["statuses"] == {"pass": 1}
    assert (workspace / microbatch.STAGE_NAMES[5] / "papers" / "paper-1").is_symlink()
    assert (workspace / microbatch.STAGE_NAMES[6] / "paper-1").is_symlink()
    assert (workspace / microbatch.STAGE_NAMES[7] / "task-1").is_symlink()
