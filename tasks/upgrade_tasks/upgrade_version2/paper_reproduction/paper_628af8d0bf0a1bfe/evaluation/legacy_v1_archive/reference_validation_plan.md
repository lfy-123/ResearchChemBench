# 第一版参考验证执行与剩余审查

更新：2026-09-28T13:23:23.032097+00:00。

已完成适用科学矩阵、原始证据哈希核对和当前AR/PR结果schema复验。详见`phase1_reference_binding.json`及`verified_computation_reference.md`。

本次修复仅绑定已有实算证据；没有修改公开题面、评分标准或科学结果。

原开发计划与来源页码完整保存在 `docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_628af8d0bf0a1bfe/PR/7af33cc514b4ba6323b7777030330150ae250f6e651685aa77773da6c7bc74d6/evaluation/reference_validation_plan.md`，其“未计算”状态属于历史阶段。

## 已完成科学端点

- identity
- relaxed_minima
- fixed_core_controls
- 84_native_tensors
- BLA
- 12_causal_contrasts
- basis_sensitivity
- rotation_sensitivity

## 尚未完成的独立工作

- 主协调对最终V1包与逐篇交接的审查。
- 独立语义评分器校准尚未执行。
- 未开展盲测AR；不得补造过去的自主发现轨迹。

## 科学限制

- Finite gas-scaffold magnetic response with frozen commoncore and separately frozen periphery. No current-density,crystalpacking,excitedstate,reactivityoruniversal aromaticityclaim. Limited basis andquadraturetests are explicit; no forcedreplication ofsource23.6/19.2ppm.
