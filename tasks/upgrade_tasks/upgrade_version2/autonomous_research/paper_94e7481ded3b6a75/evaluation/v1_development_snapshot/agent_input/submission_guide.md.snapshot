# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

First version uses source PBNA C24H22B2N2, neutral singlet, with the two mapped B-phenyl torsions. Compute S0 and a tracked S1 on released and identically restrained motion coordinates, primary gas phase with common CH2Cl2 sensitivity. A restrained excited-state point is an intervention, not an unconstrained S1 minimum. Retain all B/N connectivity.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.state_geometry`: mandatory rows S0_free, S1_free, S0_restrained, S1_restrained; numeric metrics electronic_Eh, torsion_degree, excitation_eV, oscillator_strength. Keep geometric and electronic-state records distinct; S1 and S0 energies must refer to the stated same protocol and geometry.
- `results.motion_response`: mandatory rows vertical_fixed_motion, relaxed_motion; numeric metrics excitation_change_eV, CT_distance_change_A, relaxation_kJ_mol. Inspect NTO/transition densities and local geometry; compute paired effects rather than infer them from frontier orbital pictures.
- `results.local_robustness`: mandatory rows second_torsion_or_method, common_solvent; numeric metrics primary_effect_eV, control_effect_eV, uncertainty_eV. Actual motion/method or medium sensitivity bounds the isolated-molecule claim; no quantum yield, knr or bulk AIE is scored.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
