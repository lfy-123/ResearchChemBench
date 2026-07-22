from __future__ import annotations

import math
from pathlib import Path

import pytest

from researchchem_toolbox import service
from researchchem_toolbox.artifacts import ArtifactStore
from researchchem_toolbox.backends.common import atoms_and_coordinates, structure_dict
from researchchem_toolbox.backends.electronic import _resolve_mace_model
from researchchem_toolbox.backends.reaction import (
    _pysisyphus_failure_detail,
    _pysisyphus_xtb_gfn,
)
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


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("gfn2", 2),
        ("GFN2-xTB", 2),
        ("xTB_GFN2", 2),
        ("GFN-FF", "ff"),
    ],
)
def test_pysisyphus_accepts_conventional_xtb_method_labels(label, expected):
    assert _pysisyphus_xtb_gfn(label) == expected


def test_atomic_structure_missing_coordinates_has_a_typed_error():
    with pytest.raises(ValueError, match="position_angstrom.*xyz"):
        atoms_and_coordinates(
            {"atoms": [{"symbol": "H", "xyz": [0.0, 0.0, 0.0]}]}
        )


def test_pysisyphus_reports_xtb_scc_nonconvergence(tmp_path: Path):
    marker = tmp_path / "crashed_calculator_000" / ".sccnotconverged"
    marker.parent.mkdir()
    marker.touch()

    detail = _pysisyphus_failure_detail(tmp_path, "opaque native traceback")

    assert "did not converge its SCC" in detail
    assert "crashed_calculator_000/.sccnotconverged" in detail
    assert "automatic backend-selection" in detail


def test_pysisyphus_reports_overlapping_atoms_from_native_xtb_output(tmp_path: Path):
    output = tmp_path / "crashed_calculator_000" / "xtb.out"
    output.parent.mkdir()
    output.write_text(
        "Some atoms in the start geometry are *very* close.\n"
        "XTB REFUSES TO CONTINUE\n"
        "Found *very* short distance of 0.000E+00 for C52-O53\n"
        "[ERROR] Program stopped due to fatal error\n",
        encoding="utf-8",
    )

    detail = _pysisyphus_failure_detail(tmp_path, "opaque native traceback")

    assert "atoms in the start geometry" in detail
    assert "REFUSES TO CONTINUE" in detail
    assert "0.000E+00 for C52-O53" in detail


def test_inline_atomic_structure_is_rejected_before_worker(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(service, "probe_all_backends", _available)
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **_kwargs: (_ for _ in ()).throw(
            AssertionError("malformed inline structure must not reach the worker")
        ),
    )

    result = service.execute_action(
        "optimize_geometry",
        {
            "backend_id": "xtb",
            "inputs": {
                "structure": {
                    "atoms": [{"symbol": "H", "xyz": [0.0, 0.0, 0.0]}],
                    "charge": 0,
                    "multiplicity": 1,
                }
            },
            "method_spec": {"method": "gfn2"},
            "action_settings": {"optimization_level": "normal"},
        },
    )

    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "invalid_atomic_structure"
    assert "position_angstrom" in result["error"]["message"]


def test_orca_parallel_request_is_rejected_before_health_or_worker(
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
            "backend_id": "orca",
            "inputs": {"structure": H2},
            "method_spec": {"method": "HF", "basis": "STO-3G"},
            "action_settings": {},
            "resource_limits": {"cpu_cores": 4, "walltime_seconds": 300},
        },
    )

    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "invalid_resource_limits"
    assert "validated maximum 1" in result["error"]["message"]
    assert "no resource substitution or fallback" in result["error"]["message"]


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


def test_vibration_inputs_reject_a_structure_artifact_in_the_hessian_slot(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    structure_ref = ArtifactStore().put_json(
        H2,
        semantic_type="AtomicStructure",
        producer_action="optimize_geometry",
        producer_backend="xtb",
    )
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda _values: (_ for _ in ()).throw(AssertionError("health probe must not run")),
    )
    result = service.execute_action(
        "derive_vibrational_modes",
        {
            "inputs": {
                "hessian": {"artifact_id": structure_ref.artifact_id},
                "structure": {"artifact_id": structure_ref.artifact_id},
            },
            "action_settings": {"linearity": "nonlinear"},
        },
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "artifact_semantic_mismatch"
    assert "two differently typed values" in result["error"]["message"]


def test_sella_nested_calculator_settings_fail_before_worker(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda _values: (_ for _ in ()).throw(AssertionError("health probe must not run")),
    )
    result = service.execute_action(
        "locate_transition_state",
        {
            "backend_id": "sella",
            "component_backends": {"calculator": "xtb"},
            "inputs": {"initial_guess": H2},
            "method_spec": {"calculator_method": {"method": "gfn2"}},
            "action_settings": {
                "calculator_action_settings": {"calculate_energy": {}},
                "force_threshold_ev_per_angstrom": 0.1,
                "max_steps": 5,
                "internal_coordinates": False,
                "initial_trust_radius": 0.1,
                "minimum_model_quality": 1e-4,
                "finite_difference_step": 0.05,
                "three_point_differences": False,
                "steps_per_diagonalization": 3,
                "diagonalization_interval": 1,
                "allow_fragments": True,
                "refine_initial_hessian_iterations": 0,
            },
        },
    )
    assert result["status"] == "invalid_request"
    assert "calculate_forces" in result["error"]["message"]


def test_pysisyphus_rejects_invalid_native_enums_before_worker(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda _values: (_ for _ in ()).throw(AssertionError("health probe must not run")),
    )
    result = service.execute_action(
        "locate_transition_state",
        {
            "backend_id": "pysisyphus",
            "inputs": {"initial_guess": H2},
            "method_spec": {
                "calculator_backend": "xtb",
                "method": "GFN2-xTB",
            },
            "action_settings": {
                "optimizer": "dimer",
                "convergence": "normal",
                "max_cycles": 10,
                "hessian_init": "lindh",
            },
        },
    )
    assert result["status"] == "invalid_request"
    assert "optimizer='dimer'" in result["error"]["message"]
    assert "rsirfo" in result["error"]["message"]


def test_backend_failure_persists_a_diagnostic_artifact(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(service, "probe_all_backends", _available)
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **_kwargs: {
            "status": "failed",
            "error": {
                "code": "backend_exception",
                "message": "synthetic calculator failure",
                "traceback": "full diagnostic traceback",
            },
        },
    )
    result = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "xtb",
            "inputs": {"structure": H2},
            "method_spec": {"method": "gfn2"},
            "action_settings": {},
        },
    )
    assert result["status"] == "failed"
    assert len(result["output_artifacts"]) == 1
    diagnostic = result["output_artifacts"][0]
    assert diagnostic["semantic_type"] == "BackendDiagnostic"
    payload = ArtifactStore().load({"artifact_id": diagnostic["artifact_id"]})
    assert payload["error"]["traceback"] == "full diagnostic traceback"


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


def test_thermochemistry_rejects_hessian_in_frequency_slot_before_worker(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    store = ArtifactStore()
    hessian_ref = store.put_json(
        {"matrix": [[1.0]], "unit": "eV/angstrom^2"},
        semantic_type="Hessian",
        producer_action="calculate_hessian",
        producer_backend="test",
    )
    energy_ref = store.put_json(
        {"energy": -1.0, "unit": "eV"},
        semantic_type="EnergyResult",
        producer_action="calculate_energy",
        producer_backend="test",
    )
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda _values: (_ for _ in ()).throw(AssertionError("health probe must not run")),
    )

    result = service.execute_action(
        "derive_thermochemistry",
        {
            "backend_id": "internal_thermochemistry",
            "inputs": {
                "energy": energy_ref.artifact_id,
                "frequencies": hessian_ref.artifact_id,
            },
            "method_spec": {},
            "action_settings": {
                "temperature_kelvin": 353.15,
                "pressure_pa": 101325.0,
                "geometry": "nonlinear",
                "symmetry_number": 1,
                "spin": 0.0,
                "ignore_imaginary_modes": False,
            },
        },
    )

    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "artifact_semantic_mismatch"
    assert "requires FrequencyResult" in result["error"]["message"]
    assert "derive_vibrational_modes explicitly" in result["error"]["message"]


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
