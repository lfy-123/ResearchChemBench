from __future__ import annotations

import json
from pathlib import Path

from src.stages.stage00_remote_corpus import DATASETS, prepare_remote_corpus


class FakeStore:
    def __init__(self):
        self.payloads = {
            "s3://example/pdfs/10.1000_one.pdf": b"main-one",
            "s3://example/pdfs/10.1000_two.pdf": b"main-two",
            "s3://example/support/10.1000_one_sup_1.pdf": b"si-one",
        }
        self.rows = [
            {
                "doi": "10.1000/one",
                "pdf_filename": "10.1000_one.pdf",
                "relative_path": "pdfs/10.1000_one.pdf",
                "support_path": ["support/10.1000_one_sup_1.pdf"],
                "title": "One",
                "journal_name": "Journal",
            },
            {
                "doi": "10.1000/two",
                "pdf_filename": "10.1000_two.pdf",
                "relative_path": "pdfs/10.1000_two.pdf",
                "support_path": [],
                "title": "Two",
                "journal_name": "Journal",
            },
        ]

    def iter_uris(self, _prefix, *, start_after=None):
        for uri in sorted(key for key in self.payloads if key.startswith(_prefix)):
            if not start_after or uri > start_after:
                yield uri

    def iter_jsonl(self, _uri):
        yield from self.rows

    def stat(self, uri):
        return {"size_bytes": len(self.payloads[uri]), "etag": f"etag-{len(self.payloads[uri])}"}

    def copy_to(self, uri, destination):
        target = Path(destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.payloads[uri])
        return self.stat(uri)


def test_stage00_groups_main_and_supplementary_and_resumes(tmp_path, monkeypatch):
    dataset = "fake"
    monkeypatch.setitem(
        DATASETS,
        dataset,
        {
            "root": "s3://example/",
            "pdf_prefix": "s3://example/pdfs/",
            "metadata_uri": "s3://example/metadata.jsonl",
            "metadata_root": "s3://example/",
            "supplementary_prefix": "s3://example/support/",
        },
    )
    result = prepare_remote_corpus(tmp_path, dataset=dataset, count=2, store=FakeStore())

    assert result["summary"]["papers"] == 2
    assert result["summary"]["supplementary_documents"] == 1
    rows = [json.loads(line) for line in (tmp_path / "selected_papers.jsonl").read_text().splitlines()]
    first = tmp_path / "corpus" / rows[0]["paper_id"]
    assert len(list((first / "main").glob("*.pdf"))) == 1
    assert len(list((first / "supplementary").glob("*.pdf"))) == 1
    assert json.loads((first / "paper.json").read_text())["doi"] == "10.1000/one"

    resumed = prepare_remote_corpus(tmp_path, dataset=dataset, count=2, store=FakeStore())
    assert resumed["summary"]["reused"] is True
    assert len(list((tmp_path / "corpus").glob("*/paper.json"))) == 2


def test_stage00_uses_existing_inventory_not_stale_metadata_path(tmp_path, monkeypatch):
    store = FakeStore()
    store.rows[0]["support_path"] = ["stale/10.1000_one_sup_99.pdf"]
    monkeypatch.setitem(
        DATASETS,
        "fake-stale",
        {
            "root": "s3://example/",
            "pdf_prefix": "s3://example/pdfs/",
            "supplementary_prefix": "s3://example/support/",
            "metadata_uri": "s3://example/metadata.jsonl",
            "metadata_root": "s3://example/",
        },
    )

    result = prepare_remote_corpus(
        tmp_path, dataset="fake-stale", count=1, store=store
    )

    record = result["records"][0]
    assert record["supplementary_discovery"]["metadata_support_hints"] == [
        "stale/10.1000_one_sup_99.pdf"
    ]
    assert record["supplementary_discovery"]["matched_remote_uris"] == [
        "s3://example/support/10.1000_one_sup_1.pdf"
    ]
    assert record["supplementary_copy_status"] == "copied"


def test_stage00_large_dataset_strategy_verifies_metadata_objects(tmp_path, monkeypatch):
    store = FakeStore()
    store.rows[0]["support_path"] = [
        "support/10.1000_one_sup_1.pdf",
        "support/10.1000_one_sup_2.pdf",
    ]
    monkeypatch.setitem(
        DATASETS,
        "fake-verified",
        {
            "root": "s3://example/",
            "pdf_prefix": "s3://example/pdfs/",
            "supplementary_prefix": "s3://example/support/",
            "supplementary_discovery": "metadata_verified",
            "metadata_uri": "s3://example/metadata.jsonl",
            "metadata_root": "s3://example/",
        },
    )

    result = prepare_remote_corpus(
        tmp_path, dataset="fake-verified", count=1, store=store
    )

    record = result["records"][0]
    assert len(record["supplementary_documents"]) == 1
    assert record["supplementary_discovery"]["matched_remote_uris"] == [
        "s3://example/support/10.1000_one_sup_1.pdf"
    ]
    assert len(record["supplementary_discovery"]["verification_failures"]) == 1


def test_stage00_rejects_metadata_support_uri_outside_dataset_prefix(
    tmp_path, monkeypatch
):
    store = FakeStore()
    store.rows[0]["support_path"] = [
        "s3://example/other/10.1000_one_sup_1.pdf"
    ]
    monkeypatch.setitem(
        DATASETS,
        "fake-prefix",
        {
            "root": "s3://example/",
            "pdf_prefix": "s3://example/pdfs/",
            "supplementary_prefix": "s3://example/support/",
            "supplementary_discovery": "metadata_verified",
            "metadata_uri": "s3://example/metadata.jsonl",
            "metadata_root": "s3://example/",
        },
    )

    result = prepare_remote_corpus(
        tmp_path, dataset="fake-prefix", count=1, store=store
    )

    discovery = result["records"][0]["supplementary_discovery"]
    assert discovery["matched_remote_uris"] == []
    assert "outside the dataset supplementary prefix" in discovery[
        "verification_failures"
    ][0]["error"]
