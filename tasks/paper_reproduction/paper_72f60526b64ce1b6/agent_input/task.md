# Scientific objective

Independently calculate the zero-field dipole magnitude of the isolated neutral singlet A–D donor–acceptor molecule supplied in the public XYZ. The authors qualitatively hypothesize that donor–acceptor electronic asymmetry produces a measurable intrinsic dipole and responds asymmetrically to an applied field; use that hypothesis only to motivate validation, not as a numerical answer. The measured endpoint is the total molecular dipole magnitude in Debye at 0 V.

# Public inputs and scientific boundaries

Use `data/inputs/AD_isolated.xyz` exactly as supplied: 22 atoms, coordinates in Å, charge 0, multiplicity 1, isolated molecule with no Au atoms and no external field. `system.json` repeats these identities. You may generate conformers or optimize the geometry, but must state any changes and preserve the supplied connectivity. Do not use the paper, SI, general web or hidden evaluator. Do not calculate a junction or transport observable.

# Required scientific validation/investigation

Choose and justify an electronic-structure method, basis/model, software and convergence settings independently. Calculate the dipole for the stated neutral singlet endpoint and report the sign/axis convention and magnitude. Validate the result with a converged calculation and a geometry/stationarity check (or clearly explain a scientifically justified alternative if optimization is not performed). Report charge, multiplicity, atom-order provenance, software, method, convergence evidence and any limitations. Completion requires a parseable result plus enough provenance to reproduce it; stop after the endpoint is converged and the validation evidence is recorded, or report bounded failure with the attempted settings and cause.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the dipole magnitude in Debye, method/provenance, validation status and a concise scientific conclusion. A bounded-failure branch is allowed only with truthful null result fields and an explanation of the failed calculation.
