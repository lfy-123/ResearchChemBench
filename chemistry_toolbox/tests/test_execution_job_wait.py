from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from chemistry_toolbox.mcp.execution_models import JobWaitRequest
from chemistry_toolbox.mcp.open_execution import _wait_execution_jobs


class FakeClock:
    def __init__(self, on_sleep=None):
        self.value = 0.0
        self.on_sleep = on_sleep

    def monotonic(self) -> float:
        return self.value

    def time(self) -> float:
        return 1_700_000_000.0 + self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds
        if self.on_sleep:
            self.on_sleep(self.value)


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for name in ("code", "outputs", "report", "tool_logs"):
        (tmp_path / name).mkdir()
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_EXECUTION_MODE", "local")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "16")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "64000")
    return tmp_path


def _write_job(
    workspace: Path,
    suffix: str,
    status: str,
    *,
    stderr: str = "",
) -> str:
    job_id = f"job_{suffix * 32}"
    directory = workspace / "outputs" / "execution_jobs" / job_id
    directory.mkdir(parents=True)
    record = {
        "schema_version": 1,
        "job_id": job_id,
        "job_type": "native_software",
        "status": status,
        "supervisor_pid": 424242,
        "command": ["example"],
        "job_directory": f"outputs/execution_jobs/{job_id}",
        "stdout_path": f"outputs/execution_jobs/{job_id}/stdout.log",
        "stderr_path": f"outputs/execution_jobs/{job_id}/stderr.log",
        "resource_limits": {
            "cpu_cores": 4,
            "memory_mb": 8000,
            "gpu_count": 0,
            "walltime_seconds": 100,
        },
        "resource_allocation": {"cpu_ids": [0, 1, 2, 3], "gpu_ids": []},
        "submitted_at": "2023-11-14T22:13:20+00:00",
        "metadata": {"label": f"job-{suffix}", "software_id": "example"},
        "execution_mode": "local",
    }
    (directory / "status.json").write_text(json.dumps(record), encoding="utf-8")
    (directory / "request.json").write_text(
        json.dumps({**record, "staged_inputs": []}), encoding="utf-8"
    )
    (directory / "stdout.log").write_text("output\n", encoding="utf-8")
    (directory / "stderr.log").write_text(stderr, encoding="utf-8")
    return job_id


def _policy(**overrides: int) -> dict[str, int]:
    return {
        "settle_seconds": 2,
        "max_batch_seconds": 6,
        "heartbeat_seconds": 8,
        "poll_interval_seconds": 1,
        "failure_tail_chars": 40,
        **overrides,
    }


def _wait(request: JobWaitRequest, clock: FakeClock, **policy: int) -> dict:
    return _wait_execution_jobs(
        request,
        policy=_policy(**policy),
        monotonic_fn=clock.monotonic,
        sleep_fn=clock.sleep,
        unix_time_fn=clock.time,
    )


def test_partial_terminal_return_keeps_other_job_running(workspace: Path) -> None:
    success = _write_job(workspace, "a", "success")
    running = _write_job(workspace, "b", "running")

    result = _wait(JobWaitRequest(job_ids=[success, running]), FakeClock())

    assert result["return_reason"] == "settled_state_update"
    assert [item["job_id"] for item in result["newly_terminal_jobs"]] == [success]
    assert [item["job_id"] for item in result["running_jobs"]] == [running]
    assert result["remaining_job_ids"] == [running]
    assert result["resource_snapshot_stable"] is True
    assert (workspace / "outputs/execution_jobs" / success / "collection.json").is_file()
    running_status = json.loads(
        (workspace / "outputs/execution_jobs" / running / "status.json").read_text()
    )
    assert running_status["status"] == "running"
    assert running_status["supervisor_pid"] == 424242


def test_failure_is_collected_with_bounded_tail(workspace: Path) -> None:
    failed = _write_job(workspace, "c", "failed", stderr="x" * 100)

    result = _wait(JobWaitRequest(job_ids=[failed]), FakeClock())

    terminal = result["newly_terminal_jobs"][0]
    assert result["return_reason"] == "all_terminal"
    assert terminal["status"] == "failed"
    assert terminal["stderr_tail"] == "x" * 40
    assert terminal["collection_manifest"].endswith("collection.json")


def test_log_growth_does_not_reset_settle_window(workspace: Path) -> None:
    success = _write_job(workspace, "d", "success")
    running = _write_job(workspace, "e", "running")
    stdout = workspace / "outputs/execution_jobs" / running / "stdout.log"
    clock = FakeClock(lambda _: stdout.write_text(stdout.read_text() + "tick\n"))

    result = _wait(JobWaitRequest(job_ids=[success, running]), clock)

    assert result["return_reason"] == "settled_state_update"
    assert result["settled_for_seconds"] == 2


def test_state_changes_are_capped_by_aggregation_limit(workspace: Path) -> None:
    success = _write_job(workspace, "f", "success")
    running = _write_job(workspace, "1", "running")
    status_path = workspace / "outputs/execution_jobs" / running / "status.json"

    def mutate(value: float) -> None:
        status = json.loads(status_path.read_text())
        status["queue_reason"] = f"change-{value}"
        status_path.write_text(json.dumps(status), encoding="utf-8")

    result = _wait(
        JobWaitRequest(job_ids=[success, running]),
        FakeClock(mutate),
        settle_seconds=10,
        max_batch_seconds=3,
        heartbeat_seconds=20,
    )

    assert result["return_reason"] == "aggregation_time_cap"
    assert result["aggregation_duration_seconds"] == 3


def test_no_terminal_event_returns_heartbeat(workspace: Path) -> None:
    running = _write_job(workspace, "2", "running")

    result = _wait(
        JobWaitRequest(job_ids=[running]),
        FakeClock(),
        settle_seconds=1,
        max_batch_seconds=2,
        heartbeat_seconds=3,
    )

    assert result["return_reason"] == "heartbeat"
    assert result["newly_terminal_jobs"] == []
    assert result["remaining_job_ids"] == [running]


def test_wait_request_rejects_duplicate_and_invalid_ids() -> None:
    job_id = "job_" + "a" * 32
    with pytest.raises(ValidationError):
        JobWaitRequest(job_ids=[job_id, job_id])
    with pytest.raises(ValidationError):
        JobWaitRequest(job_ids=["outside-workspace"])
