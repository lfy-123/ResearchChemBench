"""Parsing and validation for batch evaluation launch specifications."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..repository import list_tasks
from ..settings import AGENT_PRESETS


class EvalConfigError(ValueError):
    """Raised for invalid batch evaluation configuration."""


@dataclass(frozen=True)
class RunSpec:
    paper_id: str
    task_type: str
    agent_key: str
    repeat: int


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError as exc:
        raise EvalConfigError(f"Config not found: {path}") from exc
    if not isinstance(value, dict):
        raise EvalConfigError("Evaluation config must be a YAML mapping")
    return value


def _normalize_list(value: Any, *, name: str) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise EvalConfigError(f"{name} must be a string or list of strings")


def resolve_specs(config: dict[str, Any]) -> list[RunSpec]:
    agents = _normalize_list(config.get("agents", ["mock"]), name="agents")
    for agent in agents:
        if agent not in AGENT_PRESETS:
            raise EvalConfigError(
                f"Unknown agent {agent!r}; valid: {sorted(AGENT_PRESETS)}"
            )

    raw_tasks = config.get("tasks", "all")
    if raw_tasks == "all":
        tasks = [
            {"paper_id": row["paper_id"], "task_type": row["task_type"]}
            for row in list_tasks()
        ]
    elif isinstance(raw_tasks, list) and all(
        isinstance(item, dict)
        and isinstance(item.get("paper_id"), str)
        and isinstance(item.get("task_type"), str)
        for item in raw_tasks
    ):
        tasks = raw_tasks
    else:
        raise EvalConfigError("tasks must be 'all' or a list of paper_id/task_type mappings")
    known_tasks = {(row["task_type"], row["paper_id"]) for row in list_tasks()}
    unknown = [
        task for task in tasks
        if (task["task_type"], task["paper_id"]) not in known_tasks
    ]
    if unknown:
        raise EvalConfigError(f"Unknown tasks: {unknown}")

    repeats = int(config.get("repeats", 1))
    if repeats < 1:
        raise EvalConfigError("repeats must be >= 1")
    return [
        RunSpec(task["paper_id"], task["task_type"], agent, repeat)
        for task in tasks
        for agent in agents
        for repeat in range(1, repeats + 1)
    ]
