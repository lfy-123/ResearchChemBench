#!/usr/bin/env python3
"""Verify isolated backend runtimes and generate Markdown/JSON reports."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from dotenv import dotenv_values


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
CONFIG_PATH = ROOT / "config" / "mcp_profiles.yaml"
LOCAL_CONFIG_PATH = ROOT / "config.local.env"
JSON_REPORT = ROOT / "docs" / "MCP_PROFILE_STATUS.json"
MARKDOWN_REPORT = ROOT / "docs" / "MCP_PROFILE_STATUS.md"
MARKER = "PROFILE_PROBE_JSON="


def run_profile(name: str, profile: dict[str, Any], args, secrets: dict[str, str]) -> dict[str, Any]:
    python = (ROOT / profile["environment"] / "bin" / "python").resolve()
    if not python.is_file():
        return {"profile": name, "required_ok": False, "error": f"Missing Python: {python}"}
    command = [str(python), str(ROOT / "scripts" / "probe_mcp_profile.py"), "--profile", name]
    if args.live_materials_project and name == "services":
        command.append("--live-materials-project")
    if args.check_models and (profile.get("health_checks") or {}).get("models"):
        command.append("--check-models")
    environment = {**os.environ, **secrets}
    environment["PYTHONPATH"] = os.pathsep.join([str(ROOT), environment.get("PYTHONPATH", "")])
    with tempfile.TemporaryDirectory(prefix=f"researchchem_{name}_probe_") as workspace:
        environment["RESEARCHCHEMBENCH_WORKSPACE"] = workspace
        completed = subprocess.run(
            command, cwd=ROOT, env=environment, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=args.timeout_seconds, check=False,
        )
    lines = [line for line in completed.stdout.splitlines() if line.startswith(MARKER)]
    if not lines:
        return {"profile": name, "required_ok": False, "returncode": completed.returncode, "error": "No structured probe output", "output_tail": completed.stdout[-4000:]}
    result = json.loads(lines[-1][len(MARKER):])
    result["returncode"] = completed.returncode
    return result


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for name, result in payload["profiles"].items():
        available = sum(item.get("available", False) for item in result.get("backend_health", {}).values())
        total = len(result.get("expected_backends", []))
        detail = result.get("error") or f"{available}/{total} backends currently available"
        rows.append(
            f"| `{name}` | `{result.get('conda_name', '-')}` | {total} | "
            f"{'通过' if result.get('required_ok') else '失败'} | {detail} |"
        )
    return "\n".join(
        [
            "# Backend runtime status", "",
            f"Generated: {payload['generated_at']}",
            f"Public MCP tools: {payload['summary']['public_action_count']} (same for every task)",
            f"Backend runtimes checked: {payload['summary']['profile_count']}",
            "", "| Runtime | Conda environment | Backends | Required checks | Detail |",
            "|---|---|---:|---|---|", *rows, "",
            "Profiles are execution runtimes only; they do not own or filter public tools.", "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", default="")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--live-materials-project", action="store_true")
    parser.add_argument("--check-models", action="store_true")
    args = parser.parse_args()
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    profiles = config["profiles"]
    selected = [item.strip() for item in args.profiles.split(",") if item.strip()] or list(profiles)
    unknown = sorted(set(selected) - set(profiles))
    if unknown:
        raise SystemExit(f"Unknown profiles: {unknown}")
    secrets = {key: str(value) for key, value in dotenv_values(LOCAL_CONFIG_PATH).items() if value is not None} if LOCAL_CONFIG_PATH.exists() else {}
    results = {name: run_profile(name, profiles[name], args, secrets) for name in selected}
    from researchchem_toolbox.catalog import action_specs

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "profile_count": len(results),
            "ready_profiles": sum(bool(item.get("required_ok")) for item in results.values()),
            "public_action_count": len(action_specs()),
        },
        "profiles": results,
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MARKDOWN_REPORT.write_text(markdown(payload), encoding="utf-8")
    print(MARKDOWN_REPORT)
    return 1 if any(not item.get("required_ok") for item in results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
