# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

Use full source BCy2/o-phenyl phosphonate 2a and deethylated anion3, not only BMe2/OMe surrogate. Full anion is C20H31BO3P, charge-1 singlet; Li+ and MeCN are singlets. Source Li2O2 dimer has two anions, two Li and four MeCN (charge0 singlet). Each Li coordinates the exposed phosphoryl O of both anions and two MeCN N atoms; intramolecular O->B contact remains distinguishable. Use balanced 2 monomer -> dimer and MeCN association cycles. Dealkylation reaction is neutral+LiI -> Li.anion+EtI; do not subtract unlike neutral/anion total energies.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.coordination_layers`: mandatory rows full_anion, Li_anion, Li_anion_2MeCN, crystal_supported_dimer; numeric metrics P_O_A, B_O_A, electronic_Eh, G_Eh. Maintain full Cy and OEt groups and distinguish dimer versus monomer identities; every geometry needs genuine convergence and frequency/constraint evidence.
- `results.balanced_cycles`: mandatory rows Li_association, MeCN_association, dimerization, deethylation; numeric metrics delta_E_kJ_mol, delta_G_kJ_mol, distortion_kJ_mol. Recompute fragment/stoichiometry-balanced differences; explicit LiI/EtI or equivalent balanced deethylation accounting is required, never bare neutral-minus-anion energy.
- `results.truncation_and_mechanism`: mandatory rows small_vs_full, coordination_vs_aggregation; numeric metrics P_O_change_A, B_O_change_A, interaction_change_kJ_mol. A full dimer is required for aggregation credit and paired small/full models for truncation. Local isolated-anion results do not explain the whole salt; no electrolyte performance claims.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.
