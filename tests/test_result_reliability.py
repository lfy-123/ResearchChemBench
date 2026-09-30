"""Cross-task regressions for saved-output evaluation; no scientific jobs/API."""
import json
import os
from pathlib import Path

import pytest

from chemistry_toolbox.src.output_contract import validate_output_contract
from evaluation.scoring.packing import pack_prompt, record_page, encoded
from evaluation.scoring.judging import ScoringBudget, run_judge
from evaluation.scoring.service import score_workspace
from evaluation.contracts.scientific_rubric import scientific_rubric
from test_judging import setup_run, fixture_verdict


@pytest.mark.parametrize("paper", ["paper_new", "paper_unrelated"])
def test_directories_and_blank_reports_use_declared_format(tmp_path, paper):
    root = tmp_path / paper
    (root / "report/structures").mkdir(parents=True)
    (root / "report/report.md").write_text(" \n")
    contract = json.dumps({"required_files": ["report", {"path": "report/structures", "allow_empty": True}],
                           "report_file": "report/report.md"}).encode()
    value = validate_output_contract(root, contract)
    assert [e["file"] for e in value["errors"]] == ["report/report.md"]
    (root / "report/report.md").write_text("The scientific goal was not achieved.")
    assert validate_output_contract(root, contract)["valid"]


def test_packing_preserves_rules_and_all_requested_pages(tmp_path):
    payload = {"authored_rule_table": [{"rule_id": "required"}], "rule_checks": [{"assessment": "fail"}],
               "evidence": {"excerpts": [{"ref": f"r{i}", "content": '\\"\u03b1' * 1000} for i in range(100)]}}
    calls = []
    def call(prompt, system, maximum):
        v = json.loads(prompt)
        calls.append(v)
        assert v["authored_rule_table"] == payload["authored_rule_table"]
        assert v["rule_checks"] == payload["rule_checks"]
        if len(calls) == 1:
            assert v["evidence"]["excerpts"]["read"]["pointer"] == "/evidence/excerpts"
            return {"type": "evidence_request", "reads": [{"ref": "review/payload", "pointer": "/evidence/excerpts/99/content", "max_chars": 800}]}
        assert v["followups"][0]["evidence"][0]["value"]
        return {"done": True}
    run_judge(tmp_path, payload, "system", budget=ScoringBudget(request_max_chars=3500, max_read_chars=800),
              call=call, read=lambda r: record_page(payload, r), validate=lambda v: None)
    for p in (tmp_path / "requests").glob("*.request.json"):
        assert json.loads(p.read_text())["input_characters"] <= 3500
    assert len(payload["evidence"]["excerpts"]) == 100


def test_single_huge_host_record_can_be_read_to_end():
    value = [{"metadata": {"blob": "z" * 20000}, "state": "failed"}]
    request = {"ref": "index/jobs", "count": 1, "max_chars": 700}
    page = record_page(value, request)
    assert len(json.dumps(page, ensure_ascii=False)) <= 700
    pointer = page["value"][0]["read"]["pointer"]
    assert pointer == "/0"
    request = {"ref": "index/jobs", "pointer": "/0/metadata/blob", "max_chars": 700}
    parts = []
    while request:
        page = record_page(value, request)
        assert len(json.dumps(page, ensure_ascii=False)) <= 700
        parts.append(page["value"])
        request = page.get("next")
    assert "".join(parts) == value[0]["metadata"]["blob"]
    with pytest.raises(ValueError):
        record_page(value, {"ref": "index/jobs", "pointer": "/999"})


def test_recovery_uses_saved_prompt_even_if_default_system_changes(tmp_path):
    def crash(v):
        raise KeyboardInterrupt()
    with pytest.raises(KeyboardInterrupt):
        run_judge(tmp_path, {"version": "old"}, "old system", budget=ScoringBudget(),
                  call=lambda *a: {"done": True}, validate=crash, read=lambda r: {})
    original = (tmp_path / "requests/0001.request.json").read_bytes()
    run_judge(tmp_path, {"version": "new"}, "new system", budget=ScoringBudget(),
              call=lambda *a: pytest.fail("persisted response must be replayed"), validate=lambda v: None,
              read=lambda r: {}, resume=True)
    assert (tmp_path / "requests/0001.request.json").read_bytes() == original


def test_judge_can_explain_optional_unresolved_rule_without_global_block(tmp_path):
    root = setup_run(tmp_path)
    def judge(prompt):
        verdict = fixture_verdict(json.loads(prompt))
        verdict["rule_assessments"][0]["assessment"] = "unresolved"
        verdict.update(unresolved_disposition="scorable", unresolved_rationale="An optional alternative is unused; the supported route can be scored.")
        return verdict
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, publish=False)
    assert result["status"] == "scored", result
    assert result["scoring_version"]["judge_protocol_version"] == 3


@pytest.mark.parametrize("maximum", [float("nan"), float("inf"), -1, True])
def test_flat_rubric_rejects_bad_weights(maximum):
    with pytest.raises(ValueError):
        scientific_rubric({"rules": [{"rule_id": "r"}], "scientific_rubric": [
            {"id": "target", "max_score": maximum, "description": "Goal", "rule_ids": ["r"]}]})


def test_multiline_diagnostic_preserves_native_frame_and_log_paths(tmp_path):
    from chemistry_toolbox.mcp.open_execution import _program_failure_diagnostic
    from chemistry_toolbox.src.execution_feedback import execution_feedback
    (tmp_path / "analysis.py").write_text("import thirdparty\nthirdparty.run()\n")
    (tmp_path / "stderr.log").write_text('Traceback (most recent call last):\n  File "analysis.py", line 2, in <module>\n    thirdparty.run()\n  File "/opt/thirdparty/reader.py", line 20, in parse\n    raise MsgError()\ntheodore.error_handler.MsgError:\n\n ERROR: The file cannot be parsed by cclib\n')
    status = {"job_type": "programmable_analysis", "status": "failed", "job_id": "fixture", "return_code": 1}
    diagnostic = _program_failure_diagnostic(tmp_path, status)
    view = execution_feedback(status=status, program_diagnostic=diagnostic)["diagnostic"]
    assert "cannot be parsed" in view["message"]
    assert view["source_line"] == 2 and view["failure_location"]["line"] == 20
    assert view["diagnostic_ref"] and view["log_paths"]


def test_activity_is_observational_and_missing_pid_is_unknown():
    from chemistry_toolbox.src.process_activity import process_activity
    value = process_activity(os.getpid())
    assert value["coverage"] == "leader_only" and value["cpu_seconds"] >= 0
    missing = process_activity(999999999)
    assert missing["status"] == "unknown" and missing["cpu_seconds"] is None


def test_revalidate_requires_recorded_normal_completion_and_is_idempotent(tmp_path):
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    from evaluation.execution.control import revalidate
    from evaluation.execution.recovery import RunRecoveryError
    root = tmp_path / "run"
    (root / "report").mkdir(parents=True)
    (root / "report/report.md").write_text("Recorded scientific result")
    payload = '{"required_files":["report"],"report_file":"report/report.md"}'
    (root / "submission_schema.json").write_text(payload)
    store = ExecutionStore(root, run_id="run")
    task = store.directory / "task_snapshot/autonomous_research/paper_fixture"
    task.mkdir(parents=True)
    store.put_record("frozen", "output_contract", {"text": payload})
    store.put_record("run", "manifest", {"run_state": "failed", "run_id": "run"})
    meta = {"run_id": "run", "status": "failed", "paper_id": "paper_fixture", "task_type": "autonomous_research",
            "exit_code": 0, "termination": "agent_completed", "report_exists": True,
            "execution_reconciliation": {"status": "success", "summary": {"active": 0, "needs_reconciliation": 0}}}
    path = root / "_meta.json"
    path.write_text(json.dumps(meta))
    before = path.read_bytes()
    assert revalidate(root)["valid"] and path.read_bytes() == before
    path.write_text(json.dumps({**meta, "termination": "cancelled"}))
    with pytest.raises(RunRecoveryError):
        revalidate(root, apply=True)
    path.write_text(json.dumps(meta))
    assert revalidate(root, apply=True)["applied"]
    assert revalidate(root, apply=True)["applied"]
    assert store.get_record("repair", "submission_validation")["before_meta"]["status"] == "failed"
    assert store.records("attempt") == {} and store.list_jobs() == []


def test_flat_weights_reuse_existing_scientific_axis(tmp_path):
    from evaluation.scoring.adapters import _runtime_contract
    from test_task_package_v19 import package
    root = package(tmp_path / "rules")
    reference = {p.name: json.loads(p.read_text()) for p in (root / "evaluation").glob("*.json")}
    rules = reference["scoring_rules.json"]
    rules["scientific_rubric"] = [{"id": "goal", "max_score": 70, "description": "Target achievement", "rule_ids": [rules["rules"][0]["rule_id"]]},
                                {"id": "interpretation", "max_score": 30, "description": "Evidence-supported interpretation", "rule_ids": [rules["rules"][-1]["rule_id"]]}]
    truth = _runtime_contract(task_type="autonomous_research", reference=reference,
                              submission=json.loads((root / "agent_input/submission_schema.json").read_text()))
    assert [(r["id"], r["max_score"]) for r in truth["scientific_conclusion_rubric"]] == [("goal", 70), ("interpretation", 30)]


def test_invalid_citation_feedback_identifies_reference_and_selector():
    from evaluation.scoring.policies import validate_judge_verdict
    def check(citation):
        raise ValueError("JSON Pointer does not exist")
    value = {"score": 1, "rationale": "Evidence", "citations": [{"ref": "workspace/report/a.json", "selector": "/missing"}]}
    with pytest.raises(ValueError) as error:
        validate_judge_verdict(value, {"evaluation_mode": "binary"}, citation_check=check)
    assert "workspace/report/a.json" in str(error.value)
    assert "/missing" in str(error.value)
    assert "Preserve other valid citations" in str(error.value)
