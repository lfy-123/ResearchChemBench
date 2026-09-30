# 已验证成功计算链：isoxazole 1a 五候选轨道

- 论文 ID：`paper_5ea491c741fbd8d4`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1016/j.molstruc.2026.145359`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：READY / PASS / QUALIFIED（当前 base reproduction、有限五候选）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_5ea491c741fbd8d4)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 固定 isoxazole 1a 的 E 化学身份；保留原候选以及种子 101、202、303、404 的四个补充构象，共五个 27 原子候选。

2. 五个候选均按 Gaussian B3LYP/6-311+G(d,p) 气相 Opt/Freq 完成；各有 75 个实频、0 虚频，并由最终几何复核 E 构型。

3. 采用分子图/对称性一致的重原子刚性对齐 RMSD 去重，不允许镜像；修正历史质心对齐错误后得到三组结构，全部五个成功候选仍保留。

4. 从各最终 SCF 本征值提取 HOMO、LUMO 并换算 eV；依最低打印电子能选 seed303，而不是依与参考值的接近程度挑选。由五候选 gap 范围评估构象敏感性。

5. 报告 Kohn–Sham 前线能级、能隙及有限气相模型下的描述符结论，对照原 evaluator 的三项数值目标。

## 3. 实际结果与支持的结论

| 量 | 选中 seed303 的实算值 |
|---|---:|
| 电子能 / Eh | −744.463909848 |
| HOMO / eV | −6.563930590 |
| LUMO / eV | −2.883862714 |
| HOMO–LUMO gap / eV | 3.680067876 |
| 五候选 gap 最大−最小 / eV | 0.001360569 |

HOMO/LUMO 与参考偏差约 0.227731/0.166763 eV，均在原 ±0.35 eV 容差内；能隙也通过原规则。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| isoxazole_b3lyp_optfreq | [input.com](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_b3lyp_optfreq/input.com) | [stdout.log](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_b3lyp_optfreq/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| isoxazole_conf_seed101_b3lyp_optfreq | [input.com](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed101_b3lyp_optfreq/input.com) | [stdout.log](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed101_b3lyp_optfreq/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| isoxazole_conf_seed202_b3lyp_optfreq | [input.com](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed202_b3lyp_optfreq/input.com) | [stdout.log](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed202_b3lyp_optfreq/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| isoxazole_conf_seed303_b3lyp_optfreq | [input.com](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed303_b3lyp_optfreq/input.com) | [stdout.log](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed303_b3lyp_optfreq/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| isoxazole_conf_seed404_b3lyp_optfreq | [input.com](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed404_b3lyp_optfreq/input.com) | [stdout.log](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/gaussian_batch/isoxazole_conf_seed404_b3lyp_optfreq/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/orbital_closure_audit_20260915.json](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/provenance/orbital_closure_audit_20260915.json)
- [artifacts/author_orbitals_20260915.json](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/author_orbitals_20260915.json)
- [report/results.json](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/verification_report.md)
- [provenance/analyze_author_orbitals_20260915.py](../../../../docs/verification/group_1/paper_5ea491c741fbd8d4/provenance/analyze_author_orbitals_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 三个低能 seed 候选几乎简并；“最低”只指已计算集合及打印精度，不代表唯一全局最低构象。
- 能隙是该模型的轨道差，不是实测光学/基本带隙，也不证明生物活性、稳定性或电荷转移速率。
- 保留 Gaussian09/16 版本差异；不把本次归档表述为新增计算或自主 agent 回放。

## 7. 成功阶段计时

五个成功 Gaussian 阶段合计 173520.3 s（48.20 h），包含并行。历史约 50 h 的日历执行窗口是另一口径，不与阶段时间相加。

本次归档没有提交、重启或停止任何计算作业。
