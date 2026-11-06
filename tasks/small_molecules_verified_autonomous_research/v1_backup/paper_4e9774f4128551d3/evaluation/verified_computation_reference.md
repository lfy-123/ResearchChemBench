## 2026-10-20 专家第一轮评分规则同步

端点自由能差降为 20 分、三轮循环物料衡算增为 30 分；明确用单次比例及其来源论证 70% 累计收率的合理性。条件解释 30 分、最终结论 20 分保留。

本节记录评分合同变更；下方原日期的计算结果、旧规则和验收范围按历史保留，不作为额外的现行评分要求。当前规则以 scoring_rules.json、reference_key_points.json 和 reference_conclusions.json 为准。本轮没有新增量子化学作业。

> 2026-10-17 当前状态同步：已有2026-10-12的现行限定科学问题验收证据，本轮复核并同步记录，没有新增量化计算。[当前状态及限制](current_verification_status.json)区分科学覆盖与评分/发布资格。下方旧pending、失败和目录位置按原日期/范围保留，不覆盖后续现行验收；本次整理不自动放行正式评分或发布。



<!-- phase2_group04_20261010T231612Z BEGIN -->

## 2026-10-11 第二阶段 group04 参考计算验证

执行状态：**PASS**。科学覆盖：**PASS**。更新时刻：2026-10-11T06:01:01.234715+00:00。

当前保留范围通过：真实端点恢复trans热力学偏好，独立详细平衡反例证明端点差不能决定30分钟单次比例；不声称已算质子化路径或全部源绝对能。

本次审查原包SHA256：`625d55a89e6458e30ee4a36e3e511f01f4181e3e91741dbb41845cfed10ee86e`；当前科学合同文件集合SHA256（不含本证据文档）：`b84bb5a7e0d15d14061d6f705604c0c8ebcfb5fef4e703b8005dd39f6bec396f`。更新后完整包SHA256在package_manifest.json及本组manifest_changes.json/completion.json，避免把本文件哈希自包含。

报告：[docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/verification_report.md)；逐目标定义/来源/差值/阈值：[docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/coverage.json)；原生日志行定位及真实耗时：[docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/native_evidence_index.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/native_evidence_index.json)。

|当前目标|判定|真实结果与边界|
|---|---|---|
|kp_identity|PASS|原生50/S20各53原子C20H30O3、q0/singlet/153实频，C6R→S，远端11S/13R/30S不变，源公开50图与原生异构SMILES一致。O-TMS图保留三远端手性，CSA为相反4/7 CIP两对映体；计量两侧C34H58O8SSi/102原子/q0。准备图不称最低点。|
|kp_question|PASS|原生高层SP+各自低层Gcorr给ΔG(S20−50)=2.64122503，对源2.3171919差+.32403313kcal/mol，恢复trans偏好。独立解三状态模型保持相同端点G与详细平衡，却在1800s给T/C≈.1、1.1、10，定量检验了从端点直接推选择性的错误推论。|
|kp_discrimination|PASS|正文6明确可逆条件只得trans，单次CSA微偏trans的1.1:1，三轮回收得到cis70%；三者不同观测。有限时间反例保持概率和详细平衡，未拟合实验，不据反例声称真实TS或实际反应已经平衡。|
|kp_uncertainty|PASS|SI21 THF/MeOH=6/.60mL(10:1)与main Scheme5 1:1冲突保留。源低层E(SCF)/DZ列其实数值匹配原生E+Gcorr，防止再加热项；高层绝对SP仍偏约.01358/.01410Eh。G09Defaults/FineGrid实际控制仍给相近正ΔG；296.15/298.15K反例只是固定G下的温度敏感性。|
|kp_conclusion|PASS|恢复源trans热力学偏好，同时证明这个定量结果不足以唯一给出CSA质子化选择性。局部有限结论有实际分子证据和新数值分析；未声称优化酸条件、精确1.1:1或70%预测。|
|conclusion_investigation|PASS|通过的是当前保留的局部问题和有据的解释边界：trans较稳，与可逆实验一致；单次质子化比例须额外动力学/介质证据。无已退休强制质子化矩阵要求，不扩大为全文机理精确复现。|

本轮计算：[docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/jobs.json)；原生退出/频率/资源记录：[docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/new_native_results.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/new_native_results.json)。旧结果复用部分不重复量化计算；重分析由本组保存的Python脚本实际执行。失败、停止、排队和正在运行均不作为科学成功。

本轮作业ID：无新增HPC，复用有效结果与独立数值分析。

未决和规则问题：

- 非当前科学通过阻塞项：溶剂1:1/10:1冲突、源绝对高层SP偏差仍保留，未认证论文所有数字。
- 历史策略问题（已失效，现行scientific_results.v1）：当时open_research允许相反或未决结论获满分；本次PASS依据实际恢复的trans偏好及定量推论检验，不依据该宽松规则。

可恢复后继：[docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/recovery_plan.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/small_molecules_20261010T231612Z_g04/recovery_plan.json)。本轮没有移动任务、修改源包/目标/阈值、启动子代理或周期resume。

<!-- phase2_group04_20261010T231612Z END -->


## 2026-10-11 科研设计升级的验证适用边界

本轮任务设计已按逐篇方案审查并合入，当前task.md SHA256为`b1f5e062b145bb38ef24289e969219885caf48f077a0a5def19d9957a3503b4b`。以上历史计算及PASS仅适用于其明确覆盖的旧目标，不自动验证新增范围或修正后的分子对象。新范围状态：PENDING_DELTA_VERIFICATION；不得据此发布。逐篇方案：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/scope_upgrade_execution_20261011T081201Z/plans/paper_4e9774f4128551d3.md`。独立验证进程会复用有效结果、补差集并追加逐目标覆盖。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`17930d32440c0ab8af52a839434aa59b0735991207de955a7056f90d1a4f3a1b`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_03/reports/paper_4e9774f4128551d3/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_03/reports/paper_4e9774f4128551d3/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_03/reports/paper_4e9774f4128551d3/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。


### 自主科研设计交叉复审补充

复审时间：2026-10-12T01:10:46.921988+00:00。本次仅修订任务合同或来源映射，不新增量化计算通过结论。已保留此前全部计算记录。父复审记录：[paper_4e9774f4128551d3](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/parent_review/paper_4e9774f4128551d3_decision.json)；变更文件：`agent_input/submission_guide.md`。

<!-- autonomy_repair_verification_new_group_06_20261012 -->

## 2026-10-12 当前自主科研设计参考验证 — group 06

科学状态：**PASS**；执行状态：**NO_ACTIVE_NEW_APPLICATION**。当前题面 SHA256：b1f5e062b145bb38ef24289e969219885caf48f077a0a5def19d9957a3503b4b；冻结设计映射 SHA256：1e538da3d012253a47f7cc7c22f4729933eaa904834e6aea1c8b951d15fc75e4。

本轮实际重读当前正文/SI、父审/target_map/verification_delta和历史原生日志、查询历史job状态；复用有效计算，仅补当前缺口。旧整体PASS不自动覆盖当前新增目标。设计文件和原始历史证据保持冻结，发布由父进程另判。

| 当前目标 | 科学状态 | 来源值 | 实算/分析 | 差值 |
|---|---|---|---|---|
| kp_thermodynamics | PASS | 2.3171919 | 2.641225026896122 | 0.32403312689612207 |
| kp_condition_dependence | PASS | {"reversible":"trans","single_pass_trans_cis":1.1} | {"endpoint_equilibrium_trans_cis_298K":86.30409040420615,"fixed_G_finite_time_ratios":[0.1,1.1,10]} | null |
| kp_recycling | PASS | {"three_round_cis_yield":0.7,"single_pass_trans_cis":1.1} | {"ideal_cumulative_cis":0.8562790195443256,"remaining_trans":0.14372098045567436,"recovery_1_09_08_cis":[0.8562790195443256,0.725860058309038,0.6074851527912752]} | {"ideal_minus_experiment_percentage_points":15.627901954432566} |
| c_stereochemistry | PASS | {"isolated_cis_three_rounds":0.7} | {"initial_50_g":0.203,"isolated_S20_g":0.143,"mass_ratio_same_formula":0.7044334975369457} | null |

逐项定义、源页码/图表、原生日志/哈希、频率/连接/状态/计量有效性及当前评分共享上限见 [coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/autonomy_repair_20261011_verification_new_group_06/coverage.json)；完整实算审查见 [verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/autonomy_repair_20261011_verification_new_group_06/verification_report.md)。

- kp_thermodynamics：53atom C20H30O3,0/singlet;153positive modes each; C6R→S,remote11S/13R/30S retained; own matchedGcorr.
- kp_condition_dependence：Independent matrix-exponential calculation conserves population/detailed balance while changing forward branching; endpointΔG cannot determine single-pass selectivity.
- kp_recycling：cis+remainingtrans+loss=1 eachround. Ideal85.63% is conditional ceiling, not prediction of70%. No fitted recovery.
- c_stereochemistry：0.143g/0.203g=.7044335 supports rounded70%; unknown losses remain unidentified. No double counting endpoint/condition evidence.

保留限制和未完成项：

- Low-level sourceDZ column equals E+Gcorr, not SCFE; do not double-add heat terms.
- Absolute sourceTZ offsets~0.014Eh remain; endpoint difference retains small residual.
- Main THF/MeOH1:1 vsSI10:1 unresolved; pureMeOH endpoint model not kinetic solvent calibration.

[资源/原生步骤与时间](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/autonomy_repair_20261011_verification_new_group_06/resource_accounting.json)；[新作业记录](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/autonomy_repair_20261011_verification_new_group_06/jobs.json)；[精确后继](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_4e9774f4128551d3/autonomy_repair_20261011_verification_new_group_06/successor.json)；[父进程待裁定问题](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/scope_upgrade_execution_20261011T081201Z/verification_new/group_06/repair_proposals.md)。

仍在运行/排队的长作业仅记WAITING_HPC，不记验证完成。平台SUCCEEDED、作者坐标或程序正常退出不能替代科学验证。未委派、未重启或周期resume Codex，未修改题目、评分窗口或全局collection_manifest。
