# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.matched_absorption

Validate paired identities; compute corresponding TD bright states and spectra in both solvents with a common broadening. Report CF3 and aryl-extension effects separately. Keep KS gap, excitation energy, spectral maximum and absorption edge as distinct observables.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.species_crosscheck

Attempt all four7a forms with mobile-proton mapping. Validate surviving minima, record collapse, and obtain same-species spectra plus NMR/IR functional-group diagnostics. Use the correct experimental medium and one shielding reference; an absent band must be marked and explained rather than fabricated as an observed peak. Deduplicate collapsed tautomer endpoints.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.solvent_species_attribution

Decompose7a CHCl3→DMF shift into fixed-species and redistribution contributions using normalized same-molecule free-energy weights. Check whether optical and NMR/IR evidence support one species model jointly. Unsupported redistribution or an indistinguishable support set must remain explicit.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.
