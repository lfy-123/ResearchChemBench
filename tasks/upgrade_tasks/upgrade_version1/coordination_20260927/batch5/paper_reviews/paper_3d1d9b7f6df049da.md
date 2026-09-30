# paper_3d1d9b7f6df049da — Y₂ 富勒烯：模式特异的磁张量导数

状态：`implemented_pending_expanded_reference`；类别：B → 加强B；AR/PR 均已完成开发实施。

## 科学升级

保留两个笼型的 96 原子 C87H7Y2 中性双重态，明确 Y 的 81/82 行映射。侧向模式候选与纵向/笼振动负对照分别做 ±h、±h/2，提交共同坐标系中的完整 g/A 张量导数、旋转协变核查，以及 20/100 K 的 Bose 占据与 n(n+1) 代理量。

## 实际核读正文/SI

正文第 3、8–10 页与 Figure 7；SI 第 2 页方法、第 20–26 页 Table S3、Figures S16/S17；同时核查原始公开坐标和电子奇偶。

## 评估改动

要求真实模式投影、步长收敛、张量框架和负对照，而非只复述侧向运动解释。坐标轴旋转造成的假导数与不同本征向量错配属于科学错误。

## 可行路线和最低先导

源方法包含 ORCA 的 PBE/def2-TZVP 与 Y ECP 几何、PBE-ZORA EPR；先验证一个双重态、侧向本征向量和稳定张量再扩展。

## 限制和新增参考缺口

新模式矩阵、负对照与导数误差未运行；不要求也不声称从这些静态代理量算出 T1/T2 或定量弛豫寿命。

## 提交和验证入口

命名结果面板：`mode_assignment`、`tensor_derivatives`、`thermal_and_frame_controls`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_3d1d9b7f6df049da`；payload SHA256 `efcdd11a7d85567ace2cfa6756831d014284814419ce7d2812db84437a454627`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_3d1d9b7f6df049da`；payload SHA256 `1d427ca9f0fff53733e9f4b4be8bdca754445c16f054483ed44c061bac0cf836`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
