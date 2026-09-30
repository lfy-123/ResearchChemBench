# Scientific objective

Independently investigate how glyme chain length (G1–G4) and glyme:KTf2N ratio (2:1, 3:1, 4:1) affect potassium–anion aggregation in the 12 named periodic bulk systems. Quantify the fraction of Tf2N− anions coordinated by at least two distinct K+ ions and determine which trends, if any, are supported by validated simulation. Report per-system AGG fraction (%), anion K+-coordination populations, K–O RDFs/first-shell distances, and a qualitative comparison to Raman ν(SN) coordination observations. This is a bulk-solvation study; do not infer battery performance or reaction mechanisms.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that shorter glymes retain more K+–Tf2N− contact ion pairs and aggregates, and that the cross-system AGG pattern tracks the Raman ν(SN) coordination response.

**Candidate route or mechanism.**
Test glyme coordination and K+–Tf2N− contact as competing first-shell environments for K+, comparing how their populations change across glyme chain lengths and glyme:salt ratios.

**Discriminating evidence.**
Use K–O(glyme) and K–O(Tf2N−) RDF shell structure, per-anion K+-coordination histograms, derived AGG fractions, and their qualitative cross-system consistency with Raman ν(SN) observations.

# Public inputs and scientific boundaries

Use only `data/inputs/molecules.json`, `systems.json`, and `measurement_definition.json`. They define the unique molecules, charge and singlet state, atom roles, 12 compositions, counts, cubic box lengths, periodic boundary, and 350.15 K target. You must choose and justify the computational model and analysis route. Do not use the paper, SI, general web, or result-bearing source material. An AGG is exactly a Tf2N− anion with at least two distinct K+ ions within the submitted anion first-shell cutoff; report the atom selector and cutoff. The scored systems are the defined bulk periodic mixtures; do not add electrodes, reactions, or battery cycling.

# Required scientific validation/investigation

Propose plausible physical explanations before testing them, then discriminate them with independent calculations. Generate and prioritize candidates only within the fixed 12-system set; retain system identity and computational provenance. For each advanced system verify charge neutrality, counts, atom typing, periodic cell, temperature control, and stable observables. Establish RDFs and justify first-shell cutoffs, compute per-anion coordination histograms and AGG fractions from individual anion identities, and quantify uncertainty/convergence using replicas, blocks, seeds, or an equivalent method. Report full coverage or a bounded-failure account listing completed/failed systems, causes, validation, and next limiting calculation. Completion requires validated all-system coverage or an explicit scientifically honest limitation; stop when the declared uncertainty/coverage criterion is met or the stated resource boundary prevents further work. Do not claim a global trend from missing or unvalidated systems.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`, plus any referenced files under `report/`. Include model provenance, per-system status and observables, validation evidence, uncertainty/limitations, coverage, and a final conclusion about supported glyme/concentration trends and Raman consistency. Bounded failure must be represented explicitly.
