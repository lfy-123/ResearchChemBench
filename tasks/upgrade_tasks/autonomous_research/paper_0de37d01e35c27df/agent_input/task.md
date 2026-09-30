# Scientific objective

Test whether oxidation-induced sulfur approach is accompanied by the occupation, spin and bonding changes required for a two-center three-electron interpretation.

# Public inputs and scientific boundaries

Use the exact mapped norDTCO C10H14S2 graph already supplied, with S16/S17, and source DTCO (1,5-dithiacyclooctane C6H12S2) as the rigidity control. Each neutral is charge 0 singlet and radical cation charge +1 doublet. Compare each at its own relaxed backbone and vertically on the other oxidation-state geometry in gas phase. A geometric S...S contact is not a covalent edge in the starting neutral graph.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **oxidation_pairs.** Cover `nor_neutral`, `nor_cation`, `DTCO_neutral`, `DTCO_cation`. Require valid structures, unrestricted spin diagnostic, natural/SOMO occupations and density/bond analysis. Bond order definition must be consistent across both topologies. Required numeric fields are `SS_distance_A`, `electronic_Eh`, `spin_S_total`, `bond_order`.

2. **vertical_geometry.** Cover `nor_cation_on_neutral`, `nor_neutral_on_cation`, `DTCO_cation_on_neutral`, `DTCO_neutral_on_cation`. Pair fixed backbone and relaxed state evidence to separate mechanical contraction from electronic bonding. Retain same atom map. Required numeric fields are `SS_distance_A`, `electronic_Eh`, `bond_order`, `antibonding_occupation`.

3. **bonding_interpretation.** Cover `rigidity_contrast`, `analysis_sensitivity`. Compare contraction against orbital occupation/spin localization and independent density evidence. A short distance without electronic support weakens the hypothesis; ring opening must have a new topology ID. Required numeric fields are `contraction_difference_A`, `bond_order_change`, `occupation_change`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Dication chemistry, full aryl series and electrochemical reversibility are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
