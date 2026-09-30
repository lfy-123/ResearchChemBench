# Scientific objective

Determine the coverage dependence of Li adsorption on Cu(111) for the supplied θ=0.04 and θ=1 first-layer systems. Compute average adsorption energy per Li atom, E_ads=(E_system−E_clean−nE_Li)/n, for each endpoint and use the signed difference to establish whether adsorption becomes more or less favorable at full coverage. Develop and test the most plausible physical explanation supported by your calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that average Li adsorption becomes less favorable as the first-layer coverage increases, with lateral interactions in a dense adlayer contributing to the weakening. They further relate this energetic trend to the observed decrease in an apparent deposition-rate coefficient during early deposition; the atomistic task concerns the vacuum-slab adsorption energetics.

**Candidate route or mechanism.**
For the first Li layer, examine a coverage-driven change from isolated Li–Cu bonding toward a close-packed fcc-hollow adlayer, where Li–Li interactions and the lattice mismatch between the Li arrangement and Cu(111) may raise the adsorption energy. The authors also consider coverage-dependent electrostatic effects associated with charge transfer between Li and the upper Cu layer.

**Discriminating evidence.**
Compare endpoint adsorption energies and their signed change, and use relaxed geometries and electronic charge analysis to test whether changes in Li–Li spacing, substrate distortion, charge transfer, or other computed observables support the proposed explanation. Supercell or other convergence checks are relevant to distinguishing a coverage effect from residual numerical sensitivity.

# Public inputs and scientific boundaries

All four XYZ files and system_manifest.json under data/inputs are public. They uniquely specify neutral Cu and Li composition, Cartesian coordinates in Å, the p(5×5) in-plane vectors, five Cu layers, 15 Å z vacuum to add/use, bottom two fixed and top three relaxable, fcc-hollow site identity, n=1 and n=25 coverage counts, neutral isolated Li reference, and singlet multiplicity. The scored system is the isolated Cu(111) slab and its specified Li adlayers; do not add a host or solvent. Electrolyte, explicit potential, defects, steps, alloying, and second-layer Li are outside scope. Select and justify the computational method, model chemistry, relaxation, and validation strategy independently.

# Required scientific validation/investigation

Construct a reproducible calculation graph containing clean slab, isolated Li, θ=0.04 and θ=1 energies. Verify identity, periodic cell, atom counts, layer masks, charge and spin. Generate and discriminate plausible explanations for the endpoint difference using computed observables (for example geometry or charge analysis) rather than asserting one. Demonstrate convergence or quantify residual sensitivity for the principal energy difference. Completion requires both endpoint energies, the signed difference, validation diagnostics, and a conclusion with uncertainty/limitations, or a bounded failure report with attempted work. Stop once the fixed endpoints and at least one convergence/sensitivity check or explicit resource limitation have been reported; optional intermediate coverages are not required and must not replace endpoint evaluation.

# Deliverables

Submit report/results.json conforming to the local submission_schema.json. Include method, per-system energies, endpoint adsorption energies with units, trend, independently reasoned explanation, validation evidence, limitations, and conclusion. If computation cannot be completed, use the bounded-failure branch with attempted calculations, missing fields, diagnostics, and an honest limitation; never fabricate values.
