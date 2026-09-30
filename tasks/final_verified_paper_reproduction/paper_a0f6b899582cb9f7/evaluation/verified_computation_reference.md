# 已验证成功计算链：M3 身份、几何与多极矩

- 论文 ID：`paper_a0f6b899582cb9f7`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1021/acsami.5c26188`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：READY / PASS / QUALIFIED（已纠正 M3 位置异构体身份）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_a0f6b899582cb9f7)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 按 SI Scheme S1 固定 M3 为 2,5-di(thiophen-2-yl)pyrazine，24 原子。正确连接图独立生成三个初始候选；历史错误 2,6/thiophen-3-yl 模型不属于这条有效链。

2. 三个正确身份候选均以 B3LYP/6-31G 气相 Opt/Freq 完成，各 66 实频、0 虚频。按最终电子能选 conf01。

3. 对全部 16 个非氢原子拟合最小二乘平面；以平面法向定义分子外平面 stacking z 轴，提取带索引的 N···S 接触和非平面 RMS。

4. 从同一最终 Gaussian 输出读取偶极与完整原始四极矩张量。保留 Gaussian 原点，只旋转张量到分子坐标系；不把无迹张量或不同原点的数值混入 raw Qzz。

5. 以 D·Å 为四极矩单位，对照 Qzz 的既有 −108.35±5 目标，并结合平面性、偶极抵消和接触结构形成限定结论。

## 3. 实际结果与支持的结论

| 量 | conf01 实算 |
|---|---:|
| 电子能 / Eh | −1367.72389219 |
| 偶极矩 / D | 0.0000（打印精度） |
| 重原子平面 RMS / Å | 0.00025046 |
| N···S / Å | 约 2.99065047 |
| 外平面 raw Qzz / D·Å | −111.07681064 |
| Qzz 与参考的绝对差 / D·Å | 2.72681064，≤5 |

支持该孤立 M3 模型的近平面、偶极抵消及负外平面四极矩描述。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| m3_correct25_conf01_B3LYP631G_20260915 | [input.com](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/qzcli_hpc/m3_correct25_conf01_B3LYP631G_20260915/repair_20260915T080901Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/qzcli_hpc/m3_correct25_conf01_B3LYP631G_20260915/repair_20260915T080901Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| m3_correct25_conf02_B3LYP631G_20260915 | [input.com](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/qzcli_hpc/m3_correct25_conf02_B3LYP631G_20260915/repair_20260915T080956Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/qzcli_hpc/m3_correct25_conf02_B3LYP631G_20260915/repair_20260915T080956Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| m3_correct25_conf03_B3LYP631G_20260915 | [input.com](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/qzcli_hpc/m3_correct25_conf03_B3LYP631G_20260915/repair_20260915T081047Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/qzcli_hpc/m3_correct25_conf03_B3LYP631G_20260915/repair_20260915T081047Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/correct_m3_closure_20260915.json](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/correct_m3_closure_20260915.json)
- [artifacts/correct_identity_multipoles_20260915.json](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/artifacts/correct_identity_multipoles_20260915.json)
- [report/results.json](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/verification_report.md)
- [provenance/analyze_correct_identity_20260915.py](../../../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/analyze_correct_identity_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- N···S 接触不单独证明普适构象锁定机制或器件因果关系。
- 四极矩对原点/张量定义敏感，必须保留本档案中的原点、旋转和 raw 定义。
- 作者正文 Gaussian03、SI Gaussian09 与实际 Gaussian16 C.01 版本不同，不能宣称逐参数完全相同。

## 7. 成功阶段计时

三个成功 Gaussian 计算分别 63.7、61.0、48.4 s，共 173.1 s；本地探针、旧错误模型及失败尝试未计入。

本次归档没有提交、重启或停止任何计算作业。
