# 已验证成功计算参考 — paper_c28b0a1c549f4575 / paper_reproduction

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文 PDF pp3–4/Fig.2；历史验证索引 SI §5 路线，本地 SI 原件未取得，不冒称本轮直接核对原件。

[论文正文](../../../../papers/paper_c28b0a1c549f4575/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/report/results.json)。

## 2. 真实有效计算流程

1. 四个完整分子图（DED2²⁺、TEA⁺、BF4⁻、PC），三种 ion–PC 对，每对两个独立初始方向。先气相 B3LYP-D3BJ/def2-SVP Opt/Freq：四单体和六复合物，共十个最低点前驱。
2. 六复合物按映射检查初始方向区别、终态去重、频率和 parent→SP 坐标一致。随后十个 B3LYP/6-311+G(2d,p) 气相电子单点，不能用 SP 正常结束代替 parent 最低点验证。
3. Ebind=Ecomplex−Eion−EPC，同一单体 convention，×627.509474 kcal/mol/Eh。两方向区间：DED2_PC [−30.088727,−29.647527]；TEA_PC [−13.187403,−12.821987]；BF4_PC [−16.540811,−16.539528]。
4. 替代方向是真实敏感性对照，最弱 DED2 仍比最强 TEA 更负。结论是孤立电子结合能排序，不等同体相溶剂自由能。

## 3. 有效产物与原始输入/输出

- [provenance/binding_progress_20260916/results.json](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/binding_progress_20260916/results.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/hpc_runs/tea_pc_a_source_bestgradient_internal_optfreq_20260916_hpc20_p6/input.com)
- [execution_jobs/job_28cdaf0cae20404dbf3f940e50074422/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_28cdaf0cae20404dbf3f940e50074422/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_28cdaf0cae20404dbf3f940e50074422/input.com)
- [execution_jobs/job_33c5aa59eb6f4886b5fc50c54d0a2ef0/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_33c5aa59eb6f4886b5fc50c54d0a2ef0/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_33c5aa59eb6f4886b5fc50c54d0a2ef0/input.com)
- [execution_jobs/job_36c9fefc561e4d4589a66716cddf72ab/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_36c9fefc561e4d4589a66716cddf72ab/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_36c9fefc561e4d4589a66716cddf72ab/input.com)
- [execution_jobs/job_5fbb4248998841a9808963257d3f6182/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_5fbb4248998841a9808963257d3f6182/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_5fbb4248998841a9808963257d3f6182/input.com)
- [execution_jobs/job_716585773558490d9262333e55c3314f/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_716585773558490d9262333e55c3314f/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_716585773558490d9262333e55c3314f/input.com)
- [execution_jobs/job_7a5016db085b41d99ea79a0638186dff/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7a5016db085b41d99ea79a0638186dff/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7a5016db085b41d99ea79a0638186dff/input.com)
- [execution_jobs/job_7b1fb25d5e7d4d458e1ccd8fe9ec817a/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7b1fb25d5e7d4d458e1ccd8fe9ec817a/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_7b1fb25d5e7d4d458e1ccd8fe9ec817a/input.com)
- [execution_jobs/job_979fd675c06f4e57bb3b328ad15edba2/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_979fd675c06f4e57bb3b328ad15edba2/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_979fd675c06f4e57bb3b328ad15edba2/input.com)
- [execution_jobs/job_f0d22d8cee914269b8a5b650e460af56/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_f0d22d8cee914269b8a5b650e460af56/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/native_workspace_batch/outputs/execution_jobs/job_f0d22d8cee914269b8a5b650e460af56/input.com)
- [local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_a_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_pc_b_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/bf4_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/bf4_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_a_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_pc_c_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/ded2_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/ded2_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/pc_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/pc_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/pc_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_a_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_pc_b_source_binding_sp_20260915/input.com)
- [local_stage_tests_20260914/tea_source_binding_sp_20260915/stdout.log](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_source_binding_sp_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_c28b0a1c549f4575/provenance/local_stage_tests_20260914/tea_source_binding_sp_20260915/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `pr_kp_process_minima` | Each named ion-PC pair is represented by independently optimized, validated retained minima from multiple starting orientations. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_kp_process_energy` | Binding energies use consistent monomer/complex bookkeeping and a declared sign convention. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_kp_result_order` | The computed DED2+-PC pair is stronger-binding than TEA+-PC. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_c_final` | The isolated-pair calculations support the authors' competitive PC-sequestration hypothesis. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

AR 额外路线构思字段不在共享历史报告中，软件回归仅标明该差异，不能补造当时自主发现轨迹。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。
