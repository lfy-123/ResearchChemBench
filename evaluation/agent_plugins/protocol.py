"""Versioned public request and optional, self-reported agent observations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .registry import evaluator_environment, sensitive_name

REQUEST_VERSION = "rcb-agent-request-v1"
EVENT_VERSION = "rcb-agent-event-v1"


def write_external_request(runner, definition) -> Path:
    from chemistry_toolbox.src.recovery_io import atomic_json, file_hash
    from ..execution.recovery import runner_store
    directory = runner.workspace / "_agent_protocol"
    directory.mkdir(exist_ok=True)
    servers = []
    for spec in runner._mcp_server_specs():
        environment = {k: v for k, v in spec.get("environment", {}).items() if not evaluator_environment(k)}
        servers.append({"name": spec["name"], "transport": "stdio",
                        "command": spec["command"][0], "args": spec["command"][1:],
                        "env": {k: v for k, v in environment.items() if not sensitive_name(k)},
                        "env_from": {k: k for k in environment if sensitive_name(k)},
                        "disabled_tools": spec.get("disabled_tools", []),
                        "tool_timeout_ms": runner.mcp_tool_timeout_ms})
    atomic_json(directory / "tools.json", {"protocol": "rcb-tools-v1", "servers": servers})
    request = {"protocol": REQUEST_VERSION, "run_id": runner.run_id, "agent_key": runner.agent_key,
               "task": {"paper_id": runner.paper_id, "task_type": runner.task_type},
               "workspace": str(runner.workspace.resolve()),
               "instructions_file": str(runner.instructions_path.resolve()),
               "public_input_files": list(runner.public_task_files),
               "submission_schema_file": str(runner.workspace / "submission_schema.json"),
               "deadline_at": runner.deadline_at, "resource_budget": runner.resource_budget_record(),
               "model_budget": {"max_tokens": runner.max_tokens, "max_turns": runner.max_turns,
                                "enforcement": definition["model_budget_enforcement"]},
               "tools": {"backend": definition["execution_backend"], "config_file": str(directory / "tools.json")},
               "options": definition["options"]}
    path = directory / "request.json"
    atomic_json(path, request)
    files = [*runner.public_task_files, "INSTRUCTIONS.md", "_agent_protocol/request.json", "_agent_protocol/tools.json"]
    runner_store(runner).put_record("frozen", "external_agent", {
        "protocol": REQUEST_VERSION, "definition": definition,
        "definition_sha256": hashlib.sha256(json.dumps(definition, sort_keys=True).encode()).hexdigest(),
        "files": {name: file_hash(runner.workspace / name) for name in files},
        "command_files": {arg: file_hash(Path(arg)) for arg in definition["command"]
                          if Path(arg).is_absolute() and Path(arg).is_file()},
    }, immutable=True)
    path.chmod(0o444)
    (directory / "tools.json").chmod(0o444)
    return path


def normalize_external_event(event, *, run_id=None):
    if not isinstance(event, dict) or event.get("protocol") != EVENT_VERSION:
        return None
    if run_id is not None and event.get("run_id") != run_id:
        return None
    if event.get("event") not in {"message", "usage", "error"}:
        return None
    if any(not isinstance(event.get(k), str) or not event[k] for k in ("event_id", "agent_id", "run_id")):
        return None
    if any(event.get(k) is not None and not isinstance(event[k], str) for k in ("session_id", "model", "parent_agent_id", "text")):
        return None
    return {"provider": "external", "kind": event["event"], "phase": None, "call_id": None,
            "status": "failed" if event["event"] == "error" else "observed",
            "agent_id": event["agent_id"], "parent_agent_id": event.get("parent_agent_id"),
            "session_id": event.get("session_id"), "event_id": event["event_id"],
            "run_id": event["run_id"], "text": event.get("text"), "model": event.get("model"),
            "usage": event.get("usage"), "provenance": "agent_reported", "raw": event}


def validate_external_request(runner):
    from chemistry_toolbox.src.recovery_io import file_hash
    from ..execution.recovery import runner_store
    frozen = runner_store(runner).get_record("frozen", "external_agent")
    if not frozen:
        return {"valid": False, "errors": ["external_protocol_snapshot_missing"]}
    errors = []
    for name, digest in frozen["files"].items():
        path = runner.workspace / name
        if path.is_symlink() or not path.resolve().is_relative_to(runner.workspace.resolve()) or not path.is_file() or file_hash(path) != digest:
            errors.append(f"external_input_modified:{name}")
    return {"valid": not errors, "errors": errors}


def external_usage(events):
    """Partial observations are lower bounds, never proof of complete accounting."""
    scopes, seen, conflicts = {}, {}, False
    for event in events:
        if event.get("provider") != "external" or event.get("kind") != "usage":
            continue
        identity = (event.get("agent_id"), event.get("session_id"), event.get("event_id"))
        payload = (event.get("model"), event.get("usage"))
        if identity in seen:
            if seen[identity] != payload:
                conflicts = True
            continue
        seen[identity] = payload
        usage = event.get("usage")
        if not isinstance(usage, dict) or usage.get("mode") not in {"delta", "cumulative"}:
            conflicts = True
            continue
        counts = [usage.get("input_tokens"), usage.get("output_tokens")]
        if any(type(v) is not int or v < 0 for v in counts):
            conflicts = True
            continue
        key = (event.get("agent_id"), event.get("session_id"), event.get("model"))
        mode, totals = scopes.get(key, (usage["mode"], [0, 0]))
        if mode != usage["mode"] or (mode == "cumulative" and any(a < b for a, b in zip(counts, totals))):
            conflicts = True
            continue
        scopes[key] = (mode, counts if mode == "cumulative" else [a + b for a, b in zip(counts, totals)])
    known = bool(scopes) and not conflicts
    inputs = sum(v[1][0] for v in scopes.values()) if known else None
    outputs = sum(v[1][1] for v in scopes.values()) if known else None
    return {"available": known, "model_step_count": None, "session_count": len(scopes) if scopes else None,
            "cost": None, "accounting_status": "conflicting" if conflicts else "partial_agent_reported" if known else "unavailable",
            "coverage": "unknown", "enforcement": "agent_cooperative",
            "tokens": {"input": inputs, "output": outputs, "total": inputs + outputs if known else None,
                       "cache_read": None, "cache_write": None, "reasoning": None}}
