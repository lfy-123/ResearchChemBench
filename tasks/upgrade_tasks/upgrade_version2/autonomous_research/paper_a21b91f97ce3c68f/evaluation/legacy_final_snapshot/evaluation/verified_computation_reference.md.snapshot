# 已验证成功计算参考 — paper_a21b91f97ce3c68f / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文与 SI S2 方法、S5 理论 J、S10–11 的 1a 坐标。

[论文正文](../../../../papers/paper_a21b91f97ce3c68f/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_a21b91f97ce3c68f/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 给定 axial-1a，完整 62 原子中性 singlet；任务本来就是该对象的 Sn–C coupling，几何不是待发现的答案。Gaussian16 B3LYP-GD3/def2TZVPP 气相 Opt/Freq，180 正频，最低 14.6467 cm⁻¹。
2. 配对该最低点和 NMR 输入/输出，保留原子顺序，Sn index1、butyl carbon indices2/3/7。B3LYP-GD3/TZP-ZORA，NMR=(SpinSpin,Mixed,ReadAtoms)，Integral=NoXCTest，指定 119Sn/13C。TZP-ZORA 是基组名，不据此虚称 Gaussian 启用了 ZORA Hamiltonian。
3. 从 FC+SD+PSO+DSO 的完整 signed J 提取 −249.688、−223.744、−205.060 Hz，算术均值 −226.164 Hz；与理论 −217±15 Hz 比较，不取绝对值、不乘作者面向实验的经验校准因子。
4. 三个键距离约 2.1844/2.1891 Å 等身份/几何数据和 native NMR isotopes、分量表作为过程证据；该单结构链不证明整个 axial/equatorial 系列或 NBO 因果。

## 3. 有效产物与原始输入/输出

- [provenance/sn_coupling_closure_20260918.json](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/sn_coupling_closure_20260918.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [local_stage_tests_20260914/compound_1a_computed_parent_tzp_zora_sn119_c13_spinspin_20260916/stdout.log](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_computed_parent_tzp_zora_sn119_c13_spinspin_20260916/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_computed_parent_tzp_zora_sn119_c13_spinspin_20260916/input.com)
- [local_stage_tests_20260914/compound_1a_full62_si_optfreq_20260915/stdout.log](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_full62_si_optfreq_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/local_stage_tests_20260914/compound_1a_full62_si_optfreq_20260915/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_ar_process_minimum` | The final reported geometry is checked for stationarity and the report states the imaginary-frequency evidence. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_process_pairs` | The three Sn–butyl carbon pairs are identified explicitly from the final geometry and retained with per-pair context. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_result_mean` | The submission reports the signed average one-bond 119Sn–13C_Bu coupling for the supplied structure in Hz. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `c_ar_final` | The validated calculation yields a defensible signed average Sn–C_Bu coupling, and any electronic-structure interpretation is presented as an inference bounded by the single-system calculation. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

不新增 equatorial/NBO 必评工作；保留当前 signed-mean 科学目标。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。
