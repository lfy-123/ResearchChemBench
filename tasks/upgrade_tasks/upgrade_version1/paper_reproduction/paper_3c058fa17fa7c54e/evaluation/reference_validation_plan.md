# Expanded reference validation plan

Status: implemented_pending_expanded_reference. No new quantum-chemical reference calculation was performed during package development.

## Inspected primary evidence

- paper_main, PDF pages [2, 3, 4]: Structures, source B3LYP calculation and inconsistent S/T labeling passages read; molecule-level energetic statement is distinct from TTA kinetics.
- paper_si, PDF pages [2]: Actual available SI inspected for B3LYP/6-31G(d,p) protocol; prior documentation did not fully exploit this local SI.

## Reusable legacy evidence

The two complete parent identities and narrow singlet/triplet computational route can be reused for a pilot; old inequalities and any state-label ambiguity cannot validate the controls. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## New reference gaps

Ethynyl control geometries, matched torsions, NTO correspondence and separately relaxed excited-state references are missing.

## Minimum pilot

Confirm parent formulas C55H34F6 and C57H35F6NO; validate ethynyl valence and common-arm maps, then calculate one parent/control matched state pair.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

Gaussian/ORCA singlet/triplet TDDFT and excited-state optimization; Multiwfn or equivalent state-density analysis. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.
