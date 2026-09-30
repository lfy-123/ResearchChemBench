# Scientific objective

Using the supplied acid and three ligand structures, independently determine whether ligand identity changes the relative methyl versus β-methylene CMD C(sp3)–H activation propensity, and identify the best-supported mechanistic explanation from your calculations. Report validated activation barriers, ratios, uncertainty, and the scope of the conclusion.

# Public inputs and scientific boundaries

`data/inputs/model_system.json` defines 1-methylcyclohexane-1-carboxylic acid, the methyl and β-methylene sites, temperature and medium. `ligand_definitions.json` gives source-supported, answer-neutral connectivity descriptions for L7, L9 and L12. Reconstruct all systems with explicit mapping, charge and multiplicity. The scored system is the isolated molecule; do not add a host or solvent. The measured objects are validated methyl and methylene CMD stationary points; the task does not score a complete catalytic cycle.

# Required scientific validation/investigation

Formulate at least two plausible explanations for any ligand-dependent trend and state predictions that discriminate them. For every ligand/site, generate and deduplicate a finite candidate set, optimize candidates, and retain only chemically coherent structures. Verify stationary-point order by frequencies and validate TS connectivity by IRC in both directions or a reproducible alternative. Report search coverage, failed candidates and the stopping condition: stop when new independent guesses no longer yield a new validated lower structure, or give a bounded-failure report if resources prevent completion. Conclusions must distinguish computed evidence from mechanistic interpretation.

# Deliverables

Submit `report/results.json` conforming to the schema, containing at least two competing hypotheses with discriminating tests, six uniquely identified ligand/site objects, per-object candidate ledgers and validation evidence, barriers, ratios, uncertainty, and a final conclusion. The bounded-failure branch must preserve attempted-object identity and missing-validation details and must not fabricate numbers.
