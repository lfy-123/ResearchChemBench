# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.spectral_series

Construct complete identities with fixed operational backbone helicity; calculateUV/ECD/gabs and state-character correspondence at one solvent/response convention. Retain full transition moments/strengths and raw states. Do not infer spectral changes from the old relative single-point energy.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.common_geometry

Use the explicit retained mono/di subunit maps, restore all monomerCl/H and quantify the common-core RMSD. Compare equivalent bands/NTO character under one broadening. State remaining composition/coupling effects; never call a clipped arbitrary fragment the fullmonomer or compare its unbalanced total energy.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.ensemble_and_sign

Sample sidechain conformers only within each fixed member/backbone, document minima/free energies and weight convergence. Perform a true mirror sign/energy calibration and one common broadening/weight perturbation. If kinetic evidence excludes equilibrium, report conditional spectra without unjustified cross-family weighting.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.
