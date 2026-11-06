# Submission requirements

Submit `report/results.json` and `report/report.md` conforming to `submission_schema.json`. The report must contain the scientific answer, actual computational results, evidence references and unresolved findings.

Molecular records require identity, composition, atom correspondence, charge, electronic state and conditions. Numerical results require physical definitions, units, references, methods, conditions and links to producing records and native artifacts. Validity evidence is required for each claimed structure, state or transformation. Supplied observations and new computed results require distinct provenance.

Retain native calculation inputs, outputs, structures and analysis files. Artifact paths are relative to the submission root and identify retained evidence files. Referenced IDs and files must resolve; checksums must match where required by the schema.

Use the schema's completion and failure statuses. Missing quantities must be omitted or null where permitted. Partial or failed submissions retain actual evidence and identify missing results and diagnostics. Execution records and resource-use fields must describe actual work. Private internal reasoning is not required.

General scientific/software documentation is permitted. Private evaluator files, reference answers and prior run outputs are excluded.

`systems` identifies molecular objects; `methods` records computational definitions; `quantities` contains numerical results; `findings` contains evidence-linked findings. `series_explanation` identifies the compared catalysts and supporting finding IDs; `conclusion` contains the final answer. `reaction_network` is optional. Solution free energies require raw thermal/standard-state conventions and any conversion to the common 1 M convention. Partial/failed submissions identify `failure.affected_results` and `failure.reason`.

Final answers are evaluated as independent scientific conclusions under `paper_science_v3` / `final_results_100`. Provide the numerical comparisons and bounded explanations requested in task.md, linked to the existing result fields and native evidence. There is no separate credit for intermediate calculation stages or calculation counts.

Address the A/B, C/D, C/E and catalyst/background comparisons separately, choosing the physical explanations and evidence. For C/E, assess the explanatory reach of your computed molecular comparisons and retain the observed time crossing. A new time-dependent kinetic model is not required; any unresolved cause must be tied to the limits of the actual evidence.
