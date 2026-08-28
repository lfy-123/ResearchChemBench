from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from src.registry import ScreeningRegistry


def _stage00_fixture(tmp_path: Path, paper_id: str = "paper-fixture"):
    stage_root = tmp_path / "run" / "stage_00_remote_corpus"
    bundle = stage_root / "corpus" / paper_id
    (bundle / "main").mkdir(parents=True)
    (bundle / "supplementary").mkdir()
    (bundle / "main" / "paper.pdf").write_bytes(b"main-pdf")
    (bundle / "supplementary" / "si.pdf").write_bytes(b"si-pdf")
    row = {
        "paper_id": paper_id,
        "dataset": "fixture",
        "doi": "10.1000/fixture",
        "title": "Fixture paper",
        "copy_status": "complete",
        "main_document": {
            "remote_uri": "s3://fixture/paper.pdf",
            "sha256": "main-hash",
        },
        "supplementary_documents": [{"remote_uri": "s3://fixture/si.pdf", "sha256": "si-hash"}],
    }
    manifest = stage_root / "source_manifest.jsonl"
    manifest.write_text(json.dumps(row) + "\n", encoding="utf-8")
    return stage_root, bundle, manifest, row


def _registry(tmp_path: Path) -> ScreeningRegistry:
    return ScreeningRegistry(
        tmp_path / "registry" / "papers.sqlite",
        export_jsonl=tmp_path / "registry" / "papers.jsonl",
    )


def test_registry_commits_stage03_rejection_before_deleting_stage00_bundle(
    tmp_path: Path,
) -> None:
    stage_root, bundle, manifest, row = _stage00_fixture(tmp_path)
    registry = _registry(tmp_path)
    registry.start_run(
        run_id="run-1",
        workspace=tmp_path / "run",
        config_path=tmp_path / "config.json",
        config_hash="config-hash",
    )
    registry.register_stage00_manifest(
        run_id="run-1",
        manifest_path=manifest,
        corpus_root=stage_root / "corpus",
    )

    summary = registry.record_stage_results(
        run_id="run-1",
        stage="stage03",
        rows=[
            {
                "paper_id": row["paper_id"],
                "decision": "core_software_uncovered",
                "passed": False,
                "software_mentions": [
                    {
                        "raw_name": "Molpro",
                        "role": "core_compute",
                        "actual_use": True,
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "software_mappings": [{"normalized_identifier": None, "catalog_present": False}],
            }
        ],
    )

    assert not bundle.exists()
    assert summary["deleted"] == 1
    assert summary["bytes_freed"] == len(b"main-pdf") + len(b"si-pdf")
    with sqlite3.connect(registry.database) as connection:
        decision, passed = connection.execute(
            "SELECT decision, passed FROM stage_results WHERE stage='stage03'"
        ).fetchone()
        asset_state = connection.execute("SELECT asset_state FROM paper_sources").fetchone()[0]
        software = connection.execute(
            "SELECT raw_name, catalog_present FROM software_mentions"
        ).fetchone()
    assert (decision, passed) == ("core_software_uncovered", 0)
    assert asset_state == "deleted"
    assert software == ("Molpro", 0)


def test_registry_prunes_rejected_stage01_attempt_attachment(tmp_path: Path) -> None:
    stage_root, bundle, manifest, row = _stage00_fixture(tmp_path)
    acquisition = (
        tmp_path
        / "run"
        / "resume_attempts"
        / "generation-0002"
        / "stage01_package"
        / "stage_01_document_preparation"
        / "package"
        / "acquisition"
        / "files"
        / row["paper_id"]
    )
    acquisition.mkdir(parents=True)
    (acquisition / "publisher-si.docx").write_bytes(b"downloaded-si")
    registry = _registry(tmp_path)
    registry.start_run(
        run_id="run-acquisition",
        workspace=tmp_path / "run",
        config_path=tmp_path / "config.json",
        config_hash="config-hash",
    )
    registry.register_stage00_manifest(
        run_id="run-acquisition",
        manifest_path=manifest,
        corpus_root=stage_root / "corpus",
    )

    summary = registry.record_stage_results(
        run_id="run-acquisition",
        stage="stage02",
        rows=[
            {
                "paper_id": row["paper_id"],
                "decision": "computational_content_not_found",
                "passed": False,
                "processing_status": "completed",
            }
        ],
    )

    assert not bundle.exists()
    assert not acquisition.exists()
    assert summary["auxiliary_deleted"] == 1
    assert summary["auxiliary_bytes_freed"] == len(b"downloaded-si")
    with sqlite3.connect(registry.database) as connection:
        action, status = connection.execute(
            """
            SELECT action, status FROM artifact_events
            WHERE action='delete_stage01_acquisition_bundle'
            """
        ).fetchone()
    assert (action, status) == ("delete_stage01_acquisition_bundle", "deleted")


def test_registry_keeps_retryable_stage01_attempt_attachment(tmp_path: Path) -> None:
    stage_root, bundle, manifest, row = _stage00_fixture(tmp_path)
    acquisition = (
        tmp_path
        / "run"
        / "resume_attempts"
        / "generation-0002"
        / "stage01_package"
        / "stage_01_document_preparation"
        / "package"
        / "acquisition"
        / "files"
        / row["paper_id"]
    )
    acquisition.mkdir(parents=True)
    (acquisition / "publisher-si.docx").write_bytes(b"downloaded-si")
    registry = _registry(tmp_path)
    registry.start_run(
        run_id="run-retryable",
        workspace=tmp_path / "run",
        config_path=tmp_path / "config.json",
        config_hash="config-hash",
    )
    registry.register_stage00_manifest(
        run_id="run-retryable",
        manifest_path=manifest,
        corpus_root=stage_root / "corpus",
    )

    summary = registry.record_stage_results(
        run_id="run-retryable",
        stage="stage02",
        rows=[
            {
                "paper_id": row["paper_id"],
                "decision": "processing_failed",
                "passed": False,
                "processing_status": "failed",
                "failure_disposition": "retryable",
            }
        ],
    )

    assert bundle.is_dir()
    assert acquisition.is_dir()
    assert summary["auxiliary_deleted"] == 0


@pytest.mark.parametrize(
    ("decision", "processing_status", "failure_disposition"),
    [
        ("processing_failed", "failed", "retryable"),
        ("processing_pending", "pending", "pending"),
        ("uncertain", "completed", None),
    ],
)
def test_registry_prunes_every_nonpassing_stage01_result(
    tmp_path: Path,
    decision: str,
    processing_status: str,
    failure_disposition: str | None,
) -> None:
    stage_root, bundle, manifest, row = _stage00_fixture(tmp_path)
    acquisition = (
        tmp_path
        / "run"
        / "resume_attempts"
        / "generation-0002"
        / "stage01_package"
        / "stage_01_document_preparation"
        / "package"
        / "acquisition"
        / "files"
        / row["paper_id"]
    )
    acquisition.mkdir(parents=True)
    (acquisition / "publisher-si.docx").write_bytes(b"downloaded-si")
    registry = _registry(tmp_path)
    registry.start_run(
        run_id="run-stage01-terminal",
        workspace=tmp_path / "run",
        config_path=tmp_path / "config.json",
        config_hash="config-hash",
    )
    registry.register_stage00_manifest(
        run_id="run-stage01-terminal",
        manifest_path=manifest,
        corpus_root=stage_root / "corpus",
    )

    summary = registry.record_stage_results(
        run_id="run-stage01-terminal",
        stage="stage01",
        rows=[
            {
                "paper_id": row["paper_id"],
                "decision": decision,
                "passed": False,
                "processing_status": processing_status,
                "failure_disposition": failure_disposition,
            }
        ],
    )

    assert not bundle.exists()
    assert not acquisition.exists()
    assert summary["deleted_paper_ids"] == [row["paper_id"]]
    assert summary["auxiliary_deleted"] == 1


def test_registry_never_prunes_stage04_or_later_rejections(tmp_path: Path) -> None:
    for stage in ("stage04", "stage05", "stage06", "stage07"):
        stage_root, bundle, manifest, row = _stage00_fixture(tmp_path / stage)
        registry = _registry(tmp_path / stage)
        registry.start_run(
            run_id=f"run-{stage}",
            workspace=tmp_path / stage / "run",
            config_path=tmp_path / "config.json",
            config_hash="config-hash",
        )
        registry.register_stage00_manifest(
            run_id=f"run-{stage}",
            manifest_path=manifest,
            corpus_root=stage_root / "corpus",
        )

        registry.record_stage_results(
            run_id=f"run-{stage}",
            stage=stage,
            rows=[{"paper_id": row["paper_id"], "decision": "reject", "passed": False}],
        )

        assert bundle.is_dir(), stage


@pytest.mark.parametrize("decision", ["uncertain", "processing_failed"])
def test_registry_preserves_stage02_hold_assets(tmp_path: Path, decision: str) -> None:
    stage_root, bundle, manifest, row = _stage00_fixture(tmp_path)
    registry = _registry(tmp_path)
    registry.start_run(
        run_id="run-hold",
        workspace=tmp_path / "run",
        config_path=tmp_path / "config.json",
        config_hash="config-hash",
    )
    registry.register_stage00_manifest(
        run_id="run-hold",
        manifest_path=manifest,
        corpus_root=stage_root / "corpus",
    )

    summary = registry.record_stage_results(
        run_id="run-hold",
        stage="stage02",
        rows=[{"paper_id": row["paper_id"], "decision": decision, "passed": False}],
    )

    assert bundle.is_dir()
    assert summary["deleted"] == 0


def test_registry_exports_rejected_paper_after_assets_are_deleted(tmp_path: Path) -> None:
    stage_root, bundle, manifest, row = _stage00_fixture(tmp_path)
    registry = _registry(tmp_path)
    registry.start_run(
        run_id="run-export",
        workspace=tmp_path / "run",
        config_path=tmp_path / "config.json",
        config_hash="config-hash",
    )
    registry.register_stage00_manifest(
        run_id="run-export",
        manifest_path=manifest,
        corpus_root=stage_root / "corpus",
    )
    registry.record_stage_results(
        run_id="run-export",
        stage="stage02",
        rows=[
            {
                "paper_id": row["paper_id"],
                "decision": "not_pure_computational",
                "passed": False,
                "validated_evidence": [{"evidence_id": "ev-1"}],
            }
        ],
    )

    summary = registry.finish_run(run_id="run-export", status="completed")
    exported = json.loads(registry.export_path.read_text(encoding="utf-8").splitlines()[0])

    assert not bundle.exists()
    assert summary["source_assets"]["deleted"] == 1
    assert exported["sources"][0]["asset_state"] == "deleted"
    assert exported["sources"][0]["main_remote_uri"] == "s3://fixture/paper.pdf"
    assert exported["stages"]["stage02"][0]["decision"] == "not_pure_computational"
