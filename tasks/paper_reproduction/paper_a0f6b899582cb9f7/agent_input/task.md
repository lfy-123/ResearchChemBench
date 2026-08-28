# Scientific objective

Determine the isolated neutral singlet molecule's optimized geometry, dipole magnitude, full electric quadrupole tensor, and the component along the molecular pi-pi stacking axis for 2,5-di(thiophen-2-yl)pyrazine (M3). The authors' qualitative hypothesis is that a planar conjugated structure with an intramolecular N···S conformational lock can provide a large stacking-axis quadrupole while the net dipole cancels; independently plan calculations that test this hypothesis. Do not assume any author numerical result.

# Public inputs and scientific boundaries

Use `data/inputs/m3_identity.json` and `data/inputs/m3.xyz`. They define C12H8N2S2, neutral charge, singlet multiplicity, connectivity, atom order and an initial coordinate frame. The initial coordinates are not a reference geometry. The object is one isolated molecule in vacuum; no crystal, solvent, blend, polymer, or device calculation is requested. Report tensor units, origin, axis convention, and how the stacking axis was selected. Do not use the paper, SI or general web.

# Required scientific validation/investigation

Choose and justify an electronic-structure method capable of geometry optimization and multipole analysis. Optimize from the supplied structure and, if relevant, additional distinct conformers; deduplicate by connectivity and geometry. Demonstrate convergence and validate a minimum with frequencies or an explicitly justified alternative. Quantify planarity, the shortest chemically relevant N···S distance, dipole magnitude, and all quadrupole components in one declared molecular frame. Completion requires a converged, validated structure and a reproducible extraction of the requested observables, or a documented bounded failure with attempted methods and remaining limitation. Stop after the selected conformer set is converged under your stated criterion and no newly generated starting conformer changes the qualitative structural assignment, or report why that condition could not be met.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, software, convergence/validation evidence, geometry metrics, tensor, axis convention, and a conclusion relating the observed structure and multipoles to the stated qualitative hypothesis. Numeric values must be your calculations, not copied references.
