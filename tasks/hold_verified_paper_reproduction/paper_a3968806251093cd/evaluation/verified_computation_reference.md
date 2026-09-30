# 已验证成功计算参考：compound 7a 几何方法比较

- 论文：`paper_a3968806251093cd`；分组：group_2；模式：`paper_reproduction`。
- 更新日期：2026-09-23。本轮只核对既有原始日志并重做几何后处理，没有新增量子化学计算。
- 当前状态：经用户批准修复指令、输入身份及评分；两模式各 4 个关键点、1 个主要科学结论、5 条语义规则。本目录仍为 HOLD，未执行目录迁移。
- 用途：归档真实成功计算、证明科学子问题可计算；不是评分标准，也不是要求 agent 使用私有起点的执行模板。评分以五个 evaluator JSON 为准。本文件及链接均为 evaluator-private。

## 1. 科学对象与论文依据

[正文](../../../../papers/paper_a3968806251093cd/documents/main.pdf) §2.4（PDF pp3–4）、§3.2/Fig.3、§3.3（p5）及结论（p11），[SI](../../../../papers/paper_a3968806251093cd/documents/supplementary_001.pdf) Tables S1–S3（pp8–10）。
对象是正确取代位置的 7a：C20H17ClN6OS、46 原子、中性单重态、C17=N3 的 E-imine、N5-H thione。公开 mapped SMILES 已明确 E 身份；它没有提供任意优化坐标或确定单键构象。

论文使用 B3LYP 与 CAM-B3LYP/6-311+G(d,p) 气相路线比较 SCXRD 几何，并宣称 CAM 的几何/IR 更优。当前任务仅包含几何方法比较；频率用于验证极小值，不新增实验 IR 优劣目标。AR 自选模型，PR 使用作者方法对。本次存量验证采用作者对，证明该几何子问题存在真实计算解；不把验证者已知作者路线说成 AR 自主选择过程。

## 2. 成功链 A：完整来源 CIF 起点

1. 从私有 CCDC 2266402 单个分子的 46 个 atom sites 和晶胞转换 Cartesian 起点，保持源标签、E-imine 和 N5-H。只提取孤立分子，没有优化周期晶体。转换、源文件和几何依据见 [CIF_AUDIT.json](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/cif_7a_20260920/CIF_AUDIT.json)，起点见 [crystal_source_labelled.xyz](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/cif_7a_20260920/crystal_source_labelled.xyz)。
2. 两方法用完全相同的起点，各自自由优化并计算频率。实际为 Gaussian 16 C.01、0/1、气相、无溶剂/色散/约束。各自输入中的路线为：

```text
#p B3LYP/6-311+G(d,p) Opt=(CalcFC,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine
#p CAM-B3LYP/6-311+G(d,p) Opt=(CalcFC,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine
```

每项 %NProcShared=20、%Mem=90GB。论文正文写 G09，而参考文献提到 G16 C.01；这里如实记录实际验证软件，不声称恢复了作者未公开的完整输入和默认值。
3. 逐份重读日志：优化完成、两次正常终止、无 Error termination、各 132 个正频率。日志末段 Cartesian 坐标与归档 XYZ 逐坐标相同；完整重原子连接及每个重原子的 H 数与当前图匹配，E-imine/N5-H/0/1 均成立。最低频率分别 6.0884、3.9248 cm⁻¹。
4. 从两个真实端点，按公开映射各提取 13 键长、23 去重键角、11 二面角，共 94 项。SI 重复的 C6–N1–C7 只计一次，Cl1/Cl2 是同一个氯。numpy 与 RDKit 独立计算一致。
5. 按当前公开 `a396_geometry_comparison_v2` 后处理：保留原始有符号二面角；对每个模型整组 11 个二面角分别与实验向量的 +1/−1 分支比较，以圆周误差 SSE 最小选择一个整体符号，按公开规则处理平局。该规则是经批准的 benchmark 比较约定，不冒充论文原统计方法。当前两个实际端点均选择 +1；因此下表与历史主要结果相同。
6. 六项误差均支持此构象比较中的 CAM 优势。不混合 Å 和 °，不添加事后权重。

| 类别/误差 | B3LYP | CAM-B3LYP |
|---|---:|---:|
| 13 键长 MAE / Å | 0.009136258 | 0.007269655 |
| 13 键长 RMSE / Å | 0.011941034 | 0.008624190 |
| 23 键角 MAE / ° | 0.834539904 | 0.796413820 |
| 23 键角 RMSE / ° | 1.105572345 | 1.070749519 |
| 11 二面角 MAE / ° | 8.241270836 | 5.521946286 |
| 11 二面角 RMSE / ° | 13.480720202 | 8.689311681 |

## 3. 成功链 B：另一正确对象构象

既有第二组计算从正确图生成初态，并参考 SI 两条二面角作构象重建，而不是独立 agent 盲测。起点与生成方式见 [starter.xyz](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/si_conformer_20260920/starter.xyz)、[structure_generation.json](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/si_conformer_20260920/structure_generation.json)。两方法从这一个共同起点分别运行与 A 相同的 Opt/Freq 路线；每个端点仍是正确 E-imine/N5-H 图且有 132 个正频率，最低频率分别 5.9010、5.0328 cm⁻¹。按相同的全部 47 行及整体反演约定后处理，两者选择 +1。

| 类别/误差 | B3LYP | CAM-B3LYP |
|---|---:|---:|
| 13 键长 MAE / Å | 0.009206282 | 0.007247510 |
| 13 键长 RMSE / Å | 0.012073208 | 0.008619332 |
| 23 键角 MAE / ° | 0.960817557 | 0.937671839 |
| 23 键角 RMSE / ° | 1.350651267 | 1.344865633 |
| 11 二面角 MAE / ° | 4.678395135 | 5.544711005 |
| 11 二面角 RMSE / ° | 5.936454955 | 7.379723964 |

这是完整且真实的混合比较：CAM 的键长/键角误差小，B3LYP 的二面角误差小。修订后 evaluator 接受其为完成几何比较，但不能把它说成复现了“CAM 全面优胜”的作者假设。两组结果也说明无需寻找一个隐藏的唯一构象来获得比较结论。

## 4. 原始计算的可追溯入口

所有路径相对仓库根；保留真实成功步骤，不把失败、重试或旧错误异构体列入有效链。

| 成功计算 | 原始输入/输出 | 优化坐标 | Gaussian elapsed |
|---|---|---|---:|
| A / CIF B3LYP | [input.com](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/cif7a_B3LYP_optfreq_20260920_20260920T150922Z/input.com) / [stdout.log](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/cif7a_B3LYP_optfreq_20260920_20260920T150922Z/stdout.log) | [XYZ](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/cif_7a_20260920/B3LYP_optimized.xyz) | 2.0446 h |
| A / CIF CAM-B3LYP | [input.com](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/cif7a_CAM_B3LYP_optfreq_20260920_20260920T151053Z/input.com) / [stdout.log](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/cif7a_CAM_B3LYP_optfreq_20260920_20260920T151053Z/stdout.log) | [XYZ](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/cif_7a_20260920/CAM-B3LYP_optimized.xyz) | 5.0318 h |
| B / 第二构象 B3LYP | [input.com](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/si7a_B3LYP_optfreq_20260920_20260920T150823Z/input.com) / [stdout.log](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/si7a_B3LYP_optfreq_20260920_20260920T150823Z/stdout.log) | [XYZ](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/si_conformer_20260920/B3LYP_optimized.xyz) | 1.3496 h |
| B / 第二构象 CAM-B3LYP | [input.com](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/si7a_CAM_B3LYP_optfreq_20260920_20260920T152432Z/input.com) / [stdout.log](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/si7a_CAM_B3LYP_optfreq_20260920_20260920T152432Z/stdout.log) | [XYZ](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/si_conformer_20260920/CAM-B3LYP_optimized.xyz) | 2.2515 h |

A 两作业累计 140.842 CPU 核时；四作业合计 212.584 CPU 核时（不是排队时间或日历工期）。平台历史审计见 [FINAL_AUDIT.md](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/cif_hold_acceptance_20260921/FINAL_AUDIT.md)。本轮未查询或操作运行作业。

## 5. 与修订任务的逐项对应

| 当前要求 | 已有证据 | 本轮结论 |
|---|---|---|
| 正确对象、E/N5-H、0/1、稳定映射 | 四份日志/XYZ，完整连接及氢分配 | 支持；不是仅按分子式认定 |
| 两个真实优化及极小值 | 两对共同起点、四份 Opt/Freq、各 132 实频 | 支持；正常退出不是唯一依据 |
| 47 行/模型及分单位 MAE/RMSE | 两组各 94 行；按公开协议重提取 | 支持；无缺行、重复行或隐藏数值目标 |
| 整体反演不改变物理比较 | 每模型两个分支；镜像/旋转/映射自测 | 后处理定义有效；这些自测不是新增量化计算 |
| 主要结论 | A 均匀 CAM 优势；B 混合优势 | 两种完整结果均与修订评分相符 |
| agent 独立构建初态与 AR 自选路线 | 公开图可独立生成 3D；历史验证是来源知情路线 | 没有进行本轮盲测，也不以此虚称任意模型/初态必收敛 |

## 6. 仍需准确表达的事实

SI 理论列有 39/47 项两方法相同、11 个二面角全部相同，且 B3LYP 的 N5–C18/N6–C19 疑似互换。既有 DFT 输出不逐数等同 SI 理论列。本轮没有修改论文表格、实验比较 CSV 或推断作者如何生成这些数字；当前任务不按这些可疑理论小数评分。

公开输入只有化学身份/映射、实验观测及计算无关的比较规则；私有 CIF、DFT 端点、误差结果、作者优胜结论均不进入 agent_input。实验观测是方法比较的参照，不是模型需要重新求得的 DFT 答案。验证允许提前知晓作者路线，不能要求其和受限 agent 的发现过程相同；这也不授权 agent 使用该私有信息。

旧错误位置异构体链排除出本文件的有效计算流程；此前混合历史状态的完整 reference 快照存于 [维护历史](task_provenance/verified_computation_reference_before_repair_20260923.md)，不会用于当前评分。

## 7. 本轮可复查产物

- [本轮修复及验收报告](task_provenance/release_review_20260923.md)。
- [任务包、评分框架及输入隔离检查](task_provenance/package_validation_20260923.json)。
- [只读本地复核脚本](task_provenance/recheck_repair_20260923.py)：直接运行只读取源记录，打印后处理/测试 JSON，不提交作业、不改文件。
- [26 项本地检查与四份原始证据复核](task_provenance/repair_validation_20260923.json)。
- [A 分支按新协议生成的私有结果](task_provenance/cif_7a_20260920_reprocessed.json)；[B 分支结果](task_provenance/si_conformer_20260920_reprocessed.json)。两者通过当前 result_schema；它们是已有计算的后处理副本，不是新量化结果或自动 judge 评分结果。
