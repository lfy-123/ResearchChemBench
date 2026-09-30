import json
import subprocess

import pytest

from chemistry_toolbox.src.backends.composite import evaluate_energy_and_forces
from evaluation.execution.runner import TaskRunner
from test_task_package_v19 import package


def component_request(backend="orca"):
    return {"component_backends": {"calculator": backend}, "method_spec": {"calculator_method": {"method": "HF", "basis": "STO-3G"}},
            "action_settings": {"calculator_action_settings": {"calculate_forces": {}, "calculate_energy": {}}},
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 60}}


@pytest.mark.parametrize("backend,energy,settings,expected", [
    ("orca", -1.0, {}, ["calculate_forces"]),
    ("orca", None, {}, ["calculate_forces", "calculate_energy"]),
    ("orca", float("nan"), {}, ["calculate_forces", "calculate_energy"]),
    ("orca", -1.0, {"future": 1}, ["calculate_forces", "calculate_energy"]),
    ("unknown_backend", -1.0, {}, ["calculate_forces", "calculate_energy"]),
])
def test_energy_reuse_capability_and_fallback(monkeypatch, backend, energy, settings, expected):
    request = component_request(backend)
    request["action_settings"]["calculator_action_settings"]["calculate_energy"] = settings
    calls = []
    def invoke(request, action, structure):
        calls.append(action)
        value = {"forces": [[0, 0, 0]], "unit": "eV/angstrom", "energy_hartree": energy} if action == "calculate_forces" else {"energy": -1.0, "unit": "hartree"}
        return value, {"calculator_status": "success"}
    monkeypatch.setattr("chemistry_toolbox.src.backends.composite.invoke_calculator_component", invoke)
    result = evaluate_energy_and_forces(request, {"atoms": [{}]})
    assert calls == expected and result[0] == -1.0
    assert result[2]["energy_source"] == ("force_result" if len(calls) == 1 else "independent_calculation")


def test_bad_forces_do_not_trigger_an_energy_workaround(monkeypatch):
    calls = []
    def invoke(request, action, structure):
        calls.append(action)
        return {"forces": [[float("nan"), 0, 0]], "unit": "eV/angstrom"}, {}
    monkeypatch.setattr("chemistry_toolbox.src.backends.composite.invoke_calculator_component", invoke)
    with pytest.raises(RuntimeError, match="finite"):
        evaluate_energy_and_forces(component_request(), {"atoms": [{}]})
    assert calls == ["calculate_forces"]


@pytest.mark.parametrize("agent", ["mock", "codex", "claude", "opencode"])
def test_git_discovery_cannot_reach_parent_or_inherited_git_dir(tmp_path, monkeypatch, agent):
    root = tmp_path / "tasks"
    package(root)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    runner = TaskRunner("paper_fixture", task_type="autonomous_research", agent_key=agent,
                        task_roots=[str(root)], workspace_root=tmp_path / "runs")
    runner.workspace.mkdir(parents=True)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / ".git"))
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", "/nonexistent-existing-boundary")
    for _ in range(2):
        environment = runner._agent_environment()
        probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=runner.workspace, env=environment, capture_output=True)
        assert probe.returncode != 0 and not probe.stdout
        assert environment["GIT_CEILING_DIRECTORIES"].startswith("/nonexistent-existing-boundary:")
    assert not (runner.workspace / ".git").exists()


@pytest.mark.integration
def test_orca_force_energy_reuse_matches_independent_single_point(tmp_path, monkeypatch):
    from chemistry_toolbox.src.backends.composite import invoke_calculator_component, energy_hartree
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    structure = {"atoms": [{"element": "H", "position_angstrom": [0, 0, 0]},
                           {"element": "H", "position_angstrom": [0, 0, 0.74]}], "charge": 0, "multiplicity": 1}
    request = component_request()
    energy, forces, energy_provenance, _ = evaluate_energy_and_forces(request, structure)
    independent, _ = invoke_calculator_component(request, "calculate_energy", structure)
    assert energy == pytest.approx(energy_hartree(independent), abs=1e-8)
    assert len(forces) == 2 and energy_provenance["energy_source"] == "force_result"
