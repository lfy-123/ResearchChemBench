from __future__ import annotations

from typing import Any


def runtime_tier(walltime_hours: float | int | None) -> str:
    if walltime_hours is None:
        return "unknown"
    hours = float(walltime_hours)
    if hours < 0:
        raise ValueError("walltime_hours must be non-negative")
    if hours <= 1:
        return "short"
    if hours <= 4:
        return "medium"
    return "long_challenge"


def normalize_runtime(runtime: dict[str, Any] | None) -> dict[str, Any]:
    output = dict(runtime or {})
    measured = output.get("measured_walltime_hours")
    estimated = output.get("estimated_walltime_hours")
    basis = measured if measured is not None else estimated
    output["runtime_tier"] = runtime_tier(basis)
    output["runtime_tier_basis"] = (
        "measured" if measured is not None else "estimated" if estimated is not None else "unknown"
    )
    cores = output.get("cpu_cores")
    if measured is not None and cores is not None:
        output["cpu_core_hours"] = round(float(measured) * float(cores), 3)
    return output
