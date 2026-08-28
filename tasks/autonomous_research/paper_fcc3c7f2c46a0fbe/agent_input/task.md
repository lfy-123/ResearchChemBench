# Scientific objective

Determine computationally whether the equilibrium structure of compound 4b reproduces its experimentally observed intramolecular XRD geometry and whether the calculated stationary point is a true minimum. Independently formulate and justify the calculation and any conformer/state checks needed to support the conclusion.

# Public inputs and scientific boundaries

`data/inputs/compound_4b.json` uniquely defines neutral, closed-shell, E-configured compound 4b. `data/inputs/geometry_comparison.json` supplies the named XRD bond lengths, angles and torsions in angstrom and degree. Study the isolated electronic-ground-state molecule; crystal packing, solvent, temperature effects and unlisted properties are outside scope. No author route, software, model chemistry or result values are supplied.

# Required scientific validation/investigation

Select and justify a reproducible optimization and harmonic-frequency route. Establish convergence and classify the optimized structure as a true minimum or report failure. Preserve each supplied atom-label selector and report calculated value plus deviation for every observable, with periodic-aware torsion differences and aggregate MAE/RMSE/correlation where meaningful. Explain starting structures, conformer/state coverage, deduplication and why the stopping point is scientifically adequate. Completion is a converged stationary point with frequency validation and complete geometry comparison, or an honest bounded-failure report containing diagnostics and limitations. Stop when the selected state is validated and additional planned starting-structure checks no longer change the conclusion, or clearly report that the stopping condition could not be met.

# Deliverables

Write `report/results.json` as specified by `submission_schema.json`, including route, coordinates/path, convergence, frequencies/minimum status, complete per-observable comparisons, metrics, conclusion and limitations. A failed or incomplete investigation must use the explicit failure branch and must not invent numerical results.
