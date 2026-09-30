# Verified computation reference — paper_534ae3b6e2fb695f (paper_reproduction)

> Evaluator-private provenance, not agent input and not an alternative scoring rule. This archive records existing successful calculations and read-only postprocessing. No new quantum calculation or public-starter replay was performed. `docs/verification` is read-only; historical records are not edited.

## Approved boundary repair — release reconciliation (2026-09-15)

The current task separates global nucleophilicity, local nitrogen descriptors, ring-plane angles and bonded linker torsions. The previously missing plane residuals, atom mapping and probe provenance have now been extracted from existing outputs, not filled with evaluator targets.

## Paper basis and benchmark scope

- [Main paper](../../../../papers/paper_534ae3b6e2fb695f/documents/main.pdf), PDF p. 3: three diamines and nucleophilicity order/values (ODA 4.26, 6FODA 3.68, PFMB 3.56 eV); noncoplanar geometry and distinct local descriptors.
- [Reviewer-response attachment](../../../../papers/paper_534ae3b6e2fb695f/documents/supplementary_001.pdf), PDF p. 16, Fig. R9: reported indices 4.2622/3.6839/3.5562 and rounded HOMOs. This attachment is reviewer-response material, not a uniquely specified author computational protocol. The printed HOMOs and indices do not recover one identical TCE reference.
- The gas B3LYP/TZVP-on-B3LYP-D3BJ/SVP protocol, fixed TCE −9.1212 eV scale and explicit plane/torsion definitions are approved benchmark conventions. They are not relabelled as uniquely disclosed author definitions. Existing numeric targets/tolerances are unchanged. TMC is context-only.

## Successful calculation chain

1. Use the identity-corrected molecular graph. Match every heavy atom in the archived geometry to the public map by element and full covalent adjacency (distance diagnostic: 1.25 × covalent-radii sum). All three graphs match, with no added/missing heavy-atom edges. No identity is inferred from numerical proximity to a target.
2. ORCA gas neutral-singlet B3LYP-D3BJ/def2-SVP Opt/Freq, TightSCF. Each log contains optimization completion and normal termination. Read the corresponding `input.hess`; remove only the six printed translation/rotation zeros. All physical modes are positive.
3. At the same neutral geometry, use the archived B3LYP-D3BJ/def2-TZVP AIM single points for N (0,1), N−1 (+1,2) and N+1 (−1,2). The actual WFN consumed by Multiwfn matches its source calculation; nuclear element order and coordinates match the neutral geometry to less than 0.000002 Å. N+1 is an auxiliary CDFT probe, not required to define global N or f−.
4. Existing Multiwfn CDFT menu 22 → 2 outputs provide HOMO and Hirshfeld charges. Global N = HOMO − (−9.1212 eV); f−(A) = q_A(N−1) − q_A(N); local N(A) = global N × f−(A). Charge/HOMO/index printing is rounded independently, so multiplying four-decimal printed intermediates need not exactly reproduce the five-decimal local output.
5. On the same final neutral geometry, fit each public six-carbon ring by SVD. Report RMS/max normal residuals and acos(|n₁·n₂|). Calculate every listed consecutive bonded torsion separately, using the public signed atan2 convention. PFMB uses 2–3–12–13, not the nonbonded 4–12 selector.
6. Compare global quantities across the three molecules; do not transfer that ordering to local site indices or infer experimental kinetic constants/polymer performance.

## Actual extracted results

| Molecule | HOMO / eV | Global N / eV | Two N-site local indices / e·eV | Ring-plane / ° | Linker torsions / ° | Ring RMS residuals / Å | Physical modes; minimum / cm⁻¹ |
|---|---:|---:|---|---:|---|---|---|
| ODA | -5.0314 | 4.0898 | 1: 0.30109; 11: 0.30159 | 70.470423 | 41.818161; 41.593386 | 0.002385085; 0.002374957 | 75; 12.393977 |
| 6FODA | -5.6680 | 3.4532 | 7: 0.27352; 19: 0.27024 | 85.699977 | 56.899717; -123.841294 | 0.002827836; 0.002796100 | 93; 26.608321 |
| PFMB | -5.7765 | 3.3447 | 7: 0.28815; 18: 0.28822 | 78.420356 | -78.307281 | 0.000888802; 0.000808246 | 90; 38.438758 |

## Raw output anchors

### ODA

- [Final geometry](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/ODA_identity_corrected_retry/1_20260903T002322Z_422/input.xyz) (the archived filename `input.xyz` contains ORCA's final geometry); [Opt/Freq log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/ODA_identity_corrected_retry/1_20260903T002322Z_422/orca_stdout.log); [Full Hessian/frequency list](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/ODA_identity_corrected_retry/1_20260903T002322Z_422/input.hess).
- [N single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/ODA_N_wfn_cdft_tzvp_sp/1_20260903T023708Z_270/orca_stdout.log); [Nminus1 single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/ODA_Nminus1_cdft_tzvp_sp/1_20260903T020048Z_578/orca_stdout.log); [Nplus1 single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/ODA_Nplus1_cdft_tzvp_sp/1_20260903T020048Z_578/orca_stdout.log).
- [Existing Multiwfn output](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/artifacts/multiwfn/cdft_ODA_identity_corrected/cdft_run.out); [CDFT result](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/artifacts/multiwfn/cdft_ODA_identity_corrected/CDFT.txt); [Invocation record](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/cdft_multiwfn_short_20260903T023945Z.json).

### 6FODA

- [Final geometry](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/6FODA_identity_corrected_retry/1_20260903T002322Z_345/input.xyz) (the archived filename `input.xyz` contains ORCA's final geometry); [Opt/Freq log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/6FODA_identity_corrected_retry/1_20260903T002322Z_345/orca_stdout.log); [Full Hessian/frequency list](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/6FODA_identity_corrected_retry/1_20260903T002322Z_345/input.hess).
- [N single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/6FODA_N_wfn_cdft_tzvp_sp/1_20260903T023708Z_501/orca_stdout.log); [Nminus1 single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/6FODA_Nminus1_cdft_tzvp_sp/1_20260903T020048Z_270/orca_stdout.log); [Nplus1 single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/6FODA_Nplus1_cdft_tzvp_sp/1_20260903T020048Z_424/orca_stdout.log).
- [Existing Multiwfn output](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/artifacts/multiwfn/cdft_6FODA_identity_corrected/cdft_run.out); [CDFT result](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/artifacts/multiwfn/cdft_6FODA_identity_corrected/CDFT.txt); [Invocation record](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/cdft_multiwfn_short_20260903T023945Z.json).

### PFMB

- [Final geometry](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/PFMB_identity_corrected_retry/1_20260903T002331Z_422/input.xyz) (the archived filename `input.xyz` contains ORCA's final geometry); [Opt/Freq log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/PFMB_identity_corrected_retry/1_20260903T002331Z_422/orca_stdout.log); [Full Hessian/frequency list](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/PFMB_identity_corrected_retry/1_20260903T002331Z_422/input.hess).
- [N single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/PFMB_N_wfn_cdft_tzvp_sp/1_20260903T022724Z_501/orca_stdout.log); [Nminus1 single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/PFMB_Nminus1_cdft_tzvp_sp/1_20260903T021617Z_578/orca_stdout.log); [Nplus1 single-point log](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/qzcli_hpc/PFMB_Nplus1_cdft_tzvp_sp/1_20260903T020049Z_347/orca_stdout.log).
- [Existing Multiwfn output](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/artifacts/multiwfn/cdft_PFMB_identity_corrected/cdft_run.out); [CDFT result](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/artifacts/multiwfn/cdft_PFMB_identity_corrected/CDFT.txt); [Invocation record](../../../../docs/verification/group_6/paper_534ae3b6e2fb695f/provenance/cdft_multiwfn_short_20260903T023800Z.json).

## Completeness and remaining limits

The current global-index ordering is ODA > 6FODA > PFMB. Deviations from paper targets are −0.1702, −0.2268 and −0.2153 eV, within the unchanged AR ±0.7 / PR ±0.5 eV tolerances. Both N sites, final geometry, full map, each plane residual and each linker torsion now have evidence. Local indices have their own ordering and are not scored against global targets. Ring-plane angles are not compared to the paper's four-atom angle values.

Complete numerical records, map tables, charge probes and all frequencies: [boundary_repair_evidence.json](task_provenance/boundary_repair_evidence.json), `release_reconciliation`. Re-extract read-only with `scripts/replay_three_boundary_observables.py paper_534ae3b6e2fb695f --release-details`.

Historical status: old group fields `descriptor_value/dihedral_deg` are historical summaries, not complete representations of the current contract. This reference reconciles the evidence without changing group reports. The result supports the approved finite gas-phase descriptor task; it does not prove global conformer exhaustiveness or membrane kinetics. The global calibration is a benchmark adaptation, not a newly inferred paper formula.

## Archive independence (2026-09-18)

The scientific route, model definition, extraction algorithm, computed summary and primary raw-output links above are part of this reference itself. The maintenance-only JSON under `task_provenance/` is supplementary and can be removed at release without removing those explanations. Historical commentary is not a scored submission requirement.

## Evidence scope review (2026-09-19)

For current-format use, identify each `release_reconciliation.molecules[]` by `molecule_id` and map it to submission `id`. Preserve `homo_eV`, `global_nucleophilicity_eV`, `ring_plane_angle_deg` and `linker_torsions`; `plane_fits[].rms_residual_A` supplies `plane_fit_residuals_A`. The two `nitrogen_local_nucleophilicity` records become site_values of the explicitly defined Hirshfeld condensed N*f-minus local descriptor, with the retained CDFT output as evidence. Use `xyz_source`, `atom_mapping` and `optimization` for geometry, mapping and validation evidence. Apply the already public fixed TCE -9.1212 eV convention, not a new TCE computation. TMC stays context-only. This is a representation of retained observations, not new conformer or sensitivity evidence.
