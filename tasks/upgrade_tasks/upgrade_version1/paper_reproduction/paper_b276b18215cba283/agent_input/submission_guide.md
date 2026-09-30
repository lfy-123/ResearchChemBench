# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use the neutral singlet single-arm C26H27NO3 and complete three-arm C66H69N3O3 graphs. Cisoid/transoid are mapped torsional families on each exocyclic arm, not a change of composition. Primary gas-phase calculations permit direct comparison with the source; a common ethanol continuum is the environment sensitivity, not a model of a membrane. Each full-model result requires arm partitions and matched transition densities.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.relaxed_models`: mandatory rows single_transoid, single_cisoid, three_transoid, three_cisoid; numeric metrics excitation_eV, oscillator_strength, G_Eh. Retain at least four low roots in the three-arm model with NTO and arm-resolved transition-density fractions; do not equate root labels across models.
- `results.arm_geometry_control`: mandatory rows single_on_three_transoid, single_on_three_cisoid, three_fixed_arm; numeric metrics excitation_eV, oscillator_strength, interarm_transfer_fraction. Extract mapped arm from full geometry under a declared cap rule; compare frozen and relaxed arm and complete model. Preserve graph/partition/constraint files.
- `results.transfer_and_medium`: mandatory rows gas_transfer, ethanol_transfer; numeric metrics single_shift_eV, three_shift_eV, difference_eV. Quantify whether transfer survives medium, state mapping and method/conformer uncertainty; actual full-model data are mandatory. No membrane or two-photon mechanism inferred.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.

Metric applicability clarification: For single_on_three_transoid and single_on_three_cisoid, interarm_transfer_fraction is null with metric_applicability_reason: the capped single-arm object has no second arm. Excitation, oscillator strength and the mapped frozen-arm calculation remain mandatory. The three_fixed_arm row still requires a numeric interarm transfer fraction from the full three-arm transition density, with explicit fragment partitions and normalization; null is forbidden there.
