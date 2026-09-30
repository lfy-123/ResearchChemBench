# Scientific objective

Characterize how substitution across the neutral BQ1–BQ7 boron(III) 8-hydroxyquinoline complex series affects excited-state energetics, S1/T1 spin–orbit coupling, intersystem crossing, fluorescence rate and calculated fluorescence yield. Independently formulate plausible physical explanations for observed differences and discriminate them using calculations; do not assume any proposed mechanism in advance.

# Public inputs and scientific boundaries

Use `data/inputs/bq_series.json`, `data/inputs/experimental_solution_fluorescence.json` (observed toluene solution values only), and your own calculations. Each named member is a neutral monomer (charge 0), with singlet S0/S1 and triplet T1/T2; B is bonded to two phenyl ipso carbons and N/O of one deprotonated 8-hydroxyquinolinate. Positions and formulas are explicit. The default boundary is an isolated monomer with implicit toluene. A BQ7 stacked dimer in water may be investigated only if its generated geometry, selection rule and model are reported. You choose software and model chemistry. Do not use the paper, SI, general web, or hidden evaluator files.

# Required scientific validation/investigation

Generate and document structures for all seven named members. Define at least two plausible, testable explanations for the observed photophysical variation, calculate observables capable of discriminating them, and state which evidence supports or weakens each explanation. Validate state identity, convergence/stationarity, common energy references, units, SOC/rate provenance and uncertainty. Completion requires either validated observables for all members or a bounded-failure record for each missing item. Stop after the named series and optional single dimer; report coverage and why further calculations would or would not change the conclusion.

# Deliverables

Write `report/results.json` following `submission_schema.json`, with per-member manifest IDs, status, observables and validation, provenance (raw/log paths or hashes where available), hypotheses and discrimination evidence, conclusion, limitations, and completion status. For a fully successful member use the complete-observables branch. If any requested observable cannot be obtained, use that member's bounded-failure branch, preserve every attempted numeric observable, name each missing observable, and explain the failure and alternatives in validation/provenance/notes; never use fabricated numeric placeholders. Each hypothesis must cite the per-member evidence used to discriminate it. The top-level status is `complete` only if all seven members are complete, otherwise `bounded_failure`.
