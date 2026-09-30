# 已验证成功计算参考 — paper_ffa556cc3acdf0bc / paper_reproduction

整理日期：2026-09-24。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文 PDF p2/Fig.1 碳标签；SI S4 实验、S5/Table S2、S12 方法及 S26–32 构象。

[论文正文](../../../../papers/paper_ffa556cc3acdf0bc/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_ffa556cc3acdf0bc/documents/supplementary_001.pdf)
[补充材料 supplementary_002.pdf](../../../../papers/paper_ffa556cc3acdf0bc/documents/supplementary_002.pdf)

## 2. 真实有效计算流程

1. 任务已限定两个相对构型 candidate_A(8R*) 与 candidate_B(8S*)，各两个 81 原子 C30H45N3O3 中性 singlet 构象。按正文结构图/楔键映射 30 个实验碳，不能用原子顺序猜化学标签。此次公开仅补身份映射，不补 shift/DP4 答案。
2. 四构象各有完整的 M06-2X-D3/def2-SVP 筛查 Opt/Freq 和 B3LYP/6-31G(d) Opt/Freq；八份完整频率均 237 正模。历史验证直接复用已完成的四个 B3LYP 最低点，较晚补齐的 M06 筛查对应相同来源构象族；不是从这些 M06 输出重新串接执行四次 B3LYP 优化。SI S12–13 的作者路线和本段真实执行关系须区分。
3. 在上述四个 B3LYP 最低点上完成 GIAO mPW1PW91/6-311G(d,p)/PCM 13C NMR，逐原子核对其父几何；候选链共十二份有效 native 作业。使用来源图确定的 30 碳映射，按各 B3LYP 电子能在 298.15 K 作 Boltzmann 平均，以自由能 G 权重作对照；SI NMR 段没有唯一指定 E/G。PCM(chloroform) 是结合 CDCl3 实验的验证重建条件，SI Table S2 只明确 PCM，不能伪称原文指定了溶剂。
4. 主分析采用 DP4+ 方法作者 Sarotti-Lab 配套参数库 `data_base_QM.xlsx / CHCl3 / B12`、mPW1PW91/6-311G(d,p)/PCM 对应的 TMS 碳屏蔽标准 **188.48755 ppm**，将屏蔽换算为位移；该标准不是从目标论文位移拟合的答案。另有真实 TMS GIAO 输出 **189.1954 ppm**，其几何仅经 ETKDG/MMFF-UFF 准备、未证实 DFT 最低点，因此只用于敏感性对照，不是主校准。
5. 按 DP4+ 的 Student-t scaled/unscaled likelihood 乘积并在两候选间归一化；主校准下电子能 E 权重的 candidate_B(8S*,9aR*,12aR*)=99.999956799%，candidate_A=.000043201%；G 权重的 candidate_B=99.999937279%。对应 `dp4_results.json.author_standard_computed` 分支，主校准见 `primary_TMS_calibration`；顶层 `computed` 为历史 TMS 的敏感性分支，不混作主结果。主分析与对照的胜者一致。

## 3. 有效产物与原始输入/输出

- [provenance/nmr_subproblem_closure_20260918.json](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/nmr_subproblem_closure_20260918.json)
- [provenance/carbon_mapping_20260918/result.json](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/carbon_mapping_20260918/result.json)
- [provenance/carbon_mapping_20260918/nmr_results.json](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/carbon_mapping_20260918/nmr_results.json)
- [provenance/carbon_mapping_20260918/dp4_results.json](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/carbon_mapping_20260918/dp4_results.json)
- [实际父几何复用关系、主校准和十二项原生计算索引](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/AUTHOR_NMR_CLOSURE_20260918.md)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [hpc_runs/candidate_A_repaired_block1_13c_nmr_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_A_repaired_block1_13c_nmr_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_A_repaired_block1_13c_nmr_hpc20_p6/input.com)
- [hpc_runs/candidate_A_repaired_block1_optfreq_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_A_repaired_block1_optfreq_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_A_repaired_block1_optfreq_hpc20_p6/input.com)
- [hpc_runs/candidate_A_repaired_block2_13c_nmr_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_A_repaired_block2_13c_nmr_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_A_repaired_block2_13c_nmr_hpc20_p6/input.com)
- [hpc_runs/candidate_B_repaired_block1_13c_nmr_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_B_repaired_block1_13c_nmr_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_B_repaired_block1_13c_nmr_hpc20_p6/input.com)
- [hpc_runs/candidate_B_repaired_block2_13c_nmr_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_B_repaired_block2_13c_nmr_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_B_repaired_block2_13c_nmr_hpc20_p6/input.com)
- [hpc_runs/candidate_b_conf1_source_m062x_gd3_screen_20260915_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_b_conf1_source_m062x_gd3_screen_20260915_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/candidate_b_conf1_source_m062x_gd3_screen_20260915_hpc20_p6/input.com)
- [hpc_runs/tetramethylsilane_repaired_13c_nmr_reference_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/tetramethylsilane_repaired_13c_nmr_reference_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/hpc_runs/tetramethylsilane_repaired_13c_nmr_reference_hpc20_p6/input.com)
- [execution_jobs/job_779f60e34931411d9a05fc42109d6675/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/native_workspace_batch/outputs/execution_jobs/job_779f60e34931411d9a05fc42109d6675/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/native_workspace_batch/outputs/execution_jobs/job_779f60e34931411d9a05fc42109d6675/input.com)
- [execution_jobs/job_9ac55284354b4c109e0c993e7f4e4900/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/native_workspace_batch/outputs/execution_jobs/job_9ac55284354b4c109e0c993e7f4e4900/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/native_workspace_batch/outputs/execution_jobs/job_9ac55284354b4c109e0c993e7f4e4900/input.com)
- [execution_jobs/job_b6b1a4ab367a4d20a07d0514754ea3b0/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/native_workspace_batch/outputs/execution_jobs/job_b6b1a4ab367a4d20a07d0514754ea3b0/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/native_workspace_batch/outputs/execution_jobs/job_b6b1a4ab367a4d20a07d0514754ea3b0/input.com)
- [local_stage_tests_20260914/candidate_a_conf1_source_m062x_gd3_screen_20260915/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/local_stage_tests_20260914/candidate_a_conf1_source_m062x_gd3_screen_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/local_stage_tests_20260914/candidate_a_conf1_source_m062x_gd3_screen_20260915/input.com)
- [local_stage_tests_20260914/candidate_a_conf2_source_m062x_gd3_screen_internal_repair_20260918/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/local_stage_tests_20260914/candidate_a_conf2_source_m062x_gd3_screen_internal_repair_20260918/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/local_stage_tests_20260914/candidate_a_conf2_source_m062x_gd3_screen_internal_repair_20260918/input.com)
- [local_stage_tests_20260914/candidate_b_conf2_source_m062x_gd3_screen_internal_repair_20260918/stdout.log](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/local_stage_tests_20260914/candidate_b_conf2_source_m062x_gd3_screen_internal_repair_20260918/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/local_stage_tests_20260914/candidate_b_conf2_source_m062x_gd3_screen_internal_repair_20260918/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_input` | Both candidate geometries are validated as complete C30H45N3O3 neutral singlets and mapped to the 30 carbon shifts. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_compare` | Both named candidates receive comparable 13C predictions and normalized statistical scores. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_result` | The comparative carbon NMR analysis supports the 8S*,9aR*,12aR* candidate. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `c_final` | Within the supplied two-candidate scope, pyrethalkaline A is assigned relative configuration 8S*,9aR*,12aR*. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

这是已给定候选的相对构型 NMR 区分，不要求重现 BALLOON/PM3 全搜索或 ECD/绝对构型。当前 evaluator 不对旧 R² 差异作硬评分。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。
