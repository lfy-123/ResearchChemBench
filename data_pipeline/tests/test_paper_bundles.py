from __future__ import annotations

import json

from src.stages.stage01_inventory import group_inventory_by_paper, inventory_corpus
from src.stages.stage02_parsing import build_paper_text_bundles


def test_inventory_uses_stage00_paper_manifest_and_groups_si(tmp_path, monkeypatch):
    bundle = tmp_path / "paper_1"
    (bundle / "main").mkdir(parents=True)
    (bundle / "supplementary").mkdir()
    main = bundle / "main" / "paper.pdf"
    si = bundle / "supplementary" / "paper_si.pdf"
    main.write_bytes(b"main")
    si.write_bytes(b"si")
    (bundle / "paper.json").write_text(
        json.dumps(
            {
                "paper_id": "paper_1",
                "doi": "10.1000/example",
                "dataset": "fake",
                "main_document": {
                    "relative_path": "main/paper.pdf",
                    "document_role": "main_paper",
                    "remote_uri": "s3://fake/paper.pdf",
                },
                "supplementary_documents": [
                    {
                        "relative_path": "supplementary/paper_si.pdf",
                        "document_role": "supplementary",
                        "remote_uri": "s3://fake/paper_si.pdf",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("src.stages.stage01_inventory.corpus.pdf_info", lambda _path: {})

    records = inventory_corpus(tmp_path)
    assert {item["paper_id"] for item in records} == {"paper_1"}
    assert {item["document_role"] for item in records} == {"main_paper", "supplementary"}
    papers = group_inventory_by_paper(records)
    assert papers[0]["main_documents"]
    assert papers[0]["supplementary_documents"]


def test_stage02_bundle_keeps_main_and_supplementary_text():
    documents = [
        {
            "paper_id": "paper",
            "document_id": "main",
            "document_role": "main_paper",
            "text_path": "/tmp/main.txt",
            "grobid_extract_status": "success",
            "title": "Paper",
        },
        {
            "paper_id": "paper",
            "document_id": "si",
            "document_role": "supplementary",
            "text_path": "/tmp/si.txt",
            "grobid_extract_status": "fallback_pdftotext",
        },
    ]
    bundle = build_paper_text_bundles(documents)[0]
    assert bundle["usable_main_text"] is True
    assert bundle["usable_supplementary_text"] is True
    assert bundle["has_local_supplementary"] is True
