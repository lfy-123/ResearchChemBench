from __future__ import annotations

from chemistry_toolbox.mcp.execution_models import (
    DocumentationReadRequest,
    DocumentationSearchRequest,
    SoftwareInspectRequest,
)
from chemistry_toolbox.mcp.software_catalog import (
    inspect_software,
    read_software_documentation,
    search_software_documentation,
    software_document_chunks,
)


HIGH_FREQUENCY_SOFTWARE = {"orca", "gaussian", "crest", "vasp", "lobster"}


def test_high_frequency_software_has_index_tasks_and_troubleshooting() -> None:
    for software_id in HIGH_FREQUENCY_SOFTWARE:
        chunks = software_document_chunks(software_id, include_cached=False)
        topics = {topic for chunk in chunks if not chunk["shared"] for topic in chunk["topics"]}
        assert "index" in topics
        assert "troubleshooting" in topics
        assert len({chunk["path"] for chunk in chunks if not chunk["shared"]}) >= 4


def test_inspection_returns_compact_document_topic_index() -> None:
    result = inspect_software(SoftwareInspectRequest(software_id="orca"))
    paths = {item["path"] for item in result["documentation_index"]}
    assert "chemistry_toolbox/native_software_docs/orca/INDEX.md" in paths
    assert "staging" in result["shared_documentation_topics"]


def test_exact_topic_and_section_read_is_bounded() -> None:
    result = read_software_documentation(
        DocumentationReadRequest(
            software_id="gaussian",
            topic="quickstart",
            section="required sections",
            max_chars=2000,
        )
    )
    assert result["source_policy"] == "first_party_markdown_exact_route"
    assert result["sections"][0]["heading"] == "Required sections"
    assert "blank line" in result["sections"][0]["content"]


def test_document_search_ranks_relevant_heading_and_reports_fallback() -> None:
    result = search_software_documentation(
        DocumentationSearchRequest(
            software_id="lobster",
            query="high charge spilling",
            retrieval_mode="hybrid",
        )
    )
    assert result["matches"][0]["heading"] == "Projection quality"
    assert result["matches"][0]["source_type"] == "first_party_markdown"
    assert result["retrieval"]["semantic_status"].startswith(
        ("available", "unavailable", "stale")
    )
