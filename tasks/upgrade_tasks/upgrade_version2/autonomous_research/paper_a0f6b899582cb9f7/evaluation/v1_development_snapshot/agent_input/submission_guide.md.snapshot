# Submission guide

Use `report/results.json` and `report/report.md`. The schema defines the exact core matrix; no universal free-text result can replace it.

M3 is neutral singlet 2,5-di(thiophen-2-yl)pyrazine C12H8N2S2. Use the independently reviewed builder-defined finite graphs PM6_BDD_T2_Me (C20H12O2S4), BTP_eC9_core_Me (C22H14N4S5), and BTP_eC9_full_pi_Me (C48H18F4N8O2S5), all neutral singlets. Their atom-indexed bonds and exact cut/cap boundaries are supplied in objects.json and fragment_models/. BTP core atoms 1–31 map identically into the larger model; added/removed caps and hydrogens must be explicitly mapped in paired comparisons. These are bounded source-grounded models, not recovered author coordinates or complete PM6/BTP-eC9 materials. No arbitrary fragment replacement is authorized.

`object_records` gives validated charge/spin/graph/geometry mappings for every object used. `calculation_records` links each actual job to raw input/output; Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage. All IDs in results must resolve to these records. Each required row names `calculation_ids`, `atom_map_file`, `raw_files`, `data_table_file`, and numeric `metrics`; tables contain all states/angles/conformers, not just extrema. Evaluators open these files.

- `results.contact_models`: mandatory rows PM6_face, PM6_edge, BTP_core_face, BTP_core_edge; numeric metrics interaction_kJ_mol, distortion_kJ_mol. Each pair requires complete graph, contact map and several starting orientations at fixed composition; compare released versus frozen fragments.
- `results.decomposition`: mandatory rows PM6_pair, BTP_pair; numeric metrics electrostatic_kJ_mol, dispersion_kJ_mol, exchange_kJ_mol, induction_kJ_mol. Use a single justified decomposition and identical fragmentation; terms are model-dependent, not unique causal observables. Recompute total and residual terms.
- `results.truncation_and_tensor`: mandatory rows larger_fragment, M3_tensor; numeric metrics primary_interaction_kJ_mol, control_interaction_kJ_mol, quadrupole_zz_eA2. At least one actual larger-fragment pair is core. Report all six independent tensor components with origin/axes; Qzz alone cannot prove dual binding or PCE.

Provide two real `hypothesis_tests`, an actual quantitative `sensitivity` pair and a bounded `conclusion`. The `core_matrix_complete` flag is a claim to verify, not self-certification. An `evidenced_collapse` row needs two or more raw artifacts and a mapped retained endpoint; its table must establish a real basin/identity mapping. It cannot replace a missing method calculation, failed job or aggregate comparison.

Use `partial` or `bounded_failure` with `failure_report` and actual diagnostics for unfinished work. Such submissions are accepted for audit but do not meet scientific completion. `complete` requires every core row and at least one successful real job; the scientific evaluator additionally verifies all required jobs, objects, states, arithmetic and files.

Resource times and starts are measured, not inferred from work-package count. Engine time, summed jobs and elapsed calendar time are separate. Optional work receives no required fields or mandatory failure tests. All synthetic regression fixtures are temporary format-only data and must not be submitted as research.

**Reviewed finite model contract:** complete, partial and bounded-failure submissions are distinguished by the retained scientific evidence gates. The finite fragment graph definitions and cap rules are now materialized after independent source review. Actual contact, decomposition, truncation and tensor validation remains mandatory; topology review alone is not scientific completion.


## Prelaunch diagnostic reporting

A prerequisite failure before engine launch may use empty object_records and calculation_records (where defined), empty conclusion.supporting_record_ids, and zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic evidence and failure_report. Describe the intended protocol and identify software that was not run. Do not invent a geometry, frequency, energy or job. Complete submissions retain every required scientific endpoint and actual successful engine evidence.

Metric applicability clarification: For the isolated M3_tensor row, primary_interaction_kJ_mol and control_interaction_kJ_mol are null with metric_applicability_reason because no partner is present. The full quadrupole tensor, declared origin/axes and numeric quadrupole_zz_eA2 remain mandatory. The larger_fragment row still requires both real interaction energies, a mapped larger-fragment pair and the shared M3 tensor; null cannot waive that truncation comparison. The reviewed finite fragment identities remain mandatory; the truncation-pair calculation cannot be waived.
