"""Evaluator-controlled distributed CPU worker inventory and reservations.

The local execution path does not import or use this module unless
``RESEARCHCHEMBENCH_EXECUTION_MODE=distributed``.  Distributed reservations are
stored on the shared project filesystem so concurrent benchmark runs cannot
oversubscribe the same worker.
"""

from __future__ import annotations

import fcntl
import json
import os
import socket
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .paths import PROJECT_ROOT


EXECUTION_MODE_ENV = "RESEARCHCHEMBENCH_EXECUTION_MODE"
INVENTORY_PATH_ENV = "RCB_DISTRIBUTED_WORKER_INVENTORY"
STATE_ROOT_ENV = "RCB_DISTRIBUTED_STATE_ROOT"
LEASE_TIMEOUT_SECONDS_ENV = "RCB_DISTRIBUTED_LEASE_TIMEOUT_SECONDS"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def execution_mode() -> str:
    value = os.environ.get(EXECUTION_MODE_ENV, "local").strip().casefold()
    if value not in {"local", "distributed"}:
        raise ValueError(f"{EXECUTION_MODE_ENV} must be local or distributed")
    return value


def distributed_enabled() -> bool:
    return execution_mode() == "distributed"


def _positive_integer(value: Any, *, field: str) -> int:
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an integer") from exc
    if normalized < 1:
        raise ValueError(f"{field} must be positive")
    return normalized


def _nonnegative_integer(value: Any, *, field: str) -> int:
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an integer") from exc
    if normalized < 0:
        raise ValueError(f"{field} must be non-negative")
    return normalized


def _expand_cpu_list(value: str | list[int] | tuple[int, ...]) -> tuple[int, ...]:
    if not isinstance(value, str):
        return tuple(int(item) for item in value)
    result: list[int] = []
    for part in value.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start, end = int(start_text), int(end_text)
            if end < start:
                raise ValueError(f"invalid CPU range {token!r}")
            result.extend(range(start, end + 1))
        else:
            result.append(int(token))
    if len(result) != len(set(result)):
        raise ValueError("CPU list contains duplicates")
    return tuple(result)


def select_compute_cpu_ids(
    topology: list[dict[str, Any]], count: int
) -> list[int]:
    """Choose a NUMA-balanced complete-core compute set, primary threads first."""

    cores: dict[tuple[int, int], dict[str, Any]] = {}
    for item in topology:
        key = (int(item["socket"]), int(item["core"]))
        record = cores.setdefault(
            key,
            {
                "socket": int(item["socket"]),
                "core": int(item["core"]),
                "numa_node": int(item.get("numa_node", -1)),
                "cpus": set(),
            },
        )
        record["cpus"].update(
            int(cpu) for cpu in item.get("siblings") or [item["cpu"]]
        )
    ordered_cores = sorted(
        cores.values(),
        key=lambda item: (item["numa_node"], item["socket"], item["core"]),
    )
    if not ordered_cores:
        raise ValueError("CPU topology is empty")
    threads_per_core = min(len(item["cpus"]) for item in ordered_cores)
    if threads_per_core > 1 and count % threads_per_core == 0:
        required_cores = count // threads_per_core
        by_node: dict[int, list[dict[str, Any]]] = {}
        for item in ordered_cores:
            by_node.setdefault(int(item["numa_node"]), []).append(item)
        selected: list[dict[str, Any]] = []
        node_ids = sorted(by_node)
        while len(selected) < required_cores:
            progressed = False
            for node_id in node_ids:
                if by_node[node_id] and len(selected) < required_cores:
                    selected.append(by_node[node_id].pop(0))
                    progressed = True
            if not progressed:
                break
        if len(selected) != required_cores:
            raise ValueError("not enough complete physical cores for compute CPU set")
        per_core = [sorted(item["cpus"]) for item in selected]
        return [
            cpus[thread_index]
            for thread_index in range(threads_per_core)
            for cpus in per_core
        ]
    all_cpu_ids = [
        cpu
        for thread_index in range(max(len(item["cpus"]) for item in ordered_cores))
        for item in ordered_cores
        for cpu in [sorted(item["cpus"])[thread_index]]
        if thread_index < len(item["cpus"])
    ]
    if len(all_cpu_ids) < count:
        raise ValueError("not enough CPU ids for requested compute set")
    return all_cpu_ids[:count]


@dataclass(frozen=True)
class WorkerNode:
    worker_id: str
    name: str
    gateway_ssh_target: str
    execution_ssh_target: str
    direct_ip: str
    logical_cpus: int
    physical_cores: int
    memory_mb: int
    available_cpu_cores: int
    available_memory_mb: int
    gpu_count: int
    cpu_ids: tuple[int, ...]
    known_hosts_file: str = ""
    enabled: bool = True

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], *, index: int) -> "WorkerNode":
        worker_id = str(value.get("worker_id") or value.get("id") or f"compute-{index}")
        name = str(value.get("name") or value.get("hostname") or worker_id)
        logical_cpus = _positive_integer(
            value.get("logical_cpus"), field=f"{worker_id}.logical_cpus"
        )
        available_cpu_cores = _positive_integer(
            value.get("available_cpu_cores"),
            field=f"{worker_id}.available_cpu_cores",
        )
        memory_mb = _positive_integer(
            value.get("memory_mb"), field=f"{worker_id}.memory_mb"
        )
        available_memory_mb = _positive_integer(
            value.get("available_memory_mb"),
            field=f"{worker_id}.available_memory_mb",
        )
        cpu_ids = _expand_cpu_list(
            value.get("compute_cpu_ids")
            or value.get("cpu_ids")
            or value.get("cpu_affinity")
            or tuple(range(logical_cpus))
        )
        if available_cpu_cores > logical_cpus:
            raise ValueError(f"{worker_id} exposes more CPU than it owns")
        if available_memory_mb > memory_mb:
            raise ValueError(f"{worker_id} exposes more memory than it owns")
        if len(cpu_ids) < available_cpu_cores:
            raise ValueError(
                f"{worker_id} compute CPU list has {len(cpu_ids)} entries but "
                f"exposes {available_cpu_cores}"
            )
        return cls(
            worker_id=worker_id,
            name=name,
            gateway_ssh_target=str(value.get("gateway_ssh_target") or ""),
            execution_ssh_target=str(value.get("execution_ssh_target") or ""),
            direct_ip=str(value.get("direct_ip") or ""),
            logical_cpus=logical_cpus,
            physical_cores=_positive_integer(
                value.get("physical_cores") or logical_cpus,
                field=f"{worker_id}.physical_cores",
            ),
            memory_mb=memory_mb,
            available_cpu_cores=available_cpu_cores,
            available_memory_mb=available_memory_mb,
            gpu_count=_nonnegative_integer(
                value.get("gpu_count", 0), field=f"{worker_id}.gpu_count"
            ),
            cpu_ids=cpu_ids[:available_cpu_cores],
            known_hosts_file=str(value.get("known_hosts_file") or ""),
            enabled=bool(value.get("enabled", True)),
        )

    def public_record(self) -> dict[str, Any]:
        return {
            "worker_id": self.worker_id,
            "available_cpu_cores": self.available_cpu_cores,
            "available_memory_mb": self.available_memory_mb,
            "gpu_count": self.gpu_count,
        }


def _resolve_inventory_path() -> Path | None:
    raw = os.environ.get(INVENTORY_PATH_ENV, "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def _inventory_from_environment() -> list[dict[str, Any]]:
    count = int(os.environ.get("RCB_DISTRIBUTED_WORKER_COUNT", "0") or 0)
    values: list[dict[str, Any]] = []
    for index in range(1, count + 1):
        prefix = f"RCB_DISTRIBUTED_WORKER_{index}_"
        values.append(
            {
                "worker_id": os.environ.get(prefix + "ID", f"compute-{index}"),
                "name": os.environ.get(prefix + "NAME", f"compute-{index}"),
                "gateway_ssh_target": os.environ.get(prefix + "GATEWAY_SSH_TARGET", ""),
                "execution_ssh_target": os.environ.get(prefix + "EXECUTION_SSH_TARGET", ""),
                "direct_ip": os.environ.get(prefix + "DIRECT_IP", ""),
                "logical_cpus": os.environ.get(prefix + "LOGICAL_CPUS", "0"),
                "physical_cores": os.environ.get(prefix + "PHYSICAL_CORES", "0"),
                "memory_mb": os.environ.get(prefix + "MEMORY_MB", "0"),
                "available_cpu_cores": os.environ.get(
                    prefix + "AVAILABLE_CPU_CORES",
                    os.environ.get(prefix + "LOGICAL_CPUS", "0"),
                ),
                "available_memory_mb": os.environ.get(
                    prefix + "AVAILABLE_MEMORY_MB",
                    os.environ.get(prefix + "MEMORY_MB", "0"),
                ),
                "gpu_count": os.environ.get(prefix + "GPU_COUNT", "0"),
                "cpu_affinity": os.environ.get(prefix + "COMPUTE_CPU_IDS", "")
                or os.environ.get(prefix + "CPU_AFFINITY", ""),
                "known_hosts_file": os.environ.get(
                    "RCB_DISTRIBUTED_KNOWN_HOSTS_FILE", ""
                ),
                "enabled": os.environ.get(prefix + "ENABLED", "1").casefold()
                not in {"0", "false", "no", "off"},
            }
        )
    return values


def load_worker_inventory() -> tuple[WorkerNode, ...]:
    path = _resolve_inventory_path()
    if path is not None:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"distributed worker inventory not found: {path}") from exc
        raw_workers = payload.get("workers") if isinstance(payload, dict) else None
        if not isinstance(raw_workers, list):
            raise ValueError("distributed worker inventory must contain a workers list")
    else:
        raw_workers = _inventory_from_environment()
    workers = tuple(
        WorkerNode.from_mapping(item, index=index)
        for index, item in enumerate(raw_workers, 1)
        if bool(item.get("enabled", True))
    )
    if distributed_enabled() and not workers:
        raise ValueError("distributed execution requires at least one enabled worker")
    identifiers = [worker.worker_id for worker in workers]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("distributed worker ids must be unique")
    if any(not worker.execution_ssh_target for worker in workers):
        raise ValueError("every distributed worker requires execution_ssh_target")
    return workers


def state_root() -> Path:
    raw = os.environ.get(STATE_ROOT_ENV, "").strip()
    path = Path(raw).expanduser() if raw else PROJECT_ROOT / "workspaces" / ".distributed_compute_pool"
    path = path if path.is_absolute() else PROJECT_ROOT / path
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def _lease_timeout_seconds() -> float:
    return max(60.0, float(os.environ.get(LEASE_TIMEOUT_SECONDS_ENV, "900")))


class DistributedResourceUnavailable(RuntimeError):
    def __init__(
        self,
        requested: Mapping[str, int],
        snapshot: dict[str, Any],
        *,
        reason: str = "capacity_unavailable",
    ):
        self.requested = dict(requested)
        self.snapshot = snapshot
        self.reason = reason
        super().__init__(
            "No distributed worker currently has enough resources for "
            f"requested={self.requested}; reason={reason}"
        )

    def as_error(self) -> dict[str, Any]:
        return {
            "code": "distributed_resource_capacity_unavailable",
            "message": str(self),
            "requested": self.requested,
            "resource_snapshot": self.snapshot,
            "queue_reason": self.reason,
            "retryable": True,
        }


class DistributedResourceLimitExceeded(ValueError):
    def __init__(self, requested: Mapping[str, int], snapshot: dict[str, Any]):
        self.requested = dict(requested)
        self.snapshot = snapshot
        super().__init__(
            "Distributed resource request cannot fit on one compute worker: "
            f"requested={self.requested}"
        )

    def as_error(self) -> dict[str, Any]:
        return {
            "code": "distributed_resource_limit_exceeded",
            "message": str(self),
            "requested": self.requested,
            "maximum_cpu_cores_per_job": self.snapshot[
                "maximum_cpu_cores_per_job"
            ],
            "maximum_memory_mb_per_job": self.snapshot[
                "maximum_memory_mb_per_job"
            ],
            "single_job_cross_node_execution": False,
            "retryable": False,
        }


@dataclass
class DistributedReservation:
    path: Path
    reservation_id: str
    worker: WorkerNode
    resource_limits: dict[str, int]
    resource_allocation: dict[str, Any]
    _stop_event: threading.Event | None = None
    _heartbeat_thread: threading.Thread | None = None

    def heartbeat(self) -> None:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return
        value["heartbeat_at"] = _now()
        value["heartbeat_unix"] = time.time()
        _atomic_json(self.path, value)

    def start_heartbeat(self, *, interval_seconds: float = 30.0) -> None:
        if self._heartbeat_thread is not None:
            return
        self._stop_event = threading.Event()

        def run() -> None:
            assert self._stop_event is not None
            while not self._stop_event.wait(interval_seconds):
                self.heartbeat()

        self._heartbeat_thread = threading.Thread(
            target=run,
            name=f"distributed-reservation-{self.reservation_id[:8]}",
            daemon=True,
        )
        self._heartbeat_thread.start()

    def stop_heartbeat(self) -> None:
        if self._stop_event is not None:
            self._stop_event.set()
        if self._heartbeat_thread is not None:
            self._heartbeat_thread.join(timeout=2)
        self._stop_event = None
        self._heartbeat_thread = None

    def attach_job(self, *, job_id: str, job_status_path: str) -> None:
        """Attach a persistent job record before heartbeat ownership is transferred."""

        value = json.loads(self.path.read_text(encoding="utf-8"))
        value["job_id"] = job_id
        value["job_status_path"] = job_status_path
        value["heartbeat_at"] = _now()
        value["heartbeat_unix"] = time.time()
        _atomic_json(self.path, value)

    def release(self) -> None:
        self.stop_heartbeat()
        self.path.unlink(missing_ok=True)


@dataclass
class DistributedQueueRequest:
    path: Path
    request_id: str
    resource_limits: dict[str, int]
    _stop_event: threading.Event | None = None
    _heartbeat_thread: threading.Thread | None = None

    def heartbeat(self) -> None:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return
        value["heartbeat_at"] = _now()
        value["heartbeat_unix"] = time.time()
        _atomic_json(self.path, value)

    def start_heartbeat(self, *, interval_seconds: float = 30.0) -> None:
        if self._heartbeat_thread is not None:
            return
        self._stop_event = threading.Event()

        def run() -> None:
            assert self._stop_event is not None
            while not self._stop_event.wait(interval_seconds):
                self.heartbeat()

        self._heartbeat_thread = threading.Thread(
            target=run,
            name=f"distributed-queue-{self.request_id[:8]}",
            daemon=True,
        )
        self._heartbeat_thread.start()

    def stop_heartbeat(self) -> None:
        if self._stop_event is not None:
            self._stop_event.set()
        if self._heartbeat_thread is not None:
            self._heartbeat_thread.join(timeout=2)
        self._stop_event = None
        self._heartbeat_thread = None

    def release(self) -> None:
        self.stop_heartbeat()
        self.path.unlink(missing_ok=True)


def _reservation_directory() -> Path:
    path = state_root() / "reservations"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _queue_directory() -> Path:
    path = state_root() / "queue"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _owner_process_alive(value: Mapping[str, Any]) -> bool:
    if str(value.get("owner_host") or "") != socket.gethostname():
        return True
    try:
        os.kill(int(value.get("owner_pid") or 0), 0)
    except (OSError, TypeError, ValueError):
        return False
    return True


def _read_queue_requests(*, clean_stale: bool = True) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    deadline = time.time() - _lease_timeout_seconds()
    for path in sorted(_queue_directory().glob("request_*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError):
            continue
        terminal = False
        status_path_raw = str(value.get("job_status_path") or "")
        if status_path_raw:
            try:
                status = json.loads(Path(status_path_raw).read_text(encoding="utf-8"))
                terminal = str(status.get("status") or "") in {
                    "success",
                    "failed",
                    "timeout",
                    "cancelled",
                }
            except (OSError, json.JSONDecodeError):
                pass
        stale = float(value.get("heartbeat_unix") or 0) < deadline
        if clean_stale and (terminal or (stale and not _owner_process_alive(value))):
            path.unlink(missing_ok=True)
            continue
        value["_path"] = str(path)
        values.append(value)
    return values


def _queue_sort_key(value: Mapping[str, Any]) -> tuple[int, int, float, str]:
    resources = _normalized_request(value.get("resource_limits") or {})
    return (
        -resources["cpu_cores"],
        -resources["memory_mb"],
        float(value.get("submitted_unix") or 0),
        str(value.get("request_id") or ""),
    )


def register_distributed_request(
    resources: Mapping[str, Any],
    *,
    kind: str,
    label: str,
    workspace: str = "",
    job_id: str = "",
    job_status_path: str = "",
) -> DistributedQueueRequest:
    """Register a persistent, globally ordered native/analysis job request."""

    requested = validate_distributed_resource_limits(resources)
    request_id = uuid.uuid4().hex
    path = _queue_directory() / f"request_{request_id}.json"
    now = time.time()
    _atomic_json(
        path,
        {
            "schema_version": 1,
            "request_id": request_id,
            "kind": kind,
            "label": label,
            "workspace": workspace,
            "job_id": job_id,
            "job_status_path": job_status_path,
            "owner_host": socket.gethostname(),
            "owner_pid": os.getpid(),
            "resource_limits": requested,
            "submitted_at": _now(),
            "submitted_unix": now,
            "heartbeat_at": _now(),
            "heartbeat_unix": now,
        },
    )
    request = DistributedQueueRequest(
        path=path,
        request_id=request_id,
        resource_limits=requested,
    )
    request.start_heartbeat()
    return request


def _read_active_reservations(*, clean_stale: bool = True) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    deadline = time.time() - _lease_timeout_seconds()
    for path in sorted(_reservation_directory().glob("reservation_*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError):
            continue
        terminal = False
        status_path_raw = str(value.get("job_status_path") or "")
        if status_path_raw:
            status_path = Path(status_path_raw)
            try:
                status = json.loads(status_path.read_text(encoding="utf-8"))
                terminal = str(status.get("status") or "") in {
                    "success",
                    "failed",
                    "timeout",
                    "cancelled",
                }
            except (OSError, json.JSONDecodeError):
                pass
        stale = float(value.get("heartbeat_unix") or 0) < deadline
        owner_gone = not status_path_raw and not _owner_process_alive(value)
        if clean_stale and (
            terminal or owner_gone or (stale and not status_path_raw)
        ):
            path.unlink(missing_ok=True)
            continue
        value["_path"] = str(path)
        values.append(value)
    return values


def _normalized_request(resources: Mapping[str, Any]) -> dict[str, int]:
    return {
        "cpu_cores": _positive_integer(
            resources.get("cpu_cores", 1), field="resource_limits.cpu_cores"
        ),
        "memory_mb": _positive_integer(
            resources.get("memory_mb", 4096), field="resource_limits.memory_mb"
        ),
        "gpu_count": _nonnegative_integer(
            resources.get("gpu_count", 0), field="resource_limits.gpu_count"
        ),
    }


def _worker_usage(
    worker: WorkerNode, reservations: list[dict[str, Any]]
) -> tuple[dict[str, int], set[int]]:
    usage = {"cpu_cores": 0, "memory_mb": 0, "gpu_count": 0}
    used_cpu_ids: set[int] = set()
    for reservation in reservations:
        if reservation.get("worker_id") != worker.worker_id:
            continue
        limits = _normalized_request(reservation.get("resource_limits") or {})
        for key in usage:
            usage[key] += limits[key]
        used_cpu_ids.update(
            int(item)
            for item in (reservation.get("resource_allocation") or {}).get(
                "cpu_ids", []
            )
        )
    return usage, used_cpu_ids


def _worker_free_resources(
    worker: WorkerNode, reservations: list[dict[str, Any]]
) -> tuple[dict[str, int], list[int], int]:
    usage, used_cpu_ids = _worker_usage(worker, reservations)
    free_cpu_ids = [
        cpu_id for cpu_id in worker.cpu_ids if cpu_id not in used_cpu_ids
    ]
    return (
        {
            "cpu_cores": len(free_cpu_ids),
            "memory_mb": max(0, worker.available_memory_mb - usage["memory_mb"]),
            "gpu_count": max(0, worker.gpu_count - usage["gpu_count"]),
        },
        free_cpu_ids,
        sum(item.get("worker_id") == worker.worker_id for item in reservations),
    )


def _fits(resources: Mapping[str, int], available: Mapping[str, int]) -> bool:
    return all(
        int(resources[name]) <= int(available[name])
        for name in ("cpu_cores", "memory_mb", "gpu_count")
    )


def _draining_worker_for_request(
    request: Mapping[str, Any],
    workers: tuple[WorkerNode, ...],
    reservations: list[dict[str, Any]],
) -> str | None:
    resources = _normalized_request(request.get("resource_limits") or {})
    candidates: list[tuple[int, int, int, str]] = []
    for worker in workers:
        capacity = {
            "cpu_cores": worker.available_cpu_cores,
            "memory_mb": worker.available_memory_mb,
            "gpu_count": worker.gpu_count,
        }
        if not _fits(resources, capacity):
            continue
        available, _free_cpu_ids, active_count = _worker_free_resources(
            worker, reservations
        )
        if _fits(resources, available):
            return None
        candidates.append(
            (
                active_count,
                -available["cpu_cores"],
                -available["memory_mb"],
                worker.worker_id,
            )
        )
    return min(candidates)[-1] if candidates else None


def _queue_draining_assignments(
    requests: list[dict[str, Any]],
    workers: tuple[WorkerNode, ...],
    reservations: list[dict[str, Any]],
) -> dict[str, str]:
    assignments: dict[str, str] = {}
    claimed_workers: set[str] = set()
    for request in sorted(requests, key=_queue_sort_key):
        resources = _normalized_request(request.get("resource_limits") or {})
        if any(
            worker.worker_id not in claimed_workers
            and _fits(
                resources,
                _worker_free_resources(worker, reservations)[0],
            )
            for worker in workers
        ):
            continue
        worker_id = _draining_worker_for_request(request, workers, reservations)
        if worker_id and worker_id not in claimed_workers:
            assignments[str(request.get("request_id") or "")] = worker_id
            claimed_workers.add(worker_id)
    return assignments


def pool_snapshot(*, include_internal: bool = False) -> dict[str, Any]:
    workers = load_worker_inventory()
    reservations = _read_active_reservations()
    queue_requests = _read_queue_requests()
    draining_assignments = _queue_draining_assignments(
        queue_requests, workers, reservations
    )
    draining_workers = set(draining_assignments.values())
    records: list[dict[str, Any]] = []
    totals = {
        "total_cpu_cores": 0,
        "total_memory_mb": 0,
        "available_cpu_cores": 0,
        "available_memory_mb": 0,
        "gpu_count": 0,
        "available_gpu_count": 0,
    }
    for worker in workers:
        usage, _used_cpu_ids = _worker_usage(worker, reservations)
        available = {
            "cpu_cores": max(0, worker.available_cpu_cores - usage["cpu_cores"]),
            "memory_mb": max(0, worker.available_memory_mb - usage["memory_mb"]),
            "gpu_count": max(0, worker.gpu_count - usage["gpu_count"]),
        }
        record = {
            "worker_id": worker.worker_id,
            "capacity": {
                "cpu_cores": worker.available_cpu_cores,
                "memory_mb": worker.available_memory_mb,
                "gpu_count": worker.gpu_count,
            },
            "reserved": usage,
            "available": available,
            "active_reservation_count": sum(
                item.get("worker_id") == worker.worker_id for item in reservations
            ),
            "scheduling_state": (
                "draining" if worker.worker_id in draining_workers else "available"
            ),
        }
        if include_internal:
            record.update(
                {
                    "name": worker.name,
                    "execution_ssh_target": worker.execution_ssh_target,
                    "logical_cpus": worker.logical_cpus,
                    "physical_cores": worker.physical_cores,
                    "actual_memory_mb": worker.memory_mb,
                }
            )
        records.append(record)
        totals["total_cpu_cores"] += worker.available_cpu_cores
        totals["total_memory_mb"] += worker.available_memory_mb
        totals["available_cpu_cores"] += available["cpu_cores"]
        totals["available_memory_mb"] += available["memory_mb"]
        totals["gpu_count"] += worker.gpu_count
        totals["available_gpu_count"] += available["gpu_count"]
    return {
        "execution_mode": "distributed",
        "scheduling": "largest_cpu_first",
        "worker_count": len(workers),
        "workers": records,
        **totals,
        "maximum_cpu_cores_per_job": max(
            (worker.available_cpu_cores for worker in workers), default=0
        ),
        "maximum_memory_mb_per_job": max(
            (worker.available_memory_mb for worker in workers), default=0
        ),
        "active_reservation_count": len(reservations),
        "queued_request_count": len(queue_requests),
        "draining_worker_count": len(draining_workers),
        "physical_cpu_cores_backing_pool": sum(
            round(
                worker.available_cpu_cores
                * worker.physical_cores
                / worker.logical_cpus
            )
            for worker in workers
        ),
    }


def validate_distributed_resource_limits(
    resources: Mapping[str, Any],
) -> dict[str, int]:
    """Validate that one request fits at least one worker without crossing nodes."""

    requested = _normalized_request(resources)
    workers = load_worker_inventory()
    if not any(
        requested["cpu_cores"] <= worker.available_cpu_cores
        and requested["memory_mb"] <= worker.available_memory_mb
        and requested["gpu_count"] <= worker.gpu_count
        for worker in workers
    ):
        raise DistributedResourceLimitExceeded(
            requested, pool_snapshot(include_internal=False)
        )
    return requested


def reserve_distributed_resources(
    resources: Mapping[str, Any],
    *,
    kind: str,
    label: str,
    workspace: str = "",
    job_id: str = "",
    job_status_path: str = "",
    queue_request_id: str = "",
) -> DistributedReservation:
    requested = validate_distributed_resource_limits(resources)
    lock_path = state_root() / "pool.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            workers = load_worker_inventory()
            reservations = _read_active_reservations()
            queue_requests = sorted(_read_queue_requests(), key=_queue_sort_key)
            blocked_workers: set[str] = set()
            if queue_request_id:
                current_index = next(
                    (
                        index
                        for index, item in enumerate(queue_requests)
                        if item.get("request_id") == queue_request_id
                    ),
                    None,
                )
                if current_index is None:
                    raise DistributedResourceUnavailable(
                        requested,
                        pool_snapshot(include_internal=False),
                        reason="queue_request_missing",
                    )
                for earlier in queue_requests[:current_index]:
                    earlier_resources = _normalized_request(
                        earlier.get("resource_limits") or {}
                    )
                    if any(
                        _fits(
                            earlier_resources,
                            _worker_free_resources(worker, reservations)[0],
                        )
                        for worker in workers
                    ):
                        raise DistributedResourceUnavailable(
                            requested,
                            pool_snapshot(include_internal=False),
                            reason="waiting_for_higher_priority_request",
                        )
                    draining_worker = _draining_worker_for_request(
                        earlier, workers, reservations
                    )
                    if draining_worker:
                        blocked_workers.add(draining_worker)
            candidates: list[tuple[int, int, str, WorkerNode, list[int]]] = []
            for worker in workers:
                if worker.worker_id in blocked_workers:
                    continue
                available, free_cpu_ids, _active_count = _worker_free_resources(
                    worker, reservations
                )
                if (
                    len(free_cpu_ids) < requested["cpu_cores"]
                    or available["memory_mb"] < requested["memory_mb"]
                    or available["gpu_count"] < requested["gpu_count"]
                ):
                    continue
                candidates.append(
                    (
                        len(free_cpu_ids),
                        available["memory_mb"],
                        worker.worker_id,
                        worker,
                        free_cpu_ids,
                    )
                )
            if not candidates:
                raise DistributedResourceUnavailable(
                    requested,
                    pool_snapshot(include_internal=False),
                    reason=(
                        "waiting_for_draining_worker"
                        if blocked_workers
                        else "capacity_unavailable"
                    ),
                )
            # The Agent submits large jobs first.  For each request choose the
            # worker with the most remaining capacity to avoid blocking later
            # large jobs in the same queue.
            _free_cpu, _free_memory, _worker_id, worker, free_cpu_ids = max(
                candidates, key=lambda item: (item[0], item[1], item[2])
            )
            allocation = {
                "worker_id": worker.worker_id,
                "cpu_ids": free_cpu_ids[: requested["cpu_cores"]],
                "gpu_ids": list(range(requested["gpu_count"])),
            }
            reservation_id = uuid.uuid4().hex
            path = _reservation_directory() / f"reservation_{reservation_id}.json"
            now = time.time()
            _atomic_json(
                path,
                {
                    "schema_version": 1,
                    "reservation_id": reservation_id,
                    "worker_id": worker.worker_id,
                    "worker_name": worker.name,
                    "kind": kind,
                    "label": label,
                    "workspace": workspace,
                    "job_id": job_id,
                    "job_status_path": job_status_path,
                    "owner_host": socket.gethostname(),
                    "owner_pid": os.getpid(),
                    "resource_limits": requested,
                    "resource_allocation": allocation,
                    "created_at": _now(),
                    "heartbeat_at": _now(),
                    "heartbeat_unix": now,
                },
            )
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    reservation = DistributedReservation(
        path=path,
        reservation_id=reservation_id,
        worker=worker,
        resource_limits=requested,
        resource_allocation=allocation,
    )
    reservation.start_heartbeat()
    return reservation


__all__ = [
    "DistributedReservation",
    "DistributedQueueRequest",
    "DistributedResourceLimitExceeded",
    "DistributedResourceUnavailable",
    "EXECUTION_MODE_ENV",
    "INVENTORY_PATH_ENV",
    "WorkerNode",
    "distributed_enabled",
    "execution_mode",
    "load_worker_inventory",
    "pool_snapshot",
    "register_distributed_request",
    "reserve_distributed_resources",
    "select_compute_cpu_ids",
    "state_root",
    "validate_distributed_resource_limits",
]
