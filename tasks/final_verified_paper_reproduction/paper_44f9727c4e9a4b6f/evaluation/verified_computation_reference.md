# 已验证成功计算链：1H Fe 几何、自旋与 Mössbauer

- 论文 ID：`paper_44f9727c4e9a4b6f`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1021/jacs.5c18121`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_6](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_6.md)
- 最新已归档科学状态：complete_validated / QUALIFIED_SCOPED_PASS（ORCA 版本及 Hessian 实现适配已披露）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_44f9727c4e9a4b6f)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 核对 1H 孤立 +2 阳离子为 87 原子、两个 Fe，CPCM 乙腈，无反离子或显式溶剂；保持 Fe1/Fe2 原子映射。本文只有 paper_reproduction 任务，不额外生成不存在的 autonomous 模式。

2. 在 ORCA 6.1.1 使用 TPSSh-D3BJ/ZORA/recontracted def2-TZVP、RIJCOSX/def2-J 先完成 HS 优化/频率，再以高自旋波函数准备反铁磁 broken-symmetry 初猜并完成 BS Opt/Freq。使用各自优化几何的绝热能量比较，不作未执行的自旋投影。

3. 分别核验正常终止、Fe 自旋布居和完整频率表；261 个打印的笛卡尔频率中无虚频，不把 261 全称为正的物理振动模数。BS Fe 自旋异号，S²=4.615067；HS 同号，S²=30.023148。

4. 从 BS 优化几何提取 Fe–Fe 距离；把全部 87 个坐标逐一核对后用于 Mössbauer 单点。该阶段保持 TPSSh-D3BJ/ZORA-def2-TZVP/RIJCOSX，但按 SI S6 切换为 SARC-J、DefGrid3、TightSCF，不沿用几何阶段 def2-J/默认网格。

5. 从成功完整单点的实际输出读取两个 RHO(0)，用 SI 校准 δ=−0.309785357×(ρ₀−13785)+0.325438551 换算 mm/s，不把目标 δ 当作输入密度。

6. 核对 Fe–Fe、两 Fe 位移、HS/BS 能序、负频数及自旋布居；最终逐项覆盖 4 关键点、2 结论、4 数值规则、5 语义规则。仅采用修正后完整 SP，旧错误辅助基组/网格的 SP 不进入有效结果。

## 3. 实际结果与支持的结论

| 量 | 实际值 | 参考/边界 |
|---|---:|---|
| BS Fe–Fe / Å | 3.0864318315 | 3.086 ± 0.08 |
| HS Fe–Fe / Å | 3.00487929 | 比较用 |
| Fe1 / Fe2 ρ₀ / e·bohr⁻³ | 13784.379018901 / 13784.360314861 | 从原始密度读出 |
| Fe1 / Fe2 δ / mm·s⁻¹ | 0.5178094024 / 0.5236036402 | 各 0.52 ± 0.07 |
| E(HS) / Eh | −4466.335137034752 | 分别优化几何 |
| E(BS) / Eh | −4466.361419838267 | 分别优化几何 |
| E(BS)−E(HS) | −0.026282803515 Eh ≈ −16.4927082 kcal/mol | BS 较低 |
| Fe 自旋布居 HS / BS | +4.051781,+4.055072 / −3.866589,+3.874236 | 反铁磁 BS 非纯 singlet |

支持既定模型内的反铁磁 diferric μ-1,2-peroxo 1H 指认。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| high_spin | [input.inp](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/native_workspace/1H_high_spin_optfreq_retry3/outputs/execution_jobs/job_c081d45d3edd4514b5997f0058b85fac/input.inp) | [stdout.log](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/native_workspace/1H_high_spin_optfreq_retry3/outputs/execution_jobs/job_c081d45d3edd4514b5997f0058b85fac/stdout.log) | ORCA 正常终止标记 1 处；有优化收敛标记 |
| broken_symmetry | [input.inp](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/qzcli_hpc/1H_broken_symmetry_from_high_spin_optfreq_hpc/1_20260905T055531Z_265/input.inp) | [orca_stdout.log](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/qzcli_hpc/1H_broken_symmetry_from_high_spin_optfreq_hpc/1_20260905T055531Z_265/orca_stdout.log) | ORCA 正常终止标记 1 处；有优化收敛标记 |
| corrected_mossbauer | [input.inp](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/local_orca_sp_stability_20260914T130203Z/1H_mossbauer_SARCJ_DefGrid3_warm_restart/input.inp) | [stdout.log](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/local_orca_sp_stability_20260914T130203Z/1H_mossbauer_SARCJ_DefGrid3_warm_restart/stdout.log) | ORCA 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/FE_ROUTE_AND_CLOSURE_20260915.md](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/FE_ROUTE_AND_CLOSURE_20260915.md)
- [provenance/corrected_mossbauer_evidence_20260915.json](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/corrected_mossbauer_evidence_20260915.json)
- [provenance/evaluator_crosscheck_20260915.json](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/evaluator_crosscheck_20260915.json)
- [report/results.json](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/report/results.json)
- [verification_report.md](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/verification_report.md)
- [prepare_bs_from_high_spin.py](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/prepare_bs_from_high_spin.py)
- [prepare_mossbauer_author_sp_repair.py](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/prepare_mossbauer_author_sp_repair.py)
- [close_corrected_mossbauer.py](../../../../docs/verification/group_6/paper_44f9727c4e9a4b6f/close_corrected_mossbauer.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 作者 ORCA 5.0.4，本次 6.1.1；作者数值频率，本次解析 Hessian，是明确记录的实现适配，不称为同版本 strict replay。
- BS 为有自旋污染的开放壳层行列式，未做自旋投影；局部最小值检验不证明全局最低点。
- 不验证整篇形成机制、XAS、UV–vis 或完整反应动力学。公开 mossbauer_protocol.json 是方法/校准常数，不应含目标密度和目标位移。
- 完整正确 SP 实际已本地成功结束；其目录含 stability 不是缩短参数的试算，也不虚构另一份 HPC 重跑。

## 7. 成功阶段计时

HS、BS、修正 SP 成功阶段分别为 68772.8319、167897、1125.065 s；不纳入旧失败、测试和排队时间，也不将阶段和视作日历工期。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

历史作者 Table S10 终态仅存 author_results/1H_start.xyz；当前独立 topology-only starter 明确区分 O3–O4 过氧与 O5 μ-oxo，并排除不合理短的非键合 O···O。保留已验证的 BS/HS、Fe···Fe 和 Mössbauer 计算及校准协议；没有重算新起点，也没有把构建几何写成已收敛结构。
