import json
import subprocess
from pathlib import Path

import pytest

from researchchem_toolbox.distributed_pool import (
    DistributedResourceLimitExceeded,
    load_worker_inventory,
    pool_snapshot,
    reserve_distributed_resources,
    select_compute_cpu_ids,
)
from researchchem_toolbox import runtime


def _write_inventory(path: Path) -> None:
    workers = []
    for index in range(1, 3):
        workers.append(
            {
                "worker_id": f"compute-{index}",
                "name": f"worker-{index}",
                "execution_ssh_target": f"liyuqiang@10.0.0.{index}",
                "logical_cpus": 80,
                "physical_cores": 40,
                "memory_mb": 200000,
                "available_cpu_cores": 64,
                "available_memory_mb": 128000,
                "gpu_count": 0,
                "compute_cpu_ids": list(range(index * 100, index * 100 + 64)),
            }
        )
    path.write_text(json.dumps({"schema_version": 1, "workers": workers}))


@pytest.fixture
def distributed_environment(tmp_path: Path, monkeypatch):
    inventory = tmp_path / "inventory.json"
    _write_inventory(inventory)
    monkeypatch.setenv("RESEARCHCHEMBENCH_EXECUTION_MODE", "distributed")
    monkeypatch.setenv("RCB_DISTRIBUTED_WORKER_INVENTORY", str(inventory))
    monkeypatch.setenv("RCB_DISTRIBUTED_STATE_ROOT", str(tmp_path / "state"))
    return inventory


def test_inventory_requires_explicit_schedulable_resources(distributed_environment):
    workers = load_worker_inventory()
    assert [worker.worker_id for worker in workers] == ["compute-1", "compute-2"]
    assert all(worker.logical_cpus == 80 for worker in workers)
    assert all(worker.available_cpu_cores == 64 for worker in workers)
    assert all(worker.available_memory_mb == 128000 for worker in workers)


def test_reservations_choose_worker_with_most_remaining_capacity(
    distributed_environment,
):
    first = reserve_distributed_resources(
        {"cpu_cores": 40, "memory_mb": 40000},
        kind="test",
        label="large",
    )
    try:
        second = reserve_distributed_resources(
            {"cpu_cores": 32, "memory_mb": 32000},
            kind="test",
            label="medium",
        )
        try:
            assert first.worker.worker_id != second.worker.worker_id
            snapshot = pool_snapshot()
            assert snapshot["total_cpu_cores"] == 128
            assert snapshot["available_cpu_cores"] == 56
            assert snapshot["total_memory_mb"] == 256000
            assert snapshot["available_memory_mb"] == 184000
        finally:
            second.release()
    finally:
        first.release()
    assert pool_snapshot()["available_cpu_cores"] == 128


def test_memory_is_independent_from_cpu_ratio(distributed_environment):
    reservation = reserve_distributed_resources(
        {"cpu_cores": 1, "memory_mb": 100000},
        kind="test",
        label="memory-heavy",
    )
    try:
        assert reservation.resource_limits == {
            "cpu_cores": 1,
            "memory_mb": 100000,
            "gpu_count": 0,
        }
    finally:
        reservation.release()


def test_request_larger_than_one_worker_is_rejected(distributed_environment):
    with pytest.raises(DistributedResourceLimitExceeded) as error:
        reserve_distributed_resources(
            {"cpu_cores": 65, "memory_mb": 1000},
            kind="test",
            label="too-large",
        )
    assert error.value.as_error()["retryable"] is False


def test_compute_cpu_selection_reserves_complete_physical_cores():
    topology = []
    for node in (0, 1):
        for core in range(20):
            primary = node * 100 + core
            sibling = node * 100 + 40 + core
            for cpu in (primary, sibling):
                topology.append(
                    {
                        "cpu": cpu,
                        "core": core,
                        "socket": node,
                        "numa_node": node,
                        "siblings": [primary, sibling],
                    }
                )
    selected = select_compute_cpu_ids(topology, 64)
    assert len(selected) == 64
    assert len(set(selected)) == 64
    selected_cores = {
        (item["socket"], item["core"])
        for item in topology
        if item["cpu"] in selected
    }
    assert len(selected_cores) == 32
    assert len({core for socket, core in selected_cores if socket == 0}) == 16
    assert len({core for socket, core in selected_cores if socket == 1}) == 16


def test_remote_action_uses_ssh_and_releases_reservation(
    distributed_environment, tmp_path: Path, monkeypatch
):
    runtime_python = tmp_path / "runtime-python"
    runtime_python.touch()
    monkeypatch.setattr(runtime, "runtime_python", lambda _name: runtime_python)
    monkeypatch.setattr(
        runtime,
        "runtime_environment",
        lambda _name: {"PATH": "/usr/bin", "RESEARCHCHEM_BACKEND_RUNTIME": "test"},
    )
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(
            argv,
            0,
            stdout=json.dumps({"status": "success", "result": {"ok": True}}),
            stderr="",
        )

    monkeypatch.setattr(runtime.subprocess, "run", fake_run)
    result = runtime.invoke_worker(
        runtime="test",
        payload={
            "action_id": "test_action",
            "backend_id": "test_backend",
            "request": {
                "resource_limits": {
                    "cpu_cores": 8,
                    "memory_mb": 12000,
                    "gpu_count": 0,
                }
            },
        },
        timeout_seconds=60,
    )

    assert result["status"] == "success"
    assert result["provenance"]["execution_mode"] == "distributed"
    assert result["provenance"]["compute_worker_id"] == "compute-2"
    assert len(result["provenance"]["resource_allocation"]["cpu_ids"]) == 8
    assert calls[0][0][0] == "ssh"
    envelope = json.loads(calls[0][1]["input"])
    assert envelope["payload"]["action_id"] == "test_action"
    assert envelope["environment"]["OMP_NUM_THREADS"] == "8"
    assert not list((tmp_path / "state" / "reservations").glob("*.json"))
