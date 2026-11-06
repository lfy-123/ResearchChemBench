# 2026-10-28 V3 final-results scope and evidence reuse

The same dye-2a acid/base optical–NMR explanation and species-identifiability question is retained. Five final propositions replace seven V2 nodes: one optical electronic explanation, two local NMR responses, the neutral-tautomer alternative and the responsive-species inference. Bright-state amplitudes and root correspondence support the optical conclusion rather than receiving separate intermediate credit. AR retains independent model choice; PR retains the disclosed CAM-B3LYP/cLR/GIAO author baseline.

r_aqueous_optical_explanation reuses EXISTING_RESULTS_UNIFIED_COMPARISON.json water_optics: corrected-LR acid/base 3.3011/2.6072 eV; associated LR oscillator strengths 2.5532/2.9118; H137→L138 amplitudes 0.64058/0.57630. r_nmr_acid_vs_neutral/r_nmr_base_vs_neutral reuse all four mapped H45/46/55/56 with common TMS shielding 32.0802666667 ppm: acid/neutral/base means 8.11884167/7.12474167/6.35666667 ppm. r_hydrazone_competitor reuses hydrazone cLR 2.898 eV, NMR mean 6.52629167 ppm and same-charge single-basin RRHO hydrazone-minus-azo +9.97614562/+9.04052899 kcal/mol in water/DMSO. r_joint_proton_response reuses these jointly and full H20/q0, H22/q+2, H18/q−2 identities (274-electron singlets). The historical acceptance is qualitative with numerical deviations, not strict numerical or new V3 validation.

Evidence gaps / limits: Source acid NMR 7.98 ppm already differs from experimental 6.95; native 8.11884167 differs by +1.16884167 ppm. Source scalar aggregation is incompletely disclosed; Gas base source S4 resembles native S5; weak-state ordinal correspondence remains unresolved outside the dominant-band conclusion; No unique solution protonation site, acid/base equilibrium fraction or experimental hydrazone population is established; cross-charge energies cannot supply these

This edit performs no new calculation or scientific revalidation. Only scoring_rules.json defines current scoring. All historical text below is preserved verbatim; its PASS labels and earlier scoring policies are historical, not a new full V3 pass.

---

# 当前计算验证与科学分V2参考 — 2026-10-20

验收类型：**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**。当前冻结任务范围的必要定性节点、重要披露方法与有效计算已获协调确认；formal_scoring_permitted=true。当前评分为paper_science_v2，二元叶子总分100，无过程分。此验收不声称原数值容差已通过，不承诺全部源表或整篇实验精确复现。出版/专家复核与运行评分资格分开。

## 当前科学范围与对象

Neutral, acid and base molecular response; hydrazone as competing same-formula neutral explanation; separate water optical and DMSO NMR media.

- source: CAM-B3LYP/6-31+G(d); full TDDFT with nonequilibrium corrected-LR PCM in water; SI GIAO proton shielding in PCM DMSO referenced toTMS; gas B3LYP comparison separate.
- native: Full TD, explicit IEInf1 nonequilibrium cLR optical correction; water equilibrium-ground-state minima; CAM-B3LYP/6-31+G(d) GIAO/TMS DMSO; literal source gas structures and separately relaxed controls retained.
- version: Gaussian16C.01 versusB.01 allowed by existing version exception.
- identity: Same C30N6O4 skeleton; H20/q0,H22/q+2,H18/q−2;274electrons, singlets.
- formal_source_note: Formal SI is publisher_SI.docx; method paragraph471 and TableS2 were read, not treated as missing.

## 实际计算验证过程与关键节点

1. Preserve C30N6O4 skeleton: neutralH20/q0, acidH22/q+2, baseH18/q−2, all274electrons and singlets. Neutral hydrazone is same-formula/same-charge competitor.
2. Use CAM-B3LYP/6-31+G(d) equilibrium ground-state water optimizations/frequencies and fullTD nonequilibrium cLR optical response. Explicit IEInf1 and correctedLR stages are read.
3. Keep literal source gas geometry, relaxed water models, gas CAM/B3LYP controls and paired geometry diagnostics distinct. Use acidS4/baseS1 by dominant intensity/character, retaining all six roots.
4. Compute GIAO CAM-B3LYP/6-31+G(d) PCM-DMSO proton shieldings with common TMS32.0802666667ppm. Graph-map H45/46/55/56; report all four before means.
5. Compare neutral azo/hydrazone within the same charge and medium, validate174positive modes, and combine same-charge RRHO and spectra. Do not rank different acid/base charges by unbalanced total energies.

所有以下记录复用真实既有计算；本次迁移不启动量子化学/HPC任务，不拟合参考值或容差。版本差异依既有授权，不自动视为误差来源或数值准确度证据。

## 论文值、实际值与偏差

差值定义为native−source；绝对偏差另列。表中为实数减法汇总，无新科学模拟。相对误差对近零能隙、位移或不同实验/理论口径可能误导，未机械计算。无数值评分叶子，表值不形成隐藏容差门。

| 量 | 论文值 | 实算值 | 有符号差 | 绝对差 | 单位 / 定义 |
|---|---:|---:|---:|---:|---|
| acid water bright cLR E | 3.24 | 3.3011 | 0.0611 | 0.0611 | eV / SourceTable4 correctedLR comparison |
| acid water bright oscillator strength | 2.5632 | 2.5532 | -0.0100 | 0.0100 | dimensionless / Associated native LR oscillator strength, not a separately corrected intensity |
| base water bright cLR E | 2.58 | 2.6072 | 0.0272 | 0.0272 | eV / SourceTable4 correctedLR comparison |
| base water bright oscillator strength | 2.9064 | 2.9118 | 0.0054 | 0.0054 | dimensionless / Associated native LR oscillator strength, not a separately corrected intensity |
| neutral DMSO Hmean vs source calculation | 6.95 | 7.124741666666666 | 0.174741666666666 | 0.174741666666666 | ppm / FourH arithmetic mean; source scalar averaging not fully specified |
| neutral DMSO Hmean vs experiment | 6.8 | 7.124741666666666 | 0.324741666666666 | 0.324741666666666 | ppm / Experimental comparison is separate from calculated-source residual |
| acid DMSO Hmean vs source calculation | 7.98 | 8.118841666666667 | 0.138841666666667 | 0.138841666666667 | ppm / FourH arithmetic mean; source scalar averaging not fully specified |
| acid DMSO Hmean vs experiment | 6.95 | 8.118841666666667 | 1.168841666666667 | 1.168841666666667 | ppm / Experimental comparison is separate from calculated-source residual |
| base DMSO Hmean vs source calculation | 6.35 | 6.356666666666667 | 0.006666666666667 | 0.006666666666667 | ppm / FourH arithmetic mean; source scalar averaging not fully specified |
| base DMSO Hmean vs experiment | 6.1 | 6.356666666666667 | 0.256666666666667 | 0.256666666666667 | ppm / Experimental comparison is separate from calculated-source residual |
| acid gas bright E | 2.94 | 2.9356 | -0.0044 | 0.0044 | eV / Gas table; not water |
| acid gas bright f | 2.6656 | 2.6672 | 0.0016 | 0.0016 | dimensionless / Gas table |
| base gas bright E | 1.99 | 1.9889 | -0.0011 | 0.0011 | eV / Gas table; not water |
| base gas bright f | 2.2512 | 2.2511 | -0.0001 | 0.0001 | dimensionless / Gas table |

## 额外实际结果与未复现项

- Dominant water cLR acidS4/baseS1：source=[3.24, 2.58]；native=[3.3011, 2.6072]；Use corrected-LR energies. Uncorrected LR3.2271/2.5779 retained as separate intermediate.
- DMSO calculated aromatic-H shifts neutral/acid/base：source=[6.95, 7.98, 6.35]；native=[7.12474167, 8.11884167, 6.35666667]；Four-H means; source experiment6.80/6.95/6.10ppm; source itself notes acid theory-experiment mismatch about1ppm
- Gas acid/base dominant E,f：source={"acid": [2.94, 2.6656], "base": [1.99, 2.2512]}；native={"acid": [2.9356, 2.6672], "base": [1.9889, 2.2511]}；Separate gas comparison, not substituted for water cLR
- Weak gas-base state ordering：source={"sourceS4_E": 3.05, "sourceS4_f": 0.1374}；native={"nativeS4_E": 2.8994, "nativeS4_f": 0, "source_like_state": "nativeS5"}；Ordinal discrepancy preserved; physical correspondence not assumed from energy closeness
- Hydrazone competing model：source="Not main source switch carrier"；native={"water_cLR_eV": 2.898, "DMSO_Hmean_ppm": 6.52629, "hydrazone_minus_azo_G_water_kcalmol": 9.9761, "hydrazone_minus_azo_G_DMSO_kcalmol": 9.0405}；Same-charge, same-medium comparisons only
- 中性水相cLR亮态S4=3.2136eV；neutral-hydrazone cLR=2.898eV，NMR均值6.5262916667ppm。hydrazone−azo同电荷RRHO G为water+9.9761456177、DMSO+9.0405289920kcal/mol；各174正模，最低频率10.0717/9.7657cm−1。这些不是不同电荷酸/碱人口热力学。

## 定性关键节点与仍有边界

- Identity and proton/charge balance：SUPPORTED: complete balanced models and same-electron singlet states; no cross-charge total-energy population comparison.
- Base relative optical red shift：SUPPORTED: dominant source-assigned acidS4/baseS1 cLR bands retain acid higher energy than base.
- Aromatic proton NMR acid>neutral>base：SUPPORTED: four graph-mapped protons and one consistentTMS reference; mean acid8.11884>neutral7.12474>base6.35667ppm.
- OH protonation/deprotonation response interpretation：SUPPORTED within explicit acid/base models; no unique solution protonation-site or population assignment claimed.
- Hydrazone alternative：SUPPORTED bounded exclusion: valid minima with174positive modes; same-charge RRHO differences+9.9761water/+9.0405DMSO kcal/mol and different optical/NMR response do not support hydrazone as principal switch carrier.
- Calculation validity and root correspondence：SUPPORTED for dominant bands and NMR: correction stages explicit, native files complete. Weak gas-base sourceS4/nativeS5 issue retained without renumbering native roots.
- Formal SI is a DOCX, not a missing PDF. NMR method paragraph uses TableS1 wording but the actual chemical-shift caption is TableS2; paragraph locations are explicit.
- Source water values are compared to nonequilibrium cLR corrected energies; native LR intermediates happen to be closer and are not substituted.
- Gas base sourceS4(3.05eV,f.1374) resembles nativeS5 while nativeS4 is2.8994eV/f0. Weak-state ordinal correspondence is unresolved and excluded from dominant-band scoring.
- Source calculated acid7.98ppm already differs from experiment6.95ppm; native8.11884167ppm retains rather than conceals the disagreement. Source scalar aggregation is incompletely disclosed.
- Acid NMR absolute disagreement is not hidden or repaired through selective proton averaging. Source scalar aggregation and exact reference origins remain incompletely disclosed.
- No acid/base equilibrium fractions, free ion activities, unique acid site or experimentally certified hydrazone fraction are inferred.
- Source weak-state index mismatch does not reverse task-critical strongest-band or NMR direction; no claim of complete line-by-line table equality.

## 原生输入/输出与验证分析位置

以下路径为仓库/服务器真实文件，hash为2026-10-20独立重读值。正常终止只作为执行证据；对象、状态、频率/曲率、响应定义仍是科学资格前提。

- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_acid_literalSI_dmso_GIAO_20261006_a01/input.com`；SHA256 `074729230389aaee951fd2da3b0405ebbaa8a1252126fa9b4babe5d1477422b5`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_acid_literalSI_dmso_GIAO_20261006_a01/stdout.log`；SHA256 `0cd29a2d552a48fcb94e021186f56d484c53485a0198be9ab8f2fcc97e212c90`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_acid_literalSI_gas_B3LYP_TD6_20261005_a01/input.com`；SHA256 `b8e662e845ba3da0c8750a363fe971fdb51d5bd312497ec41afa6fb9a4cb616e`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_acid_literalSI_gas_B3LYP_TD6_20261005_a01/stdout.log`；SHA256 `7504116d0e06e430cad25610c106de6eb1849a9d216a52792a10e035ab2298d4`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_acid_literalSI_gas_CAM_TD6_20261005_a01/input.com`；SHA256 `8ac56b242cf2ee40a7fcadb1139672de491c5bf84f7ca5ad8c40dfb46237bb8f`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_acid_literalSI_gas_CAM_TD6_20261005_a01/stdout.log`；SHA256 `99fc8b3e8093388ee4825e0c6bceda694df0f1786847915b2bd93d37b33bcfbf`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_base_literalSI_dmso_GIAO_20261006_a01/input.com`；SHA256 `e878bc14aba04a5e45a1ec4bdc0bf30ca429d063698597dc5aeb345f3e5ef95a`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_base_literalSI_dmso_GIAO_20261006_a01/stdout.log`；SHA256 `65ac4181e30fd985f62d641175ea71acb12acc928cea534e920d760ed712017d`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_base_literalSI_gas_B3LYP_TD6_20261005_a01/input.com`；SHA256 `8568663b93ca06547e6dcfa9027751a6c36b310b221b983f18bc6ddfd7a7962f`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_base_literalSI_gas_B3LYP_TD6_20261005_a01/stdout.log`；SHA256 `32273db5117829811a5f99bd4a3d0aaf6151d35f680826de6a191eba1ae9a71a`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_base_literalSI_gas_CAM_TD6_20261005_a01/input.com`；SHA256 `94e9a894e4d7135d2d6911ee3b4cf9ccf9124e641b4d133e35f0091d9d9fbf4f`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_base_literalSI_gas_CAM_TD6_20261005_a01/stdout.log`；SHA256 `42c4fc47dfea3c88268d9c8c9d5a15cf3293717dabd3987b1055873fcbebeb2d`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_neutral_literalSI_dmso_GIAO_20261006_a01/input.com`；SHA256 `5e153245fefa1a08cb13b392b673d83a837031e76b9d50002fb3b1c07bcd3adc`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_neutral_literalSI_dmso_GIAO_20261006_a01/stdout.log`；SHA256 `b1d3ca6c4936dd341806202021ba4da85ebf7e553376fd8dd945faeeedab658f`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_acid_water_clr_root4_v2_a01/input.com`；SHA256 `917da26c203f88da7bb94ef43ac3f7180fedbb8fef5519d0742a91d825ce8b62`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_acid_water_clr_root4_v2_a01/stdout.log`；SHA256 `c48f282da16202eb30977e612deced1459aef77315843b27ec203670299856ff`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_acid_water_optfreq_v2_a01/input.com`；SHA256 `4f7ad89c49378c09f19a17468a2fe99c989f04bcccb3a573a12bffa7aaffc4a9`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_acid_water_optfreq_v2_a01/stdout.log`；SHA256 `6707be792d0cbcdc7b11924c3d7be8dc68b76ee359fdc3e177e40e8e9f5b667b`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_base_water_clr_td6_v2_a01/input.com`；SHA256 `da37aa5b1bd515d7abd6055daf69b73ad871c255523c04258127a8d98f97a5cc`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_base_water_clr_td6_v2_a01/stdout.log`；SHA256 `7ab1ef0f47f65d7adfe8307b93e205e21ceaacff939240a177fab23cc74e64b4`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_base_water_optfreq_v2_a01/input.com`；SHA256 `3b49c7eb278e7e6a756fe9ac934777828962b26afad215beadff24ee23603fa8`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_source_base_water_optfreq_v2_a01/stdout.log`；SHA256 `72079fd1f96345567638165b6c539fc2aa3def7a1e805c42fe64c54830a8290b`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_tms_dmso_giao_v2_a01/input.com`；SHA256 `09d33ea5858fc05c16f1225a1b28bfbe4b00b71f180045450bcebf58f1d29bdd`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_tms_dmso_giao_v2_a01/stdout.log`；SHA256 `7e00e9c0ad2401dfcec6d16fae0fe9426fb2450a0676db3226e2267021d831c5`；native_output；normal_marker=True

验证汇总/实际源页与分析：

- `docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_988bc12ae3768679/ROUTE_ALIGNMENT.json`；SHA256 `6675b0e4e416b97450bde97ce25760780485dd499166bb353de3b1b7751c9e5f`
- `docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_988bc12ae3768679/NATIVE_PARAMETER_READBACK.json`；SHA256 `25c0cb22733e046bbfab8f7ae3c30f061d90399dabddc9922654a3f694d456cf`
- `docs/strict_author_route_validation_20261001/resume_after_quota_20261010T0533Z/papers/paper_988bc12ae3768679/REVIEW.json`；SHA256 `e6c212f0d0c76f57cf9a7f0a34e91c1ca8e5456c586a084d067ac1e488cbd5d8`
- `docs/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_988bc12ae3768679/EXISTING_RESULTS_UNIFIED_COMPARISON.json`；SHA256 `a580294b77fc244dfea52d98683885bdd82f466d484c3890f35a2fb08e7cbfaa`
- `docs/strict_author_route_validation_20261001/user_resolution_20261009T1305Z/papers/paper_988bc12ae3768679/sources/publisher_SI.docx`；SHA256 `b3633cc3dbdbae1fe21da6413596b8434189d1a6f4b55dafeeaa6975bc3acedf`
- source_optical：{"path": "papers/paper_988bc12ae3768679/documents/main.pdf", "sha256": "8ee6c2620ae4107f7fd8043982eb478ffa01714734e69416a7b186e9ff32e189", "pdf_pages_1based": [3, 6], "locator": "Section2.5 nonequilibrium cLR; Tables3–4,Fig4 dominant bright states"}
- source_switch：{"path": "papers/paper_988bc12ae3768679/documents/main.pdf", "sha256": "8ee6c2620ae4107f7fd8043982eb478ffa01714734e69416a7b186e9ff32e189", "pdf_pages_1based": [5, 6], "locator": "Fig3, OH protonation/deprotonation and hydrazone discussion"}
- source_nmr：{"path": "docs/strict_author_route_validation_20261001/user_resolution_20261009T1305Z/papers/paper_988bc12ae3768679/sources/publisher_SI.docx", "sha256": "b3633cc3dbdbae1fe21da6413596b8434189d1a6f4b55dafeeaa6975bc3acedf", "format": "DOCX", "locator": "word/document.xml, paragraph472 using 1-based all-descendant w:p enumeration (zero-based471); paragraph474 TableS2 caption; TableS2 chemical shifts. No PDF page claimed."}

## 时间与资源记录

本次迁移新增科学计算数0、HPC作业数0。历史输出中记录的逐作业资源可按原生/执行记录核查；没有统一完整的四篇总walltime、CPU-hour或费用记录，本报告不从核数或日志数量推算。失败、历史固定几何及控制计算不混入成功基线。

## 当前评分边界

中间科学结果80分；最终综合推断20分；全部定性叶子，满分或0。无精度充分校准的通用吸收/位移/结合能窗口，本轮不以最大残差拟合容差。身份、状态和证据是各项前提，不单独奖励。AR/PR具有相同物理判分清单；PR复现合同及合理替代义务仍由原题面约束，AR不被要求采用验证软件或固定搜索轨迹。

## 逐项科学规则—实际证据对应

下表明确本次验证对各项的支持，不使未来Agent自动获分。未来提交仍须独立有效证据。

| Rule / role / score | 实算支持 | 定位 |
|---|---|---|
| r_aqueous_base_redshift / intermediate / 20 | AcidS4 cLR3.3011eV versus baseS1 cLR2.6072eV; retain LR3.2271/2.5779 separately. | EXISTING_RESULTS_UNIFIED_COMPARISON.json/water_optics; isodpp_returned_geometry_definition_merge.json |
| r_nmr_acid_vs_neutral / intermediate / 12 | CommonTMS fourH acid8.1188416667>neutral7.1247416667ppm; all four atom shifts retained. | EXISTING_RESULTS_UNIFIED_COMPARISON.json/NMR_cases |
| r_nmr_base_vs_neutral / intermediate / 12 | CommonTMS fourH base6.3566666667<neutral7.1247416667ppm. | EXISTING_RESULTS_UNIFIED_COMPARISON.json/NMR_cases |
| r_bright_character_acid / intermediate / 10 | Main H137→L138 forward amplitude .64058; truncated doubled-square weight .8206854728, with other configurations retained; acidS4 dominant intensity. | isodpp_returned_geometry_definition_merge.json/paired_water_controls/acid |
| r_bright_character_base / intermediate / 10 | BaseS1 H137→L138 amplitude .5763 with further occupied contributions; bright f2.9118; no demanded pure single-configuration equality. | EXISTING_RESULTS_UNIFIED_COMPARISON.json/water_optics |
| r_hydrazone_competitor / intermediate / 16 | Neutral hydrazone valid174positive modes; +9.9761456177/+9.0405289920kcal/mol same-charge RRHO vsazo; cLR2.898eV andHmean6.5262916667ppm. | EXISTING_RESULTS_UNIFIED_COMPARISON.json/neutral_hydrazone_vs_azo_thermochemistry |
| r_joint_proton_response / conclusion / 20 | BalancedOH2protonated+2/phenoxide−2 identities jointly support optical/NMR direction and exclude a neutral-tautomer-only primary account, without unique site/population claim. | NATIVE_PARAMETER_READBACK.json; EXISTING_RESULTS_UNIFIED_COMPARISON.json |

补充原生输入/状态与分析路径：

- `docs/upgrade_tasks_verification/group_5/papers/paper_988bc12ae3768679/v2_execution_20260929/outputs/isodpp_returned_geometry_definition_merge_20261009_a01/isodpp_returned_geometry_definition_merge.json`；SHA256 `17bc2f4c3656b3cd4ef701585b654b7b9f913cbfc291a15f2198bb7915ded59c`

## 历史验证原文（保留；非当前验收/评分状态）

### 历史文件 docs/final_verified_science_v2_additions_20261020/astra_science_02/archive/paper_reproduction/paper_988bc12ae3768679/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot

# Verified computation reference — paper_988bc12ae3768679 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 4 | `PASS` | 最终严格状态：**PASS**。使用论文/SI 提供的 S0 Cartesian 几何，按作者 CAM-B3LYP/6-31+G(d) 气相 TDDFT 路线分别完成 +2 singlet acid（62 atoms）和 -2 singlet base（58 atoms）的 S1-S4。两个作业均正常终止，且未把早期错误的中性/PCM 探索作业纳入结果。 |
| 59 | `PASS` | 本篇 acid/base 作者路线端点、四态光谱和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Symmetric azobenzene-substituted diketopyrrolopyrroles dyes as acid-base switchable molecular-probe for colorimetric paper-based sensors
- DOI: `10.1016/j.dyepig.2025.113288`
- Task package: `tasks/final_verified_paper_reproduction/paper_988bc12ae3768679`
- Verification group: `docs/verification/group_3/paper_988bc12ae3768679`
- Paper documents: `papers/paper_988bc12ae3768679`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": "Brightest-state energies: 2a-acid=2.9342 eV; 2a-base=1.9892 eV.",
  "conclusion": "The calculated gas-phase vertical profiles are compared by brightest-state energy; a lower-energy base brightest transition supports the qualitative acid/base chromatic-switch interpretation within this boundary.",
  "limitations": "Gas-phase vertical excitations only; no solvent, vibronic, counterion or experimental band fitting. Earlier neutral/PCM exploratory jobs are excluded because their charge and phase violate the public endpoint.",
  "method": {
    "brightest_state_rule": "Within each S1-S4 set, select the state with maximum Gaussian oscillator strength.",
    "electronic_structure": "CAM-B3LYP/6-31+G(d,p) TD(Singlets,NStates=4) gas-phase vertical excitations",
    "geometry_treatment": "Supplied complete acid/base author S0 geometries; no geometry change",
    "software": "Gaussian 16 C.01; cclib parser",
    "state_coverage": "Four singlet states S1-S4 for each structure"
  },
  "structures": [
    {
      "brightest_state": "S3",
      "charge": 2,
      "input_validation": {
        "atom_count": 62,
        "converged": true,
        "geometry_provenance": "unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/acid_p2_gas_td4/stdout.log"
      },
      "multiplicity": 1,
      "name": "2a-acid",
      "states": [
        {
          "energy_eV": 2.5888,
          "gaussian_label": "Singlet-?Sym",
          "label": "S1",
          "oscillator_strength": 0.0009,
          "wavelength_nm": 478.9253646477132
        },
        {
          "energy_eV": 2.5974,
          "gaussian_label": "Singlet-?Sym",
          "label": "S2",
          "oscillator_strength": 0.0001,
          "wavelength_nm": 477.33964117964115
        },
        {
          "energy_eV": 2.9342,
          "gaussian_label": "Singlet-?Sym",
          "label": "S3",
          "oscillator_strength": 2.6631,
          "wavelength_nm": 422.548559743712
        },
        {
          "energy_eV": 2.9999,
          "gaussian_label": "Singlet-?Sym",
          "label": "S4",
          "oscillator_strength": 0.0027,
          "wavelength_nm": 413.29443781459383
        }
      ]
    },
    {
      "brightest_state": "S1",
      "charge": -2,
      "input_validation": {
        "atom_count": 58,
        "converged": true,
        "geometry_provenance": "unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/base_m2_gas_td4/stdout.log"
      },
      "multiplicity": 1,
      "name": "2a-base",
      "states": [
        {
          "energy_eV": 1.9892,
          "gaussian_label": "Singlet-?Sym",
          "label": "S1",
          "oscillator_strength": 2.2515,
          "wavelength_nm": 623.28674039815
        },
        {
          "energy_eV": 2.2631,
          "gaussian_label": "Singlet-?Sym",
          "label": "S2",
          "oscillator_strength": 0.0083,
          "wavelength_nm": 547.8511705183155
        },
        {
          "energy_eV": 2.8849,
          "gaussian_label": "Singlet-?Sym",
          "label": "S3",
          "oscillator_strength": 0.0001,
          "wavelength_nm": 429.7694838642587
        },
        {
          "energy_eV": 2.8955,
          "gaussian_label": "Singlet-?Sym",
          "label": "S4",
          "oscillator_strength": 0.0,
          "wavelength_nm": 428.1961609393887
        }
      ]
    }
  ]
}
```

Paper/SI document hashes:

- `papers/paper_988bc12ae3768679/documents/main.pdf` — SHA-256 `8ee6c2620ae4107f7fd8043982eb478ffa01714734e69416a7b186e9ff32e189` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |
- 独立计算完成后才读取 evaluator 对照；acid/base 两套气相 CAM-B3LYP/6-31+G(d) S1–S4 光谱、最亮态和能量排序均已由原始输出闭合并与 evaluator 一致。
- 本篇 acid/base 作者路线端点、四态光谱和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **60**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/status.json` — successful status record; SHA-256 `97edeb5b01014af4d035964d47cad5afb9aadf305bfba00024d9905a618c2ccd`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4_optimized.xyz` — successful execution artifact; SHA-256 `b66351d1f4e3b0013a2b3e4b9e6d31cf11153ec9c317a936e1043264557c9ff6`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/collection.json` — successful execution artifact; SHA-256 `08483fca3265064b3e20e3074a60e9ce02d2f28630ceddfaa919fd454b615514`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/formchk.log` — successful execution artifact; SHA-256 `597af31a5394846865cadbce48496732b47a62f9be1473a1b05c343a27d43117`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/input.com` — successful execution artifact; SHA-256 `b1454568ccaf88069c355f1f3f5d62d78ed8b63f53519932f2f48128f5593956`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/status.json` — successful status record; SHA-256 `c233caecd389ed07b56418f02d184636597305af5edd0851627a02366b14722b`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td_optimized.xyz` — successful execution artifact; SHA-256 `05006f9472c9779e53c2364c0b1212cee163c7ae59ffe876342c3662d9882873`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/collection.json` — successful execution artifact; SHA-256 `2e6332eb30c773690f79d305f5c4f66c0fb911b8ec7d451e6281c6a1123df22a`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/formchk.log` — successful execution artifact; SHA-256 `9107195e5bc67128d7dfb4937a06506a742938d1285d29b9ea2a990444c2942c`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/input.com` — successful execution artifact; SHA-256 `3931bd49f9499a74f878d52282aa3d455132838896f8bea1c7e2848084e4835e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/status.json` — successful status record; SHA-256 `546f302a205ba9fcdb6e35924a4405ea6a33a20ee0069ef1f087d22f3fb0177a`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4_optimized.xyz` — successful execution artifact; SHA-256 `8d914b58300661ecebc1dcc06e984c79791728e4e163d0d8f83f11c926066453`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/collection.json` — successful execution artifact; SHA-256 `ff48ac4c76a8baf6db10cff57116b952e005a8d116a4195a604f1b39de10ddc4`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/formchk.log` — successful execution artifact; SHA-256 `52ff6ff1715ba5c723b52570bca72f58c088e8cd120fea9206caf1dcd628f062`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/input.com` — successful execution artifact; SHA-256 `c06efd32dc33116b0c9c9cdf5a0eabfb505199b58bf3e7d296d04acc935167d2`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/status.json` — successful status record; SHA-256 `961a18df0d7ce35eb2441ed399990c4b8704089c4ef56159bfeaa46304ff1ea6`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4_optimized.xyz` — successful execution artifact; SHA-256 `60137b0272ac49c2791225227d065b072ca59a1319ef5114201a61bb47353200`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/collection.json` — successful execution artifact; SHA-256 `cb0620060f36bcd7dd63738953dec14bf46e695f8092e64e30b829fbc7b3c19e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/formchk.log` — successful execution artifact; SHA-256 `177349ffcea80d33775d7506f4cd41d26946616f9fea3e7020386f5f63e2e903`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/input.com` — successful execution artifact; SHA-256 `d3a0848465d1ed04fd3afd7b8239cc998aa4d9e02e2226f2533d3a74da3d6c1d`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/status.json` — successful status record; SHA-256 `3713fa58ce3f7c9863b593bf813b3c054524c81c07f1ddcc4eb5f2656a437269`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td_optimized.xyz` — successful execution artifact; SHA-256 `66a2aa72281142b7d1ae08b25fb5f8ba700057b6610752ab846c9409070ee5f9`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/collection.json` — successful execution artifact; SHA-256 `48245d2dd07e79798b08090d586f4f89be39e4814356e6c2ae4482120f0402d8`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/formchk.log` — successful execution artifact; SHA-256 `3516a8739cf4553389809c0cdf932a89e2429a74bdbbbb3fa764b5ef2432b671`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/input.com` — successful execution artifact; SHA-256 `ef219bd0438fa787cfdddf55f3aab2c07374b53568077b8cd895ee64a16bc23a`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/status.json` — successful status record; SHA-256 `fafea56cee3ac861371c53ac30d07d8b928dbc68640fddac8d54e02a8d39ed54`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4_optimized.xyz` — successful execution artifact; SHA-256 `e2e47a03e8685543d2af490e09194df7eefc66e2f734f87ef0734164b424677e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/collection.json` — successful execution artifact; SHA-256 `8670e18a469b73cba324bb33e3b4f3adccddc53aa3d126b4f05ce613c7771445`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/formchk.log` — successful execution artifact; SHA-256 `03041aaeec78052b234d88a5266171ad4bb345e633a8466fb7524229d1e5ba32`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/input.com` — successful execution artifact; SHA-256 `8c731e8e32e188a3d5db7fd94bc2bb2494f279c976149ace772a775d32be98a0`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/status.json` — successful status record; SHA-256 `97edeb5b01014af4d035964d47cad5afb9aadf305bfba00024d9905a618c2ccd`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/collection.json` — successful execution artifact; SHA-256 `08483fca3265064b3e20e3074a60e9ce02d2f28630ceddfaa919fd454b615514`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/input.com` — successful execution artifact; SHA-256 `b1454568ccaf88069c355f1f3f5d62d78ed8b63f53519932f2f48128f5593956`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/request.json` — successful execution artifact; SHA-256 `827f72283cca47146a2e41920f468cef662f20befd8fb72db8cdfcb2cdd3d856`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/status.json` — successful status record; SHA-256 `c233caecd389ed07b56418f02d184636597305af5edd0851627a02366b14722b`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/collection.json` — successful execution artifact; SHA-256 `2e6332eb30c773690f79d305f5c4f66c0fb911b8ec7d451e6281c6a1123df22a`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/input.com` — successful execution artifact; SHA-256 `3931bd49f9499a74f878d52282aa3d455132838896f8bea1c7e2848084e4835e`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/request.json` — successful execution artifact; SHA-256 `55282771dfa8100f2bb181bf0d37911658d8a074092e57ebef00ad8521b8bb30`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/status.json` — successful status record; SHA-256 `546f302a205ba9fcdb6e35924a4405ea6a33a20ee0069ef1f087d22f3fb0177a`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/collection.json` — successful execution artifact; SHA-256 `ff48ac4c76a8baf6db10cff57116b952e005a8d116a4195a604f1b39de10ddc4`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/input.com` — successful execution artifact; SHA-256 `c06efd32dc33116b0c9c9cdf5a0eabfb505199b58bf3e7d296d04acc935167d2`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/request.json` — successful execution artifact; SHA-256 `a928c1756cee554115f4e00c0a930ba1623ef533922699d31ab830832b4ca392`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/status.json` — successful status record; SHA-256 `961a18df0d7ce35eb2441ed399990c4b8704089c4ef56159bfeaa46304ff1ea6`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/collection.json` — successful execution artifact; SHA-256 `cb0620060f36bcd7dd63738953dec14bf46e695f8092e64e30b829fbc7b3c19e`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/input.com` — successful execution artifact; SHA-256 `d3a0848465d1ed04fd3afd7b8239cc998aa4d9e02e2226f2533d3a74da3d6c1d`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/request.json` — successful execution artifact; SHA-256 `04f3b89bb49d8509f4cc42b593148847aafa64e641d501c3ca1f6cfce2351147`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/status.json` — successful status record; SHA-256 `3713fa58ce3f7c9863b593bf813b3c054524c81c07f1ddcc4eb5f2656a437269`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/collection.json` — successful execution artifact; SHA-256 `48245d2dd07e79798b08090d586f4f89be39e4814356e6c2ae4482120f0402d8`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/input.com` — successful execution artifact; SHA-256 `ef219bd0438fa787cfdddf55f3aab2c07374b53568077b8cd895ee64a16bc23a`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/request.json` — successful execution artifact; SHA-256 `0740035c84c5fe1ae69b9d0ae52825c90ec563722cfdf78565e2030208298937`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/status.json` — successful status record; SHA-256 `fafea56cee3ac861371c53ac30d07d8b928dbc68640fddac8d54e02a8d39ed54`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/collection.json` — successful execution artifact; SHA-256 `8670e18a469b73cba324bb33e3b4f3adccddc53aa3d126b4f05ce613c7771445`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/input.com` — successful execution artifact; SHA-256 `8c731e8e32e188a3d5db7fd94bc2bb2494f279c976149ace772a775d32be98a0`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/request.json` — successful execution artifact; SHA-256 `465772304d6137c6a7b27a5a9e9a87d24a808f0f066299b7e0c747cf3349501b`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/base_td/status.json` — label=group_3 paper_988bc12ae3768679 base_td; submitted_at=2026-08-29T07:42:30.795787+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/stderr.log`
2. `artifacts/gaussian/acid_td/status.json` — label=group_3 paper_988bc12ae3768679 acid_td; submitted_at=2026-08-29T07:42:31.538047+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/stderr.log`
3. `artifacts/gaussian/acid_td_td4/status.json` — label=group_3 paper_988bc12ae3768679 acid_td_td4; submitted_at=2026-08-29T15:53:50.955091+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=4) SCRF=(PCM,Solvent=Water) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/stderr.log`
4. `artifacts/gaussian/base_td_td4/status.json` — label=group_3 paper_988bc12ae3768679 base_td_td4; submitted_at=2026-08-29T15:53:51.733918+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=4) SCRF=(PCM,Solvent=Water) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/stderr.log`
5. `artifacts/gaussian/acid_p2_gas_td4/status.json` — label=group_3 paper_988bc12ae3768679 acid_p2_gas_td4; submitted_at=2026-08-30T02:13:11.951180+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-31+G(d,p) TD=(Singlets,NStates=4) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/stderr.log`
6. `artifacts/gaussian/base_m2_gas_td4/status.json` — label=group_3 paper_988bc12ae3768679 base_m2_gas_td4; submitted_at=2026-08-30T02:13:16.466203+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-31+G(d,p) TD=(Singlets,NStates=4) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/stderr.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `pr_limitations`, `pr_r6`.

- Key-point IDs: `pr_process_inputs, pr_process_coverage, pr_result_acid, pr_result_base`
- Conclusion IDs: `pr_final_switch, pr_limitations`
- Scoring-rule IDs: `pr_r1, pr_r2, pr_r3, pr_r4, pr_r5, pr_r6`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `pr_r1` → reference `pr_process_inputs`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert validation; evaluator_target_present=False
- rule `pr_r2` → reference `pr_process_coverage`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert validation; evaluator_target_present=False
- rule `pr_r3` → reference `pr_result_acid`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=state identity and numeric comparison; evaluator_target_present=False
- rule `pr_r4` → reference `pr_result_base`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=state identity and numeric comparison; evaluator_target_present=False
- rule `pr_r5` → reference `pr_final_switch`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r6` → reference `pr_limitations`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].name` = `"2a-acid"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].charge` = `2`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].multiplicity` = `1`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].input_validation.atom_count` = `62`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].input_validation.geometry_provenance` = `"unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/acid_p2_gas_td4/stdout.log"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].input_validation.converged` = `true`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].label` = `"S1"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].energy_eV` = `2.5888`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].wavelength_nm` = `478.9253646477132`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].oscillator_strength` = `0.0009`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].label` = `"S2"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].energy_eV` = `2.5974`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].wavelength_nm` = `477.33964117964115`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].oscillator_strength` = `0.0001`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].label` = `"S3"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].energy_eV` = `2.9342`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].wavelength_nm` = `422.548559743712`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].oscillator_strength` = `2.6631`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].label` = `"S4"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].energy_eV` = `2.9999`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].wavelength_nm` = `413.29443781459383`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].oscillator_strength` = `0.0027`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[0].brightest_state` = `"S3"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].name` = `"2a-base"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].charge` = `-2`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].multiplicity` = `1`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].input_validation.atom_count` = `58`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].input_validation.geometry_provenance` = `"unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/base_m2_gas_td4/stdout.log"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].input_validation.converged` = `true`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].label` = `"S1"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].energy_eV` = `1.9892`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].wavelength_nm` = `623.28674039815`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].oscillator_strength` = `2.2515`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].label` = `"S2"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].energy_eV` = `2.2631`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].wavelength_nm` = `547.8511705183155`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].oscillator_strength` = `0.0083`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].label` = `"S3"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].energy_eV` = `2.8849`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].wavelength_nm` = `429.7694838642587`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].oscillator_strength` = `0.0001`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].label` = `"S4"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].energy_eV` = `2.8955`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].wavelength_nm` = `428.1961609393887`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].oscillator_strength` = `0.0`
- rule `pr_r1` / reference `pr_process_inputs` / field `$.structures` / result path `$.structures[1].brightest_state` = `"S1"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].label` = `"S1"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].energy_eV` = `2.5888`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].wavelength_nm` = `478.9253646477132`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].oscillator_strength` = `0.0009`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].label` = `"S2"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].energy_eV` = `2.5974`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].wavelength_nm` = `477.33964117964115`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].oscillator_strength` = `0.0001`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].label` = `"S3"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].energy_eV` = `2.9342`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].wavelength_nm` = `422.548559743712`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].oscillator_strength` = `2.6631`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].label` = `"S4"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].gaussian_label` = `"Singlet-?Sym"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].energy_eV` = `2.9999`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].wavelength_nm` = `413.29443781459383`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].oscillator_strength` = `0.0027`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].energy_eV` = `1.9892`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].wavelength_nm` = `623.28674039815`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].oscillator_strength` = `2.2515`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].energy_eV` = `2.2631`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].wavelength_nm` = `547.8511705183155`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].oscillator_strength` = `0.0083`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].energy_eV` = `2.8849`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].wavelength_nm` = `429.7694838642587`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].oscillator_strength` = `0.0001`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].energy_eV` = `2.8955`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].wavelength_nm` = `428.1961609393887`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].oscillator_strength` = `0.0`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].brightest_state` / result path `$.structures[*].brightest_state` = `"S3"`
- rule `pr_r2` / reference `pr_process_coverage` / field `$.structures[*].brightest_state` / result path `$.structures[*].brightest_state` = `"S1"`
- rule `pr_r5` / reference `pr_final_switch` / field `$.comparison` / result path `$.comparison` = `"Brightest-state energies: 2a-acid=2.9342 eV; 2a-base=1.9892 eV."`
- rule `pr_r5` / reference `pr_final_switch` / field `$.conclusion` / result path `$.conclusion` = `"The calculated gas-phase vertical profiles are compared by brightest-state energy; a lower-energy base brightest transition supports the qualitative acid/base chromatic-switch interpretation within this boundary."`
- rule `pr_r6` / reference `pr_limitations` / field `$.limitations` / result path `$.limitations` = `"Gas-phase vertical excitations only; no solvent, vibronic, counterion or experimental band fitting. Earlier neutral/PCM exploratory jobs are excluded because their charge and phase violate the public endpoint."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized/final structure is exposed as agent input for a scored comparison; redesign with neutral or independently generated starting geometry
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Complete XYZ geometries for named 2a-acid (+2, singlet) and 2a-base (-2, singlet) S0 structures.

Public input files and hashes:

- `agent_input/data/inputs/2a-acid.xyz` — SHA-256 `97e77fb559a4358b103df2fb1b1d8a1287c3744158bb3c7b55e70dd021403695`; size=4238 bytes; xyz_atom_count=62; xyz_comment=2a-acid Provided Cartesian geometry (angstrom); explicit_boundary_fields={"units_hint": "explicit angstrom marker"}
- `agent_input/data/inputs/2a-base.xyz` — SHA-256 `55e0e8ae86e4bf6aa39d33c313d30e82e6044a4ff8e6b31effca5a9cd623490e`; size=3960 bytes; xyz_atom_count=58; xyz_comment=2a-base Provided Cartesian geometry (angstrom); explicit_boundary_fields={"units_hint": "explicit angstrom marker"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_988bc12ae3768679/verification_report.md` — verification record; SHA-256 `422c9a2d064e2c7203428ad6f232de484912e1c7304b63d29de7a57062f81987`
- `docs/verification/group_3/paper_988bc12ae3768679/report/results.json` — verification record; SHA-256 `f40049c6d112e5e1af72df5075f1cce643a5e209e8ffa67b9d1a3ec1df59373e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/stdout.log` — referenced successful evidence; SHA-256 `ace4a1a89048726ebc75a07317520c01463a8ee0b805a8147c44433e0c139fa4`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/stdout.log` — referenced successful evidence; SHA-256 `5669b89b9807dd2c73a1350179dedd9c9c73ffe7454176f01388ed71d6c80684`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.

