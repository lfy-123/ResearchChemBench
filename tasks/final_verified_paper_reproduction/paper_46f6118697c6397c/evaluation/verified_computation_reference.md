# 已验证成功计算链：compound 2 三分支 TD50

- 论文 ID：`paper_46f6118697c6397c`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1039/d5dt02896e`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_2](../../../../docs/verification/group_2/paper_46f6118697c6397c)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_2.md)
- 最新已归档科学状态：作者路线完成，三条 CIF 派生分支及 evaluator 数值/跃迁指认审计通过。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_46f6118697c6397c)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 从 CCDC 2512981 的 compound 2 CIF 出发，按预处理档案执行对称性展开（含 2_655/5 对称操作）并分别处理无序，得到 B1_op2、B2_A_op5、B2_B_op5 三条分支；补氢后各为完整 68 原子 C18H14B2F12N6O12S4、中性单重态，保留四个 triflate 配体，不能将无序分支错误拼接或删去配体。

2. 使用 Gaussian 16 C.01，在 B3LYP-D3(BJ)/6-31+G(d)、SMD 二氯甲烷下分别执行三分支 Opt/Freq。三条均正常终止，各有 198 实频、0 虚频。

3. 将每条真实优化末态逐一用于同方法/溶剂的 TD-DFT 50 singlets 计算，保留所有状态的能量、振子强度和主要轨道展开。

4. 三分支最大振子强度均位于第 5 单重激发态。历史报告在三条分支中选择第 5 态能量最低的 B2_A_op5 作代表；这是当时的报告选择，不是当前 task 强制的筛选规则。三分支的该态能量和强度均在现行容差内，也不意味着 B2_A_op5 的基态电子能全局最低。

5. 读取所选第 5 态的 217→222 主贡献（系数 0.70257，当前编号对应 HOMO−4→LUMO），结合归档轨道分析给出 N6 相关近紫外跃迁指认，逐项对照参考能量/强度、关键点和结论。

## 3. 实际结果与支持的结论

| 分支 | 第 5 态能量 / eV | 振子强度 f |
|---|---:|---:|
| B1_op2 | 3.8445 | 0.4733 |
| B2_A_op5（代表） | 3.8138 | 0.4255 |
| B2_B_op5 | 3.8208 | 0.4292 |
| evaluator 参考 | 3.8436 ± 0.15 | 0.4243 ± 0.05 |

代表分支误差为 0.0298 eV、0.0012；支持任务所需 compound 2 主导近紫外激发及其跃迁指认；第 5 态是本方法三分支中实际得到的编号，不是对任意程序/方法强加的固定序号。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| compound2_B1_op2_optfreq | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/compound2_B1_op2_optfreq_local_migration_20260904T155532Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/compound2_B1_op2_optfreq_local_migration_20260904T155532Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_compound2_B2_A_op5_b3lyp_d3bj_631pgd_optfreq | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260905T022637Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260905T022637Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_compound2_B2_B_op5_b3lyp_d3bj_631pgd_optfreq | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260904T223914Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260904T223914Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_compound2_B1_op2_td50 | [input.com (1)](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| author_compound2_B2_A_op5_td50 | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_td50_hpc20_20260910T022113Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_td50_hpc20_20260910T022113Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| author_compound2_B2_B_op5_td50 | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_td50_hpc20_20260910T022118Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_td50_hpc20_20260910T022118Z/stdout.log) | Gaussian 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_route_evaluation_audit.json](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/author_route_evaluation_audit.json)
- [provenance/compound2_cif_preprocessing.json](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/compound2_cif_preprocessing.json)
- [report/results.json](../../../../docs/verification/group_2/paper_46f6118697c6397c/report/results.json)
- [verification_report.md](../../../../docs/verification/group_2/paper_46f6118697c6397c/verification_report.md)
- [provenance/prepare_compound2_from_cif.py](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/prepare_compound2_from_cif.py)
- [provenance/advance_46_tddft.py](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/advance_46_tddft.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- CIF 对称展开和无序处理是验证流程的必要步骤，不能把晶体中不完整 asymmetric unit 直接当作完整计算分子。
- 基态局部极小值、有限三分支与溶液连续介质模型不等于晶体堆积/全构象空间验证。
- 轨道绝对编号随程序/模型变化，评价应保留轨道性质与 HOMO−4→LUMO 映射，不把 217/222 当通用常数。

## 7. 成功阶段计时

六条成功 Opt/Freq/TD 作业的逐项时间可在原始日志及 HPC 摘要中查询；不把平台汇总时间直接称作应用 CPU 时间。

本次归档没有提交、重启或停止任何计算作业。

## Evidence scope review (2026-09-19)

The recorded excitation energy, oscillator strength and configurations support the scalar results. Complete coverage of the N6-localization assertion additionally requires retrievable same-state spatial/population evidence. An MO number is not such evidence. This revision does not certify that missing assertion or rerun TD calculations.
