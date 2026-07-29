"""Evaluator-controlled per-task compute resource budgets and reservations."""

from __future__ import annotations

import fcntl
import json
import os
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping


AVAILABLE_CPU_CORES_ENV = "RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES"
AVAILABLE_MEMORY_MB_ENV = "RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB"
AVAILABLE_GPU_COUNT_ENV = "RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT"

DEFAULT_AVAILABLE_CPU_CORES = 48
DEFAULT_AVAILABLE_MEMORY_MB = 204_800
DEFAULT_AVAILABLE_GPU_COUNT = 0

DEFAULT_REQUEST_CPU_CORES = 1
DEFAULT_REQUEST_MEMORY_MB = 4096
DEFAULT_REQUEST_GPU_COUNT = 0

ACTIVE_JOB_STATES = {"queued", "running"}


def _environment_integer(name: str, default: int, *, minimum: int) -> int:
    raw = os.environ.get(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < minimum:
        qualifier = "non-negative" if minimum == 0 else f">= {minimum}"
        raise ValueError(f"{name} must be {qualifier}")
    return value


@dataclass(frozen=True)
class ResourceBudget:
    cpu_cores: int
    memory_mb: int
    gpu_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "cpu_cores": self.cpu_cores,
            "memory_mb": self.memory_mb,
            "gpu_count": self.gpu_count,
            "source": "evaluation_policy",
            "agent_controllable": False,
            "scope": "per_task",
        }


class ResourceBudgetExceeded(ValueError):
    """Structured rejection when one request exceeds a task resource budget."""

    def __init__(
        self,
        *,
        requested: Mapping[str, int],
        budget: ResourceBudget,
        reserved: Mapping[str, int] | None = None,
        aggregate: bool = False,
    ) -> None:
        self.requested = dict(requested)
        self.budget = budget
        self.reserved = dict(reserved or _zero_resources())
        self.aggregate = aggregate
        available = {
            name: max(0, int(getattr(budget, name)) - int(self.reserved.get(name, 0)))
            for name in ("cpu_cores", "memory_mb", "gpu_count")
        }
        scope = "aggregate active-job" if aggregate else "single-request"
        super().__init__(
            f"Requested resources exceed the evaluator-controlled {scope} budget: "
            f"requested={self.requested}, reserved={self.reserved}, "
            f"available={available}, budget={budget.as_dict()}"
        )

    def as_error(self) -> dict[str, Any]:
        available = {
            name: max(
                0,
                int(getattr(self.budget, name)) - int(self.reserved.get(name, 0)),
            )
            for name in ("cpu_cores", "memory_mb", "gpu_count")
        }
        return {
            "code": (
                "aggregate_resource_budget_exceeded"
                if self.aggregate
                else "resource_budget_exceeded"
            ),
            "message": str(self),
            "requested": self.requested,
            "currently_reserved": self.reserved,
            "available": available,
            "budget": self.budget.as_dict(),
            "retryable": self.aggregate,
        }


def evaluation_resource_budget() -> ResourceBudget:
    return ResourceBudget(
        cpu_cores=_environment_integer(
            AVAILABLE_CPU_CORES_ENV,
            DEFAULT_AVAILABLE_CPU_CORES,
            minimum=1,
        ),
        memory_mb=_environment_integer(
            AVAILABLE_MEMORY_MB_ENV,
            DEFAULT_AVAILABLE_MEMORY_MB,
            minimum=128,
        ),
        gpu_count=_environment_integer(
            AVAILABLE_GPU_COUNT_ENV,
            DEFAULT_AVAILABLE_GPU_COUNT,
            minimum=0,
        ),
    )


def resource_budget_record() -> dict[str, Any]:
    return evaluation_resource_budget().as_dict()


def normalize_resource_limits(value: Any) -> dict[str, int]:
    if hasattr(value, "model_dump"):
        supplied = value.model_dump(mode="json")
    else:
        supplied = dict(value or {})
    return {
        "cpu_cores": int(supplied.get("cpu_cores") or DEFAULT_REQUEST_CPU_CORES),
        "memory_mb": int(supplied.get("memory_mb") or DEFAULT_REQUEST_MEMORY_MB),
        "gpu_count": int(
            DEFAULT_REQUEST_GPU_COUNT
            if supplied.get("gpu_count") is None
            else supplied["gpu_count"]
        ),
    }


def validate_resource_limits(
    resources: Mapping[str, int],
    *,
    budget: ResourceBudget | None = None,
) -> None:
    selected = budget or evaluation_resource_budget()
    requested = normalize_resource_limits(resources)
    if any(
        requested[name] > int(getattr(selected, name))
        for name in ("cpu_cores", "memory_mb", "gpu_count")
    ):
        raise ResourceBudgetExceeded(requested=requested, budget=selected)


def _workspace_root() -> Path:
    raw = (
        os.environ.get("RESEARCHCHEM_MCP_WORKSPACE", "").strip()
        or os.environ.get("RESEARCHCHEMBENCH_WORKSPACE", "").strip()
    )
    if not raw:
        raise RuntimeError(
            "RESEARCHCHEM_MCP_WORKSPACE or RESEARCHCHEMBENCH_WORKSPACE is required "
            "for resource reservations"
        )
    return Path(raw).expanduser().resolve()


def _budget_directory() -> Path:
    path = _workspace_root() / "outputs" / ".resource_budget"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _zero_resources() -> dict[str, int]:
    return {"cpu_cores": 0, "memory_mb": 0, "gpu_count": 0}


def _add_resources(total: dict[str, int], resources: Mapping[str, Any]) -> None:
    normalized = normalize_resource_limits(resources)
    for name in total:
        total[name] += normalized[name]


def _process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except (OSError, ValueError):
        return False
    return True


def active_resource_usage() -> dict[str, int]:
    root = _workspace_root()
    total = _zero_resources()
    jobs = root / "outputs" / "execution_jobs"
    if jobs.is_dir():
        for path in jobs.glob("job_*/status.json"):
            try:
                status = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, TypeError):
                continue
            if str(status.get("status", "")).casefold() in ACTIVE_JOB_STATES:
                _add_resources(total, status.get("resource_limits") or {})
    reservations = _budget_directory() / "reservations"
    if reservations.is_dir():
        for path in reservations.glob("*.json"):
            try:
                reservation = json.loads(path.read_text(encoding="utf-8"))
                pid = int(reservation.get("pid") or 0)
            except (OSError, json.JSONDecodeError, TypeError, ValueError):
                continue
            if pid > 0 and _process_exists(pid):
                _add_resources(total, reservation.get("resource_limits") or {})
            else:
                path.unlink(missing_ok=True)
    return total


def active_resource_jobs() -> list[dict[str, Any]]:
    """Return the active jobs and transient reservations consuming the task budget."""

    root = _workspace_root()
    records: list[dict[str, Any]] = []
    jobs = root / "outputs" / "execution_jobs"
    if jobs.is_dir():
        for path in sorted(jobs.glob("job_*/status.json")):
            try:
                status = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, TypeError):
                continue
            state = str(status.get("status", "")).casefold()
            if state not in ACTIVE_JOB_STATES:
                continue
            records.append(
                {
                    "record_type": "execution_job",
                    "job_id": status.get("job_id") or path.parent.name,
                    "job_type": status.get("job_type"),
                    "status": state,
                    "label": (status.get("metadata") or {}).get("label"),
                    "resource_limits": normalize_resource_limits(
                        status.get("resource_limits") or {}
                    ),
                    "submitted_at": status.get("submitted_at"),
                    "supervisor_pid": status.get("supervisor_pid"),
                    "release_condition": "job reaches success, failed, timeout, or cancelled",
                }
            )
    reservations = _budget_directory() / "reservations"
    if reservations.is_dir():
        for path in sorted(reservations.glob("*.json")):
            try:
                reservation = json.loads(path.read_text(encoding="utf-8"))
                pid = int(reservation.get("pid") or 0)
            except (OSError, json.JSONDecodeError, TypeError, ValueError):
                continue
            if pid <= 0 or not _process_exists(pid):
                path.unlink(missing_ok=True)
                continue
            records.append(
                {
                    "record_type": "submission_reservation",
                    "reservation_id": path.stem,
                    "pid": pid,
                    "job_type": reservation.get("kind"),
                    "label": reservation.get("label"),
                    "resource_limits": normalize_resource_limits(
                        reservation.get("resource_limits") or {}
                    ),
                    "release_condition": "the in-progress submission creates its job record or fails",
                }
            )
    return records


@contextmanager
def _budget_lock() -> Iterator[None]:
    lock_path = _budget_directory() / "quota.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@dataclass
class ResourceReservation:
    path: Path
    resource_limits: dict[str, int]

    def release(self) -> None:
        self.path.unlink(missing_ok=True)


def reserve_resources(
    resources: Mapping[str, Any],
    *,
    kind: str,
    label: str,
) -> ResourceReservation:
    requested = normalize_resource_limits(resources)
    budget = evaluation_resource_budget()
    validate_resource_limits(requested, budget=budget)
    with _budget_lock():
        reserved = active_resource_usage()
        if any(
            reserved[name] + requested[name] > int(getattr(budget, name))
            for name in requested
        ):
            raise ResourceBudgetExceeded(
                requested=requested,
                budget=budget,
                reserved=reserved,
                aggregate=True,
            )
        directory = _budget_directory() / "reservations"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"reservation_{uuid.uuid4().hex}.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "pid": os.getpid(),
                    "kind": kind,
                    "label": label,
                    "resource_limits": requested,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
    return ResourceReservation(path=path, resource_limits=requested)


__all__ = [
    "AVAILABLE_CPU_CORES_ENV",
    "AVAILABLE_GPU_COUNT_ENV",
    "AVAILABLE_MEMORY_MB_ENV",
    "DEFAULT_AVAILABLE_CPU_CORES",
    "DEFAULT_AVAILABLE_GPU_COUNT",
    "DEFAULT_AVAILABLE_MEMORY_MB",
    "DEFAULT_REQUEST_CPU_CORES",
    "DEFAULT_REQUEST_GPU_COUNT",
    "DEFAULT_REQUEST_MEMORY_MB",
    "ResourceBudget",
    "ResourceBudgetExceeded",
    "ResourceReservation",
    "active_resource_usage",
    "active_resource_jobs",
    "evaluation_resource_budget",
    "normalize_resource_limits",
    "reserve_resources",
    "resource_budget_record",
    "validate_resource_limits",
]
