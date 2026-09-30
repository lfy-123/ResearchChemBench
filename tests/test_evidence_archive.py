import json
from pathlib import Path
import shutil

import pytest

from evaluation.provenance.evidence_archive import build_run_index, export_run_archive, open_archive, resolve_reference
from evaluation.scoring.evidence import build_evidence_bundle, read_evidence_excerpt


def saved_run(tmp_path):
    root = tmp_path / "run"
    directory = root / "outputs/execution_jobs/job_example"
    directory.mkdir(parents=True)
    (root / "_meta.json").write_text(json.dumps({"run_id": "run", "api_key": "must-not-export"}))
    (root / "report").mkdir()
    (root / "report/report.md").write_text("Structure and numerical output are in the job files.")
    (directory / "request.json").write_text(json.dumps({"job_type": "native_software", "metadata": {"software_id": "orca"}, "staged_inputs": []}))
    (directory / "status.json").write_text(json.dumps({"job_id": "job_example", "status": "failed"}))
    (directory / "stdout.log").write_text("ORCA finished by error\n")
    (directory / "input.xyz").write_text("1\nOptimized geometry\nHe 0 0 0\n")
    cache = directory / ".cache"
    cache.mkdir()
    (cache / "fontlist.json").write_text("cache")
    return root


def test_portable_archive_preserves_failures_and_excludes_credentials(tmp_path):
    root = saved_run(tmp_path)
    before = (root / "_meta.json").read_bytes()
    index = build_run_index(root)
    assert index["jobs"][0]["state"] == "failed"
    assert not any("fontlist" in f["ref"] for f in index["files"])
    destination = tmp_path / "archive"
    archive = export_run_archive(root, destination)
    assert (root / "_meta.json").read_bytes() == before
    assert "must-not-export" not in (destination / "workspace/_meta.json").read_text()
    shutil.rmtree(root)
    archive = open_archive(destination)
    assert archive["verification"]["state"] == "complete"
    bundle = build_evidence_bundle(archive)
    assert any("input.xyz" in e["ref"] for e in bundle["excerpts"])
    assert all(resolve_reference(archive, f["ref"]).exists() for f in archive["files"])


def test_arche_archive_keeps_evidence_without_private_provider_homes(tmp_path):
    root = saved_run(tmp_path)
    for name in ("codex_home/session.jsonl", "codex_runtime/large-binary", "traces/model.jsonl", "evidence/result.json"):
        path = root / "outputs/arche/tasks/session" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}")
    index = export_run_archive(root, tmp_path / "archive")
    refs = {f["ref"] for f in index["files"]}
    assert not any("codex_home" in f or "codex_runtime" in f for f in refs)
    assert "workspace/outputs/arche/tasks/session/traces/model.jsonl" in refs
    assert "workspace/outputs/arche/tasks/session/evidence/result.json" in refs


def test_missing_and_escaping_references_are_explicit(tmp_path):
    root = saved_run(tmp_path)
    index = build_run_index(root)
    with pytest.raises(ValueError):
        read_evidence_excerpt(index, "../../etc/passwd")
    archive = export_run_archive(root, tmp_path / "archive")
    resolve_reference(archive, "workspace/outputs/execution_jobs/job_example/stdout.log").unlink()
    assert open_archive(tmp_path / "archive")["verification"]["state"] == "archive_incomplete"


def test_cache_cannot_displace_provenance_evidence(tmp_path):
    root = saved_run(tmp_path)
    bundle = build_evidence_bundle(root)
    assert bundle["jobs"][0]["job_id"] == "job_example"
    xyz = next(e for e in bundle["excerpts"] if e["ref"].endswith("input.xyz"))
    assert xyz["role"] == "job_output"
    assert xyz["producer"] == "job_example"
    assert "fontlist" not in json.dumps(bundle)


def test_evidence_only_never_runs_provider_or_subprocess(tmp_path, monkeypatch):
    from evaluation.scoring.cli import main
    import subprocess
    def fail(*args, **kwargs):
        raise AssertionError("evidence-only must not start a process")
    monkeypatch.setattr(subprocess, "Popen", fail)
    assert main(["--workspace", str(saved_run(tmp_path)), "--evidence-only", "--output-dir", str(tmp_path / "evidence")]) == 0


def test_compressed_logs_keep_logical_references(tmp_path):
    root = saved_run(tmp_path)
    log = root / "outputs/execution_jobs/job_example/stdout.log"
    log.write_text("header\n" + "calculation detail\n" * 10000 + "ORCA TERMINATED NORMALLY\n")
    archive = export_run_archive(root, tmp_path / "archive", compress_logs=True)
    ref = "workspace/outputs/execution_jobs/job_example/stdout.log"
    assert resolve_reference(archive, ref).suffix == ".gz"
    assert read_evidence_excerpt(archive, ref, max_chars=7)["content"] == "header\n"
    assert archive["verification"]["state"] == "complete"
    assert build_evidence_bundle(archive)["native_observations"][0]["normal_termination"] is True


@pytest.mark.parametrize("envelope", [False, True])
def test_legacy_and_enveloped_action_results_survive_export(tmp_path, envelope):
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    root = saved_run(tmp_path)
    store = ExecutionStore(root, run_id="run")
    receipt = store.accept_submission(submission_key="original", entity_type="job", request={},
        spec={"job_type":"predefined_action", "action_id":"calculate_energy"})
    result = {"action":"calculate_energy", "status":"failed", "error":{"code":"native_error", "message":"specific reason"}, "result":{"energy": -1.0}}
    folder = store.directory / "action_results"
    folder.mkdir()
    path = folder / (receipt.entity_id + (".envelope.json" if envelope else ".json"))
    path.write_text(json.dumps({"action_result": result} if envelope else result))
    archive = export_run_archive(root, tmp_path / "archive")
    shutil.rmtree(root)
    shutil.rmtree(store.directory)
    bundle = build_evidence_bundle(archive)
    job = next(j for j in bundle["jobs"] if j["job_id"] == receipt.entity_id)
    assert job["result_ref"].startswith("control/action_results/")
    excerpt = next(e for e in bundle["excerpts"] if e["ref"] == job["result_ref"])
    assert json.loads(excerpt["content"])["error"]["message"] == "specific reason"


def test_export_interruption_is_atomic_and_does_not_leave_partial_package(tmp_path, monkeypatch):
    root = saved_run(tmp_path)
    original = shutil.copy2
    def fail(source, target, **kw):
        original(source, target, **kw)
        raise OSError("disk full fixture")
    monkeypatch.setattr(shutil, "copy2", fail)
    with pytest.raises(OSError, match="disk full"):
        export_run_archive(root, tmp_path / "archive")
    assert not (tmp_path / "archive").exists()
    assert not list(tmp_path.glob(".archive-*"))


def test_required_evidence_cannot_be_silently_truncated(tmp_path):
    root = saved_run(tmp_path)
    path = root / "outputs/essential.json"
    path.write_text(json.dumps({"values": list(range(2000)), "conclusion":"late critical evidence"}))
    (root / "report/report.md").write_text("Result: outputs/essential.json")
    bundle = build_evidence_bundle(root, {"max_chars":2000})
    assert bundle["coverage"]["requires_review"]
    assert bundle["coverage"]["important_truncations"] == ["workspace/outputs/essential.json"]
    complete = build_evidence_bundle(root)
    assert complete["coverage"]["retrieval_available"]
    assert any("late critical evidence" in e["content"] for e in complete["excerpts"])


def test_action_result_arrays_are_complete_or_explicitly_require_review(tmp_path):
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    root = saved_run(tmp_path)
    store = ExecutionStore(root, run_id="run")
    receipt = store.accept_submission(submission_key="series", entity_type="job", request={},
        spec={"job_type":"predefined_action", "action_id":"calculate_energy"})
    folder = store.directory / "action_results"
    folder.mkdir()
    path = folder / (receipt.entity_id + ".json")
    values = list(range(100))
    path.write_text(json.dumps({"status":"success", "result":{"series":values}}))
    bundle = build_evidence_bundle(root)
    excerpt = next(e for e in bundle["excerpts"] if e["role"] == "action_result")
    assert json.loads(excerpt["content"])["result"]["series"] == values
    assert not bundle["coverage"]["requires_review"]
    path.write_text(json.dumps({"status":"success", "result":{"series":list(range(30000))}}))
    bundle = build_evidence_bundle(root)
    assert bundle["coverage"]["requires_review"]
    assert any(ref.endswith(path.name) for ref in bundle["coverage"]["important_truncations"])


def test_export_rejects_snapshot_claim_when_an_earlier_file_changes(tmp_path, monkeypatch):
    root = saved_run(tmp_path)
    original = shutil.copy2
    report = root / "report/report.md"
    def change_after_copy(source, target, **kwargs):
        result = original(source, target, **kwargs)
        report.write_text("Changed while exporting another file")
        return result
    monkeypatch.setattr(shutil, "copy2", change_after_copy)
    index = export_run_archive(root, tmp_path / "archive")
    assert index["verification"]["state"] == "archive_incomplete"
    assert any(problem["reason"] == "source_changed_during_export" for problem in index["problems"])
    assert build_evidence_bundle(index)["coverage"]["blocking_sources"]


def test_active_agent_export_remains_incomplete_even_with_no_running_job(tmp_path):
    root = saved_run(tmp_path)
    (root / "_meta.json").write_text('{"run_id":"run","status":"running"}')
    index = export_run_archive(root, tmp_path / "archive")
    assert index["verification"]["state"] == "archive_incomplete"
    assert any(problem["reason"] == "active_agent_during_export" for problem in index["problems"])
