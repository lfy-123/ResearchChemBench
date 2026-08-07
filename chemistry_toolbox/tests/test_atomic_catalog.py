from __future__ import annotations

from chemistry_toolbox.src.catalog import (
    action_specs,
    agent_toolbox_overview,
    backend_specs,
    catalog_snapshot,
    progressive_toolbox_overview,
    validate_catalog,
)


def test_catalog_has_planned_atomic_counts_and_no_runners():
    validate_catalog()
    actions = action_specs()
    assert sum(not specification.data_action for specification in actions.values()) >= 40
    assert sum(specification.data_action for specification in actions.values()) >= 5
    assert all(not action_id.startswith("run_") for action_id in actions)
    assert all("driver" not in specification.required_inputs for specification in actions.values())
    assert all(specification.primary_output for specification in actions.values())


def test_every_backend_choice_is_bidirectional_and_never_auto():
    actions = action_specs()
    backends = backend_specs()
    assert "auto" not in backends
    for action in actions.values():
        assert "auto" not in action.backend_ids
        for backend_id in action.backend_ids:
            assert action.id in backends[backend_id].capabilities
    for backend in backends.values():
        for action_id in backend.capabilities:
            assert backend.id in actions[action_id].backend_ids


def test_catalog_snapshot_declares_benchmark_autonomy_policy():
    first = catalog_snapshot(include_health=False)
    second = catalog_snapshot(include_health=False)
    assert first["catalog_hash"] == second["catalog_hash"]
    assert first["discovery_mode"] == "progressive"
    assert first["exposure_policy"] == "progressive_discovery"
    assert first["catalog_visibility_policy"] == "complete_task_independent"
    assert first["task_specific_tool_filtering"] is False
    assert first["backend_selection_policy"] == "per_action_explicit"
    assert set(first["provider_selection_policies"]) == {
        "agent_backend_required",
        "fixed_source",
        "internal_deterministic",
    }
    assert first["scientific_resource_selection_policy"] == "agent_explicit_no_default"
    assert first["automatic_fallback"] is False
    assert len(first["actions"]) == len(action_specs())
    assert len(first["actions"]) >= 55
    assert first["resources"]
    full = catalog_snapshot(include_health=False, discovery_mode="full")
    assert full["discovery_mode"] == "full"
    assert full["exposure_policy"] == "atomic_all"
    assert len(full["actions"]) == len(first["actions"])


def test_agent_overview_is_complete_and_contains_no_recipe():
    overview = agent_toolbox_overview(include_health=False)
    assert all(f"`{action_id}`" in overview for action_id in action_specs())
    assert "There is no hidden workflow" in overview
    assert "dispatcher never chooses them" in overview
    assert "deterministic internal Actions do not require a fake backend choice" in overview
    assert "standardize_structure →" not in overview


def test_progressive_overview_is_compact_but_indexes_every_domain():
    overview = progressive_toolbox_overview()
    assert "search_actions" in overview
    assert "execute_action" in overview
    assert all(f"`{category}`" in overview for category in {
        specification.category for specification in action_specs().values()
    })
    assert "`calculate_energy`" not in overview
    assert "task-specific retrieval" in overview
