# Scientific objective

Test whether preferential association and a metal-related dark/charge-transfer state are distinguishable explanations for HL response to Fe(III), using a source competing ion and balanced solution species.

# Public inputs and scientific boundaries

HL is the full C20H22N4O6 neutral singlet graph with two E imines and phenolic OH groups. Source sensing medium is DMF; Co(II) is selected because it is an explicitly measured partial-quenching competitor. Fe(III) spin space includes doublet/quartet/sextet; Co(II) doublet/quartet. Water/DMF ligands, protonation and counterions must be fixed with salt/pH data before a unique binding-energy cycle is defined. Do not compare unlike total compositions or assign selectivity from smallest gap.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

**Development input block.** blocked_solution_definition: DMF and competing Co(II) are confirmed, but the accessed main/SI do not fix sensing salt counterions, pH/proton reservoir or water content. Define those from source records or an explicitly authorized model before atom-complete Fe/Co exchange references. No invented salt/pH or calibrated selectivity is supplied. This development package accepts diagnostic/partial submissions only until a new reviewed version resolves the input block.

# Required scientific validation/investigation

1. **coordination_candidates.** Cover `HL`, `Fe_HL_protonated`, `Fe_HL_deprotonated`, `Co_HL_protonated`, `Co_HL_deprotonated`. All models require atom-complete solvent/counterion/proton bookkeeping and applicable spin search; apparent nonconvergence is not proof a species is absent. Required numeric fields are `G_Eh`, `spin_squared`, `excitation_eV`, `oscillator_strength`.

2. **solution_cycles.** Cover `Fe_exchange`, `Co_exchange`, `proton_exchange`. Use one balanced exchange reference and explicit proton reservoir; bare Fe3+ binding in vacuum cannot be substituted for an unreported DMF experimental salt. Required numeric fields are `delta_G_kJ_mol`, `standard_state_correction_kJ_mol`.

3. **selectivity_tests.** Cover `binding_contrast`, `state_contrast`, `speciation_sensitivity`. Keep binding preference separate from potential quenching channels, accept multiple Fe species consistent with evidence. TD/NTO alone does not produce a rate or detection limit. Required numeric fields are `binding_difference_kJ_mol`, `excitation_difference_eV`, `CT_fraction_change`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Full quenching dynamics, detection limits and biological medium are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
