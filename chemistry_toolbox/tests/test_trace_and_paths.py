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


def test_resource_budget_rejections_are_counted(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    execute_traced(
        "calculate_energy",
        {"backend_id": "xtb"},
        lambda: {
            "status": "invalid_request",
            "error": {
                "code": "resource_budget_exceeded",
                "message": "requested resources exceed the task budget",
            },
        },
    )
    metrics = process_metrics(load_tool_trace(tmp_path), workspace=tmp_path)
    assert metrics["resource_budget_rejection_count"] == 1
    assert metrics["invalid_request_count"] == 1
    assert metrics["request_rejection_count"] == 1
    assert metrics["policy_rejection_count"] == 1


def test_preflight_and_terminal_job_failures_have_separate_metrics() -> None:
    job_id = "job_failed"
    events = [
        {
            "sequence": 1,
            "tool": "submit_analysis_program",
            "status": "invalid_request",
            "arguments": {},
            "result_preview": json.dumps(
                {
                    "status": "invalid_request",
                    "error": {"code": "unstaged_workspace_relative_path"},
                }
            ),
        },
        _job_event(
            2,
            "submit_native_job",
            {"status": "success", "job_id": job_id, "job_status": "queued"},
            job_id,
        ),
        _job_event(
            3,
            "get_execution_job",
            {"status": "success", "job": {"job_id": job_id, "status": "failed"}},
            job_id,
        ),
    ]
    metrics = process_metrics(events)
    assert metrics["preflight_rejection_count"] == 1
    assert metrics["invalid_request_count"] == 1
    assert metrics["request_rejection_count"] == 1
    assert metrics["failed_execution_job_count"] == 1
    assert metrics["backend_execution_failure_count"] == 1


def test_process_metrics_report_job_context_adoption_and_bypass() -> None:
    events = [
        _job_event(
            1,
            "submit_analysis_program",
            {
                "status": "success",
                "job_id": "job_compliant",
                "job_status": "queued",
                "job_context_compliance": {
                    "status": "compliant",
                    "job_context_imported": True,
                },
            },
            "job_compliant",
        ),
        _job_event(
            2,
            "submit_analysis_program",
            {
                "status": "success",
                "job_id": "job_bypassed",
                "job_status": "queued",
                "job_context_compliance": {
                    "status": "bypassed",
                    "job_context_imported": True,
                },
            },
            "job_bypassed",
        ),
        _job_event(
            3,
            "submit_analysis_program",
            {
                "status": "success",
                "job_id": "job_plain",
                "job_status": "queued",
                "job_context_compliance": {
                    "status": "not_adopted",
                    "job_context_imported": False,
                },
            },
            "job_plain",
        ),
    ]

    metrics = process_metrics(events)

    assert metrics["analysis_program_submission_count"] == 3
    assert metrics["job_context_audited_job_count"] == 3
    assert metrics["job_context_import_count"] == 2
    assert metrics["job_context_compliant_job_count"] == 1
    assert metrics["job_context_bypass_count"] == 1
    assert metrics["job_context_not_adopted_count"] == 1


def _job_event(sequence: int, tool: str, result: dict, job_id: str) -> dict:
    return {
        "sequence": sequence,
        "tool": tool,
        "status": "success",
        "arguments": {"request": {"job_id": job_id}},
        "result_preview": json.dumps(result),
    }


@pytest.mark.parametrize(
    ("terminal_state", "successes", "failures", "incomplete"),
    [
        ("success", 1, 0, 0),
        ("failed", 0, 1, 0),
        ("timeout", 0, 1, 0),
        ("running", 0, 1, 1),
    ],
)
def test_managed_job_metrics_use_observed_terminal_state(
    terminal_state: str, successes: int, failures: int, incomplete: int
):
    job_id = "job_example"
    events = [
        _job_event(
            1,
            "submit_analysis_program",
            {"status": "success", "job_id": job_id, "job_status": "queued"},
            job_id,
        ),
        _job_event(
            2,
            "get_execution_job",
            {
                "status": "success",
                "job": {"job_id": job_id, "status": terminal_state},
            },
            job_id,
        ),
    ]

    metrics = process_metrics(events)

    assert metrics["managed_scientific_attempt_count"] == 1
    assert metrics["successful_managed_scientific_calls"] == successes
    assert metrics["failed_managed_scientific_calls"] == failures
    assert metrics["incomplete_managed_scientific_calls"] == incomplete


def test_unobserved_queued_managed_job_is_not_counted_as_success():
    job_id = "job_unobserved"
    metrics = process_metrics(
        [
            _job_event(
                1,
                "submit_native_job",
                {"status": "success", "job_id": job_id, "job_status": "queued"},
                job_id,
            )
        ]
    )

    assert metrics["successful_managed_scientific_calls"] == 0
    assert metrics["failed_managed_scientific_calls"] == 1
    assert metrics["incomplete_managed_scientific_calls"] == 1


def test_wait_execution_jobs_updates_states_and_supervision_metrics() -> None:
    success_id = "job_wait_success"
    running_id = "job_wait_running"
    events = [
        _job_event(
            1,
            "submit_native_job",
            {"status": "success", "job_id": success_id, "job_status": "queued"},
            success_id,
        ),
        _job_event(
            2,
            "submit_analysis_program",
            {"status": "success", "job_id": running_id, "job_status": "queued"},
            running_id,
        ),
        {
            "sequence": 3,
            "tool": "wait_execution_jobs",
            "status": "success",
            "arguments": {"request": {"job_ids": [success_id, running_id]}},
            "result_preview": json.dumps(
                {
                    "status": "success",
                    "newly_terminal_jobs": [
                        {"job_id": success_id, "status": "success"}
                    ],
                    "running_jobs": [
                        {"job_id": running_id, "status": "running"}
                    ],
                    "queued_jobs": [],
                    "aggregation_duration_seconds": 61.5,
                    "internal_check_count": 32,
                    "state_transitions": [{"job_id": success_id}],
                }
            ),
        },
    ]

    metrics = process_metrics(events)

    assert metrics["successful_execution_job_count"] == 1
    assert metrics["execution_job_wait_call_count"] == 1
    assert metrics["execution_job_wait_seconds"] == 61.5
    assert metrics["execution_job_wait_internal_check_count"] == 32
    assert metrics["execution_job_wait_transition_count"] == 1
    assert metrics["execution_job_wait_terminal_count"] == 1
    assert metrics["successful_managed_scientific_calls"] == 1
    assert metrics["incomplete_managed_scientific_calls"] == 1


def test_managed_job_metrics_read_complete_saved_result_when_preview_is_truncated(
    tmp_path: Path,
):
    result_directory = tmp_path / "_tool_results"
    result_directory.mkdir()
    job_id = "job_full_result"
    result_path = result_directory / "0002_get_execution_job.json"
    result_path.write_text(
        json.dumps(
            {
                "status": "success",
                "result": {
                    "status": "success",
                    "job": {"job_id": job_id, "status": "failed"},
                },
            }
        ),
        encoding="utf-8",
    )
    events = [
        _job_event(
            1,
            "submit_analysis_program",
            {"status": "success", "job_id": job_id, "job_status": "queued"},
            job_id,
        ),
        {
            "sequence": 2,
            "tool": "get_execution_job",
            "status": "success",
            "arguments": {"request": {"job_id": job_id}},
            "result_preview": "{truncated",
            "result_path": "_tool_results/0002_get_execution_job.json",
        },
    ]

    metrics = process_metrics(events, workspace=tmp_path)

    assert metrics["successful_managed_scientific_calls"] == 0
    assert metrics["failed_managed_scientific_calls"] == 1
    assert metrics["incomplete_managed_scientific_calls"] == 0


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


def test_workspace_snapshot_excludes_agent_runtime_state(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "result.txt").write_text("science", encoding="utf-8")
    job_dir = tmp_path / "outputs" / "execution_jobs" / ("job_" + "a" * 32)
    job_dir.mkdir(parents=True)
    (job_dir / "scratch.tmp").write_text("transient", encoding="utf-8")
    (tmp_path / "_opencode").mkdir()
    (tmp_path / "_opencode" / "opencode.db-wal").write_text("runtime", encoding="utf-8")

    snapshot = tracing.workspace_snapshot()

    assert "outputs/result.txt" in snapshot
    assert not any(path.startswith("outputs/execution_jobs/") for path in snapshot)
    assert "_opencode/opencode.db-wal" not in snapshot
