# Scientific objective

Separate local dealkylation, Li coordination, MeCN coordination and real dimerization contributions to P-O...B geometry through atom-balanced hierarchical models.

# Public inputs and scientific boundaries

Use full source BCy2/o-phenyl phosphonate 2a and deethylated anion3, not only BMe2/OMe surrogate. Full anion is C20H31BO3P, charge-1 singlet; Li+ and MeCN are singlets. Source Li2O2 dimer has two anions, two Li and four MeCN (charge0 singlet). Each Li coordinates the exposed phosphoryl O of both anions and two MeCN N atoms; intramolecular O->B contact remains distinguishable. Use balanced 2 monomer -> dimer and MeCN association cycles. Dealkylation reaction is neutral+LiI -> Li.anion+EtI; do not subtract unlike neutral/anion total energies.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **coordination_layers.** Cover `full_anion`, `Li_anion`, `Li_anion_2MeCN`, `crystal_supported_dimer`. Maintain full Cy and OEt groups and distinguish dimer versus monomer identities; every geometry needs genuine convergence and frequency/constraint evidence. Required numeric fields are `P_O_A`, `B_O_A`, `electronic_Eh`, `G_Eh`.

2. **balanced_cycles.** Cover `Li_association`, `MeCN_association`, `dimerization`, `deethylation`. Recompute fragment/stoichiometry-balanced differences; explicit LiI/EtI or equivalent balanced deethylation accounting is required, never bare neutral-minus-anion energy. Required numeric fields are `delta_E_kJ_mol`, `delta_G_kJ_mol`, `distortion_kJ_mol`.

3. **truncation_and_mechanism.** Cover `small_vs_full`, `coordination_vs_aggregation`. A full dimer is required for aggregation credit and paired small/full models for truncation. Local isolated-anion results do not explain the whole salt; no electrolyte performance claims. Required numeric fields are `P_O_change_A`, `B_O_change_A`, `interaction_change_kJ_mol`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** A smaller local-only version would need separate scope deletion of aggregation; the present first version retains a mandatory full dimer. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
