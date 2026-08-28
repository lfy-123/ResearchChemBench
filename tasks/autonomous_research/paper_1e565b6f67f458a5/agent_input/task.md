# Scientific objective

Autonomously determine the standard reaction Gibbs energy ΔG (kcal/mol) for thiol-site regeneration through cleavage of the disulfide bond in neutral L,L-cystine by a hydrogen-radical/proton convention. Identify and validate relevant endpoint and stationary structures, and state the isolated-molecule interpretation boundary.

# Public inputs and scientific boundaries

`data/inputs/l_cystine.json` uniquely defines neutral singlet L,L-cystine. No author mechanism, candidate transition structure, paper method, or numerical result is supplied. Define stoichiometry, products, charge/multiplicity, standard state and solvation before calculation. Exclude explicit straw, PEI, and periodic surfaces. Report ΔG in kcal/mol and validated structures. Do not use the paper, SI, or general web.

# Required scientific validation/investigation

Propose plausible explanations and discriminate alternatives where needed. Generate, identify and deduplicate conformer and stationary-point candidates; state generation, advancement, validation and stopping rules. Report convergence and frequencies for every advanced state; validate minima and one-mode transition structures, or provide bounded failure. Disclose thermochemical components, model, standard state, solvation, uncertainty and coverage. Stop when new starts reproduce known states or a transparent resource/search limit is reached.

# Deliverables

The calculation is complete when the reaction convention is explicit, all advanced states have auditable optimization/frequency evidence, and the search has either converged to reproducible states with ΔG assembled from stated components or documented a bounded failure. Write `report/results.json` using `submission_schema.json`, including hypotheses, reaction definition, state/candidate records, validation evidence, ΔG when available, method, coverage, stopping condition, uncertainty, and final conclusion. For `bounded_failure`, set `delta_g_kcal_mol` to `null` and report attempted coverage and limitations; do not invent a numerical result.
