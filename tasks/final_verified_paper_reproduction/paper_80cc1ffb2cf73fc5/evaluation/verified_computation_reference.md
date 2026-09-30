# 已验证成功计算链：Z1 Franck–Condon 谱与模式归属

- 论文 ID：`paper_80cc1ffb2cf73fc5`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1039/d5cp04796j`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：Z1-only 既有 FC 计算有效；本轮补入纯实验向量曲线并作相对对齐后处理，支持有限突出特征/进动，不支持全谱或绝对脱附能准确性。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_80cc1ffb2cf73fc5)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 固定 27 原子 Z1 mHBDI：S0 阴离子电荷 −1/单重态，D0 中性自由基电荷 0/双重态，核连接性相同。

2. Gaussian ωB97X-D/aug-cc-pVTZ 气相依次完成阴离子与中性态优化及频率。原组合日志的前四个量化段均正常结束，两态各 75 个实频。

3. 直接复用上述成功 checkpoint/Hessian，通过 ReadFC、FC、ReadFCHT 输入两个完整的 0.9566 缩放频率列表，保留完整 Duschinsky J/K；6 K、HWHM 2 cm⁻¹、网格 1 cm⁻¹。有效 FC 主作业自然正常结束。

4. 追加同波函数 FC 初筛敏感性：主设置 (75,50)，加强为 (100,75)；比较各 2501 个谱点与所选窗口的量子跃迁，不重新做成功的 Opt/Freq。

5. 解析 75 模位移、Huang–Rhys 因子及频率，使用平面投影和最大原子位移 0.1 Å 的正负有限位移检查关键模式是否为平面内弯曲。

6. 汇总相对级进及窗口内 11 个显著跃迁。当时尚未提取逐点实验数据，历史结果保留 mae=null。2026-09-16 已补入 825 点实验黑色向量 trace，并完成文末记录的相对对齐后处理；没有补造绝对峰配对或改写旧结果。

## 3. 实际结果与支持的结论

| 量 | 实算 |
|---|---:|
| 主导 neutral 模式 | mode 3，平面内弯曲 |
| mode 3 缩放频率 / cm⁻¹ | 85.9573 |
| 最大 Huang–Rhys 因子 | 1.20932 |
| FC 回收总强度 | 99.63% |
| 两初筛窗口显著跃迁数 | 均为 11 |
| 最大峰移/归一化谱差 | 输出精度内为 0 |

支持当前任务的低频中性核心弯曲 FC 级进解释；不声称所有实验带的唯一归属。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| S0/D0 Opt/Freq：仅前四个成功段 | [input.com](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/gaussian_batch/z1_author_avtz_anion_neutral_fc_corrected_g1_v2_hpc_759a1441/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/gaussian_batch/z1_author_avtz_anion_neutral_fc_corrected_g1_v2_hpc_759a1441/gaussian.log) | Gaussian 正常终止标记 4 处；有优化收敛标记；同一文件另有 1 处错误终止，仅采纳明确成功段；仅收录 Opt/Freq 成功段，随后失败的旧 FC 段不构成成功证据。 |
| FC 主计算 | [input.com](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/local_recovery_20260914/z1_fc_readonly_scaled_lists_20260914/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/local_recovery_20260914/z1_fc_readonly_scaled_lists_20260914/gaussian.log) | Gaussian 正常终止标记 1 处 |
| FC 加强初筛 | [input.com](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/local_recovery_20260914/z1_fc_readonly_scaled_lists_20260914_convergence/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/local_recovery_20260914/z1_fc_readonly_scaled_lists_20260914_convergence/gaussian.log) | Gaussian 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/fc_closure_audit_20260914.json](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/fc_closure_audit_20260914.json)
- [artifacts/fc_closure_20260914/fc_analysis.json](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/fc_closure_20260914/fc_analysis.json)
- [artifacts/fc_closure_20260914/modes_full.json](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/fc_closure_20260914/modes_full.json)
- [report/results.json](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/verification_report.md)
- [provenance/finalize_fc_recovery_20260914.py](../../../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/finalize_fc_recovery_20260914.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 原组合日志在四个成功量化段之后有旧 FC 语法错误；下表只引用其成功 Opt/Freq 段。有效 FC 来源是独立的两份正常结束新日志，不把旧失败段计作成功。
- 不证明扩散 DBS/DRS 波函数或论文所有异构体。
- 原审计包含两模式对同一结果的 schema/reference 兼容性检查，这仍不等于独立自主 agent 测试。

## 7. 成功阶段计时

原四个成功阶段 61783.3 s；有效 FC 主计算 105.43 s，因此一条主成功路线 61888.73 s（17.19 h）；额外收敛复查 65.29 s。含复查共 61954.02 s（17.21 h），均为阶段之和。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

补入的实验来自 SI Fig S1 独立黑色实测向量线，不是拟合或理论曲线。本次仅解析既有 FC 结果：0–0=18926.1908 cm⁻¹ 与实验最低峰 19444 cm⁻¹ 作相对零点对齐，得到本次后处理平移 517.8092 cm⁻¹（不作为公开常数）。没有重算 FC、没有拟合新的金标/容差。

以下为全部窗口内已存 FC 跃迁的最近实验突出峰诊断，不是唯一逐峰归属。历史审计选峰步骤：排序实验向量顶点、重复 x 取平均、按 1 cm⁻¹ 网格线性插值，再以 scipy find_peaks 的 prominence=0.02（信号单位）、最小间距 25 cm⁻¹ 提取突出峰。得到 19445、19523、19602、19694、19748、19788、19844、19889、19920、19957、20012、20038、20093 cm⁻¹ 共 13 峰；每个已存 FC 跃迁与最近突出峰比较，重复匹配不当作独立归属证据。此规则只描述已有后处理，不是新 evaluator 阈值或拟合实验误差。原始 trace 见 [公开实验 CSV](../agent_input/data/inputs/experimental_spectrum.csv)，FC 原始结果见上方 group 输出索引；维护副本为 task_provenance/experimental_comparison_20260916.json，删除维护副本不会丢失本段计算步骤。

| FC branch | Aligned calculated cm⁻¹ | Nearest selected experimental cm⁻¹ | Difference cm⁻¹ |
|---|---:|---:|---:|
| 0 | 19444.000 | 19445.0 | -1.000 |
| 3^1 | 19529.957 | 19523.0 | +6.957 |
| 3^2 | 19615.915 | 19602.0 | +13.915 |
| 3^3 | 19701.872 | 19694.0 | +7.872 |
| 10^1;3^1 | 19739.720 | 19748.0 | -8.280 |
| 3^4 | 19787.829 | 19788.0 | -0.171 |
| 16^1 | 19893.491 | 19889.0 | +4.491 |
| 18^1 | 19954.066 | 19957.0 | -2.934 |
| 16^1;3^1 | 19979.448 | 19957.0 | +22.448 |
| 18^1;3^1 | 20040.023 | 20038.0 | +2.023 |
| 16^1;3^2 | 20065.406 | 20038.0 | +27.406 |

前四个低能进动和部分高窗特征与实验呈有限对应；19748、19844、19920 等强实验特征及强度差异仍不能全部由 Z1 唯一解释。保留 mode3 对应物理位移/HR=1.20932 的历史证据与未归属限制，不宣称全部峰吻合、绝对脱附能准确或双异构体拟合已验证。旧文中“尚无公开实验数据”的描述是当时状态，由本段补齐当前输入。
