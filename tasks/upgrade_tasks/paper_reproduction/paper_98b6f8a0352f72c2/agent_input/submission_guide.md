# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Select real members12a (NMe2, C24H19N3) and12d (NEt2, C26H23N3), neutral singlets, in CHCl3 and EtOAc. Each requires S0 preparation, vertical TD at S0, tracked relaxed S1 and vertical emission at S1; report the adiabatic energy separately. Use the mapped phenyl-phenazine single-bond torsion as common intervention. Calculate experimental kr=Phi/tau only if both measured values refer to the same conditions; 1/tau alone is total decay, not radiative rate.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.solvent_series`: mandatory rows 12a_CHCl3, 12a_EtOAc, 12d_CHCl3, 12d_EtOAc; numeric metrics absorption_eV, emission_eV, adiabatic_eV, oscillator_strength, transition_dipole_D, CT_distance_A. Save S0/S1 outputs, geometry and NTO evidence with solvent response convention; never equate absorption oscillator strength with measured radiative yield.
- `results.common_torsion`: mandatory rows 12a_CHCl3, 12a_EtOAc, 12d_CHCl3, 12d_EtOAc; numeric metrics torsion_degree, absorption_eV, emission_eV, oscillator_strength. Freeze identical mapped phenyl-phenazine angle, compare released structures and track state; distinguish ground/excited geometry relaxation.
- `results.rates_and_robustness`: mandatory rows radiative_convention, substitution_vs_solvent, state_sensitivity; numeric metrics theoretical_radiative_rate_s1, rate_uncertainty_s1, excitation_change_eV. State refractive-index/local-field/degeneracy convention and formula, and whether an experimental Phi/tau comparison is available. Do not invent missing quantum yields or treat SI theoretical lifetimes as measurements.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
