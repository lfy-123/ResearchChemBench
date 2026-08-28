# Scientific objective

Determine the zero-field total dipole magnitude of the isolated neutral singlet molecule defined by the supplied Cartesian structure, and establish whether the computed electronic structure supports a non-zero intrinsic molecular polarity. The measured endpoint is dipole magnitude in Debye at 0 V.

# Public inputs and scientific boundaries

Use `data/inputs/AD_isolated.xyz` exactly as supplied: 22 atoms, coordinates in Å, charge 0, multiplicity 1, isolated molecule, no electrodes and no external field. `system.json` defines the same identity and atom order. You may optimize or otherwise validate the supplied geometry, but must disclose changes. Do not use the paper, SI, general web or hidden evaluator, and do not calculate transport or junction properties.

# Required scientific validation/investigation

Select and justify an independent computational method, basis/model, software and convergence settings. Compute the dipole at the specified endpoint, report axis/sign convention and magnitude, and validate with convergence plus a geometry/stationarity check or a justified alternative. Record charge, multiplicity, atom-order provenance, software, method, convergence evidence and limitations. Completion requires a parseable result and reproducible provenance; stop once the endpoint is converged and validation is documented, or report bounded failure with attempted settings and cause.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the dipole magnitude in Debye, method/provenance, validation status and an evidence-based conclusion. A bounded-failure branch is allowed only with truthful null result fields and an explanation.
