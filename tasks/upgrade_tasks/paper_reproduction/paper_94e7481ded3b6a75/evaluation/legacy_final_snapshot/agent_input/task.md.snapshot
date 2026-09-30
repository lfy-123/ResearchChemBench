# Scientific objective

Independently test the paper's qualitative claim that the electronic structure of the B-phenyl BN-anthracene PBNA can be characterized quantitatively by frontier-orbital and thermochemical calculations. Compute the PBNA HOMO and LUMO energies and the electronic energy, zero-point energy, Gibbs free energy, and entropy for the specified isolated molecule. The author context is that PBNA is the B-phenyl reference used to compare B-functionalized BN-anthracenes and that its frontier orbitals are described as mainly delocalized over the BN-anthracene scaffold; independently test this context rather than assuming it.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors use PBNA as a B-phenyl reference and interpret its frontier-orbital distribution in relation to the BN-anthracene scaffold. The relevant claim is qualitative and should be tested from the supplied isolated molecule rather than assumed.

**Candidate route or mechanism.**
Characterize PBNA through one converged neutral-singlet stationary-point calculation, then relate the computed HOMO and LUMO energies and spatial distributions to the scaffold-based interpretation. Treat the orbital localization as a property to verify, not as a fixed outcome.

**Discriminating evidence.**
Use the same validated structure for the six requested orbital and thermochemical observables, and support the localization interpretation with orbital populations, visualizations, or another reproducible spatial analysis with the method and spatial-analysis definition reported explicitly.

# Public inputs and scientific boundaries

The research object is the molecule named PBNA, formula C24H22B2N2, represented by the 50 Cartesian atoms in `data/inputs/pbna.xyz`. The first line is the atom count and the second is a comment; coordinates are in angstrom and element symbols are explicit. Use charge 0 and multiplicity 1. `data/inputs/system.json` specifies the observables, 298.15 K thermochemical reporting temperature, no solvent, and an isolated-molecule boundary. Do not use crystal packing, counterions, explicit solvent, or excited-state dynamics. The measured quantities are HOMO/LUMO orbital energies in eV; E, ZPE, and G in hartree; and total entropy in cal mol−1 K−1. You may choose software implementing the primary comparison protocol below and supplementary analysis methods; report them exactly. The primary absolute energies and thermochemistry are protocol-specific.

Primary comparison protocol: neutral singlet PBNA, gas-phase B3LYP/6-31G(d), with geometry optimization and harmonic frequency/thermochemistry at 298.15 K and 1 atm. Extract electronic energy, unscaled zero-point energy, electronic-plus-thermal Gibbs energy, entropy and frontier orbital energies for the same validated structure. Other methods are supplementary comparisons and do not replace these primary absolute-energy observables. Orbital pictures or a defined population analysis may support localization; squared AO coefficients alone are not normalized atomic/fragment populations.

# Required scientific validation/investigation

Parse and preserve the explicit element identity and atom count, verify the neutral-singlet electron count, and document any geometry preparation. Optimize the structure or otherwise define the stationary structure used for properties. Validate optimization convergence and establish whether the final structure is a minimum by a frequency calculation or an equivalent defensible vibrational test; report the number of imaginary frequencies and any failure. Compute all six requested observables on the same identified final structure and report units. Compare the frontier-orbital localization qualitatively using an orbital population/visualization analysis if available, clearly distinguishing computed evidence from interpretation. The investigation is complete only when the structure identity, method, convergence, stationary-point validation, all six observables, and a conclusion supported by those observables are present.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include a validation record, method and structure identity, all six values on success, or a truthful `status` of `bounded_failure` with diagnostics and partial values when the required calculation cannot be completed. Include a concise conclusion about the PBNA frontier-orbital distribution from the computed orbital evidence, plus paths to logs or output files when available.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
