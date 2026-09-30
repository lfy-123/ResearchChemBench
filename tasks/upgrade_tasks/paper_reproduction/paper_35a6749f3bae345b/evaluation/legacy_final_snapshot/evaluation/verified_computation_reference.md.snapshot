# 已验证成功计算参考 — paper_35a6749f3bae345b / paper_reproduction

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 2）

正文 Table 2，SI S22/Table S15 与 S24/Table S17 的 S0 坐标、S5/S7 及 S1 结构/跃迁表。

[论文正文](../../../../papers/paper_35a6749f3bae345b/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_2/paper_35a6749f3bae345b/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_35a6749f3bae345b/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. DBC-Ph=C32H21N/54 原子、DBC-Nap=C36H23N/60 原子，均中性 singlet。历史验证使用作者知情结构，保持原子映射；这些优化终态现在仅存 evaluation/author_results，不再给待评 agent。
2. Gaussian16 C.01 B3LYP/6-31+G(d,p)/IEFPCM(toluene) 分别完成两分子的 S0 Opt/Freq 和最低 singlet S1 TD Opt/Freq。Ph S0/S1 各 156 个正频；Nap S0/S1 各 174 个正频。Nap S1 使用 20260921 checked-root 完整链，非旧未收敛分支。
3. 在各优化态读 TD 跃迁并核对 root、singlet、振子强度和主要组态；S0 列表来自独立 TD10 日志，S1 来自收敛态分析。按同一索引计算 DBC–Nphenyl/para-aryl 扭角；DBC–Nphenyl 急角平面扭转 Ph S0/S1=64.6788/54.6879°，Nap=64.8819/81.6929°。Nap S1 接近正交，不能把四态一概写成 moderate。
4. 由对应已保存波函数作 Multiwfn Mulliken 与 SCPA 的 HOMO/LUMO 片段分析，连同跃迁和几何解释取代基影响；不同 population scheme 的百分比不强行合并为唯一 CT 比例。Ph S1 412.06 nm 与 SI 441.44 nm 的差异保留，不冒称逐数值复现。

## 3. 有效产物与原始输入/输出

- [provenance/completed_state_analysis_20260922/INDEPENDENT_RESULTS.json](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/completed_state_analysis_20260922/INDEPENDENT_RESULTS.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [qzcli_hpc/author_DBC_Nap_SI_S18_S1_checked_root_optfreq_20260921_20260921T113512Z/stdout.log](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_DBC_Nap_SI_S18_S1_checked_root_optfreq_20260921_20260921T113512Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_DBC_Nap_SI_S18_S1_checked_root_optfreq_20260921_20260921T113512Z/input.com)
- [qzcli_hpc/author_dbc_nap_b3lyp_631pgdp_pcm_toluene_optfreq_hpc20_20260906T000639Z/stdout.log](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_nap_b3lyp_631pgdp_pcm_toluene_optfreq_hpc20_20260906T000639Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_nap_b3lyp_631pgdp_pcm_toluene_optfreq_hpc20_20260906T000639Z/input.com)
- [qzcli_hpc/author_dbc_nap_b3lyp_631pgdp_pcm_toluene_s0_td10_20260911T055117Z/stdout.log](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_nap_b3lyp_631pgdp_pcm_toluene_s0_td10_20260911T055117Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_nap_b3lyp_631pgdp_pcm_toluene_s0_td10_20260911T055117Z/input.com)
- [qzcli_hpc/author_dbc_ph_b3lyp_631pgdp_pcm_toluene_optfreq_si54_repaired_20260908T100248Z/stdout.log](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_ph_b3lyp_631pgdp_pcm_toluene_optfreq_si54_repaired_20260908T100248Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_ph_b3lyp_631pgdp_pcm_toluene_optfreq_si54_repaired_20260908T100248Z/input.com)
- [qzcli_hpc/author_dbc_ph_b3lyp_631pgdp_pcm_toluene_s0_td10_20260911T055110Z/stdout.log](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_ph_b3lyp_631pgdp_pcm_toluene_s0_td10_20260911T055110Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_ph_b3lyp_631pgdp_pcm_toluene_s0_td10_20260911T055110Z/input.com)
- [qzcli_hpc/author_dbc_ph_s1_b3lyp_631pgdp_pcm_toluene_tdoptfreq_si54_repaired_20260908T100252Z/stdout.log](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_ph_s1_b3lyp_631pgdp_pcm_toluene_tdoptfreq_si54_repaired_20260908T100252Z/stdout.log)；[input.com](../../../../docs/verification/group_2/paper_35a6749f3bae345b/provenance/qzcli_hpc/author_dbc_ph_s1_b3lyp_631pgdp_pcm_toluene_tdoptfreq_si54_repaired_20260908T100252Z/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp1` | Validate supplied neutral singlet identities and converged S0/S1 states. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp2` | Quantify molecule- and state-resolved inter-ring twisting and relate transitions/orbitals to substituent effects. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `c1` | The calculation supports or qualifies the source structure-property interpretation through explicit Ph-versus-Nap, S0-versus-S1 geometry and electronic evidence. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

当前公开 starter 是无端点几何约束的 ETKDGv3 独立图嵌入，未作量化回放。身份正确、方法可计算与“该具体初猜已独立收敛”是不同声明。该任务现有语义评分保留逐态结果和支持/限定假设的空间。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

## 6. 2026-09-23 测量定义与当前任务的补充对应

SI pp11/13 Tables S5/S7 分别列出 Ph/Nap 在 S0 和 S1 优化几何的 5 个 singlet TD 根，而不是 S1→Sn 激发态吸收。删除未定义的“requested window”替代条件，明确两几何各至少根 1–5。schema 的 validated 分支补两几何/根唯一性覆盖，partial/failure 分支保持可提交，不用缺失值凑成功。真实历史记录 Ph 的 S0/S1 为 10/5 根，Nap 为 10/10 根，已有计算足够；未新添计算目标。
