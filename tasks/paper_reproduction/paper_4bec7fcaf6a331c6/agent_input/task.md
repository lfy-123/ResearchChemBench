# Scientific objective

Determine, by an independently planned periodic electronic-structure calculation, the energy relative to the calculated Fermi level of the occupied Au–S hybrid state in the specified SCH3/Au(111) model. Test the authors' qualitative hypothesis that this occupied hybrid state provides the finite-energy electronic threshold relevant to direct charge-transfer CID. The scored object is the pDOS feature, not a kinetic rate.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json` and `data/inputs/methanethiol.xyz`. They define neutral methanethiol fragment connectivity, Au(111) lattice constant, 2x2 periodic cell, 12 Au layers, 13 Å vacuum, one adsorbate per four surface Au atoms, two-sided adsorption, and an initially tilted fcc placement. Build all missing slab coordinates deterministically and report the construction convention. The model is periodic and idealized; do not claim it reproduces the full decanethiol SAM, solution, or unknown experimental interface. The measured quantity is the occupied Au–S hybrid pDOS energy relative to EF, in eV.

# Required scientific validation/investigation

Plan and execute a defensible relaxation followed by DOS/pDOS analysis using methods you choose and disclose. Validate force/energy convergence, preservation or relaxation of the adsorption-site identity, charge and spin treatment, k-point/cell adequacy, and projection/EF alignment. Identify the candidate hybrid feature by an explicit reproducible rule and distinguish it from the Au d-band. Include at least one sensitivity or independent validation calculation. Completion requires a converged geometry, a documented pDOS extraction, and either a validated feature assignment or a scientifically justified bounded failure. Stop after the target calculation and the stated validation are complete; if resources prevent completion, stop and report the exact failed stage, attempted coverage, and limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include methods, structure identity, convergence evidence, pDOS feature extraction, energy relative to EF, validation, conclusion, and limitations. Do not report an unsupported precision.
