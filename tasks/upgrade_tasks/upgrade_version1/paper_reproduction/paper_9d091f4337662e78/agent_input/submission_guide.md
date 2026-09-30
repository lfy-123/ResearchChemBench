# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.ensemble_search

Search both configurations independently, show per-seed generation/deduplication, refine all retained conformers and document excluded populations. Supply geometries, G values, degeneracy and weights normalized within each configuration. Validate stereochemistry and minima. Conformer collapse is deduplicated, not artificially counted.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.ensemble_ECD

Provide per-conformer transition/rotatory strengths, weighted spectrum and analysis code under one convention. Verify a mirror pair has matching energy and opposite rotatory sign within numerical convergence. Never average R and S populations into one spectrum or choose the sign from the known label.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.configuration_discrimination

Compare both frozen ensemble predictions against the heldout experimental band; compute residual/sign diagnostics across cutoff and broadening perturbations. Account separately for digitization and model errors. A two-member support set is valid only after the required searches and comparisons, not as a substitute for them.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.
