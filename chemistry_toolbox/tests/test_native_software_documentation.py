from __future__ import annotations

import importlib.util
import json
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
from chemistry_toolbox.mcp.open_tools import (
    search_software_documentation as traced_search_software_documentation,
    validate_native_job as traced_validate_native_job,
)
from chemistry_toolbox.mcp.execution_models import NativeJobRequest


HIGH_FREQUENCY_SOFTWARE = {"orca", "gaussian", "crest", "vasp", "lobster"}
PLACEHOLDER_SOFTWARE: set[str] = set()
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
    assert len(generated) >= 350
    for path, expected in generated.items():
        assert path.read_text(encoding="utf-8") == expected
    guides, profiles, contracts = module.load_sources()
    assert len(guides) == len(profiles) == len(contracts) == 63
    assert set(guides) == set(profiles) == set(contracts)
    assert {
        software_id
        for software_id, profile in profiles.items()
        if profile["operational_status"] == "placeholder"
    } == PLACEHOLDER_SOFTWARE
    for software_id in set(guides) - PLACEHOLDER_SOFTWARE:
        root = module.DOCS_ROOT / software_id
        for filename in module.STANDARD_FILES:
            assert (root / filename).is_file(), (software_id, filename)
        example = root / "examples" / "interface_smoke"
        assert (example / "native_command.sh").is_file()
        assert (example / "submit_request.json").is_file()
        assert (example / "smoke_result.json").is_file()


def test_manual_example_contracts_have_valid_file_roles_and_resources() -> None:
    script = TOOLBOX_ROOT / "scripts" / "generate_native_software_manuals.py"
    spec = importlib.util.spec_from_file_location("generate_native_manuals", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    guides, profiles, contracts = module.load_sources()

    assert profiles["openmolcas"]["installed_version"] == "25.10"
    for software_id, guide in guides.items():
        for executable, command in guide["commands"].items():
            contract = contracts[software_id]["commands"][executable]
            assert not set(contract["inputs"]) & set(contract["outputs"])
            assert module._parallel_width(contract["arguments"]) <= contract[
                "resource_limits"
            ]["cpu_cores"]
            if command.get("enabled", True) is not True:
                for filename in module.STANDARD_FILES:
                    path = module.DOCS_ROOT / software_id / filename
                    if path.is_file():
                        assert f"Command: `{executable}`" not in path.read_text(
                            encoding="utf-8"
                        )

    psi4_contract = contracts["psi4"]["commands"]["psi4"]
    assert "output.dat" in psi4_contract["outputs"]
    assert "output.dat" not in psi4_contract["inputs"]
    assert psi4_contract["resource_limits"]["cpu_cores"] == 4


def test_detailed_manuals_are_substantive_and_examples_match_current_contract() -> None:
    for root in sorted((TOOLBOX_ROOT / "native_software_docs").iterdir()):
        if not root.is_dir() or root.name.startswith("_") or root.name in PLACEHOLDER_SOFTWARE:
            continue
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(root.glob("*.md"))
        )
        assert len(combined.splitlines()) >= 180, root
        for required in (
            "Installed version",
            "Working directory",
            "Resource",
            "convergence",
            "Pre-submission checklist",
        ):
            assert required.casefold() in combined.casefold(), (root, required)
        example = root / "examples" / "interface_smoke" / "submit_request.json"
        if not example.is_file():
            example = root / "examples" / "action_smoke" / "submit_request.json"
        request = json.loads(example.read_text(encoding="utf-8"))
        assert request["software_id"] == root.name
        assert "walltime_seconds" not in request["resource_limits"]


def test_native_interface_smoke_manifest_covers_catalog_and_hashes_verify() -> None:
    script = TOOLBOX_ROOT / "scripts" / "run_native_interface_smokes.py"
    spec = importlib.util.spec_from_file_location("run_native_interface_smokes", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.verify(module.DEFAULT_EVIDENCE)
    assert result["valid"], result["errors"]
    manifest = json.loads(module.DEFAULT_EVIDENCE.joinpath("manifest.json").read_text())
    guide_ids = set(
        yaml.safe_load((TOOLBOX_ROOT / "config" / "native_software_guides.yaml").read_text())[
            "software"
        ]
    )
    evidence_ids = {item["software_id"] for item in manifest["software"]}
    assert evidence_ids == guide_ids
    assert sum(result["counts"].values()) == len(guide_ids) == 63
    assert result["counts"].get("skipped", 0) == 0


def test_read_only_software_search_traces_without_workspace_scan(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def unexpected_snapshot():
        raise AssertionError("read-only software search must not scan workspace artifacts")

    monkeypatch.setattr("chemistry_toolbox.mcp.tracing.workspace_snapshot", unexpected_snapshot)
    result = traced_search_software_documentation(
        DocumentationSearchRequest(
            software_id="gaussian",
            query="route blank line title",
            retrieval_mode="lexical",
        )
    )
    assert result["status"] == "success"
    event = yaml.safe_load((tmp_path / "_tool_trace.jsonl").read_text().splitlines()[0])
    assert event["tool"] == "search_software_documentation"
    assert event["artifacts"] == []


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


def test_inspection_exposes_smoke_axes_and_known_runtime_blockers() -> None:
    orca = inspect_software(SoftwareInspectRequest(software_id="orca"))
    assert orca["executable_resolved"] is True
    assert orca["interface_smoke_status"] == "passed"
    assert orca["scientific_smoke_status"] == "passed"
    assert orca["native_available_for_submission"] is True

    for software_id in ("yambo", "sharc", "kinbot"):
        expanded = inspect_software(SoftwareInspectRequest(software_id=software_id))
        assert expanded["scientific_smoke_status"] == "passed"
        assert expanded["smoke_evidence"]["scientific_action_cases"]

    pysisyphus = inspect_software(SoftwareInspectRequest(software_id="pysisyphus"))
    assert pysisyphus["scientific_smoke_status"] == "passed"
    assert pysisyphus["smoke_evidence"]["recorded_test_level"] == "scientific_smoke"

    for software_id in ("vesta", "arkane", "rmg"):
        healthy = inspect_software(SoftwareInspectRequest(software_id=software_id))
        assert healthy["interface_smoke_status"] == "passed"
        assert healthy["native_available_for_submission"] is True
        assert healthy["known_runtime_blockers"] == []


def test_native_lint_failure_routes_to_exact_documentation_section(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = traced_validate_native_job(
        NativeJobRequest(
            software_id="gaussian",
            executable="g16",
            arguments=[],
            staged_inputs=[],
        )
    )
    assert result["status"] == "invalid_request"
    route = result["documentation_recovery"][0]
    assert route["tool"] == "read_software_documentation"
    assert route["request"]["software_id"] == "gaussian"
    assert route["request"]["topic"] == "troubleshooting"


def test_inspection_uses_validated_example_contracts() -> None:
    psi4 = inspect_software(SoftwareInspectRequest(software_id="psi4"))
    request = next(
        item["native_job_request_template"]
        for item in psi4["native_invocation_guides"]
        if item["executable"] == "psi4"
    )
    assert request["resource_limits"]["cpu_cores"] == 4
    assert request["declared_outputs"] == ["output.dat"]
    assert {item["target_path"] for item in request["staged_inputs"]} == {"input.dat"}


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
