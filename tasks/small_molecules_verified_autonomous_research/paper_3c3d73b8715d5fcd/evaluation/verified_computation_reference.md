## 2026-10-20 专家第一轮评分规则同步

endo/exo 差异项改为定性排序，仍为 10 分；不再强制命中 7.5±2.0 kcal/mol。

本节记录评分合同变更；下方原日期的计算结果、旧规则和验收范围按历史保留，不作为额外的现行评分要求。当前规则以 scoring_rules.json、reference_key_points.json 和 reference_conclusions.json 为准。本轮没有新增量子化学作业。

> 2026-10-17副本维护：历史verified_tasks位置按原日期保留；当前副本位于small_molecules_verified_autonomous_research。仅修复相对链接，未改变计算结论、QRC证据范围或科学规则。

> 2026-10-10 用户纠正后的现行评分口径：本包采用 scientific_results.v1，以论文在当前任务范围内的中间关键点和最终结论作为目标；自主性指方法与探索过程选择，不指用相反或未定结论替代必评结果。原验证数据、数值容差、科学权重和有限模型范围保留。下方 open_research/替代结论得分说法仅为旧版本历史，不再生效。本包继续留在 verified_tasks；见[本次修正](../../../verified_tasks/PAPER_OUTCOME_ALIGNMENT_20261010.md)。

> 2026-10-10 任务整理状态：本包已补齐明确的最终参考结论并同步评分规则，已修复公开提交的证据保存路径，并通过科学规则正反例回放和 final 入口准备。以下历史记录中“结论登记、证据路径、评分回放待处理”的维护状态由本条更新；科学数值、原始计算流程和证据索引完整保留。验证范围仍以本文逐节点说明为准，不等于完整盲 AR 运行。本包继续留在 verified_tasks 等待用户确认迁移。详见[本次整理与验收](../../../verified_tasks/RELEASE_COMPLETION_20261010.md)。

# 已验证计算参考：paper_3c3d73b8715d5fcd / autonomous_research

> 当前状态更新时间：2026-10-09；HPC/已完成日志快照：2026-10-09T12:52:16.493331+00:00。本节取代此前旧资格判断。私有验证档案，不导出给被评agent。

**当前有限机制/能量比较有真实计算支持，主要结果与论文小幅相符；保留替代连接证据的准确范围。**

科学参考状态：`reference_supported_with_pathway_boundaries`。AR/PR共享相同科学结果证据；这不是盲AR过程认证或正式发布批准。

## 已完成的验证计算与方法

73 份原生日志：17 个核心物种的优化/频率及溶剂、高级别单点，10 条 IRC 与12个端点优化/频率（含TS3双向位移后优化）。组装 E_high+Gcorr_low+(E_solv_low−E_gas_low)，显式处理 CO 和标准态。

## 与论文对应量的比较

| 物理量 | 计算 / kcal mol⁻¹ | 论文 | 差值 |
| --- | --- | --- | --- |
| 总活化自由能 | 22.739174 | 22.8 | -0.060826 |
| exo−endo | 7.558220 | 7.5 | +0.058220 |
| [2+2]局部势垒 | 17.053933 | 17.1 | -0.046067 |
| β-H局部势垒 | 6.020002 | 6.0 | +0.020002 |
| 还原消除局部势垒 | 8.915452 | 8.9 | +0.015452 |

**当前有据结论：**参考支持 endo-OCM 起始和两类产物竞争，总势垒22.739174、exo−endo7.558220 kcal/mol。TS3采用QRC连接替代，不能改写成原生IRC成功；不认证唯一全局机制或实验产率。

## 当前关键点与最终结论的证据覆盖

| 当前节点 | 类型 | 已完成证据与边界 |
| --- | --- | --- |
| chemical_continuity | process | 六个单负模TS、实际路径/端点及原子/配平对应；TS3为已接受QRC，exo开放端点与endo INT1构象不同。 |
| cycloisomerization | result | 总势垒以INT11所代表的物理参考定义，22.739174对22.8；不能改用局部INT1势垒。 |
| competing_product | result | 真实[2+2]连通和17.053933局部势垒；TS5+CO−TS2=0.132922 kcal/mol支持限定模型的竞争。 |
| pathway_discrimination | result | G_exo−G_endo=7.558220，与主文Figure1的7.5相符。 |
| answer | final | 参考支持 endo-OCM 起始和两类产物竞争，总势垒22.739174、exo−endo7.558220 kcal/mol。TS3采用QRC连接替代，不能改写成原生IRC成功；不认证唯一全局机制或实验产率。 |

## 尚缺项与作业状态

当前有限参考科学目标没有已确认必须新增的量子计算；本次没有为本篇新提交验证作业。与全论文、所有替代方法或完整自主搜索不同，不作额外外推。

## 直接证据与本次同步

- [COMPUTED_HIGH_LEVEL_PROFILE.json](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/resumption_20260925/COMPUTED_HIGH_LEVEL_PROFILE.json)
- [FINAL_REFERENCE_AUDIT.json](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json)
- [论文依据 main](../../../../papers/paper_3c3d73b8715d5fcd/documents/main.pdf)：PDF pp.2–3 Scheme 3/Figure 1; Computational Methods section
- [论文依据 si](../../../../papers/paper_3c3d73b8715d5fcd/documents/supplementary_001.pdf)：S34–43 energetic discussion/Table S2; S44–46 catalyst/substrate; S48 product 4D; S51 product 3D
- [原生日志复核](../../../verified_tasks/maintenance_tools/post_upgrade_review_20261008/native_recheck.json)；[独立量值重提取](../../../verified_tasks/maintenance_tools/post_upgrade_review_20261008/recomputed_quantities.json)
- [保留的包维护记录](task_provenance/maintenance_audit.md)；[七篇状态及本次同步总结](../../../verified_tasks/VERIFICATION_REFERENCE_UPDATE_20261009.md)

本次更新只同步已完成事实、状态及维护引用。既定科学目标、权重和数值容差保持；此前最终结论登记、证据目录索引、正式评分回放和部署读取隔离问题仍需按待确认方案处理。

---

## 历史计算档案与原始输入输出索引

> 以下记录按当时版本保留，旧节点名/题面范围/“当前”状态以本页上方最新解释为准。原始数值和输入输出引用保留。

# 已验证计算参考：paper_3c3d73b8715d5fcd / autonomous_research

> 2026-09-29 修后同步：任务修复和当前评分映射见第 3、6 节；全部仍在 verified_tasks，未获迁移确认。
核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/autonomous_research/paper_3c3d73b8715d5fcd`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 2。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

低层 Gaussian 16 C.01 PW6B95D3，非 Rh 原子 6-311G(d,p)、Rh def2-TZVP/ECP；气相 Opt/Freq，随后同几何 SMD 1,4-dioxane 单点及 ORCA 6.1.1 ωB97M-V/def2-QZVP 高层单点。17 个物种，全部中性单重态；低层热化学 298 K 解析转换为任务 298.15 K；CO 0.0085 M，其余 1 M。原文正文物理第 3 页给出 INT11 起算 22.8、exo−endo 7.5 kcal/mol，当前各容差 ±2.0。

论文来源：[正文](../../../../papers/paper_3c3d73b8715d5fcd/documents/main.pdf)；[SI](../../../../papers/paper_3c3d73b8715d5fcd/documents/supplementary_001.pdf)。上述页码为 PDF 物理页码。

完整 substrate 1D(24 atom)/Rh dimer(12 atom) 是当前给定反应物，合法；另有未在 task 中说明的 README_coordinates.xyz(14 atom)。其第 1 个 C 坐标来自 SI INT1（物理第 46 页），其余 13 行来自 TS1endo 尾部（第 47 页），是混拼的作者答案结构片段，不是第二个完整底物。修前两模式曾公开此文件；本轮已原字节移入 [私有作废片段](author_results/invalid_mixed_coordinate_fragment.xyz)，并注明不用，不再导出给 agent。

## 2. 有效计算链、结果与推导

采用 Gsol=Ehigh+Gcorr_low+(ESMD_low−Egas_low)+ΔG_RRHO(298→298.15)+RT ln(CRT/p0)。统一参照 0.5 Rh_dimer+1D，对 28 原子缺 CO 物种补上游离 CO。复算总体势垒 TS1endo−INT11=22.739173663，TS1exo−TS1endo=7.558219734 kcal/mol。六 TS、十二全实频连接端点：TS1endo: INT1↔INT2；TS1exo: 开链配位构象↔exo 环化物；TS2: INT2↔有机片段为 4D 的 Rh 配合物；TS3: INT2↔INT3+CO；TS4: INT3↔INT4；TS5: INT4↔INT5，有机片段为 3D。五个 TS 的十方向有限 IRC（各 50 点）后继续端点优化；TS3 原生 IRC 未成功，采用负模双向位移+优化的 QRC 替代。exo 开链端点不等同 endo INT1；endo/exo 标签由来源 SI 几何支持，不伪称无作者信息的立体搜索。

| 物种 | E gas low / Eh | E SMD low / Eh | E high / Eh | G sol 298.15 / Eh |
| --- | --- | --- | --- | --- |
| CO | -113.4782617080 | -113.4732508540 | -113.3442157619 | -113.3546669614 |
| Rh_dimer | -1596.6151683100 | -1596.6154061800 | -1595.0911225946 | -1595.0964548330 |
| 1D | -427.1708928980 | -427.1755269150 | -426.5025342858 | -426.3339115642 |
| INT1 | -1225.4782834400 | -1225.4883740900 | -1224.0429158270 | -1223.8688311695 |
| INT2 | -1225.5083292200 | -1225.5197455400 | -1224.0720882860 | -1223.8929741951 |
| INT3 | -1111.9940101400 | -1112.0066655500 | -1110.6952544829 | -1110.5229185856 |
| INT4 | -1111.9917268700 | -1112.0046621300 | -1110.6942238895 | -1110.5251259138 |
| INT5 | -1111.9850326600 | -1111.9973724500 | -1110.6888695510 | -1110.5207391902 |
| INT11 | -1225.4933015400 | -1225.5033157200 | -1224.0594375600 | -1223.8845089097 |
| TS1endo | -1225.4615898300 | -1225.4715672500 | -1224.0236209016 | -1223.8482717298 |
| TS1exo | -1225.4462237000 | -1225.4576150000 | -1224.0100849916 | -1223.8362269400 |
| TS2 | -1225.4775791000 | -1225.4871186300 | -1224.0422070047 | -1223.8657970227 |
| TS3 | -1225.4753230500 | -1225.4867684300 | -1224.0402064462 | -1223.8663278453 |
| TS4 | -1111.9781084500 | -1111.9913368900 | -1110.6804692296 | -1110.5133251016 |
| TS5 | -1111.9740265000 | -1111.9864250800 | -1110.6769296692 | -1110.5109182362 |
| 3D | -427.2191422080 | -427.2248196490 | -426.5526413236 | -426.3784509496 |
| 4D | -427.2147788250 | -427.2210275580 | -426.5484325669 | -426.3738558035 |

| 物种（CO已配平） | 共同参照相对G / kcal mol⁻¹ |
| --- | --- |
| INT1 | 8.350778 |
| INT2 | -6.799200 |
| INT3 | 2.857323 |
| INT4 | 1.472203 |
| INT5 | 4.224914 |
| INT11 | -1.487153 |
| TS1endo | 21.252021 |
| TS1exo | 28.810241 |
| TS2 | 10.254734 |
| TS3 | 9.921637 |
| TS4 | 8.877325 |
| TS5 | 10.387656 |

## 3. 修后当前必评关键点与结论覆盖（2026-09-29）

本表对齐本包当前五个 evaluator JSON。历史真实计算链及数值仍见第 2、4、5 节；reference 不新增评分门槛。

| 当前 ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| kp_process_stationary_points / process | The investigation validates minima with no imaginary frequencies and transition states with one imaginary frequency plus a connectivity test, and retains candidate identity through energy assembly. | 17 个低层驻点、6 个一虚频 TS、12 个正频端点，10 个有限 IRC 加 TS3 QRC；连接逐项见上。 | rule_process_validation |
| kp_process_energy_assembly / process | Relative Gibbs energies consistently combine electronic, thermal and solvation contributions at the stated temperature and solvent standard states. | 34 组 low→solvent/high 几何配对逐原子一致；统一浓度、温度、CO 配平的复算剖面。 | rule_process_assembly |
| kp_result_activation / result | The cycloisomerization profile has an overall activation free energy of 22.8 kcal/mol from INT11. | TS1endo−INT11=22.739173663 kcal/mol，22.8±2.0。 | rule_activation |
| kp_result_endo_exo / result | The endo-OCM transition state is favored over exo-OCM by 7.5 kcal/mol. | TS1exo−TS1endo=7.558219734 kcal/mol，7.5±2.0。 | rule_endo_exo |

| 结论 ID / 角色 | 当前科学主张 | 支持关键点及边界 |
| --- | --- | --- |
| conclusion_mechanism / final | Within the stated model and computational boundary, the validated profile supports endo-OCM as the preferred initiating OCM and supports a cycloisomerization path whose overall barrier is about 22.8 kcal/mol. | kp_process_stationary_points, kp_result_activation, kp_result_endo_exo, kp_process_energy_assembly。六 TS、十二连接端点和势垒有作者路线证据；TS3 是 QRC 替代有限 IRC，exo 开链端点不等同 endo INT1。替代协议应单独判断可比性，未认证自主盲搜索。 |

修前→修后：关键点 4→4；结论记录 2→1。现有结论为科学成果，不另给普通免责声明计分。真实计算支持范围不因本次改关联而扩大。

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CO_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_CO_SI_PW6B95D3_mixed_optfreq_20260915_20260915T115903Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_CO_SI_PW6B95D3_mixed_optfreq_20260915_20260915T115903Z/stdout.log) | [0, 1] | -113.4782617080 | -113.4922300000 | 1 / 0 / 2253.3736 | native normal |
| 2 | CO_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_CO_validated_minimum_SMD_dioxane_SP_20260915_20260916T043451Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_CO_validated_minimum_SMD_dioxane_SP_20260915_20260916T043451Z/stdout.log) | [0, 1] | -113.4732508540 | — | — | native normal |
| 3 | CO_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_CO_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_CO_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -113.3442157619 | — | — | native normal |
| 4 | Rh_dimer_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_Rh_dimer_SI_PW6B95D3_mixed_optfreq_20260915_20260915T115909Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_Rh_dimer_SI_PW6B95D3_mixed_optfreq_20260915_20260915T115909Z/stdout.log) | [0, 1] | -1596.6151683100 | -1596.6232500000 | 30 / 0 / 30.6071 | native normal |
| 5 | Rh_dimer_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_Rh_dimer_validated_minimum_SMD_dioxane_SP_20260915_20260916T043459Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_Rh_dimer_validated_minimum_SMD_dioxane_SP_20260915_20260916T043459Z/stdout.log) | [0, 1] | -1596.6154061800 | — | — | native normal |
| 6 | Rh_dimer_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_Rh_dimer_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_Rh_dimer_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1595.0911225946 | — | — | native normal |
| 7 | 1D_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_1D_SI_PW6B95D3_mixed_optfreq_20260915_20260915T115916Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_1D_SI_PW6B95D3_mixed_optfreq_20260915_20260915T115916Z/stdout.log) | [0, 1] | -427.1708928980 | -427.0006290000 | 66 / 0 / 43.485 | native normal |
| 8 | 1D_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_1D_validated_minimum_SMD_dioxane_SP_20260915_20260916T043507Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_1D_validated_minimum_SMD_dioxane_SP_20260915_20260916T043507Z/stdout.log) | [0, 1] | -427.1755269150 | — | — | native normal |
| 9 | 1D_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_1D_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_1D_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -426.5025342858 | — | — | native normal |
| 10 | INT1_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT1_SI_PW6B95D3_mixed_optfreq_20260915_20260915T120925Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT1_SI_PW6B95D3_mixed_optfreq_20260915_20260915T120925Z/stdout.log) | [0, 1] | -1225.4782834400 | -1225.2970920000 | 84 / 0 / 30.4477 | native normal |
| 11 | INT1_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT1_validated_minimum_SMD_dioxane_SP_20260915_20260916T043515Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT1_validated_minimum_SMD_dioxane_SP_20260915_20260916T043515Z/stdout.log) | [0, 1] | -1225.4883740900 | — | — | native normal |
| 12 | INT1_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT1_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT1_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1224.0429158270 | — | — | native normal |
| 13 | INT2_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT2_SI_PW6B95D3_mixed_optfreq_20260915_20260915T120932Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT2_SI_PW6B95D3_mixed_optfreq_20260915_20260915T120932Z/stdout.log) | [0, 1] | -1225.5083292200 | -1225.3207850000 | 84 / 0 / 39.685 | native normal |
| 14 | INT2_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT2_validated_minimum_SMD_dioxane_SP_20260915_20260916T043543Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT2_validated_minimum_SMD_dioxane_SP_20260915_20260916T043543Z/stdout.log) | [0, 1] | -1225.5197455400 | — | — | native normal |
| 15 | INT2_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT2_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT2_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1224.0720882860 | — | — | native normal |
| 16 | INT3_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT3_SI_PW6B95D3_mixed_optfreq_20260915_20260915T120939Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT3_SI_PW6B95D3_mixed_optfreq_20260915_20260915T120939Z/stdout.log) | [0, 1] | -1111.9940101400 | -1111.8120080000 | 78 / 0 / 40.6687 | native normal |
| 17 | INT3_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT3_validated_minimum_SMD_dioxane_SP_20260915_20260916T043522Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT3_validated_minimum_SMD_dioxane_SP_20260915_20260916T043522Z/stdout.log) | [0, 1] | -1112.0066655500 | — | — | native normal |
| 18 | INT3_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT3_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT3_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1110.6952544829 | — | — | native normal |
| 19 | INT4_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT4_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043309Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT4_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043309Z/stdout.log) | [0, 1] | -1111.9917268700 | -1111.8126830000 | 78 / 0 / 65.5877 | native normal |
| 20 | INT4_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT4_validated_stationary_SMD_dioxane_SP_20260916_20260916T105418Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT4_validated_stationary_SMD_dioxane_SP_20260916_20260916T105418Z/stdout.log) | [0, 1] | -1112.0046621300 | — | — | native normal |
| 21 | INT4_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT4_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT4_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1110.6942238895 | — | — | native normal |
| 22 | INT5_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT5_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043316Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT5_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043316Z/stdout.log) | [0, 1] | -1111.9850326600 | -1111.8075500000 | 78 / 0 / 30.1744 | native normal |
| 23 | INT5_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT5_validated_stationary_SMD_dioxane_SP_20260916_20260916T105427Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT5_validated_stationary_SMD_dioxane_SP_20260916_20260916T105427Z/stdout.log) | [0, 1] | -1111.9973724500 | — | — | native normal |
| 24 | INT5_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT5_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT5_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1110.6888695510 | — | — | native normal |
| 25 | INT11_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT11_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043323Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT11_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043323Z/stdout.log) | [0, 1] | -1225.4933015400 | -1225.3113430000 | 84 / 0 / 46.7319 | native normal |
| 26 | INT11_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT11_validated_stationary_SMD_dioxane_SP_20260916_20260916T105435Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT11_validated_stationary_SMD_dioxane_SP_20260916_20260916T105435Z/stdout.log) | [0, 1] | -1225.5033157200 | — | — | native normal |
| 27 | INT11_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT11_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_INT11_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1224.0594375600 | — | — | native normal |
| 28 | TS1endo_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043331Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043331Z/stdout.log) | [0, 1] | -1225.4615898300 | -1225.2792490000 | 84 / 1 / -344.5198 | native normal |
| 29 | TS1endo_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_stationary_SMD_dioxane_SP_20260916_20260916T105443Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_stationary_SMD_dioxane_SP_20260916_20260916T105443Z/stdout.log) | [0, 1] | -1225.4715672500 | — | — | native normal |
| 30 | TS1endo_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1224.0236209016 | — | — | native normal |
| 31 | TS1exo_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043339Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043339Z/stdout.log) | [0, 1] | -1225.4462237000 | -1225.2639600000 | 84 / 1 / -255.7719 | native normal |
| 32 | TS1exo_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_stationary_SMD_dioxane_SP_20260916_20260916T105450Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_stationary_SMD_dioxane_SP_20260916_20260916T105450Z/stdout.log) | [0, 1] | -1225.4576150000 | — | — | native normal |
| 33 | TS1exo_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1224.0100849916 | — | — | native normal |
| 34 | TS2_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043347Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043347Z/stdout.log) | [0, 1] | -1225.4775791000 | -1225.2946150000 | 84 / 1 / -247.2291 | native normal |
| 35 | TS2_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_stationary_SMD_dioxane_SP_20260916_20260916T105458Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_stationary_SMD_dioxane_SP_20260916_20260916T105458Z/stdout.log) | [0, 1] | -1225.4871186300 | — | — | native normal |
| 36 | TS2_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1224.0422070047 | — | — | native normal |
| 37 | TS3_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043355Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043355Z/stdout.log) | [0, 1] | -1225.4753230500 | -1225.2929840000 | 84 / 1 / -56.5575 | native normal |
| 38 | TS3_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_validated_stationary_SMD_dioxane_SP_20260916_20260916T105505Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_validated_stationary_SMD_dioxane_SP_20260916_20260916T105505Z/stdout.log) | [0, 1] | -1225.4867684300 | — | — | native normal |
| 39 | TS3_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1224.0402064462 | — | — | native normal |
| 40 | TS4_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043402Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043402Z/stdout.log) | [0, 1] | -1111.9781084500 | -1111.8007250000 | 78 / 1 / -751.1947 | native normal |
| 41 | TS4_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_stationary_SMD_dioxane_SP_20260916_20260916T105513Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_stationary_SMD_dioxane_SP_20260916_20260916T105513Z/stdout.log) | [0, 1] | -1111.9913368900 | — | — | native normal |
| 42 | TS4_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1110.6804692296 | — | — | native normal |
| 43 | TS5_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043410Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043410Z/stdout.log) | [0, 1] | -1111.9740265000 | -1111.7986050000 | 78 / 1 / -707.0583 | native normal |
| 44 | TS5_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_stationary_SMD_dioxane_SP_20260916_20260916T105520Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_stationary_SMD_dioxane_SP_20260916_20260916T105520Z/stdout.log) | [0, 1] | -1111.9864250800 | — | — | native normal |
| 45 | TS5_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -1110.6769296692 | — | — | native normal |
| 46 | 3D_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_3D_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043418Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_3D_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043418Z/stdout.log) | [0, 1] | -427.2191422080 | -427.0422690000 | 66 / 0 / 38.3163 | native normal |
| 47 | 3D_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_3D_validated_stationary_SMD_dioxane_SP_20260916_20260916T105526Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_3D_validated_stationary_SMD_dioxane_SP_20260916_20260916T105526Z/stdout.log) | [0, 1] | -427.2248196490 | — | — | native normal |
| 48 | 3D_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_3D_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_3D_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -426.5526413236 | — | — | native normal |
| 49 | 4D_low | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_4D_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043426Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_4D_SI_PW6B95D3_mixed_optfreq_20260915_20260916T043426Z/stdout.log) | [0, 1] | -427.2147788250 | -427.0369490000 | 66 / 0 / 52.4274 | native normal |
| 50 | 4D_solvent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_4D_validated_stationary_SMD_dioxane_SP_20260916_20260916T105533Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_4D_validated_stationary_SMD_dioxane_SP_20260916_20260916T105533Z/stdout.log) | [0, 1] | -427.2210275580 | — | — | native normal |
| 51 | 4D_high | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_4D_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/input.inp) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_4D_validated_geometry_wB97MV_def2QZVP_ORCA611_SP_mpi_v5_20260925/stdout.log) | 0 / 1（ORCA input） | -426.5484325669 | — | — | native normal |
| 52 | ENDPOINT_REVIEW/TS1endo/endpoints/forward | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T164721Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T164721Z/stdout.log) | [0, 1] | -1225.4782896000 | -1225.2970480000 | 84 / 0 / 30.8376 | native normal |
| 53 | ENDPOINT_REVIEW/TS1endo/endpoints/forward/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_forward_20260925_20260925T154005Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_forward_20260925_20260925T154005Z/stdout.log) | [0, 1] | -1225.4776253200 | — | — | native normal |
| 54 | ENDPOINT_REVIEW/TS1endo/endpoints/reverse | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T164738Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T164738Z/stdout.log) | [0, 1] | -1225.5083372800 | -1225.3207760000 | 84 / 0 / 39.7585 | native normal |
| 55 | ENDPOINT_REVIEW/TS1endo/endpoints/reverse/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_reverse_20260925_20260925T152749Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1endo_validated_saddle_IRC_reverse_20260925_20260925T152749Z/stdout.log) | [0, 1] | -1225.4888651800 | — | — | native normal |
| 56 | ENDPOINT_REVIEW/TS1exo/endpoints/forward | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T164755Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T164755Z/stdout.log) | [0, 1] | -1225.4886539800 | -1225.3031930000 | 84 / 0 / 39.9552 | native normal |
| 57 | ENDPOINT_REVIEW/TS1exo/endpoints/forward/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_forward_20260925_20260925T152808Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_forward_20260925_20260925T152808Z/stdout.log) | [0, 1] | -1225.4673074800 | — | — | native normal |
| 58 | ENDPOINT_REVIEW/TS1exo/endpoints/reverse | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T165855Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T165855Z/stdout.log) | [0, 1] | -1225.4683182900 | -1225.2868860000 | 84 / 0 / 45.5928 | native normal |
| 59 | ENDPOINT_REVIEW/TS1exo/endpoints/reverse/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_reverse_20260925_20260925T152826Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS1exo_validated_saddle_IRC_reverse_20260925_20260925T152826Z/stdout.log) | [0, 1] | -1225.4603194700 | — | — | native normal |
| 60 | ENDPOINT_REVIEW/TS2/endpoints/forward | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T165914Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T165914Z/stdout.log) | [0, 1] | -1225.5005091000 | -1225.3187130000 | 84 / 0 / 27.4068 | native normal |
| 61 | ENDPOINT_REVIEW/TS2/endpoints/forward/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_forward_20260925_20260925T152845Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_forward_20260925_20260925T152845Z/stdout.log) | [0, 1] | -1225.4982244000 | — | — | native normal |
| 62 | ENDPOINT_REVIEW/TS2/endpoints/reverse | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T165934Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T165934Z/stdout.log) | [0, 1] | -1225.5083280900 | -1225.3208400000 | 84 / 0 / 37.5853 | native normal |
| 63 | ENDPOINT_REVIEW/TS2/endpoints/reverse/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_reverse_20260925_20260925T154022Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS2_validated_saddle_IRC_reverse_20260925_20260925T154022Z/stdout.log) | [0, 1] | -1225.4844738000 | — | — | native normal |
| 64 | ENDPOINT_REVIEW/TS4/endpoints/forward | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T171015Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T171015Z/stdout.log) | [0, 1] | -1111.9917357500 | -1111.8131880000 | 78 / 0 / 61.7362 | native normal |
| 65 | ENDPOINT_REVIEW/TS4/endpoints/forward/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_forward_20260925_20260925T154113Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_forward_20260925_20260925T154113Z/stdout.log) | [0, 1] | -1111.9908267300 | — | — | native normal |
| 66 | ENDPOINT_REVIEW/TS4/endpoints/reverse | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T171032Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T171032Z/stdout.log) | [0, 1] | -1111.9940087900 | -1111.8119330000 | 78 / 0 / 40.5874 | native normal |
| 67 | ENDPOINT_REVIEW/TS4/endpoints/reverse/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_reverse_20260925_20260925T154130Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS4_validated_saddle_IRC_reverse_20260925_20260925T154130Z/stdout.log) | [0, 1] | -1111.9857351800 | — | — | native normal |
| 68 | ENDPOINT_REVIEW/TS5/endpoints/forward | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T171048Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_forward_accepted_endpoint_optfreq_20260925_20260925T171048Z/stdout.log) | [0, 1] | -1111.9917213700 | -1111.8127670000 | 78 / 0 / 64.3107 | native normal |
| 69 | ENDPOINT_REVIEW/TS5/endpoints/forward/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_forward_20260925_20260925T154147Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_forward_20260925_20260925T154147Z/stdout.log) | [0, 1] | -1111.9840937200 | — | — | native normal |
| 70 | ENDPOINT_REVIEW/TS5/endpoints/reverse | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T171105Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_reverse_accepted_endpoint_optfreq_20260925_20260925T171105Z/stdout.log) | [0, 1] | -1111.9850405600 | -1111.8075390000 | 78 / 0 / 29.9411 | native normal |
| 71 | ENDPOINT_REVIEW/TS5/endpoints/reverse/IRC_parent | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_reverse_20260925_20260925T160321Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS5_validated_saddle_IRC_reverse_20260925_20260925T160321Z/stdout.log) | [0, 1] | -1111.9828267900 | — | — | native normal |
| 72 | TS3_QRC_COMPLETED/plus | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_computed_negative_mode_QRC_plus_tight_optfreq_20260926_20260926T025643Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_computed_negative_mode_QRC_plus_tight_optfreq_20260926_20260926T025643Z/stdout.log) | [0, 1] | -1225.5083205300 | -1225.3208780000 | 84 / 0 / 38.2571 | native normal |
| 73 | TS3_QRC_COMPLETED/minus | [输入](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_computed_negative_mode_QRC_minus_tight_optfreq_20260926_20260926T025701Z/input.com) / [原始输出](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/qzcli_hpc/author_TS3_computed_negative_mode_QRC_minus_tight_optfreq_20260926_20260926T025701Z/stdout.log) | [0, 1] | -1225.4779664700 | -1225.2974350000 | 84 / 0 / 16.2738 | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`；`Program Version 6.1.1  -  RELEASE   -`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1, 7, 46, 49 | `#p PW6B95D3/6-311G(d,p) Opt=(CalcFC,MaxCyc=300,MaxStep=10) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 2, 8 | `#p PW6B95D3/6-311G(d,p) SP SCRF=(SMD,Solvent=1,4-Dioxane) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51 | `! wB97M-V def2-QZVP TightSCF NoAutoStart` |
| 4, 10, 13, 16, 19, 22, 25 | `#p PW6B95D3/GenECP Opt=(CalcFC,MaxCyc=300,MaxStep=10) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 5, 11, 14, 17 | `#p PW6B95D3/GenECP SP SCRF=(SMD,Solvent=1,4-Dioxane) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine` |
| 20, 23, 26, 29, 32, 35, 38, 41, 44 | `#p PW6B95D3/GenECP SP SCRF=(SMD,Solvent=1,4-Dioxane) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 28, 31, 34, 37, 40, 43 | `#p PW6B95D3/GenECP Opt=(TS,CalcFC,NoEigenTest,MaxCyc=300,MaxStep=10) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 47, 50 | `#p PW6B95D3/6-311G(d,p) SP SCRF=(SMD,Solvent=1,4-Dioxane) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 52, 54, 56, 58, 60, 62, 64, 66, 68, 70 | `#p PW6B95D3/GenECP Opt=(CalcFC,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 53, 57, 61, 65, 69 | `#p PW6B95D3/GenECP IRC=(CalcFC,Forward,MaxPoints=50,StepSize=5,MaxCycle=100) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 55, 59, 63, 67, 71 | `#p PW6B95D3/GenECP IRC=(CalcFC,Reverse,MaxPoints=50,StepSize=5,MaxCycle=100) NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |
| 72, 73 | `#p PW6B95D3/GenECP Opt=(Tight,CalcFC,MaxCyc=300,MaxStep=10) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine Temperature=298` |

## 5. 模型、连接与后处理原始出处

- [provenance/resumption_20260925/COMPUTED_HIGH_LEVEL_PROFILE.json](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/resumption_20260925/COMPUTED_HIGH_LEVEL_PROFILE.json)
- [provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json)
- [provenance/resumption_20260926/ENDPOINT_REVIEW/INDEPENDENT_RESULTS.json](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/resumption_20260926/ENDPOINT_REVIEW/INDEPENDENT_RESULTS.json)
- [provenance/resumption_20260926/TS3_QRC_COMPLETED/INDEPENDENT_RESULTS.json](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/provenance/resumption_20260926/TS3_QRC_COMPLETED/INDEPENDENT_RESULTS.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../docs/verification/group_2/paper_3c3d73b8715d5fcd/report/results.json)

## 6. 修后包检查与未认证事项（2026-09-29）

当前策略为 `dual_axis_100.scientific_results.v1`；真实历史 report 对本包的实际输出检查：**通过**。本包已执行 12 个提交样例，每个分别经过 JSON Schema 和真实 validate_output_contract；合成正反例只测试格式，未加入本计算档案的科学证据。

六 TS、十二连接端点和势垒有作者路线证据；TS3 是 QRC 替代有限 IRC，exo 开链端点不等同 endo INT1。替代协议应单独判断可比性，未认证自主盲搜索。

[逐包维护记录](task_provenance/maintenance_audit.md)及[集中报告第30节](../../../verified_tasks/MAINTENANCE_REPORT.md)记录实际修改、检查与未闭合项。普通免责声明已取消必填及独立计分，身份/态/收敛/频率/路径/参考态和真实失败证据保留。

本次没有新电子结构计算、HPC 操作、完整 LLM 评分或 AR 盲测；没有迁移 final/hold。文件导出检查只覆盖 agent_input 物化，不能替代部署侧父目录、容器挂载和网络隔离。完整原始证据直接链接在第 4、5 节，不依赖 task_provenance 的长期存在。


<!-- phase2-verification-group05-20261010T231612Z -->

## 2026-10-11 第二阶段第5组独立参考计算验证

检查时间：2026-10-11T06:17:42.688533+00:00。当前运行状态：**PASS**；已完成证据的科学判定：**PASS**。

当前有限参考的全部必需结果已恢复。17个物种的高低层能量重新组装，6个鞍点和两条产物通道的原生连接复核通过。

被验证科学任务的初始包SHA256：`e7093dcb8c6b0be7a4517f8f29ca8fade672eed09272fd906280ba87060062ca`。本轮只追加证据并重建manifest；任务/evaluator/阈值保持不变。更新后的包hash由本组manifest_changes.json记录，避免把含自身hash的文档递归纳入hash。

完整逐目标报告：[verification_report.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/verification_report.md)；覆盖表：[coverage.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/coverage.json)；作业和续接：[jobs.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/jobs.json)、[resumption.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/resumption.json)。

| 当前必需目标 | 状态 | 真实证据及缺口 |
|---|---|---|
| chemical_continuity | PASS | 重新解析6个TS振动位移、10个IRC后优化端点和2个QRC端点：endo OCM连接INT1/INT2；直接还原消除得到4D；β-H消除连接INT3/INT4；最终还原消除连接INT4/INT5并得到3D。TS3仅由双向负模位移+优化连接INT2与INT3+CO，原生IRC失败保留。 |
| cycloisomerization | PASS | 采用INT11共同参照，endo OCM为最高点。释放CO显式加入28原子物种；G=Ehigh+低层热项+低层溶剂差+温度/浓度修正，不能用INT1的局部势垒代替总体势垒。 |
| competing_product | PASS | 直接还原消除与环异构化产品通道均有实际连接。不同中间体的局部势垒单列；共同参照下TS5+CO比TS2高0.133 kcal/mol，符合两通道能量接近。 |
| pathway_discrimination | PASS | 两种OCM几何/负模不同，实际成键投影和两侧端点支持其区别。exo的开链配位构象不强行等同endo INT1。 |
| answer | PASS | 有限模型支持endo OCM及竞争的环异构化/[2+2]通道；总体势垒22.739、exo−endo7.558 kcal/mol。当前任务不要求全局机理排除或实验产率预测。 |

| 比较量 | 计算值 | 论文值 | 差值 | 单位 | 既有容差 |
|---|---|---|---|---|---|
| overall_from_INT11 | 22.73917355954875 | 22.8 | -0.060826440451251074 | kcal/mol | 2.0 |
| direct_RE_from_INT2 | 17.053933182004673 | 17.1 | -0.04606681799532808 | kcal/mol | None |
| betaH_from_INT3 | 6.020002121740156 | 6.0 | 0.020002121740155587 | kcal/mol | None |
| RE_from_INT4 | 8.915452272385092 | 8.9 | 0.015452272385092058 | kcal/mol | None |
| TS5_plusCO_minus_TS2 | 0.13292228648351845 | None | None | kcal/mol | None |
| exo_minus_endo | 7.558219733162783 | 7.5 | 0.05821973316278317 | kcal/mol | 2.0 |

`None`表示没有可用计算值/未定义通用数值窗口；不能理解为零误差或放宽容差。水合PT按已核原文舍入及物理可比性判定，不从ET借容差。

实际计算/重新分析记录：

- [independent_connectivity_replay.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/outputs/independent_connectivity_replay.json)
- [independent_energy_replay.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/outputs/independent_energy_replay.json)

逐个原生日志路径、SHA256、能量/频率/电荷自旋、提取位置及CPU/墙钟：[native_readback.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/outputs/native_readback.json)、[new_native_results.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/outputs/new_native_results.json)。源PDF/DOCX哈希及文字：[sources/index.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_2/paper_3c3d73b8715d5fcd/small_molecules_20261010T231612Z_g05/sources/index.json)。这些索引绑定真实native文件；平台SUCCEEDED和来源坐标不替代科学验证。

- 限定：作者启发的有限参考验证，不是公开输入盲发现。
- 限定：TS3原生IRC未成功；双向QRC优化端点为当前任务允许的替代连接证据，不宣称完整IRC轨迹。
- 限定：ORCA6.1.1/Gaussian16C.01替代源软件；298→298.15 K用原生熵一阶校正，误差远低于打印精度；CO浓度8.5 mM，其他物种1 M。
- 限定：本轮直接按原生日志原子顺序重算成键模式；例如TS1exo实际C2–C5变化，避免沿用历史文件未映射的原子编号。

本次是授权可读作者路线的参考计算验证，不证明盲发现。旧记录完整保留；旧局部PASS不能替代本轮扩展范围。


## 2026-10-11 自主科研设计修订后的证据适用边界

本版本已完成父进程设计复审；设计摘要SHA256：`057ad915f146fe08dd4efabe143fcef7cf83af170decbad108b5b3ee59749ec7`。本条只认证题面、输入与科学结果评分合同的一致性，不新增量化计算PASS或发布认证。历史原生日志和上文验证结论保留；能否覆盖修订后的科学结果，以逐项物理对象及范围为准。

逐篇来源及修改：[change_report](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_3c3d73b8715d5fcd/change_report.md)；当前关键点/结论对应：[target_map](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_3c3d73b8715d5fcd/target_map.json)；复用和待补差集：[verification_delta](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/20261010T231612Z/autonomy_repair_20261011/group_01/reports/paper_3c3d73b8715d5fcd/verification_delta.json)。身份纠错、必需结果或适用范围变化的部分不能由旧包整体PASS自动继承；仅路径/措辞变化且科学对象未变的证据继续有效。
