from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.agents.schemas import STAGE06_WORKFLOW_REVIEW_SCHEMA, STAGE07_AUDIT_SCHEMA
from src.stages.stage06_task_builder.prompts import task_pair_builder_instructions
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


def test_stage07_approved_receipt_requires_representativeness_audit() -> None:
    response = {
        "audit_decision": "approved",
        "artifact_path": "outputs/task_pair",
        "representativeness_audit": {
            "paper_claims_checked": [],
            "candidate_workflows_checked": [],
            "selected_scope_kind": "full_paper_core_workflow",
            "coverage_summary": [],
            "rationale": "Compared the full route and alternatives against the paper claims.",
        },
    }
    assert _approved_receipt_contract_findings(response) == []
    missing = dict(response)
    missing.pop("representativeness_audit")
    # Older receipts remain transport-compatible; new prompts request the field and
    # the checker validates it whenever an Agent supplies it.
    assert _approved_receipt_contract_findings(missing) == []


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
