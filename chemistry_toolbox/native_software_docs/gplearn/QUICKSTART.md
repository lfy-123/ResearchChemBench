---
software_id: gplearn
versions: ["0.4.3"]
topics: ["quickstart", "typed-actions", "staging", "resources"]
aliases: ["gplearn", "symbolic regression"]
inputs: ["CSV table", "explicit split", "search hyperparameters"]
outputs: ["model JSON", "metrics", "artifacts"]
last_smoke_tested: "2026-08-05"
---
# gplearn Quickstart

## Complete Action flow

1. Inspect `fit_symbolic_regression_baseline` with backend `gplearn`.
2. Stage one CSV under the evaluation workspace.
3. Declare feature columns, target column, and the ID column.
4. Provide disjoint train and validation ID lists.
5. Select the metric and every allowed symbolic function explicitly.
6. Bound population size, generations, tournament size, depth, and `n_jobs`.
7. Supply an integer random seed and run the typed Action.
8. Check held-out metrics, expression complexity, warnings, and provenance.

## Toolbox submission request

Use `execute_action` with `action_id=fit_symbolic_regression_baseline`,
`backend_id=gplearn`, and an Action request matching
`examples/action_smoke/submit_request.json`. The example is a schema guide;
replace all paths, columns, IDs, and scientific settings.

## Input contract

The CSV must contain a unique non-empty ID column, every requested numeric
feature, and one numeric target. Missing values, duplicate IDs, nonnumeric
values, or absent split IDs are rejected. Train and validation IDs must be
disjoint. Rows not named by either list are not silently added.

## Search contract

The function set is an allow-list of gplearn primitives. Population size and
generation count control the main search budget. Tournament size controls
selection pressure. Initial depth and parsimony coefficient affect expression
complexity. Genetic-operation probabilities must satisfy the Action contract.

## Reproducibility

Use one explicit seed for a baseline and several explicit seeds for a stability
study. Keep the data split and all hyperparameters identical when comparing
seeds. A repeated seed should reproduce the same expression and metrics in the
fixed runtime.

## Resource mapping

Set `resource_limits.cpu_cores` and keep `action_settings.n_jobs` at or below
that value. Memory grows with row count, feature count, population, and parallel
workers. Start with a bounded pilot before increasing population or generations.
Do not supply `walltime_seconds`; evaluation policy owns it.

## Output checks

Require `status=success`, a non-empty symbolic expression, finite train and
validation metrics, the expected train/validation counts, and retained input
and result artifacts. Compare the validation metric with a simple baseline.

## Convergence interpretation

Genetic programming does not provide mathematical convergence. Treat the best
fitness history, held-out error, expression stability, and search-budget
sensitivity as separate evidence. A low training error alone is insufficient.

## Working directory and provenance

The backend records the exact runtime, explicit Agent settings, source artifact,
result artifact, and selected backend. Keep the CSV immutable across comparisons.
