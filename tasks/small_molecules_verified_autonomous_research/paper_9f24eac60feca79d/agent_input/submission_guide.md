# Technical submission specification

Submit `report/results.json` and `report/report.md`. Use agent-defined identities and lists for objects, networks, key transformations and results; the schema imposes no pathway labels or reaction-step count. Entries describe the actual investigation, including available results and failed attempts.

For molecular objects identify full connectivity, stereochemistry, charge, multiplicity and environment. For each numerical result retain units, physical definition, reference state, conditions and the actual calculation/analysis record. A network may include transformations for which a transition state or barrier is inapplicable or uncomputed; use null or omit the optional barrier and explain its status. Reaction stoichiometry and any exchanged particles must be explicit. Do not identify a method-specific electronic descriptor as an experimental activation free energy.

Claimed minima and saddles require the appropriate stationarity, curvature and electronic-state evidence. Claimed elementary barriers additionally require valid connectivity to the stated neighboring states, by IRC or a justified equivalent. A candidate energy height is distinct from a validated barrier. Retain source inputs, native outputs and analysis code with artifact hashes and locators. Match result IDs to the stated objects and records; file names and array order have no scientific meaning.

Separate supplied observations from new findings and give the evidence supporting the final chemical explanation. 

Use the supplied public task inputs, independently generated results and runtime resources. General technical documentation is permitted. Record actual resource use and a concise execution/decision record; private internal reasoning is not requested.

Describe the investigated objects, methods, actual calculation or analysis records, numerical results and their evidence links. Other results or optional barriers may remain null when their absence is explained. No minimum number of network steps, transition states or competing mechanisms is imposed. A rigorous counterexample or an evidence-backed bound can support an answer when it addresses the scoped question; agreement with an expected explanation and a supported-claim label are not required. The schema only checks that this evidence representation exists, not its truth or scientific sufficiency. When no physical result was obtained, retain execution records and available evidence without inventing values.
