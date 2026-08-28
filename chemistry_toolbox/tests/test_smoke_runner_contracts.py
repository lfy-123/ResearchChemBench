from __future__ import annotations

import ast
from pathlib import Path

import pytest

from chemistry_toolbox.scripts import (
    run_data_source_smokes,
    run_scientific_resource_smokes,
)
from chemistry_toolbox.scripts.run_full_action_scientific_validation import (
    _artifact_criterion,
    _attempt_passed,
    _scientific_criteria,
)
from chemistry_toolbox.scripts.run_native_interface_smokes import PROBES, classify_probe
from chemistry_toolbox.src.service import _validate_inline_atomic_structures

TOOLBOX_ROOT = Path(__file__).resolve().parents[1]


def _literal_dict_keys(script_name: str) -> set[str]:
    source = TOOLBOX_ROOT.joinpath("scripts", script_name).read_text(encoding="utf-8")
    tree = ast.parse(source)
    return {
        key.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Dict)
        for key in node.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }


def test_action_backend_matrix_does_not_set_evaluator_walltime() -> None:
    keys = _literal_dict_keys("run_action_backend_matrix_smokes.py")
    assert keys.isdisjoint({"walltime_seconds", "timeout_seconds"})


def test_action_gap_runner_does_not_set_evaluator_walltime() -> None:
    keys = _literal_dict_keys("run_action_gap_smokes.py")
    assert keys.isdisjoint({"walltime_seconds", "timeout_seconds"})


@pytest.mark.parametrize(
    "script_name",
    ["run_backend_gap_smokes.py", "run_goodvibes_action_smokes.py"],
)
def test_other_action_smoke_runners_do_not_set_evaluator_walltime(
    script_name: str,
) -> None:
    keys = _literal_dict_keys(script_name)
    assert keys.isdisjoint({"walltime_seconds", "timeout_seconds"})


def test_action_gap_plumed_distance_uses_a_real_non_structure_atoms_argument() -> None:
    source = TOOLBOX_ROOT.joinpath("scripts", "run_action_gap_smokes.py").read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    definitions = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant) and key.value == "collective_variables":
                definitions.append(ast.literal_eval(value))
    assert definitions == [
        [{"label": "distance", "type": "DISTANCE", "ATOMS": [1, 2]}]
    ]
    assert (
        _validate_inline_atomic_structures(
            "evaluate_collective_variables",
            "plumed",
            {
                "trajectory": "trajectory.xyz",
                "topology": "topology.pdb",
                "collective_variables": definitions[0],
            },
        )
        is None
    )


def test_backend_gap_goodvibes_request_declares_complete_scientific_settings() -> None:
    source = TOOLBOX_ROOT.joinpath("scripts", "run_backend_gap_smokes.py").read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    requests = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or len(node.args) < 4:
            continue
        case_id = node.args[0]
        if not isinstance(case_id, ast.Constant) or case_id.value != "goodvibes_gaussian_water":
            continue
        request = node.args[3]
        assert isinstance(request, ast.Dict)
        for key, value in zip(request.keys, request.values):
            if isinstance(key, ast.Constant) and key.value == "action_settings":
                requests.append(ast.literal_eval(value))

    assert requests == [
        {
            "temperature_kelvin": 298.15,
            "standard_state": "gas_1atm",
            "entropy_model": "grimme",
            "enthalpy_model": "head_gordon",
            "frequency_scale_factor": 1.0,
            "zpe_scale_factor": 1.0,
            "symmetry_correction": False,
            "imaginary_frequency_policy": "retain",
            "entropy_frequency_cutoff_cm1": 100.0,
            "enthalpy_frequency_cutoff_cm1": 100.0,
            "free_rotor_inertia_model": "global",
        }
    ]


def test_native_probe_marks_runtime_linker_and_gamess_config_errors_failed() -> None:
    failed_process = {"process_status": "failed"}
    for output in (
        "libstdc++.so.6: version `GLIBCXX_3.4.32' not found",
        "libstdc++.so.6: version `CXXABI_1.3.15' not found",
        "Please run 'config' first, to set up GAMESS compiling information",
    ):
        status, _reason = classify_probe(failed_process, output, cancelled=False)
        assert status == "failed"


def test_native_probe_preserves_expected_missing_input_classification() -> None:
    status, _reason = classify_probe(
        {"process_status": "failed"},
        "ERROR: No input file 'dftb_in.hsd' found.",
        cancelled=False,
    )
    assert status == "started_input_required"


def test_vesta_native_probe_uses_the_headless_interface() -> None:
    assert PROBES["vesta"] == ("VESTA", ["-nogui", "-h"])


def test_data_source_smoke_help_does_not_execute_live_actions(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        run_data_source_smokes,
        "execute_action",
        lambda *_args, **_kwargs: pytest.fail("--help executed a live action"),
    )
    with pytest.raises(SystemExit) as exc_info:
        run_data_source_smokes.main(["--help"])
    assert exc_info.value.code == 0
    assert "--output" in capsys.readouterr().out


def test_scientific_resource_smoke_help_does_not_execute_calculations(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        run_scientific_resource_smokes,
        "execute_action",
        lambda *_args, **_kwargs: pytest.fail("--help executed a calculation"),
    )
    with pytest.raises(SystemExit) as exc_info:
        run_scientific_resource_smokes.main(["--help"])
    assert exc_info.value.code == 0
    assert "--output" in capsys.readouterr().out


def _successful_action_response(action_id: str, backend_id: str, result: dict) -> dict:
    return {
        "status": "success",
        "action": action_id,
        "backend": backend_id,
        "result": result,
        "output_artifacts": [],
        "provenance": {"automatic_fallback_count": 0},
    }


@pytest.mark.parametrize(
    ("action_id", "backend_id", "action_request", "result"),
    [
        (
            "calculate_forces",
            "nwchem",
            {"inputs": {"structure": {"atoms": [{}, {}, {}]}}},
            {"forces": [0.0] * 9, "unit": "eV/angstrom"},
        ),
        (
            "calculate_phonon_density_of_states",
            "phonopy",
            {"inputs": {}},
            {"frequency_thz": [0.0, 1.0], "density_of_states": [0.0, 2.0]},
        ),
        (
            "analyze_free_energy_convergence",
            "pymbar",
            {"inputs": {}},
            {
                "convergence": [
                    {"fraction": 0.5, "delta_f_uncertainty": 0.2},
                    {"fraction": 1.0, "delta_f_uncertainty": 0.1},
                ],
                "unit": "dimensionless_reduced_free_energy",
            },
        ),
        (
            "minimize_system_energy",
            "lammps",
            {"inputs": {}},
            {"lammps_data_path": "minimized.data", "minimized": True},
        ),
        (
            "resolve_chemical_identity",
            "pubchem",
            {"inputs": {}},
            {"match_count": 1, "identity": {"cid": 962}, "candidates": [{"cid": 962}]},
        ),
        (
            "integrate_reaction_network",
            "cantera",
            {"inputs": {}},
            {"time_seconds": [0.0, 1.0], "mole_fractions": [[1.0, 0.0], [0.5, 0.5]]},
        ),
    ],
)
def test_full_action_validator_accepts_supported_scientific_result_shapes(
    action_id: str,
    backend_id: str,
    action_request: dict,
    result: dict,
) -> None:
    response = _successful_action_response(action_id, backend_id, result)
    criteria = _scientific_criteria(
        action_id, backend_id, action_request, response, workspace=None
    )
    assert _attempt_passed(criteria), [
        item for item in criteria if item["required"] and not item["passed"]
    ]


def test_full_action_validator_accepts_empty_diagnostic_log_artifact(
    tmp_path: Path,
) -> None:
    diagnostic = tmp_path / "job.err"
    diagnostic.write_bytes(b"")
    response = {
        "output_artifacts": [
            {
                "path": "job.err",
                "semantic_type": "BackendLog",
                "sha256": (
                    "e3b0c44298fc1c149afbf4c8996fb924"
                    "27ae41e4649b934ca495991b7852b855"
                ),
            }
        ]
    }

    criterion = _artifact_criterion(response, tmp_path)

    assert criterion["passed"] is True


def test_full_action_pysisyphus_neb_has_enough_images_for_cubic_spline() -> None:
    source = TOOLBOX_ROOT.joinpath(
        "scripts", "run_full_action_scientific_validation.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(source)
    image_counts = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or len(node.args) < 4:
            continue
        case_id = node.args[0]
        if not (
            isinstance(case_id, ast.Constant)
            and case_id.value == "pysisyphus_h2_neb"
        ):
            continue
        request = node.args[3]
        assert isinstance(request, ast.Dict)
        for key, value in zip(request.keys, request.values):
            if isinstance(key, ast.Constant) and key.value == "action_settings":
                image_counts.append(ast.literal_eval(value)["images"])

    assert image_counts == [5]


def test_full_action_profiler_ignores_negative_dispatch_without_provider() -> None:
    source = TOOLBOX_ROOT.joinpath(
        "scripts", "run_full_action_scientific_validation.py"
    ).read_text(encoding="utf-8")
    assert "raise ValueError(\"could not resolve the Action provider" not in source
    assert "Negative dispatch tests deliberately reject auto/unsupported" in source
