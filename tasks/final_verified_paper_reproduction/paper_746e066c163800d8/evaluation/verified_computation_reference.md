# 已验证成功计算链：compound 5 螺烯内缘扭转

- 论文 ID：`paper_746e066c163800d8`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1016/j.dyepig.2025.113306`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_746e066c163800d8)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：READY / PASS / QUALIFIED（compound 5 几何子目标）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_746e066c163800d8)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 根据 SI Table S1/S2 核对 compound 5 结构及五个内缘扭转的原子映射；保持同一化学身份，不扩展到非线性光学性质。

2. 执行作者 B3LYP/6-31G(d) 气相 Gaussian Opt/Freq 主计算；得到 210 个实频和 0 个虚频。

3. 在同一身份上完成更紧的 Opt=Tight、UltraFine、Tight SCF 几何/频率复核；同样得到 210 实频，作为数值稳健性检查而非另一个参考目标。

4. 从两份最终 orientation 按固定四原子序列提取五个有符号内缘二面角，计算五角绝对值的平均，并与论文计算 27.1°、实验边界 27.0°比较。完整五角和链式原子索引见专用几何分析 JSON。

## 3. 实际结果与支持的结论

| 量 | 主计算 | Tight 复核 |
|---|---:|---:|
| 电子能 / Eh | −1843.68626335 | −1843.68626335 |
| 最低实频 / cm⁻¹ | 20.5698 | 20.5613 |
| 五个内缘扭转绝对值平均 / ° | 27.09676855 | 27.09673780 |

两次平均角差约 0.00003075°，支持论文所述螺旋扭曲程度及任务的几何比较结论。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| baseline | [input.com](../../../../docs/verification/group_1/paper_746e066c163800d8/artifacts/gaussian_batch/helicene_b3lyp_optfreq/input.com) | [stdout.log](../../../../docs/verification/group_1/paper_746e066c163800d8/artifacts/gaussian_batch/helicene_b3lyp_optfreq/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| tighter_check | [input.com](../../../../docs/verification/group_1/paper_746e066c163800d8/provenance/qzcli_hpc/compound5_b3lyp_tight_geometry_check_20260915/repair_20260915T080810Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_746e066c163800d8/provenance/qzcli_hpc/compound5_b3lyp_tight_geometry_check_20260915/repair_20260915T080810Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/inner_rim_closure_audit_20260915.json](../../../../docs/verification/group_1/paper_746e066c163800d8/provenance/inner_rim_closure_audit_20260915.json)
- [artifacts/inner_rim_complete_20260915.json](../../../../docs/verification/group_1/paper_746e066c163800d8/artifacts/inner_rim_complete_20260915.json)
- [report/results.json](../../../../docs/verification/group_1/paper_746e066c163800d8/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_746e066c163800d8/verification_report.md)
- [provenance/close_inner_rim_20260915.py](../../../../docs/verification/group_1/paper_746e066c163800d8/provenance/close_inner_rim_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 有限结构/方法验证，不声称穷举所有构象或验证论文 NLO 结论。
- 历史源任务的 experimental_torsion_boundary 将页码写成 p6，正确比较位置为正文 p4；数值未变。当前维护包已将该实验目标资料与作者终态置于 evaluation/author_results，不再作为 agent 输入；canonical 源任务保持只读。
- 作者 Gaussian09 与实际 Gaussian16 的版本差异保留。

## 7. 成功阶段计时

主成功计算 215349.6 s，Tight 复核 2042.0 s，合计 217391.6 s（60.39 h）。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

历史成功几何的五角按 mean(abs(phi)) 重提取为 27.09676855°，收紧优化检查为 27.09673780°，支持原 27.1±2° 金标。公开 XYZ 已改为 topology-only ETKDG 初始结构；原终态及实验 27.0° 只存 author_results。历史作者路线证据继续有效，但未声称从该新 starter 重做 Opt/Freq。
