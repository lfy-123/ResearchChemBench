# Scientific objective

Test whether M3 has comparable evidence for interaction with PM6 and BTP-eC9 fragments and whether apparent attraction arises from electrostatics, dispersion or distortion.

# Author-provided scientific guidance

The authors propose a planar N...S-locked quadrupolar additive with affinity for donor BDD and acceptor BTP-eC9 regions. Main Fig1 shows pair models; source M3 DFT is B3LYP/6-31G. Pair energy decomposition and matched truncation controls are new. The printed quadrupole unit D is not a canonical quadrupole unit; use a declared origin and e angstrom squared or properly converted atomic units.

# Public inputs and scientific boundaries

M3 is neutral singlet 2,5-di(thiophen-2-yl)pyrazine C12H8N2S2. Use the independently reviewed builder-defined finite graphs PM6_BDD_T2_Me (C20H12O2S4), BTP_eC9_core_Me (C22H14N4S5), and BTP_eC9_full_pi_Me (C48H18F4N8O2S5), all neutral singlets. Their atom-indexed bonds and exact cut/cap boundaries are supplied in objects.json and fragment_models/. BTP core atoms 1–31 map identically into the larger model; added/removed caps and hydrogens must be explicitly mapped in paired comparisons. These are bounded source-grounded models, not recovered author coordinates or complete PM6/BTP-eC9 materials. No arbitrary fragment replacement is authorized.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

**Reviewed model definition.** The finite fragment graph definitions and cap rules are now materialized after independent source review. Actual contact, decomposition, truncation and tensor validation remains mandatory; topology review alone is not scientific completion.

# Required scientific validation/investigation

1. **contact_models.** Cover `PM6_face`, `PM6_edge`, `BTP_core_face`, `BTP_core_edge`. Each pair requires complete graph, contact map and several starting orientations at fixed composition; compare released versus frozen fragments. Required numeric fields are `interaction_kJ_mol`, `distortion_kJ_mol`.

2. **decomposition.** Cover `PM6_pair`, `BTP_pair`. Use a single justified decomposition and identical fragmentation; terms are model-dependent, not unique causal observables. Recompute total and residual terms. Required numeric fields are `electrostatic_kJ_mol`, `dispersion_kJ_mol`, `exchange_kJ_mol`, `induction_kJ_mol`.

3. **truncation_and_tensor.** Cover `larger_fragment`, `M3_tensor`. At least one actual larger-fragment pair is core. Report all six independent tensor components with origin/axes; Qzz alone cannot prove dual binding or PCE. Required numeric fields are `primary_interaction_kJ_mol`, `control_interaction_kJ_mol`, `quadrupole_zz_eA2`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Bulk blend morphology and device simulations are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.

Metric applicability clarification: For the isolated M3_tensor row, primary_interaction_kJ_mol and control_interaction_kJ_mol are null with metric_applicability_reason because no partner is present. The full quadrupole tensor, declared origin/axes and numeric quadrupole_zz_eA2 remain mandatory. The larger_fragment row still requires both real interaction energies, a mapped larger-fragment pair and the shared M3 tensor; null cannot waive that truncation comparison. The reviewed finite fragment identities remain mandatory; the truncation-pair calculation cannot be waived.
