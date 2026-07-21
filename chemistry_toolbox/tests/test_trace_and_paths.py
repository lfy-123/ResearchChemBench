import json
from pathlib import Path

import pytest

from chemistry_toolbox.mcp import tracing
from chemistry_toolbox.mcp.tracing import execute_traced
from chemistry_toolbox.mcp.workspace import (
    resolve_workspace_output_path,
    resolve_workspace_path,
)
from evaluation.trace import load_tool_trace, normalized_tool_calls, process_metrics


def test_workspace_path_confinement(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    safe = resolve_workspace_path("outputs/result.json", create_parent=True)
    assert safe == tmp_path / "outputs" / "result.json"
    with pytest.raises(ValueError):
        resolve_workspace_path("../hidden/ground_truth.json")
    with pytest.raises(ValueError):
        resolve_workspace_output_path("data/overwrite.xyz")
    with pytest.raises(ValueError):
        resolve_workspace_output_path("_meta.json")


def test_workspace_rejects_symlink_escape(tmp_path: Path, monkeypatch):
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret", encoding="utf-8")
    (tmp_path / "link").symlink_to(outside, target_is_directory=True)
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    with pytest.raises(ValueError, match="Symlink"):
        resolve_workspace_path("link/secret.txt", must_exist=True)


def test_traced_execution_records_result_and_artifact(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_RUN_ID", "test-run")
    (tmp_path / "outputs").mkdir()

    def operation():
        (tmp_path / "outputs" / "value.json").write_text('{"value": 4}\n')
        return {"value": 4}

    assert execute_traced("fake_tool", {"x": 2}, operation) == {"value": 4}
    events = load_tool_trace(tmp_path)
    assert len(events) == 1
    assert events[0]["status"] == "success"
    assert events[0]["artifacts"][0]["path"] == "outputs/value.json"
    assert normalized_tool_calls(events) == [{"fake_tool": {"x": 2}}]
    assert process_metrics(events)["successful_tool_calls"] == 1
    result = json.loads((tmp_path / events[0]["result_path"]).read_text())
    assert result["result"] == {"value": 4}


def test_trace_sequence_does_not_overwrite_after_multiple_calls(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    execute_traced("first", {}, lambda: 1)
    execute_traced("second", {}, lambda: 2)
    results = sorted((tmp_path / "_tool_results").glob("[0-9]*.json"))
    assert [path.name for path in results] == ["0001_first.json", "0002_second.json"]


def test_trace_records_action_status_instead_of_transport_success(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    returned = execute_traced(
        "calculate_energy",
        {"backend_id": "xtb"},
        lambda: {
            "status": "failed",
            "error": {"code": "backend_failed", "message": "calculation failed"},
        },
    )
    assert returned["status"] == "failed"
    events = load_tool_trace(tmp_path)
    assert events[0]["status"] == "failed"
    assert events[0]["transport_status"] == "success"
    assert normalized_tool_calls(events) == []
    assert process_metrics(events)["failed_tool_calls"] == 1
    result = json.loads((tmp_path / events[0]["result_path"]).read_text())
    assert result["status"] == "failed"
    assert result["transport_status"] == "success"


def test_invalid_trace_limits_are_rejected_before_tool_execution(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEM_MCP_MAX_ARTIFACT_FILES", "not-an-integer")
    called = False

    def operation():
        nonlocal called
        called = True
        return 123

    with pytest.raises(ValueError, match="positive integer"):
        execute_traced("never_started", {}, operation)
    assert not called


def test_trace_failure_does_not_replace_original_tool_exception(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def fail_capture(*_args, **_kwargs):
        raise OSError("simulated trace failure")

    monkeypatch.setattr(tracing, "_capture_changed_artifacts", fail_capture)

    def operation():
        raise KeyError("original tool failure")

    with pytest.raises(KeyError, match="original tool failure"):
        execute_traced("failing_tool", {}, operation)
