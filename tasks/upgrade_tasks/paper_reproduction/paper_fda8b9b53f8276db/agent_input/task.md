# Scientific objective

Determine whether local bond residuals and cis/trans preference are attributable to torsional conformation or medium, keeping the original six-bond cis validation separate from thermochemistry.

# Author-provided scientific guidance

The authors compare a gas-phase cis local minimum with crystal intramolecular bonds using Gaussian03 B3LYP/6-311+G(2d,p). The crystal pyridyl orientation differs; a local minimum need not be globally lowest. The paired cis/trans solvent and torsion controls are benchmark extensions.

# Public inputs and scientific boundaries

Use neutral singlet 6,7-dimethyl-2-(pyridin-2-yl)quinoxaline, C15H13N3, from CCDC2433822. Cis/trans is the mapped N1-C1-C2-N2 torsion; preserve deposited labels. Primary gas phase and acetonitrile continuum at 298.15 K, consistent 1 M molecular convention for solution. Six bonds are exactly those in experimental_bonds.json; seven SI or 33 CIF bond sets must not enter this RMSE.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **conformer_environment.** Cover `cis_gas`, `trans_gas`, `cis_MeCN`, `trans_MeCN`. Validate graph/minima, searches and environment-specific conformer identity; a released candidate may merge into another basin with actual evidence. Required numeric fields are `electronic_Eh`, `G_Eh`, `torsion_degree`.

2. **six_bond_residuals.** Cover `cis_gas`, `trans_gas`, `cis_MeCN`, `trans_MeCN`. Recompute six unrounded residuals and RMSE against the authorized experimental distances. Separate any larger bond statistics; include OLS with intercept only if called R squared. Required numeric fields are `C1_C2_A`, `C2_C3_A`, `N1_C1_A`, `N2_C2_A`, `N3_C3_A`, `C1_C10_A`, `RMSE_A`.

3. **torsional_intervention.** Cover `gas_fixed_vs_relaxed`, `MeCN_fixed_vs_relaxed`. A defined mapped torsion restraint and relaxed counterpart distinguish geometric from solvent effects. Nonstationary restrained points receive no borrowed harmonic G. Required numeric fields are `torsion_degree`, `delta_E_kJ_mol`, `residual_change_A`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** CIF neighbor clusters, solid-state explanation and NMR are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
