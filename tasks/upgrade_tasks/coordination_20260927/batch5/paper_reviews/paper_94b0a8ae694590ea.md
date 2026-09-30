# paper_94b0a8ae694590ea — SWCNT 界面：吸附、功函数与电荷转移

状态：`implemented_pending_expanded_reference`；类别：A → B；AR/PR 均已完成开发实施。

## 科学升级

保留三个完整 2BF/2BT/2C8Ph 分子；补充明确标为基准定义的 (10,10) 理想管，12 重复单元/480 C、轴向周期和 18 Å 横向真空。用完整吸附体、冻结片段和松弛片段分解 Eint/Edef/Eads，报告共同真空基准的功函数及密度差；24 单元配双吸附体检验固定覆盖度的尺寸影响。

## 实际核读正文/SI

正文材料方法的 XFS22 管径/长度及分子 DFT 讨论，SI 第 10、15、20 页分子身份。论文未指定单一手性，新增管结构为 ASE 理想起点而非伪称源 CIF。

## 评估改动

同覆盖度尺寸、k 点/真空和姿态敏感性绑定输出；禁止仅用孤立 HOMO/LUMO、混淆真空能零或把分子间不同式总能直接比较。

## 可行路线和最低先导

ASE 加已配置 GPAW/QE 等周期路线；先验证清洁管和一个 2BF 位姿，再扩三分子。

## 限制和新增参考缺口

未求新吸附极小点、密度或功函数参考；结果仅适用于明确模型，不推材料功率因子、输运或未支持 NEGF。

## 提交和验证入口

命名结果面板：`interface_matrix`、`boundary_controls`、`charge_mechanism`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_94b0a8ae694590ea`；payload SHA256 `6b2f3f08ea530f4362fa8e18a7972d9844fff3178770eedc43d038076acd028b`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_94b0a8ae694590ea`；payload SHA256 `a9490afbdb09d90b5b7b8dd92437e7b9fb7c877acbeba0f00d38a94107a598bc`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
