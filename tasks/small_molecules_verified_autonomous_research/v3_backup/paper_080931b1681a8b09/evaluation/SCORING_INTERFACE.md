# case_08 V3 conclusion-only interface

Revision: `human_review_conclusion_evidence_20261102`. Policy: `paper_science_v3`; runtime: `final_results_100`.
There are 4 separately weighted semantic outcomes totaling 100 points. All outcomes are binary. Tiered outcomes explicitly include their cumulative scientific conditions in expected; assess them in full.
Use the authored `expected` and `scientific_requirements` for scientific assessment.
Each rule's `qualification` and `required_numerical_evidence` specify mandatory computed quantities and native evidence. Verify the submitted values, definitions and provenance before passing the scientific conclusion; missing necessary quantities/evidence fail only the affected items.
Return one `scientific_conclusions` entry and one matching `rule_assessments` entry per rule, with evidence citations and rationale.
The judge response field `numeric_results` must be an empty list: it is reserved for hard numeric target checks, which this revision has none of. This does NOT permit the submitter to omit numbers: `report/results.json.metrics` must contain the required computed quantities, linked from claims and supported by native records. Cite and assess those values in the semantic rationale, without returning a numeric_check, score, weight or invented tolerance.
The host awards each passed item's fixed weight. A local failure does not erase other supported outcomes.
`whole_case_success` requires all core items, independently of the retained partial score.
Use `objective_issue_flags` for demonstrated reference defects; never convert infrastructure failures into scientific zeros.

The scientific question remains in `agent_input/task.md`. Source numbers and historical scoring prose in `verified_computation_reference.md` / `historical_reference` have no active acceptance force.
This revision does not change the general evaluator engine, completed scores or frozen running-task copies.
