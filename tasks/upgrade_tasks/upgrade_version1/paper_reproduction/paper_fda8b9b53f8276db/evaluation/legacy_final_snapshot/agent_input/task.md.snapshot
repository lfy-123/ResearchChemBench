# Scientific objective

Determine a vibrationally stable cis local-minimum geometry of the isolated neutral singlet molecule 6,7-dimethyl-2-(pyridin-2-yl)quinoxaline (compound 1), and quantify its bond-length agreement with the six supplied experimental observations. Independently construct the calculation and interpret the results. The requested cis conformer is not asserted to be the global energy minimum.

# Author-provided scientific guidance

The author comparison concerns a gas-phase cis local minimum and crystal intramolecular distances. The deposited crystal has a different pyridyl orientation. A converged local minimum can differ from the global lowest-energy conformer; the claim concerns the stated cis geometry, vibrational stability and mapped bond comparison. Independently choose and justify a computational protocol.

# Public inputs and scientific boundaries

Use `data/inputs/ccdc_record.json`, the immutable `data/inputs/ccdc_2433822.cif` and `data/inputs/experimental_bonds.json`. Confirm CCDC 2433822 provenance, C15H13N3 identity, charge 0 and multiplicity 1. Extract the complete molecular component and preserve its connectivity and CIF atom labels through a documented mapping. Database retrieval is not required.

The target cis orientation places pyridyl N1 and the adjacent quinoxaline N2 on the same side about the inter-ring C1-C2 bond. Record the mapped N1-C1-C2-N2 torsion and coordinates to demonstrate the assignment; mirror-related torsional signs represent the same cis family. Construct starting orientations from the supplied structure and optimize them independently. A single relaxation of the deposited orientation need not reach the target. Other conformers may be reported separately, and a lower-energy alternative does not invalidate a correctly identified cis local minimum. The physical boundary is an isolated gas-phase molecule, not periodic packing or solvent.

Do not use hidden evaluator files, private verification results, paper/SI optimized coordinates or their calculated answers. The supplied experimental bond lengths and molecular identity are authorized public inputs.

# Required investigation

1. Generate and optimize the target cis geometry with a justified method, basis and convergence protocol. Retain candidate identities and selection evidence for any alternatives actually considered.
2. Validate the selected geometry by frequencies/Hessian or a justified equivalent. Report all imaginary modes, convergence information and failures, and establish that the coordinate and validation files describe the same selected geometry.
3. Map each of C1-C2, C2-C3, N1-C1, N2-C2, N3-C3 and C1-C10 exactly once to the optimized atoms. Use the experimental lengths in `experimental_bonds.json` for the primary comparison, preserving optimized-coordinate precision. Do not substitute a different experimental rounding convention.
4. Report all six residuals, nonnegative RMSE, and ordinary-least-squares R² with an intercept (x experimental, y calculated). Explain the observed agreement and gas-phase/crystal distinction. A high R² alone does not establish small absolute errors or correct conformer identity.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`: system/input provenance, protocol, selected geometry, atom mapping, conformer assignment and signed torsion, frequency evidence, six-row bond table, RMSE/R² and supported conclusion. Include reproducible input/log/coordinate/analysis paths. A failure may be reported truthfully with missing observables identified; it does not satisfy an uncomputed scientific endpoint. Optional supplementary analyses do not replace the required cis result.

# Partial or unsuccessful submission

Use `status: "partial"` or `status: "bounded_failure"` when required calculations or analyses remain unavailable. Retain all actual partial results in their original fields. Include `failure` with a nonempty `reason`, a nonempty `missing_observables` array naming the unavailable result fields, and an `evidence` array of existing input, output or diagnostic paths (empty only if no artifact was produced). Explain which calculation failed or was not attempted; do not invent output files.

For these two statuses, the schema permits `null` for the specified unavailable calculated values, selected structures, state assignments or output paths. Keep the known molecular identities, charges, multiplicities, units and attempted methods. Report actual counts, including zero generated/validated candidates when appropriate. An unavailable frequency result is `null`, not zero imaginary modes or an empty list claiming a completed frequency analysis. A genuinely computed zero or an established empty imaginary-mode list remains valid evidence. A missing comparison is not a zero difference or zero RMSE.

Other statuses, and omission of status where the original schema permits it, retain the complete-result format. Passing this format check does not establish scientific completion: uncomputed endpoints receive no completion credit, and existing scientific rules still assess the actual evidence. This reporting branch does not change the scientific target, required successful investigation, or numerical acceptance criteria.
