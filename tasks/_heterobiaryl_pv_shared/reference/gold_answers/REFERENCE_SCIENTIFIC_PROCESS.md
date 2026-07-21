# 论文参考科研过程

这不是作者发布的自动化脚本，而是依据正文、公开输出和所用软件重建的参考流程。

1. 为 P0、P1、P2 建立正确的 P(V) 中间体，检查元素、三维结构、电荷与闭壳层单重态。
2. 在乙醇 SMD 环境中以 ωB97XD/6-31+G(d) 优化候选中间体、产物和过渡态。
3. 进行频率计算：稳定点应无虚频；过渡态应只有一个与目标成键/断键对应的虚频。
4. 从过渡态向两个方向运行 IRC，确认连接到预期中间体和 dearomatized 产物侧驻点。
5. 对 BiPy、PhPy 和竞争 C–O 路径保持一致的数值设置，避免把方法差异误当作路径差异。
6. 在优化结构上运行 ωB97XD/def2-QZVPP 单点能作为独立 DFT 高基组检查。
7. 使用 ORCA 4.0.1.2 进行 DLPNO-CCSD(T)/cc-pVDZ 与 cc-pVTZ 单点并形成 cc-pV(DT)Z 外推结果；核对具体设置应以原始 ORCA 输出为准。
8. 使用 GoodVibes 将频率热修正与高水平单点电子能组合。论文引用 GoodVibes 2.0.1，但当前可访问正文未写明所有后处理参数；本 benchmark 明确固定为 353.15 K（80°C）、1 M 溶液标准态。低频、构象集合和浓度修正必须记录，298.15 K 只能作为独立敏感性分析。发表图数值与重新处理数值应分栏比较，不能默认完全相同。
9. 计算相对 G、ΔG‡、ΔGreact 和路径间 ΔΔG‡。
10. 对关键双质子化路径运行 Wiberg 键级/等价布居分析，并将键级随 IRC 的变化与结构变化对应。
11. 将计算得到的低配体偶联势垒与取代基相对速率、NMR 和 EtONa 实验整合，分别判断决速步骤、选择性决定步骤和不可逆步骤。

对应工具箱 Action：

- normalize_qcschema_molecule
- optimize_geometry
- locate_transition_state
- calculate_hessian
- derive_vibrational_modes
- trace_intrinsic_reaction_coordinate
- calculate_energy
- derive_thermochemistry
- calculate_bond_orders
- parse_quantum_chemistry_output
