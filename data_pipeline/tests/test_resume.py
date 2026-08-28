from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config import load_config
from src.core.io import write_json
from src.core.resume import (
    ResumeConfigurationMismatch,
    ResumeStateStore,
    scientific_stage_fingerprints,
)
from src.core.resume_importer import import_legacy_run
from src.core.resume_workflow import (
    BatchSpec,
    _effective_batch_start_stage,
    _stage_range_requires_sandbox,
    command_digest,
    expanded_invalidation,
    prepare_resume,
)


def _record(paper_id: str, *, decision: str, passed: bool, failed: bool = False):
    return {
        "paper_id": paper_id,
        "processing_status": "failed" if failed else "completed",
        "decision": decision,
        "passed": passed,
    }


def test_uninitialized_batch_automatically_resumes_from_stage00(tmp_path: Path):
    workspace = tmp_path / "batches" / "batch-0012"
    spec = BatchSpec(
        batch_id="batch-0012",
        index=12,
        target_slot_start=11001,
        count=1000,
        config_path=tmp_path / "configs" / "batch-0012.json",
        workspace=workspace,
        is_new=False,
    )

    assert (
        _effective_batch_start_stage(spec, requested_start_stage="stage02")
        == "stage00"
    )

    write_json(
        workspace / "stage_00_remote_corpus" / "stage_summary.json",
        {"stage": "stage00"},
    )
    assert (
        _effective_batch_start_stage(spec, requested_start_stage="stage02")
        == "stage02"
    )


def test_resume_reuses_scientific_reject_and_retries_objective_failure(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage02",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row=_record("paper-a", decision="computational_content_not_found", passed=False),
        imported=False,
    )
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage02",
        paper_id="paper-b",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-b",
        row=_record("paper-b", decision="processing_failed", passed=False, failed=True),
        imported=False,
    )

    reject = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage02",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
    )
    failed = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage02",
        paper_id="paper-b",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-b",
    )

    assert reject.action == "reuse"
    assert reject.status == "terminal_reject"
    assert failed.action == "run"
    assert failed.status == "retryable_failed"


def test_pending_stage_record_stays_pending_instead_of_becoming_reject(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage04",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row=_record("paper-a", decision="processing_pending", passed=False)
        | {"processing_status": "pending"},
        imported=False,
    )

    item = store.current_work_item(
        outer_batch_id="batch-0001", stage="stage04", paper_id="paper-a"
    )
    assert item["status"] == "pending"


def test_stage04_timeout_is_terminal_and_not_resumed(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    row = _record("paper-a", decision="deep_parse_failed", passed=False, failed=True) | {
        "failure_disposition": "terminal",
        "failure_class": "mineru_timeout",
        "error": {"error_type": "MinerUTimeout", "message": "deadline exceeded"},
    }
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage04",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row=row,
        imported=False,
    )

    planned = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage04",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
    )

    assert planned.action == "reuse"
    assert planned.status == "terminal_reject"


def test_resume_invalidates_missing_artifact_and_requires_explicit_config_change(
    tmp_path: Path,
):
    store = ResumeStateStore.for_run_root(tmp_path)
    artifact = tmp_path / "normalized.md"
    artifact.write_text("content", encoding="utf-8")
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage01",
        paper_id="paper-a",
        document_id="doc-a",
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row={**_record("paper-a", decision="pass", passed=True), "document_id": "doc-a"},
        artifacts=[artifact],
        imported=False,
    )
    artifact.unlink()

    plan = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage01",
        paper_id="paper-a",
        document_id="doc-a",
        config_fingerprint="config-a",
        input_fingerprint="input-a",
    )
    assert plan.action == "run"
    assert plan.status == "retryable_failed"

    with pytest.raises(ResumeConfigurationMismatch):
        store.plan_work(
            outer_batch_id="batch-0001",
            stage="stage01",
            paper_id="paper-a",
            document_id="doc-a",
            config_fingerprint="config-b",
            input_fingerprint="input-a",
        )


def test_selection_ledger_keeps_pruned_paper_identity(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    first = store.reserve_selection(
        dataset="dataset",
        source_main_uri="s3://bucket/a.pdf",
        normalized_doi="10.1/a",
        source_record_key="a.pdf",
        paper_id="paper-a",
        target_slot_ordinal=1,
        outer_batch_id="batch-0001",
    )
    store.update_selection_copy(
        first["selection_id"],
        copy_state="materialized",
        local_assets_state="pruned_terminal",
    )
    same = store.reserve_selection(
        dataset="dataset",
        source_main_uri="s3://bucket/a.pdf",
        normalized_doi="10.1/a",
        source_record_key="a.pdf",
        paper_id="paper-a",
        target_slot_ordinal=2,
        outer_batch_id="batch-0002",
    )

    assert same["selection_id"] == first["selection_id"]
    assert store.selected_main_uris("dataset") == {"s3://bucket/a.pdf"}
    assert store.max_target_slot() == 1


def test_terminal_pruning_does_not_invalidate_reusable_upstream_artifact(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    selection = store.reserve_selection(
        dataset="dataset",
        source_main_uri="s3://bucket/a.pdf",
        normalized_doi=None,
        source_record_key="a.pdf",
        paper_id="paper-a",
        target_slot_ordinal=1,
        outer_batch_id="batch-0001",
    )
    source = tmp_path / "paper-a.pdf"
    source.write_bytes(b"pdf")
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage01_package",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row={
            **_record("paper-a", decision="pass", passed=True),
            "package_status": "complete_confirmed_no_si",
        },
        artifacts=[source],
        imported=False,
    )
    source.unlink()
    store.update_selection_copy(
        selection["selection_id"],
        copy_state="materialized",
        local_assets_state="pruned_terminal",
    )

    plan = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage01_package",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
    )

    assert plan.action == "reuse"
    assert plan.status == "forwarded"


@pytest.mark.parametrize("stage", ["stage01", "stage01_package"])
def test_stage01_nonpass_is_terminal_instead_of_retryable(tmp_path: Path, stage: str):
    store = ResumeStateStore.for_run_root(tmp_path)
    row = _record("paper-a", decision="processing_failed", passed=False, failed=True)
    if stage == "stage01_package":
        row["package_status"] = "retryable_acquisition_error"
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage=stage,
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row=row,
        imported=False,
    )

    item = store.current_work_item(
        outer_batch_id="batch-0001", stage=stage, paper_id="paper-a"
    )
    assert item["status"] == "terminal_reject"


def test_pruned_legacy_stage01_failure_is_not_requeued(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    selection = store.reserve_selection(
        dataset="dataset",
        source_main_uri="s3://bucket/a.pdf",
        normalized_doi=None,
        source_record_key="a.pdf",
        paper_id="paper-a",
        target_slot_ordinal=1,
        outer_batch_id="batch-0001",
    )
    store.update_selection_copy(
        selection["selection_id"],
        copy_state="materialized",
        local_assets_state="pruned_terminal",
    )
    store.record_retryable_failure(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage01",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        failure_class="document_parse_failed",
        error={"message": "legacy retryable result"},
    )
    with store.transaction() as connection:
        connection.execute(
            "UPDATE stage_work_items SET status='retryable_failed' WHERE stage='stage01'"
        )

    assert store.terminalize_pruned_stage01_work() == 1

    plan = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage01",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
    )

    assert plan.action == "reuse"
    assert plan.status == "terminal_reject"
    item = store.current_work_item(
        outer_batch_id="batch-0001", stage="stage01", paper_id="paper-a"
    )
    assert item["failure_class"] == "stage01_assets_pruned_terminal"


def test_resume_detects_missing_declared_artifact_without_manifest(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage04",
        paper_id="paper-a",
        document_id="doc-a",
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row={
            **_record("paper-a", decision="pass", passed=True),
            "document_id": "doc-a",
            "content_blocks_path": str(tmp_path / "missing.jsonl"),
        },
        artifacts=(),
        imported=False,
    )

    plan = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage04",
        paper_id="paper-a",
        document_id="doc-a",
        config_fingerprint="config-a",
        input_fingerprint="input-a",
    )

    assert plan.action == "run"
    assert plan.status == "retryable_failed"


def test_imported_attempt_is_idempotent(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    kwargs = dict(
        generation=0,
        outer_batch_id="batch-0001",
        stage="stage03",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="",
        row=_record("paper-a", decision="software_covered", passed=True),
        imported=True,
    )
    first = store.record_result(**kwargs)
    second = store.record_result(**kwargs)

    assert first == second
    with store.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM stage_attempts").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM stage_work_items").fetchone()[0] == 1


def test_invalidated_work_can_rerun_with_the_same_configuration(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage03",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row=_record("paper-a", decision="software_covered", passed=True),
        imported=False,
    )

    assert store.invalidate_stage("stage03") == 1
    plan = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage03",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        invalidated=True,
    )

    assert plan.action == "run"
    with store.connect() as connection:
        current = connection.execute(
            "SELECT status, is_current FROM stage_work_items WHERE stage='stage03'"
        ).fetchone()
        attempts = connection.execute(
            "SELECT COUNT(*) FROM stage_attempts WHERE stage='stage03'"
        ).fetchone()[0]
    assert dict(current) == {"status": "running", "is_current": 1}
    assert attempts == 1


def test_invalidation_cascades_to_child_checkpoints_and_downstream():
    assert expanded_invalidation(["stage03"]) == (
        "stage03",
        "stage04",
        "stage05_router",
        "stage05_auditor",
        "stage05",
    )
    assert expanded_invalidation(["stage05"]) == (
        "stage05_router",
        "stage05_auditor",
        "stage05",
    )


def test_batch_scoped_invalidation_does_not_touch_other_batches(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    for batch in ("batch-0001", "batch-0002"):
        store.record_result(
            generation=1,
            outer_batch_id=batch,
            stage="stage03",
            paper_id=f"paper-{batch[-1]}",
            document_id=None,
            config_fingerprint="config-a",
            input_fingerprint="input-a",
            row=_record(f"paper-{batch[-1]}", decision="software_covered", passed=True),
            imported=False,
        )

    changed = store.invalidate_stages(["stage03"], outer_batch_ids=["batch-0002"])

    assert changed == {"stage03": 1}
    assert store.current_work_items(outer_batch_id="batch-0001", stage="stage03")
    assert not store.current_work_items(outer_batch_id="batch-0002", stage="stage03")


def test_downstream_retry_is_blocked_when_upstream_did_not_forward(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    store.record_result(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage02",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-a",
        input_fingerprint="input-a",
        row=_record(
            "paper-a", decision="computational_content_not_found", passed=False
        ),
        imported=False,
    )
    store.record_retryable_failure(
        generation=1,
        outer_batch_id="batch-0001",
        stage="stage03",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-b",
        input_fingerprint="input-b",
        failure_class="stage03_service_unavailable",
        error={"message": "HTTP 504"},
    )

    assert store.mark_blocked_by_missing_upstream(through_stage="stage05") == 1
    item = store.current_work_item(
        outer_batch_id="batch-0001", stage="stage03", paper_id="paper-a"
    )
    assert item["status"] == "blocked_by_upstream"

    released = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage03",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-b",
        input_fingerprint="input-b",
        retry_only=True,
        upstream_ready=True,
    )
    assert released.action == "run"
    assert released.status == "retryable_failed"


def test_never_started_downstream_stays_pending_in_retry_only_mode(tmp_path: Path):
    store = ResumeStateStore.for_run_root(tmp_path)
    store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage03",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-b",
        input_fingerprint="input-b",
        allow_pending=False,
    )
    assert store.mark_blocked_by_missing_upstream(through_stage="stage05") == 1

    released = store.plan_work(
        outer_batch_id="batch-0001",
        stage="stage03",
        paper_id="paper-a",
        document_id=None,
        config_fingerprint="config-b",
        input_fingerprint="input-b",
        retry_only=True,
        upstream_ready=True,
    )

    assert released.action == "skip"
    assert released.status == "pending"


def test_dry_run_expansion_does_not_create_batch_configs(tmp_path: Path):
    template = tmp_path / "template.json"
    write_json(template, _minimal_config(tmp_path))

    _store, specs, plan = prepare_resume(
        run_root=tmp_path / "run",
        total=3,
        batch_size=2,
        template_path=template,
        stop_stage="stage00",
        materialize_expansion=False,
    )

    assert [item.count for item in specs] == [2, 1]
    assert plan["new_target_slots"] == 3
    assert not (tmp_path / "run" / "configs").exists()


def test_command_digest_accepts_cli_paths(tmp_path: Path):
    assert command_digest({"run_root": tmp_path, "batches": ["batch-0001"]})


def test_resume_store_defaults_to_shared_filesystem_safe_journal(tmp_path: Path):
    import sqlite3

    store = ResumeStateStore.for_run_root(tmp_path)
    with store.connect() as connection:
        assert connection.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "INSERT INTO import_events VALUES (?, ?, ?, ?)",
            ("test", str(tmp_path), "sha", "2026-01-01T00:00:00+00:00"),
        )
        connection.commit()
    with sqlite3.connect(store.database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM import_events").fetchone()[0] == 1


def test_stage01_runtime_service_injection_keeps_scientific_fingerprint(tmp_path: Path):
    config_path = tmp_path / "config.json"
    write_json(config_path, _minimal_config(tmp_path))
    baseline = load_config(config_path)
    prepared = json.loads(json.dumps(baseline))
    grobid = prepared["stage01"]["normalization"]["grobid"]

    assert grobid["environment"] == {}
    grobid.update(
        {
            "_sandbox_instance": 0,
            "_sandbox_runtime": None,
            "base_url": "http://127.0.0.1:39117",
            "manage_service": True,
            "timeout_seconds": 14_700,
        }
    )

    assert scientific_stage_fingerprints(prepared)["stage01"] == (
        scientific_stage_fingerprints(baseline)["stage01"]
    )


def test_stage04_storage_cleanup_keeps_scientific_fingerprint(tmp_path: Path):
    config_path = tmp_path / "config.json"
    write_json(config_path, _minimal_config(tmp_path))
    baseline = load_config(config_path)
    retained = json.loads(json.dumps(baseline))
    retained["stage04"]["mineru"]["cleanup_successful_intermediates"] = False

    assert scientific_stage_fingerprints(retained)["stage04"] == (
        scientific_stage_fingerprints(baseline)["stage04"]
    )


def test_stage_range_only_requests_sandbox_for_local_services():
    config = {
        "stage03": {"softcite": {"enabled": False}},
        "stage04": {"mineru": {"enabled": True, "managed_gpu": False}},
    }
    assert _stage_range_requires_sandbox(config, "stage01", "stage01")
    assert not _stage_range_requires_sandbox(config, "stage02", "stage03")
    assert _stage_range_requires_sandbox(config, "stage04", "stage05")
    assert not _stage_range_requires_sandbox(config, "stage05", "stage05")


def test_expansion_freezes_old_config_and_only_appends(tmp_path: Path):
    run_root = tmp_path / "run"
    template = tmp_path / "template.json"
    config = _minimal_config(tmp_path)
    write_json(template, config)
    write_json(
        run_root / "configs" / "batch-0001.json",
        {
            **config,
            "workspace": str(run_root / "batches" / "batch-0001"),
            "stage00": {**config["stage00"], "count": 2},
        },
    )
    original = (run_root / "configs" / "batch-0001.json").read_bytes()

    _store, specs, plan = prepare_resume(
        run_root=run_root,
        total=5,
        batch_size=2,
        template_path=template,
        stop_stage="stage00",
    )

    assert (run_root / "configs" / "batch-0001.json").read_bytes() == original
    assert [item.batch_id for item in specs] == ["batch-0001", "batch-0002", "batch-0003"]
    assert [item.count for item in specs] == [2, 2, 1]
    assert plan["new_batches"] == ["batch-0002", "batch-0003"]


def test_legacy_import_is_idempotent_and_classifies_objective_failure(tmp_path: Path):
    run_root = tmp_path / "run"
    batch = run_root / "batches" / "batch-0001"
    config = _minimal_config(tmp_path)
    config["workspace"] = str(batch)
    config["stage00"]["count"] = 1
    write_json(run_root / "configs" / "batch-0001.json", config)
    source = {
        "paper_id": "paper-a",
        "dataset": "en-paper-hzzj",
        "copy_status": "complete",
        "main_document": {
            "remote_uri": "s3://bucket/a.pdf",
            "sha256": "abc",
        },
    }
    from src.core.io import write_jsonl

    write_jsonl(batch / "stage_00_remote_corpus" / "source_manifest.jsonl", [source])
    write_jsonl(
        batch / "stage_02_computational_content" / "decisions.jsonl",
        [_record("paper-a", decision="processing_failed", passed=False, failed=True)],
    )
    store = ResumeStateStore.for_run_root(run_root)

    import_legacy_run(run_root, store)
    second = import_legacy_run(run_root, store)

    item = store.current_work_item(
        outer_batch_id="batch-0001", stage="stage02", paper_id="paper-a"
    )
    assert item["status"] == "retryable_failed"
    with store.connect() as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM stage_attempts WHERE stage='stage02'"
        ).fetchone()[0] == 1
    assert second["batches"][0]["status"] == "already_imported"


def _minimal_config(root: Path):
    model = {
        "enabled": True,
        "base_url": "http://127.0.0.1:9/v1",
        "model": "test-model",
        "api_key_env": "TEST_API_KEY",
        "workers": 1,
        "use_proxy": False,
    }
    return {
        "pipeline_contract": "researchchembench-data-pipeline/v2",
        "workspace": str(root / "workspace"),
        "stop_after": "stage00",
        "registry": {
            "enabled": False,
            "database": str(root / "registry.sqlite"),
            "export_jsonl": str(root / "registry.jsonl"),
            "prune_rejected_stage00_assets": False,
        },
        "execution": {"backend": "local", "sandbox": {}},
        "source": {"root": str(root)},
        "stage00": {
            "enabled": True,
            "dataset": "en-paper-hzzj",
            "count": 2,
            "credentials": str(root / "credentials"),
            "resume": True,
        },
        "stage01": {"package": {}, "normalization": {"grobid": {}}},
        "stage02": {"model_role": "stage02_screening"},
        "stage03": {
            "model_role": "stage03_screening",
            "toolbox_capabilities": str(root / "capabilities.json"),
            "software_aliases": str(root / "aliases.json"),
            "external_software_aliases": str(root / "external.json"),
        },
        "stage04": {"mineru": {"enabled": False}},
        "stage05": {},
        "stage06": {"harness": "direct_api"},
        "stage07": {"harness": "direct_api"},
        "microbatch": {},
        "models": {
            "screening": model,
            "stage02_screening": model,
            "stage03_screening": model,
            "stage05_router": model,
            "suitability": model,
            "builder": model,
            "judge": model,
        },
    }
