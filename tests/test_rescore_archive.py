import json
from pathlib import Path
import shutil

from test_task_package_v19 import package
from evaluation.provenance.evidence_archive import export_run_archive, open_archive
from evaluation.scoring.evidence import build_evidence_bundle
from evaluation.scoring.service import score_workspace
from chemistry_toolbox.src.recovery_io import control_directory


def test_rescore_uses_exported_rules_and_never_overwrites_original(tmp_path, monkeypatch):
    workspace = tmp_path / "run"
    (workspace / "report").mkdir(parents=True)
    control = control_directory(workspace, "run")
    package(control / "task_snapshot")
    (workspace / "_meta.json").write_text(json.dumps({"run_id":"run", "paper_id":"paper_fixture",
        "task_type":"autonomous_research", "status":"completed"}))
    (workspace / "report/report.md").write_text("The computed barrier is 12.3 kcal/mol, supporting path A.")
    (workspace / "report/results.json").write_text('{"barrier":12.3,"conclusion":"path A"}')
    (workspace / "_score.json").write_text('{"score":27.6,"rationale":"original"}')
    (workspace / "_tool_trace.jsonl").write_text("")
    export_run_archive(workspace, tmp_path / "archive")
    shutil.rmtree(workspace)
    shutil.rmtree(control)
    archive = open_archive(tmp_path / "archive")
    target = tmp_path / "archive/workspace"
    original = (target / "_score.json").read_bytes()
    calls = []
    def judge(prompt):
        calls.append(prompt)
        return {"score":50,"rationale":"offline fixture","criteria":[]}
    def fail(*args, **kwargs): raise AssertionError("rescore must not spawn")
    monkeypatch.setattr("subprocess.Popen", fail)
    result = score_workspace(target, rules_root=tmp_path / "archive/task_snapshot", publish=False,
        judge_call=judge, evidence_bundle=build_evidence_bundle(archive), output_dir=tmp_path / "new_score")
    assert calls, result
    assert result["score_id"]
    assert (tmp_path / "new_score/config.json").is_file()
    assert (tmp_path / "new_score/evidence.json").is_file()
    assert (target / "_score.json").read_bytes() == original
    assert not (target / "_score_history.jsonl").exists()


def test_budget_shortage_defers_instead_of_guessing_score(tmp_path):
    workspace = tmp_path / "run"
    (workspace / "report").mkdir(parents=True)
    root = tmp_path / "rules"
    package(root)
    (workspace / "_meta.json").write_text(json.dumps({"run_id":"run","paper_id":"paper_fixture","task_type":"autonomous_research"}))
    (workspace / "report/report.md").write_text("report")
    def fail(prompt): raise AssertionError("missing evidence should be resolved before judging")
    result = score_workspace(workspace, rules_root=root, judge_call=fail, publish=False,
        evidence_bundle={"coverage":{"requires_review":True}}, output_dir=tmp_path / "deferred")
    assert result["status"] == "needs_review" and result["score"] is None
