from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pymupdf

from src.stages.paper_metadata import (
    canonical_metadata_index,
    canonical_paper_metadata,
    locate_grobid_tei,
)
from src.stages.pdf_layout import (
    extract_layout_blocks,
    install_document_query_tool,
    query_layout,
    write_layout_blocks,
)
from src.stages.stage06_task_builder.prompts import final_task_synthesis_instructions
from src.stages.stage06_task_builder.stage import _prepare_input_snapshot
from src.stages.stage07_task_judge.prompts import final_task_audit_instructions


def _pdf(path: Path) -> None:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Coordinate table")
    page.insert_text((72, 100), "15   6   0   -2.783404   -1.943641   0.767615")
    document.save(path)
    document.close()


def _tei(title: str, authors: list[tuple[str, str]]) -> str:
    people = "".join(
        f"<author><persName><forename>{first}</forename><surname>{last}</surname>"
        "</persName></author>"
        for first, last in authors
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc>
<titleStmt><title type="main">{title}</title>{people}</titleStmt>
<publicationStmt><date when="2026-01-15"/></publicationStmt>
<sourceDesc><biblStruct><analytic>{people}<idno type="DOI">10.test/v20</idno></analytic>
<monogr><title level="j">Journal</title><imprint><date when="2026-01-15"/></imprint></monogr>
</biblStruct></sourceDesc></fileDesc></teiHeader><text><body><p>Body.</p></body></text></TEI>"""


def test_pdf_layout_preserves_page_text_and_bbox(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    _pdf(source)
    rows = extract_layout_blocks(source)
    assert rows
    assert {row["page"] for row in rows} == {1}
    assert all(len(row["bbox"]) == 4 for row in rows)
    assert any("-2.783404   -1.943641" in row["text"] for row in rows)


def test_layout_query_recovers_original_columns_and_context(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    _pdf(source)
    layout = tmp_path / "inputs/documents/doc_fixture/layout_blocks.jsonl"
    write_layout_blocks(source, layout)
    rows = query_layout(tmp_path / "inputs", contains="-2.783404", context=1)
    assert any("-2.783404   -1.943641" in row["text"] for row in rows)
    assert {row["document_id"] for row in rows} == {"doc_fixture"}


def test_installed_document_query_cli_supports_pages_and_contains(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    _pdf(source)
    write_layout_blocks(
        source, tmp_path / "inputs/documents/doc_fixture/layout_blocks.jsonl"
    )
    tool = install_document_query_tool(tmp_path / "inputs/tools")
    completed = subprocess.run(
        [
            sys.executable,
            str(tool),
            "--root",
            str(tmp_path / "inputs"),
            "--document",
            "doc_fixture",
            "--page",
            "1",
            "--contains",
            "coordinate",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    row = json.loads(completed.stdout.splitlines()[0])
    assert row["document_id"] == "doc_fixture"
    assert row["page"] == 1


def test_snapshot_contains_layout_but_no_scientific_reconstruction(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    markdown = tmp_path / "document.md"
    blocks = tmp_path / "content_blocks.jsonl"
    _pdf(source)
    markdown.write_text("-2.783404-1.943641", encoding="utf-8")
    blocks.write_text(
        json.dumps({"evidence_id": "ev1", "text": "coordinate table"}) + "\n",
        encoding="utf-8",
    )
    snapshot = _prepare_input_snapshot(
        stage_root=tmp_path / "stage06",
        paper_id="paper_fixture20",
        candidates=[{"paper_id": "paper_fixture20"}],
        stage02=None,
        stage03=None,
        stage04={"paper_id": "paper_fixture20"},
        documents=[
            {
                "paper_id": "paper_fixture20",
                "document_id": "doc_fixture",
                "document_role": "main_paper",
                "normalized_markdown_path": str(markdown),
                "content_blocks_path": str(blocks),
                "source_path": str(source),
            }
        ],
        config={},
        run_id="run_fixture20",
    )
    layout = snapshot["root"] / "documents/doc_fixture/layout_blocks.jsonl"
    assert layout.is_file()
    assert "-2.783404   -1.943641" in layout.read_text(encoding="utf-8")
    assert snapshot["source_manifest"][0]["layout_status"] == "available"


def test_canonical_metadata_prefers_tei_header_and_normalized_date(tmp_path: Path) -> None:
    tei = tmp_path / "doc_main.tei.xml"
    tei.write_text(
        _tei("TEI title", [("Ada", "Lovelace"), ("Grace", "Hopper")]),
        encoding="utf-8",
    )
    metadata = canonical_paper_metadata(
        paper_id="paper_fixture20",
        paper_records=[
            {"title": "Paper-level title", "doi": "10.test/v20", "journal_name": "Journal"}
        ],
        documents=[
            {
                "document_role": "main_paper",
                "source_record": {
                    "publication_date": "15 January 2026",
                    "publication_date_normalized": "2026-01-15",
                },
                "pdf_metadata": {"Author": "Ada Lovelace"},
            }
        ],
        tei_paths=[tei],
    )
    assert metadata == {
        "paper_id": "paper_fixture20",
        "title": "Paper-level title",
        "doi": "10.test/v20",
        "journal": "Journal",
        "publication_date": "2026-01-15",
        "publication_year": 2026,
        "authors": ["Ada Lovelace", "Grace Hopper"],
    }


def test_canonical_metadata_uses_only_explicit_pdf_author_list() -> None:
    common = {
        "paper_id": "paper_fixture20",
        "documents": [{"document_role": "main_paper", "pdf_metadata": {}}],
    }
    incomplete = canonical_paper_metadata(**common)
    assert incomplete["authors"] == []
    common["documents"][0]["pdf_metadata"]["Author"] = "Ada Lovelace; Grace Hopper"
    complete = canonical_paper_metadata(**common)
    assert complete["authors"] == ["Ada Lovelace", "Grace Hopper"]


def test_complete_pdf_author_list_trims_grobid_affiliation_fragments(tmp_path: Path) -> None:
    tei = tmp_path / "doc_main.tei.xml"
    tei.write_text(
        _tei(
            "Title",
            [("Ada", "Lovelace"), ("Grace", "Hopper"), ("Research", "Center")],
        ),
        encoding="utf-8",
    )
    metadata = canonical_paper_metadata(
        paper_id="paper_fixture20",
        documents=[
            {
                "document_role": "main_paper",
                "pdf_metadata": {"Author": "Ada Lovelace, and Grace Hopper"},
            }
        ],
        tei_paths=[tei],
    )
    assert metadata["authors"] == ["Ada Lovelace", "Grace Hopper"]


def test_historical_tei_locator_is_document_id_based(tmp_path: Path) -> None:
    target = (
        tmp_path
        / "batches/batch-0001/microbatches/batch-0001/resume_attempts/generation-0001"
        / "stage01/stage_01_document_preparation/raw/grobid/tei/doc_fixture.tei.xml"
    )
    target.parent.mkdir(parents=True)
    target.write_text(_tei("Title", [("Ada", "Lovelace")]), encoding="utf-8")
    assert locate_grobid_tei(tmp_path, ["doc_fixture"]) == [target]


def test_canonical_metadata_index_groups_records_by_paper() -> None:
    index = canonical_metadata_index(
        paper_ids={"paper_a", "paper_b"},
        paper_records=[
            {"paper_id": "paper_a", "title": "A"},
            {"paper_id": "paper_b", "title": "B"},
        ],
        documents=[],
    )
    assert index["paper_a"]["title"] == "A"
    assert index["paper_b"]["title"] == "B"


def test_prompts_assign_science_to_agents_without_fixed_input_checker() -> None:
    synthesis = final_task_synthesis_instructions(
        paper_id="paper_fixture20", snapshot_hash="hash"
    )
    assert "document_query.py" in synthesis
    assert "column merging is not by itself a scientific rejection reason" in synthesis
    assert "actual public input contents" in synthesis
    assert "fixed asset checklist" in synthesis
    assert "inspect_assets.py" not in synthesis
    audit = final_task_audit_instructions(paper_id="paper_fixture20")
    assert "layout/source-PDF evidence" in audit
    assert "Format validity alone is not scientific identity" in audit
    assert "You are not a fallback task builder" in audit


def test_shared_gate_does_not_import_scientific_evidence_helpers() -> None:
    source = Path("src/stages/phase_gate.py").read_text(encoding="utf-8")
    assert "pdf_layout" not in source
    assert "paper_metadata" not in source
    assert "inspect_assets" not in source
