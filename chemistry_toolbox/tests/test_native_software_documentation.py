from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

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
TOOLBOX_ROOT = Path(__file__).resolve().parents[1]


def test_high_frequency_software_has_index_tasks_and_troubleshooting() -> None:
    for software_id in HIGH_FREQUENCY_SOFTWARE:
        chunks = software_document_chunks(software_id, include_cached=False)
        topics = {topic for chunk in chunks if not chunk["shared"] for topic in chunk["topics"]}
        assert "index" in topics
        assert "troubleshooting" in topics
        assert len({chunk["path"] for chunk in chunks if not chunk["shared"]}) >= 4


def test_every_native_software_has_structured_first_party_documentation() -> None:
    script = TOOLBOX_ROOT / "scripts" / "generate_native_software_manuals.py"
    spec = importlib.util.spec_from_file_location("generate_native_manuals", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    generated = module.generated_manuals()
    assert len(generated) == 51
    for path, expected in generated.items():
        assert path.read_text(encoding="utf-8") == expected
    for software_id in module.HAND_WRITTEN_SOFTWARE:
        assert (module.DOCS_ROOT / software_id / "INDEX.md").is_file()


def test_all_first_party_manuals_use_complete_front_matter() -> None:
    required = {
        "software_id",
        "versions",
        "topics",
        "aliases",
        "inputs",
        "outputs",
        "last_smoke_tested",
    }
    for path in (TOOLBOX_ROOT / "native_software_docs").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        end = text.index("\n---\n", 4)
        metadata = yaml.safe_load(text[4:end])
        assert required <= set(metadata), path


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
    assert result["retrieval_usage"]["estimated_context_tokens"] > 0


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
    assert result["retrieval"]["estimated_context_tokens"] > 0
