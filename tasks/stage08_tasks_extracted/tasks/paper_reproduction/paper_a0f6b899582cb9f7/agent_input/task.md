# Scientific objective

Independently determine the isolated neutral singlet molecule's optimized geometry, dipole magnitude, full electric quadrupole tensor, and the physically meaningful molecular stacking-axis component for 2,5-di(thiophen-2-yl)pyrazine (M3). Establish whether its optimized structure is planar and whether a short intramolecular N···S contact is present, then state what these calculations do and do not support about its multipolar character.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that an intramolecular N···S conformational lock favors a planar conjugated structure, with cancellation of opposing molecular dipoles compatible with a substantial quadrupole along the π–π stacking direction.

**Candidate route or mechanism.**
Consider N···S contact formation as a candidate explanation for conformational planarity and equal, oppositely directed local dipoles as a candidate explanation for dipole cancellation. The authors investigate this structural and electrostatic picture through density-functional geometry optimization and molecular multipole analysis.

**Discriminating evidence.**
The authors use optimized molecular planarity and the N···S separation relative to the sum of van der Waals radii to assess the proposed conformational lock. Computed dipole magnitude and quadrupole components in a molecular frame, with a component assigned to the π–π stacking direction, test the proposed multipolar description.

# Public inputs and scientific boundaries

Use `data/inputs/m3_identity.json` and `data/inputs/m3.xyz`. They define C12H8N2S2, neutral charge, singlet multiplicity, connectivity, atom order and an initial coordinate frame. The coordinates are starting values only. The system is one isolated molecule in vacuum; keep calculations within this molecular boundary. Report tensor units, origin, axis convention, and how the stacking axis was selected. Do not use the paper, SI or general web.

# Required scientific validation/investigation

Generate and test your own explanations for the molecular structure and multipolar character. Choose and justify an electronic-structure method capable of geometry optimization and multipole analysis. Optimize from the supplied structure and, if relevant, additional distinct conformers; deduplicate by connectivity and geometry. Demonstrate convergence and validate a minimum with frequencies or an explicitly justified alternative. Quantify planarity, the shortest chemically relevant N···S distance, dipole magnitude, and all quadrupole components in one declared molecular frame. Completion requires a converged, validated structure and a reproducible extraction of the requested observables, or a documented bounded failure with attempted methods and remaining limitation. Stop after the selected conformer set is converged under your stated criterion and no newly generated starting conformer changes the qualitative structural assignment, or report why that condition could not be met.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, software, convergence/validation evidence, geometry metrics, tensor, axis convention, and a conclusion based only on your independent calculations. Numeric values must be your calculations, not copied references.
