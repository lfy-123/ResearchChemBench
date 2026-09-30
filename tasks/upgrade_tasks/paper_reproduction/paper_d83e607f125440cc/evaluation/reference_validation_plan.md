# 第一版参考验证执行与剩余审查

更新：2026-09-28T13:23:21.855893+00:00。

已完成适用科学矩阵、原始证据哈希核对和当前AR/PR结果schema复验。详见`phase1_reference_binding.json`及`verified_computation_reference.md`。

本次修复仅绑定已有实算证据；没有修改公开题面、评分标准或科学结果。

原开发计划与来源页码完整保存在 `docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_d83e607f125440cc/PR/01a49e8f75cc572d9badd577a1e7c586cf1a4956d0c2c562612da2b9212df825/evaluation/reference_validation_plan.md`，其“未计算”状态属于历史阶段。

## 已完成科学端点

- five_gas_series
- exact_atom_and_spin_identity
- minimum_curvatures
- Hirshfeld_partition
- paired_gas_conformers
- common_CPCM
- retrospective_Cl_challenge
- superfine_numerical_control
- hypothesis_discrimination

## 尚未完成的独立工作

- 主协调对最终V1包与逐篇交接的审查。
- 独立语义评分器校准尚未执行。
- 未开展盲测AR；不得补造过去的自主发现轨迹。

## 科学限制

- Five finite molecular systems and stated gas/CPCM electronic channels only. Lowest found among source and OH-rotated basins, not exhaustive global search. No functional-wide confidence interval, electrode reference, rates, yields or full flavin/electrode network. Source-compatible old basins separately retained.
