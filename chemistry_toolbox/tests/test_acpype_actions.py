from __future__ import annotations

import shutil
import subprocess
import os
from pathlib import Path

from chemistry_toolbox.src.backends import structure
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
ACPYPE = ROOT / ".envs" / "molecular-simulation-openff" / "bin" / "acpype"
GROMACS = ROOT / ".envs" / "molecular-simulation-openff" / "bin" / "gmx"
RUNTIME = ROOT / ".envs" / "molecular-simulation-openff"
BENZENE = ROOT / ".software_cache" / "sources" / "acpype" / "2023.10.27" / "source" / "tests" / "benzene.mdl"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


def _generation_request(source: Path) -> dict:
    return {
        "inputs": {"structure_file": str(source)},
        "method_spec": {
            "atom_type": "gaff2",
            "charge_method": "gas",
            "net_charge": 0,
            "multiplicity": 1,
            "charge_program": "sqm",
        },
        "action_settings": {
            "output_topologies": "gmx",
            "maximum_charge_time_seconds": 120,
            "merge_atom_types": False,
            "sort_atoms": False,
        },
        "resource_limits": {"cpu_cores": 1, "walltime_seconds": 120},
    }


def _stage_benzene(tmp_path: Path) -> Path:
    return Path(shutil.copy2(BENZENE, tmp_path / "benzene.mdl"))


def _configure_runtime(monkeypatch) -> None:
    monkeypatch.setenv("CHEMGRAPH_ACPYPE_COMMAND", str(ACPYPE))
    monkeypatch.setenv("PATH", f"{RUNTIME / 'bin'}:{os.environ.get('PATH', '')}")
    monkeypatch.setenv("LD_LIBRARY_PATH", f"{RUNTIME / 'lib'}:{os.environ.get('LD_LIBRARY_PATH', '')}")


def test_acpype_generates_real_topologies_and_gromacs_accepts_them(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    result = _execute(
        "generate_small_molecule_topology", "acpype", _generation_request(_stage_benzene(tmp_path))
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "2023.10.27"
    assert result["result"]["charge_method"] == "gas"
    assert result["result"]["force_field"] == "gaff2"
    topology = tmp_path / result["result"]["gromacs_topology_path"]
    coordinates = tmp_path / result["result"]["gromacs_coordinate_path"]
    mdp = topology.parent / "em.mdp"
    completed = subprocess.run(
        [str(GROMACS), "grompp", "-c", str(coordinates), "-p", str(topology), "-f", str(mdp), "-o", str(tmp_path / "em.tpr"), "-maxwarn", "0"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmp_path,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert (tmp_path / "em.tpr").is_file()


def test_acpype_converts_generated_amber_pair_to_gromacs(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    generated = _execute(
        "generate_small_molecule_topology", "acpype", _generation_request(_stage_benzene(tmp_path))
    )
    converted = _execute(
        "convert_amber_topology_to_gromacs",
        "acpype",
        {
            "inputs": {
                "amber_topology": str(tmp_path / generated["result"]["amber_topology_path"]),
                "amber_coordinates": str(tmp_path / generated["result"]["amber_coordinate_path"]),
            },
            "method_spec": {},
            "action_settings": {"direct_conversion": False, "sort_atoms": False},
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 60},
        },
    )
    assert converted["status"] == "success"
    assert (tmp_path / converted["result"]["gromacs_topology_path"]).is_file()
    assert (tmp_path / converted["result"]["gromacs_coordinate_path"]).is_file()


def test_acpype_action_dispatches_through_unified_service(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    request = _generation_request(_stage_benzene(tmp_path))
    request["resource_limits"].pop("walltime_seconds")
    result = execute_action(
        "generate_small_molecule_topology",
        {"backend_id": "acpype", **request},
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "2023.10.27"
