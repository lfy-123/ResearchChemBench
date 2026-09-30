# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:31:58.879296+00:00。论文 `paper_2f0a4f80a37fbccd`；模式 `PR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_2f0a4f80a37fbccd/PR/b41905e567b5f656b248e8a9c4db2bff8846150970cfec84865406ea43c56c6b`。历史final快照保持不变。

## 已完成端点

- five_full_identity_minima
- eta1_eta2_competition
- relative_ligand_geometry_alternatives
- native_modes_and_nitrate_PPh3_mixing
- four_and_five_band_comparisons
- uniform_scale_sensitivity
- bounded_candidate_set

## 适用范围与限制

- 作者知情的参考验证，非盲AR。有限五起点而非全局构象穷尽；气相B3LYP/LANL2DZ含ECP，无显式自旋轨道/晶体堆积/固态环境。统一0.96/0.98/1.00比例只测试敏感性，不能消除方法与固态误差；没有预设任意光谱通过容差，没有以缺峰降低RMSE后宣布胜者。电子能与谐振G分别保留，但不推断固态群体或氧/NO生成路径。

## 本次真实计算报告

# Ir 硝酸根配位：科学验证报告

更新：2026-09-28T13:27:18.129773+00:00。当前冻结第一版；作者知情参考验证。

## 结论

在完整分子B3LYP/LANL2DZ有限构型搜索中，最低eta2比最低eta1低65.264 kJ/mol，支持eta2的气相电子稳定性；但稳定eta1极小值确实存在，且统一光谱匹配有未匹配观测、显著残差及配体混合，不能仅靠这些KBr峰唯一确定配位模型或相对配体排列。

## 构型和驻点

|初始候选|最终配位|相对电子能(kJ/mol)|Ir–O三距离(Å)|Cl–Ir–Cl/P–Ir–P(°)|

|---|---|---:|---|---|

|ir_nitrato_b3lyp_lanl2dz_optfreq|eta2|12.9309|2.1771/2.1871/3.8787|170.27/99.41|

|eta1_O7_release|eta1|72.0380|2.0502/4.0900/3.4137|166.90/101.80|

|eta1_O8_release_recovery2|eta1|65.2637|4.1567/2.0551/3.3458|164.41/103.74|

|eta2_cisCl_transP_release|eta2|0.0000|2.1940/2.1431/3.8786|93.68/176.62|

|eta2_cisCl_cisP_release|eta2|36.6216|2.2528/2.1350/3.8947|89.46/105.31|

全部75原子、两完整PPh3、两Cl及完整NO3保留；各219内部模式均为正。原生ECP显式电子318（159α/159β），与全核418之间100个芯电子差有明确记录。所有相对能量采用同一个最低电子能零点；没有把气相电子偏好换算成固态比例。

## 同一规则下的光谱比较

原始频率窗口700–1650 cm⁻¹；硝酸根质量加权位移分数≥0.15才进入一对一匹配。先保留unity，再以0.96和0.98统一缩放重算。并列报告1532/1261/1223/802四峰与额外1561五峰，不选有利来源。

|候选|观测数|匹配数|原频率RMSE(cm⁻¹)|未匹配观测|

|---|---:|---:|---:|---|

|ir_nitrato_b3lyp_lanl2dz_optfreq|4|3|102.903|1261|

|ir_nitrato_b3lyp_lanl2dz_optfreq|5|3|102.903|1561,1261|

|eta1_O7_release|4|4|112.324||

|eta1_O7_release|5|5|177.838||

|eta1_O8_release_recovery2|4|4|187.689||

|eta1_O8_release_recovery2|5|4|187.689|1561|

|eta2_cisCl_transP_release|4|4|196.222||

|eta2_cisCl_transP_release|5|4|196.222|1561|

|eta2_cisCl_cisP_release|4|3|97.595|1261|

|eta2_cisCl_cisP_release|5|3|97.595|1561,1261|

残差只覆盖成功匹配的观测。较少模式不能因RMSE较小就获得优先；全部未匹配项保留为证据缺口。全1095个正常模及N–O有符号投影见ir_all_modes.csv和mode_analysis，未入选模式同样保留。

## 真实对照与解释

相同组成的Cl/P位点重新排列并完整释放，实际改变了最低电子构型及振动混合；两个独立eta1起点均有真实极小值，因此不能宣称eta1不存在。晶体结构证据与本次自含分子/IR问题的证据权限区分；本文不借晶体答案替代当前反例搜索。

所有比例敏感性数值及构型能量变化见results.sensitivity。没有为任一峰单独拟合比例，也没有预设任意RMSE阈值强行通过。

## 来源、资源与限制

作者知情的参考验证，非盲AR。有限五起点而非全局构象穷尽；气相B3LYP/LANL2DZ含ECP，无显式自旋轨道/晶体堆积/固态环境。统一0.96/0.98/1.00比例只测试敏感性，不能消除方法与固态误差；没有预设任意光谱通过容差，没有以缺峰降低RMSE后宣布胜者。电子能与谐振G分别保留，但不推断固态群体或氧/NO生成路径。

复用1个源eta2原生日志并重新审查；新增引擎实际启动6次，已测总作业时6.596h，已测分配核时131.930。未知中断耗时不填零；AR/PR共享物理结果。两套schema、引用文件、记录ID和当前冻结包哈希均通过；evaluator_mapping逐条对应科学证据。

入口：report/results.json、validation/ir_quality.json、validation/contract_checks.json、resource_summary.json、ir_all_modes.csv；完整原始失败/恢复记录保留在outputs和provenance。

