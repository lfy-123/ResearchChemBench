# paper_e31cc7bc7b21b610 — Ir–Ir：真实二核模型、截短与片段干预

状态：`implemented_pending_expanded_reference`；类别：A → B；AR/PR 均已完成开发实施。

## 科学升级

补全 Egan C44H52N2O6 与每配体四个 tBu→H 的 egan C28H20N2O6 映射，构建完整/截短二核 C88H104Ir2N4O12 与 C56H40Ir2N4O12 成对任务。规定 N/O 配位、局部螺旋起点和中性双重态片段；用 Eint/Edef/Eassoc、0.2/0.5 Å 分离和 30° 扭转、占据/自旋及密度交叉检验成键。

## 实际核读正文/SI

正文第 3 页计算、合成分子式及第 7–9 页成键讨论；SI 第 27–30 页实际是 54 原子 Hap4Ir2，不是上述完整/截短 Egan 配对的现成参考。原单核标量及单位问题保留私有，退出当前目标。

## 评估改动

必须完整/截短配对、固定片段电荷/自旋/相对论和同定义能量分解；单一键级或旧单核排序不足。C2h 鞍点不冒充极小点，Hap 另模型不充当新参考。

## 可行路线和最低先导

Gaussian/ORCA 相对论与 Multiwfn，强关联诊断后决定高层校准；先验证一完整/截短对和片段态。

## 限制和新增参考缺口

所有新二核最低点与片段分解未计算；仅构建了可审计图、映射和受控实验定义，不暗示 Ir–Ir 已成键。

## 提交和验证入口

命名结果面板：`dimer_states`、`fragment_interventions`、`bonding_evidence`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_e31cc7bc7b21b610`；payload SHA256 `17c1b1a3111f22d8d2b348de881f346a5fe05bfc7a8633cc40c531e3e43c8db1`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_e31cc7bc7b21b610`；payload SHA256 `829a1a30c2be0e91e1dbca0d9e55a64f1a6bf4ecfc939e6ccda865db11b913ef`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
