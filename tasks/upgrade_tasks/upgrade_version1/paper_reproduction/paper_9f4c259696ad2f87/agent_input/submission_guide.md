# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use PXX1 C43H28O3 and PXX2 C50H30O4, neutral singlets; acid is neutral B(C6F5)3. Each PXX has 0, 1 and 2 acid units; PXX1 has one carbonyl, so its second acid explores the available ether/carbonyl-site competition as a new candidate, not an asserted second independent ketone. PXX2 has two carbonyls. All whole complexes are neutral singlets. CH2Cl2 is the shared primary medium. Compare sequential acid association reactions, never bare total energies of different acid counts. Use 298.15 K and 1 M as explicit development thermochemistry conventions; no equilibrium population is inferred without concentration evidence.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.stoichiometric_series`: mandatory rows PXX1_acid0, PXX1_acid1, PXX1_acid2, PXX2_acid0, PXX2_acid1, PXX2_acid2; numeric metrics G_Eh, excitation_eV, oscillator_strength, CT_distance_A. Require actual conformer/site attempts, stoichiometric identities and matched transition densities for every acid count; evidenced dissociation/collapse is reportable.
- `results.balanced_binding`: mandatory rows PXX1_step1, PXX1_step2, PXX2_step1, PXX2_step2; numeric metrics delta_G_kJ_mol, interaction_kJ_mol, distortion_kJ_mol. Recompute PXX.acid_n minus PXX.acid_(n-1) minus free acid with common thermochemistry and 1 M correction. Demonstrate composition balance and conformer effects.
- `results.geometry_and_spectrum`: mandatory rows PXX1_acid_removed, PXX2_acid_removed, titration_discrimination; numeric metrics excitation_change_eV, oscillator_strength_change, uncertainty_eV. Remove acid at the same PXX geometry and compare independently relaxed PXX; compare observed trend without forcing unique occupancy from similar spectra. Preserve digitization/concentration limits.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
