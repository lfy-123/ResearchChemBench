# 第一版参考验证执行与剩余审查

更新：2026-09-28T13:23:30.531759+00:00。

已完成适用科学矩阵、原始证据哈希核对和当前AR/PR结果schema复验。详见`phase1_reference_binding.json`及`verified_computation_reference.md`。

本次修复仅绑定已有实算证据；没有修改公开题面、评分标准或科学结果。

原开发计划与来源页码完整保存在 `docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_0dcba54d6a1436bd/AR/4dfccf67c64e331a5b51bfd9de95114a36761aa68de00ec1cbb23cdd67d49bd4/evaluation/reference_validation_plan.md`，其“未计算”状态属于历史阶段。

## 已完成科学端点

- three_full_Z_identities
- three_source_minima
- nine_common_torsion_constrained_geometries
- 120_primary_states
- 60_CAM_states
- mapped_atom_density_correspondence
- same_angle_acceptor_contrasts
- two_method_matched_branch_sensitivities

## 尚未完成的独立工作

- 主协调对最终V1包与逐篇交接的审查。
- 独立语义评分器校准尚未执行。
- 未开展盲测AR；不得补造过去的自主发现轨迹。

## 科学限制

- ThreecompleteisolatedZmonomers, gasB3LYPgeometries andcommonPCMDCMverticalresponse. Finite3anglelocalconstraintset, nofree-minimumpopulations forgridpoints. M06/CAMsystematicspreadisactualsensitivitynotconfidenceinterval. Atomprobabilitymatchingdiscardsphase; use onlyreciprocalcharacterbranchesanddiscloseambiguousstates. CrossacceptorcomparisonisCTtypefamily, notidenticalmany-electronwavefunction. Noemission,aggregation,quantumyield,photostabilityrates ordevicepredictions. Source-awareverificationnotblindAR.
