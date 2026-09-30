# Scientific objective

Discriminate metal-induced electronic changes from ligand deformation in Cd/Co/Ni DQCS complexes, using free and frozen ligand controls and properly treated open-shell response.

# Author-provided scientific guidance

The authors use Gaussian09 B3LYP/6-311G(d,p) for DQCS and B3LYP/LanL2DZ for complexes in DMSO. SI S2 explicitly makes Co a doublet, although S8 labels its table as singlet transitions; that table heading must not force closed-shell Co TD. Gap, hardness and electrophilicity are algebraically related, not three independent mechanisms. Frozen-ligand controls are new.

# Public inputs and scientific boundaries

Full neutral DQCS is C31H27N3O3 singlet; retain the phenolic hydrogen present in the three source graphs. Metal complexes all have charge+2; Cd/Co/Ni source multiplicities are1/2/1. Primary medium DMSO. A free ligand extracted from a complex has charge0 singlet, not the parent complex charge. Identify ligand versus metal density partitions and fixed-geometry atom correspondence.

Read `data/inputs/objects.json`, `controls.json` and `data_provenance.json` together. Atom and component maps define identity; geometric preparation is independent. A supplied experimental CIF or observation is an authorized input, never a blind prediction target. Only the materialized public files may be used; no paper/SI reference outputs or private evaluator access.

# Required scientific validation/investigation

1. **relaxed_species.** Cover `DQCS`, `Cd_DQCS`, `Co_DQCS`, `Ni_DQCS`. Compute like-defined TD/NTO observables with six roots or a justified larger window. Co transitions retain doublet reference/spin character rather than forced singlet labels. Required numeric fields are `excitation_eV`, `oscillator_strength`, `metal_transition_fraction`, `spin_squared`.

2. **frozen_ligand.** Cover `ligand_from_Cd`, `ligand_from_Co`, `ligand_from_Ni`. Extract identical complete ligand graph/charge from each source complex, retaining all hydrogens; pair frozen and relaxed ligand results. Required numeric fields are `excitation_eV`, `oscillator_strength`, `ligand_distortion_kJ_mol`.

3. **attribution.** Cover `Cd_effect`, `Co_effect`, `Ni_effect`, `method_sensitivity`. Separate geometry and metal contributions with state matching and real density fractions. Do not use gap/hardness/electrophilicity algebra as independent causal evidence. Required numeric fields are `electronic_shift_eV`, `geometry_shift_eV`, `uncertainty_eV`.

Formulate at least two distinguishable explanations before the decisive comparison. Use actual paired calculations capable of refuting the favored explanation, and quantify one method, conformer, state or numerical sensitivity. Equivalent controls are acceptable only if they retain every named scientific contrast and explicit atom/stoichiometry mapping; explain the substitution in the corresponding matrix row. Preserve all failed/restarted attempts. Report real basin collapse with mapped trajectories/structures; do not create fictitious independent minima. Nonstationary constrained points cannot inherit thermal corrections from another geometry.

Scientific completion requires all core contrasts, raw evidence and the resulting inference. Support, refutation and evidence-backed indistinguishability are equally eligible. Missing endpoints, an unverified graph or nonconvergence are incomplete work, not indistinguishability. No published winner or arbitrary numerical tolerance is imposed on uncalibrated extensions.

**Optional scope.** DNA association, quenching rates and antibacterial mechanism are optional. Optional omissions never cause core failure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Include machine-readable per-point/per-state/conformer tables, actual inputs and raw engine outputs, structures, mappings and density/path/frequency evidence under `outputs/`, `structures/`, `analysis/` or `logs/`. Numeric summaries must be independently recoverable from those artifacts. Report uncertainty and resource use with actual engine starts, failures/restarts, summed job hours, calendar time and core hours. A bounded failure is a valid diagnostic submission, not scientific completion.
