# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.static_series

For each compound validate geometry, compute the complete static tensor, beta_HRS and DR, and retain raw derivative/response output. Verify unit conversion, permutation symmetry, rigid-frame invariance and orientation quadrature/analytical formula. Compare the 1→3 and5→7 pairs at equal frequency and units.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.twist_control

Validate and publish the common-core mapping, then compare relaxed5/7 with the identical signed five-torsion control. Give beta_HRS and a state/CT diagnostic on each geometry, separating extension and geometry effects. Do not claim a constrained geometry is a minimum.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.response_calibration

Calibrate compound5 static response using field-step or analytic/finite-field comparison and rotation-average convergence. Show how numerical uncertainty affects the paired attribution; a tensor or unit error cannot be hidden in broad tolerance.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.

Calibration alternatives: set calibration_method=analytic_vs_finite_field for an independent analytic-versus-finite-field comparison with one or more actual positive field magnitudes; provide each resulting HRS value and the analytic comparator. Report relative_step_variation as the relative comparator discrepancy and explain it in the convention file; do not claim a multi-step convergence series. Set finite_field_three_step (or omit the new optional field for legacy submissions) only with at least three field magnitudes and three actual HRS values. All tensor, sign, evidence, rotation and attribution checks remain required.
