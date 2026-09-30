# Scientific objective

Test whether O/F chelation and anion competition support a molecular explanation of the solvent series beyond isolated-solvent descriptors.

# Public inputs and scientific boundaries

Use PM COCCC, BM COCCCC, TFPM COCCC(F)(F)F and TFBM COCCCC(F)(F)F; all solvent molecules neutral singlets. Li+ is singlet; FSI- is F-S(=O)2-N(-)-S(=O)2-F, singlet. Core clusters contain exactly one Li+, one FSI- and one solvent (total charge0 singlet). Compare O-facing, O/F-contact where F exists, and FSI-dominated orientations at identical composition. No 2 M bulk interpretation follows from this finite-cluster design.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **cluster_orientations.** Cover `PM_solvent_contact`, `PM_anion_contact`, `BM_solvent_contact`, `BM_anion_contact`, `TFPM_solvent_contact`, `TFPM_anion_contact`, `TFBM_solvent_contact`, `TFBM_anion_contact`. For nonfluorinated solvents any F contact is to FSI and must be labeled. Fluorinated candidates include attempted bidentate and O-only starts; retain real collapse evidence. Required numeric fields are `electronic_Eh`, `Li_O_A`, `Li_F_nearest_A`, `lowest_frequency_cm1`.

2. **fragment_controls.** Cover `PM`, `BM`, `TFPM`, `TFBM`. Compute common-fragment interaction/distortion and state explicitly surface/isodensity/gauge for ESP. A gas-phase ion-solvent Eb and neutral salt-cluster interaction are separate quantities. Required numeric fields are `binding_kJ_mol`, `interaction_kJ_mol`, `distortion_kJ_mol`, `dipole_D`, `ESP_O_eV`, `RESP_O_e`.

3. **descriptor_test.** Cover `O_F_contrast`, `anion_competition`, `method_sensitivity`. Test a descriptor prediction against actual coordination and anion intervention, not a restatement of source ordering. Do not infer conductivity/SEI or bulk RDF. Required numeric fields are `paired_energy_change_kJ_mol`, `uncertainty_kJ_mol`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** 2 M molecular dynamics, RDF/CN, conductivity and battery performance are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
