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
