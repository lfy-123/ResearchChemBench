# Scientific objective

Determine the standard reaction Gibbs energy ΔG (kcal/mol) for thiol-site regeneration through cleavage of the disulfide bond in neutral L,L-cystine under an explicitly defined hydrogen/proton convention. Identify and validate relevant endpoint and stationary structures, and state the isolated-molecule interpretation boundary.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that hydrogen radicals regenerate sulfhydryl sites by cleaving oxidized disulfide linkages.

**Candidate route or mechanism.**
Consider hydrogen-radical attack on the C–S–S–C linkage as a candidate route to C–SH formation. The authors examine a cystine reactant and a candidate stationary structure associated with S–S bond breaking.

**Discriminating evidence.**
The authors use dispersion-corrected DFT with continuum solvation to optimize molecular structures and refine electronic energies with a larger basis. They assemble reaction Gibbs energies from electronic energies, thermal corrections, standard-state corrections, and the hydrogen/proton solvation convention to assess the regeneration proposal.

# Public inputs and scientific boundaries

`data/inputs/l_cystine.json` uniquely defines neutral singlet L,L-cystine. Define stoichiometry, products, charge/multiplicity, standard state and solvation before calculation. The scored system is the isolated molecule; do not add a host matrix or periodic surface. Report ΔG in kcal/mol and validated structures. Do not use the paper, SI, or general web.

# Required scientific validation/investigation

Generate and test your own plausible explanations or pathways and discriminate alternatives where needed. Generate, identify and deduplicate conformer and stationary-point candidates; state generation, advancement, validation and stopping rules. Report convergence and frequencies for every advanced state; validate minima and one-mode transition structures, or provide bounded failure. Disclose thermochemical components, model, standard state, solvation, uncertainty and coverage. Stop when new starts reproduce known states or a transparent resource/search limit is reached.

# Deliverables

The calculation is complete when the reaction convention is explicit, all advanced states have auditable optimization/frequency evidence, and the search has either converged to reproducible states with ΔG assembled from stated components or documented a bounded failure. Write `report/results.json` conforming to the local `submission_schema.json`, including reaction definition, state/candidate records, validation evidence, ΔG when available, method, coverage, stopping condition, uncertainty, and final conclusion. For `bounded_failure`, set `delta_g_kcal_mol` to `null` and report attempted coverage and limitations; do not invent a numerical result.
