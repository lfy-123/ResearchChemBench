"""Evaluator-controlled settings shared by asynchronous supervision tools."""

from __future__ import annotations

import os


ENVIRONMENT_NAMES = {
    "settle_seconds": "RESEARCHCHEMBENCH_JOB_EVENT_SETTLE_SECONDS",
    "max_batch_seconds": "RESEARCHCHEMBENCH_JOB_EVENT_MAX_BATCH_SECONDS",
    "heartbeat_seconds": "RESEARCHCHEMBENCH_JOB_WAIT_HEARTBEAT_SECONDS",
    "poll_interval_seconds": "RESEARCHCHEMBENCH_JOB_INTERNAL_POLL_INTERVAL_SECONDS",
    "failure_tail_chars": "RESEARCHCHEMBENCH_JOB_FAILURE_TAIL_CHARS",
}
DEFAULTS = {
    "settle_seconds": 60,
    "max_batch_seconds": 300,
    "heartbeat_seconds": 3600,
    "poll_interval_seconds": 2,
    "failure_tail_chars": 2000,
}


def supervision_policy() -> dict[str, int]:
    policy: dict[str, int] = {}
    for key, environment_name in ENVIRONMENT_NAMES.items():
        raw = os.environ.get(environment_name, str(DEFAULTS[key]))
        try:
            value = int(raw)
        except ValueError as exc:
            raise ValueError(f"{environment_name} must be an integer") from exc
        if value < 1:
            raise ValueError(f"{environment_name} must be positive")
        policy[key] = value
    if policy["max_batch_seconds"] < policy["settle_seconds"]:
        raise ValueError(
            f"{ENVIRONMENT_NAMES['max_batch_seconds']} must be >= "
            f"{ENVIRONMENT_NAMES['settle_seconds']}"
        )
    if policy["heartbeat_seconds"] < policy["max_batch_seconds"]:
        raise ValueError(
            f"{ENVIRONMENT_NAMES['heartbeat_seconds']} must be >= "
            f"{ENVIRONMENT_NAMES['max_batch_seconds']}"
        )
    return policy


__all__ = ["DEFAULTS", "ENVIRONMENT_NAMES", "supervision_policy"]
