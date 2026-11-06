# Submission guide

Submit `report/results.json` and `report/report.md` using the supplied schema. Use agent-defined model, object, method, execution, quantity and claim identifiers, with all references resolved. Each numerical result needs an observable definition, unit, physical reference, conditions and genuine input/output or analysis artifacts. Include explicit molecular graphs/maps, charges and spins where relevant. List cited artifacts with SHA256 and producer; use `supplied_input` for supplied files.

Use `complete` for an evidence-sufficient answer to the bounded question, `partial` for useful results with missing work, and `bounded_failure` for a supported unsuccessful investigation. These labels do not determine scientific credit. Do not encode an uncomputed result as zero. A pre-engine failure has no invented records or execution counts. Brief research decisions and resource records document actual work; no private chain of thought is requested.

Scientific scoring uses `paper_science_v3` / `final_results_100`: each independent final proposition earns its fixed weight or zero, totaling 100 points. Structures, intermediate calculation steps, software use and report completeness earn no separate points. Claim-specific checks support the affected result. Each result is judged independently as pass or fail. Established equivalent explanations pass; unresolved conflicts, missing evidence or wrong physical definitions fail only the affected result. Numerical values are evidence, without author-value matching windows. All required final propositions must pass for whole-task success.

The decision_log array may be empty, including for complete submissions. Actual scientific results, native evidence and claim-specific validity requirements still apply.
