# 已验证成功计算链：syn / anti La-KHQ 热化学

- 论文 ID：`paper_d8e5490cd9942f4f`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1039/d5dt03015c`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_2](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_2.md)
- 最新已归档科学状态：正确 +1/单重态、La ECP46MWB 作者路线的 syn/anti 热化学通过。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_d8e5490cd9942f4f)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 核对 syn/anti 均为 81 原子 [La-KHQ]+（C32H38LaN4O6+），总电荷 +1、单重态；两者原子组成与比较边界一致。

2. 在 Gaussian 使用 ωB97X-D/GenECP：C/H/N/O 为 def2SVP，La 为 ECP46MWB 大芯相对论 ECP 配套基组；SMD 水、298.15 K。分别完成 syn 与 anti 的 Opt/Freq，使用实际输入中的显式基组/ECP 区块。

3. 两条输出均正常终止，每条 237 实频、0 虚频。提取同温度、同标准态的最终电子能和热校正，读取完整 Gibbs 自由能。

4. 计算 ΔG(anti−syn) = [G(anti)−G(syn)] × 627.509474；同分子异构体的共同标准态处理不引入不对称修正。

5. 比较正的 anti−syn 自由能差及结构身份，逐项审计 evaluator 所需的 syn 热力学较低结论。

## 3. 实际结果与支持的结论

| 量 | 实际值 |
|---|---:|
| G(syn) / Eh | −1941.937433 |
| G(anti) / Eh | −1941.930431 |
| ΔG(anti−syn) / kcal mol⁻¹ | +4.393821 |
| syn / anti 虚频数 | 0 / 0 |

在当前水相连续介质模型和作者电子态/ECP 边界内，syn 低于 anti。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| author_syn_La_KHQ_wb97xd_lcrecp_water_optfreq_retry_basis_v2 | [input.com](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/provenance/qzcli_hpc/author_syn_La_KHQ_wb97xd_lcrecp_water_optfreq_retry_basis_v2_hpc20_20260911T063030Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/provenance/qzcli_hpc/author_syn_La_KHQ_wb97xd_lcrecp_water_optfreq_retry_basis_v2_hpc20_20260911T063030Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_anti_La_KHQ_wb97xd_lcrecp_water_optfreq_retry_basis_v2 | [input.com](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/provenance/qzcli_hpc/author_anti_La_KHQ_wb97xd_lcrecp_water_optfreq_retry_basis_v2_hpc20_20260911T063034Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/provenance/qzcli_hpc/author_anti_La_KHQ_wb97xd_lcrecp_water_optfreq_retry_basis_v2_hpc20_20260911T063034Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_route_evaluation_audit.json](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/provenance/author_route_evaluation_audit.json)
- [report/results.json](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/report/results.json)
- [verification_report.md](../../../../docs/verification/group_2/paper_d8e5490cd9942f4f/verification_report.md)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 旧中性电荷、格式错误的基组/ECP 或 LANL2DZ fallback 不属于本成功链。
- 仅验证两构型相对热化学；不外推为动力学、显式溶剂 MD 或所有镧系金属机制。

## 7. 成功阶段计时

成功作业 ledger 记录 syn/anti 约 17330/54767 s；分阶段和不等于并行日历工期。

本次归档没有提交、重启或停止任何计算作业。
