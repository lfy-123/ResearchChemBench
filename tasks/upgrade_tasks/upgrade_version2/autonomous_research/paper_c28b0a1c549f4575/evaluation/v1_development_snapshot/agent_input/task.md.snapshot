# Scientific objective

Determine whether competitive PC association survives ion-pair geometry and finite solvation-number controls while maintaining complete charge and composition balance.

# Public inputs and scientific boundaries

DED is 1,4-diethyl-1,4-diazabicyclo[2.2.2]octane dication, not a neutral diamine. Define A=TEA+BF4- and B=DED2+(BF4-)2 (both charge0 singlet). For each use one and two PC molecules in contact and separated configurations. PC is racemic; choose a fixed stereochemical composition and report it. Compare PC transfer A.PC+B -> A+B.PC and the corresponding second-PC exchange; compare contact/separated at equal solvent count. Source 1 M TEABF4 +0.2 M DED salt is experimental context, not a finite-cluster concentration.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **equal_composition_clusters.** Cover `TEA_PC1_contact`, `TEA_PC1_separated`, `TEA_PC2_contact`, `TEA_PC2_separated`, `DED_PC1_contact`, `DED_PC1_separated`, `DED_PC2_contact`, `DED_PC2_separated`. Keep correct anion count and PC count; separated structures may collapse, but only actual mapped optimization evidence establishes that fact. Required numeric fields are `electronic_Eh`, `G_Eh`, `ion_pair_distance_A`.

2. **PC_exchange.** Cover `first_PC`, `second_PC`. Balance both salt compositions and every PC molecule. Record component energies and coefficients so the exchange is recomputable; no direct ranking of charged DED-PC versus TEA-PC totals. Required numeric fields are `electronic_exchange_kJ_mol`, `free_energy_exchange_kJ_mol`, `distortion_kJ_mol`.

3. **ion_pair_control.** Cover `TEA_contact_effect`, `DED_contact_effect`, `conformer_sensitivity`. Separate ion pairing, PC coordination count and conformer uncertainty; conclusions only concern finite molecular necessary conditions. Required numeric fields are `delta_E_kJ_mol`, `delta_G_kJ_mol`, `uncertainty_kJ_mol`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Capacity, cycling lifetime and bulk GROMACS are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
