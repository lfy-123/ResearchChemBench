# 已验证计算参考：paper_1e3a1d290a02e5f0 / autonomous_research

> 2026-09-29 修后同步：任务修复和当前评分映射见第 3、6 节；全部仍在 verified_tasks，未获迁移确认。
核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/autonomous_research/paper_1e3a1d290a02e5f0`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 4。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

Gaussian 16 B3P86/6-311G(d,p)，气相。每个分子一个中性单重态及一个 +1 双重态最低点，再做 cation@neutral 和 neutral@cation 两个定几何单点，共 12 份真实日志。六个最低点均 102 原子、300 正频率。JY1/2/3 的 F 取代位分别 4′、3′/5′、3′/4′/5′；现有源输入身份正确。正文物理第 2 页 Figure 2、方法与第 3 页 Table 2；本地无 JY SI。源 G09 与本地 G16 不同，作者构象不能称全局最低。

论文来源：[正文](../../../../../papers/paper_1e3a1d290a02e5f0/documents/main.pdf)。上述页码为 PDF 物理页码。

molecules.json 唯一命名 JY1/2/3，电荷/态/元素式一致，JY3 是 3′,4′,5′ 三氟；无轨道能与 λ 答案。自由选方法且允许多种 λ 定义与隐藏四点靶存在协议歧义。

## 2. 有效计算链、结果与推导

每分子 λh=[E+(R0)−E+(R+)]+[E0(R+)−E0(R0)]；Hartree→eV 用 27.211386245988。六个 cross-SP 输入逐原子对应正确优化父几何。HOMO 从中性态最后完整 Alpha occupied 本征值、LUMO 从首个 virtual 提取。结果表中的 9 个数值分别满足原 HOMO/LUMO ±0.15 eV、λ ±0.03 eV：HOMO 逐渐降低，JY2 的 λ 最小。只证明孤立分子量，不证明器件性能。

| 分子 | HOMO / eV | LUMO / eV | λ / eV |
| --- | --- | --- | --- |
| JY1 | -5.238736080 | -1.819081171 | 0.213411283 |
| JY2 | -5.255879253 | -2.126841949 | 0.198457266 |
| JY3 | -5.292614625 | -2.139087073 | 0.211489071 |

| 分子 | E0(R0) | E+(R+) | E+(R0) | E0(R+) |
| --- | --- | --- | --- | --- |
| JY1 | -2579.8822542300 | -2579.6576548500 | -2579.6538306900 | -2579.8782356700 |
| JY2 | -2679.2826105200 | -2679.0570912400 | -2679.0534720600 | -2679.2789365300 |
| JY3 | -2778.6697651000 | -2778.4433081500 | -2778.4394660100 | -2778.6658351600 |

## 3. 修后当前必评关键点与结论覆盖（2026-09-29）

本表对齐本包当前五个 evaluator JSON。历史真实计算链及数值仍见第 2、4、5 节；reference 不新增评分门槛。

| 当前 ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| ar_process_identity / process | The investigation preserves the three supplied molecular identities as neutral singlets and validates an optimized structure for each. | 三身份、六最低点、完整正频；来源记录含端苯环F位点与图保持。 | ar_r_identity |
| ar_process_reproducibility / process | The report defines a reproducible internal λh energy cycle and records the model and convergence choices used for all molecules. | 12真实能量、六个正确几何cross-SP与四点公式，完整模型/态。 | ar_r_method |
| ar_homo / result | The source calculations report HOMO energies of −5.12, −5.17 and −5.18 eV for JY1, JY2 and JY3. | 三HOMO由最后occupied轨道提取，均在原±0.15内。 | ar_r_homo, ar_r_homo2, ar_r_homo3 |
| ar_lumo / result | The source calculations report LUMO energies of −1.88, −2.19 and −2.18 eV for JY1, JY2 and JY3. | 三LUMO由首virtual轨道提取，均在原±0.15内；修后已关联原有科学结论。 | ar_r_lumo, ar_r_lumo2, ar_r_lumo3 |
| ar_lambda / result | The source calculations report internal λh values of 0.191, 0.186 and 0.189 eV for JY1, JY2 and JY3. | 三λ=.213411/.198457/.211489 eV，均满足原±.03；JY2最小。 | ar_r_lambda, ar_r_lambda2, ar_r_lambda3 |

| 结论 ID / 角色 | 当前科学主张 | 支持关键点及边界 |
| --- | --- | --- |
| ar_final_trend / final | The three validated isolated-molecule HOMO/LUMO and internal hole-reorganization results establish the fluorination comparison; the source-supported HOMO trend and smallest JY2 reorganization energy are assessed from those computed properties. | ar_process_identity, ar_process_reproducibility, ar_homo, ar_lumo, ar_lambda。九个验证值均满足原容差；不同方法与 B3P86 源靶是否可比仍须科学判断。现有源值/容差未放宽，也未将分子量推广为器件性能。 |

修前→修后：关键点 5→5；结论记录 1→1。现有结论为科学成果，不另给普通免责声明计分。真实计算支持范围不因本次改关联而扩大。

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | JY1_neutral | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_acfb039a9f2346f382d9dd9471e1ad41/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_acfb039a9f2346f382d9dd9471e1ad41/stdout.log) | [0, 1] | -2579.8822542300 | -2579.1611430000 | 300 / 0 / 7.5454 | native normal |
| 2 | JY1_cation | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_e553e801a9e644a8b019dfd693ad79c3/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_e553e801a9e644a8b019dfd693ad79c3/stdout.log) | [1, 2] | -2579.6576548500 | -2578.9352150000 | 300 / 0 / 8.4205 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 3 | JY1_cation_at_neutral | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_cation_at_neutral_final_parent_sp_20260915/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_cation_at_neutral_final_parent_sp_20260915/stdout.log) | [1, 2] | -2579.6538306900 | — | — | native normal |
| 4 | JY1_neutral_at_cation | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_neutral_at_cation_final_parent_sp_20260915/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_neutral_at_cation_final_parent_sp_20260915/stdout.log) | [0, 1] | -2579.8782356700 | — | — | native normal |
| 5 | JY2_neutral | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/artifacts/gaussian_batch/JY2_neutral_optfreq__segfault_retry1/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/artifacts/gaussian_batch/JY2_neutral_optfreq__segfault_retry1/stdout.log) | [0, 1] | -2679.2826105200 | -2678.5711700000 | 300 / 0 / 7.3998 | native normal |
| 6 | JY2_cation | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_ae587ce5146747a581f6f72886f5f2a8/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_ae587ce5146747a581f6f72886f5f2a8/stdout.log) | [1, 2] | -2679.0570912400 | -2678.3440790000 | 300 / 0 / 8.2928 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 7 | JY2_cation_at_neutral | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_cation_at_neutral_final_parent_sp_20260915/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_cation_at_neutral_final_parent_sp_20260915/stdout.log) | [1, 2] | -2679.0534720600 | — | — | native normal |
| 8 | JY2_neutral_at_cation | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_neutral_at_cation_final_parent_sp_20260915/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_neutral_at_cation_final_parent_sp_20260915/stdout.log) | [0, 1] | -2679.2789365300 | — | — | native normal |
| 9 | JY3_neutral | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_optfreq_20260925_hpc20_p6/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_optfreq_20260925_hpc20_p6/stdout.log) | [0, 1] | -2778.6697651000 | -2777.9670560000 | 300 / 0 / 7.1131 | native normal |
| 10 | JY3_cation | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_optfreq_20260925_hpc20_p6/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_optfreq_20260925_hpc20_p6/stdout.log) | [1, 2] | -2778.4433081500 | -2777.7392220000 | 300 / 0 / 7.8966 | native normal |
| 11 | JY3_cation_at_neutral | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_at_neutral_sp_20260925_hpc20_p6/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_at_neutral_sp_20260925_hpc20_p6/stdout.log) | [1, 2] | -2778.4394660100 | — | — | native normal |
| 12 | JY3_neutral_at_cation | [输入](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_at_cation_sp_20260925_hpc20_p6/input.com) / [原始输出](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_at_cation_sp_20260925_hpc20_p6/stdout.log) | [0, 1] | -2778.6658351600 | — | — | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1, 2, 5, 6, 9, 10 | `#p B3P86/6-311G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512)` |
| 3, 4, 7, 8 | `#p B3P86/6-311G(d,p) NoSymm SCF=(XQC,MaxCycle=512)` |
| 11, 12 | `#p B3P86/6-311G(d,p) SP NoSymm SCF=(XQC,MaxCycle=512)` |

## 5. 模型、连接与后处理原始出处

- [provenance/source_cycle_closure_20260926/result.json](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/source_cycle_closure_20260926/result.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/report/results.json)

## 6. 修后包检查与未认证事项（2026-09-29）

当前策略为 `dual_axis_100.scientific_results.v1`；真实历史 report 对本包的实际输出检查：**通过**。本包已执行 14 个提交样例，每个分别经过 JSON Schema 和真实 validate_output_contract；合成正反例只测试格式，未加入本计算档案的科学证据。

九个验证值均满足原容差；不同方法与 B3P86 源靶是否可比仍须科学判断。现有源值/容差未放宽，也未将分子量推广为器件性能。

[逐包维护记录](task_provenance/maintenance_audit.md)及[集中报告第30节](../../../MAINTENANCE_REPORT.md)记录实际修改、检查与未闭合项。普通免责声明已取消必填及独立计分，身份/态/收敛/频率/路径/参考态和真实失败证据保留。

本次没有新电子结构计算、HPC 操作、完整 LLM 评分或 AR 盲测；没有迁移 final/hold。文件导出检查只覆盖 agent_input 物化，不能替代部署侧父目录、容器挂载和网络隔离。完整原始证据直接链接在第 4、5 节，不依赖 task_provenance 的长期存在。
