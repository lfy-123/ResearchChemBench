# Submission requirements

Submit `report/results.json` and `report/report.md` conforming to `submission_schema.json`. The report must contain the scientific answer, actual computational results, evidence references and unresolved findings.

Molecular records require identity, composition, atom correspondence, charge, electronic state and conditions. Numerical results require physical definitions, units, references, methods, conditions and links to producing records and native artifacts. Validity evidence is required for each claimed structure, state or transformation. Supplied observations and new computed results require distinct provenance.

Retain native calculation inputs, outputs, structures and analysis files. Artifact paths are relative to the submission root and identify retained evidence files. Referenced IDs and files must resolve; checksums must match where required by the schema.

Missing quantities must be omitted or null where permitted. Retain actual evidence and identify unavailable results and execution diagnostics. Execution records and resource-use fields must describe actual work. Private internal reasoning is not required.

General scientific/software documentation and independently sourced reference data are permitted. Private evaluator files, reference answers and prior run outputs are excluded.

`models` identifies computed species; `energy_ledger` contains defined quantities; `results` links findings to artifact, quantity and species IDs; `conclusion` contains the answer. `missing_results` identifies incomplete results. Electrode-referenced quantities are optional and follow the definitions below when reported.

Provide the numerical comparisons and bounded explanations requested in task.md, linked to the existing result fields and native evidence.

## Optional electrode-referenced quantities

Submission requirements for any electrode-referenced quantity reported; these quantities are optional.

Required definitions: reduced and oxidized species, electron count and potential-sign convention.

Required conditions: solvent, temperature, electrolyte and solution standard state for target and reference.

Required reference information: electrode or reference couple, unfitted conversion, junction assumptions, uncertainty, and evidence for any transfer between scales or media.

Calibration must not be fitted to an investigated compound or a desired answer. Reference data require traceable independent provenance.

Only quantities with supporting evidence may be reported.

Reported quantities use the existing quantity IDs and evidence fields; no additional potential or calibration field is required.
