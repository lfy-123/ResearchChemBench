# Expanded reference validation plan

Status: implemented_pending_expanded_reference. No new quantum-chemical reference calculation was performed during package development.

## Inspected primary evidence

- paper_main, PDF pages [5, 7, 8, 9, 10]: Computational study p5 inspected: R2SCAN/def2-TZVP/def2/J scans, no source D3 declaration; ωB97M-V/methanol density analysis is separate. Conformer/interaction discussion inspected, including the actual aromatic C–H···O donor and scans.
- paper_si, PDF pages [8, 9, 10]: TableS8 vacuum energy/entropy/G values inspected; baseline gap is not mechanically reused.

## Reusable legacy evidence

Neutral graphs and torsion labels are reusable; original constrained/optimized evidence can inform a pilot but not validate dispersion/solvent interventions. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## New reference gaps

Matched D3 switches, methanol basins, contact-disfavoring electronic controls and thermal sensitivity remain uncalculated.

## Minimum pilot

For SNaft initialize all basins, validate actual endpoint identity and a same-geometry D3 difference. Check that a contact-disfavoring constraint is geometrically possible without changing connectivity.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

ORCA R2SCAN/def2-TZVP scans/optimization and frequency; Gaussian equivalent only after method validation; GoodVibes/Python consistent thermochemistry. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.
