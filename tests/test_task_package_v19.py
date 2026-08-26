from __future__ import annotations

import json
from pathlib import Path

import pytest

from evaluation.contracts import (
    PackageManifest,
    package_content_hash,
    package_payload_entries,
    validate_task_package,
)
from evaluation.repository import (
    DuplicateTaskError,
    TaskRepository,
    load_private_reference,
    materialize_agent_files,
)
from evaluation.execution.runner import TaskRunner
from evaluation.schemas.eval_config import resolve_specs
from evaluation.scoring.adapters import load_runtime_evaluation


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value, encoding="utf-8")
    else:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def package(root: Path, *, paper_id: str = "paper_fixture", task_type: str = "autonomous_research") -> Path:
    root = root / task_type / paper_id
    _write(root / "agent_input/task.md", "# Objective\n\nCompute and explain the result.\n")
    _write(root / "agent_input/data/inputs/system.xyz", "1\ninput\nH 0 0 0\n")
    schema = {
        "required_files": ["report/results.json", "report/report.md"],
        "primary_result_file": "report/results.json",
        "result_schema": {
            "type": "object",
            "properties": {"barrier": {"type": "number"}, "conclusion": {"type": "string"}},
            "required": ["barrier", "conclusion"],
        },
    }
    _write(root / "agent_input/submission_schema.json", schema)
    _write(
        root / "task_info.json",
        {
            "paper_id": paper_id,
            "task_type": task_type,
            "title": "Fixture",
            "category": "reaction_mechanism",
            "paper": {"title": "Paper", "doi": "10.test/x", "journal": "J", "publication_date": "2026-01-01"},
            "data": [{"path": "data/inputs", "description": "Starting structure"}],
            "required_deliverables": [
                {"path": "report/results.json", "description": "Structured results"},
                {"path": "report/report.md", "description": "Scientific account"},
            ],
        },
    )
    common = {"paper_id": paper_id}
    _write(root / "evaluation/reference_key_points.json", {**common, "items": [{"key_point_id": "kp1", "statement": "Barrier", "expected": 12.3, "evidence_ids": ["ev1"], "claim_role": "intermediate"}]})
    _write(root / "evaluation/reference_conclusions.json", {**common, "items": [{"conclusion_id": "con1", "statement": "Mechanistic conclusion", "expected": "path A", "supporting_key_point_ids": ["kp1"], "evidence_ids": ["ev1"], "claim_role": "final"}]})
    _write(root / "evaluation/scoring_rules.json", {**common, "rules": [
        {"rule_id": "rule1", "reference_id": "kp1", "type": "numeric", "target": 12.3, "unit": "kcal/mol", "tolerance": 1, "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.barrier"], "comparison": "absolute_difference"}},
        {"rule_id": "rule2", "reference_id": "con1", "type": "semantic", "expected": "path A", "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.conclusion"], "comparison": "semantic_entailment"}},
    ]})
    _write(root / "evaluation/evidence_map.json", {**common, "evidence": [{"evidence_id": "ev1", "source": "paper evidence"}]})
    _write(root / "evaluation/critical_failures.json", {**common, "items": [{"id": "cf1", "description": "No computation", "condition": "no evidence"}]})
    entries = package_payload_entries(root)
    _write(
        root / "package_manifest.json",
        PackageManifest(
            paper_id=paper_id,
            task_type=task_type,
            package_content_sha256=package_content_hash(entries),
            entries=entries,
        ).model_dump(mode="json"),
    )
    return root


def refresh_manifest(root: Path) -> None:
    info = json.loads((root / "task_info.json").read_text())
    entries = package_payload_entries(root)
    _write(root / "package_manifest.json", PackageManifest(
        paper_id=info["paper_id"], task_type=info["task_type"],
        package_content_sha256=package_content_hash(entries), entries=entries,
    ).model_dump(mode="json"))


def test_v19_round_trip_and_diagnostic_tolerance(tmp_path: Path):
    root = package(tmp_path)
    report = validate_task_package(root)
    assert report.status == "passed"
    assert report.findings == []
    assert report.diagnostics == ["tolerance_requires_scientific_review:rule1"]


def test_v19_rejects_empty_evaluator_and_bad_binding(tmp_path: Path):
    root = package(tmp_path)
    rules = json.loads((root / "evaluation/scoring_rules.json").read_text())
    rules["rules"][0]["binding"]["artifact_paths"] = ["report/undeclared.json"]
    _write(root / "evaluation/scoring_rules.json", rules)
    refresh_manifest(root)
    report = validate_task_package(root)
    assert "scoring_rule_binding_artifact_undeclared:rule1:report/undeclared.json" in report.findings


def test_repository_indexes_same_paper_in_two_modes(tmp_path: Path):
    package(tmp_path, task_type="autonomous_research")
    package(tmp_path, task_type="paper_reproduction")
    repository = TaskRepository([tmp_path])
    assert [(item.task_type, item.paper_id) for item in repository.list()] == [
        ("autonomous_research", "paper_fixture"),
        ("paper_reproduction", "paper_fixture"),
    ]


def test_repository_rejects_duplicate_tuple(tmp_path: Path):
    package(tmp_path / "one")
    package(tmp_path / "two")
    with pytest.raises(DuplicateTaskError):
        TaskRepository([tmp_path / "one", tmp_path / "two"])


def test_runner_materializes_only_agent_input(tmp_path: Path):
    package(tmp_path)
    repository = TaskRepository([tmp_path])
    workspace = tmp_path / "workspace"
    files = materialize_agent_files(
        paper_id="paper_fixture", task_type="autonomous_research",
        destination=workspace, repository=repository,
    )
    assert files == ["data/inputs/system.xyz", "submission_schema.json", "task.md"]
    assert not (workspace / "evaluation").exists()
    assert not (workspace / "task_info.json").exists()
    with pytest.raises(PermissionError):
        load_private_reference(
            paper_id="paper_fixture", task_type="autonomous_research",
            repository=repository,
        )


def test_computational_mode_rejects_pdf_in_agent_input(tmp_path: Path):
    root = package(tmp_path)
    _write(root / "agent_input/data/paper.pdf", "pdf")
    refresh_manifest(root)
    report = validate_task_package(root)
    assert "paper_pdf_exposed_to_agent:agent_input/data/paper.pdf" in report.findings


def test_v19_runtime_and_scoring_adapter_use_two_field_identity(tmp_path: Path, monkeypatch):
    task_root = tmp_path / "tasks"
    package(task_root, task_type="paper_reproduction")
    monkeypatch.setattr("evaluation.repository.TASK_ROOTS", (task_root,))
    runner = TaskRunner(
        "paper_fixture",
        task_type="paper_reproduction",
        agent_key="mock",
        workspace_root=tmp_path / "workspaces",
        live_progress=False,
    )
    result = runner.run()
    assert result["status"] == "completed"
    assert result["paper_id"] == "paper_fixture"
    assert result["task_type"] == "paper_reproduction"
    assert not (runner.workspace / "evaluation").exists()
    runtime = load_runtime_evaluation(
        paper_id="paper_fixture", task_type="paper_reproduction"
    )
    assert runtime.task_type == "paper_reproduction"
    assert runtime.ground_truth["expected_result"]["key_points"]


def test_eval_config_requires_paper_id_and_task_type(monkeypatch):
    monkeypatch.setattr(
        "evaluation.schemas.eval_config.list_tasks",
        lambda: [{"paper_id": "paper_fixture", "task_type": "autonomous_research"}],
    )
    specs = resolve_specs(
        {
            "agents": ["mock"],
            "tasks": [
                {"paper_id": "paper_fixture", "task_type": "autonomous_research"}
            ],
        }
    )
    assert [(item.paper_id, item.task_type) for item in specs] == [
        ("paper_fixture", "autonomous_research")
    ]
