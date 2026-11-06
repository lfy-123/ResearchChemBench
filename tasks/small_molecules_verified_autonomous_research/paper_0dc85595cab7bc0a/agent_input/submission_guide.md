# Submission guide

Submit `report/results.json` under `submission_schema.json` and a readable `report/report.md`. The execution contract requires the readable report in addition to the schema's primary JSON file.

Use `system`, `candidates`, `validation`, `comparison`, `conclusion` and `coverage` as defined in the schema. Retain molecular/state identities, atom mappings, methods, generated candidates and native evidence. Candidates marked `advanced_validated` require the schema's numerical energy, unit and uncertainty fields. Other candidate statuses require `failure_reason`; do not invent unavailable values. 

Explain energetic definitions, stoichiometric/hydrogen bookkeeping, electronic/site evidence and the resulting closure sequence in the readable report. A field named `relative_free_energy` does not authorize relabeling another energetic quantity as Gibbs energy: state the physical definition and method of each comparison. Keep untested alternatives and unavailable quantities explicit.

## Resource protocol

Use supplied public inputs and available computational tools. Private evaluation files and archived answers are excluded.
