# Scientific objective

Determine the gas-phase ground-state coordination geometry of the four-coordinate Cu(I) cation in [Cu(L7)]BF4, where L7 is the hexyl-bridged bis(iminophosphine) Hex-bisImP. Quantify the Cu–P and Cu–N bond lengths and six labeled donor-centered Cu angles, and decide what the computed geometry supports about steric relaxation in the flexible bridge.

# Public inputs and scientific boundaries

Use `data/inputs/complex_7a_identity.json` and the accompanying SMILES file. They uniquely define L7 connectivity, one Cu(I), total charge +1, singlet multiplicity, donor labels P1/N1 and P2/N2, and exclusion of BF4− from the bonded model. You may generate 3-D conformers and choose any defensible computational model, but must preserve connectivity, protonation, charge, multiplicity and donor identities. The scored state is the optimized electronic ground-state structure of this cation in the gas phase, matching the source calculation. Report distances in Å and angles in degrees; do not report counterion contacts as coordination bonds.

# Required scientific validation/investigation

Independently formulate a computational plan, execute a geometry optimization, and validate the selected structure as a minimum. Generate at least one chemically sensible starting conformer; if multiple conformers are explored, deduplicate equivalent minima and retain provenance. The investigation is complete when the selected structure is converged under stated criteria, donor labels are unambiguous, and a vibrational analysis reports no imaginary frequencies, or when a justified alternative minimum-validation procedure is disclosed. Report method sensitivity or conformer coverage rather than silently assuming uniqueness. Stop when the validated minimum and all requested labeled observables are documented;. Do not infer an author route or claim discovery of a mechanism beyond the computed structure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include selected geometry observables, validation status/evidence, method and convergence details, starting-structure provenance, and a concise evidence-based conclusion about steric relaxation. Include coordinate or geometry-file provenance sufficient to identify P1/N1/P2/N2 and reproduce measurements.
