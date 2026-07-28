from __future__ import annotations

from pathlib import Path

import pytest

from researchchem_toolbox import service
from researchchem_toolbox.resource_budget import (
    ResourceBudgetExceeded,
    reserve_resources,
    resource_budget_record,
    validate_resource_limits,
)
from chemistry_toolbox.mcp.job_supervisor import _memory_limit_mb, _preexec


H2 = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.74]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}


@pytest.fixture
def budget_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "8")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "8192")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT", "1")
    return tmp_path


def test_budget_is_operator_controlled_and_validates_single_requests(
    budget_workspace: Path,
):
    assert resource_budget_record() == {
        "cpu_cores": 8,
        "memory_mb": 8192,
        "gpu_count": 1,
        "source": "evaluation_policy",
        "agent_controllable": False,
        "scope": "per_task",
    }
    validate_resource_limits({"cpu_cores": 8, "memory_mb": 8192, "gpu_count": 1})
    with pytest.raises(ResourceBudgetExceeded) as raised:
        validate_resource_limits(
            {"cpu_cores": 9, "memory_mb": 8192, "gpu_count": 1}
        )
    assert raised.value.as_error()["code"] == "resource_budget_exceeded"


def test_concurrent_reservations_cannot_exceed_the_task_budget(
    budget_workspace: Path,
):
    first = reserve_resources(
        {"cpu_cores": 6, "memory_mb": 6000, "gpu_count": 0},
        kind="test",
        label="first",
    )
    try:
        with pytest.raises(ResourceBudgetExceeded) as raised:
            reserve_resources(
                {"cpu_cores": 3, "memory_mb": 2500, "gpu_count": 0},
                kind="test",
                label="second",
            )
        error = raised.value.as_error()
        assert error["code"] == "aggregate_resource_budget_exceeded"
        assert error["currently_reserved"]["cpu_cores"] == 6
        assert error["retryable"] is True
    finally:
        first.release()


def test_action_rejects_resources_above_budget_before_backend_execution(
    budget_workspace: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda specifications: {
            item.id: {"available": True, "status": "available", "runtime": item.runtime}
            for item in specifications
        },
    )
    worker_called = False

    def fake_worker(**_kwargs):
        nonlocal worker_called
        worker_called = True
        return {"status": "success", "result": {}}

    monkeypatch.setattr(service, "invoke_worker", fake_worker)
    result = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "xtb",
            "inputs": {"structure": H2},
            "method_spec": {"method": "gfn2"},
            "resource_limits": {
                "cpu_cores": 9,
                "memory_mb": 4096,
                "gpu_count": 0,
            },
        },
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "resource_budget_exceeded"
    assert worker_called is False


def test_supervisor_enforces_job_memory_without_process_cpu_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delattr("os.sched_getaffinity", raising=False)

    _preexec(
        {"memory_mb": 512, "cpu_cores": 8, "walltime_seconds": 30},
        {"memory_mb": 4096},
    )()

    assert _memory_limit_mb(
        {"memory_mb": 512}, {"memory_mb": 4096}
    ) == 512
