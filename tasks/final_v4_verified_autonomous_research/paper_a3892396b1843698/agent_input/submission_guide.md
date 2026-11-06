# Submission guide

Submit report/results.json and report/report.md. The JSON schema defines typed, agent-named models, objects, methods, execution records, quantities, claims, brief research decisions, validity checks and artifact provenance. Choose the number and identity of research branches from the question and evidence. The contract is not a prescribed workflow.

Every numeric result needs an observable definition, unit, physical/statistical reference, conditions, an actual record and raw/derived artifacts. All cross-references must resolve; list each cited file with its SHA256 and producer. A producer for a supplied input is identified as supplied_input. New derived results identify a real execution record. Molecular records include explicit graphs/maps, charge and spin where relevant. Do not report an uncomputed value as zero. Give failure/partial status when necessary.

complete means an evidence-sufficient answer to the bounded question, including a well-established unresolved outcome if justified; it is not guaranteed by schema acceptance. partial retains useful supported results and explicitly states missing work. bounded_failure records genuine diagnostic evidence and supports no completed scientific claim. pre_engine failure has no invented records, methods or results and zero engine/analysis counts.

Claim-specific checks should establish the properties actually asserted. A stationary-point or mechanism claim needs the corresponding evidence; alternative numerical or statistical routes use their own valid artifacts. Use the decision_log for short goals, discriminators, outcomes and adjustments, with actual managed trace references when available. A self-authored timestamp is not independent evidence of prior prediction. No private chain of thought is requested.

## Scientific scoring

Only the final scientific results requested in task.md are scored, on a 100-point total. Each independently supported result earns its fixed points or zero. Each result is judged independently as pass or fail; supported equivalent explanations pass, while unresolved conflicts or insufficient evidence fail only the affected result. Numerical values are evidence, without author-value matching windows. Actual calculations must support the conclusions. Supplied observations are reference data, not newly calculated evidence. Structures, convergence, native outputs and analyses support the relevant conclusion and do not earn separate points. Research chronology and tool use are not scoring gates.

A complete submission may use an empty decision_log array. Actual results, completed execution records, claim-specific validity checks and linked native artifacts remain required.
