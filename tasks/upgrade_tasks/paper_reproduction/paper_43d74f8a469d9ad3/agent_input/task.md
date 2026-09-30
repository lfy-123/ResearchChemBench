# Scientific objective

Test whether restriction of the same aryl rotation changes S0/S1 energetics and transition character across two source boron dyes, distinguishing geometric restriction from chemical substitution.

# Author-provided scientific guidance

The source proposes steric shielding/restricted rotation; its torsion subsection uses PBE0/def2-SVP and a 24-point ground-state scan, while general TD calculations use M06-2X/6-311++G(d,p). These are distinct source protocols. The benchmark adds state-tracked S1 scans and relaxed/restrained comparison; a ground-state scan maximum is not a transition state and does not predict bleaching rates.

# Public inputs and scientific boundaries

Core comparison: Scheme1 compound1 C23H20BNO3 and compound2 C24H22BNO4, neutral singlets. Compound1 is fixed by CCDC2441197; compound2 adds the para-to-phenoxy methoxy group shown in Scheme1, retaining the 3,5-dimethylphenyl boron substituent. Use mapped X-B-Cipso-Cortho on that aryl branch in both. Primary gas phase and an explicitly identical optical solvent sensitivity. Source SI coordinate labels S5/S6 conflict with Scheme1 identities; their unchecked coordinate assignments are not authorized.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **torsion_profiles.** Cover `dye1_S0`, `dye1_S1`, `dye2_S0`, `dye2_S1`. Store a numeric angle-energy-property CSV with mapped atoms at each point, constrained degrees of freedom and forward/backward state overlap; include released anchors. Required numeric fields are `torsional_range_kJ_mol`, `reference_angle_degree`, `tracked_excitation_eV`.

2. **restriction_control.** Cover `dye1_restricted_vs_free`, `dye2_restricted_vs_free`. Use the same mapped angle intervention in both compounds, with actual frozen and relaxed calculations. Root switching is recorded, not smoothed away. Required numeric fields are `excitation_change_eV`, `oscillator_strength_change`, `relaxation_kJ_mol`.

3. **continuity_and_robustness.** Cover `state_following`, `method_or_grid`. Demonstrate TD root-window/step-size or method sensitivity and identify discontinuities. Do not extrapolate S0 resistance to an absolute photobleaching rate. Required numeric fields are `minimum_state_overlap`, `energy_change_eV`, `profile_change_kJ_mol`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Nonadiabatic trajectories, conical intersections and absolute lifetime prediction are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
