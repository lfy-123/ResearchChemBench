from __future__ import annotations

import json

from chemistry_toolbox.mcp.discovery_models import ProgressiveActionRequest
from chemistry_toolbox.mcp.discovery_tools import execute_action
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
    assert action["automatic_fallback"] is False

    backend = inspect_backend("goodvibes", snapshot=snapshot)
    assert "analyze_thermochemical_selectivity" in {
        item["action_id"] for item in backend["capabilities"]
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
