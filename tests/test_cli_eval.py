import json
from pathlib import Path

from evaluation.cli_eval import _load_yaml, resolve_specs, run_eval


def test_quick_mock_config_dry_run_does_not_create_batch():
    root = Path(__file__).resolve().parents[1]
    config_path = root / "eval_configs" / "quick_mock.yaml"
    config = _load_yaml(config_path)
    specs = resolve_specs(config)
    assert len(specs) == 2
    assert all(spec.agent_key == "mock" for spec in specs)
    assert run_eval(config_path, dry_run=True, no_score=True) == 0


def test_completed_batch_writes_aggregate_results(tmp_path, monkeypatch):
    config_path = tmp_path / "batch.yaml"
    config_path.write_text(
        "\n".join(
            [
                "name: results_test",
                "agents:",
                "  - mock",
                "tasks:",
                "  - Electron_Isodensity_Reproduction_01_Method_Selection",
                "repeats: 1",
                "max_concurrent_runs: 1",
                "timeout_seconds: 30",
                "max_turns: 10",
                "judge:",
                "  enabled: false",
            ]
        )
        + "\n"
    )
    monkeypatch.setattr("evaluation.cli_eval.WORKSPACES_DIR", tmp_path / "workspaces")

    assert run_eval(config_path, no_score=True) == 0

    result_paths = list((tmp_path / "workspaces" / "cli_runs").glob("batch_*/results.json"))
    assert len(result_paths) == 1
    result = json.loads(result_paths[0].read_text())
    assert result["result_type"] == "researchchembench_batch"
    assert result["summary"]["runs"] == 1
    assert result["summary"]["completed"] == 1
    assert result["runs"][0]["task"]["id"] == "Electron_Isodensity_Reproduction_01_Method_Selection"
