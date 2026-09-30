import json

import pytest

from evaluation.scoring.judging import ScoringBudget, ScoringStop, run_judge
from evaluation.scoring.policies import validate_judge_verdict
from evaluation.scoring.service import _reader, score_workspace
from test_task_package_v19 import package


def fixture_verdict(payload):
    truth = payload["task_contract"]
    def item(spec, scientific=False):
        value = {"id": spec["id"], "score": spec["max_score"] / 2, "max_score": spec["max_score"],
                 "rationale": "Offline protocol fixture, not a scientific judgment.", "citations": [{"ref": "task/contract"}]}
        if scientific:
            value["evidence_status"] = "partially_supported"
        return value
    return {"process_criteria": [item(r) for r in truth["scoring_rubric"]],
            "scientific_conclusions": [item(r, True) for r in truth["scientific_conclusion_rubric"]],
            "submission_validity": "valid", "rationale": "Offline protocol fixture.",
            "rule_assessments": [{"rule_id": r["rule_id"], "assessment": "partial",
                                  "numeric_check": r["assessment"], "rationale": "Acknowledged host check."} for r in payload["rule_checks"]],
            "_judge_usage": {"prompt_tokens": 20, "completion_tokens": 5, "total_tokens": 25}}


def setup_run(tmp_path):
    root = tmp_path / "run"
    (root / "report").mkdir(parents=True)
    package(tmp_path / "rules")
    (root / "_meta.json").write_text(json.dumps({"run_id": "run", "paper_id": "paper_fixture", "task_type": "autonomous_research", "status": "completed"}))
    (root / "report/report.md").write_text("Fixture report")
    (root / "report/results.json").write_text('{"barrier":12.3,"conclusion":"path A"}')
    return root


def test_full_service_reads_then_scores_without_source_mutation(tmp_path):
    root = setup_run(tmp_path)
    before = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    calls = []
    def judge(prompt):
        value = json.loads(prompt)
        calls.append(value)
        if not value["followups"]:
            return {"type": "evidence_request", "reads": [{"ref": "workspace/report/results.json", "selector": "/barrier"}]}
        assert value["followups"][0]["evidence"][0]["value"] == 12.3
        return fixture_verdict(value)
    out = tmp_path / "score"
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, output_dir=out, publish=False)
    assert result["status"] == "scored", result
    assert result["score"] == 25
    assert result["judge_usage"]["request_count"] == 2
    assert result["judge_usage"]["prompt_tokens"] is None
    assert {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()} == before
    resumed = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, output_dir=out, publish=False, resume=True)
    assert resumed["score_id"] == result["score_id"] and len(calls) == 2


@pytest.mark.parametrize("ref", ["index/jobs", "index/files"])
def test_index_citations_finish_scoring_and_replay_saved_response(tmp_path, monkeypatch, ref):
    from evaluation.scoring import service
    root, calls = setup_run(tmp_path), []
    directory = tmp_path / "score"
    def judge(prompt):
        calls.append(prompt)
        verdict = fixture_verdict(json.loads(prompt))
        verdict["process_criteria"][0]["citations"] = [{"ref": ref}]
        return verdict
    # Crash after transport: recovery must validate the genuine saved response,
    # publish in the same workspace, and never make another provider request.
    validate = service.validate_judge_verdict
    def crash(*args, **kwargs):
        raise KeyboardInterrupt()
    monkeypatch.setattr(service, "validate_judge_verdict", crash)
    with pytest.raises(KeyboardInterrupt):
        score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, output_dir=directory)
    monkeypatch.setattr(service, "validate_judge_verdict", validate)
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, output_dir=directory, resume=True)
    assert result["status"] == "scored", result
    assert len(calls) == 1
    assert result["scoring_directory"] == str(directory)
    assert json.loads((root / "_score.json").read_text())["score_id"] == result["score_id"]

    # A previously published version can have stale accounting after a validator
    # fix. Cached publication must use the complete, unchanged request journal.
    response = json.loads((directory / 'requests/0001.response.json').read_text())
    (directory / 'requests/0002.response.json').write_text(json.dumps(response))
    cached = score_workspace(root, rules_root=tmp_path / 'rules', judge_call=judge, output_dir=directory, resume=True)
    assert cached['judge_usage']['request_count'] == 2
    assert cached['judge_usage']['total_tokens'] == result['judge_usage']['total_tokens'] * 2
    assert len(calls) == 1


@pytest.mark.parametrize("citation", [{"ref": "index/invented"}, {"ref": "index/jobs", "selector": "/invented"}])
def test_invalid_index_citations_still_fail(tmp_path, citation):
    root = setup_run(tmp_path)
    def judge(prompt):
        verdict = fixture_verdict(json.loads(prompt))
        verdict["process_criteria"][0]["citations"] = [citation]
        return verdict
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, output_dir=tmp_path / "score")
    assert result["status"] == "judge_error"
    assert not (root / "_score.json").exists()


def test_raw_usage_survives_bad_json_and_all_early_exits_persist(tmp_path):
    root = setup_run(tmp_path)
    def judge(prompt):
        return {"raw_text": "{truncated", "_judge_usage": {"prompt_tokens": 7, "completion_tokens": 3, "total_tokens": 10}}
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, output_dir=tmp_path / "bad", publish=False)
    assert result["status"] == "judge_error"
    assert result["judge_usage"]["total_tokens"] == 20
    assert json.loads((tmp_path / "bad/requests/0001.response.json").read_text())["raw_text"] == "{truncated"
    no_calls = lambda prompt: pytest.fail("budget must block before API")
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=no_calls, output_dir=tmp_path / "budget", publish=False,
                             budget={"request_max_chars": 100})
    assert result["status"] == "needs_review" and result["judge_usage"]["request_count"] == 0
    assert (tmp_path / "budget/state.json").is_file() and (tmp_path / "budget/verdict.json").is_file()


def test_resume_saved_response_and_cached_reads_does_not_repeat_call(tmp_path):
    calls, reads = [], []
    def call(*args):
        calls.append(1)
        return {"type": "evidence_request", "reads": [{"ref": "r"}]} if len(calls) == 1 else {"answer": 1}
    def read(request):
        reads.append(1)
        return {"ref": "r", "content": "saved"}
    def crash(value):
        raise KeyboardInterrupt()
    with pytest.raises(KeyboardInterrupt):
        run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=call, read=read, validate=crash)
    result = run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=lambda *a: pytest.fail("already saved"),
                       read=lambda r: pytest.fail("already read"), validate=lambda v: v, resume=True)
    assert result["answer"] == 1 and len(calls) == 2 and len(reads) == 1


def test_replay_early_verdict_retains_usage_of_later_historical_requests(tmp_path):
    calls = []
    def call(*args):
        calls.append(1)
        return {"answer": 1, "_judge_usage": {"prompt_tokens": 10, "completion_tokens": 3, "total_tokens": 13}}
    def reject(value):
        raise ValueError('old validation defect')
    with pytest.raises(ScoringStop, match='old validation defect'):
        run_judge(tmp_path, {}, 'system', budget=ScoringBudget(), call=call, read=lambda r: {}, validate=reject)
    assert len(calls) == 2
    result = run_judge(tmp_path, {}, 'system', budget=ScoringBudget(), call=lambda *a: pytest.fail('must replay'),
                       read=lambda r: {}, validate=lambda v: None, resume=True)
    assert result['_judge_usage']['request_count'] == 2
    assert result['_judge_usage']['total_tokens'] == 26
    assert json.loads((tmp_path / 'state.json').read_text())['judge_usage'] == result['_judge_usage']


def test_in_doubt_does_not_automatically_reissue(tmp_path):
    def call(*args):
        raise TimeoutError("response lost")
    with pytest.raises(ScoringStop) as stopped:
        run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=call, read=lambda r: {}, validate=lambda v: v)
    assert stopped.value.status == "in_doubt"
    with pytest.raises(ScoringStop):
        run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=lambda *a: pytest.fail("no implicit retry"),
                  read=lambda r: {}, validate=lambda v: v, resume=True)
    result = run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=lambda *a: {"answer": 1},
                       read=lambda r: {}, validate=lambda v: v, resume=True, retry_in_doubt=True)
    assert result["_judge_usage"]["request_count"] == 2 and result["_judge_usage"]["total_tokens"] is None


@pytest.mark.parametrize("mode", ["binary", "rubric_100", "dual_axis_100"])
def test_mode_specific_validation(mode):
    truth = {"evaluation_mode": mode, "scoring_rubric": [{"id": "p", "max_score": 100}],
             "scientific_conclusion_rubric": [{"id": "s", "max_score": 100}]}
    item = {"id": "p", "score": 50, "rationale": "reason", "citations": [{"ref": "task/contract"}]}
    verdict = {"score": 1, "rationale": "reason", "citations": item["citations"]} if mode == "binary" else (
        {"score": 50, "criteria": [item], "rationale": "reason"} if mode == "rubric_100" else
        {"process_criteria": [item], "scientific_conclusions": [{**item, "id": "s", "evidence_status": "supported"}],
         "submission_validity": "valid", "rationale": "reason"})
    validate_judge_verdict(verdict, truth, citation_check=lambda c: None)
    verdict["extra_future_metadata"] = {}
    validate_judge_verdict(verdict, truth, citation_check=lambda c: None)
    if mode == "binary":
        verdict["score"] = float("nan")
    elif mode == "rubric_100":
        verdict["criteria"] = []
    else:
        verdict["submission_validity"] = "unknown-new-value"
    with pytest.raises(ValueError):
        validate_judge_verdict(verdict, truth, citation_check=lambda c: None)


def test_infrastructure_failure_resumes_with_one_explicit_attempt(tmp_path):
    def fail(*args):
        raise RuntimeError("quota unavailable")
    with pytest.raises(ScoringStop) as stopped:
        run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=fail, read=lambda r: {}, validate=lambda v: None)
    assert stopped.value.status == "suspended_infrastructure"
    result = run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=lambda *a: {"answer": 1},
                       read=lambda r: {}, validate=lambda v: None, resume=True)
    assert result["_judge_usage"]["request_count"] == 2
    assert result["_judge_usage"]["total_tokens"] is None


@pytest.mark.parametrize("limit", ["total_input_tokens", "total_output_tokens", "total_request_max_chars", "context_window_tokens"])
def test_each_cumulative_budget_and_context_reserve_stops_before_transport(tmp_path, limit):
    with pytest.raises(ScoringStop, match="budget_exhausted"):
        run_judge(tmp_path, {"rules": "long context" * 100}, "system", budget=ScoringBudget(**{limit: 1}),
                  call=lambda *a: pytest.fail("budget must be reserved before transport"), validate=lambda v: None, read=lambda r: {})


def test_unresolved_scientific_evidence_remains_needs_review(tmp_path):
    root = setup_run(tmp_path)
    def judge(prompt):
        value = fixture_verdict(json.loads(prompt))
        value["rule_assessments"][0]["assessment"] = "unresolved"
        value["unresolved_disposition"] = "needs_review"
        value["unresolved_rationale"] = "The fixture evaluator cannot read essential evidence."
        return value
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, output_dir=tmp_path / "score")
    assert result["status"] == "needs_review" and result["score"] is None
    assert result["judge_usage"]["request_count"] == 1
    assert not (root / "_score.json").exists()


@pytest.mark.parametrize("expected", ["pass", "fail"])
@pytest.mark.parametrize("structured", [False, True])
def test_numeric_acknowledgment_preserves_matching_response(expected, structured):
    acknowledgment = {"assessment": expected, "observed": 4.2} if structured else expected
    verdict = {"score": 1, "rationale": "reason", "citations": [{"ref": "task/contract"}],
               "rule_assessments": [{"rule_id": "energy", "assessment": "partial", "rationale": "Review provenance separately.",
                                     "numeric_check": acknowledgment}]}
    original = json.dumps(verdict)
    validate_judge_verdict(verdict, {"evaluation_mode": "binary"}, citation_check=lambda c: None,
                           rules=[{"rule_id": "energy", "assessment": expected}])
    assert json.dumps(verdict) == original


@pytest.mark.parametrize("reported", [None, True, [], "pass", {}, {"assessment": "pass"}, {"status": "fail"}])
def test_missing_or_conflicting_numeric_acknowledgment_is_actionable(reported):
    verdict = {"score": 0, "rationale": "reason", "citations": [{"ref": "task/contract"}],
               "rule_assessments": [{"rule_id": "energy", "assessment": "fail", "rationale": "reason", "numeric_check": reported}]}
    with pytest.raises(ValueError, match="Rule 'energy': numeric_check must be 'fail'"):
        validate_judge_verdict(verdict, {"evaluation_mode": "binary"}, citation_check=lambda c: None,
                               rules=[{"rule_id": "energy", "assessment": "fail"}])


@pytest.fixture
def virtual_reader():
    return _reader({"index": {"files": [], "jobs": []},
                    "truth": {"rule_table": [{"rule_id": "energy", "rule": {"type": "numeric"}}]},
                    "payload": {"task_contract": {"evaluation_mode": "binary"}},
                    "tools": [{"sequence": 1, "status": "failed"}],
                    "agent_events": [{"sequence": 2, "kind": "native_tool"}, {"sequence": 3, "kind": "model_turn"}],
                    "rule_checks": [{"rule_id": "energy", "assessment": "missing_value"}]})


@pytest.mark.parametrize("ref", ["task/contract", "task/rules", "event/tool/1", "event/native/2", "absence/energy", "index/jobs", "index/files"])
def test_virtual_references_never_silently_ignore_selectors(virtual_reader, ref):
    assert virtual_reader({"ref": ref})["ref"] == ref
    for selector in ("/invented/field", "$.absent", "$"):
        with pytest.raises(ValueError, match="JSON Pointer|JSONPath"):
            virtual_reader({"ref": ref, "selector": selector})


def test_virtual_reference_identities_are_checked(virtual_reader):
    assert virtual_reader({"ref": "task/rules", "rule_id": "energy"})["items"][0]["rule_id"] == "energy"
    for request in ({"ref": "task/rules", "rule_id": "invented"}, {"ref": "absence/invented"},
                    {"ref": "event/tool/999"}, {"ref": "event/native/3"}):
        with pytest.raises(ValueError):
            virtual_reader(request)


@pytest.mark.parametrize("defect", ["numeric_check", "virtual_selector", "unknown_rule"])
def test_one_format_repair_corrects_contract_and_persists_original(tmp_path, defect):
    root, calls = setup_run(tmp_path), []
    def judge(prompt):
        payload = json.loads(prompt)
        value = fixture_verdict(payload)
        calls.append(payload)
        if len(calls) == 1:
            if defect == "numeric_check":
                del value["rule_assessments"][0]["numeric_check"]
            else:
                value["process_criteria"][0]["citations"] = [{"ref": "task/rules", **(
                    {"selector": "/invented/field"} if defect == "virtual_selector" else {"rule_id": "invented"})}]
        else:
            diagnostic = payload["followups"][0]["format_error"]
            assert {"numeric_check": "Rule 'rule1': numeric_check must be 'pass'",
                    "virtual_selector": "omit selector", "unknown_rule": "Unknown authored rule"}[defect] in diagnostic
            value["rule_assessments"][0]["numeric_check"] = {"assessment": "pass", "observed": 12.3}
            value["process_criteria"][0]["citations"] = [{"ref": "task/rules", "rule_id": "rule1"},
                {"ref": "workspace/report/results.json", "selector": "/barrier"}]
        return value
    directory = tmp_path / "score"
    result = score_workspace(root, rules_root=tmp_path / "rules", output_dir=directory, judge_call=judge, publish=False)
    assert result["status"] == "scored", result
    assert len(calls) == result["judge_usage"]["request_count"] == 2
    assert result["judge_usage"]["total_tokens"] == 50
    assert result["rule_assessments"][0]["numeric_check"] == {"assessment": "pass", "observed": 12.3}
    assert (directory / "requests/0001.response.json").is_file()
    assert not (root / "_score.json").exists()
    resumed = score_workspace(root, rules_root=tmp_path / "rules", output_dir=directory, judge_call=judge, publish=False, resume=True)
    assert resumed["score_id"] == result["score_id"] and len(calls) == 2
