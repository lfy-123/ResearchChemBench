from __future__ import annotations

import json

import pytest

from researchchem_toolbox import resources
from researchchem_toolbox.backends import docking, electronic, mlip, periodic
from researchchem_toolbox.backends.common import resolve_input_file
from researchchem_toolbox.catalog import catalog_snapshot


def _test_registry(tmp_path, monkeypatch):
    element_root = tmp_path / "elements"
    element_root.mkdir()
    (element_root / "Si.psp8").write_text("pseudo", encoding="utf-8")
    parameter_root = tmp_path / "parameters"
    parameter_root.mkdir()
    (parameter_root / "Si-Si.skf").write_text("sk", encoding="utf-8")
    model_path = tmp_path / "model.pt"
    model_path.write_bytes(b"model")
    potcar_path = tmp_path / "POTCAR.Si"
    potcar_path.write_text("potcar", encoding="utf-8")
    config = tmp_path / "resources.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "selection_policy": "agent_explicit_no_default",
                "resources": [
                    {
                        "id": "test_pseudos",
                        "display_name": "Test pseudos",
                        "kind": "element_file_collection",
                        "selectable": True,
                        "compatible_backends": ["abinit"],
                        "format": "PSP8",
                        "version": "test",
                        "path": str(element_root),
                        "element_pattern": "{element}.psp8",
                        "expected_file_count": 1,
                    },
                    {
                        "id": "test_parameters",
                        "display_name": "Test SK",
                        "kind": "slater_koster_parameter_set",
                        "selectable": True,
                        "compatible_backends": ["dftbplus"],
                        "format": "SKF",
                        "version": "test",
                        "path": str(parameter_root),
                        "file_glob": "*.skf",
                        "expected_file_count": 1,
                    },
                    {
                        "id": "runtime_binary",
                        "display_name": "Runtime binary",
                        "kind": "backend_executable",
                        "selectable": False,
                        "compatible_backends": ["gnina"],
                        "path": str(tmp_path / "binary"),
                    },
                    {
                        "id": "test_model",
                        "display_name": "Test model",
                        "kind": "model_checkpoint",
                        "selectable": True,
                        "compatible_backends": ["deepmd"],
                        "path": str(model_path),
                        "model_branches": ["branch_a"],
                        "model_branch_aliases": {"alias_a": "branch_a"},
                    },
                    {
                        "id": "test_potcar",
                        "display_name": "Test POTCAR",
                        "kind": "single_file_resource",
                        "selectable": True,
                        "compatible_backends": ["vasp"],
                        "path": str(potcar_path),
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("RESEARCHCHEM_RESOURCE_CONFIG", str(config))
    resources._load_config_at.cache_clear()
    return element_root, parameter_root


def test_registered_resources_require_explicit_family_and_element(tmp_path, monkeypatch):
    element_root, parameter_root = _test_registry(tmp_path, monkeypatch)
    assert resources.resolve_resource_reference("resource://test_pseudos/Si") == element_root / "Si.psp8"
    assert resources.resolve_resource_reference(
        {"resource_id": "test_pseudos", "element": "Si"}
    ) == element_root / "Si.psp8"
    assert resources.resolve_resource_reference("resource://test_parameters") == parameter_root
    assert resources.resolve_resource_reference("resource://test_model") == tmp_path / "model.pt"
    assert resources.resolve_resource_reference("resource://test_potcar") == tmp_path / "POTCAR.Si"
    with pytest.raises(ValueError, match="requires an explicit chemical element"):
        resources.resolve_resource_reference("resource://test_pseudos")
    with pytest.raises((ValueError, FileNotFoundError), match="does not contain element|missing"):
        resources.resolve_resource_reference("resource://test_pseudos/C")
    with pytest.raises(ValueError, match="runtime-managed"):
        resources.resolve_resource_reference("resource://runtime_binary")
    with pytest.raises(ValueError):
        resources.resolve_resource_reference("resource://test_pseudos/../Si")


def test_common_file_resolver_accepts_only_registered_resource_refs(tmp_path, monkeypatch):
    element_root, _ = _test_registry(tmp_path, monkeypatch)
    assert resolve_input_file("resource://test_pseudos/Si") == element_root / "Si.psp8"
    with pytest.raises(ValueError, match="Unknown scientific resource"):
        resolve_input_file("resource://not_registered/Si")


def test_variant_collections_require_an_exact_agent_selection(tmp_path, monkeypatch):
    family = tmp_path / "vasp_pbe"
    potcar = family / "Fe_pv" / "POTCAR"
    potcar.parent.mkdir(parents=True)
    potcar.write_text("Fe_pv POTCAR", encoding="utf-8")
    manifest = tmp_path / "vasp_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "resource_id": "test_vasp_variants",
                "selection_policy": "agent_explicit_no_default",
                "variants": {
                    "Fe_pv": {
                        "element": "Fe",
                        "relative_path": "Fe_pv/POTCAR",
                        "sha256": "unused-in-resolver-test",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    config = tmp_path / "variant_resources.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "selection_policy": "agent_explicit_no_default",
                "resources": [
                    {
                        "id": "test_vasp_variants",
                        "display_name": "Test VASP variants",
                        "kind": "variant_file_collection",
                        "selectable": True,
                        "compatible_backends": ["vasp"],
                        "path": str(family),
                        "manifest": str(manifest),
                        "manifest_filename_field": "relative_path",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("RESEARCHCHEM_RESOURCE_CONFIG", str(config))
    resources._load_config_at.cache_clear()

    assert (
        resources.resolve_resource_reference(
            "resource://test_vasp_variants/Fe_pv"
        )
        == potcar
    )
    assert resources.resolve_resource_reference(
        {"resource_id": "test_vasp_variants", "selection": "Fe_pv"}
    ) == potcar
    metadata = resources.resource_reference_metadata(
        "resource://test_vasp_variants/Fe_pv"
    )
    assert metadata["element"] == "Fe"
    assert metadata["selection"] == "Fe_pv"
    snapshot = resources.resource_snapshot()[0]
    assert snapshot["selection_syntax"] == "resource://test_vasp_variants/<Variant>"
    assert snapshot["variants"] == ["Fe_pv"]
    with pytest.raises(ValueError, match="explicit safe variant"):
        resources.resolve_resource_reference("resource://test_vasp_variants")
    with pytest.raises(ValueError, match="does not contain variant"):
        resources.resolve_resource_reference("resource://test_vasp_variants/Fe")
    with pytest.raises(ValueError):
        resources.resolve_resource_reference("resource://test_vasp_variants/../Fe_pv")


def test_catalog_exposes_resource_policy_and_coverage(tmp_path, monkeypatch):
    _test_registry(tmp_path, monkeypatch)
    snapshot = catalog_snapshot(include_health=False)
    assert snapshot["scientific_resource_selection_policy"] == "agent_explicit_no_default"
    assert {item["id"] for item in snapshot["resources"]} == {
        "test_pseudos",
        "test_parameters",
        "runtime_binary",
        "test_model",
        "test_potcar",
    }
    pseudo = next(item for item in snapshot["resources"] if item["id"] == "test_pseudos")
    assert pseudo["selection_syntax"] == "resource://test_pseudos/<Element>"
    assert pseudo["elements"] == ["Si"]
    model = next(item for item in snapshot["resources"] if item["id"] == "test_model")
    assert model["selection_syntax"] == "resource://test_model"
    assert model["size_bytes"] == 5


def test_deepmd_branch_validation_keeps_model_choice_explicit(tmp_path, monkeypatch):
    _test_registry(tmp_path, monkeypatch)
    metadata = resources.resource_reference_metadata("resource://test_model")
    assert mlip._deepmd_head(tmp_path / "model.pt", "alias_a", metadata) == "branch_a"
    with pytest.raises(ValueError, match="explicit named model_branch"):
        mlip._deepmd_head(tmp_path / "model.pt", "", metadata)
    with pytest.raises(ValueError, match="Unknown DeePMD model_branch"):
        mlip._deepmd_head(tmp_path / "model.pt", "unknown", metadata)


def test_gnina_adapter_keeps_hardware_and_model_choice_explicit(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    receptor = tmp_path / "receptor.pdbqt"
    ligand = tmp_path / "ligand.pdbqt"
    receptor.write_text("ATOM\n", encoding="utf-8")
    ligand.write_text("ROOT\nENDROOT\nTORSDOF 0\n", encoding="utf-8")
    captured = {}

    def fake_run_external(**kwargs):
        captured.update(kwargs)
        output = kwargs["directory"] / "poses.pdbqt"
        output.write_text(
            "MODEL 1\n"
            "REMARK minimizedAffinity -7.25\n"
            "REMARK CNNscore 0.81\n"
            "REMARK CNNaffinity 6.40\n"
            "ENDMDL\n",
            encoding="utf-8",
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": "",
            "stderr": "",
            "command": ["gnina"],
        }

    monkeypatch.setattr(docking, "run_external", fake_run_external)
    result = docking.execute(
        "dock_ligand",
        "gnina",
        {
            "inputs": {
                "receptor": "receptor.pdbqt",
                "ligand": "ligand.pdbqt",
                "search_space": {
                    "center_angstrom": [0, 0, 0],
                    "size_angstrom": [10, 10, 10],
                },
            },
            "method_spec": {"cnn_model": "builtin_default", "cnn_scoring": "rescore"},
            "action_settings": {
                "exhaustiveness": 1,
                "num_modes": 1,
                "use_gpu": False,
                "cpu": 1,
                "seed": 7,
            },
        },
    )
    assert result["status"] == "success"
    assert "--no_gpu" in captured["arguments"]
    assert "--energy_range" not in captured["arguments"]
    assert "--cnn" not in captured["arguments"]
    assert result["result"]["scores"][0]["cnn_pose_score"] == pytest.approx(0.81)


def test_orca_input_maps_agent_cpu_limit_to_pal_without_selecting_a_method():
    text = electronic._render_orca(
        "calculate_energy",
        {
            "atoms": [
                {"element": "H", "position_angstrom": [0, 0, 0]},
                {"element": "H", "position_angstrom": [0, 0, 0.74]},
            ]
        },
        {"method": "HF", "basis": "STO-3G"},
        {},
        {"cpu_cores": 2},
    )
    assert "! HF STO-3G SP" in text
    assert "%pal\n  nprocs 2\nend" in text


def test_orca_input_exposes_typed_smd_solvent():
    text = electronic._render_orca(
        "calculate_energy",
        {
            "atoms": [
                {"element": "H", "position_angstrom": [0, 0, 0]},
                {"element": "H", "position_angstrom": [0, 0, 0.74]},
            ]
        },
        {
            "method": "wB97X-D3",
            "basis": "def2-SVP",
            "solvation_model": "smd",
            "solvent": "Ethanol",
        },
        {},
        {"cpu_cores": 1},
    )
    assert "! wB97X-D3 def2-SVP SP CPCM" in text
    assert '%cpcm\n  smd true\n  solvent "Ethanol"\nend' in text


def test_orca_optimization_reads_final_xyz_not_first_trajectory_frame(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def fake_run_external(**kwargs):
        directory = kwargs["directory"]
        (directory / "job.xyz").write_text(
            "2\nfinal\nH 0 0 0\nH 0 0 0.70\n", encoding="utf-8"
        )
        (directory / "job_trj.xyz").write_text(
            "2\ninitial\nH 0 0 0\nH 0 0 0.90\n", encoding="utf-8"
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": (
                "Program Version 6.1.1\n"
                "FINAL SINGLE POINT ENERGY -1.0\n"
                "THE OPTIMIZATION HAS CONVERGED\n"
                "****ORCA TERMINATED NORMALLY****\n"
            ),
            "stderr": "",
            "command": ["orca", "job.inp"],
        }

    monkeypatch.setattr(electronic, "run_external", fake_run_external)
    result = electronic.execute(
        "optimize_geometry",
        "orca",
        {
            "inputs": {
                "structure": {
                    "atoms": [
                        {"element": "H", "position_angstrom": [0, 0, 0]},
                        {"element": "H", "position_angstrom": [0, 0, 0.90]},
                    ]
                }
            },
            "method_spec": {"method": "HF", "basis": "STO-3G"},
            "action_settings": {
                "optimization_convergence": "Tight",
                "max_steps": 20,
            },
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "6.1.1"
    assert result["result"]["structure"]["atoms"][1]["position_angstrom"][2] == pytest.approx(0.70)
    assert result["result"]["structure"]["source_path"].endswith("job.xyz")


def test_orca_completion_rejects_zero_exit_error_termination():
    diagnostic = electronic._orca_completion_error(
        "ORCA finished by error termination in Startup\n  .... aborting the run\n",
        "*** An error occurred in MPI_Type_match_size\nPMIX ERROR: UNREACHABLE\n",
    )
    assert diagnostic is not None
    assert "MPI_Type_match_size" in diagnostic
    assert "error termination" in diagnostic


def test_orca_completion_requires_normal_termination_marker():
    diagnostic = electronic._orca_completion_error(
        "Program Version 6.1.1\nFINAL SINGLE POINT ENERGY -1.0\n",
        "",
    )
    assert diagnostic is not None
    assert "TERMINATED NORMALLY" in diagnostic


def test_orca_completion_accepts_normal_termination_marker():
    assert electronic._orca_completion_error(
        "Program Version 6.1.1\n****ORCA TERMINATED NORMALLY****\n",
        "",
    ) is None


def test_orca_adapter_rejects_zero_exit_error_termination(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def fake_run_external(**_kwargs):
        return {
            "available": True,
            "returncode": 0,
            "stdout": "ORCA finished by error termination in Startup\n  .... aborting the run\n",
            "stderr": "*** An error occurred in MPI_Type_match_size\n",
            "command": ["orca", "job.inp"],
        }

    monkeypatch.setattr(electronic, "run_external", fake_run_external)
    with pytest.raises(RuntimeError, match="ORCA did not terminate normally"):
        electronic.execute(
            "calculate_energy",
            "orca",
            {
                "inputs": {
                    "structure": {
                        "atoms": [{"element": "He", "position_angstrom": [0, 0, 0]}]
                    }
                },
                "method_spec": {"method": "HF", "basis": "STO-3G"},
                "action_settings": {},
                "resource_limits": {"cpu_cores": 2},
            },
        )


def test_orca_normal_nonconverged_optimization_remains_partial_success(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def fake_run_external(**kwargs):
        (kwargs["directory"] / "job.xyz").write_text(
            "2\nlast geometry\nH 0 0 0\nH 0 0 0.80\n", encoding="utf-8"
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": (
                "Program Version 6.1.1\n"
                "FINAL SINGLE POINT ENERGY -0.9\n"
                "****ORCA TERMINATED NORMALLY****\n"
            ),
            "stderr": "",
            "command": ["orca", "job.inp"],
        }

    monkeypatch.setattr(electronic, "run_external", fake_run_external)
    result = electronic.execute(
        "optimize_geometry",
        "orca",
        {
            "inputs": {
                "structure": {
                    "atoms": [
                        {"element": "H", "position_angstrom": [0, 0, 0]},
                        {"element": "H", "position_angstrom": [0, 0, 0.90]},
                    ]
                }
            },
            "method_spec": {"method": "HF", "basis": "STO-3G"},
            "action_settings": {"optimization_convergence": "Tight", "max_steps": 1},
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert result["status"] == "partial_success"
    assert result["result"]["converged"] is False


def test_dftb_input_uses_explicit_agent_method_fields(tmp_path, monkeypatch):
    parameter_root = tmp_path / "sk"
    parameter_root.mkdir()
    (parameter_root / "Si-Si.skf").write_text("sk", encoding="utf-8")
    monkeypatch.setattr(periodic, "resolve_input_file", lambda _value: parameter_root)
    structure = {
        "atoms": [{"element": "Si", "position_angstrom": [0, 0, 0]}],
        "cell_angstrom": [[5.43, 0, 0], [0, 5.43, 0], [0, 0, 5.43]],
        "pbc": [True, True, True],
    }
    path, _arguments, _stdin = periodic._simple_periodic_input(
        "dftbplus",
        "calculate_periodic_energy",
        {
            "inputs": {"structure": structure},
            "method_spec": {
                "parameter_set": "resource://test_parameters",
                "k_points": {"grid": [1, 1, 1], "shift": [0, 0, 0]},
                "scc": True,
                "max_angular_momenta": {"Si": "d"},
            },
            "action_settings": {"scc_tolerance": 1e-8, "max_scc_iterations": 100},
        },
        tmp_path,
    )
    text = path.read_text(encoding="utf-8")
    assert 'Si = "d"' in text
    assert "SCC = Yes" in text
    assert "SCCTolerance = 1e-08" in text
    assert "ParserVersion = 14" in text
    assert "Driver = {}" not in text


def test_periodic_parsers_distinguish_atomic_force_and_physical_stress_units(tmp_path):
    qe_stdout = """
     atom    1 type  1   force =     0.10000000    0.20000000    0.30000000
     Total force =     0.374166     Total SCF correction =     0.000000
    """
    request = {
        "inputs": {
            "structure": {
                "atoms": [{"element": "Si", "position_angstrom": [0, 0, 0]}],
                "cell_angstrom": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                "pbc": [True, True, True],
            }
        }
    }
    qe = periodic._parse_qe(
        "calculate_periodic_forces", qe_stdout, tmp_path, request
    )
    assert qe["forces"] == [[0.1, 0.2, 0.3]]

    abinit_stdout = """
 Cartesian components of stress tensor (hartree/bohr^3)
  sigma(1 1)= -1.0E-05  sigma(3 2)=  4.0E-06
  sigma(2 2)= -2.0E-05  sigma(3 1)=  5.0E-06
  sigma(3 3)= -3.0E-05  sigma(2 1)=  6.0E-06
 Cartesian components of stress tensor (GPa)
  sigma(1 1)= -9.0E-01  sigma(3 2)=  4.0E-01
  sigma(2 2)= -8.0E-01  sigma(3 1)=  5.0E-01
  sigma(3 3)= -7.0E-01  sigma(2 1)=  6.0E-01
 cartesian forces (hartree/bohr) at end:
    1      0.10000000000000     0.20000000000000     0.30000000000000
 cartesian forces (eV/Angstrom) at end:
    1      5.10000000000000     5.20000000000000     5.30000000000000
    """
    assert periodic._parse_abinit_stress(abinit_stdout) == [
        [-1e-5, 6e-6, 5e-6],
        [6e-6, -2e-5, 4e-6],
        [5e-6, 4e-6, -3e-5],
    ]
    assert periodic._parse_abinit_forces(abinit_stdout, 1) == [[0.1, 0.2, 0.3]]


def test_dftb_relax_driver_uses_parser14_block_structure(tmp_path, monkeypatch):
    parameter_root = tmp_path / "sk"
    parameter_root.mkdir()
    (parameter_root / "Si-Si.skf").write_text("sk", encoding="utf-8")
    monkeypatch.setattr(periodic, "resolve_input_file", lambda _value: parameter_root)
    structure = {
        "atoms": [{"element": "Si", "position_angstrom": [0, 0, 0]}],
        "cell_angstrom": [[5.43, 0, 0], [0, 5.43, 0], [0, 0, 5.43]],
        "pbc": [True, True, True],
    }
    path, _arguments, _stdin = periodic._simple_periodic_input(
        "dftbplus",
        "relax_periodic_structure",
        {
            "inputs": {"structure": structure},
            "method_spec": {
                "parameter_set": "resource://test_parameters",
                "k_points": {"grid": [1, 1, 1], "shift": [0, 0, 0]},
                "scc": True,
                "max_angular_momenta": {"Si": "d"},
            },
            "action_settings": {
                "scc_tolerance": 1e-8,
                "max_scc_iterations": 100,
                "force_threshold_ev_per_angstrom": 0.1,
                "max_steps": 5,
                "relax_cell": False,
            },
        },
        tmp_path,
    )
    text = path.read_text(encoding="utf-8")
    assert "Driver = GeometryOptimization {\n" in text
    assert "  MaxSteps = 5\n" in text
    assert "  Convergence = {\n" in text
    assert "  LatticeOpt = No\n" in text


def test_vasp_input_requires_explicit_potcar_and_scientific_controls(
    tmp_path, monkeypatch
):
    potcar = tmp_path / "POTCAR.Si"
    potcar.write_text("Si test POTCAR\n", encoding="utf-8")
    monkeypatch.setattr(periodic, "resolve_input_file", lambda _value: potcar)
    request = {
        "inputs": {
            "structure": {
                "atoms": [
                    {"element": "Si", "position_angstrom": [0, 0, 0]},
                    {"element": "Si", "position_angstrom": [1.35, 1.35, 1.35]},
                ],
                "cell_angstrom": [[5.43, 0, 0], [0, 5.43, 0], [0, 0, 5.43]],
                "pbc": [True, True, True],
            }
        },
        "method_spec": {
            "pseudopotentials": {"Si": "resource://test_potcar"},
            "encut_ev": 245.0,
            "k_points": {"grid": [2, 2, 2], "shift": [0, 0, 0]},
            "kpoint_scheme": "gamma",
            "precision": "Accurate",
            "algorithm": "Normal",
            "ismear": 0,
            "sigma_ev": 0.05,
            "spin_polarized": False,
            "real_space_projection": False,
            "xc_family": "pbe",
        },
        "action_settings": {"scf_convergence_ev": 1e-6, "max_scf_cycles": 80},
    }
    symbols, order = periodic._write_vasp_inputs(
        "calculate_periodic_energy", request, tmp_path
    )
    assert symbols == ["Si", "Si"]
    assert order == [0, 1]
    incar = (tmp_path / "INCAR").read_text(encoding="utf-8")
    assert "ENCUT = 245.0" in incar
    assert "GGA = PE" in incar
    assert "ISPIN = 1" in incar
    assert "LREAL = .FALSE." in incar
    assert (tmp_path / "POTCAR").read_text(encoding="utf-8").startswith(
        "Si test POTCAR"
    )


def test_vasp_rejects_a_registered_variant_for_the_wrong_element(
    tmp_path, monkeypatch
):
    potcar = tmp_path / "Fe_pv" / "POTCAR"
    potcar.parent.mkdir()
    potcar.write_text("Fe POTCAR", encoding="utf-8")
    monkeypatch.setattr(periodic, "resolve_input_file", lambda _value: potcar)
    monkeypatch.setattr(
        periodic,
        "resource_reference_metadata",
        lambda _value: {
            "kind": "variant_file_collection",
            "selection": "Fe_pv",
            "element": "Fe",
        },
    )
    request = {
        "inputs": {
            "structure": {
                "atoms": [{"element": "Si", "position_angstrom": [0, 0, 0]}],
                "cell_angstrom": [[5, 0, 0], [0, 5, 0], [0, 0, 5]],
                "pbc": [True, True, True],
            }
        },
        "method_spec": {
            "pseudopotentials": {
                "Si": "resource://test_vasp_variants/Fe_pv"
            },
            "encut_ev": 400,
            "k_points": {"grid": [1, 1, 1], "shift": [0, 0, 0]},
            "kpoint_scheme": "gamma",
            "precision": "Accurate",
            "algorithm": "Normal",
            "ismear": 0,
            "sigma_ev": 0.05,
            "spin_polarized": False,
            "real_space_projection": False,
            "xc_family": "pbe",
        },
        "action_settings": {"scf_convergence_ev": 1e-6, "max_scf_cycles": 60},
    }
    with pytest.raises(ValueError, match="belongs to element 'Fe', not 'Si'"):
        periodic._write_vasp_inputs("calculate_periodic_energy", request, tmp_path)


def test_vasp_parser_restores_original_atom_order(tmp_path):
    (tmp_path / "OUTCAR").write_text(
        " free  energy   TOTEN  =      -10.500000 eV\n"
        " TOTAL-FORCE (eV/Angst)\n"
        " -------------------------------------------------------------------\n"
        " 0 0 0  1.0 1.1 1.2\n"
        " 0 0 0  2.0 2.1 2.2\n"
        " 0 0 0  3.0 3.1 3.2\n"
        " -------------------------------------------------------------------\n"
        " total drift: 0 0 0\n",
        encoding="utf-8",
    )
    request = {
        "inputs": {
            "structure": {
                "atoms": [
                    {"element": "Si", "position_angstrom": [0, 0, 0]},
                    {"element": "C", "position_angstrom": [1, 1, 1]},
                    {"element": "Si", "position_angstrom": [2, 2, 2]},
                ],
                "cell_angstrom": [[5, 0, 0], [0, 5, 0], [0, 0, 5]],
                "pbc": [True, True, True],
            }
        }
    }
    result = periodic._parse_vasp_result(
        "calculate_periodic_forces", tmp_path, request, ["Si", "C", "Si"], [0, 2, 1]
    )
    assert result["energy_ev"] == pytest.approx(-10.5)
    assert result["forces"] == [
        [1.0, 1.1, 1.2],
        [3.0, 3.1, 3.2],
        [2.0, 2.1, 2.2],
    ]
