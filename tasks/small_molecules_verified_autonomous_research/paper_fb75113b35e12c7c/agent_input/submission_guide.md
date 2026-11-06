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

Failed work must include attempted inputs, error logs
and an explanation; do not invent missing results. Report actual resource use in the readable report.

Schema acceptance checks structure and does not certify scientific completion.

Choose your own hypotheses, computational models and research approach.
