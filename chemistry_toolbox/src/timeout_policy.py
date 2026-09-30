"""Evaluator-controlled timeout policy for managed toolbox execution.

The normal Action layer keeps its evaluator timeout.  Native software jobs have
an additional evaluator-side escape hatch for long-running, auditable jobs:
``RESEARCHCHEMBENCH_UNBOUNDED_NATIVE_SOFTWARE_IDS`` is a comma-separated set of
software ids whose supervisor walltime is deliberately disabled.  This is not
an Agent-controlled request field and does not remove CPU, memory, affinity, or
cancellation controls.
"""

from __future__ import annotations

import os
import re
from typing import Literal


ExecutionClass = Literal["compute", "fast"]

COMPUTE_ACTION_TIMEOUT_ENV = "RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS"
FAST_ACTION_TIMEOUT_ENV = "RESEARCHCHEMBENCH_FAST_ACTION_TIMEOUT_SECONDS"
UNBOUNDED_NATIVE_SOFTWARE_IDS_ENV = "RESEARCHCHEMBENCH_UNBOUNDED_NATIVE_SOFTWARE_IDS"

# Every managed toolbox Action receives a 24-hour default walltime.  The
# execution class is retained for provenance and for deployment-specific
# environment overrides, but it no longer imposes a shorter default on data
# Actions.  Gaussian may still be explicitly evaluator-configured as
# unbounded through ``UNBOUNDED_NATIVE_SOFTWARE_IDS_ENV`` below.
DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS = 86400
DEFAULT_FAST_ACTION_TIMEOUT_SECONDS = 86400


def _positive_environment_integer(name: str, default: int) -> int:
    raw = os.environ.get(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


def compute_action_timeout_seconds() -> int:
    return _positive_environment_integer(
        COMPUTE_ACTION_TIMEOUT_ENV,
        DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
    )


def fast_action_timeout_seconds() -> int:
    # Keep the historical invariant that a fast/data Action cannot outlive a
    # deployment's explicitly reduced compute budget.  With no override both
    # classes default to 86400 seconds; when only the compute policy is
    # overridden, the implicit fast default follows that lower policy instead
    # of failing validation.
    compute_timeout = compute_action_timeout_seconds()
    value = _positive_environment_integer(
        FAST_ACTION_TIMEOUT_ENV,
        min(DEFAULT_FAST_ACTION_TIMEOUT_SECONDS, compute_timeout),
    )
    if value > compute_timeout:
        raise ValueError(
            f"{FAST_ACTION_TIMEOUT_ENV} cannot exceed {COMPUTE_ACTION_TIMEOUT_ENV}"
        )
    return value


def timeout_seconds_for(execution_class: ExecutionClass) -> int:
    if execution_class == "compute":
        return compute_action_timeout_seconds()
    if execution_class == "fast":
        return fast_action_timeout_seconds()
    raise ValueError(f"Unknown execution class: {execution_class!r}")


def unbounded_native_software_ids() -> frozenset[str]:
    """Return evaluator-selected native software ids with no walltime cutoff."""

    raw = os.environ.get(UNBOUNDED_NATIVE_SOFTWARE_IDS_ENV, "")
    values = {
        item.strip().lower().replace("-", "_")
        for item in raw.split(",")
        if item.strip()
    }
    invalid = sorted(item for item in values if not re.fullmatch(r"[a-z][a-z0-9_]*", item))
    if invalid:
        raise ValueError(
            f"{UNBOUNDED_NATIVE_SOFTWARE_IDS_ENV} contains invalid software ids: {invalid}"
        )
    return frozenset(values)


def native_software_timeout_seconds(software_id: str) -> int | None:
    """Get the native-job walltime, or ``None`` for evaluator-unbounded jobs."""

    normalized = software_id.strip().lower().replace("-", "_")
    if normalized in unbounded_native_software_ids():
        return None
    return compute_action_timeout_seconds()


def native_timeout_policy_record(software_id: str) -> dict[str, object]:
    """Describe the effective native-job timeout policy in provenance."""

    timeout = native_software_timeout_seconds(software_id)
    return {
        "execution_class": "compute",
        "software_id": software_id,
        "timeout_seconds": timeout,
        "walltime_unbounded": timeout is None,
        "source": (
            "evaluation_policy_unbounded_native_software"
            if timeout is None
            else "evaluation_policy"
        ),
        "agent_controllable": False,
    }


def timeout_policy_record(execution_class: ExecutionClass) -> dict[str, object]:
    return {
        "execution_class": execution_class,
        "timeout_seconds": timeout_seconds_for(execution_class),
        "source": "evaluation_policy",
        "agent_controllable": False,
    }


__all__ = [
    "COMPUTE_ACTION_TIMEOUT_ENV",
    "DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS",
    "DEFAULT_FAST_ACTION_TIMEOUT_SECONDS",
    "ExecutionClass",
    "FAST_ACTION_TIMEOUT_ENV",
    "UNBOUNDED_NATIVE_SOFTWARE_IDS_ENV",
    "compute_action_timeout_seconds",
    "fast_action_timeout_seconds",
    "native_software_timeout_seconds",
    "native_timeout_policy_record",
    "timeout_policy_record",
    "timeout_seconds_for",
    "unbounded_native_software_ids",
]
