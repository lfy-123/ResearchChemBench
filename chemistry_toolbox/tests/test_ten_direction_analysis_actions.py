from __future__ import annotations

import pytest

from chemistry_toolbox.src.service import execute_action


@pytest.fixture(autouse=True)
def _isolated_workspace(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))


def test_adsorption_energy_uses_explicit_stoichiometric_references(tmp_path, monkeypatch):
    result = execute_action(
        "calculate_adsorption_energy",
        {
            "backend_id": "internal_periodic_analysis",
            "inputs": {
                "adsorbed_system_energy": -121.0,
                "clean_surface_energy": -100.0,
                "reference_species": [
                    {"label": "H2", "energy": -10.0, "stoichiometric_coefficient": 2.0}
                ],
            },
            "method_spec": {},
            "action_settings": {"energy_unit": "ev", "adsorbate_count": 1.0},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["adsorption_energy_ev"] == pytest.approx(-1.0)
    assert "sign_convention" in result["result"]


def test_pressure_enthalpy_diagram_interpolates_phase_crossing():
    result = execute_action(
        "construct_pressure_enthalpy_phase_diagram",
        {
            "backend_id": "internal_periodic_analysis",
            "inputs": {
                "phase_records": [
                    {"phase_id": "alpha", "pressure_gpa": 0.0, "enthalpy": 0.0},
                    {"phase_id": "alpha", "pressure_gpa": 10.0, "enthalpy": 1.0},
                    {"phase_id": "beta", "pressure_gpa": 0.0, "enthalpy": 1.0},
                    {"phase_id": "beta", "pressure_gpa": 10.0, "enthalpy": 0.0},
                ]
            },
            "method_spec": {},
            "action_settings": {
                "enthalpy_unit": "ev_per_formula_unit",
                "energy_tolerance_ev_per_formula_unit": 1e-8,
                "maximum_reported_transitions": 10,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["transitions"][0]["interpolated_transition_pressure_gpa"] == pytest.approx(5.0)
    assert [item["stable_phases"][0] for item in result["result"]["stable_phase_records"]] == ["alpha", "beta"]


def test_phonon_stability_separates_acoustic_tolerance_from_instability():
    stable = execute_action(
        "assess_phonon_stability",
        {
            "backend_id": "internal_periodic_analysis",
            "inputs": {
                "phonon_records": [
                    {"q_point": [0.0, 0.0, 0.0], "frequencies": [-0.01, 0.0, 0.01, 4.0]},
                    {"q_point": [0.5, 0.0, 0.0], "frequencies": [1.0, 2.0, 3.0, 5.0]},
                ]
            },
            "method_spec": {},
            "action_settings": {
                "frequency_unit": "thz",
                "imaginary_tolerance": 0.05,
                "gamma_q_tolerance": 1e-8,
                "acoustic_gamma_tolerance": 0.05,
                "maximum_returned_imaginary_modes": 20,
            },
        },
    )
    assert stable["result"]["dynamically_stable"] is True
    assert stable["result"]["gamma_acoustic_modes_within_tolerance"] is True

    unstable_request = {
        "inputs": {
            "phonon_records": [
                {"q_point": [0.0, 0.0, 0.0], "frequencies": [0.0, 0.0, 0.0, 4.0]},
                {"q_point": [0.5, 0.0, 0.0], "frequencies": [-0.5, 2.0, 3.0, 5.0]},
            ]
        },
        "method_spec": {},
        "action_settings": {
            "frequency_unit": "thz",
            "imaginary_tolerance": 0.05,
            "gamma_q_tolerance": 1e-8,
            "acoustic_gamma_tolerance": 0.05,
            "maximum_returned_imaginary_modes": 20,
        },
    }
    unstable = execute_action(
        "assess_phonon_stability",
        {"backend_id": "internal_periodic_analysis", **unstable_request},
    )
    assert unstable["result"]["dynamically_stable"] is False
    assert unstable["result"]["imaginary_mode_count"] == 1


def test_post_transition_state_branching_reports_failures_and_recrossing():
    result = execute_action(
        "analyze_post_transition_state_trajectory_ensemble",
        {
            "backend_id": "internal_reaction_analysis",
            "inputs": {
                "trajectory_outcomes": [
                    {"trajectory_id": "t1", "status": "success", "product_label": "A", "recrossed": False},
                    {"trajectory_id": "t2", "status": "success", "product_label": "A", "recrossed": True},
                    {"trajectory_id": "t3", "status": "success", "product_label": "B", "recrossed": False},
                    {"trajectory_id": "t4", "status": "success", "product_label": None, "recrossed": False},
                    {"trajectory_id": "t5", "status": "failed"},
                ]
            },
            "method_spec": {},
            "action_settings": {
                "confidence_level": 0.95,
                "failure_policy": "exclude",
                "minimum_successful_trajectories": 4,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["branching"][0]["product_label"] == "A"
    assert result["result"]["branching"][0]["fraction"] == pytest.approx(0.5)
    assert result["result"]["recrossing_fraction_of_successful"] == pytest.approx(0.25)
    assert result["result"]["failed_trajectory_ids"] == ["t5"]


def test_nonadiabatic_ensemble_populations_hops_and_partial_failure():
    result = execute_action(
        "analyze_nonadiabatic_trajectory_ensemble",
        {
            "backend_id": "internal_trajectory_analysis",
            "inputs": {
                "trajectories": [
                    {"trajectory_id": "t1", "status": "success", "times_fs": [0, 5, 10], "state_indices": [1, 1, 0]},
                    {"trajectory_id": "t2", "status": "success", "times_fs": [0, 5, 10], "state_indices": [1, 0, 0]},
                    {"trajectory_id": "t3", "status": "failed", "times_fs": [0, 5], "state_indices": [1, 2]},
                ]
            },
            "method_spec": {},
            "action_settings": {
                "state_count": 3,
                "initial_state_index": 1,
                "time_grid_fs": [0.0, 5.0, 10.0],
                "confidence_level": 0.95,
                "failure_policy": "include_until_failure",
            },
        },
    )
    assert result["status"] == "success"
    assert [item["available_trajectory_count"] for item in result["result"]["population_records"]] == [3, 3, 2]
    assert result["result"]["population_records"][1]["states"][1]["population"] == pytest.approx(1 / 3)
    assert result["result"]["total_hop_count"] == 3
    assert result["result"]["first_departure_time_fs"]["median"] == pytest.approx(5.0)
