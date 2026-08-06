from __future__ import annotations

from pathlib import Path

from src.core.io import read_json
from src.orchestration import screening_microbatch


def _documents(tmp_path: Path, papers: int) -> list[dict]:
    output = []
    for index in range(papers):
        path = tmp_path / f"paper-{index}.pdf"
        path.write_bytes(b"%PDF-test")
        output.append(
            {
                "paper_id": f"paper-{index}",
                "document_id": f"document-{index}",
                "document_role": "main_paper",
                "source_path": str(path),
                "sha256": f"hash-{index}",
            }
        )
    return output


def test_redesigned_microbatch_groups_papers_and_aggregates_in_order(tmp_path, monkeypatch):
    documents = _documents(tmp_path, 5)

    def fake_extract(records, _client, **_kwargs):
        return [
            {
                **item,
                "grobid_extract_status": "success",
                "grobid_request_attempted": True,
                "grobid_request_failed": False,
                "text_path": item["source_path"],
            }
            for item in records
        ]

    def fake_assess(bundles, **_kwargs):
        return [
            {
                **item,
                "computation_relevance": {
                    "decision": "strong_candidate",
                    "evidence": [],
                    "used_llm": False,
                },
                "pipeline_routing": {"continue": True, "stage_03": "strong_candidate"},
            }
            for item in bundles
        ]

    monkeypatch.setattr(screening_microbatch, "extract_documents_with_grobid", fake_extract)
    monkeypatch.setattr(screening_microbatch, "assess_computation_relevance", fake_assess)
    config = {
        "microbatch": {
            "size": 2,
            "concurrency": 2,
            "resume": True,
            "stage_limits": {"2": 2, "3": 2},
        },
        "grobid_extract": {"workers": 1, "fallback": {}},
        "stage03_computation_relevance": {
            "method_ontology": "ontology",
            "evidence_rules": "rules",
            "negative_contexts": "negative",
            "workers": 1,
            "use_llm": False,
            "llm": {},
        },
    }
    result = screening_microbatch.run_screening_microbatches(
        config=config,
        base=tmp_path,
        workspace=tmp_path / "workspace",
        canonical_inventory=documents,
        end_stage=3,
        grobid_client=object(),
        softcite_client=None,
        toolbox_profile=None,
        store_factory=lambda _records: None,
    )
    assert result["microbatch"]["batches"] == 3
    assert result["stage02"]["papers"] == 5
    assert result["stage03"]["decisions"] == {"strong_candidate": 5}
    for index, expected in enumerate((2, 2, 1), start=1):
        state = read_json(
            tmp_path / "workspace/microbatches" / f"batch_{index:06d}" / "state.json"
        )
        assert state["completed_stages"] == [2, 3]
        assert len(state["paper_ids"]) == expected


def test_redesigned_microbatch_resume_does_not_repeat_completed_stages(tmp_path, monkeypatch):
    documents = _documents(tmp_path, 2)

    def fake_extract(records, _client, **_kwargs):
        return [
            {
                **item,
                "grobid_extract_status": "success",
                "text_path": item["source_path"],
            }
            for item in records
        ]

    monkeypatch.setattr(screening_microbatch, "extract_documents_with_grobid", fake_extract)
    config = {
        "microbatch": {"size": 1, "concurrency": 2, "resume": True},
        "grobid_extract": {"workers": 1, "fallback": {}},
    }
    kwargs = {
        "config": config,
        "base": tmp_path,
        "workspace": tmp_path / "workspace",
        "canonical_inventory": documents,
        "end_stage": 2,
        "grobid_client": object(),
        "softcite_client": None,
        "toolbox_profile": None,
        "store_factory": lambda _records: None,
    }
    first = screening_microbatch.run_screening_microbatches(**kwargs)
    assert first["stage02"]["documents"] == 2
    monkeypatch.setattr(
        screening_microbatch,
        "extract_documents_with_grobid",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("stage repeated")),
    )
    resumed = screening_microbatch.run_screening_microbatches(**kwargs)
    assert resumed["stage02"]["documents"] == 2
