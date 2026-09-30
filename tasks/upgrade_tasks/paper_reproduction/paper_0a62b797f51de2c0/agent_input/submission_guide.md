# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.length_series

Calculate all three substitution levels at n=1,2,3 with the same caps, method and state definition. Validate minima and conformer/torsion coverage. Compute dipole/ESP and independent electron-hole separation/overlap; do not infer charge separation from polarization alone.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.regiochemical_control

Verify the two same-formula graphs differ in cyano position, then compare at relaxed and identical inter-ring torsions. Attribute any difference to the specified regio/twist intervention while acknowledging state-character changes. Supply all matched atom maps and NTO evidence.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.length_holdout

Freeze an explicit ordering or quantitative relationship using n<=2 before testing all n=3 members. State prediction residual/rank success and whether the regio control falsifies a dipole-only explanation. Do not claim polymer-length convergence from three short chains.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.
