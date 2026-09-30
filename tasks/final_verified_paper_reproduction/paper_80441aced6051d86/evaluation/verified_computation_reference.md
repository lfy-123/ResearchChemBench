# 已验证成功计算参考 — paper_80441aced6051d86 / paper_reproduction

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 4）

正文 PDF p3 方法、p4/Fig.4；原始 SI DOCX（本地 source_downloads/mmc1.docx）的 optimized monomer/dimer 坐标表。

[论文正文](../../../../papers/paper_80441aced6051d86/documents/main.pdf)；[当前成功结果与证据索引](../../../../docs/verification/group_4/paper_80441aced6051d86/report/results.json)。

## 2. 真实有效计算流程

1. 历史验证输入为作者 G1 64 原子 +2 singlet monomer 与 128 原子 +4 singlet dimer 优化结构，未含 counterions。这些结构是任务待求几何的答案，因此现已私有化；公开结构从完整化学图独立生成。
2. Gaussian16 B3LYP-GD3/6-31G(d)/PCM(water) monomer/dimer Opt/Freq；成功 monomer 链 20260918、dimer 链 20260919。分别 186/378 正频、正常结束；dimer 的 negligible-forces/Stationary-point 收敛亦为有效结果。
3. 由终态同一原子映射提取两组 monomer 芳环二面角：benzyl–pyridinium 51.975518/51.979518°，均值 51.977518°；pyridinium–naphthalene 32.407037/32.411726°，均值 32.409382°。后者不是 dimer twist。
4. 对 dimer 两 naphthalene 最小二乘平面定同向平均法线；核对原始终态/几何后处理给 interplanar separation 3.778995 Å、完整 centroid 距离 5.353514 Å、slip 44.901541°。两距离不能混用，私有目标 3.63 Å 是堆积平面间距。
5. 以已优化 monomer 扭转、dimer offset packing 及最低点证据支持现有结构结论，不新增吸收/发射计算或溶液聚集自由能。

## 3. 有效产物与原始输入/输出

- [provenance/conclusion_reaudit_20260921.json](../../../../docs/verification/group_4/paper_80441aced6051d86/provenance/conclusion_reaudit_20260921.json)
- [artifacts/source_downloads/1-s2.0-S0143720825008265-mmc1.docx](../../../../docs/verification/group_4/paper_80441aced6051d86/artifacts/source_downloads/1-s2.0-S0143720825008265-mmc1.docx)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [local_stage_tests_20260914/g1_dimer_full128_source_internal_recalcfc_optfreq_20260919/stdout.log](../../../../docs/verification/group_4/paper_80441aced6051d86/provenance/local_stage_tests_20260914/g1_dimer_full128_source_internal_recalcfc_optfreq_20260919/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_80441aced6051d86/provenance/local_stage_tests_20260914/g1_dimer_full128_source_internal_recalcfc_optfreq_20260919/input.com)
- [local_stage_tests_20260914/g1_monomer_full64_si_gd3_pcm_optfreq_internal_repair_20260918/stdout.log](../../../../docs/verification/group_4/paper_80441aced6051d86/provenance/local_stage_tests_20260914/g1_monomer_full64_si_gd3_pcm_optfreq_internal_repair_20260918/stdout.log)；[input.com](../../../../docs/verification/group_4/paper_80441aced6051d86/provenance/local_stage_tests_20260914/g1_monomer_full64_si_gd3_pcm_optfreq_internal_repair_20260918/input.com)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_input` | The report verifies the supplied G1 monomer and dimer as the stated atom-count, charge and singlet systems and preserves their identities during analysis. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_min` | Both relaxed structures are validated as minima or the report gives a scientifically justified stability alternative and diagnostics. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_mono` | The monomer geometry has the reported twisted dihedral pattern. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_dimer` | The dimer geometry has the reported offset parallel packing descriptors. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `c_final` | Within the supplied ground-state structural boundary, the computed monomer is twisted and the dimer is an offset, parallel stack consistent with the authors' J-aggregate assignment. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

水作为主比较介质已获批准公开。新 starter 为两个独立 monomer 图嵌入和中立无碰撞装配，不继承 SI packing；没有从该 starter 新作优化。不新增 RMSD 评分，作者终态仅支持现有描述符/身份检查。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

补充核对：09-21 历史审计 JSON 的末尾 slip_definition 一句把法线/平面写反，但同文件实际结果同时列出 slip=44.901541°、angle_to_normal=45.098459°。本任务与计算档案采用这些数值对应的“质心向量与平均平面的急角”，不沿用那句元数据，也未改动历史文件。

## 6. 2026-09-23 测量定义与当前任务的补充对应

正文 p3–4 的单体扭转/二聚体堆积仍为科学目标；group_4/finalize_paper_804.py:124–153 的实际验证使用 SVD 最小二乘平面及 acos(abs(dot)) 急角，原题面却允许任意 dihedral 定义。现公开原子环集合与主测量口径，保留既有 target/tolerance。task 曾承诺 inline coordinates，而 complete schema 只接收 structure_path，现统一为非空文件路径；不新增坐标格式分支。二聚体 slip 仍是质心向量与平均平面的急角，不改为法线角。独立 starter 和私有作者结果均未改。
