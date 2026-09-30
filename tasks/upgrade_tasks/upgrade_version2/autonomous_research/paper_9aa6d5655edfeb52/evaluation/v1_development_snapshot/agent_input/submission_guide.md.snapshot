# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use fused 2a C18H20B10 and nonfused source precursor1a C18H21B10Br, both neutral singlets. Precursor1a is 1-(8-bromonaphthalen-1-yl)-2-phenyl-o-carborane; it is not a pure geometric un-fusion because Br/H composition differs. Public graph edits remove the B3-aryl fusion edge, restore B3-H and add aryl-Br. Preserve the closo cage adjacency and mapped cage C1-C2 axis; a multicenter cage edge is not an ordinary two-center bond-order assertion. Primary THF continuum.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.fusion_pair`: mandatory rows fused2a, nonfused1a; numeric metrics excitation_eV, oscillator_strength, cage_CC_A, lowest_frequency_cm1. Require NTO/state character, valid ground-state modes and both distinct chemical identities; no KS-gap or NICS proxy for quantum yield.
- `results.cage_displacement`: mandatory rows 2a_minus, 2a_plus, 1a_minus, 1a_plus; numeric metrics displacement_A, relative_E_kJ_mol, excitation_eV, oscillator_strength. Use symmetric ±0.05 angstrom coordinate perturbations around each own relaxed C-C reference as design points, with fixed and orthogonally relaxed versions. The displacement size is a chosen intervention, not a reference tolerance.
- `results.causal_limits`: mandatory rows fusion_vs_motion, method_sensitivity; numeric metrics excitation_change_eV, response_eV_per_A, uncertainty_eV. Keep Br substitution as a chemical confound, report vibrational/displacement response and trigger higher-level diagnostics for near-degenerate state mixing. A compound conclusion need not isolate fusion uniquely.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
