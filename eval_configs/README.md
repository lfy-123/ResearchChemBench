# Evaluation configurations

These YAML files are optional launch presets for `python -m evaluation.cli` and
`scripts/run_agent_eval.sh`. The evaluator can also run without a checked-in
YAML file by receiving `--agent` and `--task` directly.

- `examples/`: small, documented smoke and Agent examples.
- `suites/`: maintained benchmark suites intended for regular runs.
- `campaigns/`: study-specific configurations retained for reproducibility.
- `campaigns/*/archived_reruns/`: historical retry subsets; not standard suites.

Host-specific or secret-bearing overrides must use the suffix `.local.yaml`.
They are ignored recursively by Git.
