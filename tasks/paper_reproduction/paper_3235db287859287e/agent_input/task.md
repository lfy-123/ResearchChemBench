# Scientific objective

Determine, for the explicitly defined neutral 3aa molecule, the 298 K Gibbs free-energy difference ΔG(E) − ΔG(Z) between its Z and E alkene stereoisomers, identify the lower-free-energy stereoisomer, and test whether each optimized structure is a valid minimum. The authors qualitatively propose that steric congestion favors one alkene arrangement; independently test this hypothesis.

# Public inputs and scientific boundaries

Use `data/inputs/3aa_stereoisomers.json`. It defines methyl 3-phenyl-2-((phenylsulfinyl)methyl)acrylate (formula C17H16O3S), charge 0, multiplicity 1, and authoritative isomeric SMILES and configuration labels for objects `3aa_Z` and `3aa_E`. The research object is only these two molecular stereoisomers. The measured quantity is their signed relative Gibbs free energy at a declared temperature and standard-state convention, in kcal/mol. Do not report reaction yield, electrochemical potential, rate, or a full mechanism.

# Required scientific validation/investigation

Generate and optimize at least one structure for each named object, choosing and briefly justifying a defensible common computational protocol. Verify connectivity and assigned E/Z geometry after optimization; perform vibrational analysis and report that each accepted structure has zero imaginary frequencies. Use the same charge, multiplicity, solvent treatment, temperature, and energy convention for both. If multiple conformers are explored, deduplicate them by structural identity and state how many were searched and how the retained conformer was selected. The calculation is complete when both named objects have either validated minima and a signed ΔG(E)−ΔG(Z), or a truthful bounded-failure record identifying which validation failed. Stop after both objects are validated or after reasonable attempts are exhausted; do not claim a global conformer minimum without documenting coverage. Interpret any preference only within this model boundary.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include the protocol and its rationale, object-by-object validation evidence (including geometry/configuration and vibrational results), energies/free energies and units, signed difference, favored object or bounded-failure status, conformer/search coverage, and limitations. Include enough command/output or log references for an evaluator to verify the process claims.
