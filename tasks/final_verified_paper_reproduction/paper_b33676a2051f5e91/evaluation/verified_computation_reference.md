# 已验证成功计算链：Int-3 β-scission TS / IRC

- 论文 ID：`paper_b33676a2051f5e91`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1039/d5gc05996h`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_4](../../../../docs/verification/group_4/paper_b33676a2051f5e91)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_4.md)
- 最新已归档科学状态：READY / PASS / MATCH / QUALIFIED（Int-3 指定 β-scission 通道；产物侧 IRC 为有限路径）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_b33676a2051f5e91)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 按 SI 的 Int-3/TS-4b 身份核对 24 原子 C10H13O 中性自由基双重态及原子映射。使用作者结构作为验证起点，不把由图感知失真产生的 radical_electrons=7 当作真实电子态。

2. 用 Gaussian UBHandHLYP/aug-cc-pVDZ、SMD 乙腈、298.15 K 分别完成 Int-3 的 Opt/Freq 和目标 TS 的 Opt=(TS,CalcFC,…)/Freq。SCRF 在输入续行中，不能只读取首行后误判缺少溶剂；SI 不要求 QST3。

3. 反应物 66 个模式均为实频，TS 66 个模式中仅一个虚频 −474.9764 cm⁻¹。对负模式位移做键长投影，C12–C13 延长与 C12–O24 缩短对应目标 β-scission。

4. 从该 TS 分别运行同级 IRC=(LQA,CalcFC,Forward/Reverse,MaxPoints=80,StepSize=5)。forward 在第 64 点检测到 Int-3 侧极小值；reverse 在 80 点上限正常结束，进入乙酰苯+乙基自由基分离区。用分子图、C–C/C=O 距离和乙基自旋支持通道归属。

5. 从反应物与 TS 的同温度 Gibbs 总能计算 (G_TS−G_Int3)×627.509474；不以未优化的分离产物端点能量构造本任务没有验证的产物解离自由能。

6. 将势垒、单虚频/位移、双向通道及范围限定逐项核对 evaluator，保留产物侧未验证有限距离极小值的事实。

## 3. 实际结果与支持的结论

| 量 | 实际值 |
|---|---:|
| G(Int-3) / Eh | −463.661083 |
| G(TS) / Eh | −463.646904 |
| ΔG‡ / kcal mol⁻¹ | 8.8974568327（参考 9.07 ± 2.0） |
| C12–C13：Int-3 → TS / Å | 1.53763364 → 2.06424080 |
| C12–O24：Int-3 → TS / Å | 1.39731876 → 1.25383293 |
| reverse 终点 C12–C13 / C12–O24 / Å | 3.65849248 / 1.21342529 |
| reverse 终点乙基自旋 | 0.998047 |

支持指定 Int-3 → 乙酰苯 + 乙基自由基通道及其 TS 相对势垒。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| reactant | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_0ca67f7e40bd440eab8861701bf0d8b3/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_0ca67f7e40bd440eab8861701bf0d8b3/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| ts | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_3fed45618b73427f8c87b8ae02bd96fc/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/native_workspace_batch/outputs/execution_jobs/job_3fed45618b73427f8c87b8ae02bd96fc/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| forward | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_forward_lqa_irc_20260914_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_forward_lqa_irc_20260914_hpc20_p6/stdout.log) | Gaussian 正常终止标记 1 处 |
| reverse | [input.com](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_reverse_lqa_irc_20260914_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_b33676a2051f5e91/hpc_runs/b336_beta_scission_reverse_lqa_irc_20260914_hpc20_p6/stdout.log) | Gaussian 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_channel_closure_20260915.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/author_channel_closure_20260915.json)
- [provenance/evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/evaluation_task_qualification.json)
- [report/results.json](../../../../docs/verification/group_4/paper_b33676a2051f5e91/report/results.json)
- [verification_report.md](../../../../docs/verification/group_4/paper_b33676a2051f5e91/verification_report.md)
- [prepare_lqa_recovery_20260914.py](../../../../docs/verification/group_4/paper_b33676a2051f5e91/prepare_lqa_recovery_20260914.py)
- [finalize_author_channel_20260915.py](../../../../docs/verification/group_4/paper_b33676a2051f5e91/finalize_author_channel_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- reverse 是正常终止但达到 MaxPoints 的有限 IRC，不是无限分离极限，也没有产物端点的后续 Opt/Freq；这不被伪写成完整产物极小值验证。
- 仅验证 Int-3 乙基通道，不声称计算了竞争甲基通道或完整聚合物机制。
- group 总表的乙基自旋写成 0.998147，本归档采用专门原始审计 JSON 的 0.998047，不放大这一转录差异。

## 7. 成功阶段计时

四个有效阶段 elapsed 分别为 36517.1、221250.5、6654.0、6673.5 s，合计 271095.1 s（75.3042 h）；CPU 合计 328625.6 s（91.2849 核时）。均排除失败/被替代路径，wall 合计非日历工期。

本次归档没有提交、重启或停止任何计算作业。

## Evidence scope review (2026-09-19)

The archived ethyl-scission chain supports the PR/local-path comparison. It does not itself establish comparison of chemically different AR beta-scission channels. Different starting guesses for the same mapped cleavage remain one channel unless distinct discriminating evidence is provided.
