# Scientific objective

Explain spectral differences across source monomers1a-1d by testing electronic substitution/topology effects against common local geometry and matched transition character.

# Author-provided scientific guidance

The authors use Gaussian16 B3LYP/6-31+G(d,p), frequency validation and TDDFT to assign low-energy bands, including dark versus bright transitions. Public experimental absorption is input evidence. Common-chelate interventions and an independently retained spectral trend are benchmark additions. The paper crystallographic white-light/polymorph results are outside this molecular first version.

# Public inputs and scientific boundaries

Use neutral singlet 1a C11H8BF2NO and 1b/1c/1d C15H10BF2NO; retain their distinct azaarene fusion/connectivity. Primary toluene medium matches experimental_absorption.json and main Fig2/Table1. A gas-phase source baseline is a separate sensitivity, not a toluene measurement. A shared geometry means a mapped local B-N-O/chelate scaffold, not a forced whole-graph atom bijection across different fused isomers. Geometry constraints must be stated and released controls retained.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **relaxed_monomers.** Cover `1a`, `1b`, `1c`, `1d`. Retain low-root tables, full oscillator distribution and NTOs; observed absorption maximum need not be S1 when a dark state is lower. Required numeric fields are `excitation_eV`, `oscillator_strength`, `CT_distance_A`.

2. **common_geometry.** Cover `1a_common`, `1b_common`, `1c_common`, `1d_common`. Actual shared-chelate constraints with atom correspondence and released pairs are mandatory; four original spectra alone are insufficient. Required numeric fields are `excitation_eV`, `oscillator_strength`, `constraint_deformation_kJ_mol`.

3. **spectral_test.** Cover `electronic_vs_geometry`, `independent_trend`, `method_sensitivity`. Separate band energy, intensity and character, with stated broadening/assignment and digitization uncertainty. A retrospective holdout must not be mislabeled a blind prediction. Required numeric fields are `predicted_shift_eV`, `observed_shift_eV`, `uncertainty_eV`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Real crystal dimers, polymorph mapping and white-light mechanisms are separate optional modules. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
