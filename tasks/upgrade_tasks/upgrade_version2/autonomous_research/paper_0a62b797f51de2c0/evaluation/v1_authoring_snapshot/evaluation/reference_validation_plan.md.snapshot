# Expanded reference validation plan

Status: implemented_pending_expanded_reference. No new quantum-chemical reference calculation was performed during package development.

## Inspected primary evidence

- paper_main, PDF pages [2, 4, 5]: Scheme1 inspected visually, confirming alternating para-phenylene/thiophene connectivity; charge-separation interpretation read.
- paper_si, PDF pages [6]: Computational geometry/dipole protocol read. The expanded finite oligomers are specified as new benchmark models.

## Reusable legacy evidence

Monomer substituent identities and original dipole protocol are reusable provenance; old three-monomer scalar ranking is insufficient. The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.

## New reference gaps

The ten new explicit oligomer/regio graphs require independently calculated geometry/state references and a frozen length prediction.

## Minimum pilot

Verify valence, cap/count consistency and regio non-isomorphism using RDKit. Run CN1_n1 and one CN1_n2 torsion point before committing the full series.

## Full expanded validation

Execute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.

## Available route and resource boundary

RDKit for graph assembly, Gaussian/ORCA TDDFT and NTO/density analysis; Multiwfn or reproducible Python integration. Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.
