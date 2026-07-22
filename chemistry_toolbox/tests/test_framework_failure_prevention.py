from __future__ import annotations

import math
from pathlib import Path

import pytest

from researchchem_toolbox import service
from researchchem_toolbox.artifacts import ArtifactStore
from researchchem_toolbox.backends.common import structure_dict
from researchchem_toolbox.backends.electronic import _resolve_mace_model
from researchchem_toolbox.catalog import action_specs, mcp_action_description


H2 = {
    "atoms": [
        {"element": "H", "position_angstrom": [-0.37, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.37, 0.0, 0.0]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


def test_xyz_comment_charge_and_multiplicity_are_preserved(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    data = tmp_path / "data"
    data.mkdir()
    path = data / "charged.xyz"
    path.write_text(
        "2\nseed_id=test charge=2 multiplicity=3\nH 0 0 0\nH 0 0 0.8\n",
        encoding="utf-8",
    )

    parsed = structure_dict("data/charged.xyz")

    assert parsed["charge"] == 2
    assert parsed["multiplicity"] == 3


def _available(specifications):
    return {
        item.id: {"available": True, "status": "available", "runtime": item.runtime}
        for item in specifications
    }


def test_compact_artifact_refs_are_verified_and_expanded_before_dispatch(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    store = ArtifactStore()
    structure_ref = store.put_json(
        H2,
        semantic_type="AtomicStructure",
        producer_action="test_structure",
        producer_backend="test",
    )
    assert store.load({"artifact_id": structure_ref.artifact_id}) == H2

    calls = []
    monkeypatch.setattr(service, "probe_all_backends", _available)
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **kwargs: calls.append(kwargs)
        or {"status": "success", "result": {"energy": -1.0, "unit": "hartree"}},
    )
    result = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "xtb",
            "inputs": {"structure": {"artifact_id": structure_ref.artifact_id}},
            "method_spec": {"method": "gfn2"},
            "action_settings": {},
        },
    )

    assert result["status"] == "success"
    dispatched = calls[0]["payload"]["request"]["inputs"]["structure"]
    assert dispatched == structure_ref.model_dump(mode="json")
    assert [item["artifact_id"] for item in result["input_artifacts"]] == [
        structure_ref.artifact_id
    ]


def test_unknown_compact_artifact_is_rejected_without_starting_backend(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda _values: (_ for _ in ()).throw(AssertionError("health probe must not run")),
    )
    result = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "xtb",
            "inputs": {"structure": {"artifact_id": "art_00000000000000000000000000000000"}},
            "method_spec": {"method": "gfn2"},
            "action_settings": {},
        },
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "invalid_artifact_reference"


def test_backend_specific_inputs_and_enums_fail_before_health_or_worker(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda _values: (_ for _ in ()).throw(AssertionError("health probe must not run")),
    )

    goodvibes = service.execute_action(
        "derive_thermochemistry",
        {
            "backend_id": "goodvibes",
            "inputs": {"energy": {}, "frequencies": {}},
            "method_spec": {},
            "action_settings": {"temperature_kelvin": 298.15},
        },
    )
    assert goodvibes["status"] == "invalid_request"
    assert "output_file" in goodvibes["error"]["message"]

    mace = service.execute_action(
        "optimize_geometry",
        {
            "backend_id": "mace",
            "inputs": {"structure": H2},
            "method_spec": {
                "model": "medium-mpa-0",
                "device": "cpu",
                "allow_model_download": False,
            },
            "action_settings": {
                "fmax_ev_per_angstrom": 0.05,
                "optimizer": "ase",
                "max_steps": 20,
            },
        },
    )
    assert mace["status"] == "invalid_request"
    assert "['bfgs', 'lbfgs', 'fire']" in mace["error"]["message"]
    assert mace["provenance"]["automatic_fallback_count"] == 0


def test_action_description_exposes_backend_specific_thermochemistry_contracts():
    description = mcp_action_description(action_specs()["derive_thermochemistry"])
    assert "goodvibes [inputs=output_file" in description
    assert "internal_thermochemistry [inputs=energy,frequencies" in description
    assert "action_settings.geometry=[monatomic|linear|nonlinear]" in description
    assert "ignore_imaginary_modes" in description


def test_mace_installed_alias_resolution_is_exact_and_never_guesses(monkeypatch):
    project_root = Path(__file__).resolve().parents[2]
    monkeypatch.setenv("RESEARCHCHEMBENCH_MODEL_CACHE", str(project_root / ".model_cache"))
    selected = _resolve_mace_model("medium-mpa-0", allow_download=False)
    assert selected == str(project_root / ".model_cache/mace/macempa0mediummodel")
    legacy_alias = _resolve_mace_model("MACE-MP-0-medium", allow_download=False)
    assert legacy_alias == str(
        project_root / ".model_cache/mace/20231203mace128L1_epoch199model"
    )
    assert _resolve_mace_model(legacy_alias, allow_download=False) == legacy_alias
    with pytest.raises(ValueError, match="Unknown MACE model label"):
        _resolve_mace_model("MACE-MP-medium-unknown", allow_download=True)


def test_hessian_artifact_chains_directly_into_finite_linear_thermochemistry(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    store = ArtifactStore()
    hessian = [[0.0 for _ in range(6)] for _ in range(6)]
    for index in range(6):
        hessian[index][index] = 0.5 + index * 0.01
    hessian_ref = store.put_json(
        {"matrix": hessian, "unit": "eV/angstrom^2"},
        semantic_type="Hessian",
        producer_action="test_hessian",
        producer_backend="test",
    )
    energy_ref = store.put_json(
        {"energy": -1.0, "unit": "eV"},
        semantic_type="EnergyResult",
        producer_action="test_energy",
        producer_backend="test",
    )

    vibrations = service.execute_action(
        "derive_vibrational_modes",
        {
            "inputs": {
                "hessian": {"artifact_id": hessian_ref.artifact_id},
                "structure": H2,
            },
            "method_spec": {},
            "action_settings": {"linearity": "linear"},
        },
    )
    assert vibrations["status"] == "success"
    assert vibrations["result"]["structure"]["atoms"][0]["element"] == "H"

    thermochemistry = service.execute_action(
        "derive_thermochemistry",
        {
            "backend_id": "internal_thermochemistry",
            "inputs": {
                "energy": energy_ref.artifact_id,
                "frequencies": {
                    "artifact_id": vibrations["output_artifacts"][0]["artifact_id"]
                },
            },
            "method_spec": {},
            "action_settings": {
                "temperature_kelvin": 298.15,
                "pressure_pa": 101325.0,
                "geometry": "linear",
                "symmetry_number": 2,
                "spin": 0.0,
                "ignore_imaginary_modes": False,
            },
        },
    )
    assert thermochemistry["status"] == "success"
    assert all(
        math.isfinite(thermochemistry["result"][name])
        for name in ("enthalpy_ev", "entropy_ev_per_kelvin", "gibbs_free_energy_ev")
    )


def test_scalar_frequency_entries_are_valid_thermochemistry_inputs(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = service.execute_action(
        "derive_thermochemistry",
        {
            "backend_id": "internal_thermochemistry",
            "inputs": {
                "energy": {"energy": -1.0, "unit": "eV"},
                "frequencies": {
                    "frequencies_cm1": [0, 0, 0, 0, 0, 4401],
                    "structure": H2,
                },
            },
            "method_spec": {},
            "action_settings": {
                "temperature_kelvin": 298.15,
                "pressure_pa": 101325.0,
                "geometry": "linear",
                "symmetry_number": 2,
                "spin": 0.0,
                "ignore_imaginary_modes": False,
            },
        },
    )
    assert result["status"] == "success"
    assert math.isfinite(result["result"]["gibbs_free_energy_ev"])
