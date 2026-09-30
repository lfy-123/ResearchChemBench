# Expanded reference validation plan

Status: implemented_pending_expanded_reference. No new quantum-chemical reference calculation was performed during package development.

## Inspected primary evidence

- paper_main, PDF pages [3, 4, 5]: Theoretical section and toluene experimental comparison read; Cbz is a real source member.
- paper_si, PDF pages [11, 12, 13, 30, 31]: S0/S1 root/geometry tables andCbz identity inspected; original state conventions do not imply ESA.

## Reusable legacy evidence

The two original graph/independent-start identity files are reusable; no author terminal geometry is required. Old S0-only evidence does not establish the expanded relaxation cycle. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## New reference gaps

State-followedS1 minima, consistent four-point cycles, common-twist contrasts andCbz frozen prediction remain uncalculated.

## Minimum pilot

ValidatePh/Nap S1 following and four-point energy meaning beforeCbz; check non-equilibrium solvent capability in chosen engine.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

Gaussian/ORCA excited-state optimization and TD/NTO analysis; Python four-point bookkeeping. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.
