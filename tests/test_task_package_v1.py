from __future__ import annotations

import json
from pathlib import Path

import pytest

from evaluation.execution.runner import TaskRunner
from evaluation.repository import (
    DuplicateTaskIdError,
    TaskNotRunnableError,
    TaskRepository,
    load_private_reference,
    materialize_agent_files,
)
from evaluation.scoring.adapters import load_runtime_evaluation
from evaluation.scoring.service import score_workspace
from researchchembench_contracts import (
    COMPUTATIONAL_REFERENCE_SCHEMA_V1,
    PACKAGE_MANIFEST_SCHEMA_V1,
    SUBMISSION_SCHEMA_V1,
    TASK_INFO_SCHEMA_V1,
    TASK_PACKAGE_SCHEMA_V1,
    package_content_hash,
    package_payload_entries,
    validate_task_package,
)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _package(tmp_path: Path, *, task_id: str = "fixture_reproduction") -> Path:
    root = tmp_path / task_id
    (root / "data" / "inputs").mkdir(parents=True)
    (root / "evaluation").mkdir()
    (root / "task.md").write_text("# Run the declared workflow\n", encoding="utf-8")
    (root / "data" / "inputs" / "structure.xyz").write_text(
        "1\nfixture\nH 0 0 0\n", encoding="utf-8"
    )
    _write_json(
        root / "task_info.json",
        {
            "schema_version": TASK_INFO_SCHEMA_V1,
            "task_id": task_id,
            "task_family_id": "fixture_family",
            "task_type": "paper_reproduction",
            "source_id": "source_fixture",
            "title": "Fixture reproduction",
            "category": "test",
            "tags": [],
            "runtime_readiness": "ready",
            "required_capabilities": [],
            "data": [
                {
                    "name": "Input structure",
                    "path": "data/inputs/structure.xyz",
                    "type": "chemical/x-xyz",
                    "description": "Synthetic contract fixture.",
                }
            ],
            "required_deliverables": [
                {
                    "path": "report/results.json",
                    "description": "Structured results.",
                    "allow_empty": False,
                },
                {
                    "path": "report/report.md",
                    "description": "Scientific report.",
                    "allow_empty": False,
                },
            ],
            "related_task_ids": [],
            "reference_schema": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
        },
    )
    _write_json(
        root / "submission_schema.json",
        {
            "schema_version": SUBMISSION_SCHEMA_V1,
            "task_id": task_id,
            "required_files": ["report/results.json", "report/report.md"],
            "primary_result_file": "report/results.json",
            "result_schema": {
                "type": "object",
                "properties": {"value": {"type": "number"}},
                "required": ["value"],
                "additionalProperties": True,
            },
            "allowed_extra_fields": True,
        },
    )
    _write_json(
        root / "evaluation" / "reference.json",
        {
            "schema_version": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
            "task_id": task_id,
            "task_type": "paper_reproduction",
            "answer_items": [
                {
                    "answer_id": "answer_value",
                    "kind": "numeric_final_result",
                    "canonical_answer": 1.5,
                    "claim_role": "final",
                    "evidence_grade": "A",
                    "evidence_ids": ["evidence_fixture"],
                    "metadata": {},
                }
            ],
            "acceptance_profiles": [
                {
                    "acceptance_profile_id": "profile_value",
                    "answer_id": "answer_value",
                    "acceptance_type": "numeric_tolerance",
                    "parameters": {"absolute_tolerance": 0.1, "unit": "arb"},
                    "required_propositions": [],
                    "forbidden_contradictions": [],
                    "description": "Fixture tolerance.",
                }
            ],
            "submission_bindings": [
                {
                    "binding_id": "binding_value",
                    "acceptance_profile_id": "profile_value",
                    "artifact_paths": ["report/results.json"],
                    "observed_fields": ["$.value"],
                    "comparison": "numeric_tolerance",
                    "document_binding": False,
                }
            ],
            "process_key_points": [
                {
                    "key_point_id": "execute",
                    "title": "Execute",
                    "description": "Perform the declared calculation.",
                    "evidence_requirements": ["report/results.json"],
                    "metadata": {},
                }
            ],
            "final_conclusions": [
                {
                    "conclusion_id": "conclusion_value",
                    "statement": "Report the resulting value.",
                    "answer_ids": ["answer_value"],
                    "acceptance_profile_ids": ["profile_value"],
                    "required_evidence": ["report/results.json"],
                    "metadata": {},
                }
            ],
            "critical_failures": [],
            "private_evidence": {},
            "evaluation_constraints": {},
        },
    )
    entries = package_payload_entries(root)
    _write_json(
        root / "package_manifest.json",
        {
            "schema_version": PACKAGE_MANIFEST_SCHEMA_V1,
            "package_schema": TASK_PACKAGE_SCHEMA_V1,
            "task_id": task_id,
            "task_family_id": "fixture_family",
            "task_type": "paper_reproduction",
            "reference_schema": COMPUTATIONAL_REFERENCE_SCHEMA_V1,
            "assembler_version": "fixture-v1",
            "package_content_sha256": package_content_hash(entries),
            "entries": [entry.model_dump(mode="json") for entry in entries],
            "public_to_agent": ["task.md", "submission_schema.json", "data/**"],
            "manifest_self_excluded": True,
        },
    )
    return root


def _rewrite_package(
    root: Path,
    *,
    task_type: str | None = None,
    readiness: str | None = None,
    reference_schema: str | None = None,
) -> None:
    info_path = root / "task_info.json"
    info = json.loads(info_path.read_text(encoding="utf-8"))
    if task_type:
        info["task_type"] = task_type
    if readiness:
        info["runtime_readiness"] = readiness
    if reference_schema:
        info["reference_schema"] = reference_schema
    _write_json(info_path, info)

    reference_path = root / "evaluation" / "reference.json"
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    if task_type in {"paper_reproduction", "autonomous_research"}:
        reference["task_type"] = task_type
    if reference_schema:
        reference["schema_version"] = reference_schema
        if reference_schema != COMPUTATIONAL_REFERENCE_SCHEMA_V1:
            reference = {
                "schema_version": reference_schema,
                "task_id": info["task_id"],
                "payload": {"future_adapter_owned": True},
            }
    _write_json(reference_path, reference)

    manifest_path = root / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["task_type"] = info["task_type"]
    manifest["reference_schema"] = info["reference_schema"]
    entries = package_payload_entries(root)
    manifest["entries"] = [entry.model_dump(mode="json") for entry in entries]
    manifest["package_content_sha256"] = package_content_hash(entries)
    _write_json(manifest_path, manifest)


def test_task_package_v1_round_trip(tmp_path: Path):
    root = _package(tmp_path)
    report = validate_task_package(root)
    assert report.status == "passed", report.findings
    assert report.task_id == root.name
    assert report.task_type == "paper_reproduction"


def test_task_package_v1_rejects_unlisted_build_record(tmp_path: Path):
    root = _package(tmp_path)
    (root / "stage07_audit.json").write_text("{}\n", encoding="utf-8")
    report = validate_task_package(root)
    assert report.status == "failed"
    assert "unexpected_top_level_entry:stage07_audit.json" in report.findings


def test_task_package_v1_rejects_private_agent_allowlist(tmp_path: Path):
    root = _package(tmp_path)
    manifest_path = root / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["public_to_agent"].append("evaluation/reference.json")
    _write_json(manifest_path, manifest)
    report = validate_task_package(root)
    assert report.status == "failed"
    assert "private_entry_publicly_allowlisted:evaluation/reference.json" in report.findings


def test_task_package_v1_rejects_duplicate_answer_projection(tmp_path: Path):
    root = _package(tmp_path)
    reference_path = root / "evaluation" / "reference.json"
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    reference["acceptance_profiles"][0]["target"] = 1.5
    _write_json(reference_path, reference)
    report = validate_task_package(root)
    assert report.status == "failed"
    assert any("computational_reference_invalid" in item for item in report.findings)


def test_task_package_v1_requires_explicit_structured_binding_schema(tmp_path: Path):
    root = _package(tmp_path)
    schema_path = root / "submission_schema.json"
    submission = json.loads(schema_path.read_text(encoding="utf-8"))
    submission["result_schema"] = {
        "type": "object",
        "required": ["value"],
        "additionalProperties": True,
    }
    _write_json(schema_path, submission)
    entries = package_payload_entries(root)
    manifest_path = root / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["entries"] = [entry.model_dump(mode="json") for entry in entries]
    manifest["package_content_sha256"] = package_content_hash(entries)
    _write_json(manifest_path, manifest)
    report = validate_task_package(root)
    assert report.status == "failed"
    assert any("binding_schema_path_open" in item for item in report.findings)


def test_repository_v2_recurses_filters_and_keeps_private_reference_private(
    tmp_path: Path,
):
    ready = _package(
        tmp_path / "paper_reproduction", task_id="fixture_reproduction"
    )
    pending = _package(
        tmp_path / "autonomous_research", task_id="fixture_autonomous"
    )
    _rewrite_package(
        pending, task_type="autonomous_research", readiness="needs_software"
    )
    repository = TaskRepository([tmp_path])

    assert [item.task_id for item in repository.list()] == [
        "fixture_autonomous",
        "fixture_reproduction",
    ]
    assert [
        item.task_id
        for item in repository.list(task_type="paper_reproduction", runnable_only=True)
    ] == ["fixture_reproduction"]
    assert [
        item.task_id
        for item in repository.list(readiness="needs_software")
    ] == ["fixture_autonomous"]
    with pytest.raises(PermissionError):
        load_private_reference("fixture_reproduction", repository=repository)
    assert (
        load_private_reference(
            "fixture_reproduction",
            evaluator_context=True,
            repository=repository,
        )["task_id"]
        == "fixture_reproduction"
    )

    workspace = tmp_path / "materialized"
    copied = materialize_agent_files(
        "fixture_reproduction", workspace, repository=repository
    )
    assert copied == [
        "data/inputs/structure.xyz",
        "submission_schema.json",
        "task.md",
    ]
    assert not (workspace / "evaluation").exists()
    assert not (workspace / "task_info.json").exists()
    assert not (workspace / "package_manifest.json").exists()
    assert ready.is_dir()


def test_repository_v2_catalogs_unknown_adapter_but_will_not_run_it(tmp_path: Path):
    package = _package(
        tmp_path / "experiment_validation", task_id="fixture_experiment"
    )
    _rewrite_package(
        package,
        task_type="experiment_validation",
        reference_schema="experiment-validation-reference.future",
    )
    repository = TaskRepository([tmp_path])
    record = repository.get("fixture_experiment")
    assert record.evaluation_ready is False
    assert record.runnable is False
    assert repository.list(runnable_only=True) == []


def test_repository_v2_rejects_global_task_id_collision(tmp_path: Path):
    _package(
        tmp_path / "first" / "paper_reproduction",
        task_id="duplicate_fixture",
    )
    _package(
        tmp_path / "second" / "paper_reproduction",
        task_id="duplicate_fixture",
    )
    with pytest.raises(DuplicateTaskIdError, match="duplicate_task_id"):
        TaskRepository([tmp_path / "first", tmp_path / "second"])


def test_legacy_adapter_reads_embedded_instruction_without_creating_task_md(
    tmp_path: Path,
):
    root = tmp_path / "legacy_fixture"
    _write_json(
        root / "task_info.json",
        {
            "task_id": "legacy_fixture",
            "source_id": "legacy_source",
            "category": "legacy",
            "task": "Legacy embedded instruction.",
        },
    )
    _write_json(root / "target_study" / "ground_truth.json", {})
    repository = TaskRepository([tmp_path])
    assert repository.get("legacy_fixture").package_format == "legacy"
    assert not (root / "task.md").exists()


@pytest.mark.parametrize(
    ("task_type", "task_id"),
    [
        ("paper_reproduction", "runtime_reproduction"),
        ("autonomous_research", "runtime_autonomous"),
    ],
)
def test_v1_runner_isolates_reference_and_dual_axis_adapter_scores(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    task_type: str,
    task_id: str,
):
    task_root = _package(tmp_path / "tasks" / task_type, task_id=task_id)
    _rewrite_package(task_root, task_type=task_type)
    monkeypatch.setattr("evaluation.repository.TASK_ROOTS", (tmp_path / "tasks",))

    runner = TaskRunner(task_id, agent_key="mock", workspace_root=tmp_path / "runs")
    runner.setup_workspace()
    assert not (runner.workspace / "evaluation").exists()
    assert not (runner.workspace / "task_info.json").exists()
    assert (runner.workspace / "submission_schema.json").is_file()
    metadata = json.loads((runner.workspace / "_meta.json").read_text(encoding="utf-8"))
    assert metadata["task_type"] == task_type
    assert metadata["task_package_content_sha256"]

    runtime = load_runtime_evaluation(task_id)
    truth = runtime.ground_truth
    assert truth["evaluation_mode"] == "dual_axis_100"
    assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
    assert sum(
        item["max_score"] for item in truth["scientific_conclusion_rubric"]
    ) == 100
    assert runtime.policy_id == "dual_axis_100.v1"

    (runner.workspace / "report" / "report.md").write_text(
        "Computed result with linked evidence.\n", encoding="utf-8"
    )
    verdict = {
        "scientific_conclusions": [
            {
                "id": item["id"],
                "score": item["max_score"],
                "max_score": item["max_score"],
                "evidence_status": "supported",
                "rationale": "fixture",
            }
            for item in truth["scientific_conclusion_rubric"]
        ],
        "scientific_conclusion_score": 100,
        "process_criteria": [
            {
                "id": item["id"],
                "score": item["max_score"],
                "max_score": item["max_score"],
                "rationale": "fixture",
            }
            for item in truth["scoring_rubric"]
        ],
        "research_process_score": 100,
        "submission_validity": "valid",
        "critical_failures": [],
        "objective_issue_flags": [],
        "rationale": "fixture",
    }
    result = score_workspace(runner.workspace, judge_call=lambda _prompt: verdict)
    assert result["score"] == 100
    assert result["evaluator_adapter_id"] == "computational-science-dual-axis.v1"
    assert result["evaluation_policy_id"] == "dual_axis_100.v1"
    assert "expected_result" not in result


def test_v1_runner_rejects_unregistered_evaluator_adapter(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    package = _package(
        tmp_path / "tasks" / "experiment_validation", task_id="future_experiment"
    )
    _rewrite_package(
        package,
        task_type="experiment_validation",
        reference_schema="experiment-validation-reference.future",
    )
    monkeypatch.setattr("evaluation.repository.TASK_ROOTS", (tmp_path / "tasks",))
    with pytest.raises(TaskNotRunnableError, match="evaluator_adapter_unavailable"):
        TaskRunner(
            "future_experiment", agent_key="mock", workspace_root=tmp_path / "runs"
        )
