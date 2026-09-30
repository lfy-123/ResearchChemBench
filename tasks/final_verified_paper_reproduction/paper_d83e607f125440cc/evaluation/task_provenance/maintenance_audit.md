# 2026-09-26 逐包维护记录

论文：`paper_d83e607f125440cc`；模式：`paper_reproduction`。修前基线940d3d04；格式步骤5d18a199。用户已确认复查无新增阻断，并批准按本批清单迁入 final；作者优化TS仍不得公开。

## 原文依据

SI S6、Tables S8/S10/S13/S16，PDF pp34–36；正文的氧化机理解释。

## 问题与实际修复

保留2g已知母体输入和2a自行构建；明确气相绝热电子断键能，+1 doublet母体/+1 singlet去氢片段/中性doublet H，排除主结果中的ZPE/热修正；修复HF方法误写、最低点字段绑定和普通停止/免责声明门槛。

## 成功计算支持

母体/片段四份OptFreq、H单点和Hirshfeld单点共6步骤；S=0.400976，2g/2a电子BDE=198.527743115/172.594617223 kJ/mol。

完整步骤和原始来源见[verified_computation_reference](../verified_computation_reference.md)，尤其当前第7节。不重写历史计算，不把格式样例作为科学证据。

## 输入角色与边界

PR历史结果可直接匹配新schema；AR旧结果缺investigation，只作为同一科学量的验证证据，不补造自主规划。格式测试里的AR investigation是明确标注的synthetic外壳，不是新验证。

## 关键点/结论及评分

保留3个科学关键点、1个科学结论；采用dual_axis_100.scientific_results.v1。普通limitation没有独立得分或必填门槛，实际身份/频率/连接/敏感性职责仍保留。所有结果型关键点已关联主结论，不以增加空洞结论凑数。

## 验收与状态

运行本批维护回归脚本检查真实结果（必要无损字段映射）、明确标注的synthetic格式样例、失败与不完整反例、包/manifest、实际评分适配和仅导出agent_input。科学语义由逐项原文/真实输出核对，不宣称调用过LLM judge或独立agent盲测。实际主机网络/挂载隔离尚未实测。详见[本批汇总](../../../../verified_tasks/MAINTENANCE_REPORT.md)第25节。已按负责人确认迁入对应 final 目录；本记录保留用于审计，当前 final 路径为本包所在目录。

本轮收尾：提交正反例、普通声明缺失/空值、对象顺序及真实结果映射均经 schema 和实际运行器检查；完成/失败不混淆，失败说明不替代未完成科学成果。数值靶和容差与修前基线核对未改。详见本批汇总第25.3节的实际测试数量及未覆盖范围。

## 2026-09-27 已获准的指令/评分冲突修复

修前可恢复基线为 `5dd1e1b8ea1f7efa1a4029834e4a7188ade8d0e8`。再次核对SI S6和真实母体频率输出后，确认旧题面允许等效极小点证据，而schema强迫填写频率数。现将task、schema、kp_minimum、r_minimum统一为频率/等效证据两分支；旧频率格式仍兼容，等效分支要求可查证的驻定性及全部内部自由度正曲率证据，不凭普通优化收敛放行，不要求捏造频率数。删除误入PR的AR调查记录句子，不扩展科学目标。

输入数据、原数值靶/容差、3个关键点与1个结论均未改变。真实6步计算仍支持目标；更新reference第8节及当前规则索引，没有更改历史计算。专项回归为 `tasks/final_verified_maintenance_tools/test_contract_fixes_20260927.py`，全批回归仍为 `test_20260926.py`；实际结果见[汇总第27节](../../../../verified_tasks/MAINTENANCE_REPORT.md#27-2026-09-27-两篇指令评估冲突的获准修复与-group-4-交接)。格式测试不等于科学验证，没有新增QM、完整LLM评分或迁入final。


## 2026-09-27 迁移后当前状态

本包已在 2026-09-27 按负责人确认从 `tasks/verified_tasks` 完整迁入对应 `tasks/final_verified_*` 目录。迁移只改变目录位置及本档案中的相对链接/状态说明；公开输入、提交 schema、evaluator、参考数值、评分容差和私有验证档案未改变。迁移后重新执行包契约、显式 final 加载和 manifest 检查。
