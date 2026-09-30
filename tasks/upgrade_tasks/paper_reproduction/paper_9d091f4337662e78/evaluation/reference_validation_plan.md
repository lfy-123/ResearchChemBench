# Expanded reference validation plan

Status: implemented_pending_expanded_reference. No new quantum-chemical reference calculation was performed during package development.

## Inspected primary evidence

- paper_main, PDF pages [4, 6, 7]: Experimental Figure2 visually checked and only black compound1 trace digitized; methods/experimental ECD text inspected.
- paper_si, PDF pages [5]: TableS1 establishes that the three former conformers cover only52.06%, so expanded search cannot be replaced by their old normalization.

## Reusable legacy evidence

Connectivity and known E geometry survive. Old three-conformer energies may be privately inspected for pilot cost, but are not an ensemble reference or permitted starting-answer set. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## New reference gaps

New independent enantiomer searches, complete refined spectra, holdout residuals and calibrated sampling/method uncertainty are not calculated.

## Minimum pilot

Check CIP17 on independently embedded mirror structures; calculate one mirror pair and a conformer cluster to validate energy equality, rotatory sign and feasible TD cost.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

CREST/xTB or systematic conformer search, Gaussian/ORCA DFT/TD-ECD and GoodVibes or auditable Python thermochemistry. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.
