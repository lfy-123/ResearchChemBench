# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:23:33.288591+00:00。论文 `paper_94e7481ded3b6a75`；模式 `PR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_94e7481ded3b6a75/PR/11bf5fe43ae821d10db3ff70b90e9a20f1aaee257904beed38e4c088a606ce61`。历史final快照保持不变。

## 已完成端点

- state_geometry.S0_free
- state_geometry.S1_free
- state_geometry.S0_restrained
- state_geometry.S1_restrained
- motion_response.vertical_fixed_motion
- motion_response.relaxed_motion
- local_robustness.second_torsion_or_method
- local_robustness.common_solvent

## 适用范围与限制

- Single isolated PBNA in gas with fixed-geometry CH2Cl2 continuum sensitivity; no crystal/aggregate calculation, quantum yield, nonradiative rate or lifetime claim.
- Source-aware native reuse is not blind autonomous discovery. Only two angular interventions and local S1 minima; no exhaustive conformer search.
- B3LYP/6-31G(d) electronic quantities; no thermal or standard-state corrections used, constrained points have no thermodynamic statistical weight.
- D is a normalized X+Y hole/electron first-moment distance; symmetry can cancel opposing transfers. Fragment transfer and NTO evidence remain necessary.
- State matching uses reciprocal endpoint AO overlaps plus native ten-root trajectory energy gaps/dominant contributions. Large geometric endpoint changes reduce overlaps; higher roots can mix and are not forced into root-number identity.
- Sensitivity spreads are actual protocol/angle contrasts, not statistical confidence intervals or total model error.
- Main PDF p7 describes PBNA as AIE-inactive. These local molecular controls do not establish aggregation-induced emission; TPE-derivative observations cannot be transferred to PBNA.

## 本次真实计算报告

# PBNA 分子运动限制：科学验证

更新：2026-09-28T06:23:37.119496+00:00。当前冻结版本：00e759ce1b7e2eb1d19233719fba0e39e6c594795c41ceda6ec8689b33ac2069。作者知情参考验证，非盲AR。

## 作者路线与问题

主文Fig3/Fig4与SI p19采用Gaussian/B3LYP/6-31G(d)。历史PBNA自由S0重新核验后复用；S1、共同两角运动约束、DCM电子介质控制和态匹配均为新实算。只考察C24H22B2N2分子局部解释。

## 主要结论

PBNA分子局部扭转确实改变同一低激发态：固定30度相对自由S0几何的激发能变化-0.0979eV，固定75度为+0.0828eV；共同CH2Cl2下30度变化-0.0987eV。电子密度、态重叠和S1弛豫均支持局部几何响应，但变化方向依角度，不能推出任意运动限制必然红移或证明聚集AIE。

|几何/环境|S0总能(Eh)|S1总能(Eh)|两角(度)|激发能(eV)|f|D(Å)|
|---|---:|---:|---|---:|---:|---:|
|PBNA_both30_relaxed_TD10|-1087.14088153|-1087.01650975|30.0001, 30.0001|3.3843|0.3686|0.00691058|
|PBNA_free_TD10_pilot|-1087.14452188|-1087.01683854|130.7639, 53.4018|3.4744|0.2459|0.00000510|
|PBNA_both30_fixed_TD10|-1087.11039414|-1086.98630854|30.0000, 30.0000|3.3765|0.3390|0.00659991|
|PBNA_free_TD10_DCM|-1087.15095845|-1087.02511733|130.7639, 53.4018|3.4243|0.3165|0.00000265|
|PBNA_both75_fixed_TD10|-1087.14142754|-1087.01070348|75.0000, 75.0000|3.5572|0.1432|0.05278900|
|PBNA_both30_fixed_TD10_DCM|-1087.11731209|-1086.99509942|30.0000, 30.0000|3.3256|0.4398|0.01941787|
|PBNA_S0_both75_restrained_TD10|-1087.14302564|-1087.01226118|74.9999, 74.9999|3.5583|0.1411|0.01155024|
|PBNA_S1_free_optfreq_TD10|-1087.13598592|-1087.02501134|142.2591, 42.1718|3.0198|0.2448|0.00000560|
|PBNA_S1_both75_restrained_TD10|-1087.13513196|-1087.02004355|75.0000, 75.0000|3.1317|0.1270|0.02044297|
|PBNA_S1_both30_restrained_TD10|-1087.13314904|-1087.02378549|30.0001, 30.0001|2.9759|0.2882|0.01875382|

## 弛豫与态对应

自由S1弛豫ΔE=-21.457683kJ/mol；两角30度受限弛豫ΔE=-19.102453kJ/mol；差=2.355231kJ/mol。由各自S0几何的E1出发到对应S1端点，未混入热修正。S1端点gap差=-0.0439eV；S0受限优化后的vertical gap差=-0.0901eV。

全部19/18/18组原生S1优化步（具体数量由quality记录）保持>0.4eV的S1/S2间隙和95→96主成分；端点通过十态AO物理重叠互为最佳匹配，数据及竞争根重叠在quality。不同几何的重叠降低如实保留；没有声称每一步都做了完整波函数重叠。

两自由S0/S1端点各144正频率。30/75度点只要求相应受限优化收敛和实际角度，并明确不是自由极小值。

## 电子密度与稳健性

D采用归一化X+Y空穴/电子AO一阶矩，非激发差分电荷。自由对称PBNA的D近零，但跨片段分量约0.15，不能据D一项声称没有电荷重排。NTO权重、完整十态转移矩阵和所有片段分区均可重算。

30度气相/CH2Cl2响应分别-0.0979/-0.0987eV，差-0.0008eV。75度对照+0.0828eV使符号反转，因此结论是角度相关的局部响应。实际控制差仅为模型敏感性，不是统计误差条。

## 边界、消耗与验收

- Single isolated PBNA in gas with fixed-geometry CH2Cl2 continuum sensitivity; no crystal/aggregate calculation, quantum yield, nonradiative rate or lifetime claim.
- Source-aware native reuse is not blind autonomous discovery. Only two angular interventions and local S1 minima; no exhaustive conformer search.
- B3LYP/6-31G(d) electronic quantities; no thermal or standard-state corrections used, constrained points have no thermodynamic statistical weight.
- D is a normalized X+Y hole/electron first-moment distance; symmetry can cancel opposing transfers. Fragment transfer and NTO evidence remain necessary.
- State matching uses reciprocal endpoint AO overlaps plus native ten-root trajectory energy gaps/dominant contributions. Large geometric endpoint changes reduce overlaps; higher roots can mix and are not forced into root-number identity.
- Sensitivity spreads are actual protocol/angle contrasts, not statistical confidence intervals or total model error.

AR/PR同一实算证据，两套原始schema与live/snapshot SHA检查通过。全部关键点、scoring规则、结论和critical failures逐项见evaluator_mapping.json。新增原生引擎15次，后处理单列；已测原生分配核时103.3812。历史自由S0节省1次相同计算，旧记录资源单独保留，不和新增重复计数。

证据：report/results.json、validation/pbna_quality.json、pbna_state_geometry.csv、validation/contract_checks.json、resource_summary.json；calculation records链接原始输入/输出/几何。

