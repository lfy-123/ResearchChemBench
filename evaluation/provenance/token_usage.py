"""Measure and compare recorded OpenCode token usage for benchmark workspaces."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

TOKEN_FIELDS = (
    "total",
    "input",
    "output",
    "reasoning",
    "cache_read",
    "cache_write",
)


def _empty_tokens() -> dict[str, int]:
    return {field: 0 for field in TOKEN_FIELDS}


def _message_tokens(message: dict[str, Any]) -> dict[str, int | None]:
    value = message.get("tokens") if isinstance(message.get("tokens"), dict) else {}
    cache = value.get("cache") if isinstance(value.get("cache"), dict) else {}
    def counter(number):
        return number if isinstance(number, int) and not isinstance(number, bool) and number >= 0 else None
    total, output = counter(value.get("total")), counter(value.get("output"))
    # Old provider input fields can exclude cache. Normalize only from explicit
    # total/output counters; do not guess absent cache/reasoning as zero or add
    # reasoning again to a reported output total.
    input_total = total - output if total is not None and output is not None and total >= output else None
    return {"total": total, "input": input_total, "output": output,
            "reasoning": counter(value.get("reasoning")), "cache_read": counter(cache.get("read")),
            "cache_write": counter(cache.get("write"))}


def _add_tokens(target, tokens):
    for field in TOKEN_FIELDS:
        target[field] = target[field] + tokens[field] if target[field] is not None and tokens[field] is not None else None


def workspace_token_usage(workspace: str | Path) -> dict[str, Any]:
    """Aggregate all primary and child OpenCode assistant-step usage."""

    root = Path(workspace).expanduser().resolve()
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    store = ExecutionStore.open_existing(root)
    if store is not None:
        details = store.usage_details()
        meta_path = root / "_meta.json"
        meta = json.loads(meta_path.read_text()) if meta_path.is_file() else {}
        tokens = dict(input=details["input_tokens"], output=details["output_tokens"], total=details["total_tokens"],
                      cache_read=details["cached_input_tokens"], cache_write=details["cache_write_input_tokens"],
                      reasoning=details["reasoning_output_tokens"])
        if details.get("accounting_status") == "unavailable":
            tokens = {key: None for key in tokens}
        return {"model_step_count": None, "agent_completed_turns": details["agent_completed_turns"],
                "session_count": len(details["by_session"]), "cost": 0.0, "cost_available": False,
                "tokens": tokens, "by_session": details["by_session"], "steps": [],
                "run_id": store.run_id, "model": meta.get("model"), "workspace": str(root),
                "first_model_step_tokens": {field: None for field in TOKEN_FIELDS},
                "context_file_bytes": {name: (root / name).stat().st_size if (root / name).is_file() else 0
                                       for name in ("INSTRUCTIONS.md", "_toolbox_catalog.json")},
                "source": "portable_control_archive" if store.path == root.parent / "control" / "execution.sqlite3" else "persistent_execution_store",
                "usage_details": details, "input_semantics": "total input including cached input",
                "model_step_count_available": False}
    database = root / "_opencode" / "opencode.db"
    if not database.is_file():
        raise FileNotFoundError(f"OpenCode database not found: {database}")
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            "SELECT session_id, time_created, data FROM message ORDER BY time_created, id"
        ).fetchall()
    finally:
        connection.close()

    aggregate = _empty_tokens()
    by_session: dict[str, dict[str, int]] = {}
    steps: list[dict[str, Any]] = []
    cost = 0.0
    for session_id, created, raw in rows:
        try:
            message = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        tokens = _message_tokens(message)
        _add_tokens(aggregate, tokens)
        session = by_session.setdefault(str(session_id), _empty_tokens())
        _add_tokens(session, tokens)
        cost += float(message.get("cost") or 0.0)
        steps.append(
            {
                "session_id": str(session_id),
                "time_created": created,
                "finish": message.get("finish"),
                **tokens,
            }
        )

    file_metrics = {}
    for name in ("INSTRUCTIONS.md", "_toolbox_catalog.json", "opencode.json"):
        path = root / name
        file_metrics[name] = path.stat().st_size if path.is_file() else 0
    meta = {}
    meta_path = root / "_meta.json"
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            meta = {}
    return {
        "workspace": str(root),
        "paper_id": meta.get("paper_id"),
        "task_type": meta.get("task_type"),
        "run_id": meta.get("run_id"),
        "model": meta.get("model"),
        "tool_discovery_mode": meta.get("tool_discovery_mode", "legacy_full"),
        "model_step_count": len(steps),
        "session_count": len(by_session),
        "cost": cost,
        "tokens": aggregate if steps else dict.fromkeys(TOKEN_FIELDS),
        "first_model_step_tokens": (
            {field: steps[0][field] for field in TOKEN_FIELDS} if steps else dict.fromkeys(TOKEN_FIELDS)
        ),
        "by_session": by_session,
        "context_file_bytes": file_metrics,
        "tool_call_count": meta.get("tool_call_count"),
        "successful_tool_calls": meta.get("successful_tool_calls"),
        "failed_tool_calls": meta.get("failed_tool_calls"),
        "input_semantics": "total input derived from explicit provider total minus output; unknown otherwise",
        "usage_details": {"accounting_status": "unavailable" if not steps else
                          "reported" if all(aggregate[field] is not None for field in ("total", "input", "output")) else "partial"},
    }


def compare_token_usage(before: str | Path, after: str | Path) -> dict[str, Any]:
    baseline = workspace_token_usage(before)
    candidate = workspace_token_usage(after)
    reductions = {}
    for field in TOKEN_FIELDS:
        old = baseline["tokens"][field]
        new = candidate["tokens"][field]
        reductions[field] = ((old - new) / old * 100.0) if old and new is not None else None
    old_first = baseline["first_model_step_tokens"]["total"]
    new_first = candidate["first_model_step_tokens"]["total"]
    return {
        "baseline": baseline,
        "candidate": candidate,
        "reduction_percent": reductions,
        "first_model_step_total_reduction_percent": (
            (old_first - new_first) / old_first * 100.0 if old_first and new_first is not None else None
        ),
    }


def _markdown(result: dict[str, Any]) -> str:
    before = result["baseline"]
    after = result["candidate"]
    reduction = result["reduction_percent"]
    lines = [
        "| Metric | Before | After | Reduction |",
        "|---|---:|---:|---:|",
    ]
    labels = {
        "total": "Total recorded tokens",
        "input": "Input tokens (see source semantics)",
        "cache_read": "Cache-read tokens",
        "cache_write": "Cache-write tokens",
        "output": "Output tokens",
        "reasoning": "Reasoning tokens",
    }
    for field in ("total", "input", "cache_read", "cache_write", "output", "reasoning"):
        value = reduction[field]
        reduction_text = "N/A" if value is None else f"{value:.2f}%"
        lines.append(
            f"| {labels[field]} | {_number(before['tokens'][field])} | "
            f"{_number(after['tokens'][field])} | {reduction_text} |"
        )
    first = result["first_model_step_total_reduction_percent"]
    lines.append(
        f"| First model step total | {_number(before['first_model_step_tokens']['total'])} | "
        f"{_number(after['first_model_step_tokens']['total'])} | "
        f"{'N/A' if first is None else f'{first:.2f}%'} |"
    )
    lines.append(
        f"| INSTRUCTIONS.md bytes | {before['context_file_bytes']['INSTRUCTIONS.md']:,} | "
        f"{after['context_file_bytes']['INSTRUCTIONS.md']:,} | — |"
    )
    return "\n".join(lines)


def _number(value):
    return "unavailable" if value is None else f"{value:,}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = compare_token_usage(args.before, args.after)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else _markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
