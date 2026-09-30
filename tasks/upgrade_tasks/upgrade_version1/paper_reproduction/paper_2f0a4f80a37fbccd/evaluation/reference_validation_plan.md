# 第一版参考验证执行与剩余审查

更新：2026-09-28T13:31:58.881011+00:00。

已完成适用科学矩阵、原始证据哈希核对和当前AR/PR结果schema复验。详见`phase1_reference_binding.json`及`verified_computation_reference.md`。

本次修复仅绑定已有实算证据；没有修改公开题面、评分标准或科学结果。

原开发计划与来源页码完整保存在 `docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_2f0a4f80a37fbccd/PR/b41905e567b5f656b248e8a9c4db2bff8846150970cfec84865406ea43c56c6b/evaluation/reference_validation_plan.md`，其“未计算”状态属于历史阶段。

## 已完成科学端点

- five_full_identity_minima
- eta1_eta2_competition
- relative_ligand_geometry_alternatives
- native_modes_and_nitrate_PPh3_mixing
- four_and_five_band_comparisons
- uniform_scale_sensitivity
- bounded_candidate_set

## 尚未完成的独立工作

- 主协调对最终V1包与逐篇交接的审查。
- 独立语义评分器校准尚未执行。
- 未开展盲测AR；不得补造过去的自主发现轨迹。

## 科学限制

- 作者知情的参考验证，非盲AR。有限五起点而非全局构象穷尽；气相B3LYP/LANL2DZ含ECP，无显式自旋轨道/晶体堆积/固态环境。统一0.96/0.98/1.00比例只测试敏感性，不能消除方法与固态误差；没有预设任意光谱通过容差，没有以缺峰降低RMSE后宣布胜者。电子能与谐振G分别保留，但不推断固态群体或氧/NO生成路径。
