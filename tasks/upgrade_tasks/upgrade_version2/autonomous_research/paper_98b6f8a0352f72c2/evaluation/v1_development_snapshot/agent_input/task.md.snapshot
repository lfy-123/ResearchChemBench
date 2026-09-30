# Scientific objective

Determine whether donor substitution and solvent effects on absorption, emission and CT survive matched torsional geometry and consistent state definitions.

# Public inputs and scientific boundaries

Select real members12a (NMe2, C24H19N3) and12d (NEt2, C26H23N3), neutral singlets, in CHCl3 and EtOAc. Each requires S0 preparation, vertical TD at S0, tracked relaxed S1 and vertical emission at S1; report the adiabatic energy separately. Use the mapped phenyl-phenazine single-bond torsion as common intervention. Calculate experimental kr=Phi/tau only if both measured values refer to the same conditions; 1/tau alone is total decay, not radiative rate.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **solvent_series.** Cover `12a_CHCl3`, `12a_EtOAc`, `12d_CHCl3`, `12d_EtOAc`. Save S0/S1 outputs, geometry and NTO evidence with solvent response convention; never equate absorption oscillator strength with measured radiative yield. Required numeric fields are `absorption_eV`, `emission_eV`, `adiabatic_eV`, `oscillator_strength`, `transition_dipole_D`, `CT_distance_A`.

2. **common_torsion.** Cover `12a_CHCl3`, `12a_EtOAc`, `12d_CHCl3`, `12d_EtOAc`. Freeze identical mapped phenyl-phenazine angle, compare released structures and track state; distinguish ground/excited geometry relaxation. Required numeric fields are `torsion_degree`, `absorption_eV`, `emission_eV`, `oscillator_strength`.

3. **rates_and_robustness.** Cover `radiative_convention`, `substitution_vs_solvent`, `state_sensitivity`. State refractive-index/local-field/degeneracy convention and formula, and whether an experimental Phi/tau comparison is available. Do not invent missing quantum yields or treat SI theoretical lifetimes as measurements. Required numeric fields are `theoretical_radiative_rate_s1`, `rate_uncertainty_s1`, `excitation_change_eV`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Thin-film nonradiative lifetimes and full device efficiency are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
