# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:23:23.031648+00:00。论文 `paper_628af8d0bf0a1bfe`；模式 `PR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_628af8d0bf0a1bfe/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_628af8d0bf0a1bfe/PR/7af33cc514b4ba6323b7777030330150ae250f6e651685aa77773da6c7bc74d6`。历史final快照保持不变。

## 已完成端点

- identity
- relaxed_minima
- fixed_core_controls
- 84_native_tensors
- BLA
- 12_causal_contrasts
- basis_sensitivity
- rotation_sensitivity

## 适用范围与限制

- Finite gas-scaffold magnetic response with frozen commoncore and separately frozen periphery. No current-density,crystalpacking,excitedstate,reactivityoruniversal aromaticityclaim. Limited basis andquadraturetests are explicit; no forcedreplication ofsource23.6/19.2ppm.

## 本次真实计算报告

# 4a/4c pentalene 科学验证报告

更新时间：2026-09-28T04:43:08.379995+00:00。作者知情参考验证；AR/PR共用物理证据，非盲AR。

## 科学问题与作者路线

SI方法为M06-2X/6-31++G(d)优化频率及6-311+G(2d,p)GIAO；旧小分子身份错误结果排除。正文较小屏蔽基组作为显式敏感性，而非静默混算。完整4a=C36H14F12S2(64原子)、4c=C34H22O2S2(60原子)，两个五碳环与8个独立核心碳严格映射。

## 真实结果

完整4a的法向去屏蔽响应在松弛及相同8碳核心条件下均强于4c，全部12个成对探针对比保留正号。固定核心后差异反而增大，故核心几何差异不能单独解释取代关联；外围构象与非局部磁响应仍是归因限制。BLA和正NICS支持这一有限骨架的反芳香性讨论，不证明普适芳香性或反应性。

|条件|±1.0Å两环均值|±1.7Å两环均值|±2.3Å两环均值|

|---|---:|---:|---:|

|4a_commoncore_grid|65.938430|24.264898|9.694637|

|4a_relaxed_basis_sensitivity|63.589411|23.014413|9.044427|

|4a_relaxed_grid|63.584359|23.168517|9.124276|

|4c_commoncore_grid|53.728023|18.417737|6.555975|

|4c_relaxed_basis_sensitivity|55.561810|19.092460|6.886577|

|4c_relaxed_grid|55.396565|19.192122|6.958576|

|4c_rotated_grid|55.329048|19.134272|6.905980|

均值单位ppm，完整84个原始3×3张量、单环、单侧值和坐标均保留。共同核心由预先对齐的两核心平均，在2026-09-27T12:46:48Z冻结。外围分别固定于原松弛坐标，没有声称控制全分子所有几何。

BLA：4a_relaxed_grid=0.101166075A; 4c_relaxed_grid=0.094315505A; 4a_commoncore_grid=0.097741266A; 4c_commoncore_grid=0.097741266A。BLA = mean(single-bond-set lengths [(2, 3), (4, 13), (1, 13), (4, 7), (5, 6)]) - mean(double-bond-set lengths [(1, 2), (3, 4), (5, 13), (6, 7)]), A; same mapped topological sets for both full molecules and all controls. Positive means the single set is longer. This is a declared fused-core descriptor, not an alternating perimeter of an odd ring.

在|h|=1.7Å处松弛差3.97640ppm，固定核心差5.84716ppm；几何贡献−1.87077ppm。替代屏蔽基组的松弛差3.92195ppm，差值变化−0.05445ppm；4c整体旋转均值变化−0.05785ppm。方向保持，剩余离散积分误差如实保留。

单正侧1.7Å源可比量单列于validation/nics_quality.json，未混用双侧均值或强行拟合23.6/19.2旧锚点。

## evaluator、契约和证据

全部5个keypoints、结论、6条评分项及3条criticalfailure逐项映射evaluator_mapping.json。AR/PR schema、实际证据路径与记录引用均通过；科学验收依据为原生日志身份、正曲率、固定坐标、张量运算及真实敏感性，不由格式检查代替。

## 复用与消耗

精确复用两套身份修正后的完整分子优化/频率，省去2次同等Opt/Freq。早期低原子数结果不复用为科学端点；不同旧AR泛函和探针定义结果不混入。新增7次完整GIAO响应，完成分配核时79.104。未知历史核时不估算。资源逐作业见resource_summary.json。

## 产物与限制

results.json包含原生日志和XYZ逐记录路径；nics_evidence.json保留所有探针；validation/nics_quality.json含逐坐标/连通性/BLA检查；code/包含本地可重算分析。共同核心几何下外围仍不同，因此可排除核心几何单独解释，但不能宣称唯一纯电子因果分解。没有未完成的必需矩阵计算。

