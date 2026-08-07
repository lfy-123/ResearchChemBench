# Evaluation engine

This package owns benchmark orchestration and scoring. Scientific software
execution remains in `chemistry_toolbox/`, while task inputs and evaluator-only
targets remain in `tasks/`.

| Path | Responsibility |
|---|---|
| `cli.py` | Single-run and batch command-line orchestration |
| `settings.py` | Environment-backed evaluator settings and Agent presets |
| `schemas/` | Validated task models and evaluation launch specifications |
| `execution/` | Workspace construction, Agent adapters, process supervision, and live progress |
| `scoring/` | Judge prompts, deterministic scoring policies, and scoring service |
| `provenance/` | Managed traces, model I/O, token usage, and result summaries |
| `repository.py` | Task/run discovery and safe file-tree access |
| `web/` | Flask API and static browser interface |
| `testing/` | Deterministic test Agent used by local validation |

Preferred entry points:

```bash
python -m evaluation
python -m evaluation.cli --agent mock --task TASK_ID --no-score
researchchembench-eval eval_configs/suites/full.yaml
```

`python -m evaluation.cli_eval` remains available only for compatibility with
older automation.
