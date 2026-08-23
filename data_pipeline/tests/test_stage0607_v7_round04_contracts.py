"""Round04 regression tests for the mode-aware hidden evaluator transport contract.

These tests intentionally use paper-neutral fixtures.  They exercise syntax and
publication-state behavior only; no chemistry-specific target or rule is encoded.
"""

from __future__ import annotations

from pathlib import Path

from src.contracts import read_json, write_json
from src.stages.stage06_task_builder.prompts import hidden_reference_instructions
from src.stages.stage06_task_builder.stage import (
    _normalize_hidden_reference_contract,
    _task_pair_builder_transport_findings,
)
from src.stages.stage06_task_builder.validation import acceptance_profile_type_findings
from src.stages.stage06_task_builder.validation import validate_hidden_reference
from src.stages.stage07_task_judge.stage import _finalize_stage07_response
from src.stages.stage07_task_judge.validation import stage07_mechanical_pre_publish_check


def _binding(*, field: str = "$.values", artifact: str = "report/results.json") -> dict:
    return {
        "artifact_paths": [artifact],
        "observed_fields": [field],
        "canonical_projection": {"value": 1},
        "comparison": "numeric_tolerance",
    }


def _make_pair(tmp_path: Path, hidden: dict, *, pair_id: str = "pair-round04") -> Path:
    pair = tmp_path / "pair"
    (pair / "hidden_reference").mkdir(parents=True)
    write_json(pair / "hidden_reference" / "ground_truth_common.json", hidden)
    for mode, task_mode, suffix in (
        ("paper_reproduction", "guided_reproduction", "_reproduction"),
        ("autonomous_research", "open_discovery", "_autonomous"),
    ):
        root = pair / mode
        (root / "data" / "inputs").mkdir(parents=True)
        (root / "data" / "inputs" / "input.xyz").write_text(
            "1\nneutral input\nH 0 0 0\n", encoding="utf-8"
        )
        (root / "task.md").write_text(
            "Determine the declared scientific result and document the process.\n",
            encoding="utf-8",
        )
        info = {
            "task_id": f"{pair_id}{suffix}",
            "task_pair_id": pair_id,
            "source_id": "source-round04",
            "category": "computational_chemistry",
            "mode": mode,
            "scientific_mode": mode,
            "task_mode": task_mode,
        }
        spec = {
            "task_id": info["task_id"],
            "task_pair_id": pair_id,
            "mode": mode,
            "scientific_mode": mode,
            "complexity_profile": {"level": "medium", "rationale": "fixture"},
        }
        write_json(root / "task_info.json", info)
        write_json(root / "task_spec.json", spec)
        write_json(
            root / "submission_contract.json",
            {
                "required_files": ["report/results.json", "report/report.md"],
                "results_schema": {
                    "type": "object",
                    "properties": {
                        "values": {"type": "object"},
                        "conclusion": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
        )
        write_json(
            root / "process_rubric.json",
            [
                {
                    "id": "process-1",
                    "criterion_type": "route_fidelity",
                    "max_score": 1,
                    "evidence_artifacts": ["report/process_trace.jsonl"],
                }
            ],
        )
    return pair


def _base_hidden(*, truths: list[dict], profiles: list[dict]) -> dict:
    return {
        "status": "ready",
        "task_pair_id": "pair-round04",
        "evaluation_mode": "binary",
        "score_max": 1,
        "expected_result": {},
        "ground_truth_items": truths,
        "acceptance_profiles": profiles,
        "scientific_conclusion_rubric": [
            {
                "id": truth["ground_truth_id"],
                "statement": "A declared result is supported.",
                "acceptance_rule": "Apply the typed acceptance profile.",
                "ground_truth_ids": [truth["ground_truth_id"]],
                "acceptance_profile_ids": [
                    truth.get("acceptance_profile_id")
                    or truth.get("acceptance_profile")
                ],
                "required_evidence": ["ev-round04"],
            }
            for truth in truths
        ],
    }


def test_hidden_prompt_aligns_shared_and_mode_matrix_binding_contracts() -> None:
    prompt = hidden_reference_instructions(task_pair_id="pair-round04")
    normalized = " ".join(prompt.split())
    assert "use a shared `submission_binding`" in normalized
    assert "`mode_submission_bindings`" in normalized
    assert "one row for each applicable public mode" in normalized


def test_vector_profile_aliases_are_normalized_without_collapsing_tolerances() -> None:
    raw = _base_hidden(
        truths=[
            {
                "ground_truth_id": "gt-vector",
                "acceptance_profile": "legacy-vector",
                "acceptance_type": "numeric_intermediate_result",
                "canonical_answer": {"a": 1.0, "b": 2.0},
                "acceptance_parameters": {
                    "numeric_tolerances": {"a_atol": 5e-6, "b_atol": 5e-5}
                },
                "evidence_grade": "A",
                "claim_role": "intermediate",
                "applies_to_modes": ["paper_reproduction"],
            }
        ],
        profiles=[
            {
                "profile_id": "legacy-vector",
                "kind": "numeric_intermediate_result",
                "submission_binding": {
                    "artifact": "report/results.json",
                    "binding_type": "document",
                    "document_target": "values",
                    "projection": {"a": 1.0, "b": 2.0},
                    "comparison_type": "numeric_tolerance",
                },
            }
        ],
    )
    normalized = _normalize_hidden_reference_contract(raw)
    profile = normalized["acceptance_profiles"][0]
    assert profile["type"] == "numeric_tolerance"
    assert profile["numeric_tolerances"] == {"a_atol": 5e-6, "b_atol": 5e-5}
    assert profile["applies_to_modes"] == ["paper_reproduction"]
    binding = profile["submission_binding"]
    assert binding["artifact_paths"] == ["report/results.json"]
    assert binding["observed_fields"] == ["document"]
    assert binding["document_binding"] is True
    assert binding["canonical_projection"] == {"a": 1.0, "b": 2.0}
    assert binding["comparison"] == "numeric_tolerance"
    assert acceptance_profile_type_findings(profile) == []


def test_numeric_profile_rejects_nonfinite_or_negative_scalar_tolerance() -> None:
    findings = acceptance_profile_type_findings(
        {
            "acceptance_profile_id": "ap-invalid-tolerance",
            "type": "numeric_tolerance",
            "target": 1.0,
            "unit": "arb",
            "absolute_tolerance": -0.1,
        }
    )
    assert "numeric_acceptance_tolerance_invalid:ap-invalid-tolerance:absolute_tolerance" in findings


def test_gate_filters_mode_specific_profiles_and_accepts_shared_valid_contract(tmp_path: Path) -> None:
    truths = [
        {
            "ground_truth_id": "gt-repro",
            "acceptance_profile_id": "ap-repro",
            "acceptance_type": "numeric_tolerance",
            "canonical_answer": 1.0,
            "acceptance_parameters": {"unit": "arb", "absolute_tolerance": 0.1},
            "evidence_grade": "A",
            "claim_role": "final",
            "applies_to_modes": ["paper_reproduction"],
        },
        {
            "ground_truth_id": "gt-auto",
            "acceptance_profile_id": "ap-auto",
            "acceptance_type": "numeric_tolerance",
            "canonical_answer": 2.0,
            "acceptance_parameters": {"unit": "arb", "absolute_tolerance": 0.1},
            "evidence_grade": "A",
            "claim_role": "final",
            "applies_to_modes": ["autonomous_research"],
        },
    ]
    hidden = _base_hidden(
        truths=truths,
        profiles=[
            {
                "acceptance_profile_id": "ap-repro",
                "type": "numeric_tolerance",
                "applies_to_modes": ["paper_reproduction"],
                "mode_submission_bindings": {
                    "paper_reproduction": _binding(),
                },
            },
            {
                "acceptance_profile_id": "ap-auto",
                "type": "numeric_tolerance",
                "applies_to_modes": ["autonomous_research"],
                "mode_submission_bindings": {
                    "autonomous_research": _binding(),
                },
            },
        ],
    )
    pair = _make_pair(tmp_path, hidden)
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="pair-round04")
    assert report["mechanical_pre_publish_status"] == "passed"
    assert not any(
        finding.startswith("evaluator_acceptance_profile_contract_invalid")
        for finding in report["findings"]
    )
    assert any(
        "evaluator_acceptance_profile_not_applicable:autonomous_research:ap-repro" in item
        for item in report["diagnostics"]
    )
    assert any(
        "evaluator_acceptance_profile_not_applicable:paper_reproduction:ap-auto" in item
        for item in report["diagnostics"]
    )


def test_stage06_hidden_validator_accepts_explicit_single_mode_scope() -> None:
    truths = [
        {
            "ground_truth_id": "gt-repro",
            "acceptance_profile_id": "ap-repro",
            "acceptance_type": "numeric_tolerance",
            "canonical_answer": 1.0,
            "acceptance_parameters": {"unit": "arb", "absolute_tolerance": 0.1},
            "evidence_grade": "A",
            "claim_role": "final",
            "applies_to_modes": ["paper_reproduction"],
        },
        {
            "ground_truth_id": "gt-auto",
            "acceptance_profile_id": "ap-auto",
            "acceptance_type": "numeric_tolerance",
            "canonical_answer": 2.0,
            "acceptance_parameters": {"unit": "arb", "absolute_tolerance": 0.1},
            "evidence_grade": "A",
            "claim_role": "final",
            "applies_to_modes": ["autonomous_research"],
        },
    ]
    hidden = _normalize_hidden_reference_contract(
        _base_hidden(
            truths=truths,
            profiles=[
                {
                    "acceptance_profile_id": "ap-repro",
                    "type": "numeric_tolerance",
                    "applies_to_modes": ["paper_reproduction"],
                    "mode_submission_bindings": {"paper_reproduction": _binding()},
                },
                {
                    "acceptance_profile_id": "ap-auto",
                    "type": "numeric_tolerance",
                    "applies_to_modes": ["autonomous_research"],
                    "mode_submission_bindings": {"autonomous_research": _binding()},
                },
            ],
        )
    )
    findings = validate_hidden_reference(
        hidden,
        submission_contract={
            "required_files": ["report/results.json"],
            "results_schema": {
                "type": "object",
                "properties": {"values": {"type": "object"}},
            },
        },
    )
    assert not any("mode_scope" in finding for finding in findings)


def test_shared_profile_is_checked_for_both_modes(tmp_path: Path) -> None:
    truth = {
        "ground_truth_id": "gt-shared",
        "acceptance_profile_id": "ap-shared",
        "acceptance_type": "numeric_tolerance",
        "canonical_answer": 1.0,
        "acceptance_parameters": {"unit": "arb", "absolute_tolerance": 0.1},
        "evidence_grade": "A",
        "claim_role": "final",
        "applies_to_modes": ["paper_reproduction", "autonomous_research"],
    }
    pair = _make_pair(
        tmp_path,
        _base_hidden(
            truths=[truth],
            profiles=[
                {
                    "acceptance_profile_id": "ap-shared",
                    "type": "numeric_tolerance",
                    "submission_binding": _binding(),
                }
            ],
        ),
    )
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="pair-round04")
    assert report["mechanical_pre_publish_status"] == "passed"
    assert not any("ap-shared" in finding for finding in report["findings"])


def test_gate_blocks_typed_profile_with_missing_scientific_binding_mapping(tmp_path: Path) -> None:
    truth = {
        "ground_truth_id": "gt-malformed",
        "acceptance_profile_id": "ap-malformed",
        "acceptance_type": "numeric_intermediate_result",
        "canonical_answer": {"a": 1.0},
        "acceptance_parameters": {"numeric_tolerances": {"a_atol": 0.01}},
        "evidence_grade": "A",
        "claim_role": "intermediate",
        "applies_to_modes": ["paper_reproduction", "autonomous_research"],
    }
    profile = {
        "profile_id": "ap-malformed",
        "kind": "numeric_intermediate_result",
        "submission_binding": {
            "artifact": "report/results.json",
            "binding_type": "document",
            "document_target": "values",
        },
    }
    pair = _make_pair(tmp_path, _base_hidden(truths=[truth], profiles=[profile]))
    report = stage07_mechanical_pre_publish_check(pair, task_pair_id="pair-round04")
    assert report["mechanical_pre_publish_status"] == "failed"
    assert "evaluator_binding_projection_missing:paper_reproduction:ap-malformed" in report[
        "findings"
    ]
    assert "evaluator_binding_comparison_missing:autonomous_research:ap-malformed" in report[
        "findings"
    ]
    assert read_json(
        pair / "hidden_reference" / "ground_truth_common.json"
    )["acceptance_profiles"][0]["type"] == "numeric_tolerance"


def test_stage06_builder_transport_check_does_not_require_autonomous_tree(tmp_path: Path) -> None:
    workspace = tmp_path / "builder"
    hidden_root = workspace / "outputs" / "hidden_reference"
    reproduction = workspace / "outputs" / "paper_reproduction"
    hidden_root.mkdir(parents=True)
    reproduction.mkdir(parents=True)
    truth = {
        "ground_truth_id": "gt-builder",
        "acceptance_profile_id": "ap-builder",
        "acceptance_type": "numeric_tolerance",
        "canonical_answer": 1.0,
        "acceptance_parameters": {"unit": "arb", "absolute_tolerance": 0.1},
        "evidence_grade": "A",
        "claim_role": "intermediate",
        "applies_to_modes": ["paper_reproduction"],
    }
    hidden = _base_hidden(
        truths=[truth],
        profiles=[
            {
                "profile_id": "ap-builder",
                "type": "numeric_tolerance",
                "submission_binding": _binding(),
            }
        ],
    )
    write_json(hidden_root / "ground_truth_common.json", hidden)
    write_json(
        reproduction / "submission_contract.json",
        {"required_files": ["report/results.json"], "results_schema": {"type": "object"}},
    )
    findings = _task_pair_builder_transport_findings(
        {"status": "ready"}, workspace
    )
    assert findings == []
    assert not (workspace / "outputs" / "autonomous_research").exists()


def test_stage07_finalizer_records_hidden_contract_normalization(tmp_path: Path) -> None:
    pair = tmp_path / "task_pair"
    (pair / "paper_reproduction").mkdir(parents=True)
    (pair / "autonomous_research").mkdir(parents=True)
    truth = {
        "ground_truth_id": "gt-finalizer",
        "acceptance_profile_id": "ap-finalizer",
        "acceptance_type": "numeric_intermediate_result",
        "canonical_answer": {"a": 1.0},
        "acceptance_parameters": {"numeric_tolerances": {"a_atol": 0.01}},
        "evidence_grade": "A",
        "claim_role": "final",
        "applies_to_modes": ["paper_reproduction"],
    }
    write_json(
        pair / "hidden_reference" / "ground_truth_common.json",
        _base_hidden(
            truths=[truth],
            profiles=[
                {
                    "profile_id": "ap-finalizer",
                    "kind": "numeric_intermediate_result",
                    "submission_binding": {
                        "artifact": "report/results.json",
                        "binding_type": "document",
                        "document_target": "values",
                    },
                }
            ],
        ),
    )
    existing_record = {
        "kind": "transport_normalization",
        "file": "task_info.json",
        "before_sha256": "before",
        "after_sha256": "after",
    }
    write_json(
        pair / "orchestrator_normalizations.json",
        {"schema_version": "stage07-normalization-provenance/v1", "records": [existing_record]},
    )
    response = _finalize_stage07_response(
        response={"audit_decision": "approved"},
        task_root=pair,
        toolbox={},
    )
    records = response["orchestrator_normalization_records"]
    assert records[0] == existing_record
    assert any(row["kind"] == "hidden_reference_contract_normalization" for row in records)
    provenance = read_json(pair / "orchestrator_normalizations.json")
    assert provenance["records"] == records
