# Scientific objective

For the supplied neutral singlet Z-cAAC^Cy molecule, independently determine the signed 300 K Gibbs free-energy difference ΔG = G_coplanar − G_perpendicular between the two supplied conformational starting structures. Report the two free energies, the subtraction convention, and the scientific interpretation of the relative stability. This is a direct computational investigation; do not invent an experimental or mechanistic discovery story.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors use this comparison to assess whether the coplanar and perpendicular conformers of the mononuclear zincafluorene Z-cAAC^Cy complex have nearly equivalent conformational stability. They also interpret dispersion interactions as potentially influencing the conformational preference.

**Candidate route or mechanism.**
Treat the two supplied arrangements as competing S0 conformers of the same neutral singlet molecule and test their relative harmonic Gibbs free energies after independent geometry optimization. A dispersion-inclusive primary calculation is a relevant candidate treatment, with a corresponding no-dispersion comparison as optional sensitivity context.

**Discriminating evidence.**
The claim is distinguished by separately optimized geometries, vibrational analyses establishing local minima, consistent 300 K thermal free energies, and the signed difference G_coplanar − G_perpendicular. Structural overlays, close-contact inspection, and a method sensitivity comparison can help interpret any dispersion-related change, but are secondary to the primary endpoint.

# Public inputs and scientific boundaries

`data/inputs/perpendicular_zcaac_cy.xyz` and `data/inputs/coplanar_zcaac_cy.xyz` are complete Cartesian coordinate files for the two structures to be compared. The files explicitly contain the same neutral Zn/C/H/N molecular system; use charge 0 and singlet multiplicity unless input validation documents a contradiction. The physical boundary is the isolated molecule in its singlet ground state. The measurement boundary is the harmonic/standard-state Gibbs free-energy difference at 300 K for these two starting structures. No crystal packing, solvent population, barrier, or unseen conformer is part of the required endpoint.

# Required scientific validation/investigation

Choose and document a defensible computational route without relying on any undisclosed paper protocol. Check both files for identity and atom-count consistency, optimize or establish each structure as a stationary point, and report vibrational evidence. Treat a structure as a validated minimum only if no imaginary frequencies are found; if resources or convergence prevent this, provide a bounded-failure branch with diagnostics and do not claim a definitive ΔG. Compute consistent 300 K Gibbs free energies and the signed difference G_coplanar − G_perpendicular. Completion means both named structures have auditable calculations and the difference is reported, or a scientifically specific bounded failure explains why not. Stop after this fixed two-structure comparison; optional method sensitivity must be labeled separately.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include unique structure labels, input validation, chosen method and thermal conventions, per-structure stationary-point and free-energy records, ΔG when available, uncertainty/limitations, and a conclusion tied to the computed comparison. Keep all object-specific evidence associated with the corresponding named structure.
