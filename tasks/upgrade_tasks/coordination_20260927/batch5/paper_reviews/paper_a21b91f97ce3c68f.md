# paper_a21b91f97ce3c68f — 有机锡：几何干预与标量耦合分解

状态：`implemented_pending_expanded_reference`；类别：A → B；AR/PR 均已完成开发实施。

## 科学升级

给出 6/7/13 三对完整三正丁基锡模型，分别对应 thp、1,3-dioxan-2 和 1,3-dithian-5；明确 Sn/13C 与相连扭转四元组。对轴/赤道构象计算有符号 119Sn–13C 耦合及 FC/SD/PSO/DSO，并设置固定 Sn–C 距离的 ±30° 扭转和固定扭转的 ±0.03 Å 距离干预。

## 实际核读正文/SI

正文超共轭讨论；SI 第 2 页方法、Table S3（第 5–6 页）配对定义。源方法明确采用非相对论哈密顿量，TZP-ZORA 是基组名，不能仅凭名字称已作 ZORA。

## 评估改动

绑定 signed-J 分量、同定义平均、几何保持条件和轨道分析，不接受只由键长相关性断言超共轭因果。NBO3.1 或有验证的替代局域化可用，不强加新商业服务。

## 可行路线和最低先导

需先在已配置分子软件中验证一完整对、同位素符号和耦合基组/轨道分析，然后扩干预网格。

## 限制和新增参考缺口

新增受限 J 网格与相对论/基组敏感性未跑；跨哈密顿量数值不共享旧容差。

## 提交和验证入口

命名结果面板：`pair_matrix`、`geometric_interventions`、`mechanism_test`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_a21b91f97ce3c68f`；payload SHA256 `b74a31c5613cfcd16c4a00284b061832eee97b4ea2e28de0bc27ec27d19f1e28`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_a21b91f97ce3c68f`；payload SHA256 `c0d856037fd7a35b557cb62832876afd998d62e48bd6e0482750ad0f5b925c0e`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
