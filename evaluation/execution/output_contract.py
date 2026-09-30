"""Freeze the public output contract and use it consistently at finalization."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from chemistry_toolbox.src.output_contract import public_path, validate_output_contract
from .recovery import runner_store


def prepare_public_output_contract(workspace):
    """Expose this runner protocol's report requirement before freezing inputs."""
    path = public_path(workspace, "submission_schema.json")
    contract = json.loads(path.read_bytes()) if path.is_file() else {}
    if contract.get("report_file", "report/report.md") != "report/report.md":
        raise ValueError("Task report_file conflicts with the public benchmark report protocol")
    contract["report_file"] = "report/report.md"
    contract["framework_requirements_source"] = "benchmark-report-protocol-v1"
    path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n")


def freeze_public_output_contract(runner):
    path = public_path(runner.workspace, "submission_schema.json")
    payload = path.read_bytes() if path.is_file() else None
    runner_store(runner).put_record("frozen", "output_contract", {
        "text": payload.decode("utf-8") if payload is not None else None,
        "sha256": hashlib.sha256(payload).hexdigest() if payload is not None else None,
    }, immutable=True)


def validate_submission(runner):
    return validate_saved_submission(runner.workspace, runner.task_dir)


def validate_saved_submission(workspace, task_dir):
    workspace = Path(workspace)
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    store = ExecutionStore.open_existing(workspace)
    frozen = store.get_record("frozen", "output_contract") if store else None
    source = "frozen_public_contract"
    if frozen is None:
        # Compatibility with previous managed runs: use their frozen public
        # task snapshot, never an evaluation/reference file.
        path = Path(task_dir) / "agent_input" / "submission_schema.json"
        payload = path.read_bytes() if path.is_file() else None
        source = "task_package_public_contract"
    else:
        payload = frozen["text"].encode("utf-8") if frozen["text"] is not None else None
    effective = payload
    try:
        contract = json.loads(payload) if payload is not None else {}
    except (ValueError, UnicodeError):
        contract = None  # The common validator reports the malformed contract.
    if isinstance(contract, dict) and "report_file" not in contract and store:
        # Legacy runs already received this exact report protocol. Use only
        # hash-verified instructions, never a new requirement on old outputs.
        from chemistry_toolbox.src.recovery_io import file_hash
        instruction = workspace / "INSTRUCTIONS.md"
        expected = store.get_record("frozen", "files", {}).get("INSTRUCTIONS.md")
        if expected and instruction.is_file() and file_hash(instruction) == expected:
            if "The benchmark treats the task as incomplete if `report/report.md` is missing or empty." in instruction.read_text():
                effective = json.dumps({**contract, "report_file": "report/report.md"}).encode()
    result = validate_output_contract(workspace, effective)
    result["contract_sha256"] = hashlib.sha256(payload).hexdigest() if payload is not None else None
    try:
        path = public_path(workspace, "submission_schema.json")
        current = path.read_bytes() if path.is_file() else None
        matches = current == payload
    except (OSError, ValueError):
        matches = False
    if not matches:
        result["errors"].append({"code": "public_contract_modified", "file": "submission_schema.json",
                                 "message": "Workspace contract differs from the frozen public contract"})
        result.update(valid=False, status="invalid_request", error_count=result["error_count"] + 1)
    return {**result, "contract_source": source, "workspace_contract_matches": matches}
