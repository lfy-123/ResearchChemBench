# Submission requirements

Submit `report/results.json` and `report/report.md` conforming to `submission_schema.json`. The report must contain the scientific answer, actual computational results, evidence references and unresolved findings.

Molecular records require identity, composition, atom correspondence, charge, electronic state and conditions. Numerical results require physical definitions, units, references, methods, conditions and links to producing records and native artifacts. Validity evidence is required for each claimed structure, state or transformation. Supplied observations and new computed results require distinct provenance.

Generated evidence belongs under `outputs/`; analysis code belongs under `code/`; supplied inputs are referenced under `data/`. Framework records may use their registered public paths where allowed by the schema. Artifact paths must be durable, workspace-relative and schema-compliant, with no symlinks or temporary/cache paths. Referenced IDs and files must resolve; checksums must match where required.

Missing quantities must be omitted or null where permitted. Retain actual evidence and identify unavailable results and execution diagnostics. Execution records and resource-use fields must describe actual work. Private internal reasoning is not required.

General scientific/software documentation is permitted. Private evaluator files, reference answers and prior run outputs are excluded.

`models`, `objects`, `methods`, `records`, `results`, `claims`, `decision_log` and `validity_checks` retain their schema-defined roles. `artifact_manifest` requires paths, SHA256, roles and producer IDs. `supplied_input` identifies supplied artifacts; scientific results require their actual producing execution records.

For a `pre_engine` failure without scientific records, a diagnostic artifact may identify its real trace/event producer or use `diagnostic_only:pre_engine` with its provenance described. Scientific records, methods and results remain empty and engine/analysis counts are zero. This exception applies only to diagnostics.

Provide the numerical comparisons and bounded explanations requested in task.md, linked to the existing result fields and native evidence.
