from __future__ import annotations

import json
import sys
from pathlib import Path

DATA_PIPELINE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = DATA_PIPELINE_ROOT.parent
for import_root in (DATA_PIPELINE_ROOT, REPOSITORY_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from researchchembench_contracts import validate_task_package
from src.stages.stage07_task_judge.package import (
    assemble_task_packages,
    canonical_mode_task_id,
    project_computational_reference,
)
from src.stages.stage07_task_judge.stage import _assemble_task_packages_atomically


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _mode(root: Path, name: str) -> None:
    mode = root / name
    (mode / "data" / "inputs").mkdir(parents=True)
    (mode / "task.md").write_text(
        f"# Fixture {name}\n\nCompute the requested quantity and write the declared files.\n",
        encoding="utf-8",
    )
    (mode / "data" / "inputs" / "input.txt").write_text(
        "public input\n", encoding="utf-8"
    )
    _write_json(
        mode / "task_info.json",
        {
            "schema_version": "legacy-stage06-fixture",
            "task_id": f"agent_named_{name}",
            "task_pair_id": "agent_named_pair",
            "task_mode": "guided_reproduction" if name == "paper_reproduction" else "open_discovery",
            "scientific_mode": name,
            "source_id": "source_fixture",
            "paper_id": "paper_fixture",
            "category": "fixture",
            "required_deliverables": [
                {"path": "report/results.json", "description": "Results", "allow_empty": False},
                {"path": "report/report.md", "description": "Report", "allow_empty": False},
            ],
            "data": [
                {
                    "name": "Fixture input",
                    "path": "data/inputs/input.txt",
                    "type": "text/plain",
                    "description": "Public fixture input.",
                }
            ],
        },
    )
    _write_json(
        mode / "submission_contract.json",
        {
            "required_files": ["report/results.json", "report/report.md"],
            "submission_path": "report/results.json",
            "results_schema": {
                "type": "object",
                "properties": {"value": {"type": "number"}},
                "required": ["value"],
                "additionalProperties": True,
            },
            "allowed_extra_fields": True,
        },
    )
    _write_json(
        mode / "process_rubric.json",
        [
            {
                "id": "execute",
                "key_point": "Execute the workflow",
                "description": "Generate new computational evidence.",
                "evidence_artifacts": ["report/results.json"],
            }
        ],
    )
    # These build/audit files must never reach the final task package.
    _write_json(mode / "task_spec.json", {"private_build_contract": True})
    _write_json(mode / "route_evidence_map.json", {"hidden_route_mapping": True})


def _pair(tmp_path: Path) -> Path:
    root = tmp_path / "pair"
    _mode(root, "paper_reproduction")
    _mode(root, "autonomous_research")
    _write_json(
        root / "hidden_reference" / "ground_truth_common.json",
        {
            "status": "ready",
            "task_pair_id": "agent_named_pair",
            "evaluation_mode": "binary",
            "score_max": 1,
            "expected_result": {"value": 2.0},
            "ground_truth_items": [
                {
                    "ground_truth_id": "gt_value",
                    "kind": "numeric_final_result",
                    "canonical_answer": 2.0,
                    "acceptance_type": "numeric_tolerance",
                    "acceptance_parameters": {"absolute_tolerance": 0.2, "unit": "arb"},
                    "acceptance_profile_id": "ap_value",
                    "evidence_grade": "A",
                    "evidence_ids": ["evidence_value"],
                    "claim_role": "final",
                    "applies_to_modes": ["paper_reproduction", "autonomous_research"],
                },
                {
                    "ground_truth_id": "gt_reproduction_only",
                    "kind": "textual_intermediate_conclusion",
                    "canonical_answer": "Reproduction-only validation.",
                    "acceptance_type": "semantic_propositions",
                    "acceptance_profile_id": "ap_reproduction_only",
                    "evidence_grade": "A",
                    "evidence_ids": [],
                    "claim_role": "intermediate",
                    "applies_to_modes": ["paper_reproduction"],
                },
            ],
            "acceptance_profiles": [
                {
                    "acceptance_profile_id": "ap_value",
                    "ground_truth_id": "gt_value",
                    "type": "numeric_tolerance",
                    "parameters": {"absolute_tolerance": 0.2, "unit": "arb"},
                    "canonical_value": 2.0,
                    "target": 2.0,
                    "applies_to_modes": ["paper_reproduction", "autonomous_research"],
                    "mode_submission_bindings": {
                        "paper_reproduction": {
                            "artifact_paths": ["report/results.json"],
                            "observed_fields": ["$.value"],
                            "canonical_projection": 2.0,
                            "comparison": "numeric_tolerance",
                        },
                        "autonomous_research": {
                            "artifact_paths": ["report/results.json"],
                            "observed_fields": ["$.value"],
                            "canonical_projection": 2.0,
                            "comparison": "numeric_tolerance",
                        },
                    },
                },
                {
                    "acceptance_profile_id": "ap_reproduction_only",
                    "ground_truth_id": "gt_reproduction_only",
                    "type": "semantic_propositions",
                    "required_propositions": ["validation completed"],
                    "applies_to_modes": ["paper_reproduction"],
                    "submission_binding": {
                        "artifact_paths": ["report/report.md"],
                        "observed_fields": ["document"],
                        "comparison": "semantic_propositions",
                    },
                },
            ],
            "scientific_conclusion_rubric": [
                {
                    "id": "claim_value",
                    "statement": 2.0,
                    "acceptance_rule": "Apply the typed profile.",
                    "ground_truth_ids": ["gt_value"],
                    "acceptance_profile_ids": ["ap_value"],
                    "required_evidence": ["report/results.json"],
                }
            ],
            "critical_failures": ["No new calculation was executed."],
            "reference_evidence": {"evidence_ids": ["evidence_value"]},
            "managed_computation_policy": {"required": True},
        },
    )
    _write_json(
        root / "toolbox_requirements.json",
        [
            {
                "software_id": "future_program",
                "reason": "Required for the audited source workflow.",
            }
        ],
    )
    _write_json(root / "stage07_audit.json", {"audit_decision": "approved"})
    return root


def test_reference_projection_removes_score_and_duplicate_answers(tmp_path: Path):
    pair = _pair(tmp_path)
    hidden = json.loads(
        (pair / "hidden_reference" / "ground_truth_common.json").read_text(encoding="utf-8")
    )
    reference = project_computational_reference(
        hidden=hidden,
        task_type="autonomous_research",
        task_id="fixture_autonomous",
        process_rubric=json.loads(
            (pair / "autonomous_research" / "process_rubric.json").read_text(encoding="utf-8")
        ),
    )
    assert "evaluation_mode" not in reference
    assert "score_max" not in reference
    assert "expected_result" not in reference
    assert [item["answer_id"] for item in reference["answer_items"]] == ["gt_value"]
    assert "target" not in reference["acceptance_profiles"][0]
    assert "canonical_value" not in reference["acceptance_profiles"][0]
    assert "canonical_projection" not in reference["submission_bindings"][0]


def test_stage07_assembles_clean_complete_task_packages(tmp_path: Path):
    pair = _pair(tmp_path)
    reports = assemble_task_packages(
        pair_root=pair,
        final_tasks_root=tmp_path / "final_tasks",
        task_family_id="paper_fixture_task_pair",
        runtime_readiness="needs_software",
    )
    assert set(reports) == {"paper_reproduction", "autonomous_research"}
    assert all(report["status"] == "passed" for report in reports.values())
    for task_type, report in reports.items():
        root = Path(report["path"])
        assert root.name == canonical_mode_task_id("paper_fixture_task_pair", task_type)
        assert {path.name for path in root.iterdir()} == {
            "task.md",
            "task_info.json",
            "submission_schema.json",
            "data",
            "evaluation",
            "package_manifest.json",
        }
        assert not (root / "task_spec.json").exists()
        assert not (root / "route_evidence_map.json").exists()
        assert not (root / "stage07_audit.json").exists()
        info = json.loads((root / "task_info.json").read_text(encoding="utf-8"))
        assert info["task_type"] == task_type
        assert info["runtime_readiness"] == "needs_software"
        assert "task" not in info
        assert "task_mode" not in info
        assert validate_task_package(root).status == "passed"


def test_stage07_pair_assembly_publishes_both_modes_only_after_validation(tmp_path: Path):
    pair = _pair(tmp_path)
    reports = _assemble_task_packages_atomically(
        pair_root=pair,
        stage_root=tmp_path / "stage",
        task_family_id="paper_fixture_task_pair",
        runtime_readiness="ready",
        paper_id="paper_fixture",
    )
    assert all(report["status"] == "passed" for report in reports.values())
    assert all(Path(report["path"]).is_dir() for report in reports.values())
    assert not (tmp_path / "stage" / "package_staging" / "paper_fixture").exists()

    # A companion-mode validation failure must not publish a new half pair.
    bad_pair = _pair(tmp_path / "bad")
    (bad_pair / "autonomous_research" / "process_rubric.json").write_text(
        "[]\n", encoding="utf-8"
    )
    bad_reports = _assemble_task_packages_atomically(
        pair_root=bad_pair,
        stage_root=tmp_path / "bad_stage",
        task_family_id="paper_fixture_task_pair",
        runtime_readiness="ready",
        paper_id="paper_fixture",
    )
    assert bad_reports["autonomous_research"]["status"] == "failed"
    assert all(not report.get("path") for report in bad_reports.values())
    assert not (tmp_path / "bad_stage" / "final_tasks").exists()


def test_failed_package_does_not_leave_half_task(tmp_path: Path):
    pair = _pair(tmp_path)
    (pair / "autonomous_research" / "process_rubric.json").write_text(
        "[]\n", encoding="utf-8"
    )
    reports = assemble_task_packages(
        pair_root=pair,
        final_tasks_root=tmp_path / "final_tasks",
        task_family_id="paper_fixture_task_pair",
        runtime_readiness="ready",
    )
    assert reports["paper_reproduction"]["status"] == "passed"
    assert reports["autonomous_research"]["status"] == "failed"
    failed_path = (
        tmp_path
        / "final_tasks"
        / "autonomous_research"
        / canonical_mode_task_id("paper_fixture_task_pair", "autonomous_research")
    )
    assert not failed_path.exists()
