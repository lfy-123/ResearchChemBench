# Scientific objective

Compute and validate the product-minus-reactant Gibbs free energy for the supplied neutral-singlet Mo(VI) complex 1 and neutral-singlet Mo–NO aqua complex 3. The authors qualitatively propose an inner-sphere hydroxylamine route with electron transfer followed by proton-transfer/coordination chemistry; independently test this hypothesis without assuming unprovided intermediates.

# Public inputs and scientific boundaries

`data/inputs/reactant_1.xyz` and `data/inputs/product_3.xyz` are complete Cartesian geometries in Angstrom with authoritative atom order. Both objects are neutral singlets. Use only these inputs and your own calculations. Choose and disclose a defensible computational model, solvent treatment, temperature and standard state. Score the endpoint free-energy difference, not a hidden transition-state structure.

# Required scientific validation/investigation

For both named endpoints, obtain a converged energy or document a bounded failure; report charge, multiplicity, convergence and frequency evidence if frequencies are computed. Verify the optimized product retains the supplied chemical identity. Report product-minus-reactant Gibbs free energy in kcal/mol and one mechanistic diagnostic that tests the qualitative hypothesis. Completion requires both endpoint records, validation evidence, energy difference and limitations. Stop after one converged endpoint protocol plus one diagnostic; do not claim a full pathway without locating and validating it.

# Deliverables

Submit `report/results.json` using the schema. Include endpoint records, method, thermochemical convention, energy difference, diagnostic, conclusion and limitations, or a truthful bounded-failure branch.
