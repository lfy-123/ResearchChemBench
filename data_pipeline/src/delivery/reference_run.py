from __future__ import annotations

import json
import subprocess
import time
from collections import Counter
from pathlib import Path
from typing import Any

from src.core.io import sha256_file
from src.core.runtime import normalize_runtime


def execute_reference_run(spec: dict[str, Any]) -> dict[str, Any]:
    """Execute one explicit argv command and return a verified run manifest."""

    command = spec.get("command")
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(item, str) and item for item in command)
    ):
        raise ValueError("reference command must be a non-empty argv string list")
    cwd = Path(spec.get("cwd") or ".").expanduser().resolve()
    cwd.mkdir(parents=True, exist_ok=True)
    log_dir = Path(spec.get("log_dir") or cwd / "reference_run_logs").expanduser().resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=float(spec.get("timeout_seconds", 86_400)),
        env=None,
    )
    elapsed_hours = (time.monotonic() - started) / 3600
    stdout_path = log_dir / "stdout.log"
    stderr_path = log_dir / "stderr.log"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    artifacts = []
    for item in spec.get("artifacts", []):
        artifact = dict(item) if isinstance(item, dict) else {"path": item}
        path = Path(str(artifact.get("path") or ""))
        if not path.is_absolute():
            path = (cwd / path).resolve()
        artifact["path"] = str(path)
        artifacts.append(artifact)
    manifest = {
        "command": command,
        "cwd": str(cwd),
        "exit_code": completed.returncode,
        "measured_walltime_hours": round(elapsed_hours, 6),
        "cpu_cores": spec.get("cpu_cores"),
        "hardware": spec.get("hardware"),
        "software_versions": spec.get("software_versions", {}),
        "artifacts": artifacts,
        "stdout_log": str(stdout_path),
        "stderr_log": str(stderr_path),
        "stochastic": bool(spec.get("stochastic", False)),
        "cross_software_conversion": bool(spec.get("cross_software_conversion", False)),
        "sensitive_tolerance": bool(spec.get("sensitive_tolerance", False)),
        "unstable_convergence": bool(spec.get("unstable_convergence", False)),
    }
    return verify_reference_run(manifest)


def attach_reference_runs(
    records: list[dict[str, Any]], config: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Attach and verify externally executed reference-run manifests.

    The pipeline does not guess a universal chemistry command. A constructor runs
    the selected protocol in the target environment and registers its manifest.
    """

    config = config or {}
    manifest_dir = Path(config["manifest_dir"]).expanduser() if config.get("manifest_dir") else None
    output: list[dict[str, Any]] = []
    for record in records:
        updated = dict(record)
        reference = record.get("reference_run")
        source = "record"
        if not reference and manifest_dir:
            path = manifest_dir / f"{record['paper_id']}.json"
            if path.is_file():
                reference = json.loads(path.read_text(encoding="utf-8"))
                source = "manifest_file"
        if reference:
            verified = verify_reference_run(reference)
            verified["source"] = source
            updated["reference_run"] = verified
            runtime = dict(updated.get("runtime") or {})
            if verified.get("measured_walltime_hours") is not None:
                runtime["measured_walltime_hours"] = verified["measured_walltime_hours"]
            for field in ("cpu_cores", "hardware", "software_versions"):
                if verified.get(field) is not None:
                    runtime[field] = verified[field]
            updated["runtime"] = runtime
        updated["runtime"] = normalize_runtime(updated.get("runtime"))
        output.append(updated)
    return output


def verify_reference_run(reference: dict[str, Any]) -> dict[str, Any]:
    output = dict(reference)
    artifacts = []
    failures = []
    for item in reference.get("artifacts", []):
        artifact = dict(item)
        path = Path(str(item.get("path") or "")).expanduser()
        exists = path.is_file()
        artifact["exists"] = exists
        if exists:
            artifact["size_bytes"] = path.stat().st_size
            artifact["sha256"] = sha256_file(path)
            expected = item.get("expected_sha256")
            if expected and expected != artifact["sha256"]:
                failures.append(f"artifact checksum mismatch: {path}")
        else:
            failures.append(f"missing reference artifact: {path}")
        artifacts.append(artifact)
    exit_code = reference.get("exit_code")
    if exit_code not in (None, 0):
        failures.append(f"reference command exit_code={exit_code}")
    if not reference.get("command"):
        failures.append("reference command is not recorded")
    if reference.get("measured_walltime_hours") is None:
        failures.append("measured walltime is not recorded")
    if not artifacts:
        failures.append("no reference artifacts are registered")
    output["artifacts"] = artifacts
    output["validation_failures"] = failures
    output["status"] = "validated" if not failures else "invalid"
    output["repeat_policy"] = _repeat_policy(reference)
    return output


def reference_run_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = Counter(
        (record.get("reference_run") or {}).get("status", "missing") for record in records
    )
    tiers = Counter(
        (record.get("runtime") or {}).get("runtime_tier", "unknown") for record in records
    )
    return {
        "records": len(records),
        "reference_run_statuses": dict(statuses),
        "runtime_tiers": dict(tiers),
    }


def _repeat_policy(reference: dict[str, Any]) -> dict[str, Any]:
    risk_flags = [
        flag
        for flag in (
            "stochastic",
            "cross_software_conversion",
            "sensitive_tolerance",
            "unstable_convergence",
        )
        if reference.get(flag)
    ]
    return {
        "second_run_required": bool(risk_flags),
        "risk_flags": risk_flags,
        "reason": "risk-triggered repeat"
        if risk_flags
        else "one validated deterministic run is sufficient",
    }
