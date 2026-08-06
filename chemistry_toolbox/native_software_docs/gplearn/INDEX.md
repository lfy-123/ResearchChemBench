---
software_id: gplearn
versions: ["0.4.3"]
topics: ["index", "navigation", "capabilities", "typed-actions"]
aliases: ["gplearn", "genetic programming symbolic regression"]
inputs: ["CSV table", "feature columns", "target column", "explicit train and validation IDs"]
outputs: ["symbolic expression", "validation metrics", "seed stability report"]
last_smoke_tested: "2026-08-05"
---
# gplearn Toolbox Guide

## Installed version

The configured runtime contains `gplearn 0.4.3` in `.envs/kinetics-legacy`.
gplearn is a Python library and has no supported native CLI. Use the typed
Actions below; do not invent a `gplearn` executable or submit arbitrary Python.

## Layer 1 typed Actions

- `fit_symbolic_regression_baseline` fits one explicitly configured symbolic regressor.
- `assess_symbolic_regression_seed_stability` repeats the same search over explicit seeds.
- `summarize_symbolic_regression_results` reads bounded JSON results without refitting.

## When to use this backend

Use gplearn as an interpretable symbolic-regression baseline when the table,
features, target, split, operator set, search budget, metric, and random seeds
are explicitly supplied. It is useful for descriptor discovery and stability
checks, but it does not prove a physical law or causal relation.

## Documentation map

- `QUICKSTART.md` describes the complete Action request flow.
- `COMMON_TASKS.md` defines fitting, stability, and summary responsibilities.
- `TROUBLESHOOTING.md` lists schema, leakage, resource, and reproducibility failures.
- `examples/action_smoke/submit_request.json` records a compact request shape.

## Working directory

Every CSV or JSON input must be under `RESEARCHCHEMBENCH_WORKSPACE`. Action
outputs are written to `_tool_outputs` and content-addressed artifacts to
`_tool_artifacts`. Paths outside the workspace are rejected.

## Resource boundary

The Agent selects a bounded population, generation count, job count, and seed
list. `n_jobs` must not exceed the allocated CPU count. The evaluation policy,
not the Agent, controls walltime and total machine resources.

## Scientific boundary

The toolbox does not choose the feature columns, held-out observations,
operator set, metric, complexity penalty, or acceptable error. Those choices
must come from the benchmark task or a documented scientific protocol.

## Validation state

The upstream test suite passed, and all three typed Actions have focused tests.
A passing smoke confirms execution and deterministic result handling; it does
not establish extrapolation, dimensional consistency, or descriptor uniqueness.
