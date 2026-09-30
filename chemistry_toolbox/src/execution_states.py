"""Shared execution lifecycle; terminal outcomes do not imply scientific validity."""

TERMINAL_STATES = frozenset({
    "success", "partial_success", "failed", "timeout", "cancelled",
    "invalid_request", "unsupported", "unavailable",
})
QUEUED_STATES = frozenset({"accepted", "queued", "launching"})
RUNNING_STATES = frozenset({"running", "cancel_requested"})
BLOCKED_STATES = frozenset({"needs_reconciliation"})
ACTIVE_STATES = QUEUED_STATES | RUNNING_STATES
KNOWN_STATES = TERMINAL_STATES | ACTIVE_STATES | BLOCKED_STATES
RESULT_BEARING_STATES = frozenset({"success", "partial_success"})

ALLOWED_TRANSITIONS = {
    "accepted": {"queued", "needs_reconciliation", "cancelled", "timeout", "failed"},
    "queued": {"launching", "running", "needs_reconciliation", "cancel_requested", *TERMINAL_STATES},
    "launching": {"running", "needs_reconciliation", "cancel_requested", *TERMINAL_STATES},
    "running": {"needs_reconciliation", "cancel_requested", *TERMINAL_STATES},
    "cancel_requested": {"needs_reconciliation", *TERMINAL_STATES},
    "needs_reconciliation": {"running", "cancel_requested", *TERMINAL_STATES},
}


def validate_state(state: str) -> str:
    if state not in KNOWN_STATES:
        raise ValueError(f"unknown_execution_state: {state!r}")
    return state


def aggregate_outcomes(states) -> str:
    """A batch is successful only when all children are fully successful."""
    values = [validate_state(state) for state in states]
    if any(state not in TERMINAL_STATES for state in values):
        raise ValueError("cannot aggregate nonterminal execution outcomes")
    if all(state == "success" for state in values):
        return "success"
    return "partial_success" if any(state in RESULT_BEARING_STATES for state in values) else "failed"


def process_status(state: str) -> str:
    validate_state(state)
    if state in RESULT_BEARING_STATES:
        return "completed"
    return {
        "accepted": "queued", "queued": "queued", "launching": "launching",
        "running": "running", "cancel_requested": "cancel_requested",
        "needs_reconciliation": "needs_reconciliation", "timeout": "timed_out",
        "cancelled": "cancelled", "failed": "failed", "invalid_request": "not_started",
        "unsupported": "not_started", "unavailable": "not_started",
    }[state]
