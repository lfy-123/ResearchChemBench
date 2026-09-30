# paper_eda19e7c8edd4b39 — NiAl：空位、表面偏析和新相的闭合循环

状态：`implemented_pending_expanded_reference`；类别：A → B；AR/PR 均已完成开发实施。

## 科学升级

由两空位标量扩为 B2 的 2×2×2/3×3×3 缺陷、(100) Ni/Al 终止与 (110) 混合表面，以及 L12 Ni3Al 候选的统一化学势比较。定义体相移除—slab 加入的守恒循环、7/9 层和 15/20 Å 真空敏感性。补 B2/L12 理想起点并明说不是源 CIF。

## 实际核读正文/SI

正文第 6–8 页 Figure 6/方法；取得正式 Nature Communications SI 41467_2025_67397_MOESM1_ESM.pdf 并核读表面偏析段。仓库 supplementary_001 是同行评审文件，不能替代正式 SI。正式 SI 的析出前基体 Al 偏析在 PR/私有证据中准确保留，AR 不预告赢家。

## 评估改动

分别评估体相空位、洁净基体偏析和 Ni3Al 热力学，重算原子数/化学势和能量基准；拒绝由两空位能推出普遍 Ni 偏析、忽略终止面或将静态能量等同析出速率。

## 可行路线和最低先导

GPAW/QE 与 ASE；先验证元素/B2 参考、一个空位和混合 (110) 的守恒循环，再扩终止面/相。

## 限制和新增参考缺口

PAW/基组/k 点/展宽先导和全部新增 slab/相参考未运行；理想晶格不代表已收敛平衡结构。

## 提交和验证入口

命名结果面板：`bulk_vacancies`、`surface_cycles`、`phase_and_convergence`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_eda19e7c8edd4b39`；payload SHA256 `1838bce53b6bc4d906bcc7535f10d760121cfe69a6c4af2da604a1c4d04aa0ba`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_eda19e7c8edd4b39`；payload SHA256 `e60009455936b8249f51dcad912b3260d29e60099f62098ba29b39237fb5d684`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
