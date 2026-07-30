from __future__ import annotations

import json
import threading
import time

from chemistry_toolbox.mcp.discovery_models import (
    ActionBatchItem,
    ActionBatchRequest,
    ActionSearchRequest,
    ProgressiveActionRequest,
)
from chemistry_toolbox.mcp.discovery_tools import (
    execute_action,
    search_actions as traced_search_actions,
    submit_action_batch,
)
from chemistry_toolbox.mcp.result_transport import compact_action_result
from researchchem_toolbox.catalog import action_specs, catalog_snapshot
from researchchem_toolbox.discovery import (
    browse_action_category,
    inspect_action,
    inspect_backend,
    inspect_resource,
    list_action_domains,
    search_actions,
    search_resources,
)


def test_progressive_detail_levels_bound_discovery_payloads() -> None:
    summary = search_actions(
        query="geometry optimization",
        limit=10,
        detail_level="summary",
    )
    full = search_actions(
        query="geometry optimization",
        limit=10,
        detail_level="full",
    )
    assert len(json.dumps(summary)) < len(json.dumps(full)) * 0.6
    assert "provider_ids" in summary["actions"][0]
    assert "providers" not in summary["actions"][0]

    contract = inspect_action(
        "calculate_energy",
        detail_level="contract",
    )
    complete = inspect_action("calculate_energy", detail_level="full")
    assert len(json.dumps(contract)) < len(json.dumps(complete)) * 0.4
    assert contract["selected_request_contract"] is None

    selected = inspect_action(
        "calculate_energy",
        backend_id="orca",
        detail_level="contract",
    )
    assert selected["selected_request_contract"] is not None
    assert selected["provider_contracts"][0]["backend_id"] == "orca"
    assert "health" not in selected["provider_contracts"][0]
    assert selected["selected_request_contract"]["template_kind"] == (
        "minimal_executable_request"
    )


def test_compact_contract_prevents_common_conformer_input_errors() -> None:
    cluster = inspect_action(
        "cluster_conformers", backend_id="rdkit", detail_level="contract"
    )["selected_request_contract"]
    ensemble = cluster["required_contract"]["inputs"][0]
    assert ensemble["name"] == "ensemble"
    assert ".sdf, .mol, or multi-frame .xyz" in " ".join(
        ensemble["accepted_forms"]
    )
    assert "path to a JSON summary" in " ".join(ensemble["rejected_forms"])

    crest = inspect_action(
        "generate_conformer_ensemble",
        backend_id="crest",
        detail_level="contract",
    )["selected_request_contract"]
    assert crest["execute_action_request_template"]["inputs"]["molecule"].startswith(
        "<AtomicStructure"
    )
    assert crest["important_optional_inputs"][0]["name"] == "initial_structure"
    assert any("overrides inputs.molecule" in note for note in crest["usage_notes"])

    full = inspect_action(
        "cluster_conformers", backend_id="rdkit", detail_level="full"
    )["selected_request_contract"]
    assert "sections" in full
    assert "backend_fixed_parameters" in full


def test_batch_safe_actions_keep_independent_child_trace_and_status(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    monkeypatch.setattr(
        "chemistry_toolbox.mcp.discovery_tools._execute_action",
        lambda action_id, request: {
            "status": "success",
            "action": action_id,
            "result": {"label": request["inputs"]["label"]},
            "output_artifacts": [],
        },
    )
    result = submit_action_batch(
        ActionBatchRequest(
            action_id="calculate_energy",
            backend_id="ase_emt",
            items=[
                ActionBatchItem(item_id="point_1", inputs={"label": "one"}),
                ActionBatchItem(item_id="point_2", inputs={"label": "two"}),
            ],
        )
    )
    assert result["status"] == "success"
    assert [item["item_id"] for item in result["items"]] == ["point_1", "point_2"]
    assert [item["result"]["result"]["label"] for item in result["items"]] == [
        "one",
        "two",
    ]
    trace = [json.loads(line) for line in (tmp_path / "_tool_trace.jsonl").read_text().splitlines()]
    assert len(trace) == 2
    assert {item["arguments"]["batch_item_id"] for item in trace} == {
        "point_1",
        "point_2",
    }
    assert result["execution_mode"] == "resource_aware_parallel"
    assert result["effective_max_concurrency"] == 2


def test_action_batch_runs_children_concurrently_and_queues_excess(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "2")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "8192")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT", "0")
    active = 0
    observed_peak = 0
    lock = threading.Lock()

    def delayed(action_id, request):
        nonlocal active, observed_peak
        with lock:
            active += 1
            observed_peak = max(observed_peak, active)
        try:
            time.sleep(0.12)
            return {
                "status": "success",
                "action": action_id,
                "result": {"label": request["inputs"]["label"]},
                "output_artifacts": [],
            }
        finally:
            with lock:
                active -= 1

    monkeypatch.setattr(
        "chemistry_toolbox.mcp.discovery_tools._execute_action", delayed
    )
    started = time.monotonic()
    result = submit_action_batch(
        ActionBatchRequest(
            action_id="calculate_energy",
            backend_id="ase_emt",
            items=[
                ActionBatchItem(
                    item_id=f"point_{index}",
                    inputs={"label": str(index)},
                    resource_limits={"cpu_cores": 1, "memory_mb": 4096},
                )
                for index in range(4)
            ],
        )
    )
    elapsed = time.monotonic() - started
    assert result["status"] == "success"
    assert result["effective_max_concurrency"] == 2
    assert result["peak_concurrency"] == 2
    assert observed_peak == 2
    assert elapsed < 0.4
    assert [item["item_id"] for item in result["items"]] == [
        "point_0",
        "point_1",
        "point_2",
        "point_3",
    ]


def test_action_batch_isolates_unexpected_child_transport_failure(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def one_failure(_action_id, request):
        if request["inputs"]["label"] == "bad":
            raise RuntimeError("transport broke")
        return {"status": "success", "result": {"label": "good"}}

    monkeypatch.setattr(
        "chemistry_toolbox.mcp.discovery_tools._execute_action", one_failure
    )
    result = submit_action_batch(
        ActionBatchRequest(
            action_id="calculate_energy",
            backend_id="ase_emt",
            items=[
                ActionBatchItem(item_id="good", inputs={"label": "good"}),
                ActionBatchItem(item_id="bad", inputs={"label": "bad"}),
            ],
        )
    )
    assert result["status"] == "partial_success"
    assert result["successful_item_count"] == 1
    assert result["items"][1]["result"]["error"]["code"] == (
        "batch_child_transport_error"
    )


def test_batch_safe_inspection_recommends_parallel_batch() -> None:
    inspected = inspect_action(
        "optimize_geometry", backend_id="orca", detail_level="contract"
    )
    parallel = inspected["parallel_execution"]
    assert parallel["recommended_tool"] == "submit_action_batch"
    assert "synchronous" in parallel["warning"]
    template = parallel["request_template"]
    assert template["action_id"] == "optimize_geometry"
    assert template["backend_id"] == "orca"


def test_batch_submission_rejects_actions_without_batch_safe_contract() -> None:
    result = submit_action_batch(
        ActionBatchRequest(
            action_id="calculate_dipole_moment",
            backend_id="xtb",
            items=[ActionBatchItem(item_id="one", inputs={})],
        )
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "action_not_batch_safe"


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
    assert first["ordering"] == "stable_action_id_order"


def test_category_browse_returns_the_complete_domain_choice_set():
    snapshot = _snapshot()
    result = browse_action_category(
        category="molecular_electronic", snapshot=snapshot
    )
    expected = {
        item.id
        for item in action_specs().values()
        if item.category == "molecular_electronic"
    }
    assert result["browse_mode"] == "complete_category"
    assert {item["action_id"] for item in result["actions"]} == expected


def test_action_search_uses_aliases_and_bm25_ranking():
    snapshot = _snapshot()
    cases = {
        "single point energy": "calculate_energy",
        "conformer energy": "calculate_energy",
        "electron density surface": "calculate_electron_isodensity_surface",
        "transition state search": "locate_transition_state",
        "phonon DOS": "calculate_phonon_density_of_states",
        "MMFF94 force field optimization preoptimization": "optimize_geometry",
    }
    for query, expected_first in cases.items():
        result = search_actions(
            query=query, retrieval_mode="lexical", snapshot=snapshot
        )
        assert result["actions"][0]["action_id"] == expected_first
        assert result["actions"][0]["relevance"]["bm25"] > 0
        assert result["retrieval"]["lexical_ranker"] == "bm25"

    electronic = search_actions(
        query="electronic energy", retrieval_mode="hybrid", snapshot=snapshot
    )
    assert electronic["actions"][0]["action_id"] == "calculate_energy"
    assert electronic["retrieval"]["semantic_status"].startswith(
        ("available", "unavailable", "stale")
    )
    assert electronic["predicted_categories"]
    assert electronic["actions"][0]["matched_fields"]
    assert electronic["actions"][0]["ranking_reason"]

    transition_state = search_actions(
        query="find a stationary structure with one negative curvature",
        retrieval_mode="hybrid",
        snapshot=snapshot,
    )
    assert transition_state["actions"][0]["action_id"] == "locate_transition_state"


def test_action_search_warns_when_category_filter_hides_exact_alias_match():
    snapshot = _snapshot()
    result = search_actions(
        query="geometry optimization",
        category="structure_and_system",
        retrieval_mode="hybrid",
        snapshot=snapshot,
    )

    advisory = result["category_filter_advisory"]
    assert advisory["code"] == "exact_match_outside_requested_category"
    assert advisory["suggested_action_id"] == "optimize_geometry"
    assert advisory["suggested_category"] == "molecular_electronic"


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


def test_progressive_requests_treat_null_optional_resources_as_omitted():
    request = ProgressiveActionRequest.model_validate(
        {
            "action_id": "calculate_correlated_electron_density",
            "resource_limits": {
                "cpu_cores": 8,
                "memory_mb": None,
                "gpu_count": None,
            },
        }
    )
    assert request.resource_limits.model_dump() == {
        "memory_mb": 4096,
        "cpu_cores": 8,
        "gpu_count": 0,
    }
    assert ProgressiveActionRequest.model_validate(
        {"action_id": "calculate_energy", "resource_limits": None}
    ).resource_limits.model_dump() == {
        "memory_mb": 4096,
        "cpu_cores": 1,
        "gpu_count": 0,
    }


def test_read_only_discovery_traces_without_scanning_workspace(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def unexpected_snapshot():
        raise AssertionError("read-only discovery must not scan workspace artifacts")

    monkeypatch.setattr("chemistry_toolbox.mcp.tracing.workspace_snapshot", unexpected_snapshot)
    result = traced_search_actions(
        ActionSearchRequest(
            query="rank conformers by free energy",
            retrieval_mode="lexical",
            limit=5,
        )
    )
    assert result["status"] == "success"
    event = json.loads((tmp_path / "_tool_trace.jsonl").read_text().splitlines()[0])
    assert event["tool"] == "search_actions"
    assert event["artifacts"] == []


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

    orca = inspect_action("calculate_energy", backend_id="orca", snapshot=snapshot)
    assert orca["provider_contracts"][0]["resource_constraints"][
        "maximum_cpu_cores"
    ] == 48
    assert "maximum_walltime_seconds" not in orca["provider_contracts"][0][
        "resource_constraints"
    ]
    orca_template = orca["selected_request_contract"][
        "execute_action_request_template"
    ]
    assert orca_template["resource_limits"]["cpu_cores"] == 1
    assert orca_template["resource_limits"]["memory_mb"] == 4096
    assert orca_template["resource_limits"]["gpu_count"] == 0
    assert orca["evaluation_resource_budget"]["cpu_cores"] == 48
    resource_parameters = {
        item["name"]: item
        for item in orca["selected_request_contract"]["sections"][
            "resource_limits"
        ]["optional_with_defaults"]
    }
    assert resource_parameters["cpu_cores"]["maximum"] == 48
    assert resource_parameters["memory_mb"]["maximum"] == 204800
    assert resource_parameters["gpu_count"]["maximum"] == 0

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
    thermochemistry = inspect_action(
        "derive_thermochemistry",
        backend_id="internal_thermochemistry",
        snapshot=snapshot,
    )["selected_request_contract"]
    thermochemistry_note = thermochemistry["output_contract"]["input_handoff_note"]
    assert "derive_vibrational_modes" in thermochemistry_note
    assert "Hessian, not a FrequencyResult" in thermochemistry_note

    density_export = inspect_action(
        "export_electron_density_grid",
        backend_id="orca",
        snapshot=snapshot,
    )["selected_request_contract"]
    density_input = density_export["sections"]["inputs"]["required"][0]
    assert density_input["type"] == "ElectronDensityResult ArtifactRef"
    assert "job.gbw" in " ".join(density_input["rejected_forms"])
    assert "ElectronDensityResult artifact_id" in density_export[
        "execute_action_request_template"
    ]["inputs"]["electron_density"]


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


def test_density_result_transport_exposes_exact_next_action_handoff():
    primary = {
        "artifact_id": "art_11111111111111111111111111111111",
        "semantic_type": "ElectronDensityResult",
        "media_type": "application/json",
        "sha256": "a" * 64,
        "path": "_tool_artifacts/objects/density.json",
        "producer_action": "calculate_correlated_electron_density",
        "producer_backend": "orca",
        "parent_artifact_ids": [],
    }
    compact = compact_action_result(
        {
            "status": "success",
            "action": "calculate_correlated_electron_density",
            "result": {"files": {"gbw": "outputs/job.gbw"}},
            "input_artifacts": [],
            "output_artifacts": [primary],
            "warnings": [],
            "error": None,
        }
    )
    handoff = compact["artifact_handoff"]["next_action_example"]
    assert handoff["inputs"]["electron_density"] == primary["artifact_id"]
    assert "not result.files.gbw" in handoff["warning"]
