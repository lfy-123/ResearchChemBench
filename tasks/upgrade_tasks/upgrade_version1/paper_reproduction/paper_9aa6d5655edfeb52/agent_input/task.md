# Scientific objective

Discriminate arene fusion from cage motion as explanations of state changes in a source carborane pair, with explicit chemical differences between the pair.

# Author-provided scientific guidance

The authors attribute optical changes to C-B arene fusion and report B3LYP/6-31G(d,p), IEF-PCM(THF), Gaussian09 TDDFT. SI separately reports fluoranthene/triphenylene controls, which are not unfused carboranes. The precursor and cage C-C displacement study here is a new bounded control; its Br confound must be retained in the interpretation.

# Public inputs and scientific boundaries

Use fused 2a C18H20B10 and nonfused source precursor1a C18H21B10Br, both neutral singlets. Precursor1a is 1-(8-bromonaphthalen-1-yl)-2-phenyl-o-carborane; it is not a pure geometric un-fusion because Br/H composition differs. Public graph edits remove the B3-aryl fusion edge, restore B3-H and add aryl-Br. Preserve the closo cage adjacency and mapped cage C1-C2 axis; a multicenter cage edge is not an ordinary two-center bond-order assertion. Primary THF continuum.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **fusion_pair.** Cover `fused2a`, `nonfused1a`. Require NTO/state character, valid ground-state modes and both distinct chemical identities; no KS-gap or NICS proxy for quantum yield. Required numeric fields are `excitation_eV`, `oscillator_strength`, `cage_CC_A`, `lowest_frequency_cm1`.

2. **cage_displacement.** Cover `2a_minus`, `2a_plus`, `1a_minus`, `1a_plus`. Use symmetric ±0.05 angstrom coordinate perturbations around each own relaxed C-C reference as design points, with fixed and orthogonally relaxed versions. The displacement size is a chosen intervention, not a reference tolerance. Required numeric fields are `displacement_A`, `relative_E_kJ_mol`, `excitation_eV`, `oscillator_strength`.

3. **causal_limits.** Cover `fusion_vs_motion`, `method_sensitivity`. Keep Br substitution as a chemical confound, report vibrational/displacement response and trigger higher-level diagnostics for near-degenerate state mixing. A compound conclusion need not isolate fusion uniquely. Required numeric fields are `excitation_change_eV`, `response_eV_per_A`, `uncertainty_eV`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** Crystal emission requires real neighbors and independent convergence and is outside this core. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
