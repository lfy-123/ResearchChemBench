# Scientific objective

Discriminate pi-extension, molecular distortion and Lewis-acid coordination as explanations of PXX optical shifts while testing whether spectra identify a unique acid stoichiometry.

# Author-provided scientific guidance

The authors propose enhanced carbonyl acceptor strength and PXX-to-ketone/acid charge transfer. Gaussian 16 B3LYP/6-31G(d) PCM(CH2Cl2) is described in SI methods; the main Fig7 caption states 6-311G(d), which must be disclosed as a source discrepancy. SI p167 reports a single titration equivalence point for two-ketone compound 2 and explicitly leaves one/two site occupancy ambiguous. The full 0/1/2 matrix and frozen acid-removal controls below extend the source.

# Public inputs and scientific boundaries

Use PXX1 C43H28O3 and PXX2 C50H30O4, neutral singlets; acid is neutral B(C6F5)3. Each PXX has 0, 1 and 2 acid units; PXX1 has one carbonyl, so its second acid explores the available ether/carbonyl-site competition as a new candidate, not an asserted second independent ketone. PXX2 has two carbonyls. All whole complexes are neutral singlets. CH2Cl2 is the shared primary medium. Compare sequential acid association reactions, never bare total energies of different acid counts. Use 298.15 K and 1 M as explicit development thermochemistry conventions; no equilibrium population is inferred without concentration evidence.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **stoichiometric_series.** Cover `PXX1_acid0`, `PXX1_acid1`, `PXX1_acid2`, `PXX2_acid0`, `PXX2_acid1`, `PXX2_acid2`. Require actual conformer/site attempts, stoichiometric identities and matched transition densities for every acid count; evidenced dissociation/collapse is reportable. Required numeric fields are `G_Eh`, `excitation_eV`, `oscillator_strength`, `CT_distance_A`.

2. **balanced_binding.** Cover `PXX1_step1`, `PXX1_step2`, `PXX2_step1`, `PXX2_step2`. Recompute PXX.acid_n minus PXX.acid_(n-1) minus free acid with common thermochemistry and 1 M correction. Demonstrate composition balance and conformer effects. Required numeric fields are `delta_G_kJ_mol`, `interaction_kJ_mol`, `distortion_kJ_mol`.

3. **geometry_and_spectrum.** Cover `PXX1_acid_removed`, `PXX2_acid_removed`, `titration_discrimination`. Remove acid at the same PXX geometry and compare independently relaxed PXX; compare observed trend without forcing unique occupancy from similar spectra. Preserve digitization/concentration limits. Required numeric fields are `excitation_change_eV`, `oscillator_strength_change`, `uncertainty_eV`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** FRET, full concentration dynamics and absolute emission efficiency are outside the core. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
