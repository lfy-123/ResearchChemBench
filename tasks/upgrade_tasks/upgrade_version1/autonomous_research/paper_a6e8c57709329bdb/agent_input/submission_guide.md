# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

HL is the full C20H22N4O6 neutral singlet graph with two E imines and phenolic OH groups. Source sensing medium is DMF; Co(II) is selected because it is an explicitly measured partial-quenching competitor. Fe(III) spin space includes doublet/quartet/sextet; Co(II) doublet/quartet. Water/DMF ligands, protonation and counterions must be fixed with salt/pH data before a unique binding-energy cycle is defined. Do not compare unlike total compositions or assign selectivity from smallest gap.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.coordination_candidates`: mandatory rows HL, Fe_HL_protonated, Fe_HL_deprotonated, Co_HL_protonated, Co_HL_deprotonated; numeric metrics G_Eh, spin_squared, excitation_eV, oscillator_strength. All models require atom-complete solvent/counterion/proton bookkeeping and applicable spin search; apparent nonconvergence is not proof a species is absent.
- `results.solution_cycles`: mandatory rows Fe_exchange, Co_exchange, proton_exchange; numeric metrics delta_G_kJ_mol, standard_state_correction_kJ_mol. Use one balanced exchange reference and explicit proton reservoir; bare Fe3+ binding in vacuum cannot be substituted for an unreported DMF experimental salt.
- `results.selectivity_tests`: mandatory rows binding_contrast, state_contrast, speciation_sensitivity; numeric metrics binding_difference_kJ_mol, excitation_difference_eV, CT_fraction_change. Keep binding preference separate from potential quenching channels, accept multiple Fe species consistent with evidence. TD/NTO alone does not produce a rate or detection limit.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.

**Blocked development contract:** only partial/bounded_failure status is accepted. blocked_solution_definition: DMF and competing Co(II) are confirmed, but the accessed main/SI do not fix sensing salt counterions, pH/proton reservoir or water content. Define those from source records or an explicitly authorized model before atom-complete Fe/Co exchange references. No invented salt/pH or calibrated selectivity is supplied.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
