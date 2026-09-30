# Scientific objective

Independently determine the energy relative to the calculated Fermi level of the occupied Au–S hybrid state in the specified SCH3/Au(111) model, and assess whether that state is consistent with a finite-energy direct charge-transfer channel. The scored object is the pDOS feature, not a kinetic rate or a presumed mechanism.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that an occupied Au–S hybrid state in the Au(111) interface supplies a finite-energy electronic threshold relevant to direct charge-transfer chemical interface damping (CID).

**Candidate route or mechanism.**
Search for a hybridized occupied feature formed from sulfur-derived states and the Au atoms bonded to sulfur, and assess whether its spectral onset can support the proposed direct charge-transfer interpretation. Compare that assignment with states dominated by the Au d band.

**Discriminating evidence.**
Use sulfur and bonded-gold projected densities of states aligned to the calculated Fermi level, together with orbital or spatial character and a geometry or model sensitivity check, to distinguish Au–S hybridization from bulk-like Au d states and test the stability of the assignment.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json` and `data/inputs/methanethiol.xyz`. They define neutral methanethiol fragment connectivity, Au(111) lattice constant, 2x2 periodic cell, 12 Au layers, 13 Å vacuum, one adsorbate per four surface Au atoms, two-sided adsorption, and an initially tilted fcc placement. Build all missing slab coordinates deterministically and report the construction convention. The model is periodic and idealized; do not claim it reproduces the full decanethiol SAM, solution, or unknown experimental interface. The measured quantity is the occupied Au–S hybrid pDOS energy relative to EF, in eV.

# Required scientific validation/investigation

Propose and execute an independent computational route that can locate and validate the occupied Au–S hybrid pDOS feature. Disclose relaxation, electronic-structure, projection, charge/spin, convergence, and energy-alignment choices. Generate and discriminate any plausible competing assignments (including bulk Au d states) using explicit spectral, spatial, or orbital evidence. Include at least one sensitivity or independent validation calculation. Completion requires a converged geometry, a documented pDOS extraction, and either a validated feature assignment or a scientifically justified bounded failure. Stop after the target calculation and stated validation are complete; if resources prevent completion, stop and report the exact failed stage, attempted coverage, and limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include methods, structure identity, convergence evidence, candidate/feature discrimination, energy relative to EF, validation, conclusion, and limitations. Do not report an unsupported precision.
