"""Protocol recovery with synthetic evidence; no model or chemistry execution."""
import json
from types import SimpleNamespace

import pytest

from evaluation.provenance.evidence_archive import build_run_index
from evaluation.scoring.evidence_reading import read_registered_evidence, normalize_selection
from evaluation.scoring.judging import ScoringBudget, ScoringStop, run_judge
from evaluation.scoring.packing import record_page
from evaluation.scoring.policies import _parse_judge_json, parse_judge_response, validate_judge_verdict, JudgeContractError
from evaluation.scoring.service import _reader, score_workspace
from test_judging import setup_run, fixture_verdict
from test_resume_reliability import make_runner


@pytest.mark.parametrize("field", ["pointer", "selector"])
@pytest.mark.parametrize("pointer,expected", [("", {"": 4, "a/b": {"~key": [2, 3]}}), ("/", 4), ("/a~1b/~0key/1", 3)])
def test_common_location_for_files_and_records(tmp_path, field, pointer, expected):
    root = setup_run(tmp_path)
    value = {"": 4, "a/b": {"~key": [2, 3]}}
    (root / "report/results.json").write_text(json.dumps(value))
    index = build_run_index(root)
    file = read_registered_evidence(index, {"ref": "workspace/report/results.json", field: pointer})
    host = record_page(value, {"ref": "review/payload", field: pointer})
    assert file["value"] == host["value"] == expected
    assert read_registered_evidence(index, {"ref": file["ref"], "pointer": file["pointer"]})["value"] == expected


@pytest.mark.parametrize("location", [{"pointer": "/a", "selector": "/b"}, {"pointer": None}, {"selector": 3},
                                      {"pointer": "$.a"}, {"pointer": "/a~2"}])
def test_ambiguous_or_invalid_location_rejected(location):
    with pytest.raises(ValueError):
        normalize_selection(location)


def test_missing_file_pointer_is_not_accepted_and_all_errors_are_reported(tmp_path):
    root = setup_run(tmp_path)
    def judge(prompt):
        value = fixture_verdict(json.loads(prompt))
        value["scientific_conclusions"][0]["citations"] = [{"ref": "workspace/report/results.json", "pointer": "/invented"}]
        value["process_criteria"][0]["citations"] = []
        return value
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, publish=False)
    assert result["status"] == "judge_error"
    assert "/scientific_conclusions/0/citations/0" in result["error"]
    assert "/process_criteria/0/citations" in result["error"]
    assert "available_keys" in result["error"] and "barrier" in result["error"]
    assert result["judge_usage"]["request_count"] == 2  # Identical replies stop without a third call.


def test_host_alias_is_resolved_and_conflict_is_not_ignored():
    read = _reader({"index": {}, "payload": {"metrics": {"jobs": 3}}})
    assert read({"ref": "review/payload", "selector": "/metrics/jobs"})["value"] == 3
    with pytest.raises(ValueError, match="conflict"):
        read({"ref": "review/payload", "selector": "/metrics", "pointer": "/missing"})


READ = {"type": "evidence_request", "reads": [{"ref": "review/payload", "pointer": "/x"}]}


@pytest.mark.parametrize("raw", [json.dumps(READ) + '{"score":1}', '{"type":"evidence_request","type":"verdict"}',
                                 json.dumps(READ) + "garbage", '{"score": NaN}', json.dumps(READ) * 9,
                                 '{"score":1}{"score":1}', '{"type":"evidence_request","reads":[]}' * 2])
def test_parser_does_not_choose_or_invent_an_answer(raw):
    with pytest.raises(ValueError):
        _parse_judge_json(raw, allow_duplicate_reads=True)


def test_duplicate_reads_execute_once_and_replay_without_a_model_call(tmp_path):
    calls, reads = [], []
    def call(prompt, system, maximum):
        calls.append(prompt)
        if len(calls) == 1:
            return {"raw_text": json.dumps(READ) * 2}
        assert json.loads(prompt)["followups"][0]["evidence"] == [{"value": 7}]
        return {"done": True}
    def read(item):
        reads.append(item)
        return {"value": 7}
    kwargs = dict(budget=ScoringBudget(), config={"judge_model": "fixture", "judge_protocol_version": 3},
                  read=read, validate=lambda v: None)
    run_judge(tmp_path, {}, "system", call=call, **kwargs)
    assert len(reads) == 1 and len(calls) == 2
    saved = (tmp_path / "requests/0001.response.json").read_bytes()
    assert json.loads((tmp_path / "requests/0001.interpretation.json").read_text())["duplicate_evidence_requests"] == 2
    run_judge(tmp_path, {}, "new system", call=lambda *a: pytest.fail("replayed response"), resume=True, **kwargs)
    assert len(reads) == 1 and (tmp_path / "requests/0001.response.json").read_bytes() == saved


def test_two_different_contract_errors_can_be_repaired(tmp_path):
    root, calls = setup_run(tmp_path), []
    def judge(prompt):
        value = json.loads(prompt)
        calls.append(value)
        if len(calls) == 1:
            return {"raw_text": "{broken"}
        verdict = fixture_verdict(value)
        if len(calls) == 2:
            verdict["process_criteria"][0].pop("citations")
        if len(calls) == 3:
            assert len([v for v in value["followups"] if "format_error" in v]) == 1
            assert "citations" in value["followups"][-1]["format_error"]
        return verdict
    result = score_workspace(root, rules_root=tmp_path / "rules", judge_call=judge, publish=False)
    assert result["status"] == "scored" and len(calls) == 3
    assert result["scoring_version"]["max_format_repairs"] == 2


@pytest.mark.parametrize("status,finish", [("incomplete", None), (None, "length"), ("failed", None)])
def test_incomplete_response_never_becomes_a_verdict(status, finish):
    with pytest.raises(ValueError, match="incomplete"):
        parse_judge_response({"raw_text": '{"score": 1}', "response_status": status, "finish_reason": finish}, diagnostics={})


def test_message_boundaries_cannot_silently_change_the_answer():
    def response(texts):
        return {"raw_text": "".join(texts), "output_messages": [
            {"content": [{"type": "output_text", "text": text}]} for text in texts]}
    assert parse_judge_response(response([json.dumps(READ)] * 2), diagnostics={}) == READ
    with pytest.raises(ValueError):
        parse_judge_response(response(['{"score":', '1}']), diagnostics={})
    split = {"raw_text": '{"score":1}', "output_messages": [{"content": [
        {"type": "output_text", "text": '{"score":'}, {"type": "output_text", "text": '1}'}]}]}
    assert parse_judge_response(split, diagnostics={}) == {"score": 1}


def test_structural_error_list_is_bounded():
    verdict = {"score": 0, "rationale": "fixture", "citations": [{"ref": "unknown"}] * 100}
    def fail(c):
        raise ValueError("not registered")
    with pytest.raises(JudgeContractError) as caught:
        validate_judge_verdict(verdict, {}, citation_check=fail)
    assert caught.value.truncated and len(caught.value.errors) <= 20
    assert len(json.dumps(caught.value.errors, ensure_ascii=False)) <= 6000


@pytest.mark.parametrize("succeed", [True, False])
def test_opted_in_timeout_retry_is_bounded_and_does_not_restart_agent(make_runner, monkeypatch, succeed):
    from evaluation.execution.control import resume_scoring
    from evaluation.execution.recovery import runner_store
    from evaluation.scoring import service
    runner = make_runner()
    store = runner_store(runner)
    store.put_record("test", "failures", 0)
    assert runner.run()["status"] == "completed"
    calls = []
    def judge(prompt, **kwargs):
        calls.append(prompt)
        if len(calls) == 1 or not succeed:
            raise TimeoutError("Request timed out.")
        return fixture_verdict(json.loads(prompt))
    monkeypatch.setattr(service, "_default_judge_call", judge)
    config = {"judge": {"enabled": True, "retry_in_doubt": True}}
    result = resume_scoring(runner.workspace, config)
    assert result["status"] == ("scored" if succeed else "in_doubt")
    assert len(calls) == 2 and store.get_record("test", "calls") == 1
    assert result["judge_usage"]["total_tokens"] is None
    resume_scoring(runner.workspace, config)
    assert len(calls) == 2  # A second invocation must not reset the retry allowance.


def test_transport_records_blocks_and_timeout_without_reasoning(monkeypatch):
    import openai
    from evaluation.scoring.service import _default_judge_call
    for name, value in {"JUDGE_API_KEY": "fixture", "JUDGE_API_BASE": "http://localhost/v1", "JUDGE_MODEL_NAME": "fixture",
                        "JUDGE_WIRE_API": "responses", "JUDGE_TIMEOUT_SECONDS": "123"}.items():
        monkeypatch.setenv(name, value)
    block = SimpleNamespace(type="output_text", text=json.dumps(READ))
    message = SimpleNamespace(type="message", id="m1", status="completed", content=[block])
    response = SimpleNamespace(output_text=block.text, output=[message, SimpleNamespace(type="reasoning")], status="completed", usage=None)
    class Client:
        def __init__(self, **kwargs):
            assert kwargs["timeout"] == 123 and kwargs["max_retries"] == 0
            self.responses = SimpleNamespace(create=lambda **kw: response)
        def __enter__(self): return self
        def __exit__(self, *args): pass
    monkeypatch.setattr(openai, "OpenAI", Client)
    result = _default_judge_call("fixture")
    assert len(result["output_messages"]) == 1 and result["output_messages"][0]["id"] == "m1"
    assert result["transport"]["timeout_seconds"] == 123


def test_disabled_resume_does_not_retry_even_with_saved_permission(make_runner, monkeypatch):
    from evaluation.execution.control import resume_scoring
    from evaluation.execution.recovery import runner_store
    from evaluation.scoring import service
    runner = make_runner(resume=False)
    runner_store(runner).put_record("test", "failures", 0)
    assert runner.run()["status"] == "completed"
    calls = []
    def judge(*args, **kwargs):
        calls.append(1)
        raise TimeoutError("Request timed out.")
    monkeypatch.setattr(service, "_default_judge_call", judge)
    result = resume_scoring(runner.workspace, {"judge": {"retry_in_doubt": True}})
    assert result["status"] == "in_doubt" and len(calls) == 1


def test_old_protocol_retains_single_repair_limit(tmp_path):
    count = 0
    def call(*args):
        nonlocal count
        count += 1
        return {"raw_text": "invalid" + str(count)}
    with pytest.raises(ScoringStop) as exc:
        run_judge(tmp_path, {}, "old", budget=ScoringBudget(), call=call, validate=lambda v: None,
                  read=lambda r: {}, config={"judge_model": "fixture", "judge_protocol_version": 2})
    assert count == 2 and exc.value.status == "judge_error"
    with pytest.raises(ScoringStop):
        run_judge(tmp_path, {}, "old", budget=ScoringBudget(), call=lambda *a: pytest.fail("cannot reset repair budget"),
                  validate=lambda v: None, read=lambda r: {}, resume=True,
                  config={"judge_model": "fixture", "judge_protocol_version": 2})


@pytest.mark.parametrize("pointer", ["/01", "/-1", "/2", "/١"])
def test_array_indices_are_not_guessed(tmp_path, pointer):
    root = setup_run(tmp_path)
    (root / "report/results.json").write_text('[0,1]')
    with pytest.raises(ValueError, match="does not exist"):
        read_registered_evidence(build_run_index(root), {"ref": "workspace/report/results.json", "pointer": pointer})
    with pytest.raises(ValueError, match="does not exist"):
        record_page([0, 1], {"ref": "review/payload", "pointer": pointer})


@pytest.mark.parametrize("mode", ["binary", "rubric_100", "dual_axis_100"])
def test_prompt_evidence_example_matches_reader_contract(mode):
    from evaluation.scoring.service import _system_prompt
    prompt = _system_prompt({"evaluation_mode": mode}, ScoringBudget())
    start = prompt.index('{"type":"evidence_request"')
    example, _ = json.JSONDecoder().raw_decode(prompt[start:])
    read = _reader({"index": {}, "payload": {"process_metrics": {"count": 0}}})
    assert [read(r)["value"] for r in example["reads"]] == [{"count": 0}]


def test_lost_response_after_process_interruption_uses_explicit_policy(make_runner, monkeypatch):
    from evaluation.execution.control import resume_scoring
    from evaluation.execution.recovery import runner_store
    from evaluation.scoring import service
    runner = make_runner()
    store = runner_store(runner)
    store.put_record("test", "failures", 0)
    assert runner.run()["status"] == "completed"
    calls = []
    def judge(prompt, **kwargs):
        calls.append(1)
        if len(calls) == 1:
            raise KeyboardInterrupt()
        return fixture_verdict(json.loads(prompt))
    monkeypatch.setattr(service, "_default_judge_call", judge)
    config = {"judge": {"retry_in_doubt": True}}
    with pytest.raises(KeyboardInterrupt):
        resume_scoring(runner.workspace, config)
    result = resume_scoring(runner.workspace, config)
    assert result["status"] == "scored" and len(calls) == 2
    assert result["judge_usage"]["total_tokens"] is None
    assert store.get_record("resume", "state")["judge_in_doubt_retries"] == 1


def test_host_array_paging_aliases_are_not_silently_ignored():
    values = list(range(20))
    page = record_page(values, {"ref": "review/payload", "array_start": 13, "array_count": 4})
    assert page["value"] == [13, 14, 15, 16]
    assert record_page(values, page["next"])["value"] == [17, 18, 19]
    with pytest.raises(ValueError, match="conflict"):
        record_page(values, {"ref": "review/payload", "start": 1, "array_start": 2})
    with pytest.raises(ValueError, match="array target"):
        record_page({}, {"ref": "review/payload", "array_start": 0})


def test_remaining_budget_is_visible_and_does_not_mutate_saved_evidence(tmp_path):
    payload, seen = {"source": 7}, []
    def call(prompt, system, maximum):
        seen.append(json.loads(prompt))
        return READ if len(seen) == 1 else {"done": True}
    run_judge(tmp_path, payload, "system", budget=ScoringBudget(max_requests=2),
              call=call, read=lambda r: {"value": 7}, validate=lambda v: None,
              config={"judge_model": "fixture", "judge_protocol_version": 3})
    assert payload == {"source": 7}
    assert [v["judge_budget"]["requests_remaining_including_this"] for v in seen] == [2, 1]
    assert seen[1]["judge_budget"]["total_request_chars_remaining_before_this"] < seen[0]["judge_budget"]["total_request_chars_remaining_before_this"]
