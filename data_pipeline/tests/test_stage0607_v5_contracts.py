from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.agents.schemas import STAGE06_WORKFLOW_REVIEW_SCHEMA, STAGE07_AUDIT_SCHEMA
from src.agents.workspace import recovery_instructions
from src.stages.stage06_task_builder.prompts import (
    autonomous_converter_instructions,
    task_pair_builder_instructions,
)
from src.stages.stage06_task_builder.validation import validate_representativeness_review
from src.stages.stage07_task_judge.prompts import audit_instructions
from src.stages.stage07_task_judge.stage import _approved_receipt_contract_findings


def test_representativeness_review_is_evidence_shape_only() -> None:
    review = {
        "paper_computational_claims": [
            {"claim_id": "claim-main", "coverage": "direct", "evidence_ids": ["ev-1"]}
        ],
        "candidate_workflows": [
            {
                "workflow_id": "wf-full",
                "scope_kind": "full_paper_core_workflow",
                "claim_coverage": {"claim-main": "direct"},
                "closure": "closed",
                "resource_assessment": "feasible under the declared policy",
                "software_gap_status": "available",
            }
        ],
        "selected_workflow_id": "wf-full",
        "selection_rationale": "The connected route supports the central claim.",
        "omitted_claims": [],
    }
    assert validate_representativeness_review(review, {"ev-1"}) == []
    assert "representativeness_claims_missing" in validate_representativeness_review(
        {**review, "paper_computational_claims": []}, {"ev-1"}
    )


def test_representativeness_candidate_requires_auditable_observation_fields() -> None:
    review = {
        "paper_computational_claims": [
            {"claim_id": "claim-main", "coverage": "direct", "evidence_ids": ["ev-1"]}
        ],
        "candidate_workflows": [
            {
                "workflow_id": "wf-full",
                "scope_kind": "full_paper_core_workflow",
                "claim_coverage": {"claim-main": "direct"},
                "closure": "closed",
            }
        ],
        "selected_workflow_id": "wf-full",
        "selection_rationale": "Compared candidate routes.",
        "omitted_claims": [],
    }
    findings = validate_representativeness_review(review, {"ev-1"})
    assert "representativeness_candidate_resource_observation_missing:0" in findings
    assert "representativeness_candidate_software_status_missing:0" in findings


def test_stage_prompts_require_scope_comparison_and_do_not_treat_software_gap_as_rejection() -> None:
    builder = task_pair_builder_instructions(paper_id="paper-x", snapshot_hash="hash")
    judge = audit_instructions(
        paper_id="paper-x",
        task_pair_id="paper-x_task_pair",
        manifest_hash="hash",
        max_tool_calls=20,
        finalization_reserve=4,
    )
    for prompt in (builder, judge):
        assert "representativeness" in prompt
        assert "missing software" in prompt.casefold() or "missing program" in prompt.casefold()
        assert "never causes scientific rejection" in prompt.casefold() or "not a blocker" in prompt.casefold()
    assert "claim_id" in builder and "evidence_ids" in builder
    assert "scope_kind" in builder and "software_gap_status" in builder
    for prompt in (builder, judge):
        normalized_prompt = " ".join(prompt.split())
        assert "ultimate_claim_dependency" in prompt
        assert "advertised" in prompt.casefold() and "conclusion" in prompt.casefold()
        assert "source_constrained_construction" in prompt
        assert "tight paper-specific absolute" in normalized_prompt
    assert "must not appear as a reason" in builder
    assert "missing software must never appear in a scope downgrade rationale" in " ".join(
        judge.split()
    ).casefold()


def test_stage_prompts_use_model_neutral_execution_order() -> None:
    builder = task_pair_builder_instructions(paper_id="paper-x", snapshot_hash="hash")
    converter = autonomous_converter_instructions(
        paper_id="paper-x", task_pair_id="paper-x_task_pair"
    )
    judge = audit_instructions(
        paper_id="paper-x",
        task_pair_id="paper-x_task_pair",
        manifest_hash="hash",
        max_tool_calls=20,
        finalization_reserve=4,
    )

    assert "EXECUTION ORDER" in builder
    assert builder.index("EXECUTION ORDER") < builder.index("TOOL-BUDGET DISCIPLINE")
    assert "CONVERSION ORDER" in converter
    assert "AUDIT ORDER" in judge
    assert judge.index("AUDIT ORDER") < judge.index("SCIENTIFIC WORKFLOW")
    for prompt in (builder, converter, judge):
        assert "source" in prompt.casefold() or "evidence" in prompt.casefold()
        assert "final" in prompt.casefold() and "status" in prompt.casefold()


def test_stage_prompts_reject_trivial_redesign_and_use_one_dependency_contract() -> None:
    builder = task_pair_builder_instructions(paper_id="paper-x", snapshot_hash="hash")
    judge = audit_instructions(
        paper_id="paper-x",
        task_pair_id="paper-x_task_pair",
        manifest_hash="hash",
        max_tool_calls=20,
        finalization_reserve=4,
    )
    for prompt in (builder, judge):
        normalized = " ".join(prompt.split()).casefold()
        assert "simple arithmetic" in normalized
        assert "reported experimental measurements" in normalized
        for key in (
            "advertised_conclusion",
            "direct_computational_evidence",
            "supporting_only_evidence",
            "selected_workflow_position",
        ):
            assert key in prompt
    assert "hundreds of expensive calculations" in " ".join(judge.split())
    assert "most central item among the closed candidates is insufficient" in " ".join(
        builder.split()
    )
    assert "most central of the closed candidates" in " ".join(judge.split())
    assert "aggregate number of atom rows" in " ".join(builder.split())
    assert "an IRC cannot connect unequal atom sets" in " ".join(builder.split())
    assert "substitute the canonical values/order" in " ".join(judge.split())
    assert "`High but bounded` is not a feasibility argument" in judge
    assert "A bare assertion such as `20 optimizations are feasible` is not" in builder
    assert "Exact measured timings are useful but not mandatory" in judge
    assert "never return an approved decision with `resource_status=uncertain`" in " ".join(
        judge.split()
    ).casefold()
    assert "managed_computation_policy` as JSON objects" in judge


def test_converter_keeps_private_handoff_out_of_public_task_and_has_uncertain_status() -> None:
    prompt = autonomous_converter_instructions(
        paper_id="paper-x", task_pair_id="paper-x_task_pair"
    )
    normalized = " ".join(prompt.split()).casefold()
    assert "private handoff" in normalized
    assert "never copy, quote, serialize" in normalized
    assert "task-package files" in normalized
    assert "conversion_uncertain" in prompt
    assert "needs_conversion_retry" in prompt
    assert "code-mode" in normalized
    assert "already copied" in normalized
    assert "never create `outputs/autonomous_research/paper_reproduction/`" in normalized


def test_recovery_prompt_does_not_confuse_optional_code_mode_with_shell_failure() -> None:
    prompt = recovery_instructions("autonomous_converter", max_tool_calls=10)
    normalized = " ".join(prompt.split()).casefold()
    assert "code-mode host" in normalized
    assert "does not imply a filesystem failure" in normalized
    assert "do not repeat `pwd`" in normalized


def test_stage07_approved_receipt_requires_representativeness_audit() -> None:
    response = {
        "audit_decision": "approved",
        "scientific_decision": "approved",
        "source_stage06_decision": "provisional_constructed",
        "original_task_pair_id": "paper-x_task_pair",
        "final_task_pair_id": "paper-x_task_pair",
        "artifact_path": "outputs/task_pair",
        "selected_workflow_preserved": True,
        "repairs": [],
        "workflow_redesign": {"performed": False},
        "remaining_issues": [],
        "toolbox_status": "available",
        "execution_readiness": "ready",
        "required_additions": [],
        "resource_status": "feasible",
        "contract_status": "passed",
        "disclosure_status": "passed",
        "schema_load_diagnostic": "passed",
        "scientific_audit_table": [
            {"check": f"check-{index}", "status": "closed"}
            for index in range(6)
        ],
        "representativeness_audit": {
            "paper_claims_checked": [],
            "candidate_workflows_checked": [],
            "selected_scope_kind": "full_paper_core_workflow",
            "coverage_summary": [],
            "rationale": "Compared the full route and alternatives against the paper claims.",
            "ultimate_claim_dependency": {
                "advertised_conclusion": "The paper's principal conclusion.",
                "direct_computational_evidence": [],
                "supporting_only_evidence": [],
                "selected_workflow_position": "Directly tests the principal conclusion.",
            },
        },
    }
    assert _approved_receipt_contract_findings(response) == []
    missing = dict(response)
    missing.pop("representativeness_audit")
    assert "approved_representativeness_audit_missing" in _approved_receipt_contract_findings(
        missing
    )

    missing_table = dict(response)
    missing_table["scientific_audit_table"] = []
    assert "approved_scientific_audit_table_incomplete" in _approved_receipt_contract_findings(
        missing_table
    )

    missing_dependency = dict(response)
    missing_dependency["representativeness_audit"] = {
        **response["representativeness_audit"],
        "ultimate_claim_dependency": {},
    }
    dependency_findings = _approved_receipt_contract_findings(missing_dependency)
    assert "approved_advertised_conclusion_missing" in dependency_findings
    assert "approved_selected_workflow_dependency_position_missing" in dependency_findings


def test_batch_worker_exception_records_terminal_state(tmp_path, monkeypatch) -> None:
    script_path = Path(__file__).parents[1] / "scripts/workflows/run_stage06_07_gpt_batch.py"
    spec = importlib.util.spec_from_file_location("stage0607_batch", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class Args:
        force = True
        pipeline_root = tmp_path
        source_run = tmp_path
        config = tmp_path / "config.json"
        harness = "codex"

    def fail(*args, **kwargs):
        raise OSError("spawn failed")

    monkeypatch.setattr(module.subprocess, "run", fail)
    result = module._run_one(
        paper="paper-x",
        args=Args(),
        output_root=tmp_path / "batch",
        environment={},
    )
    assert result["state"] == "FAILED"
    assert (tmp_path / "batch/papers/paper-x/run_status.json").is_file()


def test_batch_worker_does_not_call_internal_stage_failure_completed(
    tmp_path, monkeypatch
) -> None:
    script_path = Path(__file__).parents[1] / "scripts/workflows/run_stage06_07_gpt_batch.py"
    spec = importlib.util.spec_from_file_location("stage0607_batch_summary", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class Args:
        force = True
        pipeline_root = tmp_path
        source_run = tmp_path
        config = tmp_path / "config.json"
        harness = "codex"

    def fake_run(*args, **kwargs):
        output = tmp_path / "batch/papers/paper-x"
        output.mkdir(parents=True, exist_ok=True)
        (output / "late_stage_run_summary.json").write_text(
            '{"stage06": {"artifact_delivery_failures": 1}, '
            '"stage07": {"status": "not_run"}}',
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    result = module._run_one(
        paper="paper-x",
        args=Args(),
        output_root=tmp_path / "batch",
        environment={},
    )
    assert result["state"] == "FAILED"
    assert result["failure_class"] == "stage06_artifact_delivery_failure_retryable"


def test_batch_parser_exposes_reproducible_random_sampling() -> None:
    script_path = Path(__file__).parents[1] / "scripts/workflows/run_stage06_07_gpt_batch.py"
    spec = importlib.util.spec_from_file_location("stage0607_batch_parser", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    args = module.build_parser().parse_args(["--output-root", "/tmp/out", "--limit", "10", "--random-seed", "7"])
    assert args.limit == 10
    assert args.random_seed == 7


def test_batch_parser_exposes_optional_reasoning_mode() -> None:
    script_path = Path(__file__).parents[1] / "scripts/workflows/run_stage06_07_gpt_batch.py"
    spec = importlib.util.spec_from_file_location("stage0607_batch_reasoning_mode", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    args = module.build_parser().parse_args(
        ["--output-root", "/tmp/out", "--reasoning-mode", "pro"]
    )
    assert args.reasoning_mode == "pro"
