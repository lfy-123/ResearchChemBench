# 已验证成功计算链：egan-IrCl cis-α / cis-β 相对能

- 论文 ID：`paper_e31cc7bc7b21b610`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1039/d5dt02509e`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：READY / PASS / QUALIFIED（修复元素身份后的两种 egan 异构体）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_autonomous_research`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_e31cc7bc7b21b610)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 依据 SI S26–S27 核对 cis-α / cis-β-(egan)IrCl：每种 58 原子、总电荷 0、单重态；β 的缺 H/错元素标签已在源任务修正，旧错误身份结果排除。

2. 两种结构按作者 B3LYP、Ir/SDD 基组及 ECP、其余原子/6-31G(d)，气相 Opt/Freq。α 保留正确成功作业；β 使用修正身份后成功作业。Tight/UltraFine/XQC 等数值控制在输入 deck 中保留。

3. 检查优化终止、各 168 个实频、0 虚频，并逐原子核对组成、配位和 α/β 异构体身份。

4. 从同一模型的最终电子能求 E(β)−E(α)，以 627.509474 kcal·mol⁻¹/Eh 换算，判断 α 低于 β。这里比较的是电子能，不替换成 Gibbs 能。

## 3. 实际结果与支持的结论

| 量 | 实算 |
|---|---:|
| E(α) / Eh | −2204.52499151 |
| E(β) / Eh | −2204.52269915 |
| E(β)−E(α) / kcal·mol⁻¹ | +1.43847762 |
| 各端点实频/虚频 | 168 / 0 |

支持 gas-phase cis-α 电子能更低的 evaluator 结论。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| cis_alpha Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/qzcli_hpc/cis_alpha_author_b3lyp_sdd_631gd_optfreq_v2_58atom/hpc_20260911T075318Z_1830377/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/qzcli_hpc/cis_alpha_author_b3lyp_sdd_631gd_optfreq_v2_58atom/hpc_20260911T075318Z_1830377/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| cis_beta Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/qzcli_hpc/cis_beta_author_correct_elements_20260914/repair_20260914T123300Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/qzcli_hpc/cis_beta_author_correct_elements_20260914/repair_20260914T123300Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/correct_identity_closure_20260915.json](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/correct_identity_closure_20260915.json)
- [report/results.json](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/verification_report.md)
- [provenance/finalize_correct_identity_20260915.py](../../../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/finalize_correct_identity_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 作者优化几何在当前源任务中作为供给结构；原验证针对再优化及相对能，不是异构体自主发现。本归档不为公开坐标来源另作发布合格保证。
- 不外推异构化势垒、速率、溶液平衡或 Gibbs 排序。
- 作者完整软件 build/数值默认值未全部公开；α/β 数值优化坐标算法不同但模型层级相同。

## 7. 成功阶段计时

两项成功 Gaussian 阶段分别 2381.0 和 1605.0 s，共 3986.0 s。β 本地稳定性探针 1522.98 s 另计，不与成功主链重复相加。

本次归档没有提交、重启或停止任何计算作业。
