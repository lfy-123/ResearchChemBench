# Expanded reference validation plan

Status: expanded core reference scientifically validated on 2026-09-28 by Group2. The historical authoring run itself performed no new quantum calculation; subsequent real verification is recorded in verified_computation_reference.md/json.

## Inspected primary evidence

- paper_main, PDF pages [2, 3, 4]: Fig1 checked visually for compounds1,3,5,7; HRS/DR definitions and method read.
- paper_si, PDF pages [16, 24, 26, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48]: Coordinate blocks transcribed to valence-checked graphs: C30H18, C36H20, C48H24, C52H24. Computed response tables inspected privately, not made public.

## Reusable legacy evidence

Compound5 graph and inner-rim path can be reused only after mapping validation. Its five torsions do not establish nonlinear response. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## Historical reference gaps at authoring (addressed for the core)

Static full tensors, rotation/field-step calibration and matched-twist response references are not yet computed.

## Minimum pilot

Run compound5 response and one constrained common-core point, verify atom mapping, units and rotational invariants before remaining members.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

Gaussian native static response or validated finite-field Gaussian/ORCA calculations plus Python isotropic averaging; TD/NTO diagnostic. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.

## Completed verification and interpretation limits

Four positive-frequency source-baseline minima (one explicit reuse), six full static tensors, two exact five-torsion interventions, four TD10 windows and corrected checkpoint NTOs, all-axis analytic/finite-field calibration, independent exact sphere moments, rigid rotation and grid sensitivity have native evidence. Original failed/incorrect attempts are retained and excluded from accepted quantities. Finite numerical checks do not establish universal method/state/ensemble error. No exact-answer tolerances, blind AR success or remote judge scores are claimed.
