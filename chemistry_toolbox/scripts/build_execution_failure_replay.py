#!/usr/bin/env python3
"""Build and verify an auditable replay index for historical execution failures."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
for path in (TOOLBOX_ROOT / "src", PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chemistry_toolbox.mcp.execution_models import AnalysisJobRequest, NativeJobRequest
from chemistry_toolbox.mcp.open_execution import (
    validate_analysis_program,
    validate_native_job,
)


SUBMISSION_TO_JOB_TYPE = {
    "submit_native_job": "native_software",
    "submit_analysis_program": "programmable_analysis",
}
TERMINAL_TOOLS = {"get_execution_job", "collect_execution_job"}
FAILURE_STATUSES = {"failed", "cancelled", "timed_out"}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


def submission_source_artifacts(
    event: dict[str, Any],
    request: dict[str, Any],
    job_id: str | None,
    workspace: Path,
) -> list[dict[str, Any]]:
    artifacts = [
        {
            "path": artifact.get("path"),
            "snapshot_path": artifact.get("snapshot_path"),
            "size_bytes": artifact.get("size_bytes"),
            "sha256": artifact.get("sha256"),
        }
        for artifact in event.get("artifacts") or []
        if artifact.get("snapshot_path") and artifact.get("sha256")
    ]
    known_names = {Path(str(item["path"])).name for item in artifacts if item.get("path")}
    targets = [str(request.get("script_target") or "agent_program.py")]
    targets.extend(str(item.get("target_path") or "") for item in request.get("staged_inputs") or [])
    if job_id:
        for target in targets:
            if not target or Path(target).name in known_names:
                continue
            path = workspace / "outputs" / "execution_jobs" / job_id / target
            if not path.is_file():
                continue
            relative = str(path.relative_to(workspace))
            artifacts.append(
                {
                    "path": relative,
                    "snapshot_path": relative,
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    return artifacts


def read_tool_result(trace_path: Path, event: dict[str, Any]) -> tuple[dict[str, Any] | None, Path | None]:
    relative = event.get("result_path")
    if not relative:
        return None, None
    path = trace_path.parent / str(relative)
    if not path.is_file():
        return None, path
    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, path
    result = envelope.get("result")
    return (result if isinstance(result, dict) else None), path


def replay_request(
    job_type: str,
    request: dict[str, Any],
    source_artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    replayed = json.loads(json.dumps(request))
    by_name: dict[str, str] = {}
    for artifact in source_artifacts:
        snapshot = artifact.get("snapshot_path")
        original = artifact.get("path")
        if snapshot and original:
            by_name[Path(str(original)).name] = str(snapshot)
    if job_type == "programmable_analysis":
        target = str(replayed.get("script_target") or "agent_program.py")
        if target in by_name:
            replayed["script_path"] = by_name[target]
    for staged in replayed.get("staged_inputs") or []:
        target = Path(str(staged.get("target_path") or "")).name
        if target in by_name:
            staged["source_path"] = by_name[target]
    return replayed


def revalidate(
    job_type: str,
    request: dict[str, Any],
    source_artifacts: list[dict[str, Any]],
    workspace: Path,
) -> dict[str, Any]:
    previous_workspace = os.environ.get("RESEARCHCHEM_MCP_WORKSPACE")
    os.environ["RESEARCHCHEM_MCP_WORKSPACE"] = str(workspace.resolve())
    try:
        request = replay_request(job_type, request, source_artifacts)
        if job_type == "native_software":
            parsed = NativeJobRequest.model_validate(request)
            result = validate_native_job(parsed)
        else:
            parsed = AnalysisJobRequest.model_validate(request)
            result = validate_analysis_program(parsed)
        if result.get("status") != "success" or result.get("valid") is not True:
            error = result.get("error") or {}
            return {
                "status": "rejected",
                "error_code": error.get("code"),
                "message": str(error.get("message") or result.get("status"))[:2000],
            }
        return {
            "status": "accepted",
            "calculation_intent": result.get("calculation_intent"),
            "script_sha256": result.get("script_sha256"),
            "input_deck_validation": result.get("input_deck_validation"),
        }
    except Exception as exc:  # Historical malformed requests are evidence, not runner errors.
        return {
            "status": "rejected",
            "exception_type": type(exc).__name__,
            "message": str(exc)[:2000],
        }
    finally:
        if previous_workspace is None:
            os.environ.pop("RESEARCHCHEM_MCP_WORKSPACE", None)
        else:
            os.environ["RESEARCHCHEM_MCP_WORKSPACE"] = previous_workspace


def build(workspaces_root: Path, *, run_revalidation: bool) -> dict[str, Any]:
    submissions: dict[tuple[str, str], dict[str, Any]] = {}
    immediate_failures: list[dict[str, Any]] = []
    submission_counts: Counter[str] = Counter()
    terminal_observations: Counter[str] = Counter()

    for trace_path in sorted(workspaces_root.rglob("_tool_trace.jsonl")):
        trace_relative = str(trace_path.relative_to(PROJECT_ROOT))
        trace_hash = sha256_file(trace_path)
        try:
            lines = trace_path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, start=1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            tool = event.get("tool")
            result, result_path = read_tool_result(trace_path, event)
            if tool in SUBMISSION_TO_JOB_TYPE:
                job_type = SUBMISSION_TO_JOB_TYPE[tool]
                submission_counts[job_type] += 1
                request = ((event.get("arguments") or {}).get("request") or {})
                job_id = (result or {}).get("job_id")
                source_artifacts = submission_source_artifacts(
                    event,
                    request,
                    str(job_id) if job_id else None,
                    trace_path.parent,
                )
                record = {
                    "job_id": job_id,
                    "job_type": job_type,
                    "run_id": event.get("run_id"),
                    "trace_path": trace_relative,
                    "trace_line": line_number,
                    "trace_sha256": trace_hash,
                    "submission_result_path": (
                        str(result_path.relative_to(PROJECT_ROOT)) if result_path and result_path.is_file() else None
                    ),
                    "submission_result_sha256": (
                        sha256_file(result_path) if result_path and result_path.is_file() else None
                    ),
                    "request": request,
                    "request_sha256": canonical_hash(request),
                    "source_artifacts": source_artifacts,
                    "terminal_observation": None,
                }
                if job_id:
                    submissions[(trace_relative, str(job_id))] = record
                elif (result or {}).get("status") != "success":
                    record["terminal_observation"] = {
                        "status": (result or {}).get("status") or event.get("status"),
                        "error": (result or {}).get("error") or event.get("error"),
                    }
                    immediate_failures.append(record)
                continue
            if tool not in TERMINAL_TOOLS or result is None:
                continue
            job = result.get("job") or {}
            job_id = result.get("job_id") or job.get("job_id")
            status = job.get("status") or result.get("job_status")
            if not job_id or status not in FAILURE_STATUSES:
                continue
            key = (trace_relative, str(job_id))
            if key not in submissions:
                continue
            terminal_observations[str(status)] += 1
            submissions[key]["terminal_observation"] = {
                "status": status,
                "result_path": str(result_path.relative_to(PROJECT_ROOT)) if result_path else None,
                "result_sha256": sha256_file(result_path) if result_path and result_path.is_file() else None,
                "return_code": job.get("return_code"),
                "duration_seconds": job.get("duration_seconds"),
                "resource_limits": job.get("resource_limits"),
                "resource_usage": job.get("resource_usage"),
                "error": job.get("error"),
                "stdout_tail": str(result.get("stdout_tail") or "")[-2000:],
                "stderr_tail": str(result.get("stderr_tail") or "")[-3000:],
            }

    records = [
        record
        for record in submissions.values()
        if (record.get("terminal_observation") or {}).get("status") in FAILURE_STATUSES
    ]
    records.extend(immediate_failures)
    records.sort(key=lambda item: (item["trace_path"], item["trace_line"], item.get("job_id") or ""))
    if run_revalidation:
        for record in records:
            record["current_preflight"] = revalidate(
                record["job_type"],
                record["request"],
                record["source_artifacts"],
                PROJECT_ROOT / Path(record["trace_path"]).parent,
            )

    by_type = Counter(record["job_type"] for record in records)
    by_status = Counter(
        str((record.get("terminal_observation") or {}).get("status")) for record in records
    )
    preflight = Counter(
        str((record.get("current_preflight") or {}).get("status", "not_run")) for record in records
    )
    error_codes = Counter()
    for record in records:
        error = (record.get("terminal_observation") or {}).get("error")
        if isinstance(error, dict) and error.get("code"):
            error_codes[str(error["code"])] += 1
        elif error:
            error_codes["unstructured_error"] += 1
        else:
            error_codes["no_structured_error"] += 1
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(workspaces_root.relative_to(PROJECT_ROOT)),
        "method": {
            "unit": "one submitted job or one immediately rejected submission",
            "deduplication": "trace_path plus job_id; repeated status polling is not a new failure",
            "revalidation": "current validators only; failed scientific jobs are not re-executed",
        },
        "summary": {
            "submission_counts": dict(sorted(submission_counts.items())),
            "failure_record_count": len(records),
            "failure_records_by_job_type": dict(sorted(by_type.items())),
            "failure_records_by_status": dict(sorted(by_status.items())),
            "terminal_failure_observations": dict(sorted(terminal_observations.items())),
            "current_preflight": dict(sorted(preflight.items())),
            "historical_error_codes": dict(sorted(error_codes.items())),
        },
        "records": records,
    }


def verify(manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    records = manifest.get("records") or []
    if manifest.get("summary", {}).get("failure_record_count") != len(records):
        errors.append("summary failure_record_count does not match records")
    for index, record in enumerate(records):
        prefix = f"record {index}"
        if canonical_hash(record.get("request") or {}) != record.get("request_sha256"):
            errors.append(f"{prefix}: request hash mismatch")
        for path_key, hash_key in (
            ("trace_path", "trace_sha256"),
            ("submission_result_path", "submission_result_sha256"),
        ):
            relative = record.get(path_key)
            expected = record.get(hash_key)
            if not relative or not expected:
                continue
            path = PROJECT_ROOT / relative
            if not path.is_file() or sha256_file(path) != expected:
                errors.append(f"{prefix}: invalid provenance file {relative}")
        observation = record.get("terminal_observation") or {}
        relative = observation.get("result_path")
        expected = observation.get("result_sha256")
        if relative and expected:
            path = PROJECT_ROOT / relative
            if not path.is_file() or sha256_file(path) != expected:
                errors.append(f"{prefix}: invalid terminal result {relative}")
        workspace = PROJECT_ROOT / Path(record["trace_path"]).parent
        for artifact in record.get("source_artifacts") or []:
            relative = artifact.get("snapshot_path")
            expected = artifact.get("sha256")
            if not relative or not expected:
                continue
            path = workspace / relative
            if not path.is_file() or sha256_file(path) != expected:
                errors.append(f"{prefix}: invalid source artifact {relative}")
    return {"valid": not errors, "errors": errors, "record_count": len(records)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspaces-root", type=Path, default=PROJECT_ROOT / "workspaces")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--revalidate", action="store_true")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        result = verify(args.verify.resolve())
        print(json.dumps(result, sort_keys=True))
        return 0 if result["valid"] else 1
    if args.output is None:
        parser.error("--output is required unless --verify is used")
    manifest = build(args.workspaces_root.resolve(), run_revalidation=args.revalidate)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
