# Scientific objective

Test the molecular contribution of constrained motion to BN-anthracene excitation and charge transfer, separating a local geometry effect from an unsupported aggregate explanation.

# Public inputs and scientific boundaries

First version uses source PBNA C24H22B2N2, neutral singlet, with the two mapped B-phenyl torsions. Compute S0 and a tracked S1 on released and identically restrained motion coordinates, primary gas phase with common CH2Cl2 sensitivity. A restrained excited-state point is an intervention, not an unconstrained S1 minimum. Retain all B/N connectivity.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **state_geometry.** Cover `S0_free`, `S1_free`, `S0_restrained`, `S1_restrained`. Keep geometric and electronic-state records distinct; S1 and S0 energies must refer to the stated same protocol and geometry. Required numeric fields are `electronic_Eh`, `torsion_degree`, `excitation_eV`, `oscillator_strength`.

2. **motion_response.** Cover `vertical_fixed_motion`, `relaxed_motion`. Inspect NTO/transition densities and local geometry; compute paired effects rather than infer them from frontier orbital pictures. Required numeric fields are `excitation_change_eV`, `CT_distance_change_A`, `relaxation_kJ_mol`.

3. **local_robustness.** Cover `second_torsion_or_method`, `common_solvent`. Actual motion/method or medium sensitivity bounds the isolated-molecule claim; no quantum yield, knr or bulk AIE is scored. Required numeric fields are `primary_effect_eV`, `control_effect_eV`, `uncertainty_eV`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Dimers, crystal AIE, nonradiative rates and quantum yields are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
