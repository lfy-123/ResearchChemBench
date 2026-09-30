# Scientific objective

Determine, from first-principles computational investigation, whether a chemically plausible low-energy radical elementary step connects methane and a bisulfate radical in concentrated sulfuric acid, and quantify the best validated solution-phase free-energy barrier for that step. Identify the product-side radical chemistry supported by your calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that bisulfate radical can abstract hydrogen from methane in concentrated sulfuric acid, producing a methyl radical together with sulfuric acid. They interpret this radical elementary event as a plausible entry to methane functionalization and methanesulfonic-acid chemistry.

**Candidate route or mechanism.**
Examine a hydrogen-atom-transfer pathway in which an HSO4• oxygen accepts a hydrogen atom from methane while the methane carbon becomes a methyl radical. The authors also considered closed-shell methane protonation, hydride abstraction, and C–H activation as competing mechanistic classes, so these provide useful alternatives for comparison where they fit the stated system boundary.

**Discriminating evidence.**
Use optimized reactant and product-side states, a genuine first-order saddle with its imaginary displacement assigned to the coupled C–H breaking/O–H making event, and an IRC or equivalent displacement analysis to establish connectivity. Compare solution-phase free energies and assess robustness using consistent refinements and sensitivity to conformers and electronic-structure treatment.

# Public inputs and scientific boundaries

Use `data/inputs/system_specification.json`. It fixes methane, neutral doublet HSO4•, neutral singlet H2SO4, the 98% sulfuric-acid continuum, 298.15 K, and the elementary methane-functionalization scope. The scored system is the specified molecular species evaluated in that implicit continuum; do not add an explicit host, solvent molecule, or metal complex. You may generate conformers, complexes, and transition-state guesses. State charge, multiplicity, atom mapping, and standard-state convention.

# Required scientific validation/investigation

Propose and discriminate plausible elementary explanations within the stated reactant/product boundary; do not invent a discovery story beyond calculations. Generate and deduplicate a finite set of candidate complexes and transition structures, retain candidate identity and provenance, and advance only candidates with chemically conserved atoms and spin. Validate minima by zero imaginary frequencies, candidate TSs by exactly one imaginary frequency assigned to the bond-making/bond-breaking coordinate, and connectivity by IRC or an equivalent displacement analysis. Refine the best validated candidate consistently and quantify sensitivity to conformer, method, and treatment choices. Completion requires either a validated barrier and product-side assignment or a bounded-failure report explaining why validation could not be achieved. Stop when the declared candidate-generation strategy is exhausted and further guesses are duplicates or fail the validation tests; report search coverage and limitations.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`, including candidate identities, validation evidence, selected barrier in kcal/mol when available, product-side structure, uncertainty, and conclusion. Include hypotheses when required by the local schema. The status must be `completed` or a truthful bounded-failure value with candidate-specific diagnostics. Include coordinates or unambiguous structure identifiers sufficient for checking.
