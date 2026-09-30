# paper_d8e5490cd9942f4f — La/Tb/Lu：构象、替换和配位水循环

状态：`implemented_pending_expanded_reference`；类别：A → B；AR/PR 均已完成开发实施。

## 科学升级

以完整 La 源图建立 La/Tb/Lu × syn/anti × 0/1 水矩阵，加入冻结 La 骨架金属替换和松弛配位水循环。提供正式数值 ECP/基组：La46/Tb54/Lu60 核、各 11 个显式中性原子电子，(7s6p5d)/[5s4p3d]。严格区分伪单重态与真实 Tb 4f 自旋；水脱离允许证据化分支。

## 实际核读正文/SI

正文第 3/5 页；SI 第 21–22 页 ECP/热化学、水循环与第 33 页参考 13。进一步取得源 University of Cologne MWB 系数并保存来源、内容哈希、核电荷及收缩审计。

## 评估改动

以同金属 syn/anti ΔG、固定骨架响应和原子守恒水循环代替跨金属裸总能，明定 298 K/标准态和低频处理。周期赝势安装不能替代该分子 ECP；输入系数核查不冒充引擎或极小点验证。

## 可行路线和最低先导

原数值基组/ECP 缺口已由正式文件解除；下一步为 Gaussian/ORCA 解析、电子数核对、La 极小点/频率及 Tb 单点先导。

## 限制和新增参考缺口

引擎解析、最低点、扩展水合热化学与误差仍未运行，因此保持 pending_reference。无完整交换循环不宣称定量金属萃取选择性。

## 提交和验证入口

命名结果面板：`conformer_hydration_matrix`、`replacement_and_cycles`、`ecp_and_sensitivity`。

两个模式必须提交 `report/results.json`、`report/report.md` 及实际原始产物。五份科学 evaluator、公开对象和 schema 相同，仅 PR 的作者研究指导增加路线信息。

- autonomous_research: `tasks/upgrade_tasks/autonomous_research/paper_d8e5490cd9942f4f`；payload SHA256 `e45ed3142ea20dd1f4b9f1d64684f96da3c5fa66f25a499a8f4da605ef884b88`
- paper_reproduction: `tasks/upgrade_tasks/paper_reproduction/paper_d8e5490cd9942f4f`；payload SHA256 `642fc27b2cf164926ef49d5b7ab278104384927c764c19e1321d20a5ccdd80d1`

官方包/运行时/契约与输入身份检查通过；新增科学引擎启动 0，不声明扩展科学通过。旧证据只能按私有源快照审计。
