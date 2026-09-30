# Scientific objective

Test whether BN incorporation changes state energies and charge separation beyond geometry and method uncertainty, using matched BN-AkFlu and CC-AkFlu graphs.

# Public inputs and scientific boundaries

BN-AkFlu 5a is C22H14B2N2 (40 atoms in the supplied actual graph), not the H15 typo in an old route. CC-AkFlu 5b is C26H14, 40 atoms, from SI Table S22. Both are neutral singlets in gas phase. Use each relaxed geometry and cross-evaluate on a common mapped heavy-atom scaffold; replacing B/N by C is a chemical intervention with changed nuclear charges. Track physical states via NTO/density overlap, not root numbers alone; retain six vertical roots and descriptors for the first four source baseline roots.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **relaxed_states.** Cover `BN_relaxed`, `CC_relaxed`. Preserve full S1-S6 table and S1-S4 density-analysis raw data. Sr is integral sqrt(rho_h*rho_e) over space for normalized densities; D is centroid separation. Required numeric fields are `matched_excitation_eV`, `oscillator_strength`, `D_A`, `Sr`.

2. **common_scaffold.** Cover `BN_on_CC`, `CC_on_BN`. Map the common framework and show both cross geometries. Frozen points are not optimized minima. Use NTO/transition-density mapping to avoid claiming a root switch as a direct chemical shift. Required numeric fields are `matched_excitation_eV`, `oscillator_strength`, `D_A`, `Sr`.

3. **attribution.** Cover `chemical_effect`, `geometry_effect`, `analysis_convergence`. Recalculate paired changes and analysis-grid/amplitude sensitivity independently of excitation-energy convergence. Accept a mixed or unresolved BN effect if all controls are computed. Required numeric fields are `excitation_change_eV`, `D_change_A`, `Sr_change`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** New-molecule screening, quantum yield, charge mobility and bulk packing claims are excluded. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
