# Scientific objective

Determine whether E/Z photoisomerization changes chloride affinity through host preorganization, host distortion, or the common solvent environment. Test a closed binding cycle for the (1,3)Ph host rather than infer affinity from two bound E conformers.

# Author-provided scientific guidance

The authors associate triazole preorganization and cavity accessibility with light-switchable chloride binding. They use Gaussian 16 B3LYP/6-31G*, D3(BJ), PCM acetone/UFF cavity, harmonic corrections at 298.15 K and counterpoise treatment of binding. Their (1,3)Ph titration constants overlap in uncertainty; the strong-switch claim must not be imposed on this host. The complete E/Z ensemble cycle and geometry/environment interventions below are benchmark extensions, not a claim that the source validated them.

# Public inputs and scientific boundaries

Use the complete C48H26F12N14 host: E and Z each free (charge 0, singlet) and with one chloride (charge -1, singlet), plus Cl- (singlet). Ac means acetone, not acetonitrile. Primary solution boundary: acetone, 298.15 K, 1 M standard state; convert any 1 atm RRHO terms explicitly. Sum over distinct validated conformers within each E/Z family, not between photostationary E and Z populations. TBA+ is a counterion context; an explicit TBACl sensitivity must use balanced composition. A second host is a separately chosen optional transfer check.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **species_ensembles.** Cover `E_free`, `E_bound`, `Z_free`, `Z_bound`, `chloride`. Validate minima and conformer coverage for all four chemical states; isolate electronic, ZPE, thermal and concentration corrections. Include conformer weights and all attempted structures in raw tables. Required numeric fields are `electronic_energy_Eh`, `ZPE_Eh`, `thermal_correction_Eh`, `G_1M_Eh`.

2. **binding_cycle.** Cover `E_bind`, `Z_bind`, `Z_minus_E`. Recompute G(host.Cl)-G(host)-G(Cl) for each family and DeltaDeltaG=DeltaGbind(Z)-DeltaGbind(E). Report interaction and distortion with compatible fragment geometry and BSSE conventions. Required numeric fields are `delta_G_kJ_mol`, `delta_E_kJ_mol`, `conformational_cost_kJ_mol`.

3. **intervention.** Cover `frozen_host`, `solvent_or_ion_pair`. At least one frozen/relaxed host contrast and one actual solvent/counterion sensitivity must challenge the interpretation. Do not use PSS as Boltzmann population. Required numeric fields are `primary_contrast_kJ_mol`, `control_contrast_kJ_mol`, `change_kJ_mol`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Complete titration fitting, exact PSS composition and device switching efficiency are optional and unscored. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
