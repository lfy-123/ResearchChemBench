---
software_id: gplearn
versions: ["0.4.3"]
topics: ["troubleshooting", "errors", "preflight"]
aliases: ["gplearn", "symbolic regression errors"]
inputs: ["Action request", "CSV table"]
outputs: ["diagnostic", "repair guidance"]
last_smoke_tested: "2026-08-05"
---
# gplearn Troubleshooting

## Diagnose in this order

1. Confirm backend `gplearn` is available in the kinetics runtime.
2. Inspect the Action contract and required settings.
3. Verify the CSV path is workspace-relative and the file is parseable.
4. Verify ID, feature, and target columns exactly match the header.
5. Check split disjointness and missing or duplicate IDs.
6. Check function names, probability sums, depth ranges, and numeric bounds.
7. Check `n_jobs` against allocated CPU cores.
8. Only then increase the evolutionary search budget.

## Known failures and repairs

| Symptom | Likely cause | Corrective action |
|---|---|---|
| backend unavailable | gplearn is absent from `.envs/kinetics-legacy` | recreate the declared reaction-kinetics environment and run the profile probe |
| input path rejected | CSV lies outside the workspace or is missing | stage it under `RESEARCHCHEMBENCH_WORKSPACE` and pass the relative path |
| unknown column | request and CSV header differ | inspect the header and correct the explicit column list |
| duplicate ID | ID column is not unique | construct a stable unique identifier before splitting |
| train/validation overlap | one or more IDs occur in both lists | repair the split; never let the backend resolve leakage silently |
| nonnumeric feature | a selected column contains strings or missing data | clean explicitly or select valid numeric features |
| unknown function | function set contains an unsupported primitive | use the Action allow-list returned by `inspect_action` |
| invalid genetic probabilities | crossover and mutation probabilities violate the contract | select explicit nonnegative probabilities within the documented total |
| CPU request rejected | `n_jobs` exceeds `resource_limits.cpu_cores` | reduce workers or request a justified allocation |
| unstable expression | stochastic searches find different algebraic forms | run the seed-stability Action and report all supported forms |
| low train error, poor validation | overfitting or leakage-prone search space | strengthen the split, parsimony, or search design; do not accept the model |

## False-success prevention

Process completion is not scientific success. Require finite held-out metrics,
nonempty validation data, an interpretable expression, and comparison to a
baseline. Check that protected operators are not masking invalid physical domains.

## Reproducibility failures

Changing row order, dependency versions, CPU parallelism, or the split can alter
the search. Preserve the CSV hash, seed, runtime version, complete settings, and
returned artifacts. Compare runs only when all non-seed fields are identical.

## Resource failures

Reduce population, generations, and `n_jobs` before requesting more resources.
The evaluator controls timeout. A larger budget does not repair malformed data,
an invalid operator domain, or leakage.

## Pre-submission checklist

- gplearn 0.4.3 runtime is available.
- Typed Action and backend are explicitly selected.
- CSV is inside the workspace and immutable.
- ID column is unique and complete.
- Feature and target columns are numeric.
- Train and validation IDs are explicit and disjoint.
- Target units and metric are documented.
- Function set and protected-operator implications are understood.
- Population, generations, depth, parsimony, and probabilities are bounded.
- Seed or seed list is explicit.
- `n_jobs` does not exceed allocated CPU cores.
- Held-out and stability validation criteria are defined before execution.
