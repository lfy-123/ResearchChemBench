# Submission requirements

Submit `report/results.json` and `report/report.md` conforming to `submission_schema.json`. The report must contain the scientific answer, actual computational results, evidence references and unresolved findings.

Molecular records require identity, composition, atom correspondence, charge, electronic state and conditions. Numerical results require physical definitions, units, references, methods, conditions and links to producing records and native artifacts. Validity evidence is required for each claimed structure, state or transformation. Supplied observations and new computed results require distinct provenance.

Generated evidence belongs under `outputs/`; analysis code belongs under `code/`; supplied inputs are referenced under `data/`. Framework records may use their registered public paths where allowed by the schema. Artifact paths must be durable, workspace-relative and schema-compliant, with no symlinks or temporary/cache paths. Referenced IDs and files must resolve; checksums must match where required.

Missing quantities must be omitted or null where permitted. Retain actual evidence and identify unavailable results and execution diagnostics. Execution records and resource-use fields must describe actual work. Private internal reasoning is not required.

General scientific/software documentation is permitted. Private evaluator files, reference answers and prior run outputs are excluded.

`models`, `operations`, `artifacts`, `results`, `claims` and `validations` retain their schema-defined roles. Gibbs-energy comparisons use the molecular conditions in `data/reaction_conditions.json`; native quantities and conversions must be reported.

## Final scientific conclusions

Address each required result explicitly in the final answer and connect it to the existing results/claims/artifacts records. Link the supporting calculations and validation evidence to each conclusion. Use the existing schema.
