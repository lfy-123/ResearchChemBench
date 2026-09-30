# 已验证成功计算参考 — paper_9455a82229de2427 / paper_reproduction

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 1）

正文 PDF pp3–5、SI PDF p3，CBS-QB3/0 K 反应能和原子 H 损失通道。

[论文正文](../../../../papers/paper_9455a82229de2427/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_1/paper_9455a82229de2427/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_9455a82229de2427/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. SiN 中性 doublet、isoprene 中性 singlet 和原子 H doublet 分开计算；最终有效链采用独立图构建的两个 14 原子 SiNC5H7 singlet 六元环候选，不采用早期 SI 产物作为这条链的输入。
2. Gaussian16 CBS-QB3 优化/频率及完整复合能步骤：SiN 1 个正频、isoprene 33 个正频、每个产物 36 个正频；产物最低频率分别 118.4519 和 84.6768 cm⁻¹，图连接在优化前后不变。
3. 使用已含 ZPE 的 CBS-QB3(0 K)：SiN −343.624010、isoprene −194.897942、H −0.499818 Eh；两产物 −538.079465 和 −538.081724 Eh。ΔE0=[E0(product)+E0(H)−E0(SiN)−E0(isoprene)]×2625.499638，得到 −150.52251975 与 −156.45352343 kJ/mol，均位于实验 −162±27 的窗口。
4. 两独立产物的身份、最低点和热化学支持当前产物兼容性目标。此链没有 TS/IRC/PES 连接，不将能量兼容性写成分支比或反应路径已证明。

## 3. 有效产物与原始输入/输出

- [provenance/independent_cbs_raw_audit_20260918.json](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/independent_cbs_raw_audit_20260918.json)
- [provenance/independent_cbs_closure_audit_20260918.json](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/independent_cbs_closure_audit_20260918.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [execution_jobs/job_a50efe6b34614f4586674f56311b3659/stdout.log](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a50efe6b34614f4586674f56311b3659/stdout.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a50efe6b34614f4586674f56311b3659/input.com)
- [execution_jobs/job_a900b32bde494cb09e422e5eb6ff4f0d/stdout.log](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a900b32bde494cb09e422e5eb6ff4f0d/stdout.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/native_workspace_batch/outputs/execution_jobs/job_a900b32bde494cb09e422e5eb6ff4f0d/input.com)
- [local_recovery_20260916/atomic_H_CBSQB3_reference_20260916/gaussian.log](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/local_recovery_20260916/atomic_H_CBSQB3_reference_20260916/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/local_recovery_20260916/atomic_H_CBSQB3_reference_20260916/input.com)
- [public_ring_orientation_1_CBSQB3_20260916/repair_20260918T035154Z/gaussian.log](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_1_CBSQB3_20260916/repair_20260918T035154Z/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_1_CBSQB3_20260916/repair_20260918T035154Z/input.com)
- [public_ring_orientation_2_CBSQB3_20260916/repair_20260918T035249Z/gaussian.log](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_2_CBSQB3_20260916/repair_20260918T035249Z/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_9455a82229de2427/provenance/qzcli_hpc/public_ring_orientation_2_CBSQB3_20260916/repair_20260918T035249Z/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `pr_process_validation` | Each advanced candidate is uniquely identified and its optimized stationary point is validated as a minimum or transition state using frequency evidence; claimed TS connectivity is checked. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_product_identity` | The investigation identifies neutral singlet SiNC5H7 cyclic product structures among the validated candidates. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_energy_compatibility` | The cyclic product reaction energies are compatible with the experimental atomic-H-loss exoergicity window. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_final_conclusion` | The independently validated cyclic candidates provide computational support for the authors' qualitative terminal-addition/cyclization hypothesis, while energetic agreement supports compatibility with the observed channel rather than a measured branching ratio. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

公开新增的是实验比较窗口和反应能定义，不是产物几何/计算答案；共享作者知情验证不等同 AR 盲测。历史字段 atomic_H_product_energy_hartree 在私有契约检查中无损映射为 h_energy_hartree。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。
