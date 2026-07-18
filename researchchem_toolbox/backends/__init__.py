"""Backend-local action execution entry point."""

from __future__ import annotations

from typing import Any


def execute_local(
    action_id: str,
    backend_id: str,
    request: dict[str, Any],
) -> dict[str, Any]:
    from . import data, docking, dynamics, electronic, periodic, reaction, structure

    for module in (structure, electronic, reaction, dynamics, periodic, docking, data):
        if action_id in module.ACTIONS:
            return module.execute(action_id, backend_id, request)
    return {
        "status": "unsupported",
        "error": {
            "code": "handler_missing",
            "message": f"No local handler is registered for action {action_id}",
        },
        "retryable": False,
    }
