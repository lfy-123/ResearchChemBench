# 已验证成功计算链：1M-TIPS D3 / PCM TD20

- 论文 ID：`paper_c23cfabbd34b087f`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1021/acs.joc.5c01690`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_2](../../../../docs/verification/group_2/paper_c23cfabbd34b087f)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_2.md)
- 最新已归档科学状态：显式 D3 几何→同几何 D3/PCM TD20 作者路线及跃迁审计通过。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_c23cfabbd34b087f)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 确认 1M-TIPS 计算模型是 C58H42Si2、102 原子中性单重态，保持论文采用的截取/取代模型边界。

2. 在气相以 B3LYP-D3/def2SVP 完成 Gaussian Opt/Freq；最终为 300 实频、0 虚频的局部极小值。

3. 使用该实际末态几何，执行显式带 D3 的 B3LYP/def2SVP TD20，PCM 氯仿；核对优化末态与 TD 输入逐坐标一致。不把旧未显式带 D3 的 TD 输出替换进本链。

4. 从全部 20 个 singlet 中按 f≥0.001 选最低允许跃迁，得到 state 1；同时从占据数确认 209 个 α 和 209 个 β 电子，HOMO/LUMO 对应 209/210。

5. 读取 209→210 的主要振幅 0.69912，并结合归档轨道性质讨论 π–π* 与共轭离域；与 evaluator 的波长、强度及定性解释逐项对照。

## 3. 实际结果与支持的结论

| 量 | 实际值 | evaluator 参考 |
|---|---:|---:|
| 最低允许跃迁 | state 1 | 最低满足强度门槛的 singlet |
| 波长 / nm | 735.93 | 735 ± 25 |
| 振子强度 f | 1.2539 | 1.24 ± 0.25 |
| 主贡献 | 209→210，振幅 0.69912 | HOMO→LUMO 主导 |

支持该模型低能吸收的 HOMO–LUMO 主导 π–π* 指认。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| author_b3lypd3_def2svp_optfreq_retry_20260911 | [input.com](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/qzcli_hpc/author_b3lypd3_def2svp_optfreq_retry_20260911_hpc20_20260911T062741Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/qzcli_hpc/author_b3lypd3_def2svp_optfreq_retry_20260911_hpc20_20260911T062741Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_b3lypd3_def2svp_td20_pcm_exact_d3_20260912 | [input.com](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/qzcli_hpc/author_b3lypd3_def2svp_td20_pcm_exact_d3_20260912_hpc20_20260912T212836Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/qzcli_hpc/author_b3lypd3_def2svp_td20_pcm_exact_d3_20260912_hpc20_20260912T212836Z/stdout.log) | Gaussian 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_route_evaluation_audit.json](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/author_route_evaluation_audit.json)
- [provenance/1m_tips_td_state_parse.json](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/1m_tips_td_state_parse.json)
- [report/results.json](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/report/results.json)
- [verification_report.md](../../../../docs/verification/group_2/paper_c23cfabbd34b087f/verification_report.md)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 102 原子是论文计算模型，不等于包含全部实验取代基/环境的完整实验体系。
- 当前记录支持轨道层面的定性解释，不声称做过没有证据的 NTO 或完整激发态动力学。

## 7. 成功阶段计时

原始 Gaussian 与 HPC 汇总存在应用时间/调度时间口径差异；保留各成功日志，不拼接不一致的时间字段。

本次归档没有提交、重启或停止任何计算作业。
