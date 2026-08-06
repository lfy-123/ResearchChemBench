---
software_id: gplearn
versions: ["0.4.3"]
topics: ["common-tasks", "symbolic-regression", "stability", "validation"]
aliases: ["gplearn", "symbolic descriptor"]
inputs: ["training table", "model result JSON"]
outputs: ["expression", "seed comparison", "summary"]
last_smoke_tested: "2026-08-05"
---
# gplearn Common Tasks

## Fit one baseline

Use `fit_symbolic_regression_baseline` for a single deterministic run. Provide
the CSV, feature and target columns, explicit split IDs, metric, function set,
population, generations, tournament size, constant range, initialization depth,
parsimony coefficient, genetic probabilities, sample fraction, `n_jobs`, and seed.

Validate that the returned expression is finite on both splits. Record the
held-out metric and expression length. Compare against constant, linear, or
domain-standard baselines outside this Action when the scientific task requires it.

## Assess seed stability

Use `assess_symbolic_regression_seed_stability` with two or more explicit seeds.
The Action keeps the dataset, split, metric, and search settings fixed. It returns
per-seed expressions and validation metrics, the number of unique expressions,
the dominant-expression fraction, and aggregate error statistics.

Stable validation error with unstable algebraic forms means the data may not
identify one descriptor. Stable expressions with poor held-out error are also
not useful. Interpret both axes.

## Summarize saved results

Use `summarize_symbolic_regression_results` on a toolbox-produced JSON result.
This Action performs bounded parsing and aggregation only. It does not load a
pickle, execute Python, refit a model, or change a split.

## Minimum input responsibilities

- Select chemically meaningful, unit-aware features.
- Preserve a unique row identifier.
- Define disjoint train and validation IDs before fitting.
- State the target units and metric interpretation.
- Choose an operator set compatible with feature domains.
- Bound the evolutionary budget and parallelism.
- Retain all random seeds and the exact CSV hash.

## Expected output families

- Plain symbolic expression and program representation.
- Training and held-out predictions and metrics.
- Program complexity and search history.
- Per-seed expressions and stability statistics.
- JSON and table artifacts with execution provenance.

## Domain safety

Division, logarithm, square root, and inverse functions use protected numerical
implementations. Protected execution prevents crashes but does not make every
expression physically meaningful. Check units, signs, asymptotic behavior, and
the sampled domain before interpreting a formula.

## Data leakage checks

Do not use target-derived features, future observations, duplicated structures,
or near-identical configurations across the split unless the benchmark protocol
explicitly permits them. Group-aware or composition-aware splitting must be
performed before calling this Action.

## Scientific convergence notes

Report sensitivity to population, generations, parsimony, operator set, and
random seed. A result is stronger when held-out error and expression family are
stable across justified changes. Do not call one search “converged” solely
because the generation limit was reached.

## Resource notes

Parallel workers replicate model-search memory. Use one worker for small smoke
tests. Increase `n_jobs` only when the declared CPU allocation and memory support it.
