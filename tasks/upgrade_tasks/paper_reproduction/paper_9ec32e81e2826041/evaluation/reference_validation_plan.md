# paper_9ec32e81e2826041 升级范围的参考验证计划

日期：2026-09-27。当前状态：**任务包实现完成；扩展科学范围尚未参考计算验证，不可沿用旧 PASS。**

## 科学范围与来源

锌配合物：色散—构象—吸收的因果链。首版 B 类：Test how dispersion changes conformational energetics and whether the resulting geometry change alters the electronic absorption of Z-cAACCy. Separate the direct energy contribution of the dispersion correction from geometric relaxation, and separate excitation energy, intensity and state identity.

- [main.pdf](../../../../../papers/paper_9ec32e81e2826041/documents/main.pdf), SHA256 `c494b9ed5388f0c6d968d8e80ce851426473aa9779a3c3930927445340195dec`, PDF 页码 5, 6, 7。
- [supplementary_001.pdf](../../../../../papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf), SHA256 `dbb8ec5153da3d86acde2fd320f01cc1bae86bf16cebf2fd2cf835280933d7cb`, PDF 页码 3, 21, 22。

来源核对：SI PDF p3 computational methods; p21 Table S7 and Tables S8–S11. Source DeltaG(coplanar−perpendicular) is approximately −0.1 kJ/mol with D3 and +4.8 kJ/mol without. Source example S1 transitions: perpendicular 3.1097 eV, f=0.0883; coplanar 2.4526 eV, f=0.0132. These are method-specific literature values, not a new full cross-geometry or uncertainty reference.

旧验证仅对应原范围，见[原始证据快照](legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot)。没有覆盖本次新增矩阵。公开数据中的初始几何/身份可授权使用；隐藏参考数值及解答不能注入 agent 输入。

## 可用工具与先导

Gaussian/ORCA 的 Opt/Freq、D3 和 TDDFT；Multiwfn 做 NTO/片段；GoodVibes/Python 热化学复核。

同协议复核两构象 ±D3 的最低点，先导交叉单点与一个态追踪对照；确认低频热修正和态窗口后扩矩阵。

工具已经安装不等于此对象、方法或新增矩阵已被验证。必须记录真实命令/作业次数、单作业核数、墙钟小时和 CPU 核时；本次开发没有运行新的科学引擎，不填写臆测耗时或宣称全范围可通过。

## 逐项建立数值参考

### `conformers`

Two starting families × dispersion on/off, validated basins and 300 K harmonic G.

检查重点：Verify complete identity, starting-to-final family map, stationary points and method-specific signed DeltaG. Evidence-backed collapse is allowed; failed optimizations alone do not establish absence.

### `energy_decomposition`

Diagonal and reciprocal cross-geometry electronic-energy matrix.

检查重点：Recompute dispersion and relaxation components with matched composition and energy zero. No off-diagonal G constructed from unrelated frequencies; no fixed-geometry electronic-density effect falsely attributed to post-SCF D3.

### `transitions`

Root windows and matched NTO/fragment states at representative geometries.

检查重点：Inspect real TD outputs, energies, f values and state matching. Compare wavelength and brightness separately; root ordinal or orbital percentage alone does not establish the optical mechanism.

## 校准与独立验收

1. 按公开边界和 PR 作者基线完成必要真实计算，保留 inputs、引擎输出、结构、波函数/模式/态文件及解析代码。逐个核实组成、态、原子/片段映射、收敛与最低点/约束点身份。
2. 从原始输出独立重算能量差、权重、张量投影、光谱对比或态匹配；为每个扩展 panel 建立机器可读取参考，不能把旧单点结果复制成新增对照。
3. 量化对数值收敛、构象/低频、理论水平和可接受替代方法的敏感性。只有这些真实证据建立后才能填写物理容差、等价实现及允许的未决结论。当前 evaluator 以科学条件和原始证据为规则，未伪造新数值靶值。
4. 用同一公开研究范围试运行 AR 和 PR；检查 PR 能复现作者基线且开展新增对照，AR 不依赖隐藏论文答案。两模式的科学结果评分相同，研究过程可因提供作者路线而不同。
5. 加入反例：只提交旧任务结果、换错分子/电子态、遗漏对照、混淆能量定义、捏造不存在的稳定构象、复制目标数值无日志。应在相应科学项失分；完整且有证据的反驳或歧义应被接受。
6. 依据真实先导成本设置预算；超预算先审查科学范围或方法等价性，不降低对象身份或偷偷替换结果。证据不足时保留 pending 状态。

## 科学错误边界

Dropping the Dipp ligand, mixing energy/free-energy definitions, transferring thermal corrections to cross points, claiming post-SCF D3 changes fixed-geometry density, or equating red shift with larger oscillator strength.

格式检查与科学验证分开。`bounded_failure` 是诚实部分提交，不等于新增任务验证通过。旧范围 PASS、runner completed 或 LLM 得分不能替代以上验收。
