import json
from pathlib import Path

from src.stages.stage03_computation_relevance import (
    assess_computation_relevance,
    build_review_prompt,
    llm_review,
)

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def _run(tmp_path, main: str, supplementary: str | None = None):
    main_path = tmp_path / "main.txt"
    main_path.write_text(main, encoding="utf-8")
    documents = [
        {
            "paper_id": "p1",
            "document_id": "main",
            "document_role": "main_paper",
            "text_path": str(main_path),
        }
    ]
    if supplementary is not None:
        si_path = tmp_path / "si.txt"
        si_path.write_text(supplementary, encoding="utf-8")
        documents.append(
            {
                "paper_id": "p1",
                "document_id": "si",
                "document_role": "supplementary",
                "text_path": str(si_path),
            }
        )
    bundle = {
        "paper_id": "p1",
        "main_documents": documents[:1],
        "supplementary_documents": documents[1:],
    }
    return assess_computation_relevance(
        [bundle],
        method_ontology=ASSETS / "computational_method_ontology.yaml",
        evidence_rules=ASSETS / "computation_evidence_rules.yaml",
        negative_contexts=ASSETS / "computation_negative_contexts.yaml",
    )[0]


def test_stage03_accepts_main_and_si_combined_evidence(tmp_path):
    record = _run(
        tmp_path,
        "Methods\nWe performed calculations. Computational details are provided in the Supporting Information.",
        "Computational details\nDensity functional theory geometry optimization produced orbital energies.",
    )
    assert record["computation_relevance"]["decision"] == "strong_candidate"
    assert {item["document_role"] for item in record["computation_relevance"]["evidence"]} == {
        "main_paper",
        "supplementary",
    }
    assert record["computation_relevance"]["used_llm"] is False


def test_stage03_excludes_reference_only_mentions(tmp_path):
    record = _run(
        tmp_path,
        "Introduction\nThis topic is important.\nReferences\nSmith reported previously density functional theory calculations and orbital energies.",
    )
    assert record["computation_relevance"]["decision"] == "not_computational"
    assert record["computation_relevance"]["excluded_evidence"]


def test_stage03_keeps_ambiguous_method_evidence_as_weak(tmp_path):
    record = _run(
        tmp_path,
        "Results\nDensity functional theory results include the calculated adsorption energy.",
    )
    assert record["computation_relevance"]["decision"] == "weak_candidate"


def test_stage03_rejects_experimental_calculation_language(tmp_path):
    record = _run(
        tmp_path,
        "Results\nWe performed a binding assay. The dissociation constant was calculated from the curve, and we optimized the peptide linker.",
    )
    assert record["computation_relevance"]["decision"] == "not_computational"


def test_stage03_rejects_neb_vendor_acronym(tmp_path):
    record = _run(
        tmp_path,
        "Methods\nEscherichia coli NEB 5alpha and NEB 10beta from "
        "New England Biolabs were used. We performed LCMS analysis.",
    )
    assert record["computation_relevance"]["decision"] == "not_computational"


def test_stage03_retains_repeated_method_only_signal_as_weak(tmp_path):
    record = _run(
        tmp_path,
        "Results\nThe first-principles screening identified candidate phases. "
        "Structures usable for first-principles calculations were relaxed by DFT.",
    )
    assert record["computation_relevance"]["decision"] == "weak_candidate"


def test_stage03_caps_repeated_term_score_but_keeps_raw_score(tmp_path):
    record = _run(
        tmp_path,
        "Results\n"
        + " ".join(
            "Density functional theory calculations produced orbital energies."
            for _ in range(20)
        ),
    )
    relevance = record["computation_relevance"]
    assert relevance["raw_score"] > relevance["score"]
    assert relevance["score_contribution_count"] < len(relevance["evidence"])


def test_stage03_llm_prompt_is_bounded_and_uses_evidence_excerpts(tmp_path):
    record = _run(
        tmp_path,
        "Results\nDensity functional theory results include calculated adsorption energy. "
        + "background " * 20_000,
    )
    prompt, sources = build_review_prompt(record, max_chars=6_000)
    payload = json.loads(prompt)
    assert len(prompt) <= 6_000
    assert payload["prompt_version"] == "stage03-computation-review-v1"
    assert payload["excerpts"]
    assert sources


def test_stage03_llm_verified_yes_overrides_weak_rule(tmp_path, monkeypatch):
    main_path = tmp_path / "main.txt"
    main_path.write_text(
        "Results\nDensity functional theory results include the calculated adsorption energy.",
        encoding="utf-8",
    )
    bundle = {
        "paper_id": "p1",
        "title": "Adsorption on a catalyst",
        "main_documents": [
            {
                "paper_id": "p1",
                "document_id": "main",
                "document_role": "main_paper",
                "text_path": str(main_path),
            }
        ],
        "supplementary_documents": [],
    }
    monkeypatch.setattr(llm_review, "_service_ready", lambda _config: True)

    def fake_call(**kwargs):
        assert kwargs["max_tokens"] == 1024
        assert kwargs["thinking"] is None
        payload = json.loads(kwargs["user_content"])
        excerpt = next(item for item in payload["excerpts"] if item["excerpt_id"] != "opening")
        return (
            {
                "performed_computation": "yes",
                "article_role": "original_research",
                "computation_role": "supporting",
                "method_families": ["electronic_structure"],
                "author_execution_evidence": [
                    {
                        "excerpt_id": excerpt["excerpt_id"],
                        "quote": excerpt["text"],
                        "reason": "reported result",
                    }
                ],
                "confidence": 0.9,
                "reason": "The paper reports its own calculation.",
            },
            {"duration_seconds": 0.1, "usage": {"prompt_tokens": 10}, "model_returned": "qwen"},
        )

    monkeypatch.setattr(llm_review, "call_json_chat", fake_call)
    record = assess_computation_relevance(
        [bundle],
        method_ontology=ASSETS / "computational_method_ontology.yaml",
        evidence_rules=ASSETS / "computation_evidence_rules.yaml",
        negative_contexts=ASSETS / "computation_negative_contexts.yaml",
        llm_config={
            "enabled": True,
            "base_url": "http://test/v1",
            "api_key": "test",
            "model": "qwen",
            "concurrency": 4,
        },
        llm_cache_dir=tmp_path / "cache",
    )[0]
    assert record["computation_relevance"]["rule_decision"] == "weak_candidate"
    assert record["computation_relevance"]["decision"] == "strong_candidate"
    assert record["computation_relevance"]["used_llm"] is True
    assert record["llm_computation_review"]["author_execution_evidence"]


def test_stage03_llm_unverified_yes_falls_back_to_rule(tmp_path, monkeypatch):
    record = _run(
        tmp_path,
        "Results\nDensity functional theory results include the calculated adsorption energy.",
    )
    monkeypatch.setattr(llm_review, "_service_ready", lambda _config: True)
    monkeypatch.setattr(
        llm_review,
        "call_json_chat",
        lambda **_kwargs: (
            {
                "performed_computation": "yes",
                "article_role": "original_research",
                "computation_role": "supporting",
                "method_families": [],
                "author_execution_evidence": [
                    {"excerpt_id": "opening", "quote": "invented evidence", "reason": "none"}
                ],
                "confidence": 0.99,
                "reason": "unsupported",
            },
            {},
        ),
    )
    reviewed = llm_review.apply_llm_review(
        [record],
        config={
            "enabled": True,
            "base_url": "http://test/v1",
            "api_key": "test",
            "model": "qwen",
        },
        cache_dir=tmp_path / "cache",
    )[0]
    assert reviewed["computation_relevance"]["decision"] == "weak_candidate"
    assert reviewed["llm_computation_review"]["status"] == "uncertain_rule_fallback"


def test_stage03_llm_health_failure_preserves_rule_decision(tmp_path, monkeypatch):
    record = _run(
        tmp_path,
        "Results\nDensity functional theory results include the calculated adsorption energy.",
    )
    monkeypatch.setattr(llm_review, "_service_ready", lambda _config: False)
    reviewed = llm_review.apply_llm_review(
        [record],
        config={"enabled": True, "base_url": "http://unavailable/v1", "model": "qwen"},
        cache_dir=tmp_path / "cache",
    )[0]
    assert reviewed["computation_relevance"]["decision"] == "weak_candidate"
    assert reviewed["computation_relevance"]["used_llm"] is False
    assert reviewed["llm_computation_review"]["status"] == "rule_fallback"


def test_stage03_llm_truncated_response_preserves_rule_decision(tmp_path, monkeypatch):
    record = _run(
        tmp_path,
        "Results\nDensity functional theory results include the calculated adsorption energy.",
    )
    monkeypatch.setattr(llm_review, "_service_ready", lambda _config: True)
    monkeypatch.setattr(
        llm_review,
        "call_json_chat",
        lambda **_kwargs: (
            {
                "performed_computation": "yes",
                "article_role": "original_research",
                "computation_role": "supporting",
                "method_families": ["electronic_structure"],
                "author_execution_evidence": [],
            },
            {"finish_reason": "length"},
        ),
    )

    reviewed = llm_review.apply_llm_review(
        [record],
        config={
            "enabled": True,
            "base_url": "http://test/v1",
            "api_key": "test",
            "model": "qwen",
        },
        cache_dir=tmp_path / "cache",
    )[0]

    assert reviewed["computation_relevance"]["decision"] == "weak_candidate"
    assert reviewed["computation_relevance"]["used_llm"] is False
    assert reviewed["llm_computation_review"]["status"] == "rule_fallback"
    assert "output token limit" in reviewed["llm_computation_review"]["error"]


def test_stage03_strict_llm_reviews_strong_and_rejects_uncertain(tmp_path, monkeypatch):
    record = _run(
        tmp_path,
        "Methods\nWe performed density functional theory calculations. "
        "The optimized geometry produced orbital energies.",
    )
    assert record["computation_relevance"]["decision"] == "strong_candidate"
    monkeypatch.setattr(llm_review, "_service_ready", lambda _config: True)
    monkeypatch.setattr(
        llm_review,
        "call_json_chat",
        lambda **_kwargs: (
            {
                "performed_computation": "uncertain",
                "article_role": "original_research",
                "computation_role": "supporting",
                "method_families": ["electronic_structure"],
                "author_execution_evidence": [],
                "confidence": 0.95,
                "reason": "Execution cannot be attributed.",
            },
            {},
        ),
    )
    reviewed = llm_review.apply_llm_review(
        [record],
        config={
            "enabled": True,
            "strict": True,
            "review_all_candidates": True,
            "base_url": "http://test/v1",
            "api_key": "test",
            "model": "qwen",
        },
        cache_dir=tmp_path / "strict-cache",
    )[0]
    assert reviewed["computation_relevance"]["decision"] == "llm_unconfirmed"
    assert reviewed["pipeline_routing"]["continue"] is False
    assert reviewed["llm_computation_review"]["status"] == "strict_rejected"


def test_stage03_strict_llm_failure_is_fail_closed(tmp_path, monkeypatch):
    record = _run(
        tmp_path,
        "Methods\nWe performed density functional theory calculations. "
        "The optimized geometry produced orbital energies.",
    )
    monkeypatch.setattr(llm_review, "_service_ready", lambda _config: False)
    reviewed = llm_review.apply_llm_review(
        [record],
        config={
            "enabled": True,
            "strict": True,
            "review_all_candidates": True,
            "base_url": "http://unavailable/v1",
            "model": "qwen",
        },
        cache_dir=tmp_path / "strict-cache",
    )[0]
    assert reviewed["computation_relevance"]["decision"] == "llm_unconfirmed"
    assert reviewed["pipeline_routing"]["continue"] is False
    assert reviewed["pipeline_routing"]["stop_reason"] == "llm_confirmation_required"
