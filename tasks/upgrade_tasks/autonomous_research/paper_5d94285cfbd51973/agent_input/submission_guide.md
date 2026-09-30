# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.descriptor_series

Compute the same isolated-molecule electronic descriptors for all ten systems using a shared method, validated conformer choice and minimum checks. Retain comparable sampling across members. Verify substituted ring positions and report simple RDKit descriptors independently; do not reinterpret Koopmans descriptors as measured IP/EA.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.out_of_fold

For each AZ member retain nine training IDs, train-only preprocessing, coefficients and three predictions. Use exactly the frozen features and fixed regularization, no post-hoc feature selection or dropping outliers. Recompute MAE in ordinal bins and compare the electronic model with physicochemical and mean baselines.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.null_and_resolution

Permute labels and rerun the entire frozen fold procedure; submit all scores and seed. Test dilution/endpoint uncertainty and leave-one-member influence without claiming validation from an in-sample correlation. A null result or baseline dominance is scientifically acceptable.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.
