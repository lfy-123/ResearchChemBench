# Submission guide

Write `report/results.json` and `report/report.md`. The schema is an auditable record, not a prescribed research matrix. Choose meaningful object, method, hypothesis, record and quantity IDs. Hypotheses may be an empty list when the actual route does not use explicit hypotheses; their names and number are unrestricted. Describe observable definitions, units, charge/electronic state, atom correspondence and conditions precisely. Use null plus an explanation for unavailable or inapplicable numeric values, never invented zeros.

Every quantity links to objects, calculation/analysis records and artifacts. Artifacts list workspace-relative `outputs/`, `data/` or `code/` paths with actual SHA256. Preserve full native inputs/outputs, structures, measurement provenance and analysis code appropriate to your route. Referenced IDs must resolve, files must exist, and hashes must match. Evidence review must inspect those artifacts; passing JSON shape alone earns no scientific result credit. The host format validator does not by itself verify all nested IDs, artifact hashes or scientific correctness.

Decision records are concise purposes or predictions, available evidence, actual outcomes and changes of direction. Link authentic execution traces where available; your own timestamp or retrospective story cannot establish advance prediction. Do not provide hidden internal chain-of-thought.

`complete` asserts an adequately evidenced answer to the stated question, which can be supported, refuted or genuinely unresolved. It requires substantive quantitative evidence and at least one completed analysis/calculation, not completion of any fixed count of jobs. `partial` reports supported progress with remaining gaps. `bounded_failure` reports an input/resource/computation barrier and a concrete release condition. Both require failure_report; zero starts and no artifacts are valid when nothing ran, but are not a scientific pass. Uncertainty must arise from evidence, not omitted work. Claims that were revised or withdrawn remain distinguishable from supported claims.

Keep calculations at distinct conditions, on different surfaces or with different energy references distinguishable. Only make claims justified at the supplied physical scale. No fixed model list, named control or hypothesis count is imposed. Report the actual results; agreement or disagreement alone does not establish a scored scientific finding. Choose the computational and analytical approach independently; research decisions earn no separate points.

## Scientific scoring

Scientific scoring uses a single 100-point total consisting of independent final scientific conclusions. Each item earns its fixed points when supported by valid evidence, or zero otherwise. Research effort, software use, report completeness and protocol execution earn no separate points. A negative, contrary or unresolved conclusion may be reported honestly; it earns an item only when the evidence establishes that item’s specific scientific proposition. Neither an outcome label nor a generic uncertainty statement earns credit.

V3 evaluates the required final results in the task. Linked structures, calculations and analysis support those conclusions and have no independent process score.
