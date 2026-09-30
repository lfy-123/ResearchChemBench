"""Cross-task contracts and failure boundaries, independent of scientific answers."""
import json
from types import SimpleNamespace

import pytest

from chemistry_toolbox.src.recovery_io import file_lock
from evaluation.provenance.agent_events import load_agent_events
from evaluation.provenance.evidence_archive import build_run_index
from evaluation.scoring.evidence import build_evidence_bundle
from evaluation.scoring.judging import ScoringBudget, ScoringStop, run_judge
from evaluation.scoring.policies import _parse_judge_json, validate_judge_verdict
from evaluation.scoring.service import score_workspace
from test_judging import fixture_verdict, setup_run
from test_task_package_v19 import package, refresh_manifest


@pytest.mark.parametrize("task_type", ["autonomous_research", "paper_reproduction", "experiment_validation"])
@pytest.mark.parametrize("form", ["directory", "unbound_primary", "no_status", "markdown", "root_schema"])
def test_task_modes_and_public_output_shapes(tmp_path, task_type, form):
    root = tmp_path / "run"
    (root / "report").mkdir(parents=True)
    definition = package(tmp_path / "rules", task_type=task_type, paper_id="paper_renamed")
    contract = json.loads((definition / "agent_input/submission_schema.json").read_text())
    (root / "report/results.json").write_text('{"barrier":12.3,"conclusion":"path A"}')
    (root / "report/report.md").write_text("Account of the research")
    expected = None
    if form in {"directory", "markdown"}:
        deliverable = "report" if form == "directory" else "report/report.md"
        contract = {"required_files": [deliverable]}
        rules_path = definition / "evaluation/scoring_rules.json"
        rules = json.loads(rules_path.read_text())
        for rule in rules["rules"]:
            rule.update(type="semantic", expected="Documented result", binding={"artifact_paths": [deliverable], "fields": ["$"], "comparison": "semantic_entailment"})
        rules_path.write_text(json.dumps(rules))
    elif form == "unbound_primary":
        contract.update(primary_result_file="report/outcome.json", result_schema={"type": "object"})
        contract["required_files"].append("report/outcome.json")
        expected = "task_specific_new_state"
        (root / "report/outcome.json").write_text(json.dumps({"status": expected}))
    elif form == "root_schema":
        contract = {"required_files": contract["required_files"], **contract["result_schema"]}
    (definition / "agent_input/submission_schema.json").write_text(json.dumps(contract))
    (root / "submission_schema.json").write_text(json.dumps(contract))
    info_path = definition / "task_info.json"
    info = json.loads(info_path.read_text())
    info["required_deliverables"] = [{"path": path, "description": "Deliverable"} for path in contract["required_files"]]
    info_path.write_text(json.dumps(info))
    refresh_manifest(definition)
    (root / "_meta.json").write_text(json.dumps({"run_id": "other_run", "paper_id": "paper_renamed", "task_type": task_type, "status": "completed"}))
    result = score_workspace(root, rules_root=tmp_path / "rules", output_dir=tmp_path / "score", publish=False,
                             judge_call=lambda prompt: fixture_verdict(json.loads(prompt)))
    assert result["status"] == "scored", result
    assert result["submission_status"] == "valid"
    assert result["agent_declared_outcome"] == expected
    saved = json.loads((tmp_path / "score/prepared.json").read_text())
    assert "index" not in saved and "bundle" not in saved and "evidence" not in saved["payload"]


def test_bound_evidence_survives_renaming_reordering_and_irrelevant_inventory(tmp_path):
    results = []
    for folder, job, name in [("one", "aaa", "z.json"), ("two", "zzz", "a.json")]:
        root = tmp_path / folder
        output = root / "outputs/execution_jobs" / job
        output.mkdir(parents=True)
        (output / "status.json").write_text(json.dumps({"job_id": job, "status": "failed"}))
        (output / "request.json").write_text('{"job_type":"custom_analysis"}')
        value = {"value": 12.3, "future_metadata": {"version": 42}}
        if folder == "two":
            value = dict(reversed(list(value.items())))
            (output / "000_noise.json").write_text(json.dumps({"unrelated": ["diagnostic" * 100] * 10000}))
            (root / "report").mkdir()
            (root / "report/000_noise.md").write_text("unrelated narrative" * 10000)
        (output / name).write_text(json.dumps(value))
        path = f"outputs/execution_jobs/{job}/{name}"
        index = build_run_index(root)
        bundle = build_evidence_bundle(index, {"max_chars": 1000, "rules": [{"rule_id": "rule", "rule": {"binding": {"artifact_paths": [path]}}}]})
        excerpt = next(e for e in bundle["excerpts"] if e["ref"] == "workspace/" + path)
        results.append(json.loads(excerpt["content"]))
        assert not excerpt["truncated"]
        assert bundle["jobs"][0]["state"] == "failed"
        assert "outputs" not in bundle["jobs"][0]
    assert results[0] == results[1]


@pytest.mark.parametrize("wire", ["responses", "chat_completions"])
def test_transport_returns_raw_response_usage_and_disables_sdk_retries(monkeypatch, wire):
    import openai
    from evaluation.scoring.service import _default_judge_call
    for name, value in {"JUDGE_API_KEY": "fixture", "JUDGE_API_BASE": "http://localhost/v1", "JUDGE_MODEL_NAME": "fixture",
                        "JUDGE_WIRE_API": wire, "JUDGE_REASONING_EFFORT": "high"}.items():
        monkeypatch.setenv(name, value)
    usage = SimpleNamespace(input_tokens=7, output_tokens=3, prompt_tokens=7, completion_tokens=3, total_tokens=10,
        input_tokens_details=SimpleNamespace(cached_tokens=2), output_tokens_details=SimpleNamespace(reasoning_tokens=1),
        prompt_tokens_details=SimpleNamespace(cached_tokens=2), completion_tokens_details=SimpleNamespace(reasoning_tokens=1))
    def create(**kwargs):
        assert kwargs.get("max_output_tokens", kwargs.get("max_completion_tokens")) == 123
        return SimpleNamespace(output_text="{bad json", choices=[SimpleNamespace(message=SimpleNamespace(content="{bad json"))], usage=usage, id="response")
    class Client:
        def __init__(self, **kwargs):
            assert kwargs["max_retries"] == 0
            self.responses = SimpleNamespace(create=create)
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=create))
        def __enter__(self): return self
        def __exit__(self, *args): pass
    monkeypatch.setattr(openai, "OpenAI", Client)
    response = _default_judge_call("prompt", max_output_tokens=123)
    assert response["raw_text"] == "{bad json"
    assert response["_judge_usage"]["cached_input_tokens"] == 2
    assert response["_judge_usage"]["reasoning_output_tokens"] == 1


def test_concurrent_resume_fails_before_touching_requests(tmp_path):
    root = setup_run(tmp_path)
    directory = tmp_path / "score"
    with file_lock(directory / ".lock"):
        with pytest.raises(BlockingIOError):
            score_workspace(root, rules_root=tmp_path / "rules", output_dir=directory, publish=False, resume=True)
    assert not (directory / "config.json").exists()


def test_invalid_package_leaves_review_state_and_does_not_call_judge(tmp_path):
    root = setup_run(tmp_path)
    (tmp_path / "rules/autonomous_research/paper_fixture/agent_input/task.md").write_text("changed without a new manifest")
    result = score_workspace(root, rules_root=tmp_path / "rules", output_dir=tmp_path / "score", publish=False,
        judge_call=lambda prompt: pytest.fail("broken contract must not call Judge"))
    assert result["status"] == "needs_review"
    assert (tmp_path / "score/verdict.json").is_file()


def test_cumulative_unknown_usage_and_repeated_reads_remain_bounded(tmp_path):
    calls = []
    def call(*args):
        calls.append(1)
        return {"type": "evidence_request", "reads": [{"ref": "registered"}]}
    with pytest.raises(ScoringStop, match="without_progress"):
        run_judge(tmp_path, {}, "system", budget=ScoringBudget(), call=call, validate=lambda v: None, read=lambda r: {"value": 1})
    assert len(calls) == 2
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["judge_usage"]["total_tokens"] is None
    assert state["output_tokens_accounted"] == 2 * ScoringBudget().max_output_tokens


@pytest.mark.parametrize("bad", ["duplicate", "missing", "nan", "negative", "too_large", "citation", "rule_missing", "rule_reason"])
def test_invalid_verdict_cannot_publish(bad, tmp_path):
    root = setup_run(tmp_path)
    def judge(prompt):
        value = fixture_verdict(json.loads(prompt))
        if bad == "duplicate": value["process_criteria"].append(value["process_criteria"][0])
        elif bad == "missing": value["scientific_conclusions"] = []
        elif bad in {"nan", "negative", "too_large"}: value["process_criteria"][0]["score"] = {"nan": float("nan"), "negative": -1, "too_large": 101}[bad]
        elif bad == "citation": value["process_criteria"][0]["citations"] = [{"ref": "workspace/../../secret"}]
        elif bad == "rule_missing": value["rule_assessments"] = []
        else: value["rule_assessments"][0]["rationale"] = {"not": "text"}
        return value
    result = score_workspace(root, rules_root=tmp_path / "rules", output_dir=tmp_path / "score", judge_call=judge)
    assert result["status"] == "judge_error", result
    assert result["judge_usage"]["request_count"] == 2
    assert not (root / "_score.json").exists()
    assert (root / "_scoring_attempt.json").is_file()


def test_fences_binary_fraction_and_unknown_provider_fields(tmp_path):
    assert _parse_judge_json('```json\n{"score":1}\n```') == {"score": 1}
    with pytest.raises(ValueError, match="Binary"):
        validate_judge_verdict({"score": 0.999, "rationale": "reason"}, {"evaluation_mode": "binary"}, citation_check=lambda c: None)
    events = [{"type": "item.completed", "item": {"type": {}, "status": {}, "id": []}},
              {"type": "item.completed", "item": None}, {"type": "tool_use", "part": []},
              {"type": ["future"], "part": {"state": None}}, ["unknown array"]]
    (tmp_path / "_agent_output.jsonl").write_text("\n".join(map(json.dumps, events)))
    (tmp_path / "_model_io.jsonl").write_text(json.dumps({"record_type": "model_step", "output": []}))
    values = load_agent_events(tmp_path)
    assert len(values) == len(events)
    assert sum(v["kind"] == "unparsed" for v in values) == 4
