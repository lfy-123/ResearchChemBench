#!/usr/bin/env python3
"""Run bounded live requests against all five external chemistry data actions."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.service import execute_action
from researchchem_toolbox.paths import portable_report_value


STATUS_PATH = TOOLBOX_ROOT / "config" / "data_source_smoke_status.json"


def main() -> int:
    load_dotenv(ROOT / "config.local.env", override=False)
    cases = [
        (
            "search_compounds",
            {
                "inputs": {"query": "water"},
                "method_spec": {},
                "action_settings": {"max_records": 1},
                "resource_limits": {"cpu_cores": 1},
            },
        ),
        (
            "search_protein_structures",
            {
                "inputs": {"query": "1CRN"},
                "method_spec": {},
                "action_settings": {"max_records": 1},
                "resource_limits": {"cpu_cores": 1},
            },
        ),
        (
            "search_materials",
            {
                "inputs": {"query": "mp-149"},
                "method_spec": {},
                "action_settings": {
                    "max_records": 1,
                    "fields": ["material_id", "formula_pretty"],
                },
                "resource_limits": {"cpu_cores": 1},
            },
        ),
        (
            "search_catalysis_records",
            {
                "inputs": {"query": {"reactants": "CO"}},
                "method_spec": {},
                "action_settings": {"max_records": 1},
                "resource_limits": {"cpu_cores": 1},
            },
        ),
        (
            "lookup_nist_webbook_species",
            {
                "inputs": {
                    "query": {"identifier": "7732-18-5", "namespace": "cas"}
                },
                "method_spec": {},
                "action_settings": {
                    "units": "SI",
                    "max_records": 1,
                },
                "resource_limits": {"cpu_cores": 1},
            },
        ),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="researchchem-data-source-smoke-") as temporary:
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = temporary
        for action_id, request in cases:
            started = time.monotonic()
            response = execute_action(action_id, request)
            result = response.get("result") or {}
            results.append(
                {
                    "action": action_id,
                    "backend": response.get("backend"),
                    "status": response["status"],
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "record_count": result.get("count"),
                    "error": response.get("error"),
                    "warnings": response.get("warnings", []),
                }
            )
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "summary": {
            "case_count": len(results),
            "passed": sum(item["status"] == "success" for item in results),
            "failed": sum(item["status"] != "success" for item in results),
            "all_ok": all(item["status"] == "success" for item in results),
        },
        "cases": results,
    }
    payload = portable_report_value(payload)
    STATUS_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(STATUS_PATH)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0 if payload["summary"]["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
