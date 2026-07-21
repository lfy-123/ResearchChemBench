from __future__ import annotations

import numpy as np
import pytest

from researchchem_toolbox.service import execute_action


SILICON = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [1.3575, 1.3575, 1.3575]},
    ],
    "cell_angstrom": [
        [0.0, 2.715, 2.715],
        [2.715, 0.0, 2.715],
        [2.715, 2.715, 0.0],
    ],
    "pbc": [True, True, True],
}


@pytest.mark.parametrize("backend_id", ["spglib", "pymatgen"])
def test_crystal_symmetry_backends_are_independent_choices(tmp_path, monkeypatch, backend_id: str):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "analyze_crystal_symmetry",
        {
            "backend_id": backend_id,
            "inputs": {"structure": SILICON},
            "method_spec": {},
            "action_settings": {
                "symmetry_tolerance_angstrom": 1e-3,
                "angle_tolerance_degrees": -1.0,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["space_group_number"] == 227


def test_pymatgen_supercell_and_surface_enumeration(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    supercell = execute_action(
        "build_supercell",
        {
            "backend_id": "pymatgen",
            "inputs": {"structure": SILICON},
            "method_spec": {},
            "action_settings": {"scaling_matrix": [2, 1, 1]},
        },
    )
    assert supercell["status"] == "success"
    assert supercell["result"]["atom_count"] == 4

    slabs = execute_action(
        "enumerate_surface_slabs",
        {
            "backend_id": "pymatgen",
            "inputs": {"structure": SILICON},
            "method_spec": {},
            "action_settings": {
                "miller_index": [1, 1, 1],
                "minimum_slab_thickness_angstrom": 6.0,
                "minimum_vacuum_thickness_angstrom": 8.0,
                "center_slab": True,
                "primitive": True,
                "max_terminations": 8,
            },
        },
    )
    assert slabs["status"] == "success"
    assert slabs["result"]["termination_count"] >= 1


def test_pymbar_free_energy_estimation(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    samples = np.linspace(-2.0, 2.0, 40)
    reduced = np.vstack((0.5 * (samples + 0.5) ** 2, 0.5 * (samples - 0.5) ** 2))
    result = execute_action(
        "estimate_free_energy_difference",
        {
            "backend_id": "pymbar",
            "inputs": {
                "reduced_potentials": reduced.tolist(),
                "samples_per_state": [20, 20],
            },
            "method_spec": {},
            "action_settings": {
                "uncertainty_method": "svd-ew",
                "maximum_iterations": 10000,
                "relative_tolerance": 1e-10,
                "temperature_kelvin": 298.15,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["state_count"] == 2
    assert result["result"]["delta_f"][0][0] == pytest.approx(0.0)
    assert len(result["result"]["delta_g_kj_mol"]) == 2


def test_pymbar_expectations_and_explicit_prefix_convergence(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    samples = np.linspace(-2.0, 2.0, 40)
    reduced = np.vstack((0.5 * (samples + 0.5) ** 2, 0.5 * (samples - 0.5) ** 2))
    common_inputs = {
        "reduced_potentials": reduced.tolist(),
        "samples_per_state": [20, 20],
    }
    expectation = execute_action(
        "estimate_thermodynamic_expectations",
        {
            "backend_id": "pymbar",
            "inputs": {**common_inputs, "observables": samples.tolist()},
            "method_spec": {},
            "action_settings": {
                "output": "averages",
                "observable_unit": "angstrom",
                "maximum_iterations": 10000,
                "relative_tolerance": 1e-10,
            },
        },
    )
    assert expectation["status"] == "success"
    assert len(expectation["result"]["expectation"]) == 2

    convergence = execute_action(
        "analyze_free_energy_convergence",
        {
            "backend_id": "pymbar",
            "inputs": common_inputs,
            "method_spec": {},
            "action_settings": {
                "fractions": [0.5, 1.0],
                "state_pair": [0, 1],
                "uncertainty_method": "svd-ew",
                "maximum_iterations": 10000,
                "relative_tolerance": 1e-10,
                "temperature_kelvin": 298.15,
            },
        },
    )
    assert convergence["status"] == "success"
    assert [item["sample_count"] for item in convergence["result"]["convergence"]] == [20, 40]
    assert all("delta_g_kj_mol" in item for item in convergence["result"]["convergence"])


def test_pymbar_histogram_free_energy_profile_uses_explicit_bins(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    coordinate = np.linspace(-2.0, 2.0, 40)
    reduced = np.vstack(
        (0.5 * (coordinate + 0.5) ** 2, 0.5 * (coordinate - 0.5) ** 2)
    )
    result = execute_action(
        "calculate_potential_of_mean_force",
        {
            "backend_id": "pymbar",
            "inputs": {
                "reduced_potentials": reduced.tolist(),
                "samples_per_state": [20, 20],
                "target_reduced_potential": reduced[0].tolist(),
                "collective_variable": coordinate.tolist(),
            },
            "method_spec": {},
            "action_settings": {
                "bin_edges": np.linspace(-2.1, 2.1, 8).tolist(),
                "reference": "lowest",
                "uncertainty_method": "analytical",
                "maximum_iterations": 10000,
                "relative_tolerance": 1e-10,
                "coordinate_unit": "angstrom",
                "temperature_kelvin": 298.15,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["occupied_bin_count"] == 7
    assert sum(item["sample_count"] for item in result["result"]["bins"]) == 40
    assert min(item["free_energy_reduced"] for item in result["result"]["bins"]) == pytest.approx(0.0)
    assert all("uncertainty_kj_mol" in item for item in result["result"]["bins"])
