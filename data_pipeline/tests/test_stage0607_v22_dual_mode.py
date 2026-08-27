from __future__ import annotations

from src.stages.stage06_task_builder.prompts import (
    STAGE06_SYNTHESIS_PROMPT_VERSION,
    final_task_synthesis_instructions,
)
from src.stages.stage07_task_judge.prompts import (
    STAGE07_AUDIT_PROMPT_VERSION,
    final_task_audit_instructions,
)


def test_stage06_uses_author_scientific_route_not_paper_protocol() -> None:
    prompt = final_task_synthesis_instructions(
        paper_id="paper_fixture22", snapshot_hash="snapshot"
    )
    assert STAGE06_SYNTHESIS_PROMPT_VERSION.startswith("v23-")
    assert "scientific hypothesis" in prompt
    assert "paper's software" in prompt
    assert "ordered computational protocol" in prompt
    assert "never enter either public task" in prompt
    assert "result-bearing TS" in prompt
    assert "must independently plan the computation" in prompt


def test_stage06_autonomous_route_is_not_forced_for_direct_computation() -> None:
    prompt = final_task_synthesis_instructions(
        paper_id="paper_fixture22", snapshot_hash="snapshot"
    )
    assert "formulate" in prompt and "scientific" in prompt and "route" in prompt
    assert "do not" in prompt and "invent" in prompt and "discovery" in prompt
    assert "same objective and shared research-before-discovery inputs" in prompt


def test_stage07_audits_result_artifacts_and_allows_pure_computation_similarity() -> None:
    prompt = final_task_audit_instructions(paper_id="paper_fixture22")
    assert STAGE07_AUDIT_PROMPT_VERSION.startswith("v23-")
    assert "result-bearing artifacts" in prompt
    assert "computational protocol" in prompt
    assert "direct computation" in prompt
    assert "Shared result rules are allowed" in prompt
    assert "do not" in prompt and "invented discovery" in prompt


def test_both_prompts_require_outcome_based_validation_without_protocol_fidelity() -> None:
    synthesis = final_task_synthesis_instructions(
        paper_id="paper_fixture22", snapshot_hash="snapshot"
    )
    audit = final_task_audit_instructions(paper_id="paper_fixture22")
    for prompt in (synthesis, audit):
        assert "outcome-based" in prompt or "scientific validation requirements" in prompt
        assert "software, model chemistry" in prompt
        assert "execution" in prompt and "order" in prompt
    assert "Do not prescribe" in synthesis
