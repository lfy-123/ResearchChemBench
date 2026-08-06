from pathlib import Path

from src.stages.stage03_computation_relevance import assess_computation_relevance

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
