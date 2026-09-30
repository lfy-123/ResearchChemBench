# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use neutral singlet 6,7-dimethyl-2-(pyridin-2-yl)quinoxaline, C15H13N3, from CCDC2433822. Cis/trans is the mapped N1-C1-C2-N2 torsion; preserve deposited labels. Primary gas phase and acetonitrile continuum at 298.15 K, consistent 1 M molecular convention for solution. Six bonds are exactly those in experimental_bonds.json; seven SI or 33 CIF bond sets must not enter this RMSE.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.conformer_environment`: mandatory rows cis_gas, trans_gas, cis_MeCN, trans_MeCN; numeric metrics electronic_Eh, G_Eh, torsion_degree. Validate graph/minima, searches and environment-specific conformer identity; a released candidate may merge into another basin with actual evidence.
- `results.six_bond_residuals`: mandatory rows cis_gas, trans_gas, cis_MeCN, trans_MeCN; numeric metrics C1_C2_A, C2_C3_A, N1_C1_A, N2_C2_A, N3_C3_A, C1_C10_A, RMSE_A. Recompute six unrounded residuals and RMSE against the authorized experimental distances. Separate any larger bond statistics; include OLS with intercept only if called R squared.
- `results.torsional_intervention`: mandatory rows gas_fixed_vs_relaxed, MeCN_fixed_vs_relaxed; numeric metrics torsion_degree, delta_E_kJ_mol, residual_change_A. A defined mapped torsion restraint and relaxed counterpart distinguish geometric from solvent effects. Nonstationary restrained points receive no borrowed harmonic G.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
