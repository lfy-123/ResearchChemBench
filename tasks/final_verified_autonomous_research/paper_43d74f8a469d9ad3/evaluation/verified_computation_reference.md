# 已验证成功计算参考 — paper_43d74f8a469d9ad3 / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 1）

正文 PDF pp7/11，计算方法 §3.5；本地未取得 SI 原件，不能声称逐页核验 SI。

[论文正文](../../../../papers/paper_43d74f8a469d9ad3/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/report/results.json)。

## 2. 真实有效计算流程

1. 输入为实验 CCDC 2441197 的完整 48 原子中性单重态，先以 Gaussian16/PBE0(definition PBE1PBE)/def2-SVP 优化和频率验证；138 个正频，最低 12.7931 cm⁻¹。不是从一份正常单点推断其前驱已收敛。
2. 以 N1–B1–C1–C2 = 2,4,3,6 的固定映射定义 B–ipso-aryl 扭角，整支 17 原子芳基绕 B–C 轴刚性旋转。生成 0…345°、步长 15° 的 24 点，每点同水平电子单点，不作松弛扫描。
3. 所有 24 点正常终止；Erel=(Ei−Emin)×2625.499638 kJ/mol。315° 最低，210° 最高，采样势垒 18.2665461617 kJ/mol。360° 坐标回闭误差 8.88e−16 Å；345°→0° 能差 4.47537417 kJ/mol，不要求 E345=E0，也未额外算 360°。
4. 以势能曲线讨论旋转的空间位阻；该有限基态扫描不计算光漂白速率。

## 3. 有效产物与原始输入/输出

- [provenance/torsion_current_contract_audit_20260921.json](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/torsion_current_contract_audit_20260921.json)
- [artifacts/absolute_torsion_profile_20260916.json](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/artifacts/absolute_torsion_profile_20260916.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [gaussian_batch/cif_2441197_pbe1pbe_local_cpu20_retry_hpc_7868e4a7/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/artifacts/gaussian_batch/cif_2441197_pbe1pbe_local_cpu20_retry_hpc_7868e4a7/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/artifacts/gaussian_batch/cif_2441197_pbe1pbe_local_cpu20_retry_hpc_7868e4a7/input.com)
- [local_recovery_20260915/compound1_abs_torsion_000_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_000_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_000_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_015_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_015_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_015_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_030_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_030_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_030_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_045_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_045_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_045_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_060_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_060_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_060_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_075_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_075_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_075_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_090_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_090_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_090_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_105_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_105_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_105_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_120_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_120_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_120_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_135_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_135_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_135_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_150_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_150_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_150_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_165_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_165_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_165_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_180_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_180_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_180_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_195_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_195_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_195_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_210_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_210_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_210_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_225_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_225_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_225_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_240_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_240_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_240_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_255_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_255_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_255_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_270_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_270_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_270_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_285_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_285_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_285_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_300_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_300_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_300_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_315_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_315_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_315_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_330_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_330_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_330_PBE1PBE_20260915/input.com)
- [local_recovery_20260915/compound1_abs_torsion_345_PBE1PBE_20260915/gaussian.log](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_345_PBE1PBE_20260915/gaussian.log)；[input.com](../../../../docs/verification/group_1/paper_43d74f8a469d9ad3/provenance/local_recovery_20260915/compound1_abs_torsion_345_PBE1PBE_20260915/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `ar_process_identity` | The submission keeps one unambiguous B–ipso-aryl torsion atom definition and consistent mapping across all scan points. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_process_coverage` | The scan covers 0 through 345 degrees at 15-degree increments, references energies to the minimum, and checks periodic continuity. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_result_profile` | The resulting E(theta) profile is a torsional electronic-energy profile for ester 1, not a solution photobleaching rate. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_result_interpretation` | The profile is interpreted as evidence about rotational resistance only within the selected computational model. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_final_conclusion` | The computed profile gives a bounded ground-state electronic test of torsional resistance in ester 1. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

数值是当前刚性扫描结果，不把采样最低角宣称为任意方法的唯一极小点。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。
