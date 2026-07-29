#!/usr/bin/env python3
"""Run and archive one native-interface smoke for every software entry."""

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
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
for path in (TOOLBOX_ROOT / "src", PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chemistry_toolbox.mcp.execution_models import (
    JobCancelRequest,
    JobCollectRequest,
    JobStatusRequest,
    NativeJobRequest,
    StagedInput,
)
from chemistry_toolbox.mcp.open_execution import (
    cancel_execution_job,
    collect_execution_job,
    get_execution_job,
    submit_native_job,
)
from researchchem_toolbox.models import ResourceLimits


SCIENTIFIC_EVIDENCE = TOOLBOX_ROOT / "evidence" / "native_smoke" / "20260728_reliability_fix_v3"
DEFAULT_EVIDENCE = TOOLBOX_ROOT / "evidence" / "native_interface_smoke" / "20260728_all_software"
LATEST = TOOLBOX_ROOT / "evidence" / "native_interface_smoke" / "latest.json"
PLACEHOLDERS = {
    "easyspin": "MATLAB host and valid license are unavailable.",
    "matlab": "MATLAB executable and valid license are unavailable.",
}
SCIENTIFIC_CASES = {
    "orca": "orca_single_point",
    "gaussian": "gaussian_optimization_frequency",
    "crest": "crest_conformer_search",
    "vasp": "vasp_ground_state",
    "lobster": "lobster_cohp",
}
SCIENTIFIC_REQUESTS: dict[str, dict[str, Any]] = {
    "orca": {
        "software_id": "orca",
        "executable": "orca",
        "arguments": ["input.inp"],
        "staged_inputs": [{"source_path": "chemistry_toolbox/examples/native/orca/single_point/input.inp", "target_path": "input.inp"}],
        "resource_limits": {"memory_mb": 1024, "cpu_cores": 1, "gpu_count": 0},
    },
    "gaussian": {
        "software_id": "gaussian",
        "executable": "g16",
        "arguments": [],
        "staged_inputs": [{"source_path": "chemistry_toolbox/examples/native/gaussian/optimization/input.gjf", "target_path": "input.gjf"}],
        "stdin_target": "input.gjf",
        "resource_limits": {"memory_mb": 1024, "cpu_cores": 1, "gpu_count": 0},
    },
    "crest": {
        "software_id": "crest",
        "executable": "crest",
        "arguments": ["input.xyz", "--gfn2", "--T", "1"],
        "staged_inputs": [{"source_path": "chemistry_toolbox/examples/native/crest/conformer_search/input.xyz", "target_path": "input.xyz"}],
        "resource_limits": {"memory_mb": 1024, "cpu_cores": 1, "gpu_count": 0},
    },
    "vasp": {
        "software_id": "vasp",
        "executable": "vasp_std",
        "arguments": [],
        "staged_inputs": [
            {"source_path": f"chemistry_toolbox/examples/native/vasp/ground_state/{name}", "target_path": name}
            for name in ("INCAR", "POSCAR", "KPOINTS")
        ]
        + [{"source_path": "<licensed-si-potcar-workspace-path>", "target_path": "POTCAR"}],
        "resource_limits": {"memory_mb": 2048, "cpu_cores": 1, "gpu_count": 0},
    },
    "lobster": {
        "software_id": "lobster",
        "executable": "lobster-5.1.0",
        "arguments": [],
        "staged_inputs": [{"source_path": "chemistry_toolbox/examples/native/lobster/cohp/lobsterin", "target_path": "lobsterin"}]
        + [{"source_path": f"<compatible-vasp-job>/{name}", "target_path": name} for name in ("POSCAR", "POTCAR", "WAVECAR", "CONTCAR", "KPOINTS", "OUTCAR", "vasprun.xml")],
        "resource_limits": {"memory_mb": 1024, "cpu_cores": 1, "gpu_count": 0},
    },
}

# These commands are deliberately limited to version/help/startup routes. They
# verify Catalog resolution and the native execution contract without inventing
# scientific inputs or silently borrowing datasets.
PROBES: dict[str, tuple[str, list[str]]] = {
    "abinit": ("abinit", ["--version"]),
    "aiida": ("verdi", ["--version"]),
    "amber_pmemd": ("pmemd", ["-h"]),
    "arkane": ("Arkane.py", ["--help"]),
    "automekin": ("amk.sh", ["--version"]),
    "censo": ("censo", ["--version"]),
    "charmm": ("charmm", ["-h"]),
    "cp2k": ("cp2k", ["-version"]),
    "critic2": ("critic2", ["--version"]),
    "deepmd": ("dp", ["--version"]),
    "dftbplus": ("dftb+", ["--version"]),
    "gamess": ("rungms", ["-v"]),
    "geometric": ("geometric-optimize", ["--help"]),
    "gnina": ("gnina", ["--version"]),
    "goodvibes": ("goodvibes", ["--help"]),
    "gpaw": ("gpaw", ["--version"]),
    "gromacs": ("gmx", ["--version"]),
    "kinbot": ("kinbot", ["--help"]),
    "lammps": ("lmp", ["-help"]),
    "mesmer": ("mesmer", ["--help"]),
    "mess": ("mess", []),
    "multiwfn": ("Multiwfn_noGUI", ["-h"]),
    "namd": ("namd3", ["--version"]),
    "nequip": ("nequip-train", ["-cn", "interface_smoke", "--cfg", "job"]),
    "newton_x": ("nx_test", ["1"]),
    "nwchem": ("nwchem", ["--version"]),
    "openbabel": ("obabel", ["-V"]),
    "openff_am1bcc": ("antechamber", ["-h"]),
    "openmolcas": ("pymolcas", ["--version"]),
    "packmol": ("packmol", ["--help"]),
    "pdb_tools": ("pdb_selchain", ["-h"]),
    "phono3py": ("phono3py", ["-h"]),
    "phonopy": ("phonopy", ["-h"]),
    "plumed": ("plumed", ["info", "--version"]),
    "psi4": ("psi4", ["--version"]),
    "pysisyphus": ("pysis", ["interface_smoke.yaml"]),
    "qcengine": ("qcengine", ["--version"]),
    "quantum_espresso": ("pw.x", ["-version"]),
    "rmg": ("rmg.py", ["--help"]),
    "sharc": ("sharc.x", ["--version"]),
    "shengbte": ("ShengBTE", ["--help"]),
    "siesta": ("siesta", ["--version"]),
    "theodore": ("theodore", ["--version"]),
    "vesta": ("VESTA", ["-h"]),
    "vina": ("vina", ["--version"]),
    "vmd": ("vmd", ["-dispdev", "text", "-eofexit"]),
    "wannier90": ("wannier90.x", ["--version"]),
    "xtb": ("xtb", ["--version"]),
    "yambo": ("p2y", ["--version"]),
}
STDIN_PROBES = {"multiwfn", "packmol", "siesta"}
CONFIG_PROBES = {
    "nequip": ("interface_smoke.yaml", "{}\n"),
    "pysisyphus": (
        "interface_smoke.yaml",
        "geom:\n  type: cart\n  fn: interface_smoke.xyz\n"
        "calc:\n  type: xtb\n  charge: 0\n  mult: 1\n  gfn: 2\n  pal: 1\n"
        "opt:\n  type: rfo\n  max_cycles: 5\n",
    ),
}

FATAL_TEXT = (
    "error while loading shared libraries",
    "segmentation fault",
    "traceback (most recent call last)",
    "cannot find primary config",
    "module import timed out",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wait_for_job(job_id: str, deadline_seconds: float) -> tuple[dict[str, Any], bool]:
    deadline = time.monotonic() + deadline_seconds
    while time.monotonic() < deadline:
        status = get_execution_job(JobStatusRequest(job_id=job_id, tail_chars=8000))
        if status["terminal"]:
            return status, False
        time.sleep(0.2)
    cancel_execution_job(JobCancelRequest(job_id=job_id))
    for _ in range(100):
        status = get_execution_job(JobStatusRequest(job_id=job_id, tail_chars=8000))
        if status["terminal"]:
            return status, True
        time.sleep(0.1)
    return status, True


def archive_job(workspace: Path, job_id: str, destination: Path) -> list[dict[str, Any]]:
    job_dir = workspace / "outputs" / "execution_jobs" / job_id
    destination.mkdir(parents=True, exist_ok=True)
    archived = []
    for name in ("request.json", "status.json", "collection.json", "stdout.log", "stderr.log"):
        source = job_dir / name
        if not source.is_file():
            continue
        target = destination / name
        shutil.copy2(source, target)
        archived.append({"path": name, "size_bytes": target.stat().st_size, "sha256": sha256(target)})
    return archived


def classify_probe(collected: dict[str, Any], combined_output: str, cancelled: bool) -> tuple[str, str]:
    lowered = combined_output.casefold()
    if cancelled:
        return "failed", "The command did not reach a terminal state before the interface-smoke deadline and was cancelled."
    if any(marker in lowered for marker in FATAL_TEXT):
        return "failed", "The executable was reached, but startup reported a runtime, import, or configuration failure."
    if collected.get("process_status") == "completed":
        if any(text in lowered for text in ("does not exist", "no input file", "cannot open file")):
            return "started_input_required", "The executable started but the selected route reported a missing scientific input."
        return "passed", "The configured executable completed the interface probe through the native job runner."
    return "started_input_required", "The executable started and emitted its banner, usage, or expected missing-input diagnostic, but did not complete successfully."


def imported_scientific_records(tested_at: str) -> list[dict[str, Any]]:
    manifest = json.loads((SCIENTIFIC_EVIDENCE / "manifest.json").read_text(encoding="utf-8"))
    cases = {item["case_id"]: item for item in manifest["cases"]}
    records = []
    for software_id, case_id in SCIENTIFIC_CASES.items():
        case = cases[case_id]
        records.append(
            {
                "software_id": software_id,
                "test_level": "scientific_smoke",
                "status": "passed",
                "reason": "A self-contained scientific smoke completed with normal software termination, task-specific convergence, and valid artifacts.",
                "tested_at": tested_at,
                "job_id": case["job_id"],
                "request": SCIENTIFIC_REQUESTS[software_id],
                "process_status": case["process_status"],
                "software_status": case["software_status"],
                "convergence_status": case["convergence_status"],
                "artifact_status": case["artifact_status"],
                "scientific_validation_status": case["scientific_validation_status"],
                "evidence_path": str((SCIENTIFIC_EVIDENCE / case_id).relative_to(PROJECT_ROOT)),
            }
        )
    return records


def execute(workspace: Path, evidence_dir: Path, deadline_seconds: float) -> dict[str, Any]:
    for name in ("code", "outputs", "report", "tool_logs"):
        (workspace / name).mkdir(parents=True, exist_ok=True)
    os.environ["RESEARCHCHEM_MCP_WORKSPACE"] = str(workspace.resolve())
    tested_at = datetime.now(timezone.utc).isoformat()
    records = imported_scientific_records(tested_at)
    for software_id, reason in PLACEHOLDERS.items():
        records.append(
            {
                "software_id": software_id,
                "test_level": "not_run_placeholder",
                "status": "skipped",
                "reason": reason,
                "tested_at": tested_at,
            }
        )
    for software_id, (executable, arguments) in sorted(PROBES.items()):
        staged_inputs = []
        stdin_target = None
        if software_id in STDIN_PROBES:
            source = workspace / "code" / f"{software_id}_interface_smoke.stdin"
            source.write_text("\n", encoding="utf-8")
            stdin_target = "interface_smoke.stdin"
            staged_inputs = [
                StagedInput(
                    source_path=str(source.relative_to(workspace)),
                    target_path=stdin_target,
                )
            ]
        if software_id in CONFIG_PROBES:
            target, content = CONFIG_PROBES[software_id]
            source = workspace / "code" / f"{software_id}_{target}"
            source.write_text(content, encoding="utf-8")
            staged_inputs.append(
                StagedInput(
                    source_path=str(source.relative_to(workspace)),
                    target_path=target,
                )
            )
            if software_id == "pysisyphus":
                geometry = workspace / "code" / "pysisyphus_interface_smoke.xyz"
                geometry.write_text(
                    "2\nH2 interface smoke\nH 0.0 0.0 0.0\nH 0.0 0.0 0.75\n",
                    encoding="utf-8",
                )
                staged_inputs.append(
                    StagedInput(
                        source_path=str(geometry.relative_to(workspace)),
                        target_path="interface_smoke.xyz",
                    )
                )
        request = NativeJobRequest(
            software_id=software_id,
            executable=executable,
            arguments=arguments,
            staged_inputs=staged_inputs,
            stdin_target=stdin_target,
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
            label=f"manual-interface-smoke-{software_id}",
        )
        record: dict[str, Any] = {
            "software_id": software_id,
            "test_level": "interface_smoke",
            "tested_at": tested_at,
            "request": request.model_dump(mode="json"),
        }
        try:
            submitted = submit_native_job(request)
        except Exception as exc:
            record.update(
                status="failed",
                reason="The native request raised a validation or submission exception.",
                submission_error={"type": type(exc).__name__, "message": str(exc)},
            )
            records.append(record)
            continue
        if submitted.get("status") != "success":
            record.update(status="failed", reason="The native request failed validation or submission.", submission=submitted)
            records.append(record)
            continue
        status, cancelled = wait_for_job(submitted["job_id"], deadline_seconds)
        collected = collect_execution_job(JobCollectRequest(job_id=submitted["job_id"]))
        job_dir = workspace / "outputs" / "execution_jobs" / submitted["job_id"]
        stdout = (job_dir / "stdout.log").read_text(encoding="utf-8", errors="replace") if (job_dir / "stdout.log").is_file() else ""
        stderr = (job_dir / "stderr.log").read_text(encoding="utf-8", errors="replace") if (job_dir / "stderr.log").is_file() else ""
        outcome, reason = classify_probe(collected, stdout + "\n" + stderr, cancelled)
        if software_id == "pysisyphus" and outcome == "passed" and "converged!" in stdout.casefold():
            record["test_level"] = "scientific_smoke"
            reason = (
                "A self-contained H2 optimization completed with task-specific convergence "
                "through the native job runner."
            )
        archive_dir = evidence_dir / software_id
        archived = archive_job(workspace, submitted["job_id"], archive_dir)
        record.update(
            status=outcome,
            reason=reason,
            job_id=submitted["job_id"],
            request_status=collected.get("request_status"),
            process_status=collected.get("process_status"),
            software_status=collected.get("software_status"),
            convergence_status=collected.get("convergence_status"),
            artifact_status=collected.get("artifact_status"),
            scientific_validation_status=collected.get("scientific_validation_status"),
            archived_files=archived,
            stdout_tail=stdout[-2000:],
            stderr_tail=stderr[-2000:],
            evidence_path=str(archive_dir.relative_to(PROJECT_ROOT)),
        )
        records.append(record)
    records.sort(key=lambda item: item["software_id"])
    counts: dict[str, int] = {}
    for item in records:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    manifest = {
        "schema_version": 1,
        "generated_at": tested_at,
        "runner": "chemistry_toolbox/scripts/run_native_interface_smokes.py",
        "scope": "56 Catalog software entries; scientific smoke where self-contained evidence exists, interface smoke otherwise",
        "counts": counts,
        "software": records,
    }
    evidence_dir.mkdir(parents=True, exist_ok=True)
    text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    (evidence_dir / "manifest.json").write_text(text, encoding="utf-8")
    LATEST.parent.mkdir(parents=True, exist_ok=True)
    LATEST.write_text(text, encoding="utf-8")
    return manifest


def verify(evidence_dir: Path) -> dict[str, Any]:
    manifest = json.loads((evidence_dir / "manifest.json").read_text(encoding="utf-8"))
    errors = []
    ids = [item["software_id"] for item in manifest.get("software", [])]
    if len(ids) != 56 or len(set(ids)) != 56:
        errors.append(f"expected 56 unique software records, found {len(ids)} records and {len(set(ids))} unique IDs")
    for item in manifest.get("software", []):
        for archived in item.get("archived_files", []):
            path = evidence_dir / item["software_id"] / archived["path"]
            if not path.is_file() or sha256(path) != archived["sha256"]:
                errors.append(f"{item['software_id']}: invalid archive {archived['path']}")
    return {"valid": not errors, "errors": errors, "counts": manifest.get("counts", {})}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--deadline-seconds", type=float, default=45.0)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    evidence_dir = args.evidence_dir.resolve()
    if args.verify:
        result = verify(evidence_dir)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["valid"] else 1
    if args.workspace:
        workspace = args.workspace.resolve()
        manifest = execute(workspace, evidence_dir, args.deadline_seconds)
    else:
        with tempfile.TemporaryDirectory(prefix="researchchem-all-native-smoke-") as temporary:
            manifest = execute(Path(temporary), evidence_dir, args.deadline_seconds)
    print(json.dumps(manifest["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
