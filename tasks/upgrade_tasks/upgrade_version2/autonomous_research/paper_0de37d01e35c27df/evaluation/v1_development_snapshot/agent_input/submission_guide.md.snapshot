# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use the exact mapped norDTCO C10H14S2 graph already supplied, with S16/S17, and source DTCO (1,5-dithiacyclooctane C6H12S2) as the rigidity control. Each neutral is charge 0 singlet and radical cation charge +1 doublet. Compare each at its own relaxed backbone and vertically on the other oxidation-state geometry in gas phase. A geometric S...S contact is not a covalent edge in the starting neutral graph.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.oxidation_pairs`: mandatory rows nor_neutral, nor_cation, DTCO_neutral, DTCO_cation; numeric metrics SS_distance_A, electronic_Eh, spin_S_total, bond_order. Require valid structures, unrestricted spin diagnostic, natural/SOMO occupations and density/bond analysis. Bond order definition must be consistent across both topologies.
- `results.vertical_geometry`: mandatory rows nor_cation_on_neutral, nor_neutral_on_cation, DTCO_cation_on_neutral, DTCO_neutral_on_cation; numeric metrics SS_distance_A, electronic_Eh, bond_order, antibonding_occupation. Pair fixed backbone and relaxed state evidence to separate mechanical contraction from electronic bonding. Retain same atom map.
- `results.bonding_interpretation`: mandatory rows rigidity_contrast, analysis_sensitivity; numeric metrics contraction_difference_A, bond_order_change, occupation_change. Compare contraction against orbital occupation/spin localization and independent density evidence. A short distance without electronic support weakens the hypothesis; ring opening must have a new topology ID.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
