from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pytest

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.harness import (
    _apply_schema_defaults,
    _recover_trusted_workspace_response,
    _trusted_artifact_receipt,
    _validated_structured_response,
)
from src.agents.namespace_exec import _read_only_workspace_paths
from src.agents.responses_bridge import (
    ResponsesBridge,
    _consume_final_json_tool,
    _final_json_tool,
    _normalize_returned_tool_aliases,
    _retain_file_first_artifact_write_calls,
    _retain_structured_artifact_write_calls,
    responses_to_chat,
)
from src.agents.schemas import (
    AGENT_SUMMARY_SCHEMA,
    STAGE06_AUTONOMOUS_SCHEMA,
    STAGE06_REVIEW_SCHEMA,
)
from src.agents.workspace import (
    agent_recovery_context,
    atomic_commit_tree,
    copy_recovery_artifacts,
    copytree_exact,
    make_read_only,
)
from src.contracts import read_json, write_json
from src.stages.stage06_task_builder.stage import (
    _agent_public_basis,
    _canonicalize_review_evidence_ids,
    _compact_toolbox_snapshot,
    _extract_markdown_tables,
    _interrupted_phase_artifact_recovery,
    _layout_coordinate_blocks,
    _load_phase_json_artifact,
    _normalize_evaluation_references,
    _normalize_hidden_reference_contract,
    _normalize_process_rubric,
    _normalize_public_input_path,
    _normalize_scientific_failure_contract,
    _normalize_submission_contract,
    _normalize_task_pair_artifact_contracts,
    _normalize_workflow_review_aliases,
    _reconcile_task_phase_receipt,
    _recover_public_assets,
    _reproduction_patch_script,
    _reproduction_phase_findings,
    _run_phase,
    _seed_prior_scientific_review_draft,
    _setup_autonomous_inputs,
    _setup_hidden_inputs,
    _setup_reproduction_inputs,
    _task_pair_builder_phase_findings,
    run_stage06,
)
from src.stages.stage06_task_builder.validation import (
    validate_autonomous_route_isolation,
    validate_ground_truth_consistency,
    validate_hidden_reference,
    validate_scientific_review,
    validate_task_boundary_conditions,
    validate_task_pair,
    validate_task_pair_draft,
    validate_workflow_review,
)
from src.stages.stage07_task_judge.prompts import STAGE07_AUDIT_VERSION, audit_instructions
from src.stages.stage07_task_judge.stage import (
    _audit_pair_manifest,
    _cached_audit_inputs_match,
    _require_stage07_artifact_delivery,
    _stage07_audit_initializer_script,
    _stage07_audit_packet,
    _stage07_audit_scaffold,
    run_stage07,
)
from src.stages.stage07_task_judge.validation import merge_audit_outcomes, validate_agent_audit


class _Model:
    role = "builder"
    model = "mock"
    config = {"model": "mock", "workers": 1}


def test_schema_defaults_fill_only_explicit_empty_arrays() -> None:
    schema = {
        "type": "object",
        "required": ["decision", "reasons"],
        "properties": {
            "decision": {"type": "string"},
            "reasons": {"type": "array", "items": {"type": "string"}, "default": []},
        },
    }
    assert _apply_schema_defaults({"decision": "ready"}, schema) == {
        "decision": "ready",
        "reasons": [],
    }


def test_copytree_exact_replaces_read_only_recovery_target(tmp_path: Path) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    (source / "nested").mkdir(parents=True)
    (source / "nested" / "asset.txt").write_text("recovered", encoding="utf-8")
    (destination / "nested").mkdir(parents=True)
    (destination / "nested" / "asset.txt").write_text("stale", encoding="utf-8")
    make_read_only(destination)

    copytree_exact(source, destination)

    assert (destination / "nested" / "asset.txt").read_text(encoding="utf-8") == "recovered"


def test_agent_namespace_only_freezes_top_level_input_roots(tmp_path: Path) -> None:
    canonical_inputs = tmp_path / "inputs"
    private_input = tmp_path / "private_input"
    public_task_inputs = (
        tmp_path
        / "outputs"
        / "task_pair"
        / "autonomous_research"
        / "data"
        / "inputs"
    )
    canonical_inputs.mkdir()
    private_input.mkdir()
    public_task_inputs.mkdir(parents=True)

    protected = _read_only_workspace_paths(tmp_path)

    assert protected == (canonical_inputs, private_input)
    assert public_task_inputs not in protected


def test_atomic_commit_tree_replaces_and_cleans_read_only_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    (source / "nested").mkdir(parents=True)
    (source / "nested" / "asset.txt").write_text("committed", encoding="utf-8")
    (destination / "nested").mkdir(parents=True)
    (destination / "nested" / "asset.txt").write_text("old", encoding="utf-8")
    make_read_only(destination)

    atomic_commit_tree(source, destination)

    assert (destination / "nested" / "asset.txt").read_text(encoding="utf-8") == "committed"
    assert not list(tmp_path.glob(".destination.previous-*"))


def test_positive_scientific_review_requires_complete_top_level_contract() -> None:
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            {
                "decision": "candidate_ready",
                "task_pair_id": "paper-test",
                "reject_reasons": [],
            },
            STAGE06_REVIEW_SCHEMA,
        )


def test_scientific_review_rejects_schema_generated_placeholders() -> None:
    findings = validate_scientific_review(
        {
            "decision": "scientific_reject",
            "reject_reasons": ["reject reasons"],
            "scientific_question": "scientific question",
            "evidence_map": [{"key": "value"}],
        },
        set(),
    )

    assert "scientific_review_contains_placeholder" in findings


def test_hidden_reference_aliases_are_normalized_without_changing_frozen_targets() -> None:
    expected = [
        {
            "ground_truth_id": "gt-energy",
            "kind": "numeric_tolerance",
            "canonical_answer": {"delta_e": 1.25},
            "required_propositions": [],
            "forbidden_contradictions": [],
            "acceptance_type": "numeric_tolerance",
            "acceptance_parameters": {"unit": "eV", "tolerance_eV": 0.05},
            "evidence_grade": "A",
            "evidence_ids": ["ev-1"],
            "claim_role": "final",
        },
        {
            "ground_truth_id": "gt-conclusion",
            "kind": "semantic_propositions",
            "canonical_answer": "A is favored over B.",
            "required_propositions": ["A is favored over B."],
            "forbidden_contradictions": ["B is favored over A."],
            "acceptance_type": "semantic_propositions",
            "acceptance_parameters": {},
            "evidence_grade": "B",
            "evidence_ids": ["ev-2"],
            "claim_role": "intermediate",
        },
    ]
    raw = {
        "status": "ready",
        "ground_truth_items": [
            {**expected[0], "acceptance_profile": "ap-numeric"},
            {**expected[1], "acceptance_profile": "ap-semantic"},
        ],
        "acceptance_profiles": [
            {
                "profile_id": "ap-numeric",
                "type": "numeric_tolerance",
                "default_parameters": {"unit": "eV", "tolerance_eV": 0.05},
            },
            {"profile_id": "ap-semantic", "type": "semantic_propositions"},
        ],
        "scientific_conclusion_rubric": [
            {
                "claim_id": "energy",
                "weight": 60,
                "statement": "Recover the energy.",
                "acceptance_rule": "Within 0.05 eV.",
                "required_evidence": ["computed energy"],
                "acceptance_profile": "ap-numeric",
            },
            {
                "claim_id": "conclusion",
                "weight": 40,
                "statement": "Recover the conclusion.",
                "acceptance_rule": "Require the proposition without contradiction.",
                "required_evidence": ["computed comparison"],
                "acceptance_profile": "ap-semantic",
            },
        ],
    }

    normalized = _normalize_hidden_reference_contract(raw)

    assert validate_hidden_reference(normalized, expected_ground_truth_items=expected) == []
    assert normalized["acceptance_profiles"][0]["target"] == {"delta_e": 1.25}
    assert normalized["acceptance_profiles"][0]["absolute_tolerance"] == 0.05
    assert normalized["acceptance_profiles"][1]["required_propositions"] == ["A is favored over B."]
    assert normalized["scientific_conclusion_rubric"][0]["ground_truth_ids"] == ["gt-energy"]


def test_hidden_reference_cannot_expand_or_rewrite_review_targets() -> None:
    expected = [
        {
            "ground_truth_id": "gt-1",
            "kind": "categorical",
            "canonical_answer": "A",
            "required_propositions": [],
            "forbidden_contradictions": [],
            "acceptance_type": "categorical",
            "acceptance_parameters": {},
            "evidence_grade": "A",
            "evidence_ids": ["ev-1"],
            "claim_role": "final",
        }
    ]
    raw = {
        "status": "ready",
        "ground_truth_items": [
            {**expected[0], "canonical_answer": "B", "acceptance_profile": "ap-1"},
            {
                **expected[0],
                "ground_truth_id": "gt-added",
                "acceptance_profile": "ap-added",
            },
        ],
        "acceptance_profiles": [
            {"profile_id": "ap-1", "type": "categorical"},
            {"profile_id": "ap-added", "type": "categorical"},
        ],
        "scientific_conclusion_rubric": [
            {
                "id": "all",
                "max_score": 100,
                "statement": "All claims.",
                "acceptance_rule": "Exact categories.",
                "required_evidence": ["computed result"],
                "acceptance_profile_ids": ["ap-1", "ap-added"],
                "ground_truth_ids": ["gt-1", "gt-added"],
            }
        ],
    }

    findings = validate_hidden_reference(
        _normalize_hidden_reference_contract(raw),
        expected_ground_truth_items=expected,
    )

    assert "hidden_ground_truth_target_set_changed" in findings
    assert "hidden_ground_truth_frozen_field_changed:gt-1:canonical_answer" in findings


def test_file_first_contract_supersedes_small_receipt(tmp_path: Path) -> None:
    artifact = tmp_path / "outputs" / "review.json"
    artifact.parent.mkdir(parents=True)
    artifact.write_text('{"decision":"ready","reasons":[]}', encoding="utf-8")
    request = AgentRunRequest(
        phase="review",
        record_id="paper-test",
        workspace=tmp_path,
        instructions="",
        output_schema={
            "type": "object",
            "required": ["decision", "reasons"],
            "properties": {
                "decision": {"const": "ready"},
                "reasons": {"type": "array", "items": {"type": "string"}},
            },
        },
        prompt_version="test",
        metadata={"structured_artifact_path": "outputs/review.json"},
    )

    assert _validated_structured_response(
        {"status": "written", "artifact_path": "outputs/review.json"},
        request=request,
        workspace=tmp_path,
    ) == {"decision": "ready", "reasons": []}


def test_malformed_cli_final_recovers_complete_structured_artifact(tmp_path: Path) -> None:
    artifact = tmp_path / "outputs" / "review.json"
    artifact.parent.mkdir(parents=True)
    artifact.write_text('{"decision":"ready","reasons":[]}', encoding="utf-8")
    request = AgentRunRequest(
        phase="review",
        record_id="paper-test",
        workspace=tmp_path,
        instructions="",
        output_schema={
            "type": "object",
            "required": ["decision", "reasons"],
            "properties": {
                "decision": {"const": "ready"},
                "reasons": {"type": "array", "items": {"type": "string"}},
            },
        },
        prompt_version="test",
        metadata={"structured_artifact_path": "outputs/review.json"},
    )

    assert _recover_trusted_workspace_response(
        request=request,
        workspace=tmp_path,
    ) == {"decision": "ready", "reasons": []}


def test_cli_receipt_recovers_only_from_complete_trusted_task_artifact(
    tmp_path: Path,
) -> None:
    task = tmp_path / "task"
    task.mkdir()
    (task / "task.md").write_text("# Task\n", encoding="utf-8")
    for name in ("task_info.json", "task_spec.json"):
        (task / name).write_text("{}", encoding="utf-8")
    (task / "process_rubric.json").write_text("[]", encoding="utf-8")
    request = AgentRunRequest(
        phase="stage06_autonomous_task",
        record_id="paper-test",
        workspace=tmp_path,
        instructions="",
        output_schema=STAGE06_AUTONOMOUS_SCHEMA,
        prompt_version="test",
        metadata={
            "artifact_receipt_path": "task",
            "artifact_required_files": [
                "task.md",
                "task_info.json",
                "task_spec.json",
                "process_rubric.json",
            ],
            "artifact_receipt": {
                "status": "ready",
                "summary": "Recovered complete artifact.",
                "invalid_reasons": [],
            },
        },
    )

    recovered = _trusted_artifact_receipt(request=request, workspace=tmp_path)

    assert recovered == {
        "status": "ready",
        "summary": "Recovered complete artifact.",
        "invalid_reasons": [],
        "artifact_path": "task",
        "receipt_recovered_from_artifact": True,
    }
    (task / "task_spec.json").unlink()
    assert _trusted_artifact_receipt(request=request, workspace=tmp_path) is None


def test_cli_receipt_recovery_rejects_untrusted_artifact_path(tmp_path: Path) -> None:
    request = AgentRunRequest(
        phase="stage06_autonomous_task",
        record_id="paper-test",
        workspace=tmp_path,
        instructions="",
        output_schema=STAGE06_AUTONOMOUS_SCHEMA,
        prompt_version="test",
        metadata={
            "artifact_receipt_path": "../task",
            "artifact_required_files": ["task.md"],
            "artifact_receipt": {"status": "ready"},
        },
    )

    assert _trusted_artifact_receipt(request=request, workspace=tmp_path) is None


def test_autonomous_setup_materializes_inputs_and_compacts_agent_packet(
    tmp_path: Path,
) -> None:
    public_basis = {
        "scientific_question": "Compute molecular excited states.",
        "task_direction": "excited_state_spectroscopy",
        "category": "electronic_structure",
        "input_assets": [
            {
                "path": "inputs/molecule.xyz",
                "description": "Molecular geometry",
                "role": "structure_input",
                "content": "1\nH atom\nH 0 0 0\n",
            }
        ],
    }
    toolbox = {
        "schema_version": 3,
        "profile_id": "profile-test",
        "catalog_hash": "catalog-test",
        "runtime_profile_hash": "runtime-test",
        "unknown_field_policy": "preserve",
        "execution_layers": ["predefined_action", "task_specific_python"],
        "generic_python_analysis": True,
        "method_families": {
            "electronic_structure": {
                "backends": ["orca"],
                "required_actions": ["calculate_energy"],
            },
            "molecular_dynamics": {
                "backends": ["gromacs"],
                "required_actions": ["propagate_dynamics"],
            },
        },
        "backends": {
            "orca": {
                "display_name": "ORCA",
                "availability": "declared_supported",
                "actions": ["calculate_excited_states"],
                "excited_state_support": "supported",
            },
            "gromacs": {
                "display_name": "GROMACS",
                "availability": "declared_supported",
                "actions": ["propagate_dynamics"],
            },
        },
        "native_software": {},
        "python_packages": {},
    }

    _setup_autonomous_inputs(
        tmp_path,
        public_basis=public_basis,
        toolbox_snapshot=toolbox,
        task_pair_id="paper-test",
    )

    assert (tmp_path / "task" / "data" / "inputs" / "molecule.xyz").read_text() == (
        "1\nH atom\nH 0 0 0\n"
    )
    agent_basis = read_json(tmp_path / "inputs" / "public_task_basis.json")
    assert "content" not in agent_basis["input_assets"][0]
    assert agent_basis["input_assets"][0]["materialized_path"] == ("task/data/inputs/molecule.xyz")
    compact = read_json(tmp_path / "inputs" / "toolbox_snapshot.json")
    assert set(compact["method_families"]) == {"electronic_structure"}
    assert set(compact["backends"]) == {"orca"}
    assert "gromacs" not in json.dumps(compact).casefold()


def test_agent_public_basis_does_not_mutate_canonical_packet() -> None:
    basis = {"input_assets": [{"path": "public_inputs/a.xyz", "content": "1\nA\nH 0 0 0\n"}]}

    compact = _agent_public_basis(basis)

    assert basis["input_assets"][0]["content"] == "1\nA\nH 0 0 0\n"
    assert compact["input_assets"][0]["path"] == "a.xyz"
    assert "content" not in compact["input_assets"][0]


def test_evaluation_references_drop_construction_workspace_prefix() -> None:
    value = _normalize_evaluation_references(
        {
            "inputs": ["task/inputs/a.xyz", "task/data/inputs/b.xyz"],
            "outputs": ["task/outputs/results.json", "task/report/report.md"],
            "instruction": "Read task/inputs/a.xyz and write task/outputs/results.json.",
        }
    )

    assert value == {
        "inputs": ["data/inputs/a.xyz", "data/inputs/b.xyz"],
        "outputs": ["outputs/results.json", "report/report.md"],
        "instruction": "Read data/inputs/a.xyz and write outputs/results.json.",
    }


def test_agent_recovery_context_excludes_command_output_payload(tmp_path: Path) -> None:
    stdout = tmp_path / "stdout.jsonl"
    stdout.write_text(
        json.dumps(
            {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "command": "python build.py",
                    "aggregated_output": "SECRET_PAYLOAD" * 1000,
                    "exit_code": 0,
                    "status": "completed",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    task = tmp_path / "task"
    task.mkdir()
    (task / "paper_route.md").write_text("route", encoding="utf-8")
    context = agent_recovery_context(
        SimpleNamespace(
            failure_class="invalid_agent_output",
            error={
                "error_type": "InvalidPhaseContract",
                "message": "missing_category, review_public_answer_leakage:gt3",
            },
            final_message_path=None,
            stdout_path=stdout,
            workspace=tmp_path,
        )
    )

    assert context is not None
    assert "SECRET_PAYLOAD" not in context
    assert "python build.py" in context
    assert "missing_category, review_public_answer_leakage:gt3" in context
    assert "task/paper_route.md (5 bytes)" in context
    assert len(context) <= 8001


def test_copy_recovery_artifacts_creates_private_evidence_handoff(
    tmp_path: Path,
) -> None:
    previous = tmp_path / "previous"
    destination = tmp_path / "next"
    previous.mkdir()
    destination.mkdir()
    (previous / "_agent_stdout.jsonl").write_text(
        json.dumps(
            {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "command": "rg MN15 inputs/evidence_index.json",
                    "aggregated_output": "ev_method: MN15/def2-TZVP/PCM(MeCN)",
                    "exit_code": 0,
                    "status": "completed",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    copy_recovery_artifacts(previous, destination, include_evidence_trace=True)

    handoff = (destination / "RECOVERY_EVIDENCE.md").read_text(encoding="utf-8")
    assert "rg MN15" in handoff
    assert "ev_method: MN15/def2-TZVP/PCM(MeCN)" in handoff
    assert not (destination / "inputs").exists()

    second = tmp_path / "second"
    second.mkdir()
    (destination / "_agent_stdout.jsonl").write_text(
        json.dumps(
            {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "command": "rg Table RECOVERY_EVIDENCE.md",
                    "aggregated_output": "ev_result: 1.57 eV",
                    "exit_code": 0,
                    "status": "completed",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    copy_recovery_artifacts(destination, second, include_evidence_trace=True)
    accumulated = (second / "RECOVERY_EVIDENCE.md").read_text(encoding="utf-8")
    assert "ev_method: MN15/def2-TZVP/PCM(MeCN)" in accumulated
    assert "ev_result: 1.57 eV" in accumulated


def test_reproduction_setup_renders_route_scaffold_and_preserves_data(
    tmp_path: Path,
) -> None:
    autonomous = tmp_path / "autonomous"
    (autonomous / "data" / "inputs").mkdir(parents=True)
    (autonomous / "data" / "inputs" / "a.xyz").write_text("1\nA\nH 0 0 0\n")
    (autonomous / "task.md").write_text("Autonomous task", encoding="utf-8")
    for name, value in (
        (
            "task_info.json",
            {
                "task_id": "paper-test_autonomous",
                "task_pair_id": "paper-test",
                "mode": "autonomous_research",
                "task_mode": "open_discovery",
                "scientific_mode": "autonomous_research",
            },
        ),
        (
            "task_spec.json",
            {
                "task_id": "paper-test_autonomous",
                "task_pair_id": "paper-test",
                "mode": "autonomous_research",
                "task_mode": "open_discovery",
                "scientific_mode": "autonomous_research",
            },
        ),
        ("submission_contract.json", {"required_files": ["report/report.md"]}),
        ("process_rubric.json", [{"id": "design", "max_score": 100}]),
    ):
        (autonomous / name).write_text(json.dumps(value), encoding="utf-8")
    review = {
        "task_pair_id": "paper-test",
        "paper_route": {
            "software": [{"name": "ORCA", "role": "core_compute", "evidence_ids": ["ev_1"]}],
            "method": "PBE0/def2-SVP",
            "sequence": ["optimize", "calculate frequencies"],
            "route_completeness": {
                "status": "confirmed",
                "closed_fields": ["charge and multiplicity"],
                "unresolved_fields": [],
            },
        },
        "workflow_steps": [{"step_id": "s1", "action": "optimization", "evidence_ids": ["ev_1"]}],
    }

    workspace = tmp_path / "workspace"
    _setup_reproduction_inputs(
        workspace,
        autonomous_root=autonomous,
        review=review,
        base_manifest={"content_hash": "base-hash"},
    )

    assert "ORCA" in (workspace / "task" / "paper_route.md").read_text()
    assert read_json(workspace / "task" / "workflow_spec.json")["method"] == ("PBE0/def2-SVP")
    assert read_json(workspace / "task" / "route_evidence_map.json")["route_evidence_ids"] == [
        "ev_1"
    ]
    assert (workspace / "task" / "data" / "inputs" / "a.xyz").read_text() == ("1\nA\nH 0 0 0\n")
    findings = _reproduction_phase_findings(
        workspace,
        autonomous_root=autonomous,
        review=review,
    )
    assert "reproduction_task_mode_not_guided" in findings
    assert "reproduction_task_instruction_unchanged" in findings

    script = _reproduction_patch_script()
    compile(script, "apply_reproduction_patch.py", "exec")
    completed = subprocess.run(
        [sys.executable, "private_input/apply_reproduction_patch.py"],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    patched_info = read_json(workspace / "task" / "task_info.json")
    patched_spec = read_json(workspace / "task" / "task_spec.json")
    assert patched_info["task_mode"] == "guided_reproduction"
    assert patched_info["mode"] == "paper_reproduction"
    assert patched_info["task_pair_id"] == "paper-test"
    assert patched_spec["mode"] == "paper_reproduction"
    assert patched_spec["task_mode"] == "guided_reproduction"
    assert patched_spec["scientific_mode"] == "paper_reproduction"
    assert patched_spec["task_id"] == patched_info["task_id"]
    assert patched_spec["task_pair_id"] == patched_info["task_pair_id"]
    assert (
        _reproduction_phase_findings(
            workspace,
            autonomous_root=autonomous,
            review=review,
        )
        == []
    )
    task_text_after_first_run = read_json(workspace / "task" / "task_info.json")["task"]
    repeated = subprocess.run(
        [sys.executable, "private_input/apply_reproduction_patch.py"],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    assert repeated.returncode == 0, repeated.stderr
    assert read_json(workspace / "task" / "task_info.json")["task"] == (task_text_after_first_run)


def test_compact_toolbox_uses_domain_family_without_claiming_unknown_support() -> None:
    compact = _compact_toolbox_snapshot(
        {
            "method_families": {
                "electronic_structure": {"backends": ["gaussian"]},
            },
            "backends": {
                "gaussian": {
                    "availability": "declared_supported",
                    "excited_state_support": "unknown",
                }
            },
        },
        public_basis={"scientific_question": "Calculate an excited-state spectrum."},
    )

    assert compact["backends"]["gaussian"]["excited_state_support"] == "unknown"
    assert "authoritative" in compact["audit_note"]


def test_complete_task_artifact_supersedes_stale_invalid_receipt(tmp_path: Path) -> None:
    task = tmp_path / "task"
    task.mkdir()
    for name in (
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
    ):
        (task / name).write_text("{}", encoding="utf-8")

    reconciled = _reconcile_task_phase_receipt(
        {"status": "invalid", "artifact_path": "task", "invalid_reasons": ["stale"]},
        workspace=tmp_path,
        phase="autonomous_task",
        result=object(),
    )

    assert reconciled["status"] == "ready"
    assert reconciled["invalid_reasons"] == []
    assert reconciled["receipt_reconciled_from_artifact"] is True


def test_claimed_empty_task_artifact_is_retryable(tmp_path: Path) -> None:
    (tmp_path / "task").mkdir()

    with pytest.raises(Exception) as exc_info:
        _reconcile_task_phase_receipt(
            {
                "status": "invalid",
                "artifact_path": "task",
                "invalid_reasons": ["artifact was not materialized"],
            },
            workspace=tmp_path,
            phase="autonomous_task",
            result=type(
                "Result",
                (),
                {
                    "status": "succeeded",
                    "failure_class": None,
                    "retryable": False,
                    "error": None,
                    "audit_record": lambda self: {},
                },
            )(),
        )

    assert "partial" in str(exc_info.value).casefold()


def test_scientific_reject_receipt_is_terminal_without_detail_artifact(tmp_path: Path) -> None:
    receipt = {
        "decision": "scientific_reject",
        "task_pair_id": "paper-test",
        "artifact_path": "outputs/scientific_review.json",
        "reject_reasons": ["required structure is absent"],
    }

    loaded = _load_phase_json_artifact(receipt, tmp_path, fallback=receipt)

    assert loaded == receipt


def test_positive_task_receipt_missing_artifact_is_retried(tmp_path: Path) -> None:
    calls = 0

    def responder(request: AgentRunRequest) -> dict:
        nonlocal calls
        calls += 1
        task = request.workspace / "task"
        if calls == 1:
            (task / "task.md").write_text("partial", encoding="utf-8")
        if calls == 2:
            assert (task / "task.md").read_text(encoding="utf-8") == "partial"
            for name in (
                "task_info.json",
                "task_spec.json",
                "submission_contract.json",
                "process_rubric.json",
            ):
                (task / name).write_text("{}", encoding="utf-8")
        return {
            "status": "ready",
            "artifact_path": "task",
            "invalid_reasons": [],
        }

    harness = create_agent_harness(
        "mock",
        config={"mock_responder": responder},
        model_config={"model": "mock"},
    )
    receipt, audit, workspace = _run_phase(
        harness=harness,
        stage_root=tmp_path,
        paper_id="paper-test",
        phase="autonomous_task",
        prompt_version="test",
        instructions="Write the review artifact.",
        output_schema=STAGE06_AUTONOMOUS_SCHEMA,
        fingerprint_value={"paper": "paper-test"},
        config={
            "max_attempts": 2,
            "retry_backoff_seconds": 0,
            "recovery_max_tool_calls": 1,
            "resume": False,
        },
        setup=lambda root: (
            (root / "inputs").mkdir(),
            (root / "task").mkdir(),
        ),
    )

    assert calls == 2
    assert audit["cache_hit"] is False
    assert workspace is not None
    assert (workspace / "task").is_dir()
    assert (workspace / "outputs").is_dir()
    assert receipt["status"] == "ready"


def test_scientific_review_recovery_seeds_prior_contract_as_revision_draft(
    tmp_path: Path,
) -> None:
    paper_id = "paper-test"
    prior_fingerprint = "a" * 64
    review = {
        "decision": "scientific_reject",
        "task_pair_id": paper_id,
        "selected_candidate_id": "",
        "stage05_candidate_disposition": "",
        "scientific_question": "Question",
        "public_scientific_question": "Question",
        "task_direction": "",
        "category": "",
        "workflow_summary": "Incomplete workflow",
        "workflow_steps": [],
        "public_task_basis": {},
        "paper_route": {},
        "ground_truth_items": [],
        "evidence_map": {},
        "toolbox_requirements": [],
        "resource_assessment": {},
        "reject_reasons": ["missing input"],
        "warnings": [],
    }
    checkpoint = tmp_path / "checkpoints" / paper_id / "scientific_review.json"
    checkpoint.parent.mkdir(parents=True)
    checkpoint.write_text(
        json.dumps(
            {
                "input_fingerprint": prior_fingerprint,
                "response": review,
                "agent_run": {},
            }
        ),
        encoding="utf-8",
    )
    prior_outputs = (
        tmp_path
        / "phase_artifacts"
        / paper_id
        / "scientific_review"
        / prior_fingerprint[:16]
        / "outputs"
    )
    prior_outputs.mkdir(parents=True)
    (prior_outputs / "public_inputs").mkdir()
    (prior_outputs / "public_inputs" / "asset.txt").write_text(
        "asset", encoding="utf-8"
    )
    attempt = tmp_path / "attempt"
    attempt.mkdir()

    findings = _seed_prior_scientific_review_draft(
        stage_root=tmp_path,
        paper_id=paper_id,
        checkpoint=checkpoint,
        attempt_root=attempt,
        output_schema=STAGE06_REVIEW_SCHEMA,
        semantic_validator=lambda _response, _root: ["boundary_conditions missing"],
    )

    assert findings == ["boundary_conditions missing"]
    assert read_json(attempt / "outputs" / "scientific_review.json") == review
    assert (attempt / "outputs" / "public_inputs" / "asset.txt").read_text() == "asset"
    status = read_json(attempt / "PRIOR_REVIEW_DRAFT_STATUS.json")
    assert status["authority"] == "prior_checkpoint_revision_draft"
    assert status["current_deterministic_findings"] == findings


def test_interrupted_phase_recovery_requires_exact_fingerprint_and_artifact(
    tmp_path: Path,
) -> None:
    attempt = (
        tmp_path
        / "workspaces"
        / "paper-test"
        / "autonomous_task"
        / "attempt-01-test"
    )
    (attempt / "task").mkdir(parents=True)
    (attempt / "task" / "task.md").write_text("partial", encoding="utf-8")
    (attempt / "phase_state.json").write_text(
        json.dumps(
            {
                "phase": "autonomous_task",
                "paper_id": "paper-test",
                "input_fingerprint": "exact-fingerprint",
            }
        ),
        encoding="utf-8",
    )

    recovered = _interrupted_phase_artifact_recovery(
        stage_root=tmp_path,
        paper_id="paper-test",
        phase="autonomous_task",
        input_fingerprint_value="exact-fingerprint",
    )

    assert recovered is not None
    context, workspace = recovered
    assert workspace == attempt
    assert "task/task.md" in context
    assert (
        _interrupted_phase_artifact_recovery(
            stage_root=tmp_path,
            paper_id="paper-test",
            phase="autonomous_task",
            input_fingerprint_value="different",
        )
        is None
    )


def test_public_input_paths_are_relative_to_task_input_root() -> None:
    assert _normalize_public_input_path("structures.xyz") == "structures.xyz"
    assert _normalize_public_input_path("inputs/xyz/a.xyz") == "xyz/a.xyz"
    assert _normalize_public_input_path("public_inputs/xyz/a.xyz") == "xyz/a.xyz"
    assert _normalize_public_input_path("inputs/public_inputs/data/a.json") == "data/a.json"


def test_markdown_html_table_is_exported_with_derived_evidence(tmp_path: Path) -> None:
    document_root = tmp_path / "documents" / "doc_si"
    document_root.mkdir(parents=True)
    markdown = document_root / "normalized_document.md"
    markdown.write_text(
        "Table S1. Fractional atomic coordinates for model A.\n"
        "<table><tr><th>Atom</th><th>x</th><th>y</th><th>z</th></tr>"
        "<tr><td>C1</td><td>0.1</td><td>0.2</td><td>0.3</td></tr></table>\n",
        encoding="utf-8",
    )
    canonical = [
        {
            "evidence_id": "ev-caption",
            "text": "Table S1. Fractional atomic coordinates for model A.",
        }
    ]

    derived = _extract_markdown_tables(
        markdown_path=markdown,
        document_root=document_root,
        snapshot_root=tmp_path,
        document_id="doc_si",
        document_role="supplementary",
        canonical_blocks=canonical,
    )

    assert len(derived) == 1
    assert derived[0]["block_type"] == "derived_table"
    assert derived[0]["source_ref"]["source_evidence_ids"] == ["ev-caption"]
    table_path = next((document_root / "derived_tables").glob("table-*.tsv"))
    assert table_path.read_text(encoding="utf-8") == "Atom\tx\ty\tz\nC1\t0.1\t0.2\t0.3\n"


def test_coordinate_table_continuation_is_merged(tmp_path: Path) -> None:
    document_root = tmp_path / "documents" / "doc_si"
    document_root.mkdir(parents=True)
    markdown = document_root / "normalized_document.md"
    markdown.write_text(
        "Table S1. Fractional atomic coordinates for model A.\n"
        "<table><tr><th>Atom</th><th>x</th><th>y</th><th>z</th></tr>"
        "<tr><td>C1</td><td>0.1</td><td>0.2</td><td>0.3</td></tr></table>\n\n"
        "SUPPORTING INFORMATION\n"
        "<table><tr><td>H2</td><td>0.4</td><td>0.5</td><td>0.6</td></tr>"
        "<tr><td>H3</td><td>0.7</td><td>0.8</td><td>0.9</td></tr></table>\n",
        encoding="utf-8",
    )

    derived = _extract_markdown_tables(
        markdown_path=markdown,
        document_root=document_root,
        snapshot_root=tmp_path,
        document_id="doc_si",
        document_role="supplementary",
        canonical_blocks=[],
    )

    assert len(derived) == 1
    assert derived[0]["source_ref"]["source_table_ordinals"] == [1, 2]
    table_path = next((document_root / "derived_tables").glob("table-*.tsv"))
    assert table_path.read_text(encoding="utf-8").splitlines()[-2:] == [
        "H2\t0.4\t0.5\t0.6",
        "H3\t0.7\t0.8\t0.9",
    ]


def test_coordinate_atom_label_ocr_repair_is_traced(tmp_path: Path) -> None:
    document_root = tmp_path / "documents" / "doc_si"
    document_root.mkdir(parents=True)
    markdown = document_root / "normalized_document.md"
    markdown.write_text(
        "Table S1. Fractional atomic coordinates for EO-COF.\n"
        "<table><tr><th>Atom</th><th>x</th><th>y</th><th>z</th></tr>"
        "<tr><td>C34</td><td>0.1</td><td>0.2</td><td>0.3</td></tr>"
        "<tr><td>035</td><td>0.4</td><td>0.5</td><td>0.6</td></tr>"
        "<tr><td>C36</td><td>0.7</td><td>0.8</td><td>0.9</td></tr></table>\n",
        encoding="utf-8",
    )

    derived = _extract_markdown_tables(
        markdown_path=markdown,
        document_root=document_root,
        snapshot_root=tmp_path,
        document_id="doc_si",
        document_role="supplementary",
        canonical_blocks=[],
    )

    assert len(derived) == 1
    normalizations = derived[0]["source_ref"]["normalizations"]
    assert normalizations == [
        {
            "row_number": 3,
            "column": "Atom",
            "original": "035",
            "normalized": "O35",
            "rule": "leading_zero_to_oxygen_between_sequential_atom_labels",
        }
    ]
    table_path = next((document_root / "derived_tables").glob("table-*.tsv"))
    assert "O35\t0.4\t0.5\t0.6" in table_path.read_text(encoding="utf-8")


def test_layout_coordinate_block_extracts_strict_rows_across_pages() -> None:
    pages = [
        "9. Cartesian coordinates for the optimized structures\n\nCDI-CPP\n"
        "C  0.0  1.0  -2.0\nN  1.0  2.0  -3.0\nO  2.0  3.0  -4.0\n26\n",
        "SUPPORTING INFORMATION\nH  3.0  4.0  -5.0\nH  4.0  5.0  -6.0\n"
        "H  5.0  6.0  -7.0\nZero-point correction = 1.0\n",
    ]

    blocks = _layout_coordinate_blocks(pages)

    assert len(blocks) == 1
    assert blocks[0]["label"] == "CDI-CPP"
    assert len(blocks[0]["rows"]) == 6
    assert {row[0] for row in blocks[0]["rows"]} == {1, 2}
    assert blocks[0]["rows"][0][1:] == ("C", 0.0, 1.0, -2.0)


def test_layout_coordinate_page_marker_does_not_replace_structure_label() -> None:
    pages = [
        "Cartesian coordinates\nCatalyst-TS-A\n"
        "C 0.0 0.0 0.0\nH 0.0 0.0 1.0\nH 0.0 1.0 0.0\n"
        "Zero-point correction = 0.1\n",
        "S40\nH 1.0 0.0 0.0\nC 1.0 1.0 0.0\nO 1.0 0.0 1.0\n",
    ]

    blocks = _layout_coordinate_blocks(pages)

    assert len(blocks) == 2
    assert [block["label"] for block in blocks] == ["Catalyst-TS-A", "Catalyst-TS-A"]
    assert all(block["label_confidence"] == "medium" for block in blocks)


def test_markdown_pipe_table_is_exported_and_coverage_is_recorded(tmp_path: Path) -> None:
    document_root = tmp_path / "documents" / "doc_si"
    document_root.mkdir(parents=True)
    markdown = document_root / "normalized_document.md"
    markdown.write_text(
        "Table S2. Relative energies.\n\n"
        "| State | Energy (eV) |\n"
        "|:------|------------:|\n"
        "| A | -1.20 |\n"
        "| B | -0.75 |\n",
        encoding="utf-8",
    )

    derived = _extract_markdown_tables(
        markdown_path=markdown,
        document_root=document_root,
        snapshot_root=tmp_path,
        document_id="doc_si",
        document_role="supplementary",
        canonical_blocks=[],
    )

    assert len(derived) == 1
    assert derived[0]["source_ref"]["source_formats"] == ["markdown_pipe"]
    coverage = read_json(document_root / "derived_tables" / "coverage.json")
    assert coverage["coverage_status"] == "complete"
    assert coverage["source_format_counts"]["markdown_pipe"] == 1


def test_layout_gaussian_orientation_blocks_are_split_and_mapped() -> None:
    pages = [
        "5.3 Cartesian coordinates of optimized equilibrium geometries\n"
        "optimized S0 ground state equilibrium geometry of molecule A\n"
        "1 6 0 0.000000 1.000000 -2.000000\n"
        "2 8 0 1.000000 2.000000 -3.000000\n",
        "3 1 0 2.000000 3.000000 -4.000000\n4 1 0 3.000000 4.000000 -5.000000\n",
        "optimized 3npi* excited state equilibrium geometry of molecule A\n"
        "1 6 0 4.000000 5.000000 -6.000000\n"
        "2 8 0 5.000000 6.000000 -7.000000\n"
        "3 1 0 6.000000 7.000000 -8.000000\n",
    ]

    blocks = _layout_coordinate_blocks(pages)

    assert len(blocks) == 2
    assert blocks[0]["label"] == "optimized S0 ground state equilibrium geometry of molecule A"
    assert [row[1] for row in blocks[0]["rows"]] == ["C", "O", "H", "H"]
    assert blocks[0]["row_formats"] == ["gaussian_center_atomic_number_type_and_three_floats"]
    assert blocks[1]["label"] == "optimized 3npi* excited state equilibrium geometry of molecule A"
    assert len(blocks[1]["rows"]) == 3


def test_responses_bridge_closes_failed_tool_call_history() -> None:
    payload = {
        "model": "test-model",
        "input": [
            {
                "type": "function_call",
                "call_id": "call-truncated",
                "name": "exec_command",
                "arguments": '{"cmd":"printf partial',
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": "Continue."}],
            },
        ],
        "tools": [
            {
                "type": "function",
                "name": "exec_command",
                "parameters": {
                    "type": "object",
                    "properties": {"cmd": {"type": "string"}},
                    "required": ["cmd"],
                },
            }
        ],
    }

    chat, _ = responses_to_chat(payload)

    assert chat["messages"][0]["role"] == "assistant"
    assert json.loads(chat["messages"][0]["tool_calls"][0]["function"]["arguments"])
    assert chat["messages"][1]["role"] == "tool"
    assert chat["messages"][1]["tool_call_id"] == "call-truncated"
    assert "failed before execution" in chat["messages"][1]["content"]
    assert chat["messages"][2] == {"role": "user", "content": "Continue."}


def test_responses_bridge_does_not_mix_json_mode_with_tools() -> None:
    payload = {
        "model": "test-model",
        "input": [{"role": "user", "content": "Inspect the workspace."}],
        "tools": [
            {
                "type": "function",
                "name": "exec_command",
                "parameters": {
                    "type": "object",
                    "properties": {"cmd": {"type": "string"}},
                    "required": ["cmd"],
                },
            }
        ],
        "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
    }

    chat, _ = responses_to_chat(payload)

    assert chat["tool_choice"] == "auto"
    assert chat["tools"][0]["function"]["name"] == "exec_command"
    assert "response_format" not in chat


@pytest.mark.parametrize("alias", ["Bash", "shell", "bash"])
def test_responses_bridge_normalizes_relay_shell_aliases(alias: str) -> None:
    result = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "call-alias",
                            "type": "function",
                            "function": {
                                "name": alias,
                                "arguments": json.dumps(
                                    {"command": "python -m json.tool task.json"}
                                ),
                            },
                        }
                    ],
                }
            }
        ]
    }

    normalized = _normalize_returned_tool_aliases(
        result, allowed_names={"exec_command", "update_plan"}
    )

    function = normalized["choices"][0]["message"]["tool_calls"][0]["function"]
    assert function["name"] == "exec_command"
    assert json.loads(function["arguments"]) == {
        "cmd": "python -m json.tool task.json"
    }


def test_responses_bridge_does_not_remap_shell_alias_without_exec_command() -> None:
    result = {
        "choices": [
            {
                "message": {
                    "tool_calls": [
                        {
                            "function": {
                                "name": "Bash",
                                "arguments": '{"command":"true"}',
                            }
                        }
                    ]
                }
            }
        ]
    }

    normalized = _normalize_returned_tool_aliases(result, allowed_names={"Bash"})

    assert normalized["choices"][0]["message"]["tool_calls"][0]["function"][
        "name"
    ] == "Bash"


def test_responses_bridge_uses_json_mode_without_tools() -> None:
    payload = {
        "model": "test-model",
        "input": [{"role": "user", "content": "Return the final result."}],
        "text": {"format": {"type": "json_object"}},
    }

    chat, _ = responses_to_chat(payload)

    assert "tools" not in chat
    assert chat["response_format"] == {"type": "json_object"}


def test_responses_bridge_can_use_exact_json_schema_only_without_tools() -> None:
    schema = {
        "type": "object",
        "required": ["status"],
        "additionalProperties": False,
        "properties": {"status": {"const": "ok"}},
    }
    payload = {
        "model": "test-model",
        "input": [{"role": "user", "content": "Return the result."}],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "probe_result",
                "strict": True,
                "schema": schema,
            }
        },
    }

    chat, _ = responses_to_chat(payload, prefer_json_schema=True)

    assert chat["response_format"] == {
        "type": "json_schema",
        "json_schema": {
            "name": "probe_result",
            "strict": True,
            "schema": schema,
        },
    }
    assert json.dumps(schema, ensure_ascii=False, separators=(",", ":")) in chat["messages"][-1][
        "content"
    ]


def test_harness_accepts_single_object_phase_wrapper_for_terminal_reject(tmp_path) -> None:
    from src.agents.harness import AgentRunRequest, _validated_structured_response
    from src.agents.schemas import STAGE06_REVIEW_SCHEMA

    response = {
        "scientific_review": {
            "decision": "scientific_reject",
            "task_pair_id": "paper-1",
            "scientific_question": "Question",
            "public_scientific_question": "Public question",
            "workflow_summary": "Incomplete route",
            "workflow_steps": [],
            "public_task_basis": {},
            "paper_route": {},
            "ground_truth_items": [],
            "evidence_map": {},
            "toolbox_requirements": [],
            "resource_assessment": {},
            "reject_reasons": ["missing route parameter"],
            "warnings": [],
        }
    }
    request = AgentRunRequest(
        phase="stage06_scientific_review",
        record_id="paper-1",
        workspace=tmp_path,
        instructions="Review",
        output_schema=STAGE06_REVIEW_SCHEMA,
        prompt_version="test",
    )

    normalized = _validated_structured_response(response, request=request, workspace=tmp_path)

    assert normalized["decision"] == "scientific_reject"
    assert normalized["selected_candidate_id"] == ""
    assert normalized["stage05_candidate_disposition"] == ""
    assert normalized["task_direction"] == ""
    assert normalized["category"] == ""


def test_responses_bridge_enforces_hard_tool_budget(monkeypatch) -> None:
    captured: dict = {}

    class _Response:
        is_error = False

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [{"message": {"role": "assistant", "content": '{"ok":true}'}}],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            captured.update(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=1,
    )
    bridge.seen_tool_call_ids.add("call-1")
    bridge.tool_call_count = 1

    bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Finish."}],
            "tools": [{"type": "function", "name": "read_file"}],
            "text": {"format": {"type": "json_object"}},
        }
    )

    assert "tools" not in captured
    assert captured["response_format"] == {"type": "json_object"}
    assert captured["messages"][-1]["role"] == "system"
    assert "hard tool-call budget" in captured["messages"][-1]["content"]


def test_responses_bridge_keeps_native_write_tools_during_finalization(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs"
    result = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": "write-1",
                            "type": "function",
                            "function": {
                                "name": "write",
                                "arguments": json.dumps(
                                    {
                                        "file_path": "outputs/workflow_review.json",
                                        "content": "{}",
                                    }
                                ),
                            },
                        },
                        {
                            "id": "read-1",
                            "type": "function",
                            "function": {
                                "name": "read_file",
                                "arguments": json.dumps(
                                    {"file_path": "outputs/workflow_review.json"}
                                ),
                            },
                        },
                    ],
                }
            }
        ]
    }

    _retain_file_first_artifact_write_calls(result, destination=outputs)
    assert [
        call["id"] for call in result["choices"][0]["message"]["tool_calls"]
    ] == ["write-1"]

    fixed_file = outputs / "workflow_review.json"
    fixed_result = json.loads(json.dumps(result))
    _retain_structured_artifact_write_calls(fixed_result, destination=fixed_file)
    assert [
        call["id"] for call in fixed_result["choices"][0]["message"]["tool_calls"]
    ] == ["write-1"]


def test_responses_bridge_caps_one_parallel_tool_batch(monkeypatch) -> None:
    class _Response:
        is_error = False

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": f"call-{index}",
                                    "type": "function",
                                    "function": {
                                        "name": "exec_command",
                                        "arguments": '{"cmd":"true"}',
                                    },
                                }
                                for index in range(8)
                            ],
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=5,
        finalization_reserve=2,
    )

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Inspect."}],
            "tools": [{"type": "function", "name": "exec_command"}],
        }
    )

    calls = result["choices"][0]["message"]["tool_calls"]
    assert [call["id"] for call in calls] == ["call-0", "call-1", "call-2"]
    assert bridge.seen_tool_call_ids == {"call-0", "call-1", "call-2"}
    assert bridge.tool_call_count == 3


def test_responses_bridge_restores_reasoning_for_tool_history(monkeypatch) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False

        def __init__(self, body: dict) -> None:
            self._body = body

        def json(self) -> dict:
            return self._body

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            if len(requests) == 1:
                return _Response(
                    {
                        "model": "test-model",
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": "",
                                    "reasoning_content": "private tool-selection state",
                                    "tool_calls": [
                                        {
                                            "id": "call-reasoning",
                                            "type": "function",
                                            "function": {
                                                "name": "exec_command",
                                                "arguments": '{"cmd":"true"}',
                                            },
                                        }
                                    ],
                                }
                            }
                        ],
                    }
                )
            return _Response(
                {
                    "model": "test-model",
                    "choices": [{"message": {"role": "assistant", "content": '{"ok":true}'}}],
                }
            )

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=0,
    )
    bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Inspect."}],
            "tools": [{"type": "function", "name": "exec_command"}],
        }
    )
    bridge._call_upstream(
        {
            "model": "test-model",
            "input": [
                {
                    "type": "function_call",
                    "call_id": "call-reasoning",
                    "name": "exec_command",
                    "arguments": '{"cmd":"true"}',
                },
                {
                    "type": "function_call_output",
                    "call_id": "call-reasoning",
                    "output": "ok",
                },
            ],
            "tools": [{"type": "function", "name": "exec_command"}],
        }
    )

    assistant = next(
        message for message in requests[1]["messages"] if message["role"] == "assistant"
    )
    assert assistant["reasoning_content"] == "private tool-selection state"


def test_responses_bridge_warns_before_hard_tool_budget(monkeypatch) -> None:
    captured: dict = {}

    class _Response:
        is_error = False

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [{"message": {"role": "assistant", "content": '{"ok":true}'}}],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            captured.update(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=10,
        finalization_reserve=4,
    )
    bridge.seen_tool_call_ids.update(f"call-{index}" for index in range(6))
    bridge.tool_call_count = 6

    bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Continue."}],
            "tools": [{"type": "function", "name": "exec_command"}],
        }
    )

    assert "tools" in captured
    assert "search phase is over" in captured["messages"][-1]["content"]

    captured.clear()
    bridge.seen_tool_call_ids.add("call-finalization")
    bridge.tool_call_count = 7
    bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "The file write completed."}],
            "tools": [{"type": "function", "name": "exec_command"}],
        }
    )

    assert "tools" not in captured
    assert "finalization tool call has been consumed" in captured["messages"][-1]["content"]


def test_inline_bridge_reserves_only_final_submission_call(monkeypatch) -> None:
    captured: dict = {}

    class _Response:
        is_error = False

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [{"message": {"role": "assistant", "content": '{"ok":true}'}}],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            captured.update(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=False,
    )
    bridge.tool_call_count = 8

    bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Continue."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {"format": {"type": "json_object"}},
        }
    )

    assert captured["tools"][0]["function"]["name"] == "exec_command"
    assert "search phase is over" not in captured["messages"][-1]["content"]


def test_responses_bridge_recovers_textual_tool_protocol(monkeypatch) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None

        def __init__(self, body: dict) -> None:
            self._body = body
            self.text = json.dumps(body)

        def json(self) -> dict:
            return self._body

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            if len(requests) == 1:
                return _Response(
                    {
                        "model": "test-model",
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": ('<｜｜DSML｜｜invoke name="exec_command">bad call'),
                                }
                            }
                        ],
                    }
                )
            return _Response(
                {
                    "model": "test-model",
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": '{"decision":"scientific_reject"}',
                            }
                        }
                    ],
                }
            )

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
    )

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
        }
    )

    assert result["choices"][0]["message"]["content"] == ('{"decision":"scientific_reject"}')
    assert len(requests) == 2
    assert "tools" in requests[0]
    assert "tools" not in requests[1]
    assert "No tool was executed" in requests[1]["messages"][-1]["content"]


def test_responses_bridge_promotes_complete_dsml_tool_call(monkeypatch) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": (
                                "truncated earlier markup\n"
                                "</｜｜DSML｜｜invoke>\n"
                                '<｜｜DSML｜｜invoke name="exec_command">\n'
                                '<｜｜DSML｜｜parameter name="cmd" string="true">'
                                "python3 -c &quot;print('ok')&quot;"
                                "</｜｜DSML｜｜parameter>\n"
                                "</｜｜DSML｜｜invoke>\n"
                                "</｜｜DSML｜｜tool_calls>"
                            ),
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
    )

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [
                {
                    "type": "function",
                    "name": "exec_command",
                    "parameters": {
                        "type": "object",
                        "properties": {"cmd": {"type": "string"}},
                        "required": ["cmd"],
                    },
                }
            ],
        }
    )

    message = result["choices"][0]["message"]
    assert message["content"] == ""
    assert len(message["tool_calls"]) == 1
    assert message["tool_calls"][0]["function"]["name"] == "exec_command"
    assert json.loads(message["tool_calls"][0]["function"]["arguments"]) == {
        "cmd": "python3 -c \"print('ok')\""
    }
    assert bridge.tool_call_count == 1
    assert len(requests) == 1


def test_responses_bridge_retries_repeated_textual_tool_protocol(monkeypatch) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        def __init__(self, content: str) -> None:
            self._content = content

        def json(self) -> dict:
            return {
                "model": "test-model",
                "choices": [{"message": {"role": "assistant", "content": self._content}}],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            if len(requests) < 3:
                return _Response('<｜｜DSML｜｜invoke name="exec_command">bad')
            return _Response('{"decision":"scientific_reject"}')

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
    )

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
        }
    )

    assert result["choices"][0]["message"]["content"] == ('{"decision":"scientific_reject"}')
    assert len(requests) == 3
    assert all("tools" not in request for request in requests[1:])


def test_bridge_final_json_tool_uses_lightweight_document_and_is_consumed() -> None:
    payload = {
        "text": {
            "format": {
                "type": "json_schema",
                "schema": {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "properties": {"decision": {"type": "string"}},
                    "required": ["decision"],
                },
            }
        }
    }
    tool = _final_json_tool(payload)
    assert tool["function"]["parameters"]["required"] == ["document"]
    assert tool["function"]["parameters"]["properties"] == {
        "document": {
            "type": "string",
            "description": (
                "The complete serialized JSON object required by the response contract, "
                "without Markdown fences or surrounding prose."
            ),
        }
    }

    result = {
        "choices": [
            {
                "message": {
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call-final",
                            "type": "function",
                            "function": {
                                "name": "submit_final_json",
                                "arguments": json.dumps(
                                    {"document": '{"decision":"candidate_ready"}'}
                                ),
                            },
                        }
                    ],
                }
            }
        ]
    }
    converted = _consume_final_json_tool(result)
    message = converted["choices"][0]["message"]
    assert json.loads(message["content"]) == {"decision": "candidate_ready"}
    assert message["tool_calls"] == []


def test_bridge_can_finalize_structured_artifact_via_submission_tool(
    monkeypatch, tmp_path
) -> None:
    artifact = tmp_path / "outputs" / "scientific_review.json"
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "call-final",
                                    "type": "function",
                                    "function": {
                                        "name": "submit_final_json",
                                        "arguments": json.dumps(
                                            {
                                                "decision": "scientific_reject",
                                                "reject_reasons": ["Missing coordinates."],
                                            }
                                        ),
                                    },
                                }
                            ],
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=8,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
        structured_finalization_via_submit_tool=True,
    )
    bridge.tool_call_count = 4

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [
                {"role": "user", "content": "Complete the review."},
                {
                    "type": "function_call",
                    "call_id": "call-old",
                    "name": "exec_command",
                    "arguments": '{"cmd":"read evidence"}',
                },
                {
                    "type": "function_call_output",
                    "call_id": "call-old",
                    "output": "Observed evidence: coordinates are missing.",
                },
            ],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "required": ["decision", "reject_reasons"],
                        "properties": {
                            "decision": {"type": "string"},
                            "reject_reasons": {"type": "array"},
                        },
                    },
                }
            },
        }
    )

    assert [tool["function"]["name"] for tool in requests[0]["tools"]] == [
        "submit_final_json"
    ]
    assert requests[0]["tools"][0]["function"]["parameters"]["required"] == [
        "decision",
        "reject_reasons",
    ]
    assert "response_format" not in requests[0]
    assert not any(message["role"] in {"assistant", "tool"} for message in requests[0]["messages"])
    assert any(
        "Observed evidence: coordinates are missing." in message["content"]
        for message in requests[0]["messages"]
    )
    assert bridge.final_artifact_written is True
    assert json.loads(artifact.read_text()) == {
        "decision": "scientific_reject",
        "reject_reasons": ["Missing coordinates."],
    }
    assert json.loads(result["choices"][0]["message"]["content"])["decision"] == (
        "scientific_reject"
    )


def test_bridge_recovers_early_plain_text_with_structured_submission_tool(
    monkeypatch, tmp_path
) -> None:
    artifact = tmp_path / "outputs" / "scientific_review.json"
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        def __init__(self, payload: dict) -> None:
            self.payload = payload

        def json(self) -> dict:
            return self.payload

    responses = [
        _Response(
            {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Let me inspect one more evidence block.",
                        }
                    }
                ],
            }
        ),
        _Response(
            {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "call-final",
                                    "type": "function",
                                    "function": {
                                        "name": "submit_final_json",
                                        "arguments": json.dumps(
                                            {
                                                "decision": "scientific_reject",
                                                "reject_reasons": [
                                                    "Required spin state is not reported."
                                                ],
                                            }
                                        ),
                                    },
                                }
                            ],
                        }
                    }
                ],
            }
        ),
    ]

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return responses.pop(0)

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=24,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
        structured_finalization_via_submit_tool=True,
    )
    bridge.tool_call_count = 3

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [
                {"role": "user", "content": "Complete the review."},
                {
                    "type": "function_call",
                    "call_id": "call-old",
                    "name": "exec_command",
                    "arguments": '{"cmd":"read evidence"}',
                },
                {
                    "type": "function_call_output",
                    "call_id": "call-old",
                    "output": "The paper does not report a spin state.",
                },
            ],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "required": ["decision", "reject_reasons"],
                        "properties": {
                            "decision": {"type": "string"},
                            "reject_reasons": {"type": "array"},
                        },
                    },
                }
            },
        }
    )

    assert len(requests) == 2
    assert [tool["function"]["name"] for tool in requests[0]["tools"]] == [
        "exec_command"
    ]
    assert [tool["function"]["name"] for tool in requests[1]["tools"]] == [
        "submit_final_json"
    ]
    assert not any(
        message["role"] in {"assistant", "tool"}
        for message in requests[1]["messages"]
    )
    assert bridge.final_artifact_written is True
    assert json.loads(artifact.read_text()) == {
        "decision": "scientific_reject",
        "reject_reasons": ["Required spin state is not reported."],
    }
    assert json.loads(result["choices"][0]["message"]["content"]) == {
        "decision": "scientific_reject",
        "reject_reasons": ["Required spin state is not reported."],
    }


def test_bridge_structured_artifact_finalization_recovers_reasoning_json_atomically(
    monkeypatch, tmp_path
) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "reasoning_content": (
                                "Review complete.\n```json\n"
                                '{"decision":"scientific_reject"}'
                                "\n```"
                            ),
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    artifact = tmp_path / "outputs" / "scientific_review.json"
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        structured_finalization_max_tokens=32768,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
    )
    bridge.tool_call_count = 8

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {"decision": {"type": "string"}},
                        "required": ["decision"],
                    },
                }
            },
        }
    )

    assert [tool["function"]["name"] for tool in requests[0]["tools"]] == [
        "exec_command"
    ]
    assert requests[0]["max_tokens"] == 32768
    assert json.loads(artifact.read_text()) == {"decision": "scientific_reject"}
    assert bridge.final_artifact_written is True
    assert json.loads(result["choices"][0]["message"]["content"]) == {
        "decision": "scientific_reject"
    }


def test_bridge_artifact_recovery_retains_workspace_tool_and_accepts_json_fallback(
    monkeypatch, tmp_path
) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        def __init__(self, content: str) -> None:
            self.content = content

        def json(self) -> dict:
            return {
                "model": "test-model",
                "choices": [{"message": {"role": "assistant", "content": self.content}}],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            if len(requests) == 1:
                return _Response('<｜｜DSML｜｜invoke name="exec_command">search again')
            return _Response('{"decision":"scientific_reject"}')

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    artifact = tmp_path / "outputs" / "scientific_review.json"
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
    )
    bridge.tool_call_count = 8

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {"decision": {"type": "string"}},
                        "required": ["decision"],
                    },
                }
            },
        }
    )

    assert len(requests) == 2
    assert all(
        [tool["function"]["name"] for tool in request["tools"]] == ["exec_command"]
        for request in requests
    )
    assert json.loads(artifact.read_text()) == {"decision": "scientific_reject"}
    assert json.loads(result["choices"][0]["message"]["content"]) == {
        "decision": "scientific_reject"
    }


def test_bridge_does_not_accept_unchanged_preexisting_structured_artifact(
    monkeypatch, tmp_path
) -> None:
    artifact = tmp_path / "outputs" / "scientific_review.json"
    artifact.parent.mkdir(parents=True)
    artifact.write_text('{"decision":"candidate_ready"}\n', encoding="utf-8")
    requests: list[dict] = []

    class _Response:
        is_error = False

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": '{"decision":"scientific_reject"}',
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
    )

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {"decision": {"type": "string"}},
                        "required": ["decision"],
                    },
                }
            },
        }
    )

    assert len(requests) == 1
    assert bridge.final_artifact_written is False
    assert json.loads(result["choices"][0]["message"]["content"]) == {
        "decision": "scientific_reject"
    }


def test_bridge_returns_structured_artifact_changed_after_start_without_upstream_call(
    monkeypatch, tmp_path
) -> None:
    artifact = tmp_path / "outputs" / "scientific_review.json"
    artifact.parent.mkdir(parents=True)
    artifact.write_text('{"decision":"candidate_ready"}\n', encoding="utf-8")

    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
    )
    artifact.write_text('{"decision":"scientific_reject"}\n', encoding="utf-8")

    class _Client:
        def __init__(self, **_kwargs) -> None:
            raise AssertionError("a newly changed valid artifact must bypass the upstream model")

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {"decision": {"type": "string"}},
                        "required": ["decision"],
                    },
                }
            },
        }
    )

    assert bridge.final_artifact_written is True
    assert json.loads(result["choices"][0]["message"]["content"]) == {
        "decision": "scientific_reject"
    }


def test_bridge_does_not_finish_from_newly_initialized_placeholder_scaffold(
    monkeypatch, tmp_path
) -> None:
    artifact = tmp_path / "outputs" / "objective_audit.json"
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=8,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
    )
    artifact.parent.mkdir(parents=True)
    artifact.write_text(
        json.dumps(
            {
                "audit_summary": "issues_found",
                "rationale": "AGENT_REQUIRED: complete the audit",
            }
        ),
        encoding="utf-8",
    )
    requests: list[dict] = []

    class _Response:
        is_error = False

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": '{"audit_summary":"issues_found","rationale":"reviewed"}',
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Complete the audit."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "audit_summary": {"type": "string"},
                            "rationale": {"type": "string"},
                        },
                        "required": ["audit_summary", "rationale"],
                    },
                }
            },
        }
    )

    assert len(requests) == 1
    assert bridge.final_artifact_written is False
    assert json.loads(result["choices"][0]["message"]["content"])["rationale"] == "reviewed"


def test_bridge_finalization_blocks_search_and_keeps_target_write(
    monkeypatch, tmp_path
) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "call-search",
                                    "type": "function",
                                    "function": {
                                        "name": "exec_command",
                                        "arguments": json.dumps(
                                            {"cmd": "rg target inputs/evidence_index.json"}
                                        ),
                                    },
                                },
                                {
                                    "id": "call-write",
                                    "type": "function",
                                    "function": {
                                        "name": "exec_command",
                                        "arguments": json.dumps(
                                            {
                                                "cmd": (
                                                    "python -c \"import pathlib; "
                                                    "pathlib.Path('outputs/scientific_review.json')"
                                                    ".write_text('{}')\""
                                                )
                                            }
                                        ),
                                    },
                                },
                            ],
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    artifact = tmp_path / "outputs" / "scientific_review.json"
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
    )
    bridge.tool_call_count = 8

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {"type": "object"},
                }
            },
        }
    )

    calls = result["choices"][0]["message"]["tool_calls"]
    assert [call["id"] for call in calls] == ["call-write"]
    assert len(requests) == 1


def test_bridge_finalization_keeps_target_write_with_split_path(
    monkeypatch, tmp_path
) -> None:
    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "call-write",
                                    "type": "function",
                                    "function": {
                                        "name": "exec_command",
                                        "arguments": json.dumps(
                                            {
                                                "cmd": (
                                                    "python -c \"import pathlib; "
                                                    "target = pathlib.Path('outputs') / "
                                                    "'scientific_review.json'; "
                                                    "target.write_text('{}')\""
                                                )
                                            }
                                        ),
                                    },
                                }
                            ],
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=tmp_path / "outputs" / "scientific_review.json",
    )
    bridge.tool_call_count = 8

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
        }
    )

    assert [
        call["id"] for call in result["choices"][0]["message"]["tool_calls"]
    ] == ["call-write"]


def test_bridge_finalization_falls_back_to_tool_free_json_after_repeated_reads(
    monkeypatch, tmp_path
) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        def __init__(self, ordinal: int) -> None:
            self.ordinal = ordinal

        def json(self) -> dict:
            if self.ordinal < 3:
                return {
                    "model": "test-model",
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": "",
                                "tool_calls": [
                                    {
                                        "id": f"call-read-{self.ordinal}",
                                        "type": "function",
                                        "function": {
                                            "name": "exec_command",
                                            "arguments": json.dumps(
                                                {"cmd": "rg target inputs/evidence_index.json"}
                                            ),
                                        },
                                    }
                                ],
                            }
                        }
                    ],
                }
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": '{"decision":"scientific_reject"}',
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response(len(requests))

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    artifact = tmp_path / "outputs" / "scientific_review.json"
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=artifact,
    )
    bridge.tool_call_count = 8

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Review."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {"decision": {"type": "string"}},
                        "required": ["decision"],
                    },
                }
            },
        }
    )

    assert len(requests) == 3
    assert [tool["function"]["name"] for tool in requests[1]["tools"]] == [
        "exec_command"
    ]
    assert "tools" not in requests[2]
    assert json.loads(artifact.read_text()) == {"decision": "scientific_reject"}
    assert json.loads(result["choices"][0]["message"]["content"]) == {
        "decision": "scientific_reject"
    }


def test_bridge_recovers_blank_file_first_response_to_workspace_call(
    monkeypatch,
) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        def __init__(self, ordinal: int) -> None:
            self.ordinal = ordinal

        def json(self) -> dict:
            message: dict = {"role": "assistant", "content": ""}
            if self.ordinal == 2:
                message["tool_calls"] = [
                    {
                        "id": "call-write-task",
                        "type": "function",
                        "function": {
                            "name": "exec_command",
                            "arguments": json.dumps(
                                {"cmd": "mkdir -p task && printf task > task/task.md"}
                            ),
                        },
                    }
                ]
            return {"model": "test-model", "choices": [{"message": message}]}

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response(len(requests))

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=20,
        finalization_reserve=6,
        artifact_finalization_required=True,
    )

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Build task files."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
        }
    )

    assert len(requests) == 2
    assert [tool["function"]["name"] for tool in requests[1]["tools"]] == [
        "exec_command"
    ]
    assert result["choices"][0]["message"]["tool_calls"][0]["id"] == (
        "call-write-task"
    )


def test_bridge_file_first_finalization_blocks_reads_and_keeps_task_write(
    monkeypatch, tmp_path
) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "call-read",
                                    "type": "function",
                                    "function": {
                                        "name": "exec_command",
                                        "arguments": json.dumps(
                                            {"cmd": "cat task/data/inputs/a.xyz"}
                                        ),
                                    },
                                },
                                {
                                    "id": "call-write",
                                    "type": "function",
                                    "function": {
                                        "name": "exec_command",
                                        "arguments": json.dumps(
                                            {
                                                "cmd": (
                                                    "python -c \"from pathlib import Path; "
                                                    "Path('task/task.md').write_text('task')\""
                                                )
                                            }
                                        ),
                                    },
                                },
                            ],
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=20,
        finalization_reserve=6,
        artifact_finalization_required=True,
        file_first_artifact_path=tmp_path / "task",
        file_first_required_files=["task.md", "task_info.json"],
    )
    bridge.tool_call_count = 14

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Build task files."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
        }
    )

    assert len(requests) == 1
    assert [
        call["id"] for call in result["choices"][0]["message"]["tool_calls"]
    ] == ["call-write"]


def test_bridge_file_first_complete_forces_receipt_without_tools(
    monkeypatch, tmp_path
) -> None:
    task = tmp_path / "task"
    task.mkdir()
    for name in ("task.md", "task_info.json"):
        (task / name).write_text("{}", encoding="utf-8")
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": '{"status":"ready","artifact_path":"task"}',
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=20,
        finalization_reserve=6,
        artifact_finalization_required=True,
        file_first_artifact_path=task,
        file_first_required_files=["task.md", "task_info.json"],
    )
    bridge.tool_call_count = 0

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Finish."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
        }
    )

    assert "tools" not in requests[0]
    assert json.loads(result["choices"][0]["message"]["content"])["status"] == "ready"


def test_bridge_file_first_requires_declared_file_to_change_before_receipt(
    monkeypatch, tmp_path
) -> None:
    task = tmp_path / "task"
    task.mkdir()
    (task / "task.md").write_text("autonomous", encoding="utf-8")
    (task / "task_info.json").write_text("{}", encoding="utf-8")
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        @staticmethod
        def json() -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [
                                {
                                    "id": "call-write",
                                    "type": "function",
                                    "function": {
                                        "name": "exec_command",
                                        "arguments": json.dumps(
                                            {
                                                "cmd": (
                                                    "printf reproduction > task/task.md"
                                                )
                                            }
                                        ),
                                    },
                                }
                            ],
                        }
                    }
                ],
            }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response()

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=20,
        finalization_reserve=6,
        artifact_finalization_required=True,
        file_first_artifact_path=task,
        file_first_required_files=["task.md", "task_info.json"],
        file_first_required_modified_files=["task.md"],
    )
    bridge.tool_call_count = 14

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Convert the task."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
        }
    )

    assert "tools" in requests[0]
    assert result["choices"][0]["message"]["tool_calls"][0]["id"] == "call-write"


def test_bridge_finalization_rejects_read_only_open_and_recovers_to_write(
    monkeypatch, tmp_path
) -> None:
    requests: list[dict] = []

    class _Response:
        is_error = False
        status_code = 200
        request = None
        text = ""

        def __init__(self, call: dict) -> None:
            self.call = call

        def json(self) -> dict:
            return {
                "model": "test-model",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [self.call],
                        }
                    }
                ],
            }

    read_call = {
        "id": "call-read",
        "type": "function",
        "function": {
            "name": "exec_command",
            "arguments": json.dumps(
                {"cmd": "python -c \"print(open('outputs/objective_audit.json').read())\""}
            ),
        },
    }
    write_call = {
        "id": "call-write",
        "type": "function",
        "function": {
            "name": "exec_command",
            "arguments": json.dumps(
                {
                    "cmd": (
                        "python -c \"import pathlib; "
                        "pathlib.Path('outputs/objective_audit.json').write_text('{}')\""
                    )
                }
            ),
        },
    }

    class _Client:
        def __init__(self, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        @staticmethod
        def post(_url, *, headers, json):
            requests.append(json)
            return _Response(read_call if len(requests) == 1 else write_call)

    monkeypatch.setattr("src.agents.responses_bridge.httpx.Client", _Client)
    bridge = ResponsesBridge(
        upstream_base_url="https://example.test/v1",
        api_key="test",
        model="test-model",
        timeout_seconds=5,
        max_tool_calls=12,
        finalization_reserve=4,
        artifact_finalization_required=True,
        structured_artifact_path=tmp_path / "outputs" / "objective_audit.json",
    )
    bridge.tool_call_count = 8

    result, _ = bridge._call_upstream(
        {
            "model": "test-model",
            "input": [{"role": "user", "content": "Complete the audit."}],
            "tools": [{"type": "function", "name": "exec_command"}],
            "text": {"format": {"type": "json_schema", "schema": {"type": "object"}}},
        }
    )

    assert len(requests) == 2
    assert [call["id"] for call in result["choices"][0]["message"]["tool_calls"]] == [
        "call-write"
    ]


def test_bridge_structured_finalization_allows_native_sibling_outputs_only(tmp_path) -> None:
    """A receipt phase may finish its sibling artifacts under the same outputs tree."""

    def native_call(call_id: str, path: str) -> dict:
        return {
            "id": call_id,
            "type": "function",
            "function": {
                "name": "write",
                "arguments": json.dumps({"path": path, "content": "{}"}),
            },
        }

    result = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        native_call("call-sibling", "outputs/paper_reproduction/task.md"),
                        native_call("call-hidden", "outputs/hidden_reference/ground_truth_common.json"),
                        native_call("call-outside", "outside/escape.json"),
                    ],
                }
            }
        ]
    }

    filtered = _retain_structured_artifact_write_calls(
        result,
        destination=tmp_path / "outputs" / "construction_receipt.json",
    )

    assert [call["id"] for call in filtered["choices"][0]["message"]["tool_calls"]] == [
        "call-sibling",
        "call-hidden",
    ]


def _process_rubric(prefix: str) -> list[dict]:
    rubric = [
        {"id": f"{prefix}_design", "max_score": 40, "description": "Scientific design"},
        {"id": f"{prefix}_execution", "max_score": 35, "description": "Real execution"},
        {"id": f"{prefix}_validation", "max_score": 25, "description": "Validation"},
    ]
    if prefix == "reproduction":
        rubric[0].update(
            {
                "id": "paper_route_fidelity",
                "description": "Paper route fidelity and execution",
                "evidence": (
                    "report/research_plan.json; report/tool_trace.jsonl; report/report.md"
                ),
                "evidence_artifacts": [
                    "report/research_plan.json",
                    "report/tool_trace.jsonl",
                    "report/report.md",
                ],
            }
        )
    return rubric


def _mock_responses() -> dict[str, dict]:
    review = {
        "decision": "candidate_ready",
        "task_pair_id": "pair_test_reaction",
        "selected_candidate_id": "candidate-1",
        "stage05_candidate_disposition": "accepted_with_refined_workflow",
        "scientific_question": "Determine the relative stability of two supplied structures.",
        "public_scientific_question": "Determine the relative stability of the two supplied structures.",
        "task_direction": "conformer_thermochemistry_property_calibration",
        "category": "molecular_thermochemistry",
        "workflow_summary": "Optimize both structures, compute frequencies, and compare free energies.",
        "workflow_steps": [
            {
                "step_id": "s1",
                "action": "geometry optimization",
                "depends_on": [],
                "input_artifacts": ["structures.xyz"],
                "output_artifacts": ["optimized geometries"],
                "software": "ORCA",
                "method_parameters": {"method": "PBE0"},
                "evidence_ids": ["ev_main_1"],
            },
            {
                "step_id": "s2",
                "action": "frequency and thermochemistry calculation",
                "depends_on": ["s1"],
                "input_artifacts": ["optimized geometries"],
                "output_artifacts": ["free energies"],
                "software": "ORCA",
                "method_parameters": {"temperature_K": 298.15},
                "evidence_ids": ["ev_si_1"],
            },
        ],
        "public_task_basis": {
            "target_definition": "Relative Gibbs free energy and stability ordering",
            "background_facts": ["Both structures are neutral singlets."],
            "boundary_conditions": [
                {
                    "name": "charge_and_spin",
                    "value": "neutral closed-shell singlets",
                    "evidence_ids": ["ev_main_1"],
                },
                {
                    "name": "temperature",
                    "value": "298.15 K",
                    "evidence_ids": ["ev_si_1"],
                },
            ],
            "input_completeness": {
                "status": "confirmed",
                "closed_fields": [
                    "identity",
                    "geometry",
                    "charge",
                    "multiplicity",
                    "temperature",
                ],
                "unresolved_fields": [],
            },
            "input_assets": [
                {
                    "path": "structures.xyz",
                    "content": "2\nA\nH 0 0 0\nH 0 0 0.74\n2\nB\nH 0 0 0\nH 0 0 0.80\n",
                    "description": "Two starting structures",
                    "role": "computational_input",
                    "source_evidence_ids": ["ev_main_1"],
                    "provenance": {
                        "kind": "source_copy",
                        "derivation": "verbatim machine-readable coordinates from source",
                        "introduced_values": [],
                    },
                }
            ],
        },
        "paper_route": {
            "software": ["ORCA"],
            "method": "PBE0/def2-SVP optimization and frequency calculation",
            "autonomous_forbidden_disclosures": ["ORCA", "PBE0", "def2-SVP"],
            "steps": ["optimize", "frequency", "compare Gibbs free energies"],
            "evidence_ids": ["ev_main_1", "ev_si_1"],
            "route_completeness": {
                "status": "confirmed",
                "closed_fields": ["software", "method", "basis", "temperature"],
                "unresolved_fields": [],
            },
        },
        "ground_truth_items": [
            {
                "ground_truth_id": "gt-1",
                "kind": "numeric_final_result",
                "canonical_answer": {"delta_g_kcal_mol": 9.876},
                "required_propositions": [],
                "forbidden_contradictions": [],
                "acceptance_type": "numeric_tolerance",
                "acceptance_parameters": {"absolute_tolerance": 0.5},
                "evidence_grade": "A",
                "evidence_ids": ["ev_si_1"],
                "claim_role": "final",
            },
            {
                "ground_truth_id": "gt-2",
                "kind": "textual_intermediate_conclusion",
                "canonical_answer": "Structure A is the more stable conformer.",
                "required_propositions": ["Structure A is more stable than structure B."],
                "forbidden_contradictions": ["Structure B is more stable."],
                "acceptance_type": "semantic_propositions",
                "acceptance_parameters": {},
                "evidence_grade": "A",
                "evidence_ids": ["ev_si_1"],
                "claim_role": "intermediate",
            },
        ],
        "evidence_map": [
            {"role": "input", "evidence_ids": ["ev_main_1"]},
            {"role": "route", "evidence_ids": ["ev_main_1", "ev_si_1"]},
            {"role": "result", "evidence_ids": ["ev_si_1"]},
        ],
        "toolbox_requirements": [
            {
                "software": "ORCA",
                "capability": "frequency calculation",
                "status": "missing",
                "suggested_action": "Install ORCA before benchmark execution.",
                "evidence_ids": ["ev_main_1"],
            }
        ],
        "resource_assessment": {"status": "historically_calibrated", "walltime_hours": 2},
        "reject_reasons": [],
        "warnings": [],
    }
    autonomous = {
        "status": "ready",
        "task_info": {
            "task": (
                "Using the two supplied neutral closed-shell singlets at 298.15 K, "
                "determine their relative thermodynamic stability."
            ),
            "scientific_mode_description": "Choose and validate an independent computational route.",
            "scientific_requirements": ["Generate new computed evidence for both structures."],
            "required_deliverables": [
                {"path": "report/research_plan.json", "description": "Research plan"},
                {"path": "report/tool_trace.jsonl", "description": "Execution trace"},
                {"path": "report/report.md", "description": "Scientific report"},
                {"path": "report/results.json", "description": "Computed results"},
            ],
        },
        "task_markdown": (
            "Determine the relative stability of the two neutral closed-shell singlets "
            "at 298.15 K using new calculations."
        ),
        "task_spec": {"deliverable_summary": "Relative stability evidence"},
        "submission_contract": {
            "required_files": [
                "report/research_plan.json",
                "report/tool_trace.jsonl",
                "report/report.md",
                "report/results.json",
            ]
        },
        "process_rubric": _process_rubric("autonomous"),
        "invalid_reasons": [],
    }
    reproduction = {
        "status": "ready",
        "modified_files": [
            "task/task.md",
            "task/task_info.json",
            "task/task_spec.json",
            "task/process_rubric.json",
            "task/paper_route.md",
            "task/workflow_spec.json",
            "task/route_evidence_map.json",
            "task/derived_from.json",
            "task/public_manifest.json",
        ],
        "route_disclosure_summary": "Discloses the ORCA optimization and frequency route.",
        "task_info": {
            "task": (
                "Reproduce the neutral closed-shell singlets' relative-stability calculation "
                "at 298.15 K using the disclosed paper route."
            ),
            "scientific_mode_description": "Follow the supplied method and validate its outputs.",
            "scientific_requirements": ["Use the disclosed optimization and frequency workflow."],
            "required_deliverables": [
                {"path": "report/research_plan.json", "description": "Research plan"},
                {"path": "report/tool_trace.jsonl", "description": "Execution trace"},
                {"path": "report/report.md", "description": "Scientific report"},
                {"path": "report/results.json", "description": "Computed results"},
            ],
        },
        "task_markdown": (
            "For the neutral closed-shell singlets at 298.15 K, use ORCA with "
            "PBE0/def2-SVP to optimize and frequency-check both structures, then compare "
            "Gibbs free energies."
        ),
        "task_spec": {"deliverable_summary": "Paper-route relative stability evidence"},
        "submission_contract": {},
        "process_rubric": _process_rubric("reproduction"),
        "paper_route_markdown": "Optimize, calculate frequencies at 298.15 K, and compare Gibbs free energies.",
        "workflow_spec": {"steps": review["workflow_steps"]},
        "route_evidence_map": {"route": ["ev_main_1", "ev_si_1"]},
        "invalid_reasons": [],
    }
    hidden = {
        "status": "ready",
        "expected_result": {
            "delta_g_kcal_mol": 9.876,
            "stability_order": ["A", "B"],
        },
        "ground_truth_items": [
            {
                "ground_truth_id": "gt-1",
                "kind": "numeric_final_result",
                "canonical_answer": {"delta_g_kcal_mol": 9.876},
                "required_propositions": [],
                "forbidden_contradictions": [],
                "acceptance_type": "numeric_tolerance",
                "acceptance_parameters": {"absolute_tolerance": 0.5},
                "acceptance_profile_id": "ap-1",
                "evidence_grade": "A",
                "evidence_ids": ["ev_si_1"],
                "claim_role": "final",
                "applies_to_modes": ["autonomous_research", "paper_reproduction"],
            },
            {
                "ground_truth_id": "gt-2",
                "kind": "textual_intermediate_conclusion",
                "canonical_answer": "Structure A is the more stable conformer.",
                "required_propositions": ["Structure A is more stable than structure B."],
                "forbidden_contradictions": ["Structure B is more stable."],
                "acceptance_type": "semantic_propositions",
                "acceptance_parameters": {},
                "acceptance_profile_id": "ap-2",
                "evidence_grade": "A",
                "evidence_ids": ["ev_si_1"],
                "claim_role": "intermediate",
                "applies_to_modes": ["autonomous_research", "paper_reproduction"],
            },
        ],
        "acceptance_profiles": [
            {
                "acceptance_profile_id": "ap-1",
                "type": "numeric_tolerance",
                "target": 9.876,
                "unit": "kcal/mol",
                "absolute_tolerance": 0.5,
                "submission_binding": {
                    "artifact_paths": ["report/results.json"],
                    "observed_fields": ["$.delta_g_kcal_mol"],
                    "canonical_projection": {"delta_g_kcal_mol": 9.876},
                    "comparison": "numeric_tolerance",
                },
            },
            {
                "acceptance_profile_id": "ap-2",
                "type": "semantic_propositions",
                "required_propositions": ["Structure A is more stable than structure B."],
                "forbidden_contradictions": ["Structure B is more stable."],
                "submission_binding": {
                    "artifact_paths": ["report/report.md"],
                    "observed_fields": ["document"],
                    "canonical_projection": {
                        "required_propositions": ["Structure A is more stable than structure B."]
                    },
                    "comparison": "semantic_propositions",
                },
            },
        ],
        "scientific_conclusion_rubric": [
            {
                "id": "relative_free_energy",
                "max_score": 55,
                "statement": "The relative Gibbs free energy is recovered.",
                "acceptance_rule": "Accept 9.876 kcal/mol within 0.5 kcal/mol from new evidence.",
                "required_evidence": ["frequency outputs", "thermochemistry table"],
                "ground_truth_ids": ["gt-1"],
                "acceptance_profile_ids": ["ap-1"],
            },
            {
                "id": "stability_order",
                "max_score": 45,
                "statement": "Structure A is more stable than structure B.",
                "acceptance_rule": "Require the A before B ordering from newly computed free energies.",
                "required_evidence": ["artifact-linked free-energy comparison"],
                "ground_truth_ids": ["gt-2"],
                "acceptance_profile_ids": ["ap-2"],
            },
        ],
        "critical_failures": ["No real chemistry calculation was executed."],
        "reference_evidence": {"evidence_ids": ["ev_si_1"]},
        "evidence_gate_policy": {},
        "managed_computation_policy": {"required": True},
        "invalid_reasons": [],
    }
    return {
        "stage06_scientific_review": review,
        "stage06_autonomous_task": autonomous,
        "stage06_paper_reproduction": reproduction,
        "stage06_hidden_reference": hidden,
        "stage07_objective_audit": {
            "audit_summary": "issues_found",
            "outcomes": [
                {
                    "type": "task_cost_too_high",
                    "severity": "major",
                    "scope": "both_modes",
                    "details": "The configured resource policy is insufficient for the stated full workflow.",
                    "evidence_refs": ["resource_policy.json"],
                }
            ],
            "checks": [
                {
                    "check": "mode_pair_consistency",
                    "status": "passed",
                    "evidence_refs": ["construction_validation.json"],
                }
            ],
            "toolbox_assessment": {"status": "missing_required_software"},
            "cost_assessment": {"status": "over_budget"},
            "rationale": "The task pair is coherent but currently needs software and more resources.",
        },
        "stage07_audit_repair": {
            "audit_decision": "approved_with_repairs",
            "source_stage06_decision": "provisional_constructed",
            "original_task_pair_id": "pair_test_reaction",
            "final_task_pair_id": "pair_test_reaction",
            "artifact_path": "outputs/task_pair",
            "selected_workflow_preserved": True,
            "repair_origin": "stage06_candidate_repaired",
            "repairs": [
                {
                    "category": "toolbox_metadata",
                    "details": "Recorded the missing runtime without changing the workflow.",
                    "source_evidence_ids": ["ev_main_1"],
                    "changed_files": ["toolbox_requirements.json"],
                }
            ],
            "workflow_redesign": {"performed": False},
            "remaining_issues": [],
            "toolbox_status": "needs_software",
            "required_additions": [{"software": "ORCA"}],
            "resource_status": "high_cost",
            "summary": "The original workflow was retained and its metadata was repaired.",
        },
    }


def _single_agent_mock_responder(request: AgentRunRequest) -> dict:
    assert request.phase == "stage06_task_pair_builder"
    workspace = request.workspace
    outputs = workspace / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)

    def dump(path: Path, value) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    old = _mock_responses()
    review = old["stage06_scientific_review"]
    for step in review["workflow_steps"]:
        step["step_type"] = "core_computation"
    scope = {
        "kind": "full_paper_computational_workflow",
        "included_workflow_ids": ["workflow-main"],
        "excluded_workflow_ids": [],
        "included_claim_ids": ["relative-energy", "stability-order"],
        "excluded_claim_ids": [],
        "selection_rationale": "This is the complete computational workflow supporting the main claim.",
        "larger_scope_failure_reasons": [],
        "scope_evidence_ids": ["ev_main_1", "ev_si_1"],
    }
    complexity = {
        "level": "medium",
        "scientific_core_operation_count": 2,
        "estimated_min_tool_calls": 4,
        "estimated_typical_tool_calls": 6,
        "dependency_edge_count": 1,
        "parallel_branch_count": 2,
        "system_or_state_count": 2,
        "software_capability_count": 2,
        "iterative_decisions": [],
        "validation_operations": ["frequency validation of optimized structures"],
        "reasoning_requirements": ["compare thermochemistry across both structures"],
        "non_core_operations_excluded": ["file conversion", "report writing"],
    }
    review.update(
        {
            "paper_workflow_inventory_complete": True,
            "full_paper_workflow_checked": True,
            "alternative_scope_search_complete": True,
            "workflow_inventory": [
                {
                    "workflow_id": "workflow-main",
                    "description": "Optimization, frequency analysis, and stability comparison.",
                    "claim_ids": ["relative-energy", "stability-order"],
                    "evidence_ids": ["ev_main_1", "ev_si_1"],
                }
            ],
            "workflow_scope": scope,
            "complexity_profile": complexity,
            "failure_code": "",
            "failure_reasons": [],
        }
    )
    dump(outputs / "workflow_review.json", review)

    reproduction = outputs / "paper_reproduction"
    (reproduction / "data" / "inputs").mkdir(parents=True)
    structure_content = review["public_task_basis"]["input_assets"][0]["content"]
    (reproduction / "data" / "inputs" / "structures.xyz").write_text(
        structure_content, encoding="utf-8"
    )
    deliverables = old["stage06_paper_reproduction"]["task_info"]["required_deliverables"]
    task_text = (
        "Reproduce the relative stability of the two supplied neutral closed-shell singlets "
        "at 298.15 K. Use ORCA with PBE0/def2-SVP to optimize each structure, run frequency "
        "and thermochemistry calculations, validate the stationary points, and compare the "
        "resulting Gibbs free energies."
    )
    reproduction_info = {
        "task_id": "pair_test_reaction_reproduction",
        "task_pair_id": review["task_pair_id"],
        "source_id": "paper-test",
        "category": review["category"],
        "benchmark_family": review["task_direction"],
        "mode": "paper_reproduction",
        "task_mode": "guided_reproduction",
        "scientific_mode": "paper_reproduction",
        "method_disclosure": "paper_route_disclosed",
        "pathway_disclosure": "paper_route_disclosed",
        "task": task_text,
        "scientific_mode_description": "Follow and validate the disclosed paper route.",
        "scientific_requirements": ["Execute both optimization and frequency stages."],
        "required_deliverables": [
            {**row, "allow_empty": False} for row in deliverables
        ],
        "data": [
            {
                "name": "ResearchChemBench public inputs",
                "path": "data/inputs",
                "type": "directory",
                "description": "Structures and boundary conditions.",
            }
        ],
        "archive_extractions": [],
        "workflow_scope": scope,
        "complexity_profile": complexity,
    }
    reproduction_spec = {
        "task_id": reproduction_info["task_id"],
        "task_pair_id": review["task_pair_id"],
        "mode": "paper_reproduction",
        "task_mode": "guided_reproduction",
        "scientific_mode": "paper_reproduction",
        "method_disclosure": "paper_route_disclosed",
        "pathway_disclosure": "paper_route_disclosed",
        "scientific_question": review["public_scientific_question"],
        "target_definition": review["public_task_basis"]["target_definition"],
        "boundary_conditions": review["public_task_basis"]["boundary_conditions"],
        "input_assets": [
            {
                "path": "data/inputs/structures.xyz",
                "description": "Two supplied structures",
                "role": "computational_input",
                "source_evidence_ids": ["ev_main_1"],
            }
        ],
        "workflow_scope": scope,
        "complexity_profile": complexity,
    }
    submission = old["stage06_autonomous_task"]["submission_contract"]
    (reproduction / "task.md").write_text(task_text + "\n", encoding="utf-8")
    dump(reproduction / "task_info.json", reproduction_info)
    dump(reproduction / "task_spec.json", reproduction_spec)
    dump(reproduction / "submission_contract.json", submission)
    dump(reproduction / "process_rubric.json", _process_rubric("reproduction"))
    (reproduction / "paper_route.md").write_text(
        "Use ORCA PBE0/def2-SVP optimization followed by frequency thermochemistry.\n",
        encoding="utf-8",
    )
    dump(reproduction / "workflow_spec.json", {"steps": review["workflow_steps"]})
    dump(
        reproduction / "route_evidence_map.json",
        {"route": ["ev_main_1", "ev_si_1"]},
    )
    subprocess.run(
        [sys.executable, "inputs/scripts/validate_reproduction.py"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [sys.executable, "inputs/scripts/copy_reproduction_to_autonomous.py"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    )
    autonomous = outputs / "autonomous_research"
    autonomous_text = (
        "Determine the relative stability of the two supplied neutral closed-shell singlets at "
        "298.15 K. Design and execute a defensible multi-stage computational investigation, "
        "validate the resulting structures and thermochemistry, compare both systems, and support "
        "the conclusion with newly generated evidence."
    )
    autonomous_info = dict(reproduction_info)
    autonomous_info.update(
        {
            "task_id": "pair_test_reaction_autonomous",
            "mode": "autonomous_research",
            "task_mode": "open_discovery",
            "scientific_mode": "autonomous_research",
            "method_disclosure": "none",
            "pathway_disclosure": "none",
            "task": autonomous_text,
            "scientific_mode_description": "Design and validate an independent route.",
            "scientific_requirements": ["Generate new evidence for both structures."],
        }
    )
    autonomous_spec = dict(reproduction_spec)
    autonomous_spec.update(
        {
            "task_id": autonomous_info["task_id"],
            "mode": "autonomous_research",
            "task_mode": "open_discovery",
            "scientific_mode": "autonomous_research",
            "method_disclosure": "none",
            "pathway_disclosure": "none",
        }
    )
    (autonomous / "task.md").write_text(autonomous_text + "\n", encoding="utf-8")
    dump(autonomous / "task_info.json", autonomous_info)
    dump(autonomous / "task_spec.json", autonomous_spec)
    dump(autonomous / "process_rubric.json", _process_rubric("autonomous"))

    hidden = old["stage06_hidden_reference"]
    hidden_root = outputs / "hidden_reference"
    dump(hidden_root / "ground_truth_common.json", hidden)
    dump(hidden_root / "acceptance_profiles.json", hidden["acceptance_profiles"])
    dump(hidden_root / "conclusion_rubric.json", hidden["scientific_conclusion_rubric"])
    dump(hidden_root / "private_evidence_map.json", review["evidence_map"])
    dump(outputs / "toolbox_requirements.json", review["toolbox_requirements"])
    subprocess.run(
        [sys.executable, "inputs/scripts/validate_task_pair_draft.py"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    )
    receipt = {
        "decision": "constructed",
        "task_pair_id": review["task_pair_id"],
        "artifact_path": "outputs",
        "milestones": {
            "workflow_review_validated": True,
            "reproduction_validated": True,
            "autonomous_copy_created": True,
            "autonomous_validated": True,
            "hidden_reference_validated": True,
            "pair_draft_validated": True,
        },
        "workflow_scope_kind": scope["kind"],
        "complexity_level": complexity["level"],
        "failure_code": "",
        "failure_reasons": [],
        "summary": "Built a full-paper, non-trivial two-mode task pair.",
    }
    dump(outputs / "construction_receipt.json", receipt)
    return receipt


def test_scientific_review_accepts_mapping_evidence_map_without_crashing() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["evidence_map"] = {
        "ev_main_1": "input and route evidence",
        "ev_si_1": "result evidence",
    }

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert findings == []


def test_scientific_review_collects_singular_nonprefixed_evidence_id() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["evidence_map"] = [
        {"role": "input", "evidence_id": "source-block-17"},
        {"role": "route", "evidence_ids": ["ev_main_1", "ev_si_1"]},
    ]

    findings = validate_scientific_review(
        review, {"source-block-17", "ev_main_1", "ev_si_1"}
    )

    assert findings == []


def test_scientific_review_requires_structured_public_boundary_conditions() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["public_task_basis"].pop("boundary_conditions")

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert "public_boundary_conditions_missing" in findings
    assert "public_boundary_not_disclosed:temperature_k:298.15" in findings


def test_public_physical_environment_is_not_a_route_disclosure() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["workflow_steps"][0]["method_parameters"]["solvation"] = "PCM=water"
    review["paper_route"]["autonomous_forbidden_disclosures"].extend(
        ["PCM", "water", "DFT"]
    )
    review["public_task_basis"]["boundary_conditions"].append(
        {
            "name": "target_medium",
            "value": "water",
            "evidence_ids": ["ev_main_1"],
        }
    )

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert findings == []

    review["public_task_basis"]["boundary_conditions"][-1]["value"] = (
        "water target medium, implemented in the paper with PCM and DFT"
    )
    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert "review_public_route_disclosure:pcm" in findings
    assert "review_public_route_disclosure:dft" in findings


def test_boundary_value_in_unrelated_json_field_does_not_count_as_disclosure() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["workflow_steps"][0]["method_parameters"]["solvation"] = "PCM=water"
    review["public_task_basis"]["boundary_conditions"][1]["note"] = (
        "The word water appears here but this row is a temperature condition."
    )

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert "public_boundary_not_disclosed:solvation:water" in findings


def test_periodic_target_does_not_require_molecular_multiplicity_boundary() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["workflow_steps"][0]["method_parameters"]["multiplicity"] = 1
    review["public_task_basis"]["boundary_conditions"].append(
        {
            "name": "periodicity",
            "value": "periodic unit cell",
            "evidence_ids": ["ev_main_1"],
        }
    )

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert not any("multiplicity" in finding for finding in findings)


def test_ground_truth_numeric_profile_and_text_conflicts_are_detected() -> None:
    truths = [
        {
            "ground_truth_id": "gt-sign",
            "canonical_answer": {"energy_gap": -0.25},
            "required_propositions": ["The energy gap is positive."],
            "forbidden_contradictions": ["The energy gap is positive."],
        }
    ]

    findings = validate_ground_truth_consistency(truths)

    assert "ground_truth_required_forbidden_conflict:gt-sign" in findings
    assert "ground_truth_numeric_text_sign_conflict:gt-sign:energy_gap" in findings


def test_scientific_failure_requires_full_scope_search_and_checked_sources() -> None:
    review = {
        "decision": "scientific_not_constructible",
        "task_pair_id": "paper-test",
        "paper_workflow_inventory_complete": True,
        "full_paper_workflow_checked": True,
        "alternative_scope_search_complete": False,
        "workflow_inventory": [],
        "workflow_scope": {"kind": "none"},
        "complexity_profile": {"level": "not_assessed"},
        "evidence_map": [],
        "toolbox_requirements": [],
        "resource_assessment": {},
        "failure_code": "missing_core_input",
        "failure_reasons": [
            {
                "scope_attempted": "full_paper_computational_workflow",
                "code": "missing_core_input",
                "details": "A required structure could not be located.",
                "evidence_ids": [],
                "checked_sources": [],
            }
        ],
        "warnings": [],
    }

    findings = validate_workflow_review(review, set())

    assert "workflow_review_alternative_scope_search_complete_false" in findings
    assert "scientific_failure_checked_sources_missing:0" in findings


def test_task_boundary_and_route_isolation_are_enforced(tmp_path: Path) -> None:
    task = tmp_path / "task"
    task.mkdir()
    boundaries = [
        {"name": "target_medium", "value": "water", "evidence_ids": ["ev-1"]}
    ]
    (task / "task_spec.json").write_text(
        json.dumps({"boundary_conditions": boundaries}), encoding="utf-8"
    )
    (task / "task.md").write_text(
        "Determine the target properties in water and choose an independent route.",
        encoding="utf-8",
    )
    paper_route = {
        "software": ["ORCA"],
        "autonomous_forbidden_disclosures": ["ORCA", "water"],
    }

    assert validate_task_boundary_conditions(task, expected_conditions=boundaries) == []
    assert (
        validate_autonomous_route_isolation(
            task,
            paper_route=paper_route,
            allowed_boundary_conditions=boundaries,
        )
        == []
    )

    (task / "task.md").write_text(
        "Use ORCA in gas phase to determine the target properties.", encoding="utf-8"
    )
    assert "task_instruction_boundary_conflict:target_medium" in validate_task_boundary_conditions(
        task, expected_conditions=boundaries
    )
    assert "autonomous_route_disclosure:orca" in validate_autonomous_route_isolation(
        task,
        paper_route=paper_route,
        allowed_boundary_conditions=boundaries,
    )

    (task / "task.md").write_text(
        "Use water; it must not be replaced by gas phase, vacuum, or no solvent.",
        encoding="utf-8",
    )
    assert validate_task_boundary_conditions(task, expected_conditions=boundaries) == []


def test_scientific_review_rejects_public_and_route_answer_leakage() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["public_scientific_question"] = (
        "Determine whether the relative Gibbs free energy is 9.876 kcal/mol."
    )
    review["paper_route"]["expected_result"] = 9.876

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert "review_public_answer_leakage:gt-1" in findings
    assert "review_paper_route_answer_leakage:gt-1" in findings


def test_scientific_review_rejects_paper_method_in_autonomous_packet() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["public_task_basis"]["background_facts"].append("Use the paper's PBE0/def2-SVP method.")

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert "review_public_route_disclosure:pbe0" in findings
    assert "review_public_route_disclosure:def2-svp" in findings


def test_route_validation_and_comparison_artifacts_are_not_hidden_answers() -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review["workflow_steps"][0]["description"] = (
        "Verify stationary-point character and write a barrier comparison table."
    )

    findings = validate_scientific_review(review, {"ev_main_1", "ev_si_1"})

    assert "review_reproduction_route_uses_hidden_result" not in findings


def test_agent_task_contracts_are_normalized_for_evaluation() -> None:
    contract = _normalize_submission_contract(
        {
            "required_artifacts": [
                {"path": "deliverables/report.md"},
                {"path": "deliverables/results.json"},
            ]
        }
    )
    rubric = _normalize_process_rubric(
        {
            "total_points": 100,
            "criteria": [
                {"id": "design", "points": 40, "criterion": "Scientific design"},
                {
                    "id": "execution",
                    "max_points": 60,
                    "description": "Managed execution",
                },
            ],
        }
    )

    assert contract["required_files"] == [
        "deliverables/report.md",
        "deliverables/results.json",
    ]
    assert rubric == [
        {
            "id": "design",
            "points": 40,
            "criterion": "Scientific design",
            "max_score": 40,
            "description": "Scientific design",
        },
        {
            "id": "execution",
            "max_points": 60,
            "description": "Managed execution",
            "max_score": 60,
        },
    ]


def test_workflow_review_alias_normalization_is_syntax_only() -> None:
    review = {
        "workflow_steps": [
            {"step_id": "s1", "depends_on": [], "output_artifact": "optimized"},
            {"step_id": "s2", "depends_on": ["s1"], "output_artifact": "energy"},
        ],
        "workflow_inventory": [{"workflow_id": "wf-1", "claim_ids": ["claim-1"], "evidence_ids": ["ev-1"]}],
        "workflow_scope": {"scope_kind": "partial_computational_subworkflow", "included_workflows": ["wf-1"]},
        "complexity_profile": {"core_computation_count": 2, "tool_call_count": 4, "dependency_count": 1},
        "ground_truth_items": [{"item_id": "item-1", "type": "conclusion", "value": "A follows B."}],
    }

    normalized = _normalize_workflow_review_aliases(review)

    assert normalized["workflow_scope"]["kind"] == "partial_computational_subworkflow"
    assert normalized["workflow_scope"]["included_workflow_ids"] == ["wf-1"]
    assert normalized["workflow_scope"]["included_claim_ids"] == ["claim-1"]
    assert normalized["workflow_steps"][0]["output_artifacts"] == ["optimized"]
    assert normalized["complexity_profile"]["scientific_core_operation_count"] == 2
    assert normalized["complexity_profile"]["estimated_typical_tool_calls"] == 4
    assert normalized["ground_truth_items"][0]["ground_truth_id"] == "item-1"
    # Missing scientific inputs are not manufactured by normalization.
    assert "public_task_basis" not in normalized


def test_task_pair_bootstrap_creates_contract_scaffold_from_review(tmp_path: Path) -> None:
    review = _mock_responses()["stage06_scientific_review"]
    review.update(
        {
            "workflow_scope": {
                "kind": "full_paper_computational_workflow",
                "included_workflow_ids": ["workflow-main"],
                "included_claim_ids": ["relative-energy"],
                "selection_rationale": "Complete workflow.",
                "scope_evidence_ids": ["ev_main_1", "ev_si_1"],
            },
            "complexity_profile": {
                "level": "medium",
                "scientific_core_operation_count": 2,
                "estimated_min_tool_calls": 4,
                "estimated_typical_tool_calls": 6,
                "dependency_edge_count": 1,
                "parallel_branch_count": 2,
                "system_or_state_count": 2,
                "software_capability_count": 2,
                "iterative_decisions": [],
                "validation_operations": ["frequency check"],
                "reasoning_requirements": ["compare energies"],
                "non_core_operations_excluded": [],
            },
        }
    )
    root = tmp_path / "outputs"
    root.mkdir()
    (root / "workflow_review.json").write_text(json.dumps(review), encoding="utf-8")
    script = Path("src/stages/stage06_task_builder/bootstrap_task_pair.py").resolve()
    subprocess.run([sys.executable, str(script), str(root), str(root / "workflow_review.json")], check=True)

    reproduction = root / "paper_reproduction"
    assert (reproduction / "data" / "inputs" / "structures.xyz").is_file()
    info = read_json(reproduction / "task_info.json")
    assert info["source_id"] == "paper_source"
    assert info["task_mode"] == "guided_reproduction"
    hidden = read_json(root / "hidden_reference" / "ground_truth_common.json")
    assert hidden["status"] == "ready"
    assert len(hidden["ground_truth_items"]) == 2
    assert read_json(root / "toolbox_requirements.json")


def test_submission_contract_accepts_named_artifact_path_mapping() -> None:
    contract = _normalize_submission_contract(
        {
            "artifact_paths": {
                "report": {
                    "path": "report/report.md",
                    "format": "markdown",
                    "required": True,
                },
                "results": {
                    "path": "outputs/results.json",
                    "format": "json",
                    "required": True,
                },
            }
        }
    )

    assert contract["required_files"] == [
        "report/report.md",
        "outputs/results.json",
    ]


def test_hidden_setup_creates_frozen_scaffold_and_rejects_placeholders(
    tmp_path: Path,
) -> None:
    autonomous = tmp_path / "autonomous"
    reproduction = tmp_path / "reproduction"
    autonomous.mkdir()
    reproduction.mkdir()
    submission = {
        "required_files": [
            "report/report.md",
            "outputs/results.json",
            "outputs/excitation_energies.csv",
        ]
    }
    (autonomous / "submission_contract.json").write_text(
        json.dumps(submission), encoding="utf-8"
    )
    frozen = {
        "ground_truth_id": "gt-excitation",
        "kind": "numeric_tolerance",
        "canonical_answer": {"unit": "eV", "table": {"A": 1.25}},
        "required_propositions": ["A is the lowest state."],
        "forbidden_contradictions": ["A is not the lowest state."],
        "acceptance_type": "numeric_tolerance",
        "acceptance_parameters": {"tolerance_eV": 0.1},
        "evidence_grade": "A",
        "evidence_ids": ["ev-1"],
        "claim_role": "intermediate",
    }
    workspace = tmp_path / "workspace"

    _setup_hidden_inputs(
        workspace,
        review={
            "task_pair_id": "pair-test",
            "scientific_question": "Determine the excitation energy.",
            "ground_truth_items": [frozen],
        },
        autonomous_root=autonomous,
        reproduction_root=reproduction,
        evidence_index=[{"evidence_id": "ev-1"}],
    )

    assert sorted(path.name for path in (workspace / "inputs").iterdir()) == [
        "hidden_reference_packet.json",
        "hidden_reference_scaffold.json",
        "initialize_hidden_reference.py",
    ]
    subprocess.run(
        [sys.executable, str(workspace / "inputs" / "initialize_hidden_reference.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    scaffold = read_json(workspace / "outputs" / "ground_truth_common.json")
    assert scaffold["ground_truth_items"][0]["canonical_answer"] == frozen["canonical_answer"]
    assert scaffold["ground_truth_items"][0]["applies_to_modes"] == [
        "autonomous_research",
        "paper_reproduction",
    ]
    assert scaffold["acceptance_profiles"][0]["unit"] == "eV"
    assert scaffold["acceptance_profiles"][0]["absolute_tolerance"] == 0.1
    findings = validate_hidden_reference(
        scaffold,
        expected_ground_truth_items=[frozen],
        submission_contract=submission,
    )
    assert "acceptance_submission_binding_placeholder:ap-gt-excitation" in findings
    assert "conclusion_rubric_placeholder:conclusion-gt-excitation" in findings


def test_stage07_scaffold_initializes_and_requires_agent_judgment(tmp_path: Path) -> None:
    deterministic = {
        "outcomes": [
            {
                "type": "toolbox_capability_unknown",
                "severity": "major",
                "scope": "both_modes",
                "details": "The exact excited-state capability is unverified.",
                "evidence_refs": ["toolbox_requirements.json"],
                "source": "stage06_toolbox_requirement",
            }
        ],
        "pair_audit": {
            "passed": True,
            "autonomous_input_hash": "same-hash",
            "reproduction_input_hash": "same-hash",
        },
    }
    packet = {
        "toolbox_requirements": [{"software": "Gaussian", "status": "unknown"}],
        "resource_policy": {"cpu_cores": 48, "walltime_hours": 24},
    }
    scaffold = _stage07_audit_scaffold(deterministic, packet)
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "objective_audit_scaffold.json").write_text(
        json.dumps(scaffold), encoding="utf-8"
    )
    initializer = inputs / "initialize_objective_audit.py"
    initializer.write_text(_stage07_audit_initializer_script(), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(initializer)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    artifact = read_json(tmp_path / "outputs" / "objective_audit.json")
    assert artifact["audit_summary"] == "issues_found"
    assert artifact["outcomes"] == deterministic["outcomes"]
    assert artifact["checks"][1]["status"] == "passed"
    assert set(validate_agent_audit(artifact)) == {
        "audit_rationale_placeholder",
        "cost_assessment_placeholder",
        "toolbox_assessment_placeholder",
    }

    artifact["toolbox_assessment"]["status"] = "required capability remains unverified"
    artifact["cost_assessment"]["status"] = "not obviously over budget"
    artifact["rationale"] = "The task pair is complete; one toolbox capability remains unverified."
    assert validate_agent_audit(artifact) == []


def test_stage07_prompt_enforces_repair_before_workflow_redesign() -> None:
    prompt = audit_instructions(
        paper_id="paper-test",
        task_pair_id="pair-test",
        manifest_hash="abc123",
        max_tool_calls=24,
        finalization_reserve=6,
        source_stage06_decision="provisional_constructed",
    )

    repair_rule = "First audit and attempt to repair the workflow selected by Stage06"
    redesign_rule = "Only after recording an evidence-backed"
    assert repair_rule in prompt
    assert redesign_rule in prompt
    assert prompt.index(repair_rule) < prompt.index(redesign_rule)
    assert "Missing software never causes scientific rejection" in prompt
    assert "IS ALREADY POPULATED" in prompt
    assert "Never report `approved_with_repairs`" in prompt


def test_stage07_prompt_audits_the_entire_autonomous_public_surface() -> None:
    prompt = audit_instructions(
        paper_id="paper-test",
        task_pair_id="pair-test",
        manifest_hash="abc123",
        max_tool_calls=24,
        finalization_reserve=6,
        source_stage06_decision="provisional_constructed",
    )

    assert "MANDATORY AUTONOMOUS PUBLIC-SURFACE AUDIT" in prompt
    for required_surface in (
        "task.md",
        "task_info.json",
        "task_spec.json",
        "process_rubric.json",
        "public_manifest.json",
        "submission_contract.json",
    ):
        assert required_surface in prompt
    assert "Do not declare the mode clean after reading\nonly `task.md`" in prompt
    assert "paper labels such as `Int-*` or `TS-*`" in prompt
    assert "transition-state ring\n  size" in prompt
    assert "proton-shuttle/additional-molecule role" in prompt
    assert "XYZ\ncomment" in prompt
    assert "relative paths and file bytes must be identical" in prompt
    assert "preserve the atom-count line and every element/coordinate record exactly" in prompt
    assert "Do not rename, delete, or\nreplace the parent `data/inputs/` directory" in prompt
    assert "that does not prove its child files are read-only" in prompt
    assert "relative to the task-pair root `outputs/task_pair/`" in prompt
    assert "never `outputs/task_pair/autonomous_research/task.md`" in prompt


def test_stage07_retries_when_reported_repairs_were_not_delivered(tmp_path: Path) -> None:
    baseline = tmp_path / "inputs" / "stage06_candidate" / "autonomous_research"
    delivered = tmp_path / "outputs" / "task_pair" / "autonomous_research"
    baseline.mkdir(parents=True)
    delivered.mkdir(parents=True)
    (baseline / "task.md").write_text("unchanged", encoding="utf-8")
    (delivered / "task.md").write_text("unchanged", encoding="utf-8")
    response = {
        "audit_decision": "approved_with_repairs",
        "artifact_path": "outputs/task_pair",
        "repairs": [
            {
                "changed_files": ["autonomous_research/task.md"],
            }
        ],
        "workflow_redesign": {"changed_files": []},
    }
    result = SimpleNamespace(audit_record=lambda: {})

    with pytest.raises(AgentExecutionError, match="did not deliver its task tree"):
        _require_stage07_artifact_delivery(response, tmp_path, result)

    assert result.failure_class == "missing_agent_artifact"
    assert result.retryable is True

    (delivered / "task.md").write_text("actually repaired", encoding="utf-8")
    _require_stage07_artifact_delivery(
        response, tmp_path, SimpleNamespace(audit_record=lambda: {})
    )


def test_stage07_rejects_redundant_candidate_copy_in_delivery(tmp_path: Path) -> None:
    baseline = tmp_path / "inputs" / "stage06_candidate"
    delivered = tmp_path / "outputs" / "task_pair"
    baseline.mkdir(parents=True)
    delivered.mkdir(parents=True)
    (delivered / "paper_info.json").write_text("{}", encoding="utf-8")
    nested = delivered / "stage06_candidate"
    nested.mkdir()
    (nested / "paper_info.json").write_text("{}", encoding="utf-8")
    response = {
        "audit_decision": "approved",
        "artifact_path": "outputs/task_pair",
        "repairs": [],
        "workflow_redesign": {"changed_files": []},
    }

    with pytest.raises(AgentExecutionError, match="did not deliver its task tree"):
        _require_stage07_artifact_delivery(
            response, tmp_path, SimpleNamespace(audit_record=lambda: {})
        )


def test_stage07_pair_manifest_ignores_volatile_construction_record(tmp_path: Path) -> None:
    (tmp_path / "task.md").write_text("stable task", encoding="utf-8")
    (tmp_path / "paper_info.json").write_text(
        '{"doi":"10.0000/test","constructed_at":"first"}', encoding="utf-8"
    )
    (tmp_path / "construction_record.json").write_text(
        '{"cache_hit":false,"created_at":"first"}', encoding="utf-8"
    )
    first = _audit_pair_manifest(tmp_path)["content_hash"]

    (tmp_path / "construction_record.json").write_text(
        '{"cache_hit":true,"created_at":"second"}', encoding="utf-8"
    )
    (tmp_path / "paper_info.json").write_text(
        '{"doi":"10.0000/test","constructed_at":"second"}', encoding="utf-8"
    )
    assert _audit_pair_manifest(tmp_path)["content_hash"] == first

    (tmp_path / "paper_info.json").write_text(
        '{"doi":"10.0000/changed","constructed_at":"second"}', encoding="utf-8"
    )
    assert _audit_pair_manifest(tmp_path)["content_hash"] != first


def test_stage07_safely_migrates_legacy_checkpoint_from_matching_workspace(
    tmp_path: Path,
) -> None:
    stage_root = tmp_path / "stage07"
    previous = stage_root / "workspaces" / "paper" / "objective_audit" / "attempt-01"
    pair = previous / "inputs" / "task_pair"
    pair.mkdir(parents=True)
    (pair / "task.md").write_text("stable task", encoding="utf-8")
    toolbox = {"backends": ["gaussian"]}
    resource_policy = {"cpu_cores": 48}
    (previous / "inputs" / "toolbox_snapshot.json").write_text(
        json.dumps(toolbox), encoding="utf-8"
    )
    (previous / "inputs" / "resource_policy.json").write_text(
        json.dumps(resource_policy), encoding="utf-8"
    )
    cached = {
        "prompt_version": STAGE07_AUDIT_VERSION,
        "agent_run": {
            "workspace": str(previous),
            "harness": "codex",
            "model": "test-model",
        },
    }

    assert _cached_audit_inputs_match(
        cached,
        stage_root=stage_root,
        pair_manifest_hash=_audit_pair_manifest(pair)["content_hash"],
        toolbox=toolbox,
        resource_policy=resource_policy,
        harness_name="codex",
        model_name="test-model",
    )
    assert not _cached_audit_inputs_match(
        cached,
        stage_root=stage_root,
        pair_manifest_hash=_audit_pair_manifest(pair)["content_hash"],
        toolbox={"backends": ["orca"]},
        resource_policy=resource_policy,
        harness_name="codex",
        model_name="test-model",
    )


def test_stage07_merges_same_outcome_supported_by_overlapping_evidence() -> None:
    deterministic = [
        {
            "type": "toolbox_capability_unknown",
            "severity": "blocking",
            "scope": "both_modes",
            "details": "Verify TD-DFT root analysis.",
            "evidence_refs": ["ev_method", "ev_state"],
            "source": "stage06_toolbox_requirement",
        }
    ]
    agent = [
        {
            "type": "toolbox_capability_unknown",
            "severity": "blocking",
            "scope": "both_modes",
            "details": "The deployed backend has not verified this exact capability.",
            "evidence_refs": ["ev_method", "inputs/audit_packet.json#/toolbox_focus"],
            "source": "stage06_toolbox_requirement",
        }
    ]

    assert merge_audit_outcomes(deterministic, agent) == deterministic


def _document(tmp_path: Path, document_id: str, role: str, evidence_id: str) -> dict:
    root = tmp_path / document_id
    root.mkdir()
    source_structures = root / "structures.xyz"
    source_structures.write_text(
        "2\nA\nH 0 0 0\nH 0 0 0.74\n2\nB\nH 0 0 0\nH 0 0 0.80\n",
        encoding="utf-8",
    )
    markdown = root / "normalized_document.md"
    markdown.write_text(
        "# Test computational chemistry paper\n\nMethods and results are available.\n",
        encoding="utf-8",
    )
    blocks = root / "content_blocks.jsonl"
    blocks.write_text(
        json.dumps(
            {
                "evidence_id": evidence_id,
                "document_id": document_id,
                "section_path": ["Computational Methods"],
                "block_type": "paragraph",
                "text": (
                    "ORCA optimization and frequency calculations support the reported stability. "
                    f"Machine-readable XYZ: documents/{document_id}/parser_structured/"
                    "structures.xyz"
                ),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "metadata.json").write_text(
        json.dumps(
            {"parser_output": {"content_list_v2_path": str(source_structures)}}
        ),
        encoding="utf-8",
    )
    return {
        "paper_id": "paper-test",
        "document_id": document_id,
        "document_role": role,
        "decision": "pass",
        "file_name": f"{document_id}.pdf",
        "sha256": f"sha-{document_id}",
        "doi": "10.0000/test",
        "journal_name": "Test Journal",
        "source_remote_uri": f"s3://bucket/{document_id}.pdf",
        "normalized_markdown_path": str(markdown),
        "content_blocks_path": str(blocks),
    }


def test_agent_command_adapters_are_configurable(tmp_path: Path) -> None:
    request = AgentRunRequest(
        phase="test",
        record_id="record",
        workspace=tmp_path,
        instructions="Return JSON.",
        output_schema=AGENT_SUMMARY_SCHEMA,
        prompt_version="v1",
    )
    model = {"model": "model-x", "base_url": "https://example.test/v1"}
    codex = create_agent_harness("codex", config={}, model_config=model)
    claude = create_agent_harness("claude", config={}, model_config=model)
    opencode = create_agent_harness("opencode", config={}, model_config=model)

    assert codex.command_preview(request)[:2] == ["codex", "exec"]
    assert "--output-schema" in codex.command_preview(request)
    assert claude.command_preview(request)[:2] == ["claude", "-p"]
    assert opencode.command_preview(request)[:2] == ["opencode", "run"]


def test_stage06_single_agent_builds_reproduction_first_task_pair(tmp_path: Path) -> None:
    toolbox = tmp_path / "toolbox.json"
    toolbox.write_text(json.dumps({"profile_id": "test", "backends": {}}), encoding="utf-8")
    documents = [
        _document(tmp_path, "doc-main", "main_paper", "ev_main_1"),
        _document(tmp_path, "doc-si", "supplementary", "ev_si_1"),
    ]
    config = {
        "harness": "mock",
        "workers": 1,
        "max_attempts": 1,
        "resume": True,
        "toolbox_capabilities": str(toolbox),
        "mock_responder": _single_agent_mock_responder,
    }
    stage04_records = [
        {
            "paper_id": "paper-test",
            "passed": True,
            "resource_profile": {"walltime_hours": 4},
        }
    ]
    output = run_stage06(
        candidates=[{"paper_id": "paper-test", "candidate_id": "candidate-1"}],
        stage04_records=stage04_records,
        documents=documents,
        config=config,
        model=_Model(),
        workspace=tmp_path / "run",
        run_id="single-agent-test",
    )

    record = output["records"][0]
    assert record["decision"] == "provisional_constructed"
    assert record["handoff_ready"] is True
    assert record["workflow_scope_kind"] == "full_paper_computational_workflow"
    assert record["complexity_level"] == "medium"
    pair = Path(record["task_pair_path"])
    assert validate_task_pair(pair)["passed"] is True
    construction = read_json(pair / "construction_record.json")
    assert construction["mode_generation_order"] == [
        "paper_reproduction",
        "autonomous_research",
    ]
    assert construction["mode_generation_strategy"] == "single_agent"
    assert set(construction["phase_audits"]) == {"task_pair_builder"}
    derived = read_json(pair / "autonomous_research" / "derived_from.json")
    assert derived["derived_from_mode"] == "paper_reproduction"
    assert not (pair / "autonomous_research" / "paper_route.md").exists()
    assert (pair / "paper_reproduction" / "paper_route.md").is_file()
    audit_packet = _stage07_audit_packet(
        pair_root=pair,
        pair_manifest=_audit_pair_manifest(pair),
        deterministic={},
        toolbox={},
        resource_policy={},
    )
    assert (
        audit_packet["workflow_selection"]["workflow_scope"]["kind"]
        == "full_paper_computational_workflow"
    )
    assert audit_packet["workflow_selection"]["complexity_profile"]["level"] == "medium"
    assert audit_packet["source_evidence_bundle"]["included_count"] >= 2

    rerun = run_stage06(
        candidates=[{"paper_id": "paper-test", "candidate_id": "candidate-1"}],
        stage04_records=stage04_records,
        documents=documents,
        config=config,
        model=_Model(),
        workspace=tmp_path / "run",
        run_id="single-agent-test",
    )
    assert rerun["records"][0]["decision"] == "provisional_constructed"
    rerun_pair = Path(rerun["records"][0]["task_pair_path"])
    assert read_json(rerun_pair / "construction_record.json")["phase_audits"][
        "task_pair_builder"
    ]["cache_hit"] is True


def test_stage06_hands_partial_candidate_to_stage07_without_content_retry(
    tmp_path: Path,
) -> None:
    toolbox = tmp_path / "toolbox.json"
    toolbox.write_text(json.dumps({"profile_id": "test", "backends": {}}), encoding="utf-8")
    documents = [
        _document(tmp_path, "doc-main", "main_paper", "ev_main_1"),
        _document(tmp_path, "doc-si", "supplementary", "ev_si_1"),
    ]
    calls = 0

    def partial_responder(request: AgentRunRequest) -> dict:
        nonlocal calls
        calls += 1
        receipt = _single_agent_mock_responder(request)
        shutil.rmtree(request.workspace / "outputs" / "autonomous_research")
        return receipt

    result = run_stage06(
        candidates=[{"paper_id": "paper-test", "candidate_id": "candidate-1"}],
        stage04_records=[
            {
                "paper_id": "paper-test",
                "passed": True,
                "resource_profile": {"walltime_hours": 4},
            }
        ],
        documents=documents,
        config={
            "harness": "mock",
            "workers": 1,
            "max_attempts": 3,
            "resume": False,
            "retry_backoff_seconds": 0,
            "toolbox_capabilities": str(toolbox),
            "mock_responder": partial_responder,
        },
        model=_Model(),
        workspace=tmp_path / "run",
        run_id="partial-handoff-test",
    )

    record = result["records"][0]
    assert calls == 1
    assert record["decision"] == "provisional_constructed"
    assert record["handoff_ready"] is True
    assert "candidate_task_tree_incomplete_stage07_review_required" in record[
        "handoff_warnings"
    ]
    assert Path(record["handoff_path"]).is_dir()


def test_pair_contract_normalizer_repairs_harness_field_drift(tmp_path: Path) -> None:
    toolbox = tmp_path / "toolbox.json"
    toolbox.write_text(json.dumps({"profile_id": "test", "backends": {}}), encoding="utf-8")
    documents = [
        _document(tmp_path, "doc-main", "main_paper", "ev_main_1"),
        _document(tmp_path, "doc-si", "supplementary", "ev_si_1"),
    ]
    output = run_stage06(
        candidates=[{"paper_id": "paper-test", "candidate_id": "candidate-1"}],
        stage04_records=[
            {
                "paper_id": "paper-test",
                "passed": True,
                "resource_profile": {"walltime_hours": 4},
            }
        ],
        documents=documents,
        config={
            "harness": "mock",
            "workers": 1,
            "max_attempts": 1,
            "resume": True,
            "toolbox_capabilities": str(toolbox),
            "mock_responder": _single_agent_mock_responder,
        },
        model=_Model(),
        workspace=tmp_path / "run",
        run_id="normalizer-test",
    )
    pair = Path(output["records"][0]["task_pair_path"])
    review = read_json(pair / "workflow_review.json")

    autonomous_info = read_json(pair / "autonomous_research" / "task_info.json")
    autonomous_info["task_mode"] = "autonomous_research"
    autonomous_info["workflow_scope"] = {"kind": "model_rewrite"}
    (pair / "autonomous_research" / "task_info.json").write_text(
        json.dumps(autonomous_info), encoding="utf-8"
    )
    reproduction_spec = read_json(pair / "paper_reproduction" / "task_spec.json")
    reproduction_spec["scientific_question"] = "A later model rewrite changed the target."
    reproduction_spec["complexity_profile"] = {"level": "low_complexity_trivial"}
    (pair / "paper_reproduction" / "task_spec.json").write_text(
        json.dumps(reproduction_spec), encoding="utf-8"
    )

    hidden_path = pair / "hidden_reference" / "ground_truth_common.json"
    hidden = read_json(hidden_path)
    for truth in hidden["ground_truth_items"]:
        truth["item_id"] = truth.pop("ground_truth_id")
        truth["acceptance_profile_id"] = "shared-profile"
    hidden["acceptance_profiles"] = [
        {
            "acceptance_profile_id": "shared-profile",
            "type": "numeric_tolerance",
            "unit": "kcal/mol",
        }
    ]
    hidden["scientific_conclusion_rubric"] = [
        {"id": "incomplete", "max_score": 100, "description": "model shorthand"}
    ]
    hidden_path.write_text(json.dumps(hidden), encoding="utf-8")
    (pair / "hidden_reference" / "acceptance_profiles.json").write_text(
        json.dumps({"profiles": hidden["acceptance_profiles"]}), encoding="utf-8"
    )
    (pair / "hidden_reference" / "conclusion_rubric.json").write_text(
        json.dumps({"rubric": hidden["scientific_conclusion_rubric"]}), encoding="utf-8"
    )
    review["toolbox_requirements"] = [{"software": "ORCA", "available": True}]

    assert _normalize_task_pair_artifact_contracts(pair, review) == []
    assert validate_task_pair_draft(pair, review=review) == []
    assert read_json(pair / "autonomous_research" / "task_info.json")[
        "task_mode"
    ] == "open_discovery"
    repaired_hidden = read_json(hidden_path)
    assert len(repaired_hidden["acceptance_profiles"]) == len(
        repaired_hidden["ground_truth_items"]
    )
    assert read_json(pair / "hidden_reference" / "acceptance_profiles.json") == repaired_hidden[
        "acceptance_profiles"
    ]


def test_stage06_builds_isolated_task_pair_with_toolbox_gap(tmp_path: Path) -> None:
    toolbox = tmp_path / "toolbox.json"
    toolbox.write_text(json.dumps({"profile_id": "test", "backends": {}}), encoding="utf-8")
    documents = [
        _document(tmp_path, "doc-main", "main_paper", "ev_main_1"),
        _document(tmp_path, "doc-si", "supplementary", "ev_si_1"),
    ]
    config = {
        "harness": "mock",
        "mode_generation_strategy": "legacy_multi_phase",
        "workers": 1,
        "max_attempts": 1,
        "resume": True,
        "toolbox_capabilities": str(toolbox),
        "mock_responses": _mock_responses(),
    }
    stage04_records = [
        {
            "paper_id": "paper-test",
            "passed": True,
            "resource_profile": {"walltime_hours": 4},
        }
    ]
    output = run_stage06(
        candidates=[{"paper_id": "paper-test", "candidate_id": "candidate-1"}],
        stage04_records=stage04_records,
        documents=documents,
        config=config,
        model=_Model(),
        workspace=tmp_path / "run",
        run_id="test-run",
    )

    record = output["records"][0]
    assert record["decision"] == "constructed"
    assert record["toolbox_gap_present"] is True
    pair = Path(record["task_pair_path"])
    assert (pair / "paper_info.json").is_file()
    assert not (pair / "autonomous_research" / "paper_route.md").exists()
    assert (pair / "paper_reproduction" / "paper_route.md").is_file()
    assert (pair / "hidden_reference" / "ground_truth_common.json").is_file()
    assert not (pair / "autonomous_research" / "hidden_reference").exists()
    assert not (pair / "paper_reproduction" / "hidden_reference").exists()
    assert validate_task_pair(pair)["passed"] is True
    for mode, task_mode, suffix in (
        ("autonomous_research", "open_discovery", "_autonomous"),
        ("paper_reproduction", "guided_reproduction", "_reproduction"),
    ):
        task_info = read_json(pair / mode / "task_info.json")
        task_spec = read_json(pair / mode / "task_spec.json")
        assert task_info["mode"] == mode
        assert task_info["scientific_mode"] == mode
        assert task_info["task_mode"] == task_mode
        assert task_info["task_id"].endswith(suffix)
        assert task_spec["mode"] == mode
        assert task_spec["scientific_mode"] == mode
        assert task_spec["task_mode"] == task_mode
        assert task_spec["task_id"] == task_info["task_id"]
        assert task_spec["task_pair_id"] == task_info["task_pair_id"]

    autonomous_truth = read_json(pair / "hidden_reference" / "ground_truth_autonomous.json")
    reproduction_truth = read_json(pair / "hidden_reference" / "ground_truth_reproduction.json")
    assert (
        autonomous_truth["scientific_conclusion_rubric"]
        == reproduction_truth["scientific_conclusion_rubric"]
    )
    assert autonomous_truth["scoring_rubric"] != reproduction_truth["scoring_rubric"]

    rerun = run_stage06(
        candidates=[{"paper_id": "paper-test", "candidate_id": "candidate-1"}],
        stage04_records=stage04_records,
        documents=documents,
        config=config,
        model=_Model(),
        workspace=tmp_path / "run",
        run_id="test-run",
    )
    assert rerun["records"][0]["decision"] == "constructed"
    rerun_pair = Path(rerun["records"][0]["task_pair_path"])
    phase_audits = read_json(rerun_pair / "construction_record.json")["phase_audits"]
    assert all(
        phase_audits[phase]["cache_hit"]
        for phase in ("review", "autonomous", "reproduction", "hidden_reference")
    )

    judge_model = _Model()
    judge_model.role = "judge"

    def stage07_responder(request: AgentRunRequest) -> dict:
        response = _mock_responses()[request.phase]
        requirements_path = request.workspace / "outputs" / "task_pair" / "toolbox_requirements.json"
        requirements = read_json(requirements_path)
        if isinstance(requirements, dict):
            requirements["stage07_verified"] = True
        else:
            requirements.append(
                {
                    "software": "ORCA",
                    "status": "missing",
                    "stage07_verified": True,
                }
            )
        write_json(requirements_path, requirements)
        return response

    stage07 = run_stage07(
        build_records=output["records"],
        documents=documents,
        config={
            **config,
            "mock_responses": _mock_responses(),
            "mock_responder": stage07_responder,
            "resource_policy": {"walltime_hours": 1},
        },
        model=judge_model,
        workspace=tmp_path / "run",
        run_id="test-run",
    )
    audit = stage07["records"][0]
    assert audit["audit_decision"] == "approved_with_repairs"
    assert audit["selected_workflow_preserved"] is True
    assert audit["toolbox_status"] == "needs_software"
    assert Path(audit["task_pair_path"]).is_dir()
    assert not (Path(audit["audit_path"]) / "gold_run").exists()


def test_stage06_canonicalizes_stale_and_wildcard_evidence_ids() -> None:
    canonical = {
        "ev_doc_abc123_000009_cafebabe",
        "ev_doc_def456_000233_d7ebf11f41ba",
    }
    review = {
        "scope": [
            "ev_doc_abc123_000009_deadbeef",
            "ev_doc_def456_000233_*",
            "ev_derived_doc_def456_d7ebf11f41ba",
        ]
    }

    normalized = _canonicalize_review_evidence_ids(review, canonical)

    assert normalized["scope"] == [
        "ev_doc_abc123_000009_cafebabe",
        "ev_doc_def456_000233_d7ebf11f41ba",
        "ev_doc_def456_000233_d7ebf11f41ba",
    ]


def test_stage06_normalizes_only_scientific_failure_aliases() -> None:
    normalized = _normalize_scientific_failure_contract(
        {
            "decision": "scientific_not_constructible",
            "failure_code": "missing_essential_input_assets",
            "failure_reasons": [
                {
                    "code": "missing_input_assets",
                    "scope": "full_paper_computational_workflow",
                    "evidence_id": "ev-1",
                    "checked_sources": "SI",
                }
            ],
        }
    )

    assert normalized["failure_code"] == "missing_core_input"
    assert normalized["failure_reasons"][0]["code"] == "missing_core_input"
    assert normalized["failure_reasons"][0]["scope_attempted"] == (
        "full_paper_computational_workflow"
    )
    assert normalized["failure_reasons"][0]["evidence_ids"] == ["ev-1"]
    assert normalized["failure_reasons"][0]["checked_sources"] == ["SI"]

    orchestration_failure = _normalize_scientific_failure_contract(
        {
            "decision": "scientific_not_constructible",
            "failure_code": "irreparable_construction",
            "failure_reasons": [],
        }
    )
    assert orchestration_failure["failure_code"] == "irreparable_construction"


def test_stage06_public_asset_recovery_requires_canonical_byte_match(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "inputs"
    source_file = (
        source_root
        / "documents"
        / "doc_abc123"
        / "derived_coordinates"
        / "coordinates-001-test.xyz"
    )
    source_file.parent.mkdir(parents=True)
    source_file.write_text(
        "1\noptimized geometry at B3LYP/def2-SVP\nH 0 0 0\n",
        encoding="utf-8",
    )
    reproduction = tmp_path / "outputs" / "paper_reproduction"
    staged = reproduction / "data" / "inputs" / "structure.xyz"
    staged.parent.mkdir(parents=True)
    staged.write_bytes(source_file.read_bytes())
    evidence_id = "ev_derived_doc_abc123_feedface"
    evidence_index = [
        {
            "evidence_id": evidence_id,
            "text": (
                "Machine-readable XYZ: documents/doc_abc123/derived_coordinates/"
                "coordinates-001-test.xyz"
            ),
            "source_ref": {
                "derivation": "strict_pdf_coordinates_to_xyz",
                "introduced_values": [],
            },
        }
    ]

    assets, unresolved = _recover_public_assets(
        mode_roots=[reproduction],
        rows=[
            {
                "path": "structure.xyz",
                "source_file": (
                    "documents/doc_abc123/derived_coordinates/coordinates-001-test.xyz"
                ),
                "source_evidence_id": evidence_id,
            }
        ],
        source_root=source_root,
        evidence_index=evidence_index,
    )

    assert unresolved == []
    assert assets[0]["content"].splitlines()[1] == (
        "Source-provided geometry: structure.xyz"
    )
    assert staged.read_text(encoding="utf-8").splitlines()[1] == (
        "Source-provided geometry: structure.xyz"
    )
    assert assets[0]["provenance"]["kind"] == "deterministic_transform"
    assert assets[0]["provenance"]["transform_id"] == (
        "xyz_route_comment_redaction_v1"
    )
    assert assets[0]["source_evidence_ids"] == [evidence_id]

    assets, unresolved = _recover_public_assets(
        mode_roots=[reproduction],
        rows=[
            {
                "path": "structure.xyz",
                "source_file": (
                    "documents/doc_abc123/derived_coordinates/coordinates-001-test.xyz"
                ),
                "source_evidence_id": evidence_id,
                "note": "Best-effort reconstruction; verify against the figure.",
            }
        ],
        source_root=source_root,
        evidence_index=evidence_index,
    )

    assert "unverified_public_asset_provenance:structure.xyz" in unresolved
    assert assets[0]["provenance"]["kind"] == "unverified_agent_staging"


def test_stage06_negative_builder_contract_normalizes_before_schema_validation(
    tmp_path: Path,
) -> None:
    evidence_id = "ev_doc_abc123_000001_cafebabe"
    stale_id = "ev_doc_abc123_000001_deadbeef"
    (tmp_path / "inputs").mkdir()
    write_json(
        tmp_path / "inputs" / "evidence_index.json",
        [{"evidence_id": evidence_id, "text": "Required structure is absent."}],
    )
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    write_json(
        outputs / "workflow_review.json",
        {
            "decision": "scientific_not_constructible",
            "task_pair_id": "paper-test-pair",
            "paper_workflow_inventory_complete": True,
            "full_paper_workflow_checked": True,
            "alternative_scope_search_complete": True,
            "workflow_inventory": [],
            "workflow_scope": {
                "scope_kind": "full_paper_computational_workflow",
                "scope_evidence_ids": [stale_id],
            },
            "complexity_profile": {},
            "evidence_map": {"missing_input": {"evidence_ids": [stale_id]}},
            "toolbox_requirements": [],
            "resource_assessment": {},
            "failure_code": "missing_input_assets",
            "failure_reasons": [
                {
                    "scope_attempted": "full_paper_computational_workflow",
                    "code": "missing_input_assets",
                    "details": "The source contains no executable molecular coordinates.",
                    "evidence_id": stale_id,
                    "checked_sources": "main paper and SI",
                }
            ],
            "warnings": [],
        },
    )
    receipt = {
        "decision": "constructed",
        "task_pair_id": "stale",
        "artifact_path": "outputs",
        "milestones": {},
        "failure_code": "",
        "failure_reasons": [],
        "summary": "",
    }

    findings = _task_pair_builder_phase_findings(
        receipt, tmp_path, evidence_ids={evidence_id}
    )

    assert findings == []
    normalized_review = read_json(outputs / "workflow_review.json")
    assert normalized_review["failure_code"] == "missing_core_input"
    assert normalized_review["failure_reasons"][0]["evidence_ids"] == [evidence_id]
    assert receipt["decision"] == "scientific_not_constructible"
    assert receipt["failure_code"] == "missing_core_input"
