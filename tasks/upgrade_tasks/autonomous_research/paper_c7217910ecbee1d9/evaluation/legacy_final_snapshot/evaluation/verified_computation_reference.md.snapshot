# 已验证成功计算参考 — paper_c7217910ecbee1d9 / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 2）

正文及 SI DOCX Computational details 的 PAl12[B(C6F5)3]2 对象和 PBE0/def2-SVP 路线。

[论文正文](../../../../papers/paper_c7217910ecbee1d9/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/report/results.json)。
[补充材料 supplementary_001.docx](../../../../papers/paper_c7217910ecbee1d9/documents/supplementary_001.docx)

## 2. 真实有效计算流程

1. 完整对象 PAl12B2C36F30，共 81 原子。构建两种配位位置/取向（opposite、obtuse），每种中性取 doublet/quartet、阴离子取 singlet/triplet，共八个候选；不是 52 原子简化模型。
2. Gaussian16 PBE0/def2-SVP 气相 Opt/Freq，对八候选均取得完整 237 模、无虚频结果，保留同电荷/自旋下去重、能量和配体连接检查。一条脱离接触的候选没有作为所选 endpoint。
3. 各电荷态分别取最低 E+ZPE：opposite 中性 doublet E=−7657.13468088/ZPE=.331902 Eh；opposite anion singlet E=−7657.27967667/ZPE=.331401 Eh。AEA=(E0neutral−E0anion)×27.211386245988=3.959169350 eV；纯电子值 3.945536446 eV。
4. 检查所选两态的 P–Al、30 条 Al12 icosahedral 边、Al–B 接触、两配体和 30 个 C–F 键，支持框架保留与 3.93±0.30 eV 的 AEA 比较。结构框架保留不伪称完整 superatomic 电子壳层分析。

## 3. 有效产物与原始输入/输出

- [provenance/final_closure_20260919/independent_results.json](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/final_closure_20260919/independent_results.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m1_nonclashing_optfreq_20260916_20260917T033059Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m1_nonclashing_optfreq_20260916_20260917T033059Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m1_nonclashing_optfreq_20260916_20260917T033059Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m3_nonclashing_optfreq_20260916_20260917T045136Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m3_nonclashing_optfreq_20260916_20260917T045136Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_anion_m3_nonclashing_optfreq_20260916_20260917T045136Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m2_nonclashing_optfreq_20260916_20260917T024030Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m2_nonclashing_optfreq_20260916_20260917T024030Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m2_nonclashing_optfreq_20260916_20260917T024030Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m4_nonclashing_optfreq_20260916_20260917T040114Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m4_nonclashing_optfreq_20260916_20260917T040114Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_obtuse_neutral_m4_nonclashing_optfreq_20260916_20260917T040114Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_anion_m3_nonclashing_optfreq_20260916_20260917T033053Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m3_nonclashing_optfreq_20260916_20260917T033053Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m3_nonclashing_optfreq_20260916_20260917T033053Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/input.com)
- [qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m4_nonclashing_optfreq_20260916_20260917T021003Z/stdout.log](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m4_nonclashing_optfreq_20260916_20260917T021003Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m4_nonclashing_optfreq_20260916_20260917T021003Z/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `ar_process_minimum` | The report independently defines candidate generation, deduplication, optimization, endpoint validation and calculation coverage for both charge states. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_process_aea_definition` | The AEA uses the adiabatic neutral/anionic energy difference and an explicit ZPE convention. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_result_aea` | The source endpoint AEA is 3.93 eV. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_result_framework` | The optimized ligated system retains the specified PAl12 core framework within the isolated-cluster model. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `ar_final_claim` | Within independently declared search coverage, the validated AEA and framework assessment answer the specified isolated-cluster question without unsupported global claims. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

完整 site/spin 有限链支持现有 AEA 与结构框架目标，不要求全球构象穷举或未评的 AIMD。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。
