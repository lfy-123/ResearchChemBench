"""Parsing and validation for batch evaluation launch specifications."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..repository import TaskRepository, list_tasks
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
        content = path.read_text(encoding="utf-8")
        value = yaml.safe_load(content) or {}
    except FileNotFoundError as exc:
        raise EvalConfigError(f"Config not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise EvalConfigError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvalConfigError("Evaluation config must be a YAML mapping")
    if "agent_definitions" in value:
        # SafeLoader otherwise silently overwrites duplicate registrations.
        # Keep legacy YAML semantics for configs without external definitions.
        root = yaml.compose(content)
        definitions = [node for key, node in root.value if key.value == "agent_definitions"]
        if len(definitions) != 1:
            raise EvalConfigError("Duplicate agent_definitions mapping")
        node = definitions[0]
        if isinstance(node, yaml.MappingNode):
            names = [key.value for key, _ in node.value]
            if len(names) != len(set(names)):
                raise EvalConfigError("Duplicate agent registration in agent_definitions")
    return value


def _normalize_list(value: Any, *, name: str) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise EvalConfigError(f"{name} must be a string or list of strings")


def resolve_task_repository(config: dict[str, Any], *, config_dir: Path) -> TaskRepository | None:
    """Explicit final-package selection without changing canonical discovery."""
    source = config.get("task_source")
    if source is None:
        return None
    if not isinstance(source, dict) or source.get("kind") != "final_verified" or set(source) != {"kind", "root"}:
        raise EvalConfigError("task_source requires kind=final_verified and root")
    root = source["root"]
    tasks = config.get("tasks")
    if not isinstance(root, str) or not root.strip():
        raise EvalConfigError("task_source.root must be a path")
    if not isinstance(tasks, list) or not tasks or any(
        not isinstance(t, dict) or not isinstance(t.get("paper_id"), str) or not isinstance(t.get("task_type"), str)
        for t in tasks
    ):
        raise EvalConfigError("final_verified requires an explicit nonempty tasks list; tasks: all is not allowed")
    return TaskRepository.from_final(config_dir / Path(root).expanduser(),
                                     approved_tasks=[(t["task_type"], t["paper_id"]) for t in tasks])


def resolve_specs(config: dict[str, Any], *, agent_registry=None, task_repository=None) -> list[RunSpec]:
    registry = AGENT_PRESETS if agent_registry is None else agent_registry
    agents = _normalize_list(config.get("agents", ["mock"]), name="agents")
    for agent in agents:
        if agent not in registry:
            raise EvalConfigError(
                f"Unknown agent {agent!r}; valid: {sorted(registry)}"
            )

    rows = list_tasks() if task_repository is None else list_tasks(repository=task_repository)
    raw_tasks = config.get("tasks", "all")
    if raw_tasks == "all":
        tasks = [
            {"paper_id": row["paper_id"], "task_type": row["task_type"]}
            for row in rows
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
    known_tasks = {(row["task_type"], row["paper_id"]) for row in rows}
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
