# 已验证成功计算参考 — paper_8d8940710de08f7f / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 5）

正文 §2.8 的 CPCM；SI 的 in-vacuo 表题与配对能量核对存在差异，按已批准的甲醇主协议解释。

[论文正文](../../../../papers/paper_8d8940710de08f7f/documents/main.pdf)；[当前成功结果与证据索引](../../../../runs/hold_verification/group_5/closure_20260918/paper_8d8940710de08f7f/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_8d8940710de08f7f/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. SNaft/SAntr 中性 singlet 的 V(+)、V(−)、Z 六个原结构；Z 按周期扭角 ±140…180° 同一 near-trans 身份。保留实际 signed C–S–N–C，不用名称猜构象。
2. 六个 ORCA6.1.1 R2SCAN/def2-TZVP/def2-J split-RI-J/CPCM(methanol) Opt/Freq 完成。采用已记录 DEFGRID2/TightSCF 和各输入的优化设置；缺失 SNaft V+ 后续成功链补齐，不混入旧真空六态。
3. 直接读取各 Final Gibbs free energy：298.15 K/1 atm，Grimme QRRHO entropy reference frequency100 cm⁻¹。以每个分子最低 G 为零，×627.509474 kcal/mol/Eh；SNaft Z gap2.638125、SAntr2.763389；V± gap .227309/.210636。
4. 检查完整频率/无虚频、signed torsion 和 C–H···O 接触；V-like stabilization 的解释由相对 G 与真实几何联系支持，不虚构 QTAIM 接触能或独占因果。已有配对溶剂单点检验支持采用甲醇条件，正文/SI 表题冲突保留为 benchmark 解释。

## 3. 有效产物与原始输入/输出


下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [execution_jobs/job_1907328a3c02414e943017761a14dba2/stdout.log](../../../../docs/verification/group_5/paper_8d8940710de08f7f/native_workspace/outputs/execution_jobs/job_1907328a3c02414e943017761a14dba2/stdout.log)
- [execution_jobs/job_2864c00911a84195b7f52469ba309fa6/stdout.log](../../../../docs/verification/group_5/paper_8d8940710de08f7f/native_workspace/outputs/execution_jobs/job_2864c00911a84195b7f52469ba309fa6/stdout.log)
- [execution_jobs/job_6a86cb264d954952b1d4400b1d8b951e/stdout.log](../../../../docs/verification/group_5/paper_8d8940710de08f7f/native_workspace/outputs/execution_jobs/job_6a86cb264d954952b1d4400b1d8b951e/stdout.log)
- [execution_jobs/job_a40573c7f94b400bbc9c657a0a00a7cb/stdout.log](../../../../docs/verification/group_5/paper_8d8940710de08f7f/native_workspace/outputs/execution_jobs/job_a40573c7f94b400bbc9c657a0a00a7cb/stdout.log)
- [execution_jobs/job_a53ce5a934bc43e9a8893f935c6639f9/stdout.log](../../../../docs/verification/group_5/paper_8d8940710de08f7f/native_workspace/outputs/execution_jobs/job_a53ce5a934bc43e9a8893f935c6639f9/stdout.log)
- [snaft_vplus_si_methanol_missing_minimum_20260916/20260916T143959_872493_112/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_closure_20260916/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_vplus_si_methanol_missing_minimum_20260916/20260916T143959_872493_112/orca_stdout.log)；[input.inp](../../../../runs/hold_verification/group_5/santr_closure_20260916/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_vplus_si_methanol_missing_minimum_20260916/20260916T143959_872493_112/input.inp)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_ar_process_minima` | Each of the three named torsion-region states for each molecule is treated as a stationary-point candidate and validated as a minimum before comparison. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_process_relative` | Relative Gibbs energies are formed by subtracting the lowest Gibbs energy separately within each molecule's three-state set. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_result_energy` | The neutral V-like states are nearly degenerate and the neutral Z state is higher by roughly 3 kcal/mol for each molecule. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_result_interpretation` | The computed energetic pattern is interpreted using the reported structural interaction evidence for the two molecules and their calculated states. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `con_ar_final_order` | For both neutral molecules, the two V-like conformers are the low-energy pair and Z is less favorable by about 3 kcal/mol; the V pair is close in energy. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

公开的是介质、温压和100cm⁻¹ thermochemistry协议而非能序/答案；仍保留方法选择，另介质仅作独立敏感性结果。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。
