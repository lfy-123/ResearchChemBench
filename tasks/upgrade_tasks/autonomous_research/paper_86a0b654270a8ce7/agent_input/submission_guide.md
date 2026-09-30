# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Both complete IrC60H63N4O2 isomers are neutral singlets, in THF at 339 K. Preserve Ir coordination identity; report E, solvent contribution, ZPE/thermal and low-frequency correction separately with one standard state. The source predicts a preference, but a contrary converged method is not discarded. Contact-separation restraints measure interaction plus deformation and must not be called pure pi-stacking energies.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.isomer_ensembles`: mandatory rows isomer1, isomer2; numeric metrics electronic_Eh, solvation_Eh, thermal_Eh, low_frequency_Eh, G_339K_Eh. Use low-energy conformer coverage and frequency evidence with identical 339 K convention; reconstruct ensemble G and document degeneracy.
- `results.stacking_intervention`: mandatory rows isomer1_contact, isomer2_contact; numeric metrics centroid_distance_A, relative_angle_degree, delta_E_kJ_mol, distortion_kJ_mol. Submit mapped aromatic ring atoms and frozen/released contacts, controlling other geometry. Distortion cannot be removed by merely labeling the difference stacking.
- `results.ranking_robustness`: mandatory rows method_change, thermal_model_change; numeric metrics delta_G_2_minus_1_kJ_mol, uncertainty_kJ_mol. Quantify sign and interval under actual methods and thermal treatment; unresolved ranking after complete data is acceptable. Isolated yields are not a scored equilibrium ratio.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
