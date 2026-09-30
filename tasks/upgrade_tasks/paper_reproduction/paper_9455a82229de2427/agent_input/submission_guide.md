# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Reactants SiN (0, doublet) and isoprene C5H8 (0, singlet) produce SiNC5H7 (0, singlet) plus H (0, doublet). Doublet SiNC5H8 addition/rearrangement structures share the reactant atom map. Use separated reactants as zero for E0=Eelectronic+ZPE at 0 K. Collision energy 25±1 kJ/mol and experimental channel exoergicity -162±27 kJ/mol are observations, not computed answers. Enumerate terminal-C1/C4 attack by Si and N, then at least ring closure and H-loss alternatives. Declare explored bond edits and remaining search limits.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.candidate_space`: mandatory rows terminal_C1_Si, terminal_C4_Si, terminal_C1_N, terminal_C4_N; numeric metrics lowest_E0_kJ_mol, product_reaction_E0_kJ_mol. Provide mapped graph-edit enumeration, attempted structures, state validity and products for the four attack families. Multiple seeds collapsing to one product are legitimate only with raw mapped evidence; no requirement for four distinct products.
- `results.connected_routes`: mandatory rows main_route, competitor_route; numeric metrics maximum_relative_E0_kJ_mol, reaction_E0_kJ_mol, collision_margin_kJ_mol. Submit ordered mapped nodes/edges, optimized endpoints, TS and IRC files or continuous no-barrier path evidence. Recompute all nodes relative to SiN+isoprene, including the free H atom.
- `results.accessibility`: mandatory rows thermodynamic_vs_kinetic, method_sensitivity; numeric metrics main_minus_competitor_kJ_mol, uncertainty_kJ_mol. Separate lowest-energy product, channel exoergicity and accessible barrier. Compare collision margins and demonstrate method/ZPE sensitivity; no 298 K equilibrium abundance or branching ratio inference.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
