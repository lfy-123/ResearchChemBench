# Scientific objective

For the uniquely specified isolated molecule PBNA, independently compute and interpret its frontier-orbital energies and thermochemical properties. Determine whether the resulting evidence supports a defensible statement about the spatial distribution of its HOMO and LUMO and quantify the result using the public primary comparison protocol below without relying on an external paper.

# Public inputs and scientific boundaries

The research object is PBNA, formula C24H22B2N2, represented by the 50 Cartesian atoms in `data/inputs/pbna.xyz`. The first line is the atom count and the second is a comment; coordinates are in angstrom and element symbols are explicit. Use charge 0 and multiplicity 1. `data/inputs/system.json` specifies HOMO/LUMO energies in eV; electronic energy, zero-point energy and Gibbs free energy in hartree; and entropy in cal mol−1 K−1 at 298.15 K. The boundary is one isolated gas-phase molecule with no solvent, crystal packing, counterion, or excited-state dynamics. Independently plan the preparation, execution and analysis; choose executable software implementing the primary protocol and report it exactly. No author-specific candidate ranking, target value, or expected direction is supplied.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

Primary comparison protocol: neutral singlet PBNA, gas-phase B3LYP/6-31G(d), with geometry optimization and harmonic frequency/thermochemistry at 298.15 K and 1 atm. Extract electronic energy, unscaled zero-point energy, electronic-plus-thermal Gibbs energy, entropy and frontier orbital energies for the same validated structure. Other methods are supplementary comparisons and do not replace these primary absolute-energy observables. Orbital pictures or a defined population analysis may support localization; squared AO coefficients alone are not normalized atomic/fragment populations.

# Required scientific validation/investigation

Verify the explicit atom list, atom count, charge, multiplicity, and electron count before calculation. Plan and execute a defensible geometry/property workflow, validate convergence, and establish whether the final structure is a minimum by a frequency calculation or an equivalent vibrational test. Obtain all six observables from the same identified structure, and use orbital populations, plots, or another reproducible analysis to support or qualify any HOMO/LUMO localization statement. The investigation is complete when the method, structure identity, convergence, stationary-point result, all six observables, evidence for the localization interpretation are reported.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. On success provide all six values, validation evidence, the chosen method, localization conclusion. On bounded failure provide diagnostics, validation status, any truthful partial values, and the next scientifically justified step that was not executed. Include output/log paths when available.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
