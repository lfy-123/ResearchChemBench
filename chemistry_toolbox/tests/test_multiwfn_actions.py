from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from researchchem_toolbox.service import execute_action


SOURCE = Path(
    ".software_cache/multiwfn/2026.7.15/"
    "Multiwfn_2026.7.15_bin_Linux_noGUI/examples/H2.fch"
).resolve()


def _wavefunction(tmp_path: Path) -> Path:
    target = tmp_path / "H2.fch"
    shutil.copy2(SOURCE, target)
    return target


@pytest.mark.parametrize("population", ["mulliken", "lowdin"])
def test_multiwfn_atomic_charges(tmp_path, monkeypatch, population: str):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    wavefunction = _wavefunction(tmp_path)
    result = execute_action(
        "calculate_atomic_charges",
        {
            "backend_id": "multiwfn",
            "inputs": {"structure": str(wavefunction)},
            "method_spec": {"population_analysis": population},
            "action_settings": {},
            "resource_limits": { "cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "2026.7.15"
    assert result["result"]["analysis"] == population
    assert result["result"]["charges"] == pytest.approx([0.0, 0.0], abs=1.0e-7)
    assert result["provenance"]["arbitrary_menu_input_allowed"] is False
    assert len(result["provenance"]["required_citations"]) == 2


@pytest.mark.parametrize(
    ("definition", "expected"),
    [
        ("mayer", 1.00000001),
        ("wiberg_lowdin", 1.00000001),
        ("mulliken", 0.83866316),
    ],
)
def test_multiwfn_bond_order_definitions(
    tmp_path, monkeypatch, definition: str, expected: float
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    wavefunction = _wavefunction(tmp_path)
    result = execute_action(
        "calculate_bond_orders",
        {
            "backend_id": "multiwfn",
            "inputs": {"structure": str(wavefunction)},
            "method_spec": {"bond_order_definition": definition},
            "action_settings": {"minimum_bond_order": 0.05},
            "resource_limits": { "cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["analysis"] == definition
    bond = result["result"]["bonds"][0]
    assert (bond["atom_index_a"], bond["atom_index_b"]) == (0, 1)
    assert bond["bond_order"] == pytest.approx(expected)
