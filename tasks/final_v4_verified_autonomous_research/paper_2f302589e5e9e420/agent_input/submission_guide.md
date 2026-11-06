# Submission

Submit `report/results.json` under `submission_schema.json` and a readable `report/report.md`. Use the schema's existing objects/systems, methods, records, results and claims fields. Preserve their identity links and provide units, observable definitions, reference conventions and relevant uncertainty for every number.

Link actual inputs, native outputs and reproducible analyses using workspace-relative artifact paths and SHA256 hashes. A claim must link to its computed or analyzed evidence; a disclosed value or supplied observation is not a newly calculated result. State the physical system, charge/spin, environment and scope actually supported. Geometry, frequency or connectivity evidence is required only for the claim that depends on it. Do not label constrained structures as free minima or use thermodynamics alone to establish a kinetic preference.

The required scientific outputs are listed in `task.md`. Final conclusions alone share 100 points. Evidence is necessary to establish a conclusion; delivering a structure, executing a protocol, maintaining a research log or filling a report does not independently earn points. Supported equivalent scientific explanations are eligible. Missing work and generic uncertainty do not establish a result. An unresolved scientific conflict fails the affected item; author-value matching windows do not apply.

Use `complete`, `partial` or `bounded_failure` honestly and list missing work where required by the schema. A research-log field may remain empty; it records optional brief decisions, not private chain of thought. Schema validation checks format and does not certify scientific success.

Use the supplied task inputs and resources provided by the runner, plus general scientific/software documentation. Do not access private evaluation files or prior verification archives.
