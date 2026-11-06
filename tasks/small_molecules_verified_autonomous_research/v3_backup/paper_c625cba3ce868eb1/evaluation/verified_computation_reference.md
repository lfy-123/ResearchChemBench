# 2026-11-04 来源、原生结果与评分口径复核

正文PDF3–5和SI PDF30 Fig.S50支持反应物局部位点极化的有界解释，不证明唯一机制或势垒。历史MK结果重新读取后与旧记录一致，水/DCM及网格变化均保留极化方向。本次明确：单个孤立构象的距离较短不能单独建立选择性的分子原因；替代预组织解释需把该构型与相关位点的反应区分联系起来。继续接受有证据支持的反应物极化解释，不新增TS、固定构象数量或对7的必算要求。原100分保留为历史Judge记录，需按修订规则另行复评才产生新分数。

本次逐份原始读取：[source_readback.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/GPT61_四项复核与运行修复_20261104/source_readback.json)；[修改方案](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/GPT61_四项复核与运行修复_20261104/修改方案.md)。以下历史验证记录保留原样，不恢复旧数值门槛。

# Round-one scope notice — 2026-11-03

The existing scientific scope is retained. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## 2026-10-27 V3 final-result scope

This version scores independent final answers only. Current rules are in scoring_rules.json; per-conclusion evidence reuse and limits are in final_result_coverage.json. Historical native calculations below are retained unchanged and are not an automatic PASS for the new rubric. No new quantum calculation was run.

> 2026-10-17 当前状态同步：已有2026-10-11的现行限定科学问题验收证据，本轮复核并同步记录，没有新增量化计算。[当前状态及限制](current_verification_status.json)区分科学覆盖与评分/发布资格。下方旧pending、失败和目录位置按原日期/范围保留，不覆盖后续现行验收；本次整理不自动放行正式评分或发布。



<!-- phase2-verification-20261010T231612Z-group03 -->
## 2026-10-11 第二阶段第3组：当前范围的参考计算验证

核查时间：2026-10-11T06:30:25.314640+00:00；状态：**PASS**。当前全部必需科学目标已验证通过（仅下述当前范围）。

当前保留范围的有限分子解释验证通过：水相原始MK极化比8.7943、同密度加密比8.6380，对照源9.0；新增DCM的R4/7有符号电荷差−.483009/−.056217e、比8.5919。R/E、OH/OOH图和六元闭环拓扑保持。支持与来源相容的反应物电子偏置解释，并明确未隔离OOH唯一因果、未求动力学势垒。 正文PDF4明确将极化限定于反应物、未由此指定唯一机理，本次判定遵守这一来源边界。

本轮开始时审查的包 SHA-256：`c2c51f074c088bb888eed0273c89099aefc3563c76ce141412c450cb8bedb1d9`。科学合同及所有非reference载荷的哈希保持不变；本次仅追加本证据段并更新本包manifest。更新后完整包哈希由package_manifest.json和本组completion.json记录，避免自引用哈希。

本次可读作者原文/SI并复用其路线，属于参考计算验证，**不是盲测结果**。历史记录保留；若历史PASS覆盖范围小于当前任务，以本轮逐目标覆盖为准。

|当前目标|状态|来源结果|实际结果|差值、原容差与解释|
|---|---|---|---|---|
|kp_identity|VERIFIED|Correctidentityandringtopology|{"positive_modes": [93, 69], "OH": [21, 22], "OOH": [23, 24, 25], "O21_to_C4_ring": 6, "O21_to_C2_ring": 7}|图路径21-18-15-9-6-4成6环；连接2为7环。原图22是H；未把裸Br−当亲电试剂。|
|kp_selectivity|VERIFIED|{"signed_charge_differences_e": [-0.441, -0.049], "magnitude_ratio": 9.0}|{"default_difference_e": [-0.484265, -0.055066], "default_ratio": 8.79426506374169, "dense_difference_e": [-0.427513, -0.049492], "dense_ratio": 8.638022306635419, "DCM_signed_difference_e": [-0.483009, -0.05621700000000002], "DCM_ratio": 8.591867228774213}|默认差值残差−.043265/−.006066e，加密+.013487/−.000492e；定性方向/大小关系保留，无来源支持的统一电荷容差。|
|kp_causality|VERIFIED|Author polarizingrationale; otherstructuraleffectsacknowledged|Same-densityMKsampling preservesordering; skeleton/branching/stereochemistry confounded|水相/同密度拟合控制与新增DCM比较共同支持有限反应物电子偏置；OOH与支化/立体共同变化，唯一OOH因果未主张。当前条款要求合理审视混杂，不要求在不主张唯一因果时强制完整TS/控制矩阵。|
|kp_uncertainty|VERIFIED|{"NBS_printed_mM": 473, "NBS_amount_mmol": 0.284, "DCM_mL": 6}|{"amount_volume_mM": 47.33333333333333, "DCM_sensitivity": [{"object": "R4", "native_log": "docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/outputs/R4_DCM_optfreq_MK/gaussian.log", "sha256": "9952366b8aa0291c4405a9ae9ba006143bada9a7de2b68f20caffe2d8d81d843", "water_population_log": "docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/R4_default_density1/gaussian.log", "water_population_sha256": "424a376c366a35593af6077548ed19985831c638ce71122b57e352e5cf2337e7", "modes": 93, "minfreq": 19.7819, "MK_signed_DCM_e": -0.483009, "MK_signed_water_e": -0.484265, "DCM_minus_water_e": 0.0012559999999999794, "DCM_vs_water_same_index_graph": true}, {"object": "7", "native_log": "docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/outputs/7_DCM_optfreq_MK/gaussian.log", "sha256": "d99634af0ee3ce2ded5b01c50abac41f131422f278ad9d603a43d10ed8767dac", "water_population_log": "docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/v2_execution_20260929/outputs/Br_saved_curvature_and_MK_density_control_20261007/a01/native_population/7_default_density1/gaussian.log", "water_population_sha256": "b84648198f5a9e1569f0dbbdd5a1698dc3c30f34ed656e842703a4753398181e", "modes": 69, "minfreq": 36.5721, "MK_signed_DCM_e": -0.05621700000000002, "MK_signed_water_e": -0.055066000000000004, "DCM_minus_water_e": -0.0011510000000000131, "DCM_vs_water_same_index_graph": true}]}|保留来源浓度冲突；室温未赋虚构精度；C01替代来源A03不声称二进制一致。|
|kp_scope|VERIFIED|Nonenzymecontrol can reproduce relatedproduct pattern|Localgraphandpolarization only; failed67atompath explicitly excluded|没有酶因果、全级联收率或完整动力学声明。|
|conclusion_investigation|VERIFIED|R4strongeralkenepolarization supports limitedselectivityrationale|R4相较7的更强烯烃极化在源水相与新DCM均成立；更负C2与Br亲电作用、OH闭合C4的六元拓扑给出与来源相容的有限解释。未宣称动力学顺序或唯一微观机制。|当前有限问题的来源核心方向、正确结构、数量比较、介质检验和不确定性已覆盖；此PASS不涵盖TS/速率/产率，亦非因开放规则允许未解决结果而通过。|

来源页码/图表、物理定义、输入输出路径及SHA-256见 [coverage.json](../../../../docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/coverage.json)；完整结论和逐作业诊断见 [verification_report.md](../../../../docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/verification_report.md)。
新原始计算记录见 [jobs.json](../../../../docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/jobs.json)、[完成结果原生提取](../../../../docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/new_completed_results.json)、[实际资源与步骤](../../../../docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/resource_accounting.json)。每个结果JSON链接真实应用日志；平台SUCCEEDED、孤立实频或哈希本身均不构成机理通过。

当前结论边界：

- PASS仅限当前(R)-4有限分子解释，不涵盖整个3/4混合物、完整动力学、酶控制或产率。
- 水相/DCM连续介质与一个构象不代表实际NBS/Et3N全系综；未主张唯一微观机理。
- 源473mM与量体积47.3mM冲突保留，未用于速率结论。
- 67atom历史点5失败保留，不作为通过证据；当前题未在不主张TS时强制该特定路线。

后继条件、依赖job IDs及一次性恢复入口见 [successor.json](../../../../docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/successor.json)。运行/排队作业未标成科学完成；未启动自动周期resume。来源/规则问题见 [本组修复建议](../../../small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/phase2_verification/group_03/repair_proposals.md)，本轮未修改题目或放宽阈值。


## 2026-10-11 科研设计升级的验证适用边界

本轮任务设计已按逐篇方案审查并合入，当前task.md SHA256为`03b81b90bee517fed35f54173b7cbdc8773e6b28879e112b53e20e88e8b11db8`。以上历史计算及PASS仅适用于其明确覆盖的旧目标，不自动验证新增范围或修正后的分子对象。新范围状态：PENDING_DELTA_VERIFICATION；不得据此发布。逐篇方案：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/scope_upgrade_execution_20261011T081201Z/plans/paper_c625cba3ce868eb1.md`。独立验证进程会复用有效结果、补差集并追加逐目标覆盖。

<!-- scope-upgrade-independent-verification-g04-20261011 -->

## 2026-10-11 本轮冻结范围的独立增量验证

更新：2026-10-11T21:34:33.999654+00:00。执行状态：**PASS**；当前科学状态：**PASS**；所有必需结果恢复：**true**。

当前冻结task.md SHA256：`03b81b90bee517fed35f54173b7cbdc8773e6b28879e112b53e20e88e8b11db8`。本进程逐项检查assignment设计hash不变，只追加reference并重建本包manifest；新包hash见本组manifest_changes.json。

| 当前必需目标/结论 | 状态 | native与源差异/可比性 |
|---|---|---|
| kp_reactant_polarization | PASS | native：`{"water_default_R4_e": [-0.533926, -0.049661], "water_dense_R4_e": [-0.499762, -0.072249], "water_default_7_e": [-0.313449, -0.258383], "water_dense_7_e": [-0.309513, -0.260021], "R4_signed_water_default_e": -0.484265, "R4_signed_water_dense_e": -0.427513, "water_default_ratio_R4_to_7": 8.79426506374169, "water_dense_ratio_R4_to_7": 8.638022306635419}`；native−source：`{"default_R4_atom_residual_e": [-0.026926, 0.016339], "dense_R4_atom_residual_e": [0.007238, -0.006249], "default_signed_residual_e": -0.043265, "dense_signed_residual_e": 0.013487}`。同一全H MK/ESP观测，水相B3LYP/CBSB7；默认与加密并列而非挑值。源未给网格/半径，不定义新统一容差。当前目标允许恢复定量方向/极化，不强制未校准逐原子精确相等。 |
| kp_local_regioselectivity | PASS | native：`{"DCM_R4_e": [-0.528946, -0.045937], "DCM_7_e": [-0.311241, -0.255024], "DCM_R4_signed_e": -0.483009, "DCM_7_signed_e": -0.056217, "DCM_ratio": 8.591867228774213, "DCM_minima_positive_modes": [93, 69], "closures": {"O21_C4": 6, "O21_C2": 7}, "balanced_bromination_product_graphs": 2}`；native−source：`{"DCM_minus_water_R4_signed_e": 0.001256}`。独立DCM量化检验与两个守恒产物图共同连接底物偏置到六/七元结果，超出重复一个水相电荷标量。NBS亲电Br加至更负C2、OH闭合C4给六元；反向为七元。是与源相容的有限电子解释，不是动力学/特定bromiranium证明。 |
| conclusion_reaction | PASS | native：`{"bounded_electronic_structural_explanation": true, "unique_microscopic_mechanism": false, "kinetics_or_yield_predicted": false}`；native−source：`null`。正文p4明确reactant-level相关性范围；DCM介质与竞争图增量证据支持当前限定结论。7仍是可选电子参照，非NBS产率控制。 |

完整逐目标报告：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/verification_report.md)；来源/源值/单位/参照/原容差与全部hidden目标：[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/coverage.json)。

重新读取的Gaussian原始证据：[native_reextraction.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/native_reextraction.json)；化学图、立体、电荷与参照算术：[reuse_analysis.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/reuse_analysis.json)；新增实际原生进展：[new_native_readback.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/new_native_readback.json)。

已完成旧作业收取：[historical_jobs_collected.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/historical_jobs_collected.json)；新增作业：[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/jobs.json)；实际步骤/墙钟：[resource_accounting.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/resource_accounting.json)；精确后继：[successor.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/successor.json)。

人口计算几何与最低点对应、DCM变化及公开R/E：[population_geometry_and_public_stereo.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_4/paper_c625cba3ce868eb1/scope_upgrade_20261011T081201Z_g04/population_geometry_and_public_stereo.json)。

PASS严格限于当前允许的源边界电子/结构解释；未认证具体TS、动力学、唯一OOH因果、纯R4产率或精确MK末位小数。水相和DCM原生结果均复用，未重算有效结果。

旧PASS或平台SUCCEEDED未用作科学判据。新计算若仍运行，不能称验证完成。源模型/单位/零点问题不通过改变目标或扩大容差解决。本次可读作者路线，非盲测；未启动周期resume或另一个Codex。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`a0956887c604aa6d3a9fc32bebacee929f4a3dee9e2b4121adc536f619e08735`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_03/reports/paper_c625cba3ce868eb1/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_03/reports/paper_c625cba3ce868eb1/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_03/reports/paper_c625cba3ce868eb1/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。


### 自主科研设计交叉复审补充

复审时间：2026-10-12T01:10:47.491427+00:00。本次仅修订任务合同或来源映射，不新增量化计算通过结论。已保留此前全部计算记录。父复审记录：[paper_c625cba3ce868eb1](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/parent_review/paper_c625cba3ce868eb1_decision.json)；变更文件：`agent_input/submission_guide.md`。
