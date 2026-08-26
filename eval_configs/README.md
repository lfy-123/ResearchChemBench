# Evaluation configurations

These YAML files are optional launch presets for `python -m evaluation.cli` and
`scripts/run_agent_eval.sh`. The evaluator can also run without a checked-in
YAML file by receiving `--agent`, `--paper-id` and `--task-type` directly.

- `examples/`: small, documented smoke and Agent examples.
- `suites/`: maintained benchmark suites intended for regular runs.

Task selections use explicit mappings:

```yaml
tasks:
  - paper_id: paper_2aca1dd116799b28
    task_type: autonomous_research
```

Use `tasks: all` when the preset should select every installed v19 package.

Host-specific or secret-bearing overrides must use the suffix `.local.yaml`.
They are ignored recursively by Git.
