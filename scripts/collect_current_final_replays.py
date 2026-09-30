#!/usr/bin/env python3
"""Read-only status collector for the two current-final Gaussian replays.

The collector never submits, stops, or mutates an HPC job.  It records the
platform state and any persisted application output; scientific promotion to
the final evaluator archive is deliberately left to a later, evidence-gated
step after normal termination, frequency, and geometry-identity checks.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "docs/verification/current_final_replays"
WS = "ws-6e6ba362-e98e-45b2-9c5a-311998e93d65"
QZCLI_HOME = "/inspire/hdd/global_user/lifangyuan-253108110077/lfy_cc/.qzcli"
QZCLI_PATH = "/inspire/hdd/global_user/lifangyuan-253108110077/lfy_cc/qzcli_tool"
JOBS = {
    "paper_0dc85595cab7bc0a": {
        "job_id": "hpc-job-fac8f89c-e30e-4467-8d4d-0f4039dae417",
        "case": "current_final_displaced_1_cis",
        "method": "B3LYP/6-31G(d,p) EmpiricalDispersion=GD3BJ Opt Freq",
    },
    "paper_221aafe4bd916a11": {
        "job_id": "hpc-job-9ecf7b40-f515-45f7-8846-9666c77a4e07",
        "case": "current_final_displaced_2a",
        "method": "wB97XD/6-31G(d,p) Opt Freq PCM acetonitrile",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def application_state(path: Path) -> dict:
    stdout = path / "stdout.log"
    text = stdout.read_text(errors="replace") if stdout.is_file() else ""
    frequencies = []
    for line in text.splitlines():
        if "Frequencies --" in line:
            for value in re.findall(r"[-+]?\d+(?:\.\d+)?", line.split("--", 1)[1]):
                frequencies.append(float(value))
    return {
        "files": sorted(p.name for p in path.iterdir() if p.is_file()) if path.is_dir() else [],
        "stdout_sha256": digest(stdout),
        "input_sha256": digest(path / "input.com"),
        "normal_termination": "Normal termination of Gaussian" in text,
        "optimization_completed": "Optimization completed" in text,
        "frequency_count": len(frequencies) or None,
        "imaginary_frequency_count": sum(v < 0 for v in frequencies) if frequencies else None,
        "wrapper_status": (json.loads((path / "status.json").read_text()).get("return_code")
                           if (path / "status.json").is_file() else None),
        "success_marker": (path / "complete.marker").is_file(),
        "failure_marker": (path / "failure.marker").is_file(),
    }


def main() -> int:
    os.environ["QZCLI_HOME"] = QZCLI_HOME
    if QZCLI_PATH not in sys.path:
        sys.path.insert(0, QZCLI_PATH)
    from qzcli.api import QzAPI

    jobs = {j.get("job_id"): j for j in QzAPI().list_hpc_jobs(WS, page_size=500).get("jobs", [])}
    records = []
    for paper_id, spec in JOBS.items():
        job = jobs.get(spec["job_id"], {})
        out = OUT_ROOT / paper_id
        platform = {
            "job_id": spec["job_id"],
            "status": job.get("status", "NOT_VISIBLE"),
            "priority_level": job.get("priority_level"),
            "priority_name": job.get("priority_name"),
            "compute_group": job.get("logic_compute_group_name"),
            "cpu": (job.get("resource_spec_price") or {}).get("cpu_count"),
            "memory_gib": (job.get("resource_spec_price") or {}).get("memory_size_gib"),
            "timeline": job.get("timeline"),
        }
        app = application_state(out) if out.is_dir() else {"files": []}
        scientific_status = (
            "READY_FOR_GEOMETRY_IDENTITY_REVIEW"
            if platform["status"] in {"SUCCEEDED", "SUCCEEDED_RETAINING"}
            and app.get("normal_termination") and app.get("success_marker")
            else "WAITING_FOR_TERMINAL_SUCCESS"
        )
        records.append({"paper_id": paper_id, "case": spec["case"], "method": spec["method"],
                        "observed_at_utc": now(), "platform": platform, "application": app,
                        "scientific_status": scientific_status})
    payload = {"generated_at_utc": now(), "policy": "read-only; no job mutation", "records": records}
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "replay_status.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Current-final replay status", "", f"Generated: {payload['generated_at_utc']}",
             "", "This is a read-only HPC/application snapshot. No job was submitted or stopped.", ""]
    for row in records:
        p = row["platform"]; a = row["application"]
        lines += [f"## {row['paper_id']}", "", f"- Job: `{p['job_id']}`; status: `{p['status']}`; priority: `{p.get('priority_name')}`",
                  f"- Group: `{p.get('compute_group')}`; allocation: `{p.get('cpu')}` CPU / `{p.get('memory_gib')}` GiB",
                  f"- Application: normal={a.get('normal_termination')}, optimization={a.get('optimization_completed')}, frequencies={a.get('frequency_count')}, imaginary={a.get('imaginary_frequency_count')}",
                  f"- Scientific gate: **{row['scientific_status']}**", ""]
    (OUT_ROOT / "replay_status.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
