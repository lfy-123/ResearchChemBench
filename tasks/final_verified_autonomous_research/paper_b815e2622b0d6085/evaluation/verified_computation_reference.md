# 当前复核补充（2026-09-23）

已核对 2026-09-21 acceptance 结果与本文件的 2026-09-20 两网格闭环，并于 2026-09-23 重读六份 OUTCAR 核实正常结束、EDIFF 收敛和对应 PROCAR 存在。Cl/Br/I 的 2×2×1、3×3×1 HSE06/no-SOC 自洽投影链、Pb-p 框架态识别、fundamental/framework 以及 edge/same-k 四类 gap 均一致；3×3−2×2 最大变化为 0.019514 eV，框架 edge gap 均落在原 evaluator 容差内。当前任务的科学可计算性获得支持，按用户授权移入 final。此前本段“公开 2H 输入/修正 H 相”的描述是误混入 VSe2 论文的问题，本篇为三种 Pb 晶体，不存在该问题；现予纠正。当前验收见 runs/hold_verification/group_6/paper_b815e2622b0d6085/20260921_acceptance/report/results.json。本次未重算、未修改任务输入或评分目标。

# Verified computation reference — paper_b815e2622b0d6085 (autonomous_research)

> Evaluator-private provenance, never agent input or an alternative scoring rule. This record incorporates three real supplementary SCFs completed on 2026-09-16 and raw-output re-extraction on 2026-09-20. The maintenance itself launches no quantum calculation. This is author-route verification, not a blind autonomous-agent replay.

## Approved boundary repair — second-grid verification completed (2026-09-20)

The original second-grid physical-state identity gap is closed. Both meshes now have independent, converged HSE06 projections for Cl, Br and I, with the same parent geometry and PAW identity. Current scoped evaluator requirements are supported. The task was moved from HOLD to final after the authorized 2026-09-23 review; neither the scientific target nor its tolerances have changed.

The authoritative current record is [verification_supplement.json](verification_supplement.json). It includes schema-valid `author_route_results` reconstructed from real output, per-object raw hashes, all four observables, independent assignment checks and evaluator alignment. It must not be exposed as an agent answer. [boundary_repair_evidence.json](boundary_repair_evidence.json) preserves the pre-supplement `release_reconciliation` unchanged as history and explicitly points to the current supplement.

## Paper basis and declared model

- [Main paper](../../../../papers/paper_b815e2622b0d6085/documents/main.pdf), PDF pp. 2, 4–5: periodic PAW/HSE06, lower organic unoccupied states versus Pb-related states, and a separate approximate SOC correction. [SI](../../../../papers/paper_b815e2622b0d6085/documents/supplementary_001.pdf), S1/S2/S9, supports the bounded structural-correlation discussion; S6–S8 concerns reduced-model SOC.
- The unchanged supplied parents map to Cl/Br/I CCDC 2499860/2499862/2499861, each 64 atoms and neutral. Source CIF metadata is 296 K, labelled 300 K/room temperature in the paper and approved task. Periodic expansion matches actual POSCAR atoms to approximately 2.1e−15 Å, with unchanged cell, composition and occupancy.
- HSE06, AEXX=0.25, HFSCREEN=0.2 Å⁻¹, ISPIN=2, LSORBIT=F, EDIFF=1e−7 eV, NSW=0, default ENCUT=400 eV, unchanged PAW, LORBIT=11. Actual software is VASP 6.3.2; author VASP 6.3.0 is a disclosed implementation difference. Mesh dimensions, parallel layout and restart controls are numerical execution choices, not fully specified author inputs.

## Successful calculation chain

1. Retain the valid 2×2×1 Γ-centered fixed-parent HSE06 projection runs; do not recompute them.
2. The historical 3×3×1 eigenvalue-only runs have no projections and zero-byte WAVECAR files. They cannot establish framework identity. Use the three later complete 3×3×1 self-consistent projected runs listed below instead. Compatible local-test wavefunctions supplied initial guesses only; production `ICHARG=0` performed full HSE06 SCF, not a frozen-density substitute.
3. Confirm SCF convergence and normal VASP termination in all six actual outputs. Check same-parent/POTCAR hashes, independent PROCAR/XML projection data, complete supplementary WAVECAR headers and hashes. XML versus EIGENVAL agrees within its four-versus-six-decimal printing precision; final gaps use EIGENVAL.
4. Partition inorganic Pb4Br12 and organic atoms by periodic connectivity. The four carbon-bound ring halogens are organic, including the Br substituents. Normalize printed atom projections and compare component/element/angular-momentum groups for every saved unoccupied state. Keep all lower states; do not select by target energy or band ordinal.
5. In both meshes all eight lower unoccupied bands have organic:C:p leading character. The first framework:Pb:p-leading manifold is independently found, with band 133 recorded only as the resulting index. It is the lowest Pb-p-leading candidate at every sampled k/spin. Both meshes retain full lower-state and selected-candidate records.
6. I remains a supported mixed state: at Γ its total inorganic fraction is approximately 0.475862, but Pb-p=0.344828 leads C-p=0.220690 and I-p=0.124138. No extra >50% inorganic threshold is introduced. Common-Γ component vectors agree within printed precision; this supports sampled-domain identity but is not wavefunction overlap or a full-zone continuity proof.
7. Independently extract global-over-sampled-set occupied/unoccupied extrema and minimum same-k/same-spin differences for both fundamental and assigned framework sets. Retain occupation, spin, fractional reciprocal coordinates, degenerate edge sets (1e−5 eV), and signed/absolute changes. Directness compares edge sets modulo reciprocal translations, not Γ membership.

## Values and independent state stability

| Crystal | Mesh | Fundamental edge | Fundamental same-k | Framework edge | Framework same-k |
|---|---|---:|---:|---:|---:|
| Cl | 2×2×1 | 3.094104 | 3.094105 | 4.664272 | 4.664273 |
| Cl | 3×3×1 | 3.080154 | 3.102962 | 4.649296 | 4.674125 |
| Br | 2×2×1 | 3.105698 | 3.105699 | 4.660486 | 4.660486 |
| Br | 3×3×1 | 3.101139 | 3.119048 | 4.651595 | 4.669504 |
| I | 2×2×1 | 3.109971 | 3.109976 | 4.460078 | 4.488663 |
| I | 3×3×1 | 3.122884 | 3.126038 | 4.463777 | 4.469149 |

All energies are eV. Each following cell is signed change (3×3−2×2); nonnegative absolute change.

| Crystal | Fundamental edge | Fundamental same-k | Framework edge | Framework same-k |
|---|---:|---:|---:|---:|
| Cl | −0.013950; 0.013950 | +0.008857; 0.008857 | −0.014976; 0.014976 | +0.009852; 0.009852 |
| Br | −0.004559; 0.004559 | +0.013349; 0.013349 | −0.008891; 0.008891 | +0.009018; 0.009018 |
| I | +0.012913; 0.012913 | +0.016062; 0.016062 | +0.003699; 0.003699 | −0.019514; 0.019514 |

Assigned primary framework edge residuals against unchanged Cl 4.63 / Br 4.64 / I 4.44 eV targets are +0.034272 / +0.020486 / +0.020078 eV. All meet ±0.15 eV after independent physical identity validation. These comparisons do not use fundamental, same-k or SOC values in place of framework edge gaps.

Second-grid Pb-p ranges are Cl 0.680272–0.691781, Br 0.591549–0.680556, I 0.344828–0.431507. Leading-character margins remain positive, including a minimum 0.124138 for I. All lower candidates and component atom indices are retained in the linked complete records.

## Raw evidence anchors

| Crystal | Reused primary projection | Independent supplementary projection | Full re-extracted record |
|---|---|---|---|
| Cl | [2×2 PROCAR](../../../../docs/verification/group_6/paper_b815e2622b0d6085/provenance/qzcli_hpc/Cl_parent_HSE06_lorbit_analysis/1_20260903T215944Z_267/PROCAR) | [3×3 PROCAR](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260915_kmesh_identity/production/Cl/PROCAR), [OUTCAR](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260915_kmesh_identity/production/Cl/OUTCAR) | [Cl JSON](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260920_current_hold_audit/reextraction/Cl.json) |
| Br | [2×2 PROCAR](../../../../docs/verification/group_6/paper_b815e2622b0d6085/provenance/qzcli_hpc/Br_parent_HSE06_lorbit_analysis/1_20260903T215944Z_267/PROCAR) | [3×3 PROCAR](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260915_kmesh_identity/production/Br/PROCAR), [OUTCAR](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260915_kmesh_identity/production/Br/OUTCAR) | [Br JSON](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260920_current_hold_audit/reextraction/Br.json) |
| I | [2×2 PROCAR](../../../../docs/verification/group_6/paper_b815e2622b0d6085/provenance/qzcli_hpc/I_parent_HSE06_lorbit_analysis/1_20260903T215950Z_344/PROCAR) | [3×3 PROCAR](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260915_kmesh_identity/production/I/PROCAR), [OUTCAR](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260915_kmesh_identity/production/I/OUTCAR) | [I JSON](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260920_current_hold_audit/reextraction/I.json) |

Each run directory also retains INCAR/POSCAR/POTCAR/KPOINTS/EIGENVAL/vasprun.xml. Supplementary runs retain complete WAVECAR and application records; Cl/Br/I elapsed OUTCAR times are 4245.471/4828.429/5309.973 s. Exact timestamps, file hashes and per-rule checks are in the current supplement and [independent audit](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260920_current_hold_audit/report/results.json). See the [detailed review](../../../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260920_current_hold_audit/report/supplementary_verification.md) for the full evaluator comparison.

## Scientific interpretation and limits

Both meshes support I having the smallest framework gap; fundamental gaps instead place I slightly highest. The a-axis norms are Cl 9.2210, Br 9.3638 and I 9.6254 Å. This correlation is not an isolated causal strain experiment: independently observed I organic-framework admixture is a plausible alternative contribution. Cl/Br fine ordering reverses between meshes, so a robust strict three-way ordering is not claimed.

Sampled directness changes with the mesh. Non-Γ same-k extrema can be direct; an indirect sampled label is not a proof of exact full-Brillouin-zone extrema. Projection normalization uses rounded PAW-sphere weights, not exact whole-space probabilities. Optical allowedness remains `not_established`; no matrix elements, direct-parent SOC or reduced-model SOC result is claimed from these calculations. None is an extra mandatory computation under the current evaluator.

Historical status: the 2026-09-15 missing-projection finding remains correct for its specific old 3×3 directories. Later valid supplementary outputs close that gap. Old same-ordinal diagnostics and original group PASS labels are retained as history, not reused as current physical-identity proof. No scientific objective, public input, grading target or tolerance was relaxed; additional required quantum calculations: zero.
