# Scientific objective

Independently plan and execute a computational test of the authors' qualitative proposal that an optimized molecular model of compound 4b can represent its crystallographic geometry. Use the public neutral, closed-shell, E-configured 4b identity and determine an equilibrium geometry, minimum status, and agreement with the supplied XRD observables. Do not assume that the author's reported computational protocol is the only valid route.

# Public inputs and scientific boundaries

`data/inputs/compound_4b.json` uniquely defines the isolated molecule, formula, charge, multiplicity and E stereochemistry. `data/inputs/geometry_comparison.json` gives the complete named atom selections and experimental XRD values, in angstrom and degree. The target is the isolated electronic-ground-state molecule; crystal packing, solvent, temperature effects and unlisted observables are outside scope. The paper's software, model chemistry, ordered protocol and computed values are not public inputs.

# Required scientific validation/investigation

Choose and justify a reproducible electronic-structure route, optimize the molecule, and calculate harmonic frequencies at a consistent level or a clearly justified validation level. Demonstrate convergence and identify whether the optimized structure is a true minimum (or report a bounded failure with the evidence). For every named bond, angle and torsion, retain the atom label, report the calculated value and signed/absolute deviation from XRD; use a periodic-aware torsion deviation. Report aggregate MAE/RMSE and correlation where defined, and discuss conformer/starting-geometry coverage. Completion requires either a converged stationary point plus frequency result and complete comparison, or a documented bounded failure with attempted inputs, diagnostics and limitations. Stop after convergence and frequency validation of the selected state plus a documented check that no materially different low-energy conformer was found under the stated search plan; do not claim exhaustive conformer coverage unless demonstrated.

# Deliverables

Write `report/results.json` following `submission_schema.json`. Include method, software, coordinates or a coordinate-file path, convergence evidence, frequencies/minimum status, all per-observable comparisons, aggregate metrics, and a conclusion tied to the qualitative author hypothesis. If computation fails, use the schema's failure branch and provide diagnostics rather than fabricated values.
