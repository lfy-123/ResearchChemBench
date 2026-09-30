# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

BN-AkFlu 5a is C22H14B2N2 (40 atoms in the supplied actual graph), not the H15 typo in an old route. CC-AkFlu 5b is C26H14, 40 atoms, from SI Table S22. Both are neutral singlets in gas phase. Use each relaxed geometry and cross-evaluate on a common mapped heavy-atom scaffold; replacing B/N by C is a chemical intervention with changed nuclear charges. Track physical states via NTO/density overlap, not root numbers alone; retain six vertical roots and descriptors for the first four source baseline roots.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.relaxed_states`: mandatory rows BN_relaxed, CC_relaxed; numeric metrics matched_excitation_eV, oscillator_strength, D_A, Sr. Preserve full S1-S6 table and S1-S4 density-analysis raw data. Sr is integral sqrt(rho_h*rho_e) over space for normalized densities; D is centroid separation.
- `results.common_scaffold`: mandatory rows BN_on_CC, CC_on_BN; numeric metrics matched_excitation_eV, oscillator_strength, D_A, Sr. Map the common framework and show both cross geometries. Frozen points are not optimized minima. Use NTO/transition-density mapping to avoid claiming a root switch as a direct chemical shift.
- `results.attribution`: mandatory rows chemical_effect, geometry_effect, analysis_convergence; numeric metrics excitation_change_eV, D_change_A, Sr_change. Recalculate paired changes and analysis-grid/amplitude sensitivity independently of excitation-energy convergence. Accept a mixed or unresolved BN effect if all controls are computed.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
