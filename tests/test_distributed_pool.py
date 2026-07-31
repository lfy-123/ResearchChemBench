import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from researchchem_toolbox.distributed_pool import (
    DistributedResourceLimitExceeded,
    DistributedResourceUnavailable,
    effective_compute_cpu_cores,
    load_worker_inventory,
    job_scheduling_snapshot,
    pool_snapshot,
    register_distributed_request,
    reserve_distributed_resources,
    select_compute_core_groups,
    select_compute_cpu_ids,
    threads_per_physical_core,
)
from researchchem_toolbox.remote_scratch import (
    cleanup_remote_scratch,
    prepare_remote_scratch,
)
from researchchem_toolbox import runtime
from researchchem_toolbox.catalog import progressive_toolbox_overview


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
                "compute_core_groups": [
                    [index * 100 + core, index * 100 + 32 + core]
                    for core in range(32)
                ],
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


def test_distributed_catalog_describes_pool_instead_of_local_aggregate_budget(
    distributed_environment,
):
    overview = progressive_toolbox_overview()
    assert "Toolbox-managed distributed compute pool" in overview
    assert "total_cpu_cores=128" in overview
    assert "maximum_cpu_cores_per_job=64" in overview
    assert "sum of concurrently active managed jobs cannot exceed" not in overview


def test_job_scheduling_snapshot_exposes_queue_and_reservations(
    distributed_environment,
) -> None:
    queued = register_distributed_request(
        {"cpu_cores": 32, "memory_mb": 32000},
        kind="analysis",
        label="queued",
        job_id="job_" + "a" * 32,
    )
    reservation = reserve_distributed_resources(
        {"cpu_cores": 16, "memory_mb": 16000},
        kind="native",
        label="running",
        job_id="job_" + "b" * 32,
    )
    try:
        snapshot = job_scheduling_snapshot()
        assert snapshot["queued_jobs"] == [
            {
                "job_id": "job_" + "a" * 32,
                "request_id": queued.request_id,
                "queue_position": 1,
                "resource_limits": {
                    "cpu_cores": 32,
                    "memory_mb": 32000,
                    "gpu_count": 0,
                },
            }
        ]
        assert snapshot["active_reservations"][0]["job_id"] == "job_" + "b" * 32
        assert snapshot["active_reservations"][0]["worker_id"] in {
            "compute-1",
            "compute-2",
        }
    finally:
        reservation.release()
        queued.release()


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


def test_orphaned_action_reservation_is_reclaimed_without_lease_delay(
    distributed_environment,
):
    reservation = reserve_distributed_resources(
        {"cpu_cores": 16, "memory_mb": 32000},
        kind="predefined_action",
        label="orphaned-action",
    )
    reservation.stop_heartbeat()
    value = json.loads(reservation.path.read_text(encoding="utf-8"))
    value["owner_pid"] = 2**31 - 1
    reservation.path.write_text(json.dumps(value), encoding="utf-8")

    snapshot = pool_snapshot()

    assert snapshot["active_reservation_count"] == 0
    assert snapshot["available_cpu_cores"] == 128
    assert not reservation.path.exists()


def test_request_larger_than_one_worker_is_rejected(distributed_environment):
    with pytest.raises(DistributedResourceLimitExceeded) as error:
        reserve_distributed_resources(
            {"cpu_cores": 65, "memory_mb": 1000},
            kind="test",
            label="too-large",
        )
    assert error.value.as_error()["retryable"] is False


def test_global_queue_prevents_small_job_from_overtaking_launchable_large_job(
    distributed_environment,
):
    large = register_distributed_request(
        {"cpu_cores": 48, "memory_mb": 48000},
        kind="analysis",
        label="large",
    )
    small = register_distributed_request(
        {"cpu_cores": 8, "memory_mb": 8000},
        kind="analysis",
        label="small",
    )
    try:
        with pytest.raises(DistributedResourceUnavailable) as error:
            reserve_distributed_resources(
                small.resource_limits,
                kind="analysis",
                label="small",
                queue_request_id=small.request_id,
            )
        assert error.value.reason == "waiting_for_higher_priority_request"
        reservation = reserve_distributed_resources(
            large.resource_limits,
            kind="analysis",
            label="large",
            queue_request_id=large.request_id,
        )
        reservation.release()
    finally:
        large.release()
        small.release()


def test_blocked_large_job_drains_one_worker_but_allows_other_workers(
    distributed_environment,
):
    first = reserve_distributed_resources(
        {"cpu_cores": 40, "memory_mb": 40000}, kind="test", label="active-1"
    )
    second = reserve_distributed_resources(
        {"cpu_cores": 40, "memory_mb": 40000}, kind="test", label="active-2"
    )
    large = register_distributed_request(
        {"cpu_cores": 64, "memory_mb": 64000},
        kind="native",
        label="waiting-large",
    )
    small = register_distributed_request(
        {"cpu_cores": 8, "memory_mb": 8000},
        kind="native",
        label="small",
    )
    try:
        snapshot = pool_snapshot()
        draining = [
            item["worker_id"]
            for item in snapshot["workers"]
            if item["scheduling_state"] == "draining"
        ]
        assert len(draining) == 1
        reservation = reserve_distributed_resources(
            small.resource_limits,
            kind="native",
            label="small",
            queue_request_id=small.request_id,
        )
        try:
            assert reservation.worker.worker_id not in draining
        finally:
            reservation.release()
    finally:
        first.release()
        second.release()
        large.release()
        small.release()


def test_compute_cpu_selection_uses_one_thread_per_physical_core():
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
    assert threads_per_physical_core(topology) == 2
    assert effective_compute_cpu_cores(topology, 64) == 32
    selected = select_compute_cpu_ids(topology, 32)
    assert len(selected) == 32
    assert len(set(selected)) == 32
    selected_cores = {
        (item["socket"], item["core"])
        for item in topology
        if item["cpu"] in selected
    }
    assert len(selected_cores) == 32
    assert len({core for socket, core in selected_cores if socket == 0}) == 16
    assert len({core for socket, core in selected_cores if socket == 1}) == 16
    groups = select_compute_core_groups(topology, 32)
    assert len(groups) == 32
    assert all(len(group) == 1 for group in groups)
    assert {cpu for group in groups for cpu in group} == set(selected)


def test_compute_cpu_capacity_is_unchanged_without_smt():
    topology = [
        {
            "cpu": cpu,
            "core": cpu,
            "socket": 0,
            "numa_node": 0,
            "siblings": [cpu],
        }
        for cpu in range(64)
    ]
    assert threads_per_physical_core(topology) == 1
    assert effective_compute_cpu_cores(topology, 64) == 64
    assert select_compute_cpu_ids(topology, 4) == [0, 1, 2, 3]


def test_smt_siblings_are_exclusive_across_reservations(
    distributed_environment,
):
    blocker = reserve_distributed_resources(
        {"cpu_cores": 64, "memory_mb": 1000}, kind="test", label="blocker"
    )
    first = reserve_distributed_resources(
        {"cpu_cores": 1, "memory_mb": 1000}, kind="test", label="odd"
    )
    second = reserve_distributed_resources(
        {"cpu_cores": 1, "memory_mb": 1000}, kind="test", label="next"
    )
    try:
        assert first.worker.worker_id == second.worker.worker_id
        first_group = set(first.resource_allocation["physical_core_groups"][0])
        assert len(first.resource_allocation["cpu_ids"]) == 1
        assert len(first.resource_allocation["blocked_sibling_cpu_ids"]) == 1
        assert first_group.isdisjoint(second.resource_allocation["cpu_ids"])
        assert first_group.isdisjoint(
            second.resource_allocation["blocked_sibling_cpu_ids"]
        )
    finally:
        first.release()
        second.release()
        blocker.release()


def test_distributed_scratch_is_unique_and_gaussian_is_job_local(tmp_path):
    root = tmp_path / "worker-scratch"
    first_environment = {
        "GAUSS_SCRDIR": "/shared/cache/gaussian/scratch",
        "RCB_DISTRIBUTED_REMOTE_SCRATCH_ROOT": str(root),
    }
    second_environment = dict(first_environment)
    first = prepare_remote_scratch(first_environment, job_token="reservation-1")
    second = prepare_remote_scratch(second_environment, job_token="reservation-2")
    try:
        assert first != second
        assert Path(first_environment["GAUSS_SCRDIR"]).parent == first
        assert Path(second_environment["GAUSS_SCRDIR"]).parent == second
        assert first_environment["TMPDIR"] == str(first)
        assert second_environment["TMPDIR"] == str(second)
        assert first_environment[
            "RESEARCHCHEM_DISTRIBUTED_SCRATCH_ISOLATION"
        ] == "worker_local_ephemeral"
    finally:
        cleanup_remote_scratch(first)
        cleanup_remote_scratch(second)
    assert not first.exists()
    assert not second.exists()


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux prctl test")
def test_parent_bound_exec_does_not_outlive_its_expected_parent(tmp_path):
    parent_program = "\n".join(
        [
            "import os, subprocess, sys, time",
            "child = subprocess.Popen([sys.executable, '-m', 'researchchem_toolbox.parent_bound_exec', str(os.getpid()), sys.executable, '-c', 'import time; time.sleep(30)'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)",
            "print(child.pid, flush=True)",
            "time.sleep(0.5)",
        ]
    )
    parent = subprocess.run(
        [sys.executable, "-c", parent_program],
        cwd=Path(__file__).parent.parent,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=True,
    )
    child_pid = int(parent.stdout.strip())
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            os.kill(child_pid, 0)
        except ProcessLookupError:
            break
        time.sleep(0.05)
    else:
        os.kill(child_pid, 9)
        pytest.fail("parent-bound command survived its expected parent")


def test_remote_action_uses_ssh_and_releases_reservation(
    distributed_environment, tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
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
    assert calls[0][0][:4] == [
        sys.executable,
        "-m",
        "researchchem_toolbox.parent_bound_exec",
        str(os.getpid()),
    ]
    assert calls[0][0][4] == "ssh"
    envelope = json.loads(calls[0][1]["input"])
    assert envelope["payload"]["action_id"] == "test_action"
    assert envelope["environment"]["OMP_NUM_THREADS"] == "8"
    assert envelope["environment"]["RESEARCHCHEMBENCH_WORKSPACE"] == str(tmp_path)
    assert envelope["distributed_reservation_id"]
    assert "RESEARCHCHEM_WORKER_RLIMIT_AS_BYTES" not in envelope["environment"]
    assert not list((tmp_path / "state" / "reservations").glob("*.json"))
