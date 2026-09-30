# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:23:22.422002+00:00。论文 `paper_2f302589e5e9e420`；模式 `AR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_2f302589e5e9e420/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_2f302589e5e9e420/AR/b8523ec7a1ebcc0dd609b8494dc94ae863d0bbd68d33ad477834e4361ed6369b`。历史final快照保持不变。

## 已完成端点

- identity
- conformers
- ensembles
- OH_interventions
- matched_backbone
- normal_modes
- low_frequency_sensitivity

## 适用范围与限制

- Finite local OH conformer search of supplied capped molecular fragments, gas298.15K. Five distinct minima retained; one collapse recorded. Population not proven exhaustive, degeneracy1, multi-level weights/properties declared. OH redshift based on native displacement evidence; unscaled gas spectra are not macroscopic FTIR. No Dk/water-uptake prediction.

## 本次真实计算报告

# EPI1/EPI2 科学验证报告

更新：2026-09-28T04:39:02.408149+00:00。作者知情参考验证，AR/PR共用物理证据，非盲AR成功。

## 科学问题与作者路线

论文将邻甲氧基与OH的分子内氢键联系到降低极性。方法段指定B3LYP-D3(BJ)/6-31G(d)优化频率、ma-def2-TZVPP性质；图4另标CAM-B3LYP/6-311G(d,p)，本报告遵从方法段并保留冲突。升级要求真实OH干预、共同骨架及系综，均按gas298.15K计算。

## 实际结果

所采样的同边界构象系综不支持“甲氧基普遍降低片段极性”：EPI2的⟨μ²⟩较EPI1高5.27%，低频处理不改变方向。源构象及OH旋转支持构象特定的OH–甲氧基相互作用，但匹配骨架与系综反转表明其不能单独解释整个树脂介电机制。

源单构象μ：EPI1 2.223986032D，EPI2 1.899046595D，变化-14.6107%。有限系综⟨μ²⟩分别3.42629945和3.60675228D²。

EPI1新低能构象比旧构象低12.324kJ/mol，权重0.990535；因此旧单构象不代表当前有限系综。EPI2反向启动之一坍缩回原盆地，已去重，不增加简并度。

OH180°固定旋转Δμ：EPI1 0.176199508D，EPI2 0.966632614D。同36原子骨架EPI2−EPI1 Δμ=0.063841843D。

EPI2源氢键构象OH频率3633.7033cm⁻¹，释放后的away构象3720.0568cm⁻¹；位移投影确认OH模式。OH...O从1.9513Å/162.25°变化至3.65435Å/41.85°。不能把固定非驻点计算当实验IR。

低频振动熵下限50/100cm⁻¹使系综百分比变为+5.36048/+5.42621%，方向不变。这是明确的熵截断敏感性，非完整自由转子qRRHO。

## evaluator与契约

AR/PR全部5keypoints、结论、6scoring rules和3critical failures逐条在evaluator_mapping.json映射；两模式results schema通过、证据路径及record ID实际解析通过。科学判断来自上述端点/控制/频率/算术，不由schema或程序退出代替。

## 历史复用及资源

复用2个经原生频率核查的旧极小点与2个同几何高层性质单点，省去4次相同科学作业。历史尝试/核时缺失不估算；legacy原清单保留失败、旧方法和初猜。新增已观察尝试12次，完成分配核时11.143，含已失败ORCA MPI尝试及明确修复。详细逐作业数据见resource_summary.json。

## 限制

本结论限定有限局部OH搜索，不代表完整全局构象空间、交联聚合物或Dk。未对图注另一泛函做选择性拟合；通过公开要求的低频敏感性审查。无剩余必需矩阵缺项。

证据入口：results.json；epi_evidence.json；vibrational_evidence.json；validation/contract_checks.json；validation/intervention_quality.json；原生日志在calculation_records中。

