"""Independent structural read-back for authored upgrade packages.

This validates packages, runtime adaptation, export boundaries, paired modes,
reference-stage disclosures and source integrity. It is not scientific reference
validation and does not run a chemistry engine or an LLM judge.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import jsonschema
from evaluation.contracts.task_package import EVALUATION_FILES, validate_task_package
from evaluation.repository import TaskRepository, materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from chemistry_toolbox.src.output_contract import validate_output_contract

DEST = ROOT / "tasks/upgrade_tasks"
COORD = DEST / "coordination_20260927"
SPEC = ROOT / "docs/evalution/update/upgrade_guidance_review_manifest_20260927.json"
MODES = ("autonomous_research", "paper_reproduction")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def artifact_path_failures(schema):
    """Probe explicit workspace-artifact patterns against directory escape."""
    failures = []
    probes = ("outputs/../evaluation/hidden.json", "outputs/sub/../../hidden.json",
              "report/../hidden.json", "analysis/../hidden.json",
              "structures/../hidden.xyz")

    def visit(node, location):
        if isinstance(node, dict):
            pattern = node.get("pattern")
            if isinstance(pattern, str) and any(x in pattern for x in ("outputs", "report", "analysis", "structures")):
                for value in probes:
                    if re.search(pattern, value):
                        failures.append({"schema_location": location, "accepted_invalid_path": value, "pattern": pattern})
            for key, value in node.items():
                visit(value, location + "/" + str(key))
        elif isinstance(node, list):
            for i, value in enumerate(node):
                visit(value, location + "/" + str(i))
    visit(schema, "")
    return failures


def inspect(pids, check_sources=False):
    results = []
    details = []

    def check(name, passed, detail=None):
        row = {"test": name, "passed": bool(passed)}
        if detail is not None:
            row["detail"] = detail
        results.append(row)

    for pid in pids:
        pair = {mode: DEST / mode / pid for mode in MODES}
        info = {"paper_id": pid, "modes": {}}
        for mode, package in pair.items():
            prefix = f"{pid}:{mode}:"
            try:
                v = validate_task_package(package)
                check(prefix + "official_package_validation", v.status == "passed", v.findings)
                if v.status != "passed":
                    continue
                # Explicit package scope keeps this checker useful during
                # concurrent development without loading half-written peers.
                repo = TaskRepository.__new__(TaskRepository)
                repo.roots = (DEST,)
                repo._approved_final_directories = (package,)
                repo._index = repo._build_index()
                runtime = load_runtime_evaluation(paper_id=pid, task_type=mode, repository=repo)
                rubric = runtime.ground_truth["scientific_conclusion_rubric"]
                check(prefix + "scientific_weights_100", abs(sum(x["max_score"] for x in rubric) - 100) < 1e-8)
                contract = read(package / "agent_input/submission_schema.json")
                schema = contract["result_schema"]
                jsonschema.validators.validator_for(schema).check_schema(schema)
                check(prefix + "valid_json_schema", True)
                path_failures = artifact_path_failures(schema)
                check(prefix + "artifact_paths_no_traversal", not path_failures, path_failures)
                required = {x["path"] if isinstance(x, dict) else x for x in contract["required_files"]}
                check(prefix + "machine_and_readable_results", {"report/results.json", "report/report.md"} <= required)
                # Minimal negative controls use the real runtime contract. They
                # cannot establish calibrated scientific scoring, but prevent
                # a structurally empty or legacy scalar submission from passing.
                with tempfile.TemporaryDirectory(prefix="upgrade_parent_negative_") as tmp:
                    work = Path(tmp)
                    (work / "report").mkdir()
                    (work / "report/report.md").write_text("Synthetic format negative control, not scientific evidence.\n")
                    for label, value in (("empty_submission", {}), ("empty_complete_results", {"status": "complete", "results": {}}), ("legacy_scalar_only", {"status": "complete", "result": 1.23, "conclusion": "Old scalar only"})):
                        (work / "report/results.json").write_text(json.dumps(value))
                        result = validate_output_contract(work, json.dumps(contract).encode())
                        check(prefix + label + "_rejected", not result["valid"])
                with tempfile.TemporaryDirectory(prefix="upgrade_parent_export_") as tmp:
                    materialize_agent_files(paper_id=pid, task_type=mode, destination=tmp, repository=repo)
                    actual = {str(p.relative_to(tmp)): sha(p) for p in Path(tmp).rglob("*") if p.is_file()}
                    expected = {str(p.relative_to(package / "agent_input")): sha(p) for p in (package / "agent_input").rglob("*") if p.is_file()}
                    check(prefix + "exact_public_export", actual == expected)
                    check(prefix + "private_files_not_exported", not any("evaluation/" in p or p.endswith((".snapshot", ".pdf")) for p in actual))
                audit_path = package / "evaluation/task_provenance/upgrade_audit.json"
                check(prefix + "upgrade_audit_exists", audit_path.is_file())
                audit = read(audit_path) if audit_path.is_file() else {}
                status = str(audit.get("status", ""))
                check(prefix + "reference_stage_not_claimed_verified", bool(status) and ("pending" in status or "blocked" in status))
                check(prefix + "reference_plan_exists", (package / "evaluation/reference_validation_plan.md").is_file())
                snapshots = audit.get("source_payload_snapshots", {})
                if snapshots:
                    bad = [name for name, rec in snapshots.items() if not (package / rec["snapshot"]).is_file() or sha(package / rec["snapshot"]) != rec["sha256"]]
                    check(prefix + "source_snapshot_hashes", not bad, bad)
                source = ROOT / f"tasks/final_verified_{mode}" / pid
                for name in ("agent_input/task.md", "agent_input/submission_schema.json", "evaluation/reference_key_points.json", "evaluation/reference_conclusions.json", "evaluation/scoring_rules.json"):
                    check(prefix + "expanded_from_final:" + name, (package / name).read_bytes() != (source / name).read_bytes())
                task = (package / "agent_input/task.md").read_text()
                check(prefix + "author_guidance_boundary", ("# Author-provided scientific guidance" in task) == (mode == "paper_reproduction"))
                info["modes"][mode] = {
                    "status": status,
                    "package_hash": read(package / "package_manifest.json")["package_content_sha256"],
                    "key_points": len(read(package / "evaluation/reference_key_points.json")["items"]),
                    "conclusions": len(read(package / "evaluation/reference_conclusions.json")["items"]),
                    "rules": len(read(package / "evaluation/scoring_rules.json")["rules"]),
                    "new_scientific_calculations_performed": audit.get("new_scientific_calculations_performed"),
                }
            except Exception as exc:
                check(prefix + "exception", False, repr(exc))
        if len(info["modes"]) == 2:
            ar, pr = pair[MODES[0]], pair[MODES[1]]
            a = {str(p.relative_to(ar / "agent_input")): sha(p) for p in (ar / "agent_input").rglob("*") if p.is_file() and p.relative_to(ar / "agent_input").as_posix() != "task.md"}
            b = {str(p.relative_to(pr / "agent_input")): sha(p) for p in (pr / "agent_input").rglob("*") if p.is_file() and p.relative_to(pr / "agent_input").as_posix() != "task.md"}
            mismatch = sorted(k for k in a.keys() | b.keys() if a.get(k) != b.get(k))
            check(pid + ":paired_public_data_and_contract", not mismatch, mismatch)
            for name in EVALUATION_FILES:
                check(pid + ":paired_scientific_evaluator:" + name, (ar / "evaluation" / name).read_bytes() == (pr / "evaluation" / name).read_bytes())
        details.append(info)
    if check_sources:
        baseline = read(COORD / "source_integrity_before.json")
        original = baseline["sha256"]
        changed = [p for p, digest in original.items() if not (ROOT / p).is_file() or sha(ROOT / p) != digest]
        now = {str(p.relative_to(ROOT)) for rel in baseline["roots"] for p in (ROOT / rel).rglob("*") if p.is_file()}
        check("protected_sources_unchanged", not changed, changed)
        check("no_added_protected_source_files", not (now - original.keys()), sorted(now - original.keys()))
    failures = [x for x in results if not x["passed"]]
    return {"status": "passed" if not failures else "failed", "papers": len(pids), "checks": len(results), "failure_count": len(failures), "scientific_reference_validation": False, "LLM_judge_run": False, "packages": details, "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, action="append")
    parser.add_argument("--paper", action="append")
    parser.add_argument("--sources", action="store_true")
    parser.add_argument("--output", type=Path, default=COORD / "parent_validation_report.json")
    args = parser.parse_args()
    records = read(SPEC)["records"]
    pids = args.paper or [r["paper_id"] for r in records if not args.batch or r["batch"] in args.batch]
    report = inspect(pids, args.sources)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in {"packages", "results"}}, ensure_ascii=False))
    failures = [r for r in report["results"] if not r["passed"]]
    print(json.dumps([{"test": r["test"], "detail": str(r.get("detail", ""))[:700]} for r in failures[:20]], ensure_ascii=False))
    if len(failures) > 20:
        print(f"{len(failures) - 20} further failures are recorded in {args.output}")
    sys.exit(bool(report["failure_count"]))
