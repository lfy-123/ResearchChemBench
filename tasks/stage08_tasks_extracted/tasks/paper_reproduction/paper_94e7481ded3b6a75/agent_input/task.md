# Scientific objective

For the uniquely specified isolated molecule PBNA, independently compute and interpret its frontier-orbital energies and thermochemical properties. Determine whether the resulting evidence supports a defensible statement about the spatial distribution of its HOMO and LUMO and quantify the result without relying on an external paper or a preselected computational protocol.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors use PBNA as a B-phenyl reference and interpret its frontier-orbital distribution in relation to the BN-anthracene scaffold. The relevant claim is qualitative and should be tested from the supplied isolated molecule rather than assumed.

**Candidate route or mechanism.**
Characterize PBNA through one converged neutral-singlet stationary-point calculation, then relate the computed HOMO and LUMO energies and spatial distributions to the scaffold-based interpretation. Treat the orbital localization as a property to verify, not as a fixed outcome.

**Discriminating evidence.**
Use the same validated structure for the six requested orbital and thermochemical observables, and support the localization interpretation with orbital populations, visualizations, or another reproducible spatial analysis while reporting method and model limitations.

# Public inputs and scientific boundaries

The research object is PBNA, formula C26H18B2N2, represented by the 50 Cartesian atoms in `data/inputs/pbna.xyz`. The first line is the atom count and the second is a comment; coordinates are in angstrom and element symbols are explicit. Use charge 0 and multiplicity 1. `data/inputs/system.json` specifies HOMO/LUMO energies in eV; electronic energy, zero-point energy and Gibbs free energy in hartree; and entropy in cal mol−1 K−1 at 298.15 K. The boundary is one isolated gas-phase molecule with no solvent, crystal packing, counterion, or excited-state dynamics. Choose and justify an executable method/software and report it exactly. No author route, candidate ranking, target value, or expected direction is supplied.

# Required scientific validation/investigation

Verify the explicit atom list, atom count, charge, multiplicity, and electron count before calculation. Plan and execute a defensible geometry/property workflow, validate convergence, and establish whether the final structure is a minimum by a frequency calculation or an equivalent vibrational test. Obtain all six observables from the same identified structure, and use orbital populations, plots, or another reproducible analysis to support or qualify any HOMO/LUMO localization statement. The investigation is complete when the method, structure identity, convergence, stationary-point result, all six observables, evidence for the localization interpretation, and at least one limitation are reported. Stop after one converged validated stationary-point workflow and a documented sensitivity/limitation assessment; if the workflow fails, stop and report a bounded failure with diagnostics and partial outputs rather than inventing values.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. On success provide all six values, validation evidence, the chosen method, localization conclusion, and limitations. On bounded failure provide diagnostics, validation status, any truthful partial values, and the next scientifically justified step that was not executed. Include output/log paths when available.
