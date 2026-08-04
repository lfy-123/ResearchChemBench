from __future__ import annotations

from minichem_toolbox.catalog import action_specs, backend_specs, catalog_snapshot, validate_catalog
from minichem_toolbox.mini_profile import MINI_ACTION_IDS, MINI_BACKEND_IDS


def test_focused_catalog_is_consistent() -> None:
    validate_catalog()
    actions = action_specs()
    backends = backend_specs()
    assert set(actions).issubset(MINI_ACTION_IDS)
    assert set(backends).issubset(MINI_BACKEND_IDS)
    assert len(actions) == 37
    assert len(backends) == 18
    assert "calculate_periodic_energy" not in actions
    assert "propagate_dynamics" not in actions
    assert "dock_ligand" not in actions


def test_case1_core_capabilities_are_exposed() -> None:
    actions = action_specs()
    for action_id in (
        "generate_conformer_ensemble",
        "calculate_energy",
        "optimize_geometry",
        "calculate_hessian",
        "locate_transition_state",
        "trace_intrinsic_reaction_coordinate",
        "derive_thermochemistry",
        "analyze_thermochemical_selectivity",
        "parse_quantum_chemistry_output",
    ):
        assert action_id in actions


def test_catalog_declares_three_peer_layers() -> None:
    snapshot = catalog_snapshot(include_health=False)
    assert [item["id"] for item in snapshot["execution_layers"]] == [
        "predefined_actions",
        "native_software",
        "programmable_analysis",
    ]
    assert snapshot["catalog_visibility_policy"] == "focused_task_independent"
    assert snapshot["resources"] == []
