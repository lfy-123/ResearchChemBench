from __future__ import annotations

import json

from chemistry_toolbox.mcp.discovery_models import ProgressiveActionRequest
from chemistry_toolbox.mcp.discovery_tools import execute_action
from chemistry_toolbox.mcp.result_transport import compact_action_result
from researchchem_toolbox.catalog import action_specs, catalog_snapshot
from researchchem_toolbox.discovery import (
    inspect_action,
    inspect_backend,
    inspect_resource,
    list_action_domains,
    search_actions,
    search_resources,
)


def _snapshot() -> dict:
    return catalog_snapshot(include_health=False, discovery_mode="progressive")


def test_domain_index_and_pagination_reach_the_complete_catalog():
    snapshot = _snapshot()
    domains = list_action_domains(snapshot=snapshot)
    assert domains["status"] == "success"
    assert sum(item["action_count"] for item in domains["domains"]) == len(action_specs())
    indexed = {
        action_id
        for domain in domains["domains"]
        for action_id in domain["action_ids"]
    }
    assert indexed == set(action_specs())

    first = search_actions(limit=100, snapshot=snapshot)
    second = search_actions(limit=100, offset=100, snapshot=snapshot)
    discovered = {
        item["action_id"] for item in [*first["actions"], *second["actions"]]
    }
    assert discovered == set(action_specs())
    assert first["ordering"] == "stable_action_id_order_not_relevance_ranked"


def test_action_search_and_inspection_return_exact_provider_contracts():
    snapshot = _snapshot()
    search = search_actions(
        query="thermochemical selectivity",
        backend_id="goodvibes",
        snapshot=snapshot,
    )
    assert "analyze_thermochemical_selectivity" in {
        item["action_id"] for item in search["actions"]
    }

    action = inspect_action(
        "analyze_thermochemical_selectivity",
        backend_id="goodvibes",
        snapshot=snapshot,
    )
    assert action["action"]["selection_policy"] == "agent_backend_required"
    contract = action["provider_contracts"][0]
    assert contract["backend_id"] == "goodvibes"
    assert contract["required_input_fields"]
    assert "method_parameter_reference" in contract
    request_contract = action["selected_request_contract"]
    assert request_contract["execute_action_request_template"]["action_id"] == (
        "analyze_thermochemical_selectivity"
    )
    assert request_contract["execute_action_request_template"]["backend_id"] == "goodvibes"
    assert request_contract["sections"]["inputs"]["required"]
    assert request_contract["sections"]["action_settings"]["required"]
    assert request_contract["output_contract"]["primary_output"]
    assert action["automatic_fallback"] is False

    morphology = search_actions(
        query="geometry optimization",
        category="molecular_electronic",
        snapshot=snapshot,
    )
    assert "optimize_geometry" in {
        item["action_id"] for item in morphology["actions"]
    }
    precise = search_actions(
        query="optimize geometry",
        action_kind="scientific",
        snapshot=snapshot,
    )
    assert "calculate_atomic_charges" not in {
        item["action_id"] for item in precise["actions"]
    }

    unresolved = inspect_action("optimize_geometry", snapshot=snapshot)
    assert unresolved["selected_request_contract"] is None
    assert "backend_id" in unresolved["request_contract_note"]

    backend = inspect_backend("goodvibes", snapshot=snapshot)
    assert "analyze_thermochemical_selectivity" in {
        item["action_id"] for item in backend["capabilities"]
    }


def test_selected_structure_contract_includes_canonical_inline_example():
    action = inspect_action(
        "optimize_geometry", backend_id="xtb", snapshot=_snapshot()
    )
    structure = next(
        field
        for field in action["selected_request_contract"]["sections"]["inputs"]["required"]
        if field["name"] == "structure"
    )
    example = structure["canonical_inline_example"]
    assert example["atoms"][0] == {
        "element": "H",
        "position_angstrom": [0.0, 0.0, 0.0],
    }


def test_registered_resources_are_searchable_and_resolvable():
    snapshot = _snapshot()
    search = search_resources(
        query="vasp paw pbe",
        backend_id="vasp",
        snapshot=snapshot,
    )
    ids = {item["resource_id"] for item in search["resources"]}
    assert "vasp_paw_pbe_54" in ids
    resource = inspect_resource("vasp_paw_pbe_54", snapshot=snapshot)
    assert resource["resource"]["selection_syntax"]
    assert "vasp" in resource["resource"]["compatible_backends"]


def test_progressive_dispatch_traces_the_real_action_id(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    for directory in ("outputs", "code", "_tool_results", "_tool_artifacts"):
        (tmp_path / directory).mkdir()
    (tmp_path / "_toolbox_catalog.json").write_text(
        json.dumps(_snapshot()), encoding="utf-8"
    )

    # Missing inputs intentionally exercises dispatcher validation without
    # launching a worker; the transport must still preserve the real Action id.
    result = execute_action(
        ProgressiveActionRequest(action_id="normalize_qcschema_molecule")
    )
    assert result["status"] == "invalid_request"
    event = json.loads((tmp_path / "_tool_trace.jsonl").read_text().splitlines()[0])
    assert event["tool"] == "normalize_qcschema_molecule"
    assert event["arguments"]["entrypoint"] == "progressive_execute_action"
    assert event["status"] == "invalid_request"


def test_composite_and_typed_handoff_contracts_are_explicit():
    snapshot = _snapshot()
    sella = inspect_action(
        "locate_transition_state", backend_id="sella", snapshot=snapshot
    )["selected_request_contract"]
    assert sella["execute_action_request_template"]["action_settings"][
        "calculator_action_settings"
    ] == {"calculate_energy": {}, "calculate_forces": {}}
    assert sella["component_request_contracts"]["calculator"][
        "required_nested_actions"
    ] == ["calculate_energy", "calculate_forces"]

    pysisyphus = inspect_action(
        "locate_transition_state", backend_id="pysisyphus", snapshot=snapshot
    )["selected_request_contract"]
    assert "hessian_init" in pysisyphus["execute_action_request_template"][
        "action_settings"
    ]
    pysis_settings = {
        item["name"]: item
        for item in pysisyphus["sections"]["action_settings"]["required"]
    }
    assert pysis_settings["optimizer"]["allowed_values"] == [
        "rsprfo",
        "prfo",
        "trim",
        "rsirfo",
        "irfo",
    ]
    assert "normal" not in pysis_settings["convergence"]["allowed_values"]
    assert any(
        item["name"] == "basis"
        for item in pysisyphus["sections"]["method_spec"]["optional_documented"]
    )

    vibrations = inspect_action(
        "derive_vibrational_modes",
        backend_id="internal_vibrations",
        snapshot=snapshot,
    )["selected_request_contract"]
    assert "never reuse one artifact_id" in vibrations["output_contract"][
        "input_handoff_note"
    ]
    required = {
        item["name"]: item
        for item in vibrations["sections"]["inputs"]["required"]
    }
    assert required["hessian"]["type"] == "Hessian | ArtifactRef"


def test_progressive_result_transport_keeps_scalars_and_compacts_dense_values():
    primary = {
        "artifact_id": "art_11111111111111111111111111111111",
        "semantic_type": "Hessian",
        "media_type": "application/json",
        "sha256": "a" * 64,
        "path": "_tool_artifacts/objects/hessian.json",
        "producer_action": "calculate_hessian",
        "producer_backend": "xtb",
        "parent_artifact_ids": ["art_22222222222222222222222222222222"],
    }
    noisy = {
        "artifact_id": "art_33333333333333333333333333333333",
        "semantic_type": "BackendFile",
        "media_type": "text/plain",
        "sha256": "b" * 64,
        "path": "outputs/stdout.log",
        "producer_action": "calculate_hessian",
        "producer_backend": "xtb",
        "parent_artifact_ids": [],
    }
    compact = compact_action_result(
        {
            "status": "success",
            "action": "calculate_hessian",
            "result": {
                "matrix": [[float(row + column) for column in range(300)] for row in range(300)],
                "unit": "hartree/bohr^2",
            },
            "input_artifacts": [],
            "output_artifacts": [primary, noisy],
            "warnings": [],
            "error": None,
        }
    )
    assert compact["result"]["unit"] == "hartree/bohr^2"
    assert compact["result"]["matrix"]["shape"] == [300, 300]
    assert compact["result"]["matrix"]["artifact_id"] == primary["artifact_id"]
    assert compact["output_artifacts"] == [primary]
    assert compact["transport"]["supplementary_artifact_count"] == 1
    assert len(json.dumps(compact)) < 10_000
