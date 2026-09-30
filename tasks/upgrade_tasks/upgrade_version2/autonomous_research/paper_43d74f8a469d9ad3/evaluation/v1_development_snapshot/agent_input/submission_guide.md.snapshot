# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Core comparison: Scheme1 compound1 C23H20BNO3 and compound2 C24H22BNO4, neutral singlets. Compound1 is fixed by CCDC2441197; compound2 adds the para-to-phenoxy methoxy group shown in Scheme1, retaining the 3,5-dimethylphenyl boron substituent. Use mapped X-B-Cipso-Cortho on that aryl branch in both. Primary gas phase and an explicitly identical optical solvent sensitivity. Source SI coordinate labels S5/S6 conflict with Scheme1 identities; their unchecked coordinate assignments are not authorized.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.torsion_profiles`: mandatory rows dye1_S0, dye1_S1, dye2_S0, dye2_S1; numeric metrics torsional_range_kJ_mol, reference_angle_degree, tracked_excitation_eV. Store a numeric angle-energy-property CSV with mapped atoms at each point, constrained degrees of freedom and forward/backward state overlap; include released anchors.
- `results.restriction_control`: mandatory rows dye1_restricted_vs_free, dye2_restricted_vs_free; numeric metrics excitation_change_eV, oscillator_strength_change, relaxation_kJ_mol. Use the same mapped angle intervention in both compounds, with actual frozen and relaxed calculations. Root switching is recorded, not smoothed away.
- `results.continuity_and_robustness`: mandatory rows state_following, method_or_grid; numeric metrics minimum_state_overlap, energy_change_eV, profile_change_kJ_mol. Demonstrate TD root-window/step-size or method sensitivity and identify discontinuities. Do not extrapolate S0 resistance to an absolute photobleaching rate.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
