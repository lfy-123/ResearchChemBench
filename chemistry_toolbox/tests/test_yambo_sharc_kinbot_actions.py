from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

from researchchem_toolbox.service import execute_action
from researchchem_toolbox.runtime import runtime_environment


ROOT = Path(__file__).resolve().parents[2]
YAMBO_FIXTURE = ROOT / ".software_cache" / "yambo" / "smoke" / "qe_si_gw_bse"
SHARC_FIXTURE = ROOT / ".software_cache" / "sharc" / "source" / "tests" / "INPUT" / "LVC_overlap"
KINBOT_FIXTURE = ROOT / ".software_cache" / "kinbot" / "smoke" / "action_nonempty_pes_validated3" / "input.json"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    return execute_action(action_id, {"backend_id": backend_id, **request})


@pytest.mark.skipif(not (YAMBO_FIXTURE / "SAVE").is_dir(), reason="Yambo silicon fixture is required")
def test_yambo_runs_real_gw_and_bse_actions(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("CHEMGRAPH_YAMBO_COMMAND", str(ROOT / ".envs" / "yambo-openmpi4" / "bin" / "yambo"))
    monkeypatch.setenv("LD_LIBRARY_PATH", str(ROOT / ".envs" / "yambo-openmpi4" / "lib"))
    shutil.copytree(YAMBO_FIXTURE / "SAVE", tmp_path / "SAVE")
    shutil.copytree(YAMBO_FIXTURE / "gw", tmp_path / "gw")
    shutil.copy2(YAMBO_FIXTURE / "gw.in", tmp_path / "gw.in")
    shutil.copy2(YAMBO_FIXTURE / "bse.in", tmp_path / "bse.in")

    gw = _execute(
        "calculate_quasiparticle_corrections", "yambo",
        {
            "inputs": {"save_directory": "SAVE", "input_file": "gw.in"},
            "method_spec": {},
            "action_settings": {"job_name": "gw", "maximum_returned_records": 20, "require_normal_exit": True},
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert gw["status"] == "success"
    assert gw["result"]["state_count"] == 2
    assert gw["result"]["states"][1]["quasiparticle_energy_ev"] == pytest.approx(4.664891)

    bse = _execute(
        "calculate_bse_optical_spectrum", "yambo",
        {
            "inputs": {"save_directory": "SAVE", "input_file": "bse.in", "restart_directories": ["gw"]},
            "method_spec": {},
            "action_settings": {"job_name": "bse,gw", "maximum_returned_records": 100, "require_normal_exit": True},
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert bse["status"] == "success"
    assert bse["result"]["point_count"] == 50
    assert bse["result"]["spectrum"][0]["epsilon_2"] == pytest.approx(0.268508)


@pytest.mark.skipif(not SHARC_FIXTURE.is_dir(), reason="SHARC LVC fixture is required")
def test_sharc_runs_complete_real_lvc_trajectory(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    sharc = ROOT / ".software_cache" / "sharc" / "source"
    general = ROOT / ".envs" / "general-modern-openmpi5"
    kinetics = ROOT / ".envs" / "kinetics-legacy"
    monkeypatch.setenv("CHEMGRAPH_SHARC_COMMAND", str(sharc / "bin" / "sharc.x"))
    monkeypatch.setenv("PATH", str(general / "bin") + os.pathsep + os.environ.get("PATH", ""))
    monkeypatch.setenv("LD_LIBRARY_PATH", str(kinetics / "lib") + os.pathsep + str(general / "lib"))
    shutil.copytree(SHARC_FIXTURE, tmp_path / "trajectory")
    result = _execute(
        "propagate_nonadiabatic_trajectory", "sharc",
        {
            "inputs": {"trajectory_directory": "trajectory"},
            "method_spec": {"interface": "lvc"},
            "action_settings": {
                "input_filename": "input", "expected_final_time_fs": 30.0,
                "final_time_tolerance_fs": 1e-6, "maximum_returned_steps": 100,
            },
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["record_count"] == 61
    assert result["result"]["final_time_fs"] == pytest.approx(30.0)


def test_kinbot_action_rejects_non_pes_input(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    path = tmp_path / "input.json"
    path.write_text(json.dumps({"title": "single-well", "pes": 0}), encoding="utf-8")
    result = _execute(
        "explore_reaction_network", "kinbot",
        {
            "inputs": {"input_file": "input.json"},
            "method_spec": {},
            "action_settings": {
                "maximum_returned_reactions": 10, "require_pes_done": True,
                "sella_force_threshold_ev_per_angstrom": 5e-4,
                "sella_max_steps": 100, "imaginary_frequency_threshold_cm1": 50.0,
            },
            "resource_limits": {"cpu_cores": 1},
        },
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "backend_input_error"
    assert "pes=1" in result["error"]["message"]


def test_kinbot_runtime_declares_local_nwchem_dependencies():
    environment = runtime_environment("kinbot")
    for variable in (
        "CHEMGRAPH_KINBOT_PES_COMMAND",
        "CHEMGRAPH_NWCHEM_COMMAND",
        "NWCHEM_BASIS_LIBRARY",
        "NWCHEM_NWPW_LIBRARY",
        "KINBOT_NWCHEM_WORK_ROOT",
    ):
        assert environment.get(variable), variable
    assert Path(environment["CHEMGRAPH_KINBOT_PES_COMMAND"]).is_file()
    assert Path(environment["CHEMGRAPH_NWCHEM_COMMAND"]).is_file()
    assert Path(environment["NWCHEM_BASIS_LIBRARY"]).is_dir()


@pytest.mark.skipif(
    os.environ.get("RESEARCHCHEMBENCH_RUN_EXPENSIVE_KINBOT_PES") != "1",
    reason="set RESEARCHCHEMBENCH_RUN_EXPENSIVE_KINBOT_PES=1 for the full local NWChem PES smoke",
)
def test_kinbot_runs_complete_local_nwchem_pes(tmp_path, monkeypatch):
    if not KINBOT_FIXTURE.is_file():
        pytest.skip("KinBot full-PES input fixture is required")
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    shutil.copy2(KINBOT_FIXTURE, tmp_path / "input.json")
    result = _execute(
        "explore_reaction_network", "kinbot",
        {
            "inputs": {"input_file": "input.json"},
            "method_spec": {},
            "action_settings": {
                "maximum_returned_reactions": 100, "require_pes_done": True,
                "sella_force_threshold_ev_per_angstrom": 5e-4,
                "sella_max_steps": 100, "imaginary_frequency_threshold_cm1": 100.0,
            },
            "resource_limits": {"cpu_cores": 1, "memory_mb": 4096, "gpu_count": 0},
        },
    )
    assert result["status"] == "success", result.get("error")
    assert result["result"]["pes_complete"] is True
    assert result["result"]["well_count"] == 1
    assert result["result"]["reaction_record_count"] == 2
    assert all(
        item["summary"].startswith("SUCCESS")
        for item in result["result"]["reaction_records"]
    )
