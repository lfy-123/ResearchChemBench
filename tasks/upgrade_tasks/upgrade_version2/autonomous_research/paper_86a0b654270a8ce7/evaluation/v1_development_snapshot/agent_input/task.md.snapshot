# Scientific objective

Determine whether the relative stability of two Ir–salen–NHC coordination isomers survives conformational, low-frequency and method controls and whether stacking offers a supported local explanation.

# Public inputs and scientific boundaries

Both complete IrC60H63N4O2 isomers are neutral singlets, in THF at 339 K. Preserve Ir coordination identity; report E, solvent contribution, ZPE/thermal and low-frequency correction separately with one standard state. The source predicts a preference, but a contrary converged method is not discarded. Contact-separation restraints measure interaction plus deformation and must not be called pure pi-stacking energies.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **isomer_ensembles.** Cover `isomer1`, `isomer2`. Use low-energy conformer coverage and frequency evidence with identical 339 K convention; reconstruct ensemble G and document degeneracy. Required numeric fields are `electronic_Eh`, `solvation_Eh`, `thermal_Eh`, `low_frequency_Eh`, `G_339K_Eh`.

2. **stacking_intervention.** Cover `isomer1_contact`, `isomer2_contact`. Submit mapped aromatic ring atoms and frozen/released contacts, controlling other geometry. Distortion cannot be removed by merely labeling the difference stacking. Required numeric fields are `centroid_distance_A`, `relative_angle_degree`, `delta_E_kJ_mol`, `distortion_kJ_mol`.

3. **ranking_robustness.** Cover `method_change`, `thermal_model_change`. Quantify sign and interval under actual methods and thermal treatment; unresolved ranking after complete data is acceptable. Isolated yields are not a scored equilibrium ratio. Required numeric fields are `delta_G_2_minus_1_kJ_mol`, `uncertainty_kJ_mol`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Complete interconversion networks and exact isolated yields are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
