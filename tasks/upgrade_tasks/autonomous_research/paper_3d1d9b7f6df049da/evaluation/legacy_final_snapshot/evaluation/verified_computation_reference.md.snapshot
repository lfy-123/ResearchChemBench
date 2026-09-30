# 已验证成功计算参考 — paper_3d1d9b7f6df049da / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 5）

正文 PDF p8 与 SI Tables S3a/S3b（PDF pp21–22）。

[论文正文](../../../../papers/paper_3d1d9b7f6df049da/documents/main.pdf)；[当前成功结果与证据索引](../../../../runs/hold_verification/group_5/closure_20260921/paper_3d1d9b7f6df049da/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_3d1d9b7f6df049da/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 保持两份 96 原子 C87H7Y2 固定 SI 几何，中性 doublet，Y 为1-based 81/82；任务为给定几何的横向振动性质，不额外增加优化任务。
2. ORCA6.1.1 PBE/def2-TZVP、Y Dolg/def2-ECP、DEFGRID3/VeryTightSCF，分别计算 Hessian；各 288 modes（6 rigid zeros、282 positive），无负频。固定几何残余梯度诊断有记录，不谎称重新优化最低点。
3. 从 native Cartesian mode 向量，以质量加权 Y kinetic participation 及相对 Y→C80 核心质心径向的 transverse fraction 判读；作者路线验证用 >.5/>.8 作为独立分析选择，不按靠近 gold 选模，也不将该阈值变成额外隐藏门槛。
4. Ih 四个横向模 38.569422/44.952490/56.192315/60.850646；D5h 66.703314/73.094561/82.391991/87.430579 cm⁻¹，各在原±12窗口，D5h 均值较高 27.263893 cm⁻¹。以模式族和频率趋势讨论振动关联，不生成未计算的定量 T1。

## 3. 有效产物与原始输入/输出


下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [y2_d5h_fixed_geometry_grid3_hessian_sensitivity_bounded2400_20260918/20260918T140810_293541_421/orca_stdout.log](../../../../runs/hold_verification/group_5/y2_bounded_20260918/paper_3d1d9b7f6df049da/provenance/qzcli_hpc/y2_d5h_fixed_geometry_grid3_hessian_sensitivity_bounded2400_20260918/20260918T140810_293541_421/orca_stdout.log)；[input.inp](../../../../runs/hold_verification/group_5/y2_bounded_20260918/paper_3d1d9b7f6df049da/provenance/qzcli_hpc/y2_d5h_fixed_geometry_grid3_hessian_sensitivity_bounded2400_20260918/20260918T140810_293541_421/input.inp)
- [y2_ih_fixed_geometry_grid3_hessian_sensitivity_bounded2400_20260918/20260918T131827_725766_188/orca_stdout.log](../../../../runs/hold_verification/group_5/y2_bounded_20260918/paper_3d1d9b7f6df049da/provenance/qzcli_hpc/y2_ih_fixed_geometry_grid3_hessian_sensitivity_bounded2400_20260918/20260918T131827_725766_188/orca_stdout.log)；[input.inp](../../../../runs/hold_verification/group_5/y2_bounded_20260918/paper_3d1d9b7f6df049da/provenance/qzcli_hpc/y2_ih_fixed_geometry_grid3_hessian_sensitivity_bounded2400_20260918/20260918T131827_725766_188/input.inp)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_input` | Both geometries are checked as neutral doublets and diagnostics reported. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_assign` | Selected modes retain identity and reproducible Y2 lateral assignment. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ih` | Ih has four lateral modes near 49.9,54.9,65.2,68.9 cm-1 (SI Table S3a; main-text rounded set 50,55,65,69). | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_d5h` | D5h has four lateral modes near 67.4,81.9,90.2,93.8 cm-1 (SI Table S3b). | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `c_trend` | D5h lateral modes are higher than Ih. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |
| `c_relax` | Higher D5h lateral frequencies support longer D5h T1, with computational evidence. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

最新成功链在 closure_20260921，不能引用旧 group bounded-failure 作为最后结果；固定几何性质与几何发现边界保持不变。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。

## 6. 2026-09-23 测量定义与当前任务的补充对应

SI Tables S3a/b 的主对照为每异构体四个 Y2 横向模式。旧 schema 允许 modes 超过四个，numeric selector 却读取整个数组与四参考配对。现将 complete 主数组限定四项，额外候选用 additional_modes，不限制探索总数；mode_id 去重由显式物理指认规则判断，schema uniqueItems 只阻止完全相同的重复记录，不冒称能自动判定所有物理重复。真实两异构体各四模式结果保留，原频率及 ±12 cm⁻¹ 容差不变。
