#!/usr/bin/env python3
"""Offline verification using saved scientific artifacts and a protocol-only Judge.

Does not call a model, launch scientific jobs, or publish a scientific score.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import unquote, urlparse
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chemistry_toolbox.src.recovery_io import atomic_json
from evaluation.provenance.agent_events import event_capture_summary, load_agent_events
from evaluation.provenance.evidence_archive import build_run_index, export_run_archive, open_archive
from evaluation.provenance.trace import load_tool_trace
from evaluation.scoring.service import score_workspace


def protocol_judge(prompt):
    """Exercise retrieval and structurally valid scoring, with no scientific claim."""
    payload = json.loads(prompt)
    if not payload["followups"]:
        excerpts = payload["evidence"]["excerpts"]
        if isinstance(excerpts, dict):
            excerpts = excerpts.get("items", [])
        candidates = [e for e in excerpts if e["role"] == "agent_report" and e["ref"].endswith(".json")]
        reads = [{"ref": "index/jobs", "count": 2}]
        if candidates:
            reads.append({"ref": candidates[0]["ref"], "selector": "", "array_count": 2})
        return {"type": "evidence_request", "reads": reads}
    for followup in payload["followups"]:
        for evidence in followup.get("evidence", []):
            if evidence.get("error"):
                raise AssertionError("Saved evidence retrieval failed: " + evidence["error"])
    truth = payload["task_contract"]
    def item(spec, scientific=False):
        value = {"id": spec["id"], "score": 0, "max_score": spec["max_score"],
                 "rationale": "Protocol-only fixture; no scientific judgment was performed.",
                 "citations": [{"ref": "task/contract"}]}
        if scientific:
            value["evidence_status"] = "unsupported"
        return value
    mode = truth.get("evaluation_mode", "binary")
    verdict = {"score": 0, "rationale": "Protocol-only fixture; no scientific judgment was performed.",
               "citations": [{"ref": "task/contract"}], "simulated_judge": True,
               "rule_assessments": [{"rule_id": r["rule_id"], "assessment": "partial", "numeric_check": r["assessment"],
                                     "rationale": "Host check acknowledged for protocol verification."} for r in payload["rule_checks"]],
               "_judge_usage": {k: 0 for k in ("prompt_tokens", "completion_tokens", "total_tokens", "cached_input_tokens", "reasoning_output_tokens")}}
    if mode == "dual_axis_100":
        verdict.update(process_criteria=[item(r) for r in truth["scoring_rubric"]],
                       scientific_conclusions=[item(r, True) for r in truth["scientific_conclusion_rubric"]],
                       submission_validity="valid", research_process_score=0, scientific_conclusion_score=0)
    elif mode == "rubric_100":
        verdict["criteria"] = [item(r) for r in truth["scoring_rubric"]]
    return verdict


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--export", action="store_true", help="Also verify a portable copy with source reads forbidden")
    parser.add_argument("--existing-archive", type=Path, help="Verify an earlier export without duplicating scientific files")
    parser.add_argument("--budget", type=Path, help="Explicit ScoringBudget JSON for this verification version")
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    output = args.output_dir.resolve()
    if output.is_relative_to(workspace):
        parser.error("output must be outside the source workspace")
    output.mkdir(parents=True, exist_ok=False)
    budget = json.loads(args.budget.read_text()) if args.budget else None
    guarded = {p: p.read_bytes() for p in [workspace / "_meta.json", workspace / "_score.json", workspace / "_tool_trace.jsonl"] if p.is_file()}
    def forbidden(*args, **kwargs):
        raise AssertionError("Offline verification cannot call API or launch a process")
    with patch("subprocess.Popen", forbidden), patch("socket.create_connection", forbidden), patch("evaluation.scoring.service._default_judge_call", forbidden):
        index = build_run_index(workspace)
        result = score_workspace(workspace, output_dir=output / "score", evidence_index=index, judge_call=protocol_judge, publish=False, budget=budget)
        if result["status"] != "scored":
            atomic_json(output / "failure.json", result)
            raise AssertionError(result.get("error", result))
        resumed = score_workspace(workspace, output_dir=output / "score", judge_call=protocol_judge, publish=False, resume=True, budget=budget)
        assert resumed["score_id"] == result["score_id"]
        prepared = json.loads((output / "score/prepared.json").read_text())
        summary = {"verification": "passed", "scientific_judgment_performed": False, "api_calls": 0,
                   "jobs": len(index["jobs"]), "tool_calls": len(load_tool_trace(workspace)),
                   "agent_capture": event_capture_summary(load_agent_events(workspace)),
                   "rule_checks": prepared["rule_checks"], "coverage": result["evidence_coverage"],
                   "submission_status": result.get("submission_status"), "agent_declared_outcome": result.get("agent_declared_outcome"),
                   "resume_reused_version": True, "score_id": result["score_id"]}
        if args.export or args.existing_archive:
            archive_dir = args.existing_archive.resolve() if args.existing_archive else output / "archive"
            archive = open_archive(archive_dir) if args.existing_archive else export_run_archive(workspace, archive_dir, compress_logs=True)
            roots = [Path(value).resolve() for value in index["source_roots"].values()]
            guarded_source_reads = True
            def audit_source_access(event, arguments):
                if guarded_source_reads and event in {"open", "sqlite3.connect"} and isinstance(arguments[0], (str, bytes, os.PathLike)):
                    value = os.fsdecode(arguments[0])
                    path = Path(unquote(urlparse(value).path) if value.startswith("file:") else value).resolve()
                    if any(path.is_relative_to(root) for root in roots):
                        raise AssertionError("Portable replay tried to read an original source: " + str(path))
            sys.addaudithook(audit_source_access)
            try:
                portable = open_archive(archive_dir)
                target = archive_dir / "workspace"
                portable_result = score_workspace(target, output_dir=output / "portable_score", rules_root=archive_dir / "task_snapshot",
                    evidence_index=portable, judge_call=protocol_judge, publish=False, budget=budget)
                assert portable_result["status"] == "scored", portable_result
                saved = json.loads((output / "portable_score/rule_checks.json").read_text())
                assert saved == prepared["rule_checks"]
                assert len(load_tool_trace(target)) == summary["tool_calls"]
                assert event_capture_summary(load_agent_events(target)) == summary["agent_capture"]
            finally:
                guarded_source_reads = False
            summary["portable_archive"] = {"state": archive["verification"]["state"], "source_reads_forbidden": True,
                                            "files": archive["verification"]["file_count"]}
        assert all(path.read_bytes() == value for path, value in guarded.items())
        summary["source_records_unchanged"] = True
        atomic_json(output / "verification.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in {"coverage", "rule_checks"}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
