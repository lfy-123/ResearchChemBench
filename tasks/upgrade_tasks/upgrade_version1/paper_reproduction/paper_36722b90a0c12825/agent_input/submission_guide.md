# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use the complete C48H26F12N14 host: E and Z each free (charge 0, singlet) and with one chloride (charge -1, singlet), plus Cl- (singlet). Ac means acetone, not acetonitrile. Primary solution boundary: acetone, 298.15 K, 1 M standard state; convert any 1 atm RRHO terms explicitly. Sum over distinct validated conformers within each E/Z family, not between photostationary E and Z populations. TBA+ is a counterion context; an explicit TBACl sensitivity must use balanced composition. A second host is a separately chosen optional transfer check.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.species_ensembles`: mandatory rows E_free, E_bound, Z_free, Z_bound, chloride; numeric metrics electronic_energy_Eh, ZPE_Eh, thermal_correction_Eh, G_1M_Eh. Validate minima and conformer coverage for all four chemical states; isolate electronic, ZPE, thermal and concentration corrections. Include conformer weights and all attempted structures in raw tables.
- `results.binding_cycle`: mandatory rows E_bind, Z_bind, Z_minus_E; numeric metrics delta_G_kJ_mol, delta_E_kJ_mol, conformational_cost_kJ_mol. Recompute G(host.Cl)-G(host)-G(Cl) for each family and DeltaDeltaG=DeltaGbind(Z)-DeltaGbind(E). Report interaction and distortion with compatible fragment geometry and BSSE conventions.
- `results.intervention`: mandatory rows frozen_host, solvent_or_ion_pair; numeric metrics primary_contrast_kJ_mol, control_contrast_kJ_mol, change_kJ_mol. At least one frozen/relaxed host contrast and one actual solvent/counterion sensitivity must challenge the interpretation. Do not use PSS as Boltzmann population.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
