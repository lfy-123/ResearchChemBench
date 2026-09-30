# 已验证成功计算链：三体系 Mulliken 电荷

- 论文 ID：`paper_6f9a36fff6964313`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1039/d5gc06239j`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_6f9a36fff6964313)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：READY / PASS / QUALIFIED（作者两层级电荷路线）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_6f9a36fff6964313)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 分别核对 TFAP、[PTMA]OTf、[TMTFABA]OTf 的完整分子/离子对身份；三个体系均为总电荷 0、单重态，原子数分别 17、32、37。保留 OTf，不把孤立阳离子与中性离子对混作同一模型。

2. 按 SI S16，先以 Gaussian 16 C.01、B3LYP-D3BJ/6-31G(d,p)、IEFPCM(MeCN) 对三个体系 Opt/Freq；分别得到 45、90、105 个实频，无虚频。

3. 在每个最低点的完全相同几何上执行 M062X-D3/def2TZVP、SMD(MeCN) 单点及 Mulliken 布居。归档分析确认各单点与父几何的原子对距离漂移为 0。

4. 由化学邻接环境映射所需原子：TFAP 羰基 C2、PTMA 季铵 N2、TMTFABA 羰基 C9/季铵 N2（Gaussian 1-based）。从完整原始 Mulliken 表提取四个电荷，计算两个有符号差值。

5. 将四项数值及羰基碳/季铵氮变化方向分别与原 evaluator 核对，不使用其它布居方案替代 Mulliken。

## 3. 实际结果与支持的结论

| 原子/差值 | 实算 / e | 论文参考 / e |
|---|---:|---:|
| TFAP 羰基 C | 0.203728 | 0.204 |
| PTMA 季铵 N | 0.040059 | 0.036 |
| TMTFABA 羰基 C | 0.198533 | 0.200 |
| TMTFABA 季铵 N | 0.058695 | 0.040 |
| 羰基 C：TMTFABA − TFAP | −0.005195 | 方向一致 |
| 季铵 N：TMTFABA − PTMA | +0.018636 | 方向一致 |

四个电荷均在既有 ±0.02 e 容差内，两个差值方向一致。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| tfap Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/qzcli_hpc/tfap_SI631gdp_GD3BJ_redundant_20260915/repair_20260915T075256Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/qzcli_hpc/tfap_SI631gdp_GD3BJ_redundant_20260915/repair_20260915T075256Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| tfap Mulliken SP | [input.com](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/local_recovery_20260915/tfap_author_M062X_GD3_def2TZVP_SMD_Mulliken_20260915/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/local_recovery_20260915/tfap_author_M062X_GD3_def2TZVP_SMD_Mulliken_20260915/gaussian.log) | Gaussian 正常终止标记 1 处 |
| ptma_otf Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/qzcli_hpc/ptma_otf_SI631gdp_GD3BJ_redundant_20260915/repair_20260915T075531Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/qzcli_hpc/ptma_otf_SI631gdp_GD3BJ_redundant_20260915/repair_20260915T075531Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| ptma_otf Mulliken SP | [input.com](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/local_recovery_20260915/ptma_otf_author_M062X_GD3_def2TZVP_SMD_Mulliken_20260915/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/local_recovery_20260915/ptma_otf_author_M062X_GD3_def2TZVP_SMD_Mulliken_20260915/gaussian.log) | Gaussian 正常终止标记 1 处 |
| tmtfaba_otf Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/qzcli_hpc/tmtfaba_otf_SI631gdp_GD3BJ_redundant_20260915/repair_20260915T080014Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/qzcli_hpc/tmtfaba_otf_SI631gdp_GD3BJ_redundant_20260915/repair_20260915T080014Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| tmtfaba_otf Mulliken SP | [input.com](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/local_recovery_20260915/tmtfaba_otf_author_M062X_GD3_def2TZVP_SMD_Mulliken_20260915/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/local_recovery_20260915/tmtfaba_otf_author_M062X_GD3_def2TZVP_SMD_Mulliken_20260915/gaussian.log) | Gaussian 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/charge_closure_audit_20260915.json](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/charge_closure_audit_20260915.json)
- [artifacts/complete_author_charges_20260915.json](../../../../docs/verification/group_1/paper_6f9a36fff6964313/artifacts/complete_author_charges_20260915.json)
- [report/results.json](../../../../docs/verification/group_1/paper_6f9a36fff6964313/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_6f9a36fff6964313/verification_report.md)
- [provenance/analyze_author_charges_20260915.py](../../../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/analyze_author_charges_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- TMTFABA N 的偏差为 0.018695 e，接近容差边界，不能称精确复刻。
- 结果依赖离子对构象和 Mulliken 定义；作者 Gaussian 16 A.03 与实际 C.01 的版本差异保留。
- 三个性质单点在本地完整自然结束，不是只运行了短初始化探针；没有再提交重复 HPC 作业。

## 7. 成功阶段计时

成功 Gaussian 阶段合计 3283.2 s：TFAP 97.6+50.4、PTMA 356.2+128.7、TMTFABA 2370.2+280.1 s。排队和失败尝试不计入。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

已有三体系作者两层级计算证明四电荷和两差值可获得，但不是完整构象/离子对稳健性证明。AR 保留自主覆盖和敏感性评估要求；未实际做的稳健性检查不能因为披露限制而自动得分，也不把单构象链冒充自主 agent 的全流程满分记录。
