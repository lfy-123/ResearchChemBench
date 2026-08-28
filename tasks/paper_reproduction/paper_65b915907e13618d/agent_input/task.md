# Scientific objective

Determine the gas-phase ground-state coordination geometry of the four-coordinate Cu(I) cation in [Cu(L7)]BF4, where L7 is the hexyl-bridged bis(iminophosphine) Hex-bisImP. Test the authors' qualitative hypothesis that the flexible C6H12 bridge permits partial relaxation of the N-donor bite geometry while retaining a distorted Cu(P,N)2 coordination environment. Report Cu–P and Cu–N bond lengths and the six labeled donor-centered Cu angles.

# Public inputs and scientific boundaries

Use `data/inputs/complex_7a_identity.json` and the accompanying SMILES file. They uniquely define L7 connectivity, one Cu(I), total charge +1, singlet multiplicity, donor labels P1/N1 and P2/N2, and exclusion of BF4− from the bonded model. You may generate 3-D conformers and choose a defensible initial arrangement, but must preserve connectivity, protonation, charge, multiplicity and donor identities. The scored state is the optimized electronic ground-state structure of this cation in the gas phase, matching the source calculation. Report distances in Å and angles in degrees; do not report counterion contacts as coordination bonds.

# Required scientific validation/investigation

Independently plan and execute a geometry optimization and a minimum verification using a defensible quantum-chemical method. The authors' qualitative route is only a hypothesis: your method, functional, basis, environment, conformer handling and execution order must be chosen and disclosed independently. Generate at least one chemically sensible starting conformer; if multiple starting conformers are used, deduplicate equivalent minima and retain their provenance. A calculation is complete when the selected structure is converged under the stated criteria, its donor labels are unambiguous, and a vibrational analysis reports no imaginary frequencies, or when an alternative minimum-validation procedure is justified and explicitly disclosed. Compare against the task's fixed labeled observables and explain method/conformer sensitivity. Stop when the converged minimum and validation evidence are documented;.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the selected geometry observables, validation status/evidence, method and convergence details, starting-structure provenance, and a concise conclusion addressing the qualitative partial-relaxation hypothesis. Include enough coordinate or geometry-file provenance for another researcher to identify P1/N1/P2/N2 and reproduce the measurements.
