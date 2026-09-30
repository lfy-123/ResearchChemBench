# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use neutral singlet 1a C11H8BF2NO and 1b/1c/1d C15H10BF2NO; retain their distinct azaarene fusion/connectivity. Primary toluene medium matches experimental_absorption.json and main Fig2/Table1. A gas-phase source baseline is a separate sensitivity, not a toluene measurement. A shared geometry means a mapped local B-N-O/chelate scaffold, not a forced whole-graph atom bijection across different fused isomers. Geometry constraints must be stated and released controls retained.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.relaxed_monomers`: mandatory rows 1a, 1b, 1c, 1d; numeric metrics excitation_eV, oscillator_strength, CT_distance_A. Retain low-root tables, full oscillator distribution and NTOs; observed absorption maximum need not be S1 when a dark state is lower.
- `results.common_geometry`: mandatory rows 1a_common, 1b_common, 1c_common, 1d_common; numeric metrics excitation_eV, oscillator_strength, constraint_deformation_kJ_mol. Actual shared-chelate constraints with atom correspondence and released pairs are mandatory; four original spectra alone are insufficient.
- `results.spectral_test`: mandatory rows electronic_vs_geometry, independent_trend, method_sensitivity; numeric metrics predicted_shift_eV, observed_shift_eV, uncertainty_eV. Separate band energy, intensity and character, with stated broadening/assignment and digitization uncertainty. A retrospective holdout must not be mislabeled a blind prediction.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
