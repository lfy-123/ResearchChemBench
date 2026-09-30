# 第一版参考验证执行与剩余审查

更新：2026-09-28T13:23:33.246263+00:00。

已完成适用科学矩阵、原始证据哈希核对和当前AR/PR结果schema复验。详见`phase1_reference_binding.json`及`verified_computation_reference.md`。

本次修复仅绑定已有实算证据；没有修改公开题面、评分标准或科学结果。

原开发计划与来源页码完整保存在 `docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_94e7481ded3b6a75/AR/ffaa41817991dd19bb1fb5c3386b05b26a5f4d9529d34c21fe904f14b75da48e/evaluation/reference_validation_plan.md`，其“未计算”状态属于历史阶段。

## 已完成科学端点

- state_geometry.S0_free
- state_geometry.S1_free
- state_geometry.S0_restrained
- state_geometry.S1_restrained
- motion_response.vertical_fixed_motion
- motion_response.relaxed_motion
- local_robustness.second_torsion_or_method
- local_robustness.common_solvent

## 尚未完成的独立工作

- 主协调对最终V1包与逐篇交接的审查。
- 独立语义评分器校准尚未执行。
- 未开展盲测AR；不得补造过去的自主发现轨迹。

## 科学限制

- Single isolated PBNA in gas with fixed-geometry CH2Cl2 continuum sensitivity; no crystal/aggregate calculation, quantum yield, nonradiative rate or lifetime claim.
- Source-aware native reuse is not blind autonomous discovery. Only two angular interventions and local S1 minima; no exhaustive conformer search.
- B3LYP/6-31G(d) electronic quantities; no thermal or standard-state corrections used, constrained points have no thermodynamic statistical weight.
- D is a normalized X+Y hole/electron first-moment distance; symmetry can cancel opposing transfers. Fragment transfer and NTO evidence remain necessary.
- State matching uses reciprocal endpoint AO overlaps plus native ten-root trajectory energy gaps/dominant contributions. Large geometric endpoint changes reduce overlaps; higher roots can mix and are not forced into root-number identity.
- Sensitivity spreads are actual protocol/angle contrasts, not statistical confidence intervals or total model error.
- Main PDF p7 describes PBNA as AIE-inactive. These local molecular controls do not establish aggregation-induced emission; TPE-derivative observations cannot be transferred to PBNA.
