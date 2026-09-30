# 2026-09-29 修后维护审查：paper_3c3d73b8715d5fcd / autonomous_research

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- 原 14 原子混拼 README_coordinates.xyz 原字节移入 evaluation/author_results，并注明不能作为合法计算结构；24 原子 1D 与 12 原子 Rh 二聚体未变。
- 移除 conclusion_limitations/rule_limitations；将能量组装关键点接回 conclusion_mechanism。
- 公开 298.15 K、1,4-dioxane、溶质 1 M/CO 8.5 mM、配平和 exo−endo 符号；完成与早期失败分支分开。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 4→4；结论记录 2→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：kp_process_stationary_points, kp_process_energy_assembly, kp_result_activation, kp_result_endo_exo
- 修后 KP：kp_process_stationary_points, kp_process_energy_assembly, kp_result_activation, kp_result_endo_exo
- 修前结论：conclusion_mechanism, conclusion_limitations
- 修后结论：conclusion_mechanism

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| kp_process_stationary_points / process | Supporting Information, Cartesian coordinates of stationary points, page S44 onward.; Main paper computational methods, frequencies, solvent, high-level single points and standard states. | rule_process_validation: $.candidates | 17 个低层驻点、6 个一虚频 TS、12 个正频端点，10 个有限 IRC 加 TS3 QRC；连接逐项见上。 |
| kp_process_energy_assembly / process | Main paper computational methods, optimization method and basis sets.; Main paper computational methods, frequencies, solvent, high-level single points and standard states. | rule_process_assembly: $.method | 34 组 low→solvent/high 几何配对逐原子一致；统一浓度、温度、CO 配平的复算剖面。 |
| kp_result_activation / result | Main paper Figure 1 discussion, overall activation free energy. | rule_activation: $.observables.cycloisomerization_activation_free_energy_kcal_mol | TS1endo−INT11=22.739173663 kcal/mol，22.8±2.0。 |
| kp_result_endo_exo / result | Main paper Figure 1 discussion, endo/exo-OCM comparison. | rule_endo_exo: $.observables.endo_exo_ocs_transition_state_difference_kcal_mol | TS1exo−TS1endo=7.558219734 kcal/mol，7.5±2.0。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| conclusion_mechanism | kp_process_stationary_points, kp_result_activation, kp_result_endo_exo, kp_process_energy_assembly | rule_final_conclusion: $.conclusion |

## 本包复查结果与科学判断

真实历史 report：通过。本包 12 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**六 TS、十二连接端点和势垒有作者路线证据；TS3 是 QRC 替代有限 IRC，exo 开链端点不等同 endo INT1。替代协议应单独判断可比性，未认证自主盲搜索。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

完整 substrate 1D(24 atom)/Rh dimer(12 atom) 是当前给定反应物，合法；另有未在 task 中说明的 README_coordinates.xyz(14 atom)。其第 1 个 C 坐标来自 SI INT1（物理第 46 页），其余 13 行来自 TS1endo 尾部（第 47 页），是混拼的作者答案结构片段，不是第二个完整底物。两模式均将此文件公开；建议经批准移入 evaluation/author_results 并注明作废/不用，而非继续导出。

低层 Gaussian 16 C.01 PW6B95D3，非 Rh 原子 6-311G(d,p)、Rh def2-TZVP/ECP；气相 Opt/Freq，随后同几何 SMD 1,4-dioxane 单点及 ORCA 6.1.1 ωB97M-V/def2-QZVP 高层单点。17 个物种，全部中性单重态；低层热化学 298 K 解析转换为任务 298.15 K；CO 0.0085 M，其余 1 M。原文正文物理第 3 页给出 INT11 起算 22.8、exo−endo 7.5 kcal/mol，当前各容差 ±2.0。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 4 个关键点、2 个现行结论记录；ID未变。Rh含一个limitation记录，不算第二个科学成果。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| rule_process_validation | kp_process_stationary_points | $.candidates | semantic / expert semantic comparison |
| rule_process_assembly | kp_process_energy_assembly | $.method | semantic / expert semantic comparison |
| rule_activation | kp_result_activation | $.observables.cycloisomerization_activation_free_energy_kcal_mol | numeric / absolute difference |
| rule_endo_exo | kp_result_endo_exo | $.observables.endo_exo_ocs_transition_state_difference_kcal_mol | numeric / absolute difference |
| rule_final_conclusion | conclusion_mechanism | $.conclusion | semantic / expert semantic comparison |
| rule_limitations | conclusion_limitations | $.limitations | semantic / expert semantic comparison |

standalone 规则：无。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | True | 仅格式可提交，不代表科学成功 |

AR 缺事前假设不得编造；

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| kp_process_stationary_points / process | 17 个低层驻点、6 个一虚频 TS、12 个正频端点，10 个有限 IRC 加 TS3 QRC；连接逐项见上。 | rule_process_validation: $.candidates |
| kp_process_energy_assembly / process | 34 组 low→solvent/high 几何配对逐原子一致；统一浓度、温度、CO 配平的复算剖面。 | rule_process_assembly: $.method |
| kp_result_activation / result | TS1endo−INT11=22.739173663 kcal/mol，22.8±2.0。 | rule_activation: $.observables.cycloisomerization_activation_free_energy_kcal_mol |
| kp_result_endo_exo / result | TS1exo−TS1endo=7.558219734 kcal/mol，7.5±2.0。 | rule_endo_exo: $.observables.endo_exo_ocs_transition_state_difference_kcal_mol |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. 两模式移出上述 14 atom 的 README_coordinates.xyz 至私有 author_results 并注明错误混拼；不改变合法底物与催化剂坐标或增加 TS 给 agent。
2. 删除 conclusion_limitations 普通免责声明得分；先将 kp_process_energy_assembly 重新接到 conclusion_mechanism，再更新规则/证据/策略。拆分 22.8 势垒与 7.5 选择性或采用明确部分成果 rubric 的权重方案另行批准。
3. 公开可比较的温度/标准态/能量定义与隐藏目标一致；如限制方法须明确批准，不声称任意方法必达同一数值。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
