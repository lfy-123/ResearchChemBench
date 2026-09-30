# paper_c23cfabbd34b087f — PAH：拓扑、取代、几何与开壳层竞争

状态：`implemented_pending_expanded_reference`；类别：A → B；AR/PR 均已完成开发实施。

## 科学升级

公开四个 1M/2M × OMe/TIPS 源模型的图和同拓扑公共骨架映射，比较 CS/BS/T 与独立占据诊断，再做冻结公共骨架的取代干预和代表高层校准。明确源计算 TIPS 模型是 C≡C–SiH3，1M/2M 差 C2H2；2M′ 是氧化对象而非另一构象。

## 实际核读正文/SI

正文电子/光学讨论；SI 第 42 页起计算方法和四模型坐标段。只保留图身份，不把原闭壳层坐标块来源或状态赢家公开。

## 评估改动

检查同式/同能量基准的态差、冻结骨架与松弛效应，并结合多参考诊断解释光谱。禁止跨分子式总能排序、错误 TIPS 全分子或默认 BS 代表真实单重态。

## 可行路线和最低先导

Gaussian/ORCA 稳定性/TD 及必要代表 CASSCF；先验证一个 1M 和一个 2M 状态组与 MCS 映射。

## 限制和新增参考缺口

新增各态极小点、冻结干预和校准参考未运行；所有新图只是输入，非优化证据。

## 提交和验证入口

命名结果面板：`relaxed_series`、`frozen_scaffold`、`calibrated_interpretation`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_c23cfabbd34b087f`；payload SHA256 `b1b85e8d183c8201ba833ff1f975bdc20681fc9b515c561fbdd42f9ee08e5680`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_c23cfabbd34b087f`；payload SHA256 `5aea85a45722a8db77daa85ef4f35dbb9e0e4ffea10367dc9a53e79d8d724eb0`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
