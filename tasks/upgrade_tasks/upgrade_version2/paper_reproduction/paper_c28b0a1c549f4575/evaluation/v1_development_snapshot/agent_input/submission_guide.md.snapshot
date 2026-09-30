# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

DED is 1,4-diethyl-1,4-diazabicyclo[2.2.2]octane dication, not a neutral diamine. Define A=TEA+BF4- and B=DED2+(BF4-)2 (both charge0 singlet). For each use one and two PC molecules in contact and separated configurations. PC is racemic; choose a fixed stereochemical composition and report it. Compare PC transfer A.PC+B -> A+B.PC and the corresponding second-PC exchange; compare contact/separated at equal solvent count. Source 1 M TEABF4 +0.2 M DED salt is experimental context, not a finite-cluster concentration.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.equal_composition_clusters`: mandatory rows TEA_PC1_contact, TEA_PC1_separated, TEA_PC2_contact, TEA_PC2_separated, DED_PC1_contact, DED_PC1_separated, DED_PC2_contact, DED_PC2_separated; numeric metrics electronic_Eh, G_Eh, ion_pair_distance_A. Keep correct anion count and PC count; separated structures may collapse, but only actual mapped optimization evidence establishes that fact.
- `results.PC_exchange`: mandatory rows first_PC, second_PC; numeric metrics electronic_exchange_kJ_mol, free_energy_exchange_kJ_mol, distortion_kJ_mol. Balance both salt compositions and every PC molecule. Record component energies and coefficients so the exchange is recomputable; no direct ranking of charged DED-PC versus TEA-PC totals.
- `results.ion_pair_control`: mandatory rows TEA_contact_effect, DED_contact_effect, conformer_sensitivity; numeric metrics delta_E_kJ_mol, delta_G_kJ_mol, uncertainty_kJ_mol. Separate ion pairing, PC coordination count and conformer uncertainty; conclusions only concern finite molecular necessary conditions.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
