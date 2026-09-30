# Expanded reference validation plan

Status: expanded core reference scientifically validated on 2026-09-28 by Group 2. Package development itself performed no new quantum calculation; subsequent real verification is recorded in verified_computation_reference.md/json.

## Inspected primary evidence

- paper_main, PDF pages [4, 5]: Table1 E00 crossings, SCE oxidation convention and main p5 4-chloroanisole/quenching evidence were read.
- paper_si, PDF pages [23, 57, 58]: Electrochemical reference conditions and calculations/association discussion were read; the main/SI reference-label discrepancy is retained.

## Reusable legacy evidence

The two donor graphs and source electronic-structure workflow are reusable. Old HOMO-only reference and its discrepancy do not validate redox free energies. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## Historical reference gaps at authoring (now addressed for the public core)

At package authoring on 2026-09-27, these calculations had not yet been performed. The subsequent Group 2 reference completed the public core cycle, diffuse-basis and qRRHO controls, and the driving-force/quenching panels; see the completed verification below. Total external electrochemical/model uncertainty is still uncalibrated and is not replaced by numerical sensitivity.

## Minimum pilot

Validate 1a anion/radical identity, spin and frequencies; freeze the relative-cycle convention before running 1e. Confirm that basis diffuse functions and solution treatment are stable.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

Gaussian or ORCA optimizations, frequency/ΔSCF and thermochemistry; Python for unit-consistent cycles. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.

## Completed verification and limits

Four same-medium anion/radical minima, four diffuse-basis stable single points, RRHO/qRRHO controls, anchored cycle, measured E00, real acceptor comparison and frozen-cycle published-plot challenge are audited. Two source minima were reused. Full native logs and executable analyses are retained in the group reference workspace. There is no missing public core endpoint. External electrochemical/model error is not calibrated; no narrow numerical tolerance is adopted. One native negligible-force optimization is explicitly qualified by its four printed criteria and positive full Hessian. See the private reference for all numbers and paths.

Reference completion means evidence-bound scientific review of the author-informed reference. No remote LLM judge, numerical score or blind autonomous-agent success is claimed.
