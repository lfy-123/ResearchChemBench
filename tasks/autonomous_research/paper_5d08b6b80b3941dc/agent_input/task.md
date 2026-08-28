# Scientific objective

Determine, from first-principles computational investigation, whether a chemically plausible low-energy radical elementary step connects methane and a bisulfate radical in concentrated sulfuric acid, and quantify the best validated solution-phase free-energy barrier for that step. Identify the product-side radical chemistry supported by your calculations without assuming a published mechanism.

# Public inputs and scientific boundaries

Use `data/inputs/system_specification.json`. It uniquely fixes methane, neutral doublet HSO4•, neutral singlet H2SO4, the 98% sulfuric-acid continuum, 298.15 K, and the elementary methane-functionalization scope. You may generate conformers, complexes, and transition-state guesses. Do not use the paper, SI, general web, or hidden source coordinates. Do not claim experimental kinetics. State charge, multiplicity, atom mapping, and standard-state convention.

# Required scientific validation/investigation

Propose and discriminate plausible elementary explanations within the stated reactant/product boundary; do not invent a discovery story beyond calculations. Generate and deduplicate a finite set of candidate complexes and transition structures, retain candidate identity and provenance, and advance only candidates with chemically conserved atoms and spin. Validate minima by zero imaginary frequencies, candidate TSs by exactly one imaginary frequency assigned to the bond-making/bond-breaking coordinate, and connectivity by IRC or an equivalent displacement analysis. Refine the best validated candidate consistently and quantify sensitivity to conformer, method, and treatment choices. Completion requires either a validated barrier and product-side assignment or a bounded-failure report explaining why validation could not be achieved. Stop when the declared candidate-generation strategy is exhausted and further guesses are duplicates or fail the validation tests; report search coverage and limitations.

# Deliverables

Write `report/results.json` containing the proposed hypotheses, candidate identities, validation evidence, selected barrier in kcal/mol when available, product-side structure, uncertainty, and conclusion. The status must be `completed` or a truthful bounded-failure value with candidate-specific diagnostics. Include coordinates or unambiguous structure identifiers sufficient for checking. Do not copy source-paper text or infer a result from the task wording.
