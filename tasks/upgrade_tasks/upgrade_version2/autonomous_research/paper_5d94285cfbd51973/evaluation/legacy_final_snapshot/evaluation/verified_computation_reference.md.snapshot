# 已验证成功计算链：AZ9 九构象电子描述符

- 论文 ID：`paper_5d94285cfbd51973`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1002/slct.202505650`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_4](../../../../docs/verification/group_4/paper_5d94285cfbd51973)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_4.md)
- 最新已归档科学状态：READY / PASS / MATCH / QUALIFIED（AZ9 气相描述符及有限构象范围）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_autonomous_research`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_5d94285cfbd51973)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 确认 AZ9 为 C23H23ClN4O2、53 原子中性单重态。用 ETKDG/MMFF94s 生成候选，档案包含 12 轮及 611 个池内构象；TFD/Butina 截止 0.03 聚成 9 个盆地，盆地数自第 3 轮后稳定。该有限饱和记录不等于穷尽全局构象空间。

2. 每个盆地各选一个代表，独立执行作者主层级 Gaussian 16 B3LYP/6-31G(d) 气相 Opt/Freq。九条均正常终止，分子图均为 AZ9，每条 153 实频、0 虚频。

3. 从九个主层级末态电子能选出 basin04，E = −1719.93864109 Eh；不按 MMFF 排名或与目标数值的接近程度选择。

4. 从所选主层级波函数提取 HOMO、LUMO、能隙和偶极矩；按任务公式推导 IP=−HOMO，EA=−LUMO，η=(LUMO−HOMO)/2，S=1/(2η)，μ_chem=(HOMO+LUMO)/2，χ=−μ_chem，ω=μ_chem²/(2η)。

5. 九条作业均包含同几何 B3LYP/6-311+G(d,p) linked SP；将所选 basin04 的大基组结果作为敏感性检查，与主层级数值分开报告，不用敏感性层级替换评分层级。

6. 对主量、派生量、结构身份、有限搜索停止依据与结论逐项核对 evaluator；明确区分论文 SI 的非常规化学势/亲电指数公式与任务公开的常规公式。

## 3. 实际结果与支持的结论

| 主层级量 | 计算值 | evaluator 参考 |
|---|---:|---:|
| HOMO / eV | −5.5913956458 | −5.5758 ± 0.35 |
| LUMO / eV | −1.1698174947 | −1.1556 ± 0.35 |
| gap / eV | 4.4215781511 | 4.4202 ± 0.35 |
| 偶极矩 / D | 6.0404 | 5.847 ± 1.0 |

派生量：IP=5.5913956 eV，EA=1.1698175 eV，η=2.2107891 eV，S=0.226163593 eV⁻¹，μ_chem=−3.38060657 eV，χ=3.38060657 eV，ω=2.5847108 eV。

大基组减主层级：ΔHOMO=−0.3496663 eV，ΔLUMO=−0.4106198 eV，Δgap=−0.0609535 eV，Δdipole=+0.3157 D。描述符在既定模型内支持任务比较，不能单独证明生物活性。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| az9_tfd_basin_01 Opt/Freq + SP | [input.com (1)](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_01_optfreq_hpc20/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_01_optfreq_hpc20/source_input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_01_optfreq_hpc20/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_02 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_02_optfreq_larger_basis_sp_hpc20_p3/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_02_optfreq_larger_basis_sp_hpc20_p3/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_03 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_03_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_03_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_04 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_04_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_04_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_05 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_05_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_05_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_06 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_06_optfreq_larger_basis_sp_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/hpc_runs/az9_tfd_basin_06_optfreq_larger_basis_sp_hpc20_p6/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_07 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_03d6a2def6f24a09be35908207102514/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_03d6a2def6f24a09be35908207102514/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_08 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_641925d42de64bb9b98c1d9a7fbea070/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_641925d42de64bb9b98c1d9a7fbea070/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |
| az9_tfd_basin_09 Opt/Freq + SP | [input.com](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_d00eed6e3253451dae3ff6e77d29a36a/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_5d94285cfbd51973/native_workspace_batch/outputs/execution_jobs/job_d00eed6e3253451dae3ff6e77d29a36a/stdout.log) | Gaussian 正常终止标记 3 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_descriptor_closure_20260914.json](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/author_descriptor_closure_20260914.json)
- [provenance/evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/evaluation_task_qualification.json)
- [report/results.json](../../../../docs/verification/group_4/paper_5d94285cfbd51973/report/results.json)
- [verification_report.md](../../../../docs/verification/group_4/paper_5d94285cfbd51973/verification_report.md)
- [provenance/generate_az9_conformer_ensemble.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/generate_az9_conformer_ensemble.py)
- [provenance/cluster_az9_tfd_ensemble.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/cluster_az9_tfd_ensemble.py)
- [provenance/prepare_az9_dft_specs.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/prepare_az9_dft_specs.py)
- [finalize_author_descriptors_20260914.py](../../../../docs/verification/group_4/paper_5d94285cfbd51973/finalize_author_descriptors_20260914.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- SI 非常规公式与任务常规公式的区别需要保留；没有通过换公式、改容差来迎合原目标。
- 九个盆地给出有限候选集合内的最低点证据，不声称数学上的全局最低点或真实溶液种群。
- 抗菌、ADMET、docking 及完整药理结论不属于此计算链的验证范围。

## 7. 成功阶段计时

六组成功 HPC 使用 20 CPU，三组成功 native 使用 1 CPU。成功日志累计 CPU 251821.2 s（69.9503 核时），wall 1048282.3 s（291.1895 h）；并行作业 wall 之和不是日历工期。

本次归档没有提交、重启或停止任何计算作业。
