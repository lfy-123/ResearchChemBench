# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:23:37.550508+00:00。论文 `paper_2f2aa11ea61a32bb`；模式 `PR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_2f2aa11ea61a32bb/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_2f2aa11ea61a32bb/PR/279027840290244156cc4a045ddd861bcc781a3cb39d054d1eca1a6c6dd1ca80`。历史final快照保持不变。

## 已完成端点

- relaxed_monomers.1a
- relaxed_monomers.1b
- relaxed_monomers.1c
- relaxed_monomers.1d
- common_geometry.1a_common
- common_geometry.1b_common
- common_geometry.1c_common
- common_geometry.1d_common
- spectral_test.electronic_vs_geometry
- spectral_test.independent_trend
- spectral_test.method_sensitivity

## 适用范围与限制

- Four isolated neutral singlet monomers; no dimer, crystal, white-light color coordinates, yield or radiative/nonradiative kinetics inferred.
- Reference evaluation is source-aware and the1dtransfer test retrospective; never a blind holdout. No individual spectral shift or fitted correction.
- Only8localchelate/F atoms held common; azaarene topologies and remote relaxed geometries differ. Residual contrast is not pure electronic causation.
- Electronic quantities only, no thermal population for constrained structures. Source gas and primarytoluene baselines are distinct.
- X+Y normalized canonical transition densities define NTO/fragmentCT/centroids. Functional dependence of absolute values remains; lowerS1andstronghigherband explicitly separated.
- Unreported experimental uncertainties not invented. Integernm rounding and actual method/linewidth spreads are separately identified and not statistical confidence intervals.
- Retain actual rotation/grid sensitivity and unresolved fine 1c/1d ordering. See outputs/evidence/bf2_quality.json; the nonexistent validation/bf2_quality.json is not evidence.

## 本次真实计算报告

# BF₂ 四单体共同几何与光谱验证

更新：2026-09-28T07:56:34.455986+00:00。作者知情参考验证，公开谱已曝光，1d测试为回顾性。

## 主要结论

1d相对1a的最低吸收带红移在释放几何为-0.3884eV、共同局部螯合骨架为-0.3558eV、CAM方法为-0.3546eV；公开甲苯低能带为-0.3396eV。局部骨架几何变化不足以单独解释红移；该干预不能分离全部外围几何与电子效应。1c最低态弱而较高态强，绝对波长、CT大小及1c/1d精细排序不具同等稳健性。

## 定义与结构

主文Fig2/Table1的甲苯低能吸收带345/375/383/381nm；1c另有339nm较强高能带。源B3LYP/6-31+G(d,p)气相路线单列，主比较新算共同甲苯。完整中性单重态1a C11H8BF2NO和1b/c/d C15H10BF2NO的连接图逐个核验。

## 端点与干预

|单体|释放S1(eV)|f|D(Å)|共同局部骨架S1(eV)|形变E(kJ/mol)|CAM S1(eV)|公开低能带(eV)|
|---|---:|---:|---:|---:|---:|---:|---:|
|1a|3.4896|0.1736|2.5193|3.4896|0.0000|3.9216|3.5937|
|1b|3.1813|0.2346|2.4002|3.1379|6.0900|3.5921|3.3062|
|1c|3.1011|0.0179|3.7582|3.0620|1.0820|3.7432|3.2372|
|1d|3.1012|0.2256|2.8370|3.1338|7.2925|3.5670|3.2542|

1a本身为共同参考，零形变是同一真实计算的恒等关系。其他成员约束同8个B/N/O/螯合碳/F坐标并释放其余坐标；全分子原子映射不能强行跨不同稠合图使用。冻结点不作自由极小值或热权重。端点态重叠采用重新实算的纯刚体对齐基态，避免将坐标旋转误判为态交换。

## 光谱、趋势和误差

1d−1a释放/共同/CAM/实验=-0.388400/-0.355800/-0.354600/-0.339566eV；局部几何贡献-0.032600eV。回顾性预测残差-0.048834eV，真实方法响应差0.033800eV。公开整数nm打印分辨率按±0.5nm传播的界0.009481eV只表示舍入，不能替代未报告的实验误差。

全部低10根列于CSV，共同高斯线宽σ0.10eV并比较0.05/0.15。低能峰1d−1a差分别{'0.05': -0.38850000000012974, '0.1': -0.38850000000012974, '0.15': -0.3890000000001299}；峰位置及强度全表和原始曲线保留。1c弱S1不能代表全谱最强峰，CAM及线宽可使低能弱峰合并；不宣称所有方法下均分辨。

CT以完整X+Y跃迁密度的空穴/电子一阶矩及Loewdin片段转移计算，基组/规范正交性和积分均核验；NTO权重与十态密度保留。方法变化显著改变CT距离和绝对跃迁能，1c/1d约0.0001eV的B3LYP差不支持稳健精细排序。

## 刚体旋转的数值敏感性

|单体|旋转后的基态能量差 (kJ/mol)|十根最大激发能差 (eV)|
|---|---:|---:|
|1b|-0.024197|0.000300|
|1c|-0.059307|0.000700|
|1d|+0.013886|0.000200|

主网格并非严格旋转不变。形变能采用与约束点相同对齐坐标系的释放基准；原坐标系值仍保留在质量记录。对残差最大的 1c，实际加密至 SuperFineGrid 并收紧 SCF 到 Conver=10，旋转能量差为 -0.064690 kJ/mol，十根最大旋转差为 0.000600 eV。这是数值敏感性测量，不是将结果强行修正到零；约 0.0001 eV 的 1c/1d 主方法排序没有足够稳健性。

## 限制与验收

- Four isolated neutral singlet monomers; no dimer, crystal, white-light color coordinates, yield or radiative/nonradiative kinetics inferred.
- Reference evaluation is source-aware and the1dtransfer test retrospective; never a blind holdout. No individual spectral shift or fitted correction.
- Only8localchelate/F atoms held common; azaarene topologies and remote relaxed geometries differ. Residual contrast is not pure electronic causation.
- Electronic quantities only, no thermal population for constrained structures. Source gas and primarytoluene baselines are distinct.
- X+Y normalized canonical transition densities define NTO/fragmentCT/centroids. Functional dependence of absolute values remains; lowerS1andstronghigherband explicitly separated.
- Unreported experimental uncertainties not invented. Integernm rounding and actual method/linewidth spreads are separately identified and not statistical confidence intervals.

AR/PR同一物理结果；两套原始schema、live冻结SHA、所有引用文件和calculationIDs通过。新原生引擎启动27次，已测分配核时47.9734；失败和中断原件保留、未知耗时不填零。复用4个气相优化频率，旧新资源不重复计。

详见report/results.json、outputs/evidence/bf2_quality.json、bf2_state_table.csv、bf2_spectral_peaks.json、evaluator_mapping.json。

