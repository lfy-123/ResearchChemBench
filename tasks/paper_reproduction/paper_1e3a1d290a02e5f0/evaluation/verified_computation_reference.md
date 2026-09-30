# 已验证计算参考：paper_1e3a1d290a02e5f0 / paper_reproduction

核查日期：2026-09-29。此文件是私有历史计算证据，不是评分 gold，不新增要求或容差，不能导出给被评 agent。

源任务：`tasks/paper_reproduction/paper_1e3a1d290a02e5f0`；Git 基线 `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`（实际未提交文件亦已备份）。来源 group 4。两模式共享作者辅助计算证据，但分别映射当前 evaluator；没有新 agent 盲测、LLM judge 或公开起点完整回放。

**结论：现有作者路线计算支持当前限定科学量及其结果趋势。任务包的公开输入、schema、评分关联/政策问题另行审查；计算可行性不等于包已可发布或自主搜索已验证。**

## 1. 论文、模型与采用协议

Gaussian 16 B3P86/6-311G(d,p)，气相。每个分子一个中性单重态及一个 +1 双重态最低点，再做 cation@neutral 和 neutral@cation 两个定几何单点，共 12 份真实日志。六个最低点均 102 原子、300 正频率。JY1/2/3 的 F 取代位分别 4′、3′/5′、3′/4′/5′；现有源输入身份正确。正文物理第 2 页 Figure 2、方法与第 3 页 Table 2；本地无 JY SI。源 G09 与本地 G16 不同，作者构象不能称全局最低。

论文来源：[正文](../../../../papers/paper_1e3a1d290a02e5f0/documents/main.pdf)。上述页码为 PDF 物理页码。

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

## 3. 当前必评关键点与结论覆盖

| 当前ID / 类型 | 当前要求 | 真实支持、范围或缺口 | 对应规则 |
| --- | --- | --- | --- |
| pr_process_identity / process | The three submitted records preserve the named JY1, JY2 and JY3 identities as neutral singlets and provide a connectivity-preserving optimized geometry plus a minimum validation for each. | JY1/2/3中性最低点各300正频，0/1；阳离子+1/2也为最低点。 | pr_r_identity |
| pr_process_lambda / process | Internal λh is derived from a documented neutral/cation energy cycle rather than asserted without state energies. | 四态能量式逐项复算，六组父子几何核对一致。 | pr_r_lambda_process |
| pr_homo / result | The calculated HOMO energies are JY1 −5.12 eV, JY2 −5.17 eV and JY3 −5.18 eV. | 三HOMO由最后occupied轨道提取，均在原±0.15内。 | pr_r_homo1 |
| pr_lumo / result | The calculated LUMO energies are JY1 −1.88 eV, JY2 −2.19 eV and JY3 −2.18 eV. | 三LUMO由首virtual轨道提取，均在原±0.15内；现有成果关联有缺口。 | pr_r_lumo1 |
| pr_lambda / result | The internal hole reorganization energies are JY1 0.191 eV, JY2 0.186 eV and JY3 0.189 eV. | 三λ=.213411/.198457/.211489 eV，均满足原±.03；JY2最小。 | pr_r_lambda1 |

| 结论 ID / 当前角色 | 当前科学主张 | 证据和接受边界 |
| --- | --- | --- |
| pr_final_trend / final | Within this isolated-molecule calculation boundary, fluorination makes the reported HOMO progressively deeper from JY1 to JY3, while JY2 has the smallest λh of the three. | 第2节原始量推导及本表支持关键点：pr_homo, pr_lambda。作者路线范围，不代表独立盲搜索。 |

## 4. 采用原始输入/输出完整索引

以下每行均直接重读原始日志，检查应用结束、能量、电子态、几何和可用频谱；正常结束不自动等于整段科学有效。E 表示该日志最后的 TD（若有）、ORCA 或 SCF 电子能。频率列给完整模数/负模数/最低频；单点/路径未做频率则为 —，不得解释为零虚频最低点。几何父子配对共本批 83 组、原子顺序和距离一致；只对实际下游做过配对的分支作此声明。

| 序 | 采用身份/步骤 | 输入与原始输出 | q / multiplicity | 电子E / Eh | 原始谐振G / Eh | 频谱 总/负/min cm⁻¹ | 核查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | JY1_neutral | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_acfb039a9f2346f382d9dd9471e1ad41/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_acfb039a9f2346f382d9dd9471e1ad41/stdout.log) | [0, 1] | -2579.8822542300 | -2579.1611430000 | 300 / 0 / 7.5454 | native normal |
| 2 | JY1_cation | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_e553e801a9e644a8b019dfd693ad79c3/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_e553e801a9e644a8b019dfd693ad79c3/stdout.log) | [1, 2] | -2579.6576548500 | -2578.9352150000 | 300 / 0 / 8.4205 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 3 | JY1_cation_at_neutral | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_cation_at_neutral_final_parent_sp_20260915/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_cation_at_neutral_final_parent_sp_20260915/stdout.log) | [1, 2] | -2579.6538306900 | — | — | native normal |
| 4 | JY1_neutral_at_cation | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_neutral_at_cation_final_parent_sp_20260915/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy1_neutral_at_cation_final_parent_sp_20260915/stdout.log) | [0, 1] | -2579.8782356700 | — | — | native normal |
| 5 | JY2_neutral | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/artifacts/gaussian_batch/JY2_neutral_optfreq__segfault_retry1/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/artifacts/gaussian_batch/JY2_neutral_optfreq__segfault_retry1/stdout.log) | [0, 1] | -2679.2826105200 | -2678.5711700000 | 300 / 0 / 7.3998 | native normal |
| 6 | JY2_cation | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_ae587ce5146747a581f6f72886f5f2a8/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/local_migration_job_ae587ce5146747a581f6f72886f5f2a8/stdout.log) | [1, 2] | -2679.0570912400 | -2678.3440790000 | 300 / 0 / 8.2928 | native normal；按 negligible forces 完成优化，非所有 displacement 阈值 YES |
| 7 | JY2_cation_at_neutral | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_cation_at_neutral_final_parent_sp_20260915/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_cation_at_neutral_final_parent_sp_20260915/stdout.log) | [1, 2] | -2679.0534720600 | — | — | native normal |
| 8 | JY2_neutral_at_cation | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_neutral_at_cation_final_parent_sp_20260915/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/local_stage_tests_20260914/jy2_neutral_at_cation_final_parent_sp_20260915/stdout.log) | [0, 1] | -2679.2789365300 | — | — | native normal |
| 9 | JY3_neutral | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_optfreq_20260925_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_optfreq_20260925_hpc20_p6/stdout.log) | [0, 1] | -2778.6697651000 | -2777.9670560000 | 300 / 0 / 7.1131 | native normal |
| 10 | JY3_cation | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_optfreq_20260925_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_optfreq_20260925_hpc20_p6/stdout.log) | [1, 2] | -2778.4433081500 | -2777.7392220000 | 300 / 0 / 7.8966 | native normal |
| 11 | JY3_cation_at_neutral | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_at_neutral_sp_20260925_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_cation_at_neutral_sp_20260925_hpc20_p6/stdout.log) | [1, 2] | -2778.4394660100 | — | — | native normal |
| 12 | JY3_neutral_at_cation | [输入](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_at_cation_sp_20260925_hpc20_p6/input.com) / [原始输出](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/hpc_runs/jy3_source_345_fluoro_neutral_at_cation_sp_20260925_hpc20_p6/stdout.log) | [0, 1] | -2778.6658351600 | — | — | native normal |

### 4.1 原生版本与实际输入路由

原始日志版本：`Gaussian 16:  ES64L-G16RevC.01  3-Jul-2019`。下表只归并相同 route 文本，未将不同模型合并；GenECP 分块及 ORCA 专用设置以对应原始输入为准。

| 上表序号 | 实际路由/方法设置 |
| --- | --- |
| 1, 2, 5, 6, 9, 10 | `#p B3P86/6-311G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512)` |
| 3, 4, 7, 8 | `#p B3P86/6-311G(d,p) NoSymm SCF=(XQC,MaxCycle=512)` |
| 11, 12 | `#p B3P86/6-311G(d,p) SP NoSymm SCF=(XQC,MaxCycle=512)` |

## 5. 模型、连接与后处理原始出处

- [provenance/source_cycle_closure_20260926/result.json](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/provenance/source_cycle_closure_20260926/result.json)
- [历史实际 report（保持原样；不等同当前两模式提交都通过）](../../../../docs/verification/group_4/paper_1e3a1d290a02e5f0/report/results.json)

## 6. 本次核查与未认证事项

本包新增参考前 package validator 为 passed，实际策略 `dual_axis_100.v1`；真实历史 report 的实际 output runner 格式检查为 True。这些是软件状态，不能替代本文件的科学判断。

本轮未新算电子结构、未提交/停止 HPC；qRRHO 重读及原始数值/几何/根序/拓扑重提取为已有结果后处理。源图/构型/CIP 审计沿用已定位原证据并核对适用性，不冒称全部重新执行。完整采用链记录在本文件，删除辅助 task_provenance 不应使来源失联。公开包只允许 agent_input；部署侧父目录、容器挂载及网络隔离本轮未实测。维护问题不通过改写 reference 变成 gold。
