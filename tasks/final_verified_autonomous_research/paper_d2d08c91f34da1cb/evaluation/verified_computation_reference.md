# 已验证成功计算链：Rhodamine101 两态低频振动

- 论文 ID：`paper_d2d08c91f34da1cb`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1016/j.dyepig.2025.113304`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：READY / PASS / QUALIFIED（当前 base reproduction 的混合模式语义比较范围）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_autonomous_research`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_d2d08c91f34da1cb)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 核对 67 原子 Rhodamine101 的两态身份与原子顺序；S0 和 S1 均为总电荷 0、单重态。验证使用作者路线提供的两态初始坐标，而不是要求验证者盲建构型。

2. 使用 Gaussian 16 C.01，以 B3LYP-D3(BJ)/aug-cc-pVDZ、SMD 甲醇分别执行 S0 Opt/Freq 和第一单重激发态 S1 TD-DFT Opt/Freq。两个输出各有 195 个正频率，均为相应态的已验证局部极小值。

3. 从原始 Gaussian 输出读取全部位移向量，以 0.967 缩放谐振频率；保留 0 < ν_scaled ≤ 125 cm⁻¹ 的全部模式，每态 14 个，不按与实验接近程度挑选。

4. 按公开 SLT CSV 的 state/mode 标签作实验频率配对；跨态模式身份另用质量加权位移重叠、坐标对齐和完整 195 模一对一映射判断。计算片段位移贡献及有限差分内部扭转响应，保留模式交换和低重叠情况。

5. 汇总 28 个窗口模式：24 个有实验配对、2 个实验栏为空、2 个额外计算模式未匹配。由有效配对算 MAE/最大误差，再依据位移/扭转证据讨论羧基苯基和 xanthene 相关混合运动的趋势。

## 3. 实际结果与支持的结论

| 实际计算量 | 结果 |
|---|---|
| S0 / S1 正频率数 | 195 / 195；虚频均为 0 |
| 实验有效配对 | 24；没有为缺失观测补造数据 |
| 总 MAE | 1.262626 cm⁻¹ |
| 最大绝对偏差 | 3.097158 cm⁻¹ |
| 模式 8 跨态变化 | 约 +0.005802 cm⁻¹，基本不变 |

支持任务中带不确定性的混合振动趋势解释；不是“所有核心模式均红移”，也不是字面上“最大偏差 < 3 cm⁻¹”。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| S0 Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/gaussian_batch/r101_s0_author_b3lypd3_augccpvdz_optfreq_hpc_f6a5fe0c/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/gaussian_batch/r101_s0_author_b3lypd3_augccpvdz_optfreq_hpc_f6a5fe0c/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| S1 Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/gaussian_batch/r101_s1_author_td_b3lypd3_augccpvdz_optfreq_hpc_721be5bc/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/gaussian_batch/r101_s1_author_td_b3lypd3_augccpvdz_optfreq_hpc_721be5bc/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/mode_closure_audit_20260915.json](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/provenance/mode_closure_audit_20260915.json)
- [artifacts/mode_identity_complete_20260914.json](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/mode_identity_complete_20260914.json)
- [artifacts/mode_character_review_20260915.json](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/mode_character_review_20260915.json)
- [report/results.json](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/verification_report.md)
- [provenance/complete_mode_identity_20260914.py](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/provenance/complete_mode_identity_20260914.py)
- [provenance/review_mode_character_20260915.py](../../../../docs/verification/group_1/paper_d2d08c91f34da1cb/provenance/review_mode_character_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 模式 1/2 跨态对应发生交换；模式 3/4/13/14 的正移、模式 8 基本不变以及低重叠均保留，不能只挑符合预期的模式。
- 实验只有标签和频率，没有实验位移向量；计算片段动能权重不是势能分布，更不证明完整超快能流机制。
- 原审计明确限定当前 base paper_reproduction；自主模式在此共用科学计算档案，不被自动写为独立评测通过。

## 7. 成功阶段计时

两态成功 Gaussian 阶段耗时合计 368989.0 s（102.50 h），不是旧不完整计时表中的 15096.1 s；后续仅作模式后处理。合计阶段时间不等于日历工期。

本次归档没有提交、重启或停止任何计算作业。
