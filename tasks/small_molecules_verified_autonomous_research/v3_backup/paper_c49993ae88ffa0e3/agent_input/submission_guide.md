# Submission requirements

Submit `report/results.json` and `report/report.md` conforming to `submission_schema.json`. The report must contain the scientific answer, actual computational results, evidence references and unresolved findings.

Molecular records require identity, composition, atom correspondence, charge, electronic state and conditions. Numerical results require physical definitions, units, references, methods, conditions and links to producing records and native artifacts. Validity evidence is required for each claimed structure, state or transformation. Supplied observations and new computed results require distinct provenance.

Generated evidence belongs under `outputs/`; analysis code belongs under `code/`; supplied inputs are referenced under `data/`. Framework records may use their registered public paths where allowed by the schema. Artifact paths must be durable, workspace-relative and schema-compliant, with no symlinks or temporary/cache paths. Referenced IDs and files must resolve; checksums must match where required.

Use the schema's completion and failure statuses. Missing quantities must be omitted or null where permitted. Partial or failed submissions retain actual evidence and identify missing results and diagnostics. Execution records and resource-use fields must describe actual work. Private internal reasoning is not required.

General scientific/software documentation is permitted. Private evaluator files, reference answers and prior run outputs are excluded.

`models`, `operations`, `artifacts`, `results`, `claims` and `validations` retain their schema-defined roles. Quantities include extraction locations and physical references.

Final answers are evaluated as independent scientific conclusions under `paper_science_v3` / `final_results_100`. Provide the numerical comparisons and bounded explanations requested in task.md, linked to the existing result fields and native evidence. There is no separate credit for intermediate calculation stages or calculation counts.

Report both required net Gibbs energies with the standardized state and association references in task.md. Use the existing quantity/reference fields to distinguish these reports from any alternative mechanistic models. The reference definitions specify comparable quantities; agreement with them does not establish a unique reactive state, solution association or transfer sequence. No additional schema fields or fixed intermediate sequence are required.
