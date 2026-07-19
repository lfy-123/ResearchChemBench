from __future__ import annotations

from pathlib import Path

import pytest

from researchchem_toolbox.backends import licensed_md, quantum_legacy


WATER = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.75716, 0.58626]},
        {"element": "H", "position_angstrom": [0.0, -0.75716, 0.58626]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}


def test_gaussian_renderer_uses_only_typed_method_and_resource_fields():
    text = quantum_legacy._render_gaussian(
        "optimize_geometry",
        WATER,
        {"method": "B3LYP", "basis": "6-31G(d)", "dispersion": "EmpiricalDispersion=GD3BJ"},
        {"scf_convergence": "Tight", "optimization_convergence": "Tight", "max_steps": 40},
        {"cpu_cores": 3, "memory_mb": 768},
    )
    assert "%NProcShared=3" in text
    assert "%Mem=768MB" in text
    assert "#P B3LYP/6-31G(d) Opt=(Tight,MaxCycles=40) SCF=Tight EmpiricalDispersion=GD3BJ" in text
    assert "0 1" in text


def test_gaussian_formatted_checkpoint_hessian_is_reconstructed(tmp_path):
    path = tmp_path / "job.fchk"
    path.write_text(
        "Cartesian Force Constants                  R   N=           3\n"
        "  1.00000000E+00  2.00000000E+00  3.00000000E+00\n",
        encoding="utf-8",
    )
    assert quantum_legacy._parse_gaussian_fchk_hessian(path, 2) == [
        [1.0, 2.0],
        [2.0, 3.0],
    ]


def test_gaussian_rejects_unparsed_correlated_total_energy_methods():
    with pytest.raises(ValueError, match="SCF/DFT total energies"):
        quantum_legacy._render_gaussian(
            "calculate_energy",
            WATER,
            {"method": "CCSD(T)", "basis": "STO-3G"},
            {"scf_convergence": "Tight"},
            {"cpu_cores": 1},
        )


def test_gamess_renderer_preserves_explicit_basis_and_convergence():
    text = quantum_legacy._render_gamess(
        "calculate_energy",
        WATER,
        {"scftyp": "RHF", "gbasis": "STO", "ngauss": 3},
        {"scf_convergence": 1e-8},
        {"memory_mb": 512},
    )
    assert "SCFTYP=RHF RUNTYP=ENERGY" in text
    assert "$SCF DIRSCF=.TRUE. CONV=8 $END" in text
    assert "$BASIS GBASIS=STO NGAUSS=3 $END" in text
    assert "O 8.0" in text


def test_namd_renderer_builds_one_segment_without_a_script_input(tmp_path, monkeypatch):
    files = {}
    for name in ("system.psf", "coordinates.pdb", "parameters.prm"):
        path = tmp_path / name
        path.write_text(name, encoding="utf-8")
        files[name] = path
    monkeypatch.setattr(licensed_md, "resolve_input_file", lambda value: Path(value))
    text = licensed_md._render_namd(
        "propagate_dynamics",
        {
            "namd_psf_path": str(files["system.psf"]),
            "coordinate_path": str(files["coordinates.pdb"]),
            "namd_parameter_paths": [str(files["parameters.prm"])],
        },
        {
            "force_field_family": "charmm",
            "exclude": "scaled1-4",
            "one_four_scaling": 1.0,
            "cutoff_angstrom": 12.0,
            "switching": True,
            "switch_distance_angstrom": 10.0,
            "pairlist_distance_angstrom": 14.0,
            "pme": False,
            "rigid_bonds": "none",
        },
        {
            "ensemble": "NVE",
            "temperature_kelvin": 300.0,
            "timestep_fs": 0.5,
            "steps": 5,
            "report_interval": 1,
            "random_seed": 7,
        },
    )
    assert "stepspercycle 5" in text
    assert "DCDfile segment.dcd" in text
    assert text.rstrip().endswith("run 5")


def test_amber_renderer_maps_agent_boundary_ensemble_and_restart():
    text = licensed_md._render_amber(
        "propagate_dynamics",
        {"boundary": "periodic", "cutoff_angstrom": 9.0, "constraints": "h_bonds"},
        {
            "ensemble": "NPT",
            "temperature_kelvin": 300.0,
            "pressure_bar": 1.0,
            "timestep_fs": 2.0,
            "steps": 100,
            "report_interval": 10,
            "random_seed": 11,
            "restart": True,
        },
    )
    assert "ntb=2" in text
    assert "ntp=1" in text
    assert "irest=1" in text
    assert "ntx=5" in text
    assert "dt=0.002" in text


def test_charmm_renderer_stages_long_paths_and_exposes_only_one_segment(tmp_path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    paths = {}
    for name in ("top.rtf", "par.prm", "system.psf", "coordinates.crd"):
        path = source / name
        path.write_text(name, encoding="utf-8")
        paths[name] = path
    monkeypatch.setattr(licensed_md, "resolve_input_file", lambda value: Path(value))
    directory = tmp_path / "run"
    directory.mkdir()
    text = licensed_md._render_charmm(
        "minimize_system_energy",
        {
            "charmm_topology_paths": [str(paths["top.rtf"])],
            "charmm_parameter_paths": [str(paths["par.prm"])],
            "charmm_psf_path": str(paths["system.psf"]),
            "charmm_coordinate_path": str(paths["coordinates.crd"]),
        },
        {
            "force_field_family": "charmm",
            "coordinate_format": "card",
            "flexible_parameters": False,
            "electrostatics": "cdie",
            "electrostatic_switch": "fswitch",
            "dielectric": 1.0,
            "vdw_switch": "vswitch",
            "cutoff_angstrom": 12.0,
            "switch_on_angstrom": 10.0,
            "pairlist_distance_angstrom": 14.0,
            "constraints": "none",
        },
        {
            "algorithm": "abnr",
            "max_iterations": 20,
            "gradient_tolerance_kcal_mol_angstrom": 0.1,
            "report_interval": 5,
        },
        directory,
    )
    assert 'read rtf card name "topology_1.rtf"' in text
    assert 'read param card name "parameter_1.prm"' in text
    assert "mini abnr nstep 20 nprint 5 tolgrad 0.1" in text
    assert (directory / "system.psf").is_file()
    assert (directory / "coordinates.crd").is_file()
