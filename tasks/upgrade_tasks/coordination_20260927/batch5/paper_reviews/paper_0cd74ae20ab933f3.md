# paper_0cd74ae20ab933f3 — Cu₂ 交换：轴向取代、几何与自旋模型

状态：`implemented_pending_expanded_reference`；类别：B → 加强B；AR/PR 均已完成开发实施。

## 科学升级

保留完整四桥 paddlewheel，建立 H/Me/OMe 三系列各自松弛核与公共 Cu₂O₈C₄/轴向 N 核的六格比较。三重态和破缺对称态保留 S²、投影、局域自旋及真实输出；代表 R_H 另作可调用的 CASSCF 或自旋翻转校准。以 J=E_S−E_T、H=−J S₁·S₂ 和三重态简并度 3 统一定义，分离取代的电子效应和几何效应。

## 实际核读正文/SI

正文 PDF 第 6–7 页 Figure 5、式 1–2；SI 第 5–6 页计算方法、第 35–36 页 Table S4 的 SF-TDA/SF-TDDFT/CASSCF 比较。原运行 J 与文献锚点的差异保留在私有快照，不作为新版正确值。

## 评估改动

重点检查六格对象一致性、投影和符号/因子、同几何高层校准及差值的不确定性。只交旧 J 或布居标量、忽略自旋污染、强排小于误差的排序均不能完成。

## 可行路线和最低先导

可走 ORCA BS-DFT/CASSCF 或已确认可调用的自旋翻转路线；先验证一个 R_H 的 BS/三重态和参考态。专用 PySCF-forge 实现不假定存在。

## 限制和新增参考缺口

公共核、三系列新增输出与高层不确定性未计算；孤立分子的交换不能证明材料热致变色。

## 提交和验证入口

命名结果面板：`exchange_matrix`、`spin_calibration`、`effect_comparison`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_0cd74ae20ab933f3`；payload SHA256 `a629d126584c9f1c87af819b854d94c90e96199a6d6690dbcb2d382479d9ebdf`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_0cd74ae20ab933f3`；payload SHA256 `660462b028ca913c75bcf16c04c698da6f969f2444c085b72d87f7ed668e459e`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
