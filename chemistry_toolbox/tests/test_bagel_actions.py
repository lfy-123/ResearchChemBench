from __future__ import annotations

from pathlib import Path

import pytest

from chemistry_toolbox.src.backends import electronic
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".software_cache" / "installations" / "bagel" / "1.2.2"
BASIS = CACHE / "runtime" / "usr" / "share" / "bagel"
BOHR_TO_ANGSTROM = 0.529177210903


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


pytestmark = pytest.mark.skipif(
    not (CACHE / "bin" / "BAGEL").is_file(),
    reason="BAGEL 1.2.2 cached runtime is required",
)


def _configure(monkeypatch) -> None:
    monkeypatch.setenv("CHEMGRAPH_BAGEL_COMMAND", str(CACHE / "bin" / "BAGEL"))
    monkeypatch.setenv(
        "CHEMGRAPH_BAGEL_MPIRUN_COMMAND", str(CACHE / "bin" / "bagel-mpirun")
    )
    monkeypatch.setenv(
        "CHEMGRAPH_BAGEL_RAW_COMMAND", str(CACHE / "runtime" / "usr" / "bin" / "BAGEL")
    )
    monkeypatch.setenv("CHEMGRAPH_BAGEL_BASIS_DIRECTORY", str(BASIS))


def _common_method(**updates) -> dict:
    method = {
        "multireference_method": "casscf",
        "basis": "svp",
        "density_fitting_basis": "svp-jkfit",
        "charge": 0,
        "multiplicity": 1,
        "active_orbitals": 4,
        "closed_orbitals": 0,
        "state_count": 1,
        "casscf_convergence": 1e-8,
        "fci_convergence": 1e-10,
        "casscf_max_iterations": 50,
    }
    method.update(updates)
    return method


def test_bagel_calculates_state_averaged_casscf_energies(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    distance = 6.0 * BOHR_TO_ANGSTROM
    structure = {
        "atoms": [
            {"element": "Li", "position_angstrom": [0.0, 0.0, distance]},
            {"element": "F", "position_angstrom": [0.0, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 1,
    }
    result = _execute(
        "calculate_multireference_state_energies",
        "bagel",
        {
            "inputs": {"structure": structure},
            "method_spec": _common_method(
                active_orbitals=4, closed_orbitals=3, state_count=4
            ),
            "action_settings": {
                "maximum_returned_states": 2,
                "mpi_ranks": 1,
                "threads_per_rank": 1,
            },
            "resource_limits": {"cpu_cores": 1, "memory_mb": 2048, "walltime_seconds": 120},
        },
    )

    assert result["status"] == "success"
    assert result["result"]["active_electrons"] == 6
    assert len(result["result"]["state_energies"]) == 2
    assert result["result"]["state_energies"][0]["energy_hartree"] < 0


def test_bagel_calculates_xms_caspt2_analytical_gradient(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    distance = 6.0 * BOHR_TO_ANGSTROM
    structure = {
        "atoms": [
            {"element": "Li", "position_angstrom": [0.0, 0.0, distance]},
            {"element": "Li", "position_angstrom": [0.0, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 1,
    }
    method = _common_method(multireference_method="xms-caspt2")
    method["caspt2_options"] = {
        "imaginary_shift_hartree": 0.0,
        "freeze_core": False,
        "sssr": True,
    }
    result = _execute(
        "calculate_multireference_nuclear_gradient",
        "bagel",
        {
            "inputs": {"structure": structure},
            "method_spec": method,
            "action_settings": {
                "state_index": 0,
                "max_zvector_iterations": 100,
                "mpi_ranks": 1,
                "threads_per_rank": 1,
            },
            "resource_limits": {"cpu_cores": 1, "memory_mb": 4096, "walltime_seconds": 120},
        },
    )

    assert result["status"] == "success"
    gradient = result["result"]["gradient_hartree_per_bohr"]
    assert len(gradient) == 2
    assert gradient[0][2] == pytest.approx(-gradient[1][2], abs=1e-8)
    assert result["result"]["energy_hartree"] == pytest.approx(-14.8779135422, abs=1e-8)


def test_bagel_calculates_explicit_casscf_nonadiabatic_coupling(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    distance = 6.0 * BOHR_TO_ANGSTROM
    structure = {
        "atoms": [
            {"element": "Li", "position_angstrom": [0.0, 0.0, distance]},
            {"element": "F", "position_angstrom": [0.0, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 1,
    }
    result = _execute(
        "calculate_nonadiabatic_coupling_vector",
        "bagel",
        {
            "inputs": {"structure": structure},
            "method_spec": _common_method(
                active_orbitals=4, closed_orbitals=3, state_count=4
            ),
            "action_settings": {
                "state_index_1": 3,
                "state_index_2": 0,
                "coupling_type": "full",
                "max_zvector_iterations": 100,
                "mpi_ranks": 1,
                "threads_per_rank": 1,
            },
            "resource_limits": {"cpu_cores": 1, "memory_mb": 4096, "walltime_seconds": 120},
        },
    )

    assert result["status"] == "success"
    assert result["result"]["energy_gap_ev"] == pytest.approx(2.2770111863, abs=1e-8)
    assert len(result["result"]["coupling_vector_atomic_units"]) == 2


def test_bagel_rejects_inconsistent_active_space_before_execution(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure(monkeypatch)
    structure = {
        "atoms": [{"element": "He", "position_angstrom": [0.0, 0.0, 0.0]}],
        "charge": 0,
        "multiplicity": 1,
    }
    with pytest.raises(ValueError, match="active electrons"):
        electronic.execute(
            "calculate_multireference_state_energies",
            "bagel",
            {
                "inputs": {"structure": structure},
                "method_spec": _common_method(active_orbitals=1, closed_orbitals=2),
                "action_settings": {
                    "maximum_returned_states": 1,
                    "mpi_ranks": 1,
                    "threads_per_rank": 1,
                },
                "resource_limits": {"cpu_cores": 1},
            },
        )
