#!/usr/bin/env python3
"""Record which public Action/Backend pairs are exercised successfully.

The optional pytest run profiles calls to the real service.execute_action
function without changing production dispatch.  Existing bounded scientific,
data-source, and toolbox smoke reports are merged as independent evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from researchchem_toolbox.catalog import action_specs, backend_specs
from researchchem_toolbox.service import execute_action


DEFAULT_OUTPUT = ROOT / "config" / "action_test_coverage.json"
EXTERNAL_REPORTS = (
    (ROOT / "config" / "action_gap_smoke_status.json", "action_gap_smoke"),
    (ROOT / "config" / "backend_gap_smoke_status.json", "backend_gap_smoke"),
    (ROOT / "config" / "scientific_resource_smoke_status.json", "scientific_resource_smoke"),
    (ROOT / "config" / "data_source_smoke_status.json", "data_source_smoke"),
    (ROOT / "docs" / "TOOLBOX_STATUS.json", "toolbox_smoke"),
)


def _record(
    records: list[dict[str, Any]],
    *,
    action_id: str,
    backend_id: str | None,
    status: str,
    source: str,
    elapsed_seconds: float | None = None,
    detail: str | None = None,
) -> None:
    if action_id not in action_specs():
        return
    records.append(
        {
            "action": action_id,
            "backend": backend_id,
            "status": status,
            "source": source,
            "elapsed_seconds": elapsed_seconds,
            "detail": detail,
        }
    )


def _merge_external_reports(records: list[dict[str, Any]]) -> None:
    for path, source in EXTERNAL_REPORTS:
        if not path.is_file():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        cases = payload.get("cases")
        if cases is None and source == "toolbox_smoke":
            cases = payload.get("smoke") or []
        for item in cases or []:
            error = item.get("error")
            if isinstance(error, dict):
                detail = str(error.get("message") or error.get("code") or "")
            else:
                detail = str(error or "")
            _record(
                records,
                action_id=str(item.get("action") or ""),
                backend_id=(str(item["backend"]) if item.get("backend") else None),
                status=str(item.get("status") or "unknown"),
                source=source,
                elapsed_seconds=item.get("elapsed_seconds"),
                detail=detail or None,
            )


def _reuse_previous_pytest(records: list[dict[str, Any]], path: Path) -> None:
    if not path.is_file():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    for action in payload.get("actions") or []:
        for item in action.get("observations") or []:
            if item.get("source") == "pytest_dynamic":
                records.append(dict(item))


def _run_pytest(records: list[dict[str, Any]], pytest_args: list[str]) -> int:
    import pytest

    target_code = execute_action.__code__
    starts: dict[int, float] = {}

    def profiler(frame, event, value):
        if frame.f_code is not target_code:
            return profiler
        key = id(frame)
        if event == "call":
            starts[key] = time.monotonic()
        elif event == "return":
            status = value.get("status") if isinstance(value, dict) else "exception"
            backend_id = value.get("backend") if isinstance(value, dict) else None
            detail = None
            if isinstance(value, dict) and value.get("error"):
                error = value["error"]
                detail = str(error.get("message") if isinstance(error, dict) else error)
            _record(
                records,
                action_id=str(frame.f_locals.get("action_id") or ""),
                backend_id=(str(backend_id) if backend_id else None),
                status=str(status or "unknown"),
                source="pytest_dynamic",
                elapsed_seconds=round(time.monotonic() - starts.pop(key, time.monotonic()), 6),
                detail=detail,
            )
        return profiler

    sys.setprofile(profiler)
    try:
        return int(pytest.main(pytest_args))
    finally:
        sys.setprofile(None)


def _summary(records: list[dict[str, Any]], pytest_exit_code: int | None) -> dict[str, Any]:
    observations: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in records:
        observations[item["action"]].append(item)

    actions = []
    successful_pairs: set[tuple[str, str]] = set()
    failed_pairs: set[tuple[str, str]] = set()
    for action_id, specification in action_specs().items():
        values = observations.get(action_id, [])
        successes = [
            item for item in values if item["status"] in {"success", "partial_success"}
        ]
        failures = [
            item for item in values if item["status"] not in {"success", "partial_success"}
        ]
        for item in successes:
            if item.get("backend"):
                successful_pairs.add((action_id, item["backend"]))
        for item in failures:
            if item.get("backend"):
                failed_pairs.add((action_id, item["backend"]))
        if successes:
            status = "runtime_success"
        elif failures:
            status = "failure_only"
        else:
            status = "not_observed"
        actions.append(
            {
                "action": action_id,
                "category": specification.category,
                "description": specification.description,
                "primary_output": specification.primary_output,
                "selection_policy": specification.selection_policy,
                "catalog_backends": list(specification.backend_ids),
                "status": status,
                "successful_backends": sorted(
                    {item["backend"] for item in successes if item.get("backend")}
                ),
                "failed_backends": sorted(
                    {item["backend"] for item in failures if item.get("backend")}
                ),
                "evidence_sources": sorted({item["source"] for item in values}),
                "observations": values,
            }
        )

    all_pairs = {
        (action.id, backend_id)
        for action in action_specs().values()
        for backend_id in action.backend_ids
    }
    backend_success = {
        backend_id
        for _action_id, backend_id in successful_pairs
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pytest_exit_code": pytest_exit_code,
        "summary": {
            "action_count": len(actions),
            "runtime_success_actions": sum(item["status"] == "runtime_success" for item in actions),
            "failure_only_actions": sum(item["status"] == "failure_only" for item in actions),
            "not_observed_actions": sum(item["status"] == "not_observed" for item in actions),
            "action_backend_pair_count": len(all_pairs),
            "successful_action_backend_pairs": len(successful_pairs),
            "failed_action_backend_pairs": len(failed_pairs - successful_pairs),
            "unobserved_action_backend_pairs": len(all_pairs - successful_pairs - failed_pairs),
            "backend_count": len(backend_specs()),
            "backends_with_runtime_success_evidence": len(backend_success),
            "backends_without_runtime_success_evidence": len(backend_specs()) - len(backend_success),
        },
        "actions": actions,
        "successful_action_backend_pairs": [list(value) for value in sorted(successful_pairs)],
        "failed_action_backend_pairs": [list(value) for value in sorted(failed_pairs - successful_pairs)],
        "unobserved_action_backend_pairs": [
            list(value) for value in sorted(all_pairs - successful_pairs - failed_pairs)
        ],
        "backends_without_runtime_success_evidence": sorted(set(backend_specs()) - backend_success),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-pytest", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("pytest_args", nargs="*", default=["-q"])
    args = parser.parse_args()

    records: list[dict[str, Any]] = []
    pytest_exit_code = None
    if args.run_pytest:
        pytest_exit_code = _run_pytest(records, args.pytest_args or ["-q"])
    else:
        _reuse_previous_pytest(records, args.output)
    _merge_external_reports(records)
    payload = _summary(records, pytest_exit_code)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return int(pytest_exit_code or 0)


if __name__ == "__main__":
    raise SystemExit(main())
