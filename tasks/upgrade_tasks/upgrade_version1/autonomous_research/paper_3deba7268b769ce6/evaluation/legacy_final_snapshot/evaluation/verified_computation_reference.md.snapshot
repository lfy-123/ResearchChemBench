# 已验证成功计算参考 — paper_3deba7268b769ce6 / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 5）

正文 PDF p4 Dye3 的59.44 kcal/mol；不能把 SI 中另一个 dye 的同数值当身份依据。

[论文正文](../../../../papers/paper_3deba7268b769ce6/documents/main.pdf)；[当前成功结果与证据索引](../../../../runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_3deba7268b769ce6/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 校准完整 Dye3 身份 C17H11N2O3S−、34 原子、E-imine、charge−1/singlet。五个 MMFF seeds 中选 seed2 再进 quantum；只一条完整 DFT 链，不伪称五构象都已 DFT 优化。
2. ORCA6.1.1 r2SCAN-3c/RI/CPCM Opt+Freq，102 modes=6 zeros+96 positive，最低8.08 cm⁻¹；原子连接与扭角判定来自终态，不从文件名判定。
3. 终态进行 full TDDFT ωB97X-D4/def2-TZVP/def2-J/RIJCOSX/CPCM，十 singlet roots，保存 NTO。按最低能可见态及电子性质选择 S1，不按与59.44的距离筛选：2.471173 eV=56.986603 kcal/mol、501.7 nm、f=1.815683526。
4. NTO/电子空穴片段支持 donor→nitrothiophene ICT，particle bridge≈.483、acceptor≈.369，不能设隐含 acceptor>50% 的门槛。S2≈356.1 nm 不是当前最低可见目标。

## 3. 有效产物与原始输入/输出


下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/orca_stdout.log](../../../../runs/hold_verification/group_5/dye3_identity_20260916/paper_3deba7268b769ce6/provenance/qzcli_hpc/dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/orca_stdout.log)；[input.inp](../../../../runs/hold_verification/group_5/dye3_identity_20260916/paper_3deba7268b769ce6/provenance/qzcli_hpc/dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/input.inp)
- [dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/orca_stdout.log](../../../../runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/provenance/local_tests/recovery_20260914/dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/orca_stdout.log)；[input.inp](../../../../runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/provenance/local_tests/recovery_20260914/dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/input.inp)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_ar_coverage` | The independent investigation retains candidate identity and validation context for the structures/states actually compared. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_minimum` | The selected candidate used for the vertical excitation is validated as a ground-state minimum. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_character` | The selected lowest visible transition has an explicit electronic-character analysis. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_energy` | The selected lowest-energy visible dye-3 transition is reported quantitatively in kcal/mol. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `con_ar_final` | An independently covered and validated calculation can support assignment of dye-3's lowest visible excitation as a phenolate-to-nitroaryl ICT state within the stated model boundary. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

保留原59.44±3 kcal/mol容差，未为匹配改变选态或扩容差。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。

## 6. 2026-09-23 测量定义与当前任务的补充对应

正文 p4 区分低能可见 ICT 与高能 UV 局域态；原题面“lowest visible”未给操作窗口。采用公开 400–700 nm 主比较定义（明示为 benchmark 约定，不冒称作者阈值），最低能选态而非最亮/最近答案选态。既有结果 S1=501.7 nm、S2=356.1 nm，因此不改变历史选态、59.44 kcal/mol target 或 ±3 容差。无窗口内态应如实提交缺失主结果，不用 UV 态顶替；原电子分布分析保持。
