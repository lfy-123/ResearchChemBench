# 第一版参考验证执行与剩余审查

更新：2026-09-28T13:23:22.422898+00:00。

已完成适用科学矩阵、原始证据哈希核对和当前AR/PR结果schema复验。详见`phase1_reference_binding.json`及`verified_computation_reference.md`。

本次修复仅绑定已有实算证据；没有修改公开题面、评分标准或科学结果。

原开发计划与来源页码完整保存在 `docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_2f302589e5e9e420/AR/b8523ec7a1ebcc0dd609b8494dc94ae863d0bbd68d33ad477834e4361ed6369b/evaluation/reference_validation_plan.md`，其“未计算”状态属于历史阶段。

## 已完成科学端点

- identity
- conformers
- ensembles
- OH_interventions
- matched_backbone
- normal_modes
- low_frequency_sensitivity

## 尚未完成的独立工作

- 主协调对最终V1包与逐篇交接的审查。
- 独立语义评分器校准尚未执行。
- 未开展盲测AR；不得补造过去的自主发现轨迹。

## 科学限制

- Finite local OH conformer search of supplied capped molecular fragments, gas298.15K. Five distinct minima retained; one collapse recorded. Population not proven exhaustive, degeneracy1, multi-level weights/properties declared. OH redshift based on native displacement evidence; unscaled gas spectra are not macroscopic FTIR. No Dk/water-uptake prediction.
