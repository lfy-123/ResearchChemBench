"""Small persistent controller policy, separate from frozen scientific configuration."""
import math
import random
import uuid
from datetime import datetime, timezone

DEFAULT_POLICY = {"max_attempts": 8, "max_wait_seconds": 3600,
                  "initial_delay_seconds": 60, "max_delay_seconds": 600}


def add_resume_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--resume", dest="resume_enabled", action="store_true", default=None,
                       help="Enable bounded recovery of the original session, including one plaintext-history fallback if Codex rejects encrypted reasoning.")
    group.add_argument("--no-resume", dest="resume_enabled", action="store_false",
                       help="Save checkpoints but stop after an infrastructure failure.")


def validate_policy(value=None):
    if value is not None and (not isinstance(value, dict) or set(value) - set(DEFAULT_POLICY)):
        raise ValueError("invalid resume_policy keys")
    policy = {**DEFAULT_POLICY, **(value or {})}
    for key, number in policy.items():
        if isinstance(number, bool) or not isinstance(number, (int, float)) or not math.isfinite(number) or number <= 0:
            raise ValueError("resume_policy requires positive finite values: " + key)
    if not isinstance(policy["max_attempts"], int) or policy["max_delay_seconds"] < policy["initial_delay_seconds"]:
        raise ValueError("invalid resume_policy attempt count or delay range")
    return policy


def configure(store, enabled=None, policy=None):
    old = store.get_record("resume", "policy", {})
    value = {"enabled": old.get("enabled", False) if enabled is None else enabled,
             "limits": validate_policy(policy if policy is not None else old.get("limits"))}
    if not isinstance(value["enabled"], bool):
        raise ValueError("resume must be a boolean")
    if old != value:
        store.put_record("resume_policy_change", uuid.uuid4().hex,
                         {"at": datetime.now(timezone.utc).isoformat(), "before": old, "after": value})
        store.put_record("resume", "policy", value)
    return value


def retry_delay(error, policy, state):
    if not policy["enabled"]:
        return None, "automatic_resume_disabled"
    if not error or not error.get("retryable"):
        return None, "failure_not_retryable"
    limits = policy["limits"]
    count = state.get("automatic_attempts", 0)
    if count >= limits["max_attempts"]:
        return None, "automatic_attempt_limit"
    base = min(limits["max_delay_seconds"], limits["initial_delay_seconds"] * 2 ** min(count, 30))
    delay = min(limits["max_delay_seconds"], base * random.uniform(1, 1.1))
    delay = max(delay, error.get("retry_after_seconds", 0))
    if not math.isfinite(delay) or state.get("wait_budget_used_seconds", 0) + delay > limits["max_wait_seconds"]:
        return None, "automatic_wait_limit"
    return delay, None


def execution_exit_code(status, evaluation_status=None):
    if status in {"preflight_failed", "recovery_blocked"}:
        return 2
    if status in {"suspended_infrastructure"}:
        return 3
    if status != "completed":
        return 1
    if evaluation_status and evaluation_status not in {"scored", "disabled", "not_started"}:
        return 4
    return 0
