# Scientific objective

Using the supplied acid and three ligand structures, independently determine whether ligand identity changes the relative methyl versus β-methylene CMD C(sp3)–H activation propensity, and identify the best-supported mechanistic explanation from your calculations. Report validated activation barriers, ratios, uncertainty, and the scope of the conclusion.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that ligand identity controls the balance between methyl and β-methylene C(sp3)–H activation in this Pd/CMD model. In particular, the MPAA/MPAThio ligand class represented by L7 and L9 is proposed to reduce the intrinsic methylene preference associated with the bidentate pyridone ligand L12, thereby favoring methyl activation.

**Candidate route or mechanism.**
A useful candidate explanation is that ligand-dependent coordination geometry and electronic environment selectively stabilize the methyl or methylene CMD transition structure. Compare this with an alternative in which the ligand primarily changes conformational organization or reactant/transition-state strain, so that the site preference changes without a simple intrinsic electronic effect.

**Discriminating evidence.**
Use independently generated, frequency-validated methyl and methylene CMD stationary points for every ligand, relative free-energy barriers on consistent reactant references, and methyl/methylene selectivity ratios with uncertainty. Compare geometrical and electronic features of the validated structures and test whether the ligand trend persists across conformers and search coverage; validate the proposed connectivity by IRC in both directions or a reproducible alternative.

# Public inputs and scientific boundaries

`data/inputs/model_system.json` defines 1-methylcyclohexane-1-carboxylic acid, the methyl and β-methylene sites, temperature and medium. `ligand_definitions.json` gives source-supported, answer-neutral connectivity descriptions for L7, L9 and L12. Reconstruct all systems with explicit mapping, charge and multiplicity. The scored system is the isolated molecule; do not add a host or solvent. The measured objects are validated methyl and methylene CMD stationary points; the task does not score a complete catalytic cycle.

# Required scientific validation/investigation

Formulate at least two plausible explanations for any ligand-dependent trend and state predictions that discriminate them. For every ligand/site, generate and deduplicate a finite candidate set, optimize candidates, and retain only chemically coherent structures. Verify stationary-point order by frequencies and validate TS connectivity by IRC in both directions or a reproducible alternative. Report search coverage, failed candidates and the stopping condition: stop when new independent guesses no longer yield a new validated lower structure, or give a bounded-failure report if resources prevent completion. Conclusions must distinguish computed evidence from mechanistic interpretation.

# Deliverables

Submit `report/results.json` conforming to the schema, containing at least two competing hypotheses with discriminating tests, six uniquely identified ligand/site objects, per-object candidate ledgers and validation evidence, barriers, ratios, uncertainty, and a final conclusion. The bounded-failure branch must preserve attempted-object identity and missing-validation details and must not fabricate numbers.
