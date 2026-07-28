from __future__ import annotations

import importlib.util
import json
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]


def test_historical_failure_replay_manifest_is_auditable() -> None:
    script = TOOLBOX_ROOT / "scripts" / "build_execution_failure_replay.py"
    spec = importlib.util.spec_from_file_location("build_execution_failure_replay", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    manifest_path = TOOLBOX_ROOT / "evidence/execution_failure_replay/20260728_manifest.json"
    result = module.verify(manifest_path)
    assert result == {"valid": True, "errors": [], "record_count": 81}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = manifest["summary"]
    assert summary["failure_records_by_job_type"] == {
        "native_software": 47,
        "programmable_analysis": 34,
    }
    assert summary["current_preflight"] == {"accepted": 12, "rejected": 69}
    assert all(record["current_preflight"]["status"] for record in manifest["records"])
