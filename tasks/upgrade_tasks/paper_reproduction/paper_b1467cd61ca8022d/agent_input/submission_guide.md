# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use PM COCCC, BM COCCCC, TFPM COCCC(F)(F)F and TFBM COCCCC(F)(F)F; all solvent molecules neutral singlets. Li+ is singlet; FSI- is F-S(=O)2-N(-)-S(=O)2-F, singlet. Core clusters contain exactly one Li+, one FSI- and one solvent (total charge0 singlet). Compare O-facing, O/F-contact where F exists, and FSI-dominated orientations at identical composition. No 2 M bulk interpretation follows from this finite-cluster design.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.cluster_orientations`: mandatory rows PM_solvent_contact, PM_anion_contact, BM_solvent_contact, BM_anion_contact, TFPM_solvent_contact, TFPM_anion_contact, TFBM_solvent_contact, TFBM_anion_contact; numeric metrics electronic_Eh, Li_O_A, Li_F_nearest_A, lowest_frequency_cm1. For nonfluorinated solvents any F contact is to FSI and must be labeled. Fluorinated candidates include attempted bidentate and O-only starts; retain real collapse evidence.
- `results.fragment_controls`: mandatory rows PM, BM, TFPM, TFBM; numeric metrics binding_kJ_mol, interaction_kJ_mol, distortion_kJ_mol, dipole_D, ESP_O_eV, RESP_O_e. Compute common-fragment interaction/distortion and state explicitly surface/isodensity/gauge for ESP. A gas-phase ion-solvent Eb and neutral salt-cluster interaction are separate quantities.
- `results.descriptor_test`: mandatory rows O_F_contrast, anion_competition, method_sensitivity; numeric metrics paired_energy_change_kJ_mol, uncertainty_kJ_mol. Test a descriptor prediction against actual coordination and anion intervention, not a restatement of source ordering. Do not infer conductivity/SEI or bulk RDF.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
