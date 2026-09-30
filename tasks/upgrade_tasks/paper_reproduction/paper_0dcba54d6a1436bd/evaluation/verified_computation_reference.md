# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:23:30.801092+00:00。论文 `paper_0dcba54d6a1436bd`；模式 `PR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_0dcba54d6a1436bd/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_0dcba54d6a1436bd/PR/dbb481ebcc731ac0dea46b23f23525c059aee019a1302452dcbfb4e93d92aacc`。历史final快照保持不变。

## 已完成端点

- three_full_Z_identities
- three_source_minima
- nine_common_torsion_constrained_geometries
- 120_primary_states
- 60_CAM_states
- mapped_atom_density_correspondence
- same_angle_acceptor_contrasts
- two_method_matched_branch_sensitivities

## 适用范围与限制

- ThreecompleteisolatedZmonomers, gasB3LYPgeometries andcommonPCMDCMverticalresponse. Finite3anglelocalconstraintset, nofree-minimumpopulations forgridpoints. M06/CAMsystematicspreadisactualsensitivitynotconfidenceinterval. Atomprobabilitymatchingdiscardsphase; use onlyreciprocalcharacterbranchesanddiscloseambiguousstates. CrossacceptorcomparisonisCTtypefamily, notidenticalmany-electronwavefunction. Noemission,aggregation,quantumyield,photostabilityrates ordevicepredictions. Source-awareverificationnotblindAR.

## 本次真实计算报告

# 三受体发光分子：几何与激发态验证

更新：2026-09-28T07:18:54.606172+00:00。当前冻结契约AR/PR共用实际物理证据；作者知情，非盲AR。

## 结论

共同15/45/75度网格下，受体种类和扭角均影响低能态。M06的受体CT支路随15→75度变蓝，NPC/AQ/PQ分别为0.2215eV, 0.0642eV, 0.0404eV，而PQ局域态近乎不变并与CT支路交换根编号。相同角度的受体CT能量仍不同，纯几何或纯受体单因素都不足。CAM保留可核验的局域/CT区分但改变排序和响应大小，不能把各条件S1混为同一态。

## 作者路线与身份

SI17–24页给B3LYP/6-31G(d,p)气相S0坐标/方法，26–29页M06/PCMDCM跃迁。完整NPC C43H39N3O2，AQ/PQ C41H32N2O2；同分子式AQ/PQ连接不同。全部端点重建canonicalisomericSMILES和唯一Z双键、核对全烷基链/电子数。复用NPC/AQ各一次OptFreq，PQC独立源坐标优化。

## 共同比较

三个自由端点及每个15/45/75度网格均实际计算；三角度在productionTD前固定，NPC45为先导。约束只固定映射受体连接扭角，其余自由度释放，原生日志与实测角度保存。约束点不作自由极小值或统计布居。

|成员|15→75 CT支路根|ΔE(eV)|Δf|
|---|---|---:|---:|
|NPCZCS|1→1|0.2215|-0.7088|
|AQCZCS|1→1|0.0642|-0.2300|
|PQCZCS|1→2|0.0404|-0.1889|

## 态匹配、根交换与敏感性

M06 下，PQ 的 CT 支路由 15° 时的根 1 变为 45°/75° 时的根 2；受体局域支路则由根 2 变为根 1。NPC 的高强度骨架支路也发生根编号变化。CAM 下 AQ 的 CT 支路从 15° 的根 1 变为 75° 的根 4；NPC 大角度下出现更强的态混合。因此，完整十根结果保留，模糊高态不强制一一配对。

各态保留完整X+Y幅度、规范MO、NTO权重、3×3片段转移矩阵和实空间空穴/电子质心。跨角度的空间AO重叠可很小，未隐藏；受体的空间转动会降低这类重叠。补充的完整原子转移概率Bhattacharyya²以相同原子顺序比较，取互为最佳的CT/LE特征支路，竞争根和相似度均保存。这是概率特征对应，不证明波函数相位一致；不对模糊高态强配对。跨不同受体使用同语义三片段CT类型，不能强称不同分子拥有同一多电子态。

|受体及支路|M06 的 75°−15° (eV)|CAM 的 75°−15° (eV)|方法差 (eV)|
|---|---:|---:|---:|
|AQ 电荷转移|0.0642|0.4691|+0.4049|
|PQ 受体局域|-0.0018|-0.0015|+0.0003|

两端分别以同几何的双向 AO 跃迁密度重叠进行跨方法匹配。AQ 的 CT 响应对泛函明显敏感；PQ 的局域支路在两种方法下都几乎不变。表中方法差是实际计算敏感性，不是统计置信区间。完整对应根、重叠矩阵及原始文件列于结果 JSON。

所有主网格至少S1–S5且实际给出10根。PQ的15度CT根1到45/75度根2；局域根反向交换。M06与CAM同几何AQCT端点由实际AO密度互为最佳匹配，响应差真实量化。NPC在CAM大角度下CT字符混合更强，报告只保留该限制，未拿一个根编号假造不变排序。

## 验收、资源与限制

结论限于完整 Z 单分子、气相 B3LYP 基态结构与共同 PCM(DCM) 垂直响应。三个角度构成有限局部网格，不能作为约束点的热布居，也不代表完整旋转势能面。概率态匹配舍弃相位，跨受体只比较同类 CT 特征；方法依赖及模糊高态均保留。此处没有计算发射、聚集、量子产率、光稳定性速率或器件性质。验证已阅读来源资料，不能称为盲测。

AR/PR两套schema、实际证据路径和recordIDs通过；livepackage与冻结SHA一致。所有keypoints、rules、criticalfailures逐条见evaluator_mapping.json。新原生启动28，已测原生分配核时147.0325，后处理单列，历史未知不估算。

证据入口：report/results.json、validation/emitter_quality.json、emitter_state_table.csv、resource_summary.json。保留原始谱/密度/完整网格/方法反例，可独立重算。

