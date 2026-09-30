# 已验证成功计算参考 — paper_e0791c047a731974 / paper_reproduction

整理日期：2026-09-24。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文 PDF pp5–6；SI PDF p7 方法、p12/Table S3、p24 Se 基组。

[论文正文](../../../../papers/paper_e0791c047a731974/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_e0791c047a731974/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_e0791c047a731974/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 完整 Cy2 阳离子 +1 singlet、去 iodide 的分子边界，给定几何用于电子态性质。Gaussian16 B3LYP/6-31G(d,p)(CHNO)+def2TZVP(Se)/SMD(chloroform) S0 Opt/Freq，180 正频。
2. 以同一 S0 geometry 分别计算六 singlet 与六 triplet TD roots，核对 singlet S²=0、triplet S²=2：vertical S1=1.8909、T1=1.0555、T2=2.1220 eV。
3. 实际验证使用 singlet reference 的 TD(Triplets,NStates=6,Root=1) T1 Opt/Freq，180 正频；以最低 triplet 身份和收敛总 excited-state energy 减 S0 electronic energy 得 adiabatic T1=1.010301083 eV。不是 T1 geometry 的 SCF-only 能量差，也没有加入 ZPE/G。
4. 从上述既有垂直能量直接相减，S1−T1=.8354 eV、T2−S1=.2311 eV，态序为 T1<S1<T2；这是数值后处理，不是新增电子结构计算。历史记录另列 Cy2 的 2T1−S1=.2201 eV，但正文 PDF p6 的 2T1>S1 条件针对 rubrene 湮灭剂，不能据 Cy2 此差值验证 rubrene 条件或增强 SOC/ISC。当前结论采用四能量、态序和垂直能隙证据。

## 3. 有效产物与原始输入/输出


下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/input.com)
- [local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/input.com)
- [local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/input.com)
- [local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stdout.log](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `pr_p1` | The submitted investigation identifies the supplied Cy2 cation geometry, charge +1, singlet starting state and omission of iodide counterions, and provides auditable S0 stationarity/frequency evidence. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_p2` | The calculation distinguishes vertical S1/T1/T2 states from a relaxed T1 state and documents state multiplicity and convergence. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_r1` | Cy2 vertical energies are approximately S1 1.8909 eV, T1 1.0556 eV and T2 2.1221 eV under the published computational framework. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_r2` | The published Cy2 relaxed T1 adiabatic energy is 1.09 eV. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `pr_c1` | The validated Cy2 calculations determine the vertical S1/T1/T2 ordering and separations together with the relaxed T1 adiabatic energy, supporting a state-energetic interpretation relevant to triplet sensitization. | 四个已有能量、态身份、收敛及上述直接相减支持；不把 Cy2 差值当成 rubrene 的判据，也不将能级解释写成 SOC/ISC 因果已验证。 |

## 5. 不能扩大解释的地方

作者 relaxed T1 为 UDFT，而有效验证为 triplet-response TD 路线。方法开放的当前任务可用此证据；不能写成两实现完全相同。不额外要求未验证 SOC/速率计算。原 group results.json 的 conclusion 曾将 Cy2 的 2T1>S1 与 sensitizer 可行性并列；该历史解释不再用作当前结论的证明，原文件保持只读。修正的是解释对象，不是原能量、容差或计算有效性；也不新增 limitation 声明得分。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。
