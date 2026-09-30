# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:56:02.783040+00:00。论文 `paper_9aa6d5655edfeb52`；模式 `AR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_9aa6d5655edfeb52/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_9aa6d5655edfeb52/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_9aa6d5655edfeb52/AR/a10b54bb7ac8403a911c7f86ace21dcde4b6e253978ecd10cac5300172fed597`。历史final快照保持不变。

## 已完成端点

- fusion_pair.fused2a
- fusion_pair.nonfused1a
- cage_displacement.2a_minus
- cage_displacement.2a_plus
- cage_displacement.1a_minus
- cage_displacement.1a_plus
- causal_limits.fusion_vs_motion
- causal_limits.method_sensitivity

## 适用范围与限制

- Source-aware reference verification, not blind AR. Complete isolated neutral singlets in IEFPCM THF; no crystal packing, emission quantum yield or rate inference.
- ±0.05A is an intervention design, not a target tolerance; finite differences are local and can include nonlinear curvature. No constrained point inherits thermal corrections.
- Different molecular formulas prohibit cross-species total-energy subtraction. No artificial graph bijection removes the real Br/H confound.
- All ten roots retained. Selected S1 has a resolved S1/S2 gap and reciprocal unique overlap throughout required paths and CAM controls. Higher-state mixing does not warrant claims of unique high-state correspondence or an exhaustive excited-state manifold.
- The two old equilibrium-response frozen spectra are diagnosed and excluded from core comparisons; repaired nonequilibrium spectra use identical frozen coordinates.
- Method and orthogonal-relaxation spreads are actual measured sensitivity components, not statistical confidence intervals.

## 本次真实计算报告

# 碳硼烷融合与笼运动：真实对照验证

更新：2026-09-28T13:55:35.145251+00:00。作者知情验证；AR/PR共享同一物理证据。

融合产物相对含Br前体的最低单重态激发能差为 +0.2012 eV（B3LYP），同几何CAM对照为 +0.1470 eV。两者自身的笼C–C位移均改变激发能；融合体固定/正交放松的中心响应分别为 -0.7750/-0.8320 eV/Å。局部笼运动是可测因素，但该两分子比较同时改变Br/H组成与其他几何，不能据此将光谱差唯一归因于融合。

## 对象、基准与正常模

融合体2a为C18H20B10，源前体1a为C18H21B10Br。两者均保留完整closo笼和全部芳基；前体并非把融合边简单断开的同分子式几何变体。两套完整基态正频率、笼C–C投影和质量加权参与度见正常模文件。

|对象|笼C–C(Å)|最低频率(cm⁻¹)|S1(eV)|f|CAM S1(eV)|
|---|---:|---:|---:|---:|---:|
|fused2a|1.726502|38.2035|3.9220|0.2357|4.2946|
|nonfused1a|1.774516|18.1111|3.7208|0.1668|4.1476|

## 同身份笼位移

表中E0代价以每个成员自身释放基态为零；约束点无热修正。固定点只改变笼两个C坐标，正交放松点仅固定相同C–C距离。所有光谱使用统一非平衡THF响应。

|对象/位移|固定E0代价(kJ/mol)|放松E0代价(kJ/mol)|固定Δ激发能(eV)|放松Δ激发能(eV)|
|---|---:|---:|---:|---:|
|fused2a/-0.05Å|1.45443|0.74828|+0.0324|+0.0306|
|fused2a/+0.05Å|1.29813|0.58644|-0.0451|-0.0526|
|nonfused1a/-0.05Å|1.30222|0.39125|+0.0372|+0.0206|
|nonfused1a/+0.05Å|1.19673|0.32819|-0.0502|-0.0489|

## 态连续性、方法与修复

全部十根的X+Y跃迁密度、NTO权重、完整三片段转移矩阵与实空间质心保留。决定性S1在所有成对比较中互为最大重叠，S1/S2间隔和竞争根同时列出；未把模糊高根强制对应。

两化学结构的激发能差为B3LYP +0.2012 eV、CAM +0.1470 eV；方法响应差0.0542eV。此差值不是置信区间。

早期融合体两个固定点因Density=Current使用了平衡溶剂响应。原始日志明确显示IEInf=0，故未混入主矩阵；在完全相同坐标上补算IEInf=1并重新解析密度。两套结果同时保存，可检查设置差异本身。

## 因果范围

局部运动响应是同一化学身份下的真实干预；它不能消除融合体/前体的Br和B–H差异。因此，可以比较化合物总体光谱与笼运动敏感性，不能给出单独的纯融合贡献或光致衰减速率。

- Source-aware reference verification, not blind AR. Complete isolated neutral singlets in IEFPCM THF; no crystal packing, emission quantum yield or rate inference.
- ±0.05A is an intervention design, not a target tolerance; finite differences are local and can include nonlinear curvature. No constrained point inherits thermal corrections.
- Different molecular formulas prohibit cross-species total-energy subtraction. No artificial graph bijection removes the real Br/H confound.
- All ten roots retained. Selected S1 has a resolved S1/S2 gap and reciprocal unique overlap throughout required paths and CAM controls. Higher-state mixing does not warrant claims of unique high-state correspondence or an exhaustive excited-state manifold.
- The two old equilibrium-response frozen spectra are diagnosed and excluded from core comparisons; repaired nonequilibrium spectra use identical frozen coordinates.
- Method and orthogonal-relaxation spreads are actual measured sensitivity components, not statistical confidence intervals.

## 验收与资源

八个核心矩阵单元、全部实际固定/放松端点及CAM控制完成。AR/PRschema、记录引用、所有证据路径与live/冻结哈希均通过。新原生启动20次，已测分配核时67.6229；后处理和历史复用单列，未知耗时不估算。

证据入口：report/results.json、validation/carborane_quality.json、carborane_state_table.csv、cage_vibrational_evidence.json、evaluator_mapping.json。

