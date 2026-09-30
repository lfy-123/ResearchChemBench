# paper_72822e4ddb5d9b11 — Ni 配合物：闭壳层、三重态和 BS 竞争

状态：`implemented_pending_expanded_reference`；类别：A → B；AR/PR 均已完成开发实施。

## 科学升级

保持完整 165 原子 C87H72Cl2N2NiO 中性配合物；B3LYP/BP86 分别尝试 CS、三重态和至少两个独立 BS 起点，提交占据、自旋布居、波函数稳定性及振动证据，分离垂直与绝热能差。显式允许有证据的 BS 坍缩而非虚构第二极小点。

## 实际核读正文/SI

正文第 4 页；SI 第 10–11 页电子态讨论和第一配位层 def2-TZVP/其余 def2-SVP 方法。核查 165 原子对应 489 个内部振动自由度。

## 评估改动

由旧单一绝热标量改为双方法电子态矩阵和固定几何控制。BS 失败不能证明闭壳层正确；只有结构、占据和收敛诊断支持的坍缩才可关闭候选。

## 可行路线和最低先导

Gaussian/ORCA 波函数与频率路线可用；先完成完整模型的 CS/T/两 BS 起点先导和第一配位层映射。

## 限制和新增参考缺口

新 BS、稳定性及双方法配对参考仍缺；频率须与声称极小点的电子面和方法一致。

## 提交和验证入口

命名结果面板：`state_matrix`、`geometry_control`、`interpretation`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_72822e4ddb5d9b11`；payload SHA256 `9ebeae83153575894bfa9c077afa44e9c073988d6b0929ff91eac75e22dd4b1c`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_72822e4ddb5d9b11`；payload SHA256 `bb3e2a9353f12c5070a30baa400a6f85c560e2011bb315f0e1db82cc7da99065`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
