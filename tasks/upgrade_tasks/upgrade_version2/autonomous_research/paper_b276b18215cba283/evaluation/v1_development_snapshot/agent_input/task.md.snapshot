# Scientific objective

Test whether the single-arm conformational optical shift survives in the full three-arm chromophore, and distinguish arm geometry from inter-arm electronic mixing.

# Public inputs and scientific boundaries

Use the neutral singlet single-arm C26H27NO3 and complete three-arm C66H69N3O3 graphs. Cisoid/transoid are mapped torsional families on each exocyclic arm, not a change of composition. Primary gas-phase calculations permit direct comparison with the source; a common ethanol continuum is the environment sensitivity, not a model of a membrane. Each full-model result requires arm partitions and matched transition densities.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **relaxed_models.** Cover `single_transoid`, `single_cisoid`, `three_transoid`, `three_cisoid`. Retain at least four low roots in the three-arm model with NTO and arm-resolved transition-density fractions; do not equate root labels across models. Required numeric fields are `excitation_eV`, `oscillator_strength`, `G_Eh`.

2. **arm_geometry_control.** Cover `single_on_three_transoid`, `single_on_three_cisoid`, `three_fixed_arm`. Extract mapped arm from full geometry under a declared cap rule; compare frozen and relaxed arm and complete model. Preserve graph/partition/constraint files. Required numeric fields are `excitation_eV`, `oscillator_strength`, `interarm_transfer_fraction`.

3. **transfer_and_medium.** Cover `gas_transfer`, `ethanol_transfer`. Quantify whether transfer survives medium, state mapping and method/conformer uncertainty; actual full-model data are mandatory. No membrane or two-photon mechanism inferred. Required numeric fields are `single_shift_eV`, `three_shift_eV`, `difference_eV`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Two-photon cross sections, membrane aggregates and absolute lifetimes are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.

Metric applicability clarification: For single_on_three_transoid and single_on_three_cisoid, interarm_transfer_fraction is null with metric_applicability_reason: the capped single-arm object has no second arm. Excitation, oscillator strength and the mapped frozen-arm calculation remain mandatory. The three_fixed_arm row still requires a numeric interarm transfer fraction from the full three-arm transition density, with explicit fragment partitions and normalization; null is forbidden there.
