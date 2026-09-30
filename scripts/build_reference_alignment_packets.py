#!/usr/bin/env python3
"""Build a compact evidence packet for each final task/reference pair.

This indexes facts for human review; it deliberately does not adjudicate
scientific equivalence or rewrite any task.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MODES = ("autonomous_research", "paper_reproduction")
GROUPS = tuple(f"group_{i}" for i in range(1, 7))
RISK = re.compile(r"optimized|optimised|relaxed|transition[ _-]?state|\bts\d*\b|product|final", re.I)
SI = re.compile(r"\bSI\b|supplementary|supporting information", re.I)
TERMS = ("optimization", "opt", "frequency", "freq", "stationary", "saddle", "minimum", "irc", "scan", "td-dft", "excitation", "hole", "electron", "band gap", "band", "dos", "work function", "dipole", "free energy", "gibbs", "conformer", "spin", "soc", "nmr", "binding energy", "formation energy", "barrier", "reaction energy", "convergence")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path, repo: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return str(path)


def load(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def sections(text: str) -> list[str]:
    return [m.group(1).strip().casefold() for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.M)]


def groups(repo: Path, paper_id: str) -> list[Path]:
    return [repo / "docs" / "verification" / g / paper_id for g in GROUPS if (repo / "docs" / "verification" / g / paper_id).is_dir()]


def archive_facts(path: Path, repo: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
    def capture(pattern: str) -> str | None:
        m = re.search(pattern, text, re.I)
        return m.group(1).strip() if m else None
    start = text.find("## Successful calculation chain")
    fence = text.find("```json", start)
    result: Any = None
    if fence >= 0:
        body = text[fence + 7:]
        end = body.find("```")
        if end >= 0:
            try: result = json.loads(body[:end].strip())
            except Exception: result = None
    ordered = text[text.find("## Ordered successful execution steps"):text.find("## Evaluator alignment", text.find("## Ordered successful execution steps") + 1)]
    steps = re.findall(r"^\s*\d+\.\s+(.+)$", ordered, re.M)
    return {
        "exists": path.is_file(), "path": rel(path, repo) if path.is_file() else None,
        "sha256": digest(path) if path.is_file() else None,
        "chain_status": capture(r"Computation-chain status:\s*\*\*([^*]+)\*\*"),
        "group_result_status": capture(r"Group result status:\s*`([^`]+)`"),
        "verification_status": capture(r"Verification-report terminal status:\s*`([^`]+)`"),
        "current_final_applicability": capture(r"Applicability to current final package:\s*\*\*([^*]+)\*\*"),
        "evaluator_field_status": capture(r"Bound result-field status:\s*\*\*([^*]+)\*\*"),
        "successful_artifact_count": capture(r"Successful status/output inventory entries:\s*\*\*([^*]+)\*\*"),
        "successful_step_count": len(steps), "successful_step_headers": steps[:40],
        "result_status": result.get("status") if isinstance(result, dict) else None,
        "result_keys": sorted(result.keys()) if isinstance(result, dict) else [],
        "result_text": json.dumps(result, ensure_ascii=False) if result is not None else "",
        "partial_or_missing_language": bool(re.search(r"partial|bounded_failure|evidence insufficient|missing|incomplete|证据不足", text, re.I)),
        "private_reference_language": bool(re.search(r"private|evaluator-private|hidden", text, re.I)),
    }


def input_facts(pkg: Path, repo: Path) -> list[dict[str, Any]]:
    rows = []
    root = pkg / "agent_input"
    for p in sorted(x for x in root.rglob("*") if x.is_file()) if root.is_dir() else []:
        text = p.read_text(encoding="utf-8", errors="replace")
        head = "\n".join(text.splitlines()[:4])
        rows.append({"path": rel(p, pkg), "sha256": digest(p), "size": p.stat().st_size,
                     "high_risk_marker": bool(RISK.search(p.name) or RISK.search(head)),
                     "si_marker": bool(SI.search(p.name) or SI.search(head)),
                     "head": head[:500] if p.suffix.casefold() in {".xyz", ".cif", ".poscar", ".vasp", ".json", ".txt"} else None})
    return rows


def group_facts(group: Path | None, repo: Path) -> dict[str, Any]:
    if group is None: return {"exists": False}
    result_path = group / "report" / "results.json"
    report_path = group / "verification_report.md"
    result = load(result_path, {}) if result_path.is_file() else {}
    report = report_path.read_text(encoding="utf-8", errors="replace") if report_path.is_file() else ""
    successful = []
    for p in sorted(group.rglob("status.json")):
        payload = load(p, {}) or {}
        status = str(payload.get("status", payload.get("state", ""))).casefold()
        rc = payload.get("return_code", payload.get("exit_code"))
        if status in {"success", "successful", "complete", "completed", "validated", "passed"} or rc == 0:
            successful.append({"path": rel(p, repo), "status": status, "return_code": rc})
    return {"exists": True, "path": rel(group, repo),
            "result_path": rel(result_path, repo) if result_path.is_file() else None,
            "result_status": result.get("status") if isinstance(result, dict) else None,
            "result_keys": sorted(result.keys()) if isinstance(result, dict) else [],
            "report_status_tokens": sorted(set(re.findall(r"\b(PASS|QUALIFIED|CONDITIONAL|BLOCKED|IN_PROGRESS|FAIL|NOT_QUALIFIED)\b", report, re.I))),
            "successful_status_count": len(successful), "successful_status_records": successful[:100]}


def build(repo: Path, out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for mode in MODES:
        root = repo / "tasks" / f"final_verified_{mode}"
        for pkg in sorted(root.glob("paper_*")):
            task_path = pkg / "agent_input" / "task.md"
            task = task_path.read_text(encoding="utf-8", errors="replace") if task_path.is_file() else ""
            info = load(pkg / "task_info.json", {}) or {}
            archive = archive_facts(pkg / "evaluation" / "verified_computation_reference.md", repo)
            gs = groups(repo, pkg.name)
            ref_text = archive.get("result_text", "") + " " + " ".join(archive.get("successful_step_headers", []))
            task_terms = {x for x in TERMS if x in task.casefold()}
            ref_terms = {x for x in TERMS if x in ref_text.casefold()}
            declared = info.get("data", []) if isinstance(info, dict) else []
            missing = [str(x.get("path", "")) for x in declared if isinstance(x, dict) and not (pkg / "agent_input" / str(x.get("path", ""))).exists()]
            public = input_facts(pkg, repo)
            record = {
                "paper_id": pkg.name, "mode": mode, "title": info.get("title"),
                "package_path": rel(pkg, repo), "task_path": rel(task_path, repo) if task_path.is_file() else None,
                "task_sha256": digest(task_path) if task_path.is_file() else None,
                "task_info_sha256": digest(pkg / "task_info.json") if (pkg / "task_info.json").is_file() else None,
                "task_sections": sections(task),
                "task_markers": {"autonomous_boundary": bool(re.search(r"do not use.{0,180}(paper|SI)|不得读取.{0,100}(论文|SI)", task, re.I | re.S)), "author_guidance_heading": "# author-provided scientific guidance" in task.casefold(), "failure_or_stop": bool(re.search(r"failure|failed|bounded|unresolved|stop|停止|失败", task, re.I)), "risk_words": sorted(set(RISK.findall(task)))},
                "task_terms": sorted(task_terms), "reference_terms": sorted(ref_terms), "reference_terms_absent_from_task": sorted(ref_terms - task_terms),
                "declared_data": [{"path": str(x.get("path", "")), "description": str(x.get("description", ""))} for x in declared if isinstance(x, dict)],
                "declared_data_missing": missing, "public_files": public,
                # Only data files are relevant to geometry/provenance leakage;
                # task.md/schema naturally contain words such as “final” and
                # must not be reported as leaked structures.
                "public_high_risk_files": [x["path"] for x in public if x["high_risk_marker"] and x["path"].startswith("agent_input/data/")], "public_si_marker_files": [x["path"] for x in public if x["si_marker"] and x["path"].startswith("agent_input/data/")],
                "archive": archive, "group_candidates": [rel(x, repo) for x in gs], "group": group_facts(gs[0] if gs else None, repo),
                "evaluator_paths": {k: rel(pkg / p, repo) for k, p in {"schema":"agent_input/submission_schema.json", "key_points":"evaluation/reference_key_points.json", "conclusions":"evaluation/reference_conclusions.json", "scoring":"evaluation/scoring_rules.json", "critical_failures":"evaluation/critical_failures.json", "paper_route":"paper_route.md"}.items() if (pkg / p).is_file()},
            }
            records.append(record)
            dest = out / mode; dest.mkdir(exist_ok=True)
            (dest / f"{pkg.name}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "records": records,
               "counts": {"total": len(records), "by_mode": dict(Counter(x["mode"] for x in records)), "archive_status": dict(Counter(x["archive"].get("chain_status") for x in records)), "applicability": dict(Counter(x["archive"].get("current_final_applicability") for x in records)), "declared_data_missing": sum(bool(x["declared_data_missing"]) for x in records), "high_risk_public_files": sum(bool(x["public_high_risk_files"]) for x in records), "missing_archive": sum(not x["archive"].get("exists") for x in records)}}
    (out / "reference_alignment_packets.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--repo", type=Path, default=Path(".")); ap.add_argument("--out", type=Path, default=Path("docs/verification/final_verified_tasks/reference_alignment_audit/packets")); args = ap.parse_args()
    print(json.dumps(build(args.repo.resolve(), args.out)["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
