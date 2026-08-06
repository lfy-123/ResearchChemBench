#!/usr/bin/env python3
"""Execute and archive the five reviewed native-software smoke jobs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
for path in (TOOLBOX_ROOT / "src", PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chemistry_toolbox.mcp.execution_models import (
    JobCollectRequest,
    JobStatusRequest,
    NativeJobRequest,
    StagedInput,
)
from chemistry_toolbox.mcp.open_execution import (
    collect_execution_job,
    get_execution_job,
    submit_native_job,
)
from researchchem_toolbox.models import ResourceLimits
from researchchem_toolbox.paths import portable_report_text, portable_report_value


EXAMPLES = TOOLBOX_ROOT / "examples" / "native"
ARCHIVE_FILES = {
    "request.json",
    "status.json",
    "collection.json",
    "stdout.log",
    "stderr.log",
    "OUTCAR",
    "vasprun.xml",
    "lobsterout",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_archived_text(path: Path) -> None:
    if path.suffix == ".json":
        value = portable_report_value(json.loads(path.read_text(encoding="utf-8")))
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        text = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(portable_report_text(text), encoding="utf-8")


def wait_for_job(job_id: str, timeout: float = 600.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = get_execution_job(JobStatusRequest(job_id=job_id, tail_chars=4000))
        if result["terminal"]:
            return result
        time.sleep(0.1)
    raise TimeoutError(f"Smoke job did not finish within {timeout} seconds: {job_id}")


def stage(workspace: Path, source: Path, target: str, prefix: str) -> StagedInput:
    destination = workspace / "code" / f"{prefix}_{Path(target).name}"
    shutil.copy2(source, destination)
    return StagedInput(
        source_path=str(destination.relative_to(workspace)),
        target_path=target,
    )


def run_case(
    case_id: str,
    request: NativeJobRequest,
    *,
    workspace: Path,
    evidence_dir: Path,
) -> tuple[dict, Path]:
    submitted = submit_native_job(request)
    if submitted.get("status") != "success":
        raise RuntimeError(f"{case_id} submission failed: {submitted}")
    finished = wait_for_job(submitted["job_id"])
    collected = collect_execution_job(JobCollectRequest(job_id=submitted["job_id"]))
    job_dir = workspace / "outputs" / "execution_jobs" / submitted["job_id"]
    archive_dir = evidence_dir / case_id
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = []
    for path in sorted(job_dir.iterdir()):
        if path.name not in ARCHIVE_FILES or not path.is_file():
            continue
        destination = archive_dir / path.name
        shutil.copy2(path, destination)
        normalize_archived_text(destination)
        archived.append(
            {
                "path": str(destination.relative_to(evidence_dir)),
                "size_bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )
    record = {
        "case_id": case_id,
        "software_id": request.software_id,
        "job_id": submitted["job_id"],
        "job_status": finished["job"]["status"],
        "request_status": collected["request_status"],
        "process_status": collected["process_status"],
        "software_status": collected["software_status"],
        "convergence_status": collected["convergence_status"],
        "artifact_status": collected["artifact_status"],
        "scientific_validation_status": collected["scientific_validation_status"],
        "calculation_intent": finished["job"].get("metadata", {}).get("calculation_intent"),
        "archived_files": archived,
    }
    return record, job_dir


def execute(workspace: Path, evidence_dir: Path, vasp_potcar: Path) -> dict:
    for name in ("code", "outputs", "report", "tool_logs"):
        (workspace / name).mkdir(parents=True, exist_ok=True)
    os.environ["RESEARCHCHEM_MCP_WORKSPACE"] = str(workspace.resolve())
    cases = []

    orca = stage(workspace, EXAMPLES / "orca/single_point/input.inp", "input.inp", "orca")
    record, _ = run_case(
        "orca_single_point",
        NativeJobRequest(
            software_id="orca",
            executable="orca",
            arguments=["input.inp"],
            staged_inputs=[orca],
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        ),
        workspace=workspace,
        evidence_dir=evidence_dir,
    )
    cases.append(record)

    gaussian = stage(
        workspace,
        EXAMPLES / "gaussian/optimization/input.gjf",
        "input.gjf",
        "gaussian",
    )
    record, _ = run_case(
        "gaussian_optimization_frequency",
        NativeJobRequest(
            software_id="gaussian",
            executable="g16",
            stdin_target="input.gjf",
            staged_inputs=[gaussian],
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        ),
        workspace=workspace,
        evidence_dir=evidence_dir,
    )
    cases.append(record)

    crest = stage(
        workspace,
        EXAMPLES / "crest/conformer_search/input.xyz",
        "input.xyz",
        "crest",
    )
    record, _ = run_case(
        "crest_conformer_search",
        NativeJobRequest(
            software_id="crest",
            executable="crest",
            arguments=["input.xyz", "--gfn2", "--T", "1"],
            staged_inputs=[crest],
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        ),
        workspace=workspace,
        evidence_dir=evidence_dir,
    )
    cases.append(record)

    vasp_inputs = [
        stage(workspace, EXAMPLES / f"vasp/ground_state/{name}", name, "vasp")
        for name in ("INCAR", "POSCAR", "KPOINTS")
    ]
    vasp_inputs.append(stage(workspace, vasp_potcar, "POTCAR", "vasp"))
    record, vasp_job_dir = run_case(
        "vasp_ground_state",
        NativeJobRequest(
            software_id="vasp",
            executable="vasp_std",
            staged_inputs=vasp_inputs,
            resource_limits=ResourceLimits(memory_mb=2048, cpu_cores=1),
        ),
        workspace=workspace,
        evidence_dir=evidence_dir,
    )
    cases.append(record)

    lobster_inputs = [
        stage(workspace, EXAMPLES / "lobster/cohp/lobsterin", "lobsterin", "lobster")
    ]
    for name in ("POSCAR", "POTCAR", "WAVECAR", "CONTCAR", "KPOINTS", "OUTCAR", "vasprun.xml"):
        lobster_inputs.append(
            StagedInput(
                source_path=str((vasp_job_dir / name).relative_to(workspace)),
                target_path=name,
            )
        )
    record, _ = run_case(
        "lobster_cohp",
        NativeJobRequest(
            software_id="lobster",
            executable="lobster-5.1.0",
            staged_inputs=lobster_inputs,
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        ),
        workspace=workspace,
        evidence_dir=evidence_dir,
    )
    cases.append(record)

    manifest = portable_report_value({
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runner": "chemistry_toolbox/scripts/run_native_smokes.py",
        "workspace": "<temporary-workspace>",
        "licensed_inputs_archived": False,
        "cases": cases,
    })
    (evidence_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify(evidence_dir: Path) -> dict:
    manifest_path = evidence_dir / "manifest.json"
    manifest = portable_report_value(json.loads(manifest_path.read_text(encoding="utf-8")))
    errors = []
    for case in manifest.get("cases", []):
        if case.get("process_status") != "completed":
            errors.append(f"{case.get('case_id')}: process did not complete")
        if case.get("scientific_validation_status") != "mechanically_valid":
            errors.append(f"{case.get('case_id')}: mechanical validation failed")
        for item in case.get("archived_files", []):
            path = evidence_dir / item["path"]
            if not path.is_file() or sha256(path) != item["sha256"]:
                errors.append(f"{case.get('case_id')}: invalid archive {item['path']}")
    return {"valid": not errors, "errors": errors, "case_count": len(manifest.get("cases", []))}


def refresh_hashes(evidence_dir: Path) -> dict:
    manifest_path = evidence_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = evidence_dir.resolve()
    for case in manifest.get("cases", []):
        for item in case.get("archived_files", []):
            path = (evidence_dir / item["path"]).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                raise ValueError(f"Invalid archived evidence path: {item['path']}")
            normalize_archived_text(path)
            item["size_bytes"] = path.stat().st_size
            item["sha256"] = sha256(path)
    manifest["workspace"] = "<temporary-workspace>"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return verify(evidence_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--vasp-potcar", type=Path)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--refresh-hashes", action="store_true")
    args = parser.parse_args()
    evidence_dir = args.evidence_dir.resolve()
    if args.refresh_hashes:
        result = refresh_hashes(evidence_dir)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["valid"] else 1
    if args.verify:
        result = verify(evidence_dir)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["valid"] else 1
    if args.vasp_potcar is None or not args.vasp_potcar.is_file():
        parser.error("--vasp-potcar must name a licensed Si POTCAR for execution")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    if args.workspace:
        workspace = args.workspace.resolve()
        execute(workspace, evidence_dir, args.vasp_potcar.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix="researchchem-native-smoke-") as temporary:
            execute(Path(temporary), evidence_dir, args.vasp_potcar.resolve())
    result = verify(evidence_dir)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
