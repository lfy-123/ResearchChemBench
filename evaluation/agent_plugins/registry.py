"""Configuration-local definitions; built-in presets are never mutated."""

from __future__ import annotations

import copy
import json
import os
import re
from pathlib import Path

from ..settings import AGENT_PRESETS


class AgentConfigError(ValueError):
    pass


def sensitive_name(name: str) -> bool:
    return bool(re.search(r"(?:api[_-]?key|password|secret|credential|authorization|(?:access|refresh|auth)[_-]?token)", name, re.I))


def evaluator_environment(name: str) -> bool:
    return any(word in name.upper() for word in ("JUDGE", "SCORER", "EVALUATOR"))


def private_environment(name: str) -> bool:
    upper = name.upper()
    return (evaluator_environment(name)
            or upper.startswith(("RESEARCHCHEMBENCH_", "RESEARCHCHEM_", "GIT_", "RCB_DISTRIBUTED_"))
            or upper in {"PYTHONPATH", "PYTHONHOME", "HOME", "PATH", "LD_PRELOAD", "BASH_ENV", "ENV"})


def _public_options(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str) or sensitive_name(key):
                raise AgentConfigError("Agent options must have public string keys; pass credentials through env_allowlist")
            _public_options(child)
    elif isinstance(value, list):
        for child in value:
            _public_options(child)


def validate_external_definition(key, definition, *, config_dir: Path) -> dict:
    if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", key):
        raise AgentConfigError("Agent names must be safe identifiers of at most 64 characters")
    if key in AGENT_PRESETS:
        raise AgentConfigError(f"Cannot override built-in agent {key!r}")
    if not isinstance(definition, dict):
        raise AgentConfigError(f"Agent {key!r} must be a mapping")
    unknown = set(definition) - {"kind", "label", "command", "env_allowlist", "options", "execution_backend", "model_budget_enforcement"}
    if unknown:
        raise AgentConfigError(f"Unknown agent definition fields: {sorted(unknown, key=str)}")
    if definition.get("kind", "external") != "external":
        raise AgentConfigError("Custom definitions must use kind=external")
    command = definition.get("command")
    if not isinstance(command, list) or not command or any(not isinstance(v, str) or not v or "\x00" in v for v in command):
        raise AgentConfigError("command must be a nonempty argv array, never a shell string")
    if any(v == "--request" or v.startswith("--request=") for v in command):
        raise AgentConfigError("The runner appends --request; do not configure it manually")
    command = list(command)
    if "/" in command[0]:
        executable = Path(command[0]).expanduser()
        command[0] = os.path.abspath(config_dir / executable)
    allowed = definition.get("env_allowlist", [])
    if not isinstance(allowed, list) or any(not isinstance(v, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", v) for v in allowed):
        raise AgentConfigError("env_allowlist must be a list of environment variable names")
    if any(private_environment(v) for v in allowed):
        raise AgentConfigError("env_allowlist cannot expose evaluator credentials or override runner-controlled environment")
    options = definition.get("options", {})
    if not isinstance(options, dict):
        raise AgentConfigError("options must be a JSON object")
    _public_options(options)
    try:
        json.dumps(options, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise AgentConfigError("options must contain finite JSON values") from exc
    backend = definition.get("execution_backend", "benchmark")
    if backend != "benchmark":
        raise AgentConfigError(f"Unregistered execution backend: {backend!r}")
    enforcement = definition.get("model_budget_enforcement", "agent_cooperative")
    if enforcement != "agent_cooperative":
        raise AgentConfigError("External model hard budgets require a trusted model gateway; only agent_cooperative is supported")
    label = definition.get("label", key)
    if not isinstance(label, str) or not label.strip():
        raise AgentConfigError("label must be a nonempty string")
    return {"kind": "external", "label": label, "command": command,
            "env_allowlist": list(dict.fromkeys(allowed)), "options": copy.deepcopy(options),
            "execution_backend": backend, "model_budget_enforcement": enforcement}


def resolve_agent_definitions(config, *, config_dir: Path) -> dict:
    definitions = config.get("agent_definitions", {})
    if not isinstance(definitions, dict):
        raise AgentConfigError("agent_definitions must be a mapping")
    registry = copy.deepcopy(AGENT_PRESETS)
    for key, definition in definitions.items():
        registry[key] = validate_external_definition(key, definition, config_dir=config_dir)
    return registry
