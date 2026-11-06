# Submission guide

Submit `report/results.json`, `report/report.md`, and the actual inputs, outputs,
logs and analysis code under `research/`. Follow `submission_schema.json`.

Use stable IDs for hypotheses, investigations, evidence and conclusions. Every
evidence investigation ID and every conclusion evidence ID must resolve to a
submitted record. Refer to real files with safe relative paths; absolute paths,
parent-directory traversal and symlinks escaping the submission are forbidden.
List each referenced artifact in reproducibility.artifact_index. Preserve object,
state and unit mappings. Numerical evidence includes its definition, units and
conditions; use null with an explanation when a value is unavailable.

For each investigation record a brief purpose, chosen method, actual outcome and
any resulting decision. Do not provide private chain of thought. No fixed number
of hypotheses or tests is required. Requirements for stationary points, kinetics
or other model checks follow the claims actually made.

Research status is complete, partial or execution_failed. Question status is
resolved, partially_resolved or unresolved. These describe different things:
careful research can leave a question unresolved. Complete or resolved claims
require completed investigations, evidence and linked conclusions; a status label
alone establishes nothing. Failed work must include attempted inputs, error logs
and an explanation; do not invent missing results. No fixed scientific compute
quota is imposed. Report actual resource use in the readable report.

Scientific result credit requires supported, physically equivalent results for the
shared scientific comparisons and their chemical implications. Different routes and
methods are allowed; an alternative explanation does not waive a missing result or
reverse a required trend. Agreement copied from a paper is insufficient. Unresolved
work may earn independent process credit without completing the scientific result.
Schema acceptance checks structure and does not certify scientific completion.

In paper_reproduction, also document fidelity to the disclosed author baseline,
protocol ambiguities and justified substitutions in the method/outcome records
and readable report. In autonomous_research, choose your own research approach.

For each numerical quantity, use a scientific name and define the molecular state(s), stereochemical mapping, physical quantity, energy zero, and complete particle/proton/counterion ledger in `definition`. Record temperature, solvent, total charge, multiplicity and thermochemical/standard-state convention in `conditions`; identify reconstruction choices when the source did not specify them. Equivalent names are allowed. Quantities are matched by this identity and definition, never by array position or numerical proximity. Use null and explain missing values; do not fill them with paper values. Scientific results and their chemical implications are scored on the shared scientific axis; planning, execution documentation and baseline fidelity belong to the independent process axis. Numerical tolerances do not certify opposite trends or mismatched species.
