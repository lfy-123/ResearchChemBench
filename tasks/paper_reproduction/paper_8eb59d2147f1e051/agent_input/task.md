# Scientific objective

Test the authors' qualitative hypothesis that Ni-containing Fe2NiSe4 provides a more kinetically favorable surface for Li–S conversion than Fe3Se4. Independently construct periodic surface models and determine the Li2S decomposition barrier on each host. Report the barrier (electronic energy, eV), the host-to-host difference and ordering, and the sulfur-reduction step your pathway represents as rate limiting. The hypothesis is qualitative only: do not assume any published geometry, software, model chemistry, or numerical result.

# Public inputs and scientific boundaries

`data/inputs/system_definition.json` identifies Fe3Se4 by ICSD 96-153-7571 and Fe2NiSe4 by ICSD 97-004-2505. Li2S is a neutral endpoint species; report the chosen spin multiplicity. Build periodic slabs from those records. rGO, solvent, electrolyte and finite-temperature cell performance are outside scope. For each host, define an intact adsorbed Li2S initial state and a same-atom, same-charge adsorbed decomposition final state. The barrier is the maximum energy on the validated minimum-energy path minus the initial-state energy. A low-index surface/termination and slab thickness must be selected from the records and explicitly named; the public input does not select a winning surface or endpoint geometry.

# Required scientific validation/investigation

Generate a finite, explicitly enumerated set of low-index terminations and chemically distinct adsorption placements for each host, deduplicate equivalent candidates, and record the reduction/advancement rule. Relax the retained initial and final states and validate that they have the stated stoichiometry, charge, surface identity, convergence, and no unexplained imaginary mode or endpoint instability. Compute and validate a minimum-energy path for each host; report image count, path convergence, maximum-energy image and endpoint energies. Compare at least one primary validated model per host and report all discarded/failed candidates and coverage. Completion requires two host barriers, a reproducible identity for each primary model, and enough convergence/path evidence for another researcher to rerun the comparison. Stop when the enumerated termination/placement set has been exhausted under the declared low-index bound, or report bounded failure with the exact unresolved stage and coverage; do not claim a unique mechanism if that condition was not met.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include model identities, candidate-generation and validation evidence, barriers in eV, ordering/difference, rate-limiting-step statement, uncertainty/limitations, and a truthful completion status. A bounded-failure branch is allowed only when the corresponding unresolved stage, attempted candidates and available measurements are supplied.
