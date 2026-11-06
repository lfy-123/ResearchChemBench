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

Scientific credit is awarded only for supported scientific results and conclusions
within the question addressed. Copying a reference result is insufficient. A
well-supported alternative can answer the question; unresolved work may establish
individual scientific findings, but effort or failure documentation alone earns
no credit.
Schema acceptance checks structure and does not certify scientific completion.

When scientific guidance is supplied, it provides starting hypotheses, models and
methods for the same scientific question; it does not add scientific objectives
or require every described calculation. Record relevant ambiguities and justified
substitutions in the method/outcome records and readable report. Without supplied
guidance, choose your own research approach.
