# Expanded reference validation plan

Status: implemented_pending_expanded_reference. No new quantum-chemical reference calculation was performed during package development.

## Inspected primary evidence

- paper_main, PDF pages [5, 6, 7]: Electronic descriptors and antimicrobial interpretation were inspected; one-molecule evidence cannot validate series prediction.
- paper_si, PDF pages [3, 4, 5, 6, 7, 31]: All ten substituent names and the C. albicans MIC column were read; the published 250/500/1000 dilution resolution is retained.

## Reusable legacy evidence

AZ9 graph, source method and its original descriptor calculation can be used as a software/identity baseline only. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## New reference gaps

The other nine electronic-structure references and conformer consistency, frozen out-of-fold/permutation baseline and uncertainty envelope are not yet calculated.

## Minimum pilot

Check all ten graphs and formulas; run AZ9 plus chemically contrasting AZ6 at the same conformer/DFT protocol, then freeze descriptors and fold code before obtaining the remaining calculations.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

RDKit for graphs and physicochemical descriptors; Gaussian/ORCA for DFT and frequency checks; Python for deterministic LOOCV and permutation analysis. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.
