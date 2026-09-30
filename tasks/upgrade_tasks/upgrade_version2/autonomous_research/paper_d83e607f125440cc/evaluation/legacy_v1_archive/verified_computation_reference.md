# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:23:21.796951+00:00。论文 `paper_d83e607f125440cc`；模式 `AR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_d83e607f125440cc/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_d83e607f125440cc/AR/bccdcbae36497ef196a2b790589d2dde579186e23c32144e1cfc4a5a2fcca079`。历史final快照保持不变。

## 已完成端点

- five_gas_series
- exact_atom_and_spin_identity
- minimum_curvatures
- Hirshfeld_partition
- paired_gas_conformers
- common_CPCM
- retrospective_Cl_challenge
- superfine_numerical_control
- hypothesis_discrimination

## 适用范围与限制

- Five finite molecular systems and stated gas/CPCM electronic channels only. Lowest found among source and OH-rotated basins, not exhaustive global search. No functional-wide confidence interval, electrode reference, rates, yields or full flavin/electrode network. Source-compatible old basins separately retained.

## 本次真实计算报告

# 苄醇氧化描述符：科学验证报告

更新2026-09-28T05:46:08.364991+00:00；冻结版本293f0578d330d57e7be613b80c4d66005db6d85f63ece4a3ce518d6c0186eed2。作者知情参考验证，非盲AR。

## 科学问题和作者路线

正文的有限分子描述符讨论分离初始氧化与自由基阳离子失氢。SI S6指定Gaussian16 B3LYP/6-311+G(d)、真空/CPCM与频率；TablesS8–S16和后续坐标仅用于追溯，不替代计算。升级扩展五成员neutral/radical/fragment、构象、共同介质、spin及假设检验。

## 实际主结果

在已采样的最低能端点及同层级电子定义下，SMe最易失电子却最难发生自由基阳离子的苄位H原子解离。OMe/SMe的构象、共同CPCM介质和加密网格检验保留这两个描述符的相反方向，反驳用单一易氧化程度排序后续失氢；不等同于反应势垒或产率。

主结果逐态选择已计算的最低电子能有效端点。H/Cl/Me仅本次源初猜盆地；OMe/SMe增加OH翻转。没有把有限搜索说成全局搜索。

|成员|I_e(kJ/mol)|D_e(kJ/mol)|S²(before)|

|---|---:|---:|---:|

|H|824.743911|139.442268|0.7605|

|Cl|813.330814|157.337553|0.7574|

|Me|788.897652|152.783849|0.7584|

|OMe|746.976158|172.594617|0.7601|

|SMe|722.948234|198.528334|0.7600|


I由低到高：SMe < OMe < Me < Cl < H；D由低到高：H < Me < Cl < OMe < SMe。不为接近成员捏造不确定度；排序限该计算方法。

## 构象、介质和数值检验

OH翻转后OMe/SMe中性端点均更低；自由基阳离子返回同一盆地（映射RMSD与ΔE见quality），片段替代盆地更高。原source盆地 I/D：{"OMe": {"I": 740.8208103542012, "D": 172.5946171256653, "n": -461.410288575, "r": -461.12812483, "f": -460.560231082, "h": -0.50215593009}, "SMe": {"I": 717.6862990589219, "D": 198.52774300315915, "n": -784.390855795, "r": -784.11750352, "f": -783.539732366, "h": -0.50215593009}}

完整altOH三态与共同CPCM电子I/D见results.pair_controls；共同气相H依预先计划保留。同CPCM H引起所有D等量变化-0.055373940kJ/mol，取代差不变。UFF/1.1/GePol/ε35.688均核对原生日志。

SuperFine/VeryTight在相同原盆地几何复核全部六项电子能与H，逐项敏感性：[{"question": "SMe fixed-source-basin SuperFine/VeryTight versus original integration/SCF", "baseline_value": 717.6862990589219, "alternative_value": 717.6870158202053, "change": 0.0007167612833427484}, {"question": "SMe source basin versus lowest observed gas endpoints", "baseline_value": 717.6862990589219, "alternative_value": 722.948233540958, "change": 5.261934482036054}, {"question": "SMe fixed-source-basin SuperFine/VeryTight versus original integration/SCF", "baseline_value": 198.52774300315915, "alternative_value": 198.5285149683017, "change": 0.0007719651425475149}, {"question": "SMe source basin versus lowest observed gas endpoints", "baseline_value": 198.52774300315915, "alternative_value": 198.52833374059858, "change": 0.0005907374394382714}, {"question": "SMe CPCM H electronic reference rather than gas-H reference", "baseline_value": 195.39252886530033, "alternative_value": 195.33715492491618, "change": -0.05537394038415755}, {"question": "OMe fixed-source-basin SuperFine/VeryTight versus original integration/SCF", "baseline_value": 740.8208103542012, "alternative_value": 740.827746924315, "change": 0.006936570113794005}, {"question": "OMe source basin versus lowest observed gas endpoints", "baseline_value": 740.8208103542012, "alternative_value": 746.9761577295917, "change": 6.155347375390534}, {"question": "OMe fixed-source-basin SuperFine/VeryTight versus original integration/SCF", "baseline_value": 172.5946171256653, "alternative_value": 172.58895661666622, "change": -0.005660508999085323}, {"question": "OMe source basin versus lowest observed gas endpoints", "baseline_value": 172.5946171256653, "alternative_value": 172.5946171256653, "change": 0.0}, {"question": "OMe CPCM H electronic reference rather than gas-H reference", "baseline_value": 168.81534692263543, "alternative_value": 168.7599729824005, "change": -0.05537394023491515}]

## 自旋与回顾检验

Hirshfeld分区不重叠且覆盖全部原子，总spin≈1；SMe硫自旋与全部杂原子分项见quality。无硫成员报告null，不伪造测量0。双重态S²annihilation前后逐native检查。

Computed Cl-minus-H D_e=17.895284760kJ/mol, opposite to monotone single-descriptor prediction. Its I_e difference has opposite sign.

Cl挑战是已经接触原文和旧结果后的回顾性检验，未声称盲预测。

## evaluator、复用、消耗和剩余问题

AR/PR全部5关键点、结论、6scoringrules和3criticalfailures逐条对照evaluator_mapping.json。全部recordID和原生日志/几何/代码路径解析，两套schema检查通过。实际验收由身份、模式、能量、对照与科学推论共同给出。复用6项独立旧原生计算（4分子端点、H与SMe自旋SP），节省等量重复作业；历史未知核时不估计。新增尝试33，已记录完成分配核时36.6054，包含失败/恢复记录，AR/PR不重复计费。

所有计划内必要端点已完成。限制：有限OH采样、同一主泛函、均相连续介质、纯电子描述符；未模拟完整光/电/黄素催化体系，不推断产率或势垒。

证据入口：results.json、benzyl_evidence.json、validation/benzyl_quality.json、validation/contract_checks.json、resource_summary.json；每个calculationrecord含原生日志和几何，可独立复算。

