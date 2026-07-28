from __future__ import annotations

from researchchem_toolbox.search_index import BM25Index, tokenize


def test_tokenizer_normalizes_common_morphology() -> None:
    assert tokenize("optimizing optimized optimization") == ["optimiz", "optimiz", "optimiz"]


def test_bm25_uses_or_recall_and_relevance_ordering() -> None:
    index = BM25Index(
        {
            "energy": "single point molecular electronic energy",
            "surface": "electron density isodensity surface volume",
            "generic": "molecular descriptor",
        }
    )
    results = index.search("single point energy surface")
    assert {item.document_id for item in results} == {"energy", "surface"}
    assert results[0].document_id == "energy"
