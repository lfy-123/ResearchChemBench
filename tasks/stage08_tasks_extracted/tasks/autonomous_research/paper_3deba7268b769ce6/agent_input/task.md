# Scientific objective

For the uniquely specified singly deprotonated E-imine dye-3 chromophore in implicit dichloromethane, independently determine the lowest-energy visible singlet Franck–Condon excitation from an optimized ground-state structure and establish its electronic character. Report the energy in kcal/mol, oscillator strength when available, and a defensible donor/acceptor interpretation. The research object is exactly the molecule in `data/inputs/dye3_phenolate.smiles`; do not replace it with another positional isomer.

# Public inputs and scientific boundaries

`data/inputs/dye3_phenolate.smiles` is authoritative for connectivity and formal charge: the E-imine of 4-aminophenol and 4′-nitro-[1,1′-biphenyl]-4-carbaldehyde, singly deprotonated at phenol (net charge −1). `data/inputs/system_spec.json` fixes charge −1, singlet multiplicity 1, dichloromethane implicit continuum (ε=9.08, n=1.424), and the target state definition. Generate 3-D coordinates and document stereochemical/conformer choices. This is a vertical electronic-structure task; solvent dynamics, vibronic spectra, photochemistry, and ensemble claims are outside scope. The scored system is the isolated molecule; do not add a host or solvent.

# Required scientific validation/investigation

Formulate and execute a reproducible computational investigation within the fixed boundary. Optimize at least one ground-state geometry and validate it as a minimum with a frequency, Hessian, or a justified equivalent. Generate and discriminate any additional plausible conformers or low-lying singlet states needed to make the lowest visible-state assignment credible; deduplicate structures and retain identity and validation context for every candidate actually compared. Compute the selected vertical excitation and use transition-density, orbital, attachment/detachment, natural-transition-orbital, or an equally explicit analysis to determine where electron density leaves and arrives. Report coverage, convergence, state-selection criteria, and limitations. Completion requires a converged validated candidate and an independently supported electronic assignment; stop when further documented candidate generation or starting-conformer tests no longer alter the assignment materially, or submit the bounded-failure branch with all diagnostics if that cannot be achieved.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include candidate identities and validation context, the selected state and energy, computational provenance, and a final conclusion grounded in the reported electronic evidence. A bounded failure must report attempted candidates/calculations and a specific limitation rather than fabricating a result.
