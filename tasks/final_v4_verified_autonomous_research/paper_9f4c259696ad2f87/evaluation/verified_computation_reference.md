# 2026-10-28 V3 最终命题与证据复用

13条改为8条最终命题100分：三种组成的光学变化、两缔合G符号及相对强弱、电子解释和物种可辨识性。五种S1配置取消独立评分，仅支撑物理解释；原本没有硬数值窗，未新增或拟合。

三条光学比较：有效更新PXX1及其mono S1=2.2664/1.8373 eV；PXX2/free/mono/bis=2.2253/1.8762/1.9543 eV，均为一致nonequilibrium PCM。两缔合步骤G在298.15 K、1 atm为−12.135405719/−9.971125543 kcal/mol；1 M为−14.029734165/−11.865453988，不混合参照。电子解释使用五体系约97–99% H→L主配置及可接受基态密度/几何，取消五个独立轨道完成分。mono/bis差0.0781 eV；FWHM0.05/0.10/0.20 eV时诊断重叠0.098895/0.320676/0.539589，不能声称实测分辨率已校准。

限制：原验收为ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION。S1较SI高0.0533–0.0853 eV（更新PXX1 +0.0624）；振子强度也有偏差。源PCM响应及精确系综未明，不能挑更近的equilibrium结果充当原基线；mono激发态密度CPHF失败仍保留；展宽未实验校准，非唯一占据结论须有界。

本轮未运行新计算；下列历史正文逐字保留，旧 PASS/V2 评分不构成本版全面通过。

---

# 当前计算验证与科学分V2参考 — 2026-10-20

验收类型：**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**。当前冻结任务范围的必要定性节点、重要披露方法与有效计算已获协调确认；formal_scoring_permitted=true。当前评分为paper_science_v2，二元叶子总分100，无过程分。此验收不声称原数值容差已通过，不承诺全部源表或整篇实验精确复现。出版/专家复核与运行评分资格分开。

## 当前科学范围与对象

PXX1,PXX1 mono-adduct,PXX2,PXX2 mono-adduct,PXX2 bis-adduct optical and sequential association evidence inDCM; bounded spectral distinguishability.

- source: Target SIpp167–170: CREST3.0.2 GFNFF/NCI7kcal; B3LYP-D3BJ/6-31G(d) PCMDCM opt/freq; TD20 B3LYP-D3BJ/6-311G(d), Gaussian16C.01. Target-specific SI overrides general-method prose.
- native: Five complete neutral-singlet full identities; mono/bis acid partners explicit; valid local minima; default5D/7F TD20 nonequilibrium PCM baseline. Updated PXX1 valid-minimum result replaces earlier unvalidated fixed geometry.
- version: Disclosed Gaussian16C.01 matches.
- response: IEInf1 nonequilibrium is baseline; IEInf0 equilibrium control is explicitly a different diagnostic. Source response default is not reported.

## 实际计算验证过程与关键节点

1. Construct full neutral-singlet PXX1/PXX2 and explicit mono/bis B(C6F5)3 complexes; PXX1 has one carbonyl and PXX2 has two.
2. Source targetSIp170: CREST3.0.2 GFNFF/NCI7kcal screening, B3LYP-D3BJ/6-31G(d) PCMDCM optimization/frequency and bounded DFT preselection. Native local minima, not exact global source conformer, validated.
3. PXX1 corrected source-method local minimum has216positive modes; bis152atoms/858electrons has450positive physical modes/stableSCF. The updated PXX1 replaces historical unvalidated fixed geometry.
4. Run TD20 B3LYP-D3BJ/6-311G(d),PCMDCM,Gaussian16C.01 default5D/7F nonequilibrium response for five species. Preserve full configurations and source/native comparisons.
5. Use geometry-level298.15K RRHO G for balanced sequential association; retain1atm and transparent1M conventions separately.
6. Analyze mono/bis overlap under explicitly diagnostic linewidths. Equilibrium IEInf0 results are kept separate even though closer to source; optional mono relaxed-density CPHF failure is not represented as a valid density calculation.

所有以下记录复用真实既有计算；本次迁移不启动量子化学/HPC任务，不拟合参考值或容差。版本差异依既有授权，不自动视为误差来源或数值准确度证据。

## 论文值、实际值与偏差

差值定义为native−source；绝对偏差另列。表中为实数减法汇总，无新科学模拟。相对误差对近零能隙、位移或不同实验/理论口径可能误导，未机械计算。无数值评分叶子，表值不形成隐藏容差门。

| 量 | 论文值 | 实算值 | 有符号差 | 绝对差 | 单位 / 定义 |
|---|---:|---:|---:|---:|---|
| PXX1 S1 E noneq | 2.204 | 2.2664 | 0.0624 | 0.0624 | eV / Accepted baselineIEInf1 |
| PXX1 S1 f noneq | 0.545 | 0.4073 | -0.1377 | 0.1377 | dimensionless / Accepted baselineIEInf1 |
| PXX1acid S1 E noneq | 1.784 | 1.8373 | 0.0533 | 0.0533 | eV / Accepted baselineIEInf1 |
| PXX1acid S1 f noneq | 0.532 | 0.4094 | -0.1226 | 0.1226 | dimensionless / Accepted baselineIEInf1 |
| PXX2 S1 E noneq | 2.14 | 2.2253 | 0.0853 | 0.0853 | eV / Accepted baselineIEInf1 |
| PXX2 S1 f noneq | 1.144 | 0.9166 | -0.2274 | 0.2274 | dimensionless / Accepted baselineIEInf1 |
| PXX2acid S1 E noneq | 1.816 | 1.8762 | 0.0602 | 0.0602 | eV / Accepted baselineIEInf1 |
| PXX2acid S1 f noneq | 0.865 | 0.6657 | -0.1993 | 0.1993 | dimensionless / Accepted baselineIEInf1 |
| PXX2bis S1 E noneq | 1.888 | 1.9543 | 0.0663 | 0.0663 | eV / Accepted baselineIEInf1 |
| PXX2bis S1 f noneq | 1.33 | 1.0607 | -0.2693 | 0.2693 | dimensionless / Accepted baselineIEInf1 |
| PXX2 binding step1 | -12.7 | -12.135405719 | 0.564594281 | 0.564594281 | kcal/mol / Native1atm RRHO; source precise standard-state convention not explicit;1M separately retained |
| PXX2 binding step2 | -10.1 | -9.971125543 | 0.128874457 | 0.128874457 | kcal/mol / Native1atm RRHO; source precise standard-state convention not explicit;1M separately retained |
| PXX2bis−mono S1 gap | 0.072 | 0.0781 | 0.0061 | 0.0061 | eV / No claimed experimental resolving-power cutoff |

## 额外实际结果与未复现项

- S1 energies PXX1,PXX1acid,PXX2,PXX2acid,PXX2bis：source=[2.204, 1.784, 2.14, 1.816, 1.888]；native=[2.2664, 1.8373, 2.2253, 1.8762, 1.9543]；Single nonequilibrium baseline; associated oscillator strengths[.4073,.4094,.9166,.6657,1.0607]
- Sequential binding G steps：source=[-12.7, -10.1]；native={"1atm": [-12.135405719, -9.971125543], "1M": [-14.029734165, -11.865453988]}；Standard-state conventions explicitly retained; compare signs/order without mixing conventions
- Mono/bisS1 separation：source=0.072；native=0.0781；PXX2 mono versus bis adduct
- Equilibrium diagnostic, not acceptance baseline：source=[2.204, 1.784, 2.14, 1.816, 1.888]；native=[2.2039, 1.7829, 2.1398, 1.8157, 1.8847]；IEInf0 response; bisS6 existing residual+.1654eV/−.1484 oscillator strength retained in archived comparison
- Nonequilibrium mono/bis overlap sensitivity：source="Source linewidth not disclosed"；native={"FWHM_eV": [0.05, 0.1, 0.2], "overlap": [0.098895, 0.320676, 0.539589]}；Diagnostic kernel dependence, not experimental resolving-power validation

## 定性关键节点与仍有边界

- Molecular identity and minima：SUPPORTED: all5 full neutral singlets, explicit acids, valid local minimum parents. Exact global author conformer is not claimed or made an undisclosed requirement.
- Lewis-acid association optical redshift：SUPPORTED: all corresponding adducts have lowerS1 energy than free ligand on one nonequilibrium protocol.
- Low-energy electronic transition character：SUPPORTED: S1 dominated by H→L approximately97–99% using explicit coefficient conventions for all5 species.
- Sequential association tendency：SUPPORTED: both G steps favorable, second weaker under consistent1atm and1M conventions; no universal equalKa or population statement.
- Mono/bis distinguishability：SUPPORTED bounded similarity: S1 separation .0781eV versus source .072eV; overlap depends on linewidth and does not prove instrument-level resolution.
- Calculation validity and response choice：SUPPORTED: five complete native TD20 outputs re-read; updated PXX1 valid geometry used; no swap to equilibrium solely for numeric closeness.
- General SIpp5–6 uses GaussianA.03/UFF/B3LYP/6-31G(d)/64states; targetSIp170 gives the section-specific CREST/D3BJ/TD20/6-311G(d) route and target revisionC.01. Private reproduction evidence preserves this distinction without altering public guidance.
- Source PCM response flag is unspecified. Native nonequilibrium is the accepted baseline; equilibrium numeric proximity cannot authenticate author response.
- Source describes nearly similar Ka but unequal sourceG already cautions against exact equality; scoring requires favorable signs, second weaker and bounded occupancy.
- Mono/bis spectral overlap is linewidth-dependent; native diagnostics do not prove instrument resolution or guaranteed coexistence.
- Optional mono excited-density CPHF failure is preserved; ground-state density/orbital and completed optical evidence remain separately usable.
- No equilibrium response is used to erase nonequilibrium residuals or claim exact source response known.
- A separate mono-adduct excited-density CPHF failure does not invalidate the completed nonequilibrium optical baseline; source density discussion is ground-state based.
- No equal association constants, guaranteed coexistence, measured linewidth or exact solution ensemble is claimed.

## 原生输入/输出与验证分析位置

以下路径为仓库/服务器真实文件，hash为2026-10-20独立重读值。正常终止只作为执行证据；对象、状态、频率/曲率、响应定义仍是科学资格前提。

- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX1_acid1_source_default5D_TD20_same_geometry_20261006_a1/stdout.log`；SHA256 `2865b725be7655ab4343cb029a82e18a7cf32a9b74812268cccdf93cd2587a0d`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX1_new_source_minimum_default5D_TD20_join_20261007_a1/stdout.log`；SHA256 `30e75305ce81a6704a4dbd7905c3e9db7ac27accaea52f023061ba728f68f6e1`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX2_acid1_source_default5D_TD20_same_geometry_20261006_a1/stdout.log`；SHA256 `496324c4392ad2d98d8bfd882e5b119a12fb866423e6e74491ccb6e4eb138770`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX2_acid2_source_default5D_TD20_same_geometry_20261006_a1/stdout.log`；SHA256 `9567233cc0ec144a70c40c9f2661f53810b46e1a036df4b1a9790d229be962c5`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX2_source_default5D_TD20_gatewording_repair_20261006_a2/stdout.log`；SHA256 `68fdddfcbefa003e5a22ad9650c4a3c3bcf335ec8ca81c5ab15adefa51009bff`；native_output；normal_marker=True

验证汇总/实际源页与分析：

- `docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_9f4c259696ad2f87/ROUTE_ALIGNMENT.json`；SHA256 `8ca70a31f2d808d5cdc5887ca10a67e154963d46cfc20371f63e20df41c2374c`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json`；SHA256 `adc3f71fe8531ed400d2dee2bb09d7af40e1fd72c97a96569629e50b2a8d5375`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX1_new_source_minimum_default5D_TD20_join_20261007_a1/RESULT.json`；SHA256 `379c672e551e8e7624d7a3eaa3b82195014d73e5c99a09c3eb8017da87629661`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX1_new_source_minimum_default5D_TD20_join_20261007_a1/NATIVE_TD20.json`；SHA256 `ccf488c1ca279c2cb11e700acd49cb96779bc372148efe2cd225525447bade06`
- source_adduct：{"path": "papers/paper_9f4c259696ad2f87/documents/main.pdf", "sha256": "592534cc448b295773af43b0783196ac34170f0e847fb7412d873e8a6e98c2ba", "pdf_pages_1based": [9, 10, 11], "locator": "Figs6–7, Lewis acid response and bounded species assignment"}
- source_association：{"path": "papers/paper_9f4c259696ad2f87/documents/supplementary_001.pdf", "sha256": "f3436ca99f362b00e082f3bc28926ef30d56c7f4cfffaf92faa92708a24569ad", "pdf_pages_1based": [167], "locator": "Sequential association free energies and unresolved occupancy"}
- source_td：{"path": "papers/paper_9f4c259696ad2f87/documents/supplementary_001.pdf", "sha256": "f3436ca99f362b00e082f3bc28926ef30d56c7f4cfffaf92faa92708a24569ad", "pdf_pages_1based": [168, 169], "locator": "FigS205,TableS1 energies/f,TableS2 configurations"}
- source_method：{"path": "papers/paper_9f4c259696ad2f87/documents/supplementary_001.pdf", "sha256": "f3436ca99f362b00e082f3bc28926ef30d56c7f4cfffaf92faa92708a24569ad", "pdf_pages_1based": [170], "locator": "Target-specific CREST/GFNFF and B3LYP-D3BJ opt/TD methods"}

## 时间与资源记录

本次迁移新增科学计算数0、HPC作业数0。历史输出中记录的逐作业资源可按原生/执行记录核查；没有统一完整的四篇总walltime、CPU-hour或费用记录，本报告不从核数或日志数量推算。失败、历史固定几何及控制计算不混入成功基线。

## 当前评分边界

中间科学结果70分；最终综合推断30分；全部定性叶子，满分或0。无精度充分校准的通用吸收/位移/结合能窗口，本轮不以最大残差拟合容差。身份、状态和证据是各项前提，不单独奖励。AR/PR具有相同物理判分清单；PR复现合同及合理替代义务仍由原题面约束，AR不被要求采用验证软件或固定搜索轨迹。

## 逐项科学规则—实际证据对应

下表明确本次验证对各项的支持，不使未来Agent自动获分。未来提交仍须独立有效证据。

| Rule / role / score | 实算支持 | 定位 |
|---|---|---|
| r_redshift_pxx1_mono / intermediate / 10 | Noneq pxx1_monoS1=1.8373<pxx1S1=2.2664eV, same response definition. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json; updatedPXX1 RESULT.json |
| r_redshift_pxx2_mono / intermediate / 10 | Noneq pxx2_monoS1=1.8762<pxx2S1=2.2253eV, same response definition. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json; updatedPXX1 RESULT.json |
| r_redshift_pxx2_bis / intermediate / 10 | Noneq pxx2_bisS1=1.9543<pxx2S1=2.2253eV, same response definition. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json; updatedPXX1 RESULT.json |
| r_s1_character_pxx1 / intermediate / 4 | S1 H→L dominated approximately97–99%, explicit native configuration convention; all20roots retained. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/source_TableS2_all100_state_bindings; updatedPXX1 RESULT.json |
| r_s1_character_pxx1_mono / intermediate / 4 | S1 H→L dominated approximately97–99%, explicit native configuration convention; all20roots retained. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/source_TableS2_all100_state_bindings; updatedPXX1 RESULT.json |
| r_s1_character_pxx2 / intermediate / 4 | S1 H→L dominated approximately97–99%, explicit native configuration convention; all20roots retained. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/source_TableS2_all100_state_bindings; updatedPXX1 RESULT.json |
| r_s1_character_pxx2_mono / intermediate / 4 | S1 H→L dominated approximately97–99%, explicit native configuration convention; all20roots retained. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/source_TableS2_all100_state_bindings; updatedPXX1 RESULT.json |
| r_s1_character_pxx2_bis / intermediate / 4 | S1 H→L dominated approximately97–99%, explicit native configuration convention; all20roots retained. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/source_TableS2_all100_state_bindings; updatedPXX1 RESULT.json |
| r_association_step1 / intermediate / 6 | PXX2mono−PXX2−acid: nativeG−12.1354057192kcal/mol1atm;−14.0297341647at1M. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/binding_G_reused |
| r_association_step2 / intermediate / 6 | PXX2bis−PXX2mono−acid: nativeG−9.9711255427kcal/mol1atm;−11.8654539882at1M. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/binding_G_reused |
| r_second_association_weaker / intermediate / 8 | −9.9711>−12.1354kcal/mol under1atm; same ordering at1M. | PXX_five_default5D_TD20_source_state_G_join_20261006_a1/RESULT.json/binding_G_reused |
| r_carbonyl_optical_account / conclusion / 15 | Full carbonyl-associated local minima, valid optical H→L evidence and all adduct redshifts support coordination/electronic interpretation; optional relaxed-density failure not used as successful result. | ROUTE_ALIGNMENT.json; SCIENTIFIC_REVIEW.json; five-species RESULT.json |
| r_occupancy_identifiability / conclusion / 15 | Mono/bis noneqS1gap .0781eV versus source .072; overlap .098895/.320676/.539589 for diagnosticFWHM.05/.10/.20; favorable sequentialG does not establish unique occupancy/equalKa. | five-species RESULT.json; COMPACT_SCIENTIFIC_RESULT.json; INDEPENDENT_OPTICAL_REVIEW.json |

补充原生输入/状态与分析路径：

- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX1_acid1_source_default5D_TD20_same_geometry_20261006_a1/run_status.json`；SHA256 `6c0a151f342ab4d7fd89836b786728f6af8374ca6291a4f42f4942f44a3112fc`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/inputs/PXX1_acid1_source_default5D_TD20_same_geometry_20261006_a1/input.com`；SHA256 `b282f21fc5aa8ba4cdd2738438aa092d74f1845ef5fcce96c9933f36375d293b`；['#p B3LYP/6-311G(d) 5D 7F EmpiricalDispersion=GD3BJ SCRF=(PCM,Solvent=Dichloromethane) Geom=AllCheck Guess=Read TD=(NStates=20) IOp(9/40=4) SCF=(VeryTight,XQC,MaxCycle=512) Integral=UltraFine NoSymm']
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX1_new_source_minimum_default5D_TD20_join_20261007_a1/run_status.json`；SHA256 `97db288364d6fd0db6b323bce30eeea9c869514895ea7ec90924e804e50f9d73`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/inputs/PXX1_new_source_minimum_default5D_TD20_join_20261007_a1/input.com`；SHA256 `5309068c62c43d8d88f8db0571211c9b86c019c01f64a2657c5c5e19afcfcabf`；['#p B3LYP/6-311G(d) 5D 7F EmpiricalDispersion=GD3BJ SCRF=(PCM,Solvent=Dichloromethane) Geom=AllCheck Guess=Read TD=(NStates=20) IOp(9/40=4) SCF=(VeryTight,XQC,MaxCycle=512) Integral=UltraFine NoSymm']
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX2_acid1_source_default5D_TD20_same_geometry_20261006_a1/run_status.json`；SHA256 `51538df0a44ddbad39d46da9174bc7f176c6f311d0a3adc2ee367a6a7c59b22f`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/inputs/PXX2_acid1_source_default5D_TD20_same_geometry_20261006_a1/input.com`；SHA256 `899a15d779d88afad9756252813043b7b6f2565db3feb12a70851a1becb1b9a8`；['#p B3LYP/6-311G(d) 5D 7F EmpiricalDispersion=GD3BJ SCRF=(PCM,Solvent=Dichloromethane) Geom=AllCheck Guess=Read TD=(NStates=20) IOp(9/40=4) SCF=(VeryTight,XQC,MaxCycle=512) Integral=UltraFine NoSymm']
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX2_acid2_source_default5D_TD20_same_geometry_20261006_a1/run_status.json`；SHA256 `8fba3446abb40d2fe936c515b43ec42238404e63ca1c9b9e35bb01e4b664764f`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/inputs/PXX2_acid2_source_default5D_TD20_same_geometry_20261006_a1/input.com`；SHA256 `852c2fd2fab5d3bde48c89136595c6af1a90f5dfc4595b3f7a0d9f369210f225`；['#p B3LYP/6-311G(d) 5D 7F EmpiricalDispersion=GD3BJ SCRF=(PCM,Solvent=Dichloromethane) Geom=AllCheck Guess=Read TD=(NStates=20) IOp(9/40=4) SCF=(VeryTight,XQC,MaxCycle=512) Integral=UltraFine NoSymm']
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/outputs/PXX2_source_default5D_TD20_gatewording_repair_20261006_a2/run_status.json`；SHA256 `248e537a3e62e01496bcb072a5328f6fda2a85e004fdd163c22bb01ac02cc7c9`
- `docs/upgrade_tasks_verification/group_3/v2_execution_20260929/papers/paper_9f4c259696ad2f87/inputs/PXX2_source_default5D_TD20_gatewording_repair_20261006_a2/input.com`；SHA256 `228e3adaebaf1a190f446957efe179ac52b2520e80d6d2a683531834ff0d9467`；['#p B3LYP/6-311G(d) 5D 7F EmpiricalDispersion=GD3BJ SCRF=(PCM,Solvent=Dichloromethane) Geom=AllCheck Guess=Read TD=(NStates=20) IOp(9/40=4) SCF=(VeryTight,XQC,MaxCycle=512) Integral=UltraFine NoSymm']
- `docs/strict_author_route_validation_20261001/supervised_continue_20261011T0932Z/workers/G3/G3_4297df1060365c8b/COMPACT_SCIENTIFIC_RESULT.json`；SHA256 `be4dafa35cf7aff2edcab446cdd26e1ca81962be8a8d4db8c6904ea323f6b705`
- `docs/strict_author_route_validation_20261001/supervised_continue_20261011T0932Z/workers/G3/G3_4297df1060365c8b/SCIENTIFIC_REVIEW.json`；SHA256 `1db0d2c847b04dbdd756f768e5e42a4d12bfbd58cd28f9a22dca80ac65ae0ef0`

逐作业已记录时间（非完整全程总资源）：

- {"case": "PXX1_acid1_source_default5D_TD20_same_geometry_20261006_a1", "started_at": "2026-10-06T09:54:39.915422+00:00", "finished_at": "2026-10-06T10:52:36.021626+00:00", "wall_seconds": 3476.1062046904117, "note": "As recorded; null means not available in this status. No allocation/requested budget substituted for actual use."}
- {"case": "PXX1_new_source_minimum_default5D_TD20_join_20261007_a1", "started_at": "2026-10-07T09:08:02.486591+00:00", "finished_at": "2026-10-07T09:24:57.506248+00:00", "wall_seconds": 1015.0197091568261, "note": "As recorded; null means not available in this status. No allocation/requested budget substituted for actual use."}
- {"case": "PXX2_acid1_source_default5D_TD20_same_geometry_20261006_a1", "started_at": "2026-10-06T10:01:00.961765+00:00", "finished_at": "2026-10-06T11:12:18.138752+00:00", "wall_seconds": 4277.177018897608, "note": "As recorded; null means not available in this status. No allocation/requested budget substituted for actual use."}
- {"case": "PXX2_acid2_source_default5D_TD20_same_geometry_20261006_a1", "started_at": "2026-10-06T10:08:22.399513+00:00", "finished_at": "2026-10-06T12:13:19.157867+00:00", "wall_seconds": 7496.758363373578, "note": "As recorded; null means not available in this status. No allocation/requested budget substituted for actual use."}
- {"case": "PXX2_source_default5D_TD20_gatewording_repair_20261006_a2", "started_at": "2026-10-06T12:55:32.623705+00:00", "finished_at": "2026-10-06T13:21:21.988930+00:00", "wall_seconds": 1549.3653204608709, "note": "As recorded; null means not available in this status. No allocation/requested budget substituted for actual use."}

## 历史验证原文（保留；非当前验收/评分状态）

### 历史文件 docs/final_verified_science_v2_additions_20261020/astra_science_02/archive/autonomous_research/paper_9f4c259696ad2f87/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot

# Verified computation reference — paper_9f4c259696ad2f87 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 8 | `BLOCKED` | - 最终状态：**BLOCKED** |
| 118 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 127 | `PASS` | - 论文复现结论：`PASS` |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Benzoyl-Xanthenoxanthenes: Versatile Chromophores for Light-Engaging Applications
- DOI: `10.1002/anie.202523349`
- Task package: `tasks/final_verified_autonomous_research/paper_9f4c259696ad2f87`
- Verification group: `docs/verification/group_1/paper_9f4c259696ad2f87`
- Paper documents: `papers/paper_9f4c259696ad2f87`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "The archived TD-DFT calculation gives S1=2.2955 eV (540.11 nm, f=0.4108) with dominant 155->156 HOMO->LUMO character (97.91% coefficient-weight estimate). This supports the lowest-band HOMO-to-LUMO assignment within the supplied-geometry, PCM(CH2Cl2) scope.",
  "input_validation": {
    "atom_count": 74,
    "charge": 0,
    "formula": "C43H28O3",
    "geometry_validated": true,
    "multiplicity": 1
  },
  "limitations": "The supplied file is used as the optimized ground-state geometry; no conformer search or harmonic Hessian was performed. The transition percentage is derived from the printed Gaussian amplitude (2*c^2), and the result is a vertical single-geometry calculation.",
  "protocol": {
    "basis": "6-31G(d)",
    "excited_state_method": "TD(B3LYP), singlets, NStates=64",
    "geometry_strategy": "Use supplied 74-atom compound_1_optimized.xyz; validate identity and retain as the ground-state geometry (no reoptimization required by task)",
    "method": "B3LYP",
    "solvation": "PCM(CH2Cl2)"
  },
  "provenance": {
    "gaussian_log": "artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log",
    "gaussian_log_sha256": "a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5",
    "input_xyz": "tasks/paper_reproduction/paper_9f4c259696ad2f87/agent_input/data/inputs/compound_1_optimized.xyz",
    "input_xyz_sha256": "96e6df67736be8fb248c6b1a1f37841a74f280258b41a972b89f89962090389f"
  },
  "results": {
    "coefficient_amplitude": 0.69968,
    "dominant_contribution_percent": 97.91,
    "dominant_transition": "155->156 (HOMO->LUMO)",
    "s1_energy_eV": 2.2955,
    "s1_oscillator_strength": 0.4108,
    "s1_wavelength_nm": 540.11,
    "state": 1
  },
  "status": "complete",
  "validation_evidence": [
    "artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log",
    "Normal termination of Gaussian 16",
    "SCF cycles=1; final SCF=-1881.21706688 Eh",
    "Supplied XYZ identity: 74 atoms, C43H28O3, charge 0, singlet"
  ]
}
```

Paper/SI document hashes:

- `papers/paper_9f4c259696ad2f87/documents/main.pdf` — SHA-256 `592534cc448b295773af43b0783196ac34170f0e847fb7412d873e8a6e98c2ba` (declared_match=True)
- `papers/paper_9f4c259696ad2f87/documents/supplementary_001.pdf` — SHA-256 `f3436ca99f362b00e082f3bc28926ef30d56c7f4cfffaf92faa92708a24569ad` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **22**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/status.json` — successful status record; SHA-256 `2c18830efd6c388dc5cce8de6fceb9f444beb6a98451210dc8ffbeaf6247024a`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log` — successful execution artifact; SHA-256 `a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/hpc_summary.json` — successful execution artifact; SHA-256 `8c3426a3adf83839ad86da64175e31f984f4605efb6a59d2018f753543266066`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/input.com` — successful execution artifact; SHA-256 `0eb02ba13cd6c22a8be1a19e082c314a098cc7d0716fff2feeea09e09e4f5e65`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/status.json` — successful status record; SHA-256 `87a5c7c2b7001be11a1fe78492a19982703e54d4ef05495fecf254e29c591562`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/collection.json` — successful execution artifact; SHA-256 `52ddc5b32066b6cf35ff9b2baf7a05bd0a13c3a9e42d2e3936a41ba94b061e50`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/input.com` — successful execution artifact; SHA-256 `81585e627802be2517eeccb0d18bf74a990352b63cd53e7a3d1f84d7afc08191`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stdout.log` — successful execution artifact; SHA-256 `0be90be21b17c5439803e018fd92df07c19e4a66b53870d1991aaf51f6d053f2`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/status.json` — successful status record; SHA-256 `87a5c7c2b7001be11a1fe78492a19982703e54d4ef05495fecf254e29c591562`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/collection.json` — successful execution artifact; SHA-256 `52ddc5b32066b6cf35ff9b2baf7a05bd0a13c3a9e42d2e3936a41ba94b061e50`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/input.com` — successful execution artifact; SHA-256 `81585e627802be2517eeccb0d18bf74a990352b63cd53e7a3d1f84d7afc08191`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/request.json` — successful execution artifact; SHA-256 `ee302405d83cd69450c2e4ee569aba03f4d9534c771a5512891fd4ba8cb283a7`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/status.json` — successful status record; SHA-256 `36aec1f36ab9980fe1fd4a5976e8b2eae17943607c0172ae69e6421aa79bb1f8`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/collection.json` — successful execution artifact; SHA-256 `6e3326ffcef07edd558f4b072f88a2272290040610a1c7a1207f815ded855734`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/input.com` — successful execution artifact; SHA-256 `bfa3dd09bd316d10522b0d24b3d861fad48a425b39a6b851932b5cd724e41549`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/request.json` — successful execution artifact; SHA-256 `e4e3e7f8d975574577979c3e7cb65d114778ad8bbc7a6dfead285c8ce222242d`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/status.json` — successful status record; SHA-256 `2c18830efd6c388dc5cce8de6fceb9f444beb6a98451210dc8ffbeaf6247024a`
- `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/gaussian.log` — successful execution artifact; SHA-256 `a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5`
- `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/input.com` — successful execution artifact; SHA-256 `0eb02ba13cd6c22a8be1a19e082c314a098cc7d0716fff2feeea09e09e4f5e65`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/status.json` — label=group_1 paper_9f4c259696ad2f87 xanthenoxanthene_b3lyp_optfreq unbounded_timeout_retry; submitted_at=2026-09-01T04:50:45.078724+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt=(CalcFC,MaxCycles=160) Freq NoSymm SCF=(XQC,MaxCycle=256); command=g16 < input.com
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/collection.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stderr.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stdout.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/xanthenoxanthene_b3lyp_optfreq.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/xanthenoxanthene_b3lyp_optfreq_unbounded_retry_summary.json`
2. `native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/status.json` — label=paper_9f4c259696ad2f87 compound1_author_b3lyp_pcm_td64 unbounded_gaussian; submitted_at=2026-09-02T22:12:47.046607+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-31G(d) TD=(Singlets,NStates=64) SCRF=(PCM,Solvent=Dichloromethane) NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512) Pop=Full; command=g16 < input.com
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/collection.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/compound1_author_b3lyp_pcm_td64.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/request.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/stderr.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/stdout.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/supervisor_spec.json`
3. `artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/status.json` — label=artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/status.json
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/compound1_author_b3lyp_pcm_td64.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/hpc_summary.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/sha256sums.txt`
4. `provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/status.json` — label=provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/status.json
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/compound1_author_b3lyp_pcm_td64.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/gaussian.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/sha256sums.txt`

## Evaluator alignment

- Key-point IDs: `kp_ar_input, kp_ar_state, kp_ar_energy, kp_ar_character`
- Conclusion IDs: `c_ar_final`
- Scoring-rule IDs: `r_ar_input, r_ar_state, r_ar_energy, r_ar_character, r_ar_conclusion`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_input` → reference `kp_ar_input`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_state` → reference `kp_ar_state`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_energy` → reference `kp_ar_energy`; type=numeric; unit=eV; tolerance=0.1; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_character` → reference `kp_ar_character`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_conclusion` → reference `c_ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_ar_energy` / reference `kp_ar_energy`: target=2.204 eV; tolerance=0.1; numeric result leaves=[2.2955]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.atom_count` = `74`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.formula` = `"C43H28O3"`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.charge` = `0`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.multiplicity` = `1`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.geometry_validated` = `true`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.method` = `"B3LYP"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.basis` = `"6-31G(d)"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.solvation` = `"PCM(CH2Cl2)"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.geometry_strategy` = `"Use supplied 74-atom compound_1_optimized.xyz; validate identity and retain as the ground-state geometry (no reoptimization required by task)"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.excited_state_method` = `"TD(B3LYP), singlets, NStates=64"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[0]` = `"artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[1]` = `"Normal termination of Gaussian 16"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[2]` = `"SCF cycles=1; final SCF=-1881.21706688 Eh"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[3]` = `"Supplied XYZ identity: 74 atoms, C43H28O3, charge 0, singlet"`
- rule `r_ar_energy` / reference `kp_ar_energy` / field `$.results.s1_energy_eV` / result path `$.results.s1_energy_eV` = `2.2955`
- rule `r_ar_character` / reference `kp_ar_character` / field `$.results.dominant_transition` / result path `$.results.dominant_transition` = `"155->156 (HOMO->LUMO)"`
- rule `r_ar_character` / reference `kp_ar_character` / field `$.results.dominant_contribution_percent` / result path `$.results.dominant_contribution_percent` = `97.91`
- rule `r_ar_conclusion` / reference `c_ar_final` / field `$.conclusion` / result path `$.conclusion` = `"The archived TD-DFT calculation gives S1=2.2955 eV (540.11 nm, f=0.4108) with dominant 155->156 HOMO->LUMO character (97.91% coefficient-weight estimate). This supports the lowest-band HOMO-to-LUMO assignment within the supplied-geometry..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized input leakage review
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained XYZ geometry for neutral singlet compound 1.

Public input files and hashes:

- `agent_input/data/inputs/compound_1_start.xyz` — SHA-256 `3bb3f780d1f81587d9364c23c3d066e6ea0b66b570089f6657bf079b11e5f0ca`; size=3217 bytes; xyz_atom_count=74; xyz_comment=Provided starting geometry of compound 1; neutral singlet; CH2Cl2 PCM; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_1/paper_9f4c259696ad2f87/verification_report.md` — verification record; SHA-256 `a72a6db7162258c06e61994f070aa4997990514d4cbe2f2dce7d3f91855d3eab`
- `docs/verification/group_1/paper_9f4c259696ad2f87/report/results.json` — verification record; SHA-256 `d011b88e731e9ce082cab5c0f7ba78f73563b56a981a61844ff660dca275ce78`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log` — referenced successful evidence; SHA-256 `a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.

### 历史文件 docs/final_verified_science_v2_additions_20261020/astra_science_02/archive/autonomous_research/paper_9f4c259696ad2f87/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot

# Development reference status

No expanded scientific reference has been certified. Status: implemented_pending_expanded_reference.

See `reference_validation_plan.md` and private `legacy_final_snapshot/` for historical material. The old PASS does not apply. New quantum calculations: 0.

