from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.contracts import write_jsonl
from src.stages.stage02_computational_content.adjudication import (
    sanitize_classification,
    should_review,
)
from src.stages.stage02_computational_content.evidence import build_evidence_packet
from src.stages.stage02_computational_content.stage import run_stage02
from src.stages.stage03_toolbox_resource_gate.stage import _stage02_evidence_ids


def _classification(
    *,
    decision: str,
    computation_role: str = "primary",
    author_experiments: str = "no",
    counterfactual: str = "main_claim_fails",
    claim_requires_computation: bool = True,
    confidence: float = 0.95,
) -> dict:
    return {
        "decision": decision,
        "article_role": "original_research",
        "performed_computation": "yes",
        "complete_computational_workflow": "yes",
        "author_performed_experiments": author_experiments,
        "computation_role": computation_role,
        "evidence_direction": (
            "pure_computation"
            if author_experiments == "no"
            else (
                "computation_predicts_then_experiment_validates"
                if computation_role == "primary"
                else "experiment_observes_then_computation_explains"
            )
        ),
        "study_mode": (
            "pure_computational"
            if author_experiments == "no"
            else "mixed_computational_experimental"
        ),
        "central_scientific_question": "What controls the reaction barrier?",
        "primary_contribution": "A calculated reaction mechanism.",
        "computational_workflow_steps": [
            {
                "step_id": "step-1",
                "action": "optimize the transition state",
                "generated_output": "activation barrier",
                "evidence_ids": ["calc"],
            }
        ],
        "central_claims": [
            {
                "statement": "The computed barrier controls selectivity.",
                "computation_required": claim_requires_computation,
                "experiment_required": False,
                "evidence_ids": ["calc"],
            }
        ],
        "experimental_contributions": (
            [{"statement": "Measured selectivity.", "evidence_ids": ["lab"]}]
            if author_experiments == "yes"
            else []
        ),
        "counterfactual_without_computation": counterfactual,
        "counterfactual_without_experiments": "partly_survives",
        "method_families": ["DFT"],
        "computational_actions": ["transition-state optimization"],
        "software_clues": ["quantum chemistry program"],
        "resource_clues": [],
        "evidence_ids": ["calc"],
        "experimental_evidence_ids": ["lab"] if author_experiments == "yes" else [],
        "conflicting_evidence_ids": [],
        "rationale": "The cited workflow produces the central claim.",
        "confidence": confidence,
    }


@pytest.mark.parametrize(
    ("response", "experiment_ids", "expected"),
    [
        (
            _classification(decision="computational_content_confirmed"),
            set(),
            "computational_content_confirmed",
        ),
        (
            _classification(
                decision="computational_primary_mixed_confirmed",
                author_experiments="yes",
            ),
            {"lab"},
            "computational_primary_mixed_confirmed",
        ),
        (
            _classification(
                decision="experimental_primary_computational_support",
                computation_role="supporting",
                author_experiments="yes",
                counterfactual="main_claim_survives",
                claim_requires_computation=False,
            ),
            {"lab"},
            "experimental_primary_computational_support",
        ),
    ],
)
def test_stage02_contract_derives_centrality_classes(
    response: dict, experiment_ids: set[str], expected: str
) -> None:
    sanitized, _warnings, _reasons = sanitize_classification(
        response,
        valid_ids={"calc", "lab"},
        computational_ids={"calc"},
        deterministic_experiment_ids=experiment_ids,
        minimum_confidence=0.85,
    )

    assert sanitized["decision"] == expected
    assert sanitized["passed"] == (expected != "experimental_primary_computational_support")


def test_stage02_contract_holds_unresolved_centrality() -> None:
    response = _classification(
        decision="computational_primary_mixed_confirmed",
        author_experiments="yes",
        counterfactual="uncertain",
    )

    sanitized, _warnings, reasons = sanitize_classification(
        response,
        valid_ids={"calc", "lab"},
        computational_ids={"calc"},
        deterministic_experiment_ids={"lab"},
        minimum_confidence=0.85,
    )

    assert sanitized["decision"] == "uncertain"
    assert should_review(sanitized["decision"], reasons)


def test_stage02_contract_uses_experiment_to_computation_direction() -> None:
    response = _classification(
        decision="computational_primary_mixed_confirmed",
        author_experiments="yes",
    )
    response["evidence_direction"] = "experiment_observes_then_computation_explains"

    sanitized, _warnings, _reasons = sanitize_classification(
        response,
        valid_ids={"calc", "lab"},
        computational_ids={"calc"},
        deterministic_experiment_ids={"lab"},
        minimum_confidence=0.85,
    )

    assert sanitized["decision"] == "experimental_primary_computational_support"
    assert not sanitized["passed"]


def test_stage02_contract_rejects_absent_computation() -> None:
    response = {
        "decision": "computational_content_not_found",
        "article_role": "original_research",
        "performed_computation": "no",
        "complete_computational_workflow": "no",
        "author_performed_experiments": "yes",
        "computation_role": "none",
        "study_mode": "noncomputational",
        "central_claims": [],
        "computational_workflow_steps": [],
        "counterfactual_without_computation": "main_claim_survives",
        "evidence_ids": [],
        "experimental_evidence_ids": ["lab"],
        "confidence": 0.98,
    }

    sanitized, _warnings, _reasons = sanitize_classification(
        response,
        valid_ids={"lab"},
        computational_ids=set(),
        deterministic_experiment_ids={"lab"},
        minimum_confidence=0.85,
    )

    assert sanitized["decision"] == "computational_content_not_found"
    assert not sanitized["passed"]


def test_stage02_contract_does_not_accept_experiment_block_as_computation() -> None:
    response = _classification(decision="computational_content_confirmed")
    response["evidence_ids"] = ["lab"]
    response["computational_workflow_steps"][0]["evidence_ids"] = ["lab"]
    response["central_claims"][0]["evidence_ids"] = ["lab"]

    sanitized, _warnings, _reasons = sanitize_classification(
        response,
        valid_ids={"calc", "lab"},
        computational_ids={"calc"},
        deterministic_experiment_ids=set(),
        minimum_confidence=0.85,
    )

    assert sanitized["decision"] == "uncertain"
    assert not sanitized["passed"]


def test_stage02_packet_balances_main_and_si_evidence() -> None:
    blocks = [
        {
            "evidence_id": "title",
            "document_id": "main",
            "document_role": "main_paper",
            "text": "Reaction Mechanism from Computation and Experiment",
        },
        {
            "evidence_id": "abstract",
            "document_id": "main",
            "document_role": "main_paper",
            "text": "We computed the reaction pathway and measured product selectivity.",
        },
        {
            "evidence_id": "main-calc",
            "document_id": "main",
            "document_role": "main_paper",
            "text": "We performed DFT calculations and computed an activation energy barrier.",
        },
        {
            "evidence_id": "main-lab",
            "document_id": "main",
            "document_role": "main_paper",
            "text": "We synthesized the catalyst and recorded NMR spectra.",
        },
        {
            "evidence_id": "conclusion-heading",
            "document_id": "main",
            "document_role": "main_paper",
            "text": "Conclusion",
        },
        {
            "evidence_id": "conclusion",
            "document_id": "main",
            "document_role": "main_paper",
            "text": "The calculated transition state explains the measured selectivity.",
        },
        *[
            {
                "evidence_id": f"si-{index}",
                "document_id": "si",
                "document_role": "supplementary",
                "text": "Density functional theory calculations were performed and optimized geometries were obtained.",
            }
            for index in range(12)
        ],
    ]

    packet = build_evidence_packet(
        paper_metadata={"title": "fixture"},
        blocks=blocks,
        config={
            "max_prompt_characters": 10000,
            "max_computational_excerpts": 6,
            "max_experimental_excerpts": 4,
        },
    )

    assert packet["rule_screen"]["computation_candidate"] is True
    assert any(row["document_role"] == "main_paper" for row in packet["narrative_evidence"])
    assert {row["document_role"] for row in packet["computational_evidence"]} == {
        "main_paper",
        "supplementary",
    }
    assert any(row["evidence_id"] == "main-lab" for row in packet["experimental_evidence"])
    selected_ids = [
        row["evidence_id"]
        for key in ("narrative_evidence", "computational_evidence", "experimental_evidence")
        for row in packet[key]
    ]
    assert len(selected_ids) == len(set(selected_ids))


def test_stage02_packet_keeps_single_explicit_method_and_focuses_long_excerpt() -> None:
    long_text = (
        "introductory context " * 200 + "We performed DFT calculations to optimize the catalyst."
    )
    packet = build_evidence_packet(
        paper_metadata={"title": "fixture"},
        blocks=[
            {
                "evidence_id": "calc",
                "document_id": "main",
                "document_role": "main_paper",
                "text": long_text,
            }
        ],
        config={"excerpt_characters": 500, "max_prompt_characters": 5000},
    )

    assert packet["rule_screen"]["computation_candidate"] is True
    assert packet["rule_screen"]["explicit_method_blocks"] == 1
    assert "DFT calculations" in packet["computational_evidence"][0]["text"]


def test_stage03_collects_nested_stage02_evidence_ids() -> None:
    assert _stage02_evidence_ids(
        {
            "evidence_ids": ["top"],
            "computational_workflow_steps": [{"evidence_ids": ["workflow"]}],
            "central_claims": [{"evidence_ids": ["claim", "top"]}],
            "experimental_contributions": [{"evidence_ids": ["experiment"]}],
        }
    ) == ["top", "workflow", "claim", "experiment"]


class _FixtureModel:
    def __init__(self, responses: list[dict], audits: list[dict] | None = None):
        self.responses = list(responses)
        self.audits = list(audits or [])
        self.calls: list[dict] = []
        self.config = {"workers": 1}
        self.model = "fixture"
        self.role = "screening"

    def call_json(self, **kwargs):
        self.calls.append(kwargs)
        response = self.responses.pop(0)
        audit = (
            self.audits.pop(0)
            if self.audits
            else {"finish_reason": "stop", "request_hash": str(len(self.calls))}
        )
        return response, audit


def _run_fixture(
    tmp_path: Path,
    blocks: list[dict],
    model: _FixtureModel,
    *,
    review_pass_decisions: bool = False,
):
    blocks_path = tmp_path / "blocks.jsonl"
    write_jsonl(blocks_path, blocks)
    return run_stage02(
        papers=[
            {
                "paper_id": "paper-1",
                "document_ids": ["doc-1"],
                "decision": "pass",
                "package_status": "complete_confirmed_no_si",
                "main_parse_ok": True,
                "supplementary_parse_ok": None,
                "partial_si_parse": False,
            }
        ],
        documents=[
            {
                "paper_id": "paper-1",
                "document_id": "doc-1",
                "document_role": "main_paper",
                "decision": "pass",
                "content_blocks_path": str(blocks_path),
            }
        ],
        config={
            "workers": 1,
            "review_on_conflict": True,
            "review_pass_decisions": review_pass_decisions,
        },
        model=model,
        workspace=tmp_path / "run",
        run_id="fixture-run",
    )


def test_stage02_obvious_noncomputation_uses_zero_model_calls(tmp_path: Path) -> None:
    model = _FixtureModel([])
    result = _run_fixture(
        tmp_path,
        [
            {
                "evidence_id": "lab",
                "document_id": "doc-1",
                "text": "We synthesized the catalyst and recorded NMR spectra.",
            }
        ],
        model,
    )

    assert result["records"][0]["decision"] == "computational_content_not_found"
    assert result["summary"]["zero_call_rejections"] == 1
    assert model.calls == []


def test_stage02_consistent_candidate_uses_one_model_call(tmp_path: Path) -> None:
    model = _FixtureModel([_classification(decision="computational_content_confirmed")])
    result = _run_fixture(
        tmp_path,
        [
            {
                "evidence_id": "calc",
                "document_id": "doc-1",
                "text": "We performed DFT calculations and computed an activation energy barrier.",
            }
        ],
        model,
    )

    assert result["records"][0]["decision"] == "computational_content_confirmed"
    assert result["summary"]["model_calls"] == 1
    assert len(model.calls) == 1


def test_stage02_verified_experiment_conflict_gets_one_review(tmp_path: Path) -> None:
    primary = _classification(decision="computational_content_confirmed")
    reviewed = _classification(
        decision="computational_primary_mixed_confirmed", author_experiments="yes"
    )
    model = _FixtureModel([primary, reviewed])
    result = _run_fixture(
        tmp_path,
        [
            {
                "evidence_id": "calc",
                "document_id": "doc-1",
                "text": "We performed DFT calculations and computed an activation energy barrier.",
            },
            {
                "evidence_id": "lab",
                "document_id": "doc-1",
                "text": "We synthesized the catalyst and recorded NMR spectra.",
            },
        ],
        model,
    )

    assert result["records"][0]["decision"] == "computational_primary_mixed_confirmed"
    assert result["summary"]["conflict_reviews"] == 1
    assert len(model.calls) == 2
    assert model.calls[0]["namespace"] == "stage02_classify"
    assert model.calls[1]["namespace"] == "stage02_contract_conflict_review"
    packet = json.loads(model.calls[0]["user_content"])
    assert packet["deterministic_author_experiment_evidence"][0]["evidence_id"] == "lab"


def test_stage02_counts_provider_attempts_across_truncation_retry(tmp_path: Path) -> None:
    response = _classification(decision="computational_content_confirmed")
    model = _FixtureModel(
        [response, response],
        audits=[
            {"finish_reason": "length", "attempts": 1, "request_hash": "first"},
            {"finish_reason": "stop", "attempts": 2, "request_hash": "retry"},
        ],
    )
    result = _run_fixture(
        tmp_path,
        [
            {
                "evidence_id": "calc",
                "document_id": "doc-1",
                "text": "We performed DFT calculations and computed an activation energy barrier.",
            }
        ],
        model,
    )

    assert result["summary"]["model_calls"] == 1
    assert result["summary"]["successful_model_http_requests"] == 3
    assert len(model.calls) == 2


def test_stage02_pass_candidate_gets_precision_review(tmp_path: Path) -> None:
    response = _classification(decision="computational_content_confirmed")
    model = _FixtureModel([response, response])
    result = _run_fixture(
        tmp_path,
        [
            {
                "evidence_id": "calc",
                "document_id": "doc-1",
                "text": "We performed DFT calculations and computed an activation energy barrier.",
            }
        ],
        model,
        review_pass_decisions=True,
    )

    assert result["records"][0]["decision"] == "computational_content_confirmed"
    assert result["summary"]["model_calls"] == 2
    assert result["summary"]["pass_precision_reviews"] == 1
    assert model.calls[1]["namespace"] == "stage02_pass_precision_review"
