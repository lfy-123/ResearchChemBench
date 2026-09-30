# Expanded reference validation plan

Status: implemented_pending_expanded_reference. No new quantum-chemical reference calculation was performed during package development.

## Inspected primary evidence

- paper_main, PDF pages [2, 3, 4]: Structure figure inspected visually: nitrothiophene versus nitrophenyl; solvent discussion and source DFT route read.
- paper_si, PDF pages [3, 4, 5]: Lower/higher band tables read and three-solvent numerical observations transcribed; DCM discrepancy isolated from required comparison.

## Reusable legacy evidence

Original E-dye3 phenolate identity and single-solvent TD setup are reusable. The old DCM-only scalar is not a reference for the expanded solvent matrix. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## New reference gaps

Dye4, all matched-solvent states, one-MeOH controls and frozen prediction residuals need reference calculations.

## Minimum pilot

Validate dye4 connectivity and one dye3 methanol cluster; check state matching and diffuse-basis stability before all six continuum jobs.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

Gaussian/ORCA continuum TDDFT, explicit one-MeOH cluster optimization and NTO analysis; no new empirical bulk-solvent model required. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.
