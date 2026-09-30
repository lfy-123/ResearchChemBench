# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Full neutral DQCS is C31H27N3O3 singlet; retain the phenolic hydrogen present in the three source graphs. Metal complexes all have charge+2; Cd/Co/Ni source multiplicities are1/2/1. Primary medium DMSO. A free ligand extracted from a complex has charge0 singlet, not the parent complex charge. Identify ligand versus metal density partitions and fixed-geometry atom correspondence.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.relaxed_species`: mandatory rows DQCS, Cd_DQCS, Co_DQCS, Ni_DQCS; numeric metrics excitation_eV, oscillator_strength, metal_transition_fraction, spin_squared. Compute like-defined TD/NTO observables with six roots or a justified larger window. Co transitions retain doublet reference/spin character rather than forced singlet labels.
- `results.frozen_ligand`: mandatory rows ligand_from_Cd, ligand_from_Co, ligand_from_Ni; numeric metrics excitation_eV, oscillator_strength, ligand_distortion_kJ_mol. Extract identical complete ligand graph/charge from each source complex, retaining all hydrogens; pair frozen and relaxed ligand results.
- `results.attribution`: mandatory rows Cd_effect, Co_effect, Ni_effect, method_sensitivity; numeric metrics electronic_shift_eV, geometry_shift_eV, uncertainty_eV. Separate geometry and metal contributions with state matching and real density fractions. Do not use gap/hardness/electrophilicity algebra as independent causal evidence.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
