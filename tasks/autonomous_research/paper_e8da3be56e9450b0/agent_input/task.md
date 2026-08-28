# Scientific objective

Independently determine the relaxed spontaneous polarization of the explicitly supplied neutral Zn/Co co-substituted BaTiO3 periodic model and establish whether it is larger than the supplied undoped BaTiO3 control. This is a direct computational test of a materials-property claim; do not assume a mechanism or preferred computational route in advance.

# Public inputs and scientific boundaries

Use `data/inputs/structure_spec.json` as authoritative for identity, charge, multiplicity, cell and substitution, `bzct_start.xyz` as the explicit 40-atom starting geometry, and `bto_reference.xyz` as the parent 5-atom basis to repeat 2×2×2. The BZCT formula is Ba7ZnTi7CoO24, formed by replacing one Ba and one Ti in translated cell (0,0,0) with Zn and Co; no oxygen vacancies are permitted. The initial cell is 7.98×7.98×8.02 Å and periodic. The measured endpoint is Berry-phase spontaneous polarization in μC/cm² relative to a stated nonpolar/reference branch, for both BZCT and BTO. Do not use the paper, SI, general web, or hidden evaluator files. Select and justify the computational method independently.

# Required scientific validation/investigation

Construct and verify both named systems, relax them, and compute polarization with an explicit branch/reference-path procedure. Report convergence of the relaxation and at least one observable-specific sensitivity check, explaining what changed and why it is adequate. Retain object identity and validation context for each system. Completion requires converged relaxed states, reproducible branch-resolved polarization estimates for both systems, a quantitative comparison, and a limitation statement. If resources or convergence prevent completion, stop with the exact attempted scope, partial results, failure cause, and a bounded scientific conclusion. Otherwise stop when the stated convergence and sensitivity requirements are met and further checks do not alter the conclusion within the reported uncertainty; report coverage of all checks actually performed.

# Submission and outcome branches

Submit `report/results.json` using the schema. Set `outcome.kind` to `complete` only when both systems have the required relaxed-structure artifact, convergence evidence, branch-resolved polarization and sensitivity result. If either calculation cannot be completed, set `outcome.kind` to `bounded_failure`, include an exact `failure_report`, and report only measurements and artifacts actually obtained: unavailable polarization, comparison, or relaxed structure may be `null`; do not invent placeholders. In either branch, include two explicitly identified system records (`bzct_2x2x2_neutral` and `bto_2x2x2_control`) and state the coverage and limitation in `conclusion`.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, together with referenced logs and structures. State the chosen route, inputs, convergence evidence, polarization values/units and branch convention, control comparison, uncertainty, and final conclusion. Do not report an invented discovery narrative.
