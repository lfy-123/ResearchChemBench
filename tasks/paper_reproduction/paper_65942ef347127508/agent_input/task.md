# Scientific objective

Determine the Gibbs free-energy barrier for axial racemization of the neutral 3a molecule in implicit toluene at 323.15 K. The author hypothesis to test is that a rotation/racemization saddle connects the two enantiomeric minima and gives a barrier consistent with the experimentally measured configurational barrier.

# Public inputs and scientific boundaries

`data/inputs/3a.xyz` and `data/inputs/ent-3a.xyz` are 57-atom XYZ geometries, with element identities and Cartesian coordinates in Å; treat them as neutral closed-shell molecules with the listed atom order. These are endpoint structures only: no transition-state, intermediate, optimized conformer, energy, or other result-bearing structure is supplied. The physical model is one isolated molecule with implicit toluene; no explicit solvent, catalyst, reaction partners, or alternative products are in scope. The measured quantities are stationary-point imaginary frequencies, TS connectivity, and ΔG‡ in kcal/mol at 323.15 K.

# Required scientific validation/investigation

Independently choose and document a computational method and a reproducible search/optimization strategy. Locate or construct a candidate racemization saddle from the two endpoint geometries, then optimize or otherwise validate the two minima and the candidate saddle, calculate frequencies, and establish that each minimum has zero imaginary frequencies and the racemization saddle has exactly one. Use IRC or a scientifically justified equivalent path-following test to show that the saddle connects 3a and ent-3a. Construct ΔG‡ explicitly as the saddle free energy minus the lower connected minimum, state the unit conversion and temperature convention, and report sensitivity or limitations caused by the SI's inconsistent temperature labels. Completion requires both endpoint classifications, a candidate-saddle classification, connectivity evidence, an explicit barrier calculation, and a conclusion about agreement with experiment. Stop after these checks are complete; if a check cannot be completed, report bounded failure with the failed check, evidence, and any results that were established, without inventing values.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For success, include the chosen method and search strategy, optimization/frequency evidence for both endpoints and the discovered saddle, IRC evidence, neutral per-structure identities, free energies and formula, barrier, experimental comparison, uncertainty/limitations, and a concise conclusion. For bounded failure, identify the failed validation step and provide evidence plus any scientifically established partial results; do not fabricate success-only numbers or structures. Do not claim global mechanistic coverage from this single modeled pathway.
