# 已验证成功计算参考 — paper_628af8d0bf0a1bfe / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文 PDF p5/Fig.5；SI S14 方法，Tables S11/S13（PDF pp51/53）。

[论文正文](../../../../papers/paper_628af8d0bf0a1bfe/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_628af8d0bf0a1bfe/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 以完整 4a/4c 中性 singlet 身份进入 Gaussian16 M06-2X/6-31++G(d) 气相 Opt/Freq；各 186/174 正频，最低 11.2785/14.4537 cm⁻¹。
2. 确定两五元全碳环 [1,2,3,4,13] 与 [4,7,6,5,13]；环心为各五核算术平均，公共 pentalene 平面取八个核心碳最小二乘拟合。在各环心沿同一法向 +1.700 Å 放置 Bq。
3. M06-2X/6-311+G(2d,p) 磁屏蔽；NICS=−nᵀσn，法向对齐 z 后不是 isotropic shielding。4a 两环 23.0310/23.3166，均值 23.1738 ppm；4c 19.1605/19.1549，均值 19.1577 ppm。
4. 从同一完整屏蔽张量重投影到各局部环法向，得到均值 23.17176917/19.15906536 ppm，最大单环变动 .00463489 ppm，4a>4c 顺序不变。这是已执行的几何/轴定义控制，不是新基组或 opposite-face 单点。

## 3. 有效产物与原始输入/输出

- [provenance/corrected_nics_results_20260916/results.json](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/corrected_nics_results_20260916/results.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/stdout.log](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_nics17_20260914/input.com)
- [local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/stdout.log](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4a_sis11_identity_corrected_optfreq_20260914/input.com)
- [local_stage_tests_20260914/4c_sis13_identity_corrected_nics17_20260914/stdout.log](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_nics17_20260914/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_nics17_20260914/input.com)
- [local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/stdout.log](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_628af8d0bf0a1bfe/provenance/local_stage_tests_20260914/4c_sis13_identity_corrected_optfreq_20260914/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `ar_process_minima` | The independent investigation validates equilibrium minima for both named neutral singlets using actual stationary-point evidence. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_process_probes` | The investigator preserves identity of both central five-membered rings and reports the 1.7 Å centroid-normal probe construction and mean operation. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_result_4a` | The independently obtained 4a endpoint is strongly positive and near the source value. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_result_4c` | The independently obtained 4c endpoint is strongly positive and near the source value. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_final` | The computed endpoint comparison supports a larger positive NICS(1.7)zz for 4a than 4c and therefore a stronger antiaromatic/paratropic response for 4a within this pair. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

正文写 6-31++G(2d,p)，SI 写 6-311+G(2d,p)；此成功链采用 SI，差异不静默消除。AR 自主的两解释生成并未在共用作者路线结果中记录，不编造历史探索。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。
