# Scientific objective

Independently test the qualitative proposal that hydrogen-radical-mediated cleavage of an L-cystine disulfide regenerates thiol sites. Compute the standard reaction Gibbs energy ΔG (kcal/mol), and identify and validate the relevant reactant and cleavage stationary structure. The object is isolated neutral L,L-cystine; no paper geometry, method, or answer is provided.

# Public inputs and scientific boundaries

`data/inputs/l_cystine.json` uniquely defines neutral singlet L,L-cystine. Use it as the disulfide reactant. Define hydrogen/proton stoichiometry, products, charge/multiplicity, standard state, and solvation in the report. The boundary excludes explicit straw, PEI, periodic surfaces, and experimental solid structure. Report ΔG in kcal/mol plus every state structure and frequency evidence. Do not use the paper, SI, or general web.

# Required scientific validation/investigation

Generate reproducible conformers and cleavage transition-state candidates, retain identities, deduplicate by an explicit structural criterion, and state advancement and stopping rules. For every advanced state report convergence, charge/multiplicity, bonding interpretation and frequencies; minima have no imaginary frequencies and a transition structure has one chemically relevant imaginary mode. Assemble ΔG from reported components and disclose model, standard-state and solvation choices. Stop when new starts reproduce known states or a transparent resource/search limit is reached. If no valid transition state is found, submit bounded failure with attempted coverage and limitations; do not fabricate ΔG.

# Deliverables

Write `report/results.json` using `submission_schema.json`, including status, reaction definition, state/candidate records, validation evidence, ΔG when available, method, coverage, stopping condition, uncertainty, and conclusion. For `bounded_failure`, set `delta_g_kcal_mol` to `null` and report the attempted coverage and limitations; do not invent a numerical result.
