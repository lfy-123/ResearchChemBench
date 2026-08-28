# Scientific objective

Compute and validate the DMSO vertical absorption maximum and relaxed-S1-to-S0 emission maximum of neutral compound 3i, and determine from the calculated electronic states whether the molecule exhibits donor-to-acceptor intramolecular charge transfer. The research object is 5-(1-benzyl-2,6-bis((E)-2-(dimethylamino)vinyl)pyridin-4(1H)-ylidene)-1,3-diethyl-2-thioxodihydropyrimidine-4,6(1H,5H)-dione.

# Public inputs and scientific boundaries

Use `data/inputs/compound_3i_optimized.xyz`, a 71-atom Cartesian geometry in Å. The file fixes atom order and elements. Treat the molecule as neutral closed-shell singlet in implicit DMSO near 298 K and 1 atm; no explicit solvent, aggregate, crystal, or experimental spectrum is included. You may generate and compare alternative conformers or starting structures, but must retain the molecular identity and disclose transformations. Measure the dominant vertical S0 absorption maximum and vertical S1→S0 emission maximum after a defensible S1 relaxation. No author route, paper method, target value, ranking, or mechanism answer is provided.

# Required scientific validation/investigation

Design and state a reproducible electronic-structure investigation: model chemistry, basis, solvation, state roots, peak extraction, convergence, and software. Validate the ground state as stationary (frequency/no-imaginary-mode analysis or justified equivalent), identify and validate the absorption state, relax and validate the relevant singlet excited state, and identify the emission transition. If multiple plausible states, conformers, or methods arise, generate, deduplicate, compare, and retain them with identity and validation context; report coverage and why further search would or would not change the conclusion. Completion requires both endpoint observables or a fully documented bounded failure, validation evidence for every advanced state, and a limitation statement. Stop after the declared protocol converges and state/conformer conclusions are stable under one justified sensitivity check; otherwise stop with explicit unresolved alternatives and coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus referenced logs/structures. Report independent numeric maxima or bounded failure, method and uncertainty, state validation, electronic-character evidence, conclusion, coverage, and limitations. Do not claim an unperformed calculation.
