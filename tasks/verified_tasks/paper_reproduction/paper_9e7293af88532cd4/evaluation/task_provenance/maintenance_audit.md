# 2026-09-29 修后维护审查：paper_9e7293af88532cd4 / paper_reproduction

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- 保留四端点和独立诊断；清理普通免责声明而不删端点/最低点/标准态检查。
- 保留 raw 1 atm、source-recipe、all-solute 1 M、bulk-water 四种量及原 1.6±8.0 kcal/mol；成功证据非空、失败可诚实报告。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 4→4；结论记录 1→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：pr_process_endpoints, pr_process_thermo, pr_result_delta, pr_result_route
- 修后 KP：pr_process_endpoints, pr_process_thermo, pr_result_delta, pr_result_route
- 修前结论：pr_final
- 修后结论：pr_final

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| pr_process_endpoints / process | SI Table S6/Table S7 endpoint coordinates | pr_r1: $.endpoints | 全部四个中性单重最低点的69/75/66/3正频；未丢原complex1。 |
| pr_process_thermo / process | SI Computational Details; SI standard-state thermochemistry | pr_r2: $.method, $.thermochemistry, $.delta_g_water_binding_source_recipe_kcal_mol | 配平Im5+water→3；从原G复算四个标准态约定。 |
| pr_result_delta / result | supplementary_001.pdf physicalS7: Im5+H2O->Product and explicit rawG difference minusRTln55.34; physicalS5 versusS6/S7 standard-state inconsistency; CartesianIm5/Product inTableS6. | pr_r3: $.delta_g_water_binding_source_recipe_kcal_mol | source_recipe 1.596081539，对现行1.6±8.0。 |
| pr_result_route / result | main text mechanistic conclusion | pr_r4: $.diagnostic, $.conclusion | 诊断与末步热化学有计算；完整路径/唯一氧化态并未证明。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| pr_final | pr_process_endpoints, pr_process_thermo, pr_result_delta, pr_result_route | pr_c1: $.conclusion |

## 本包复查结果与科学判断

最后读回 critical_failures：成功所需身份/端点/TS 等证据约束仅用于声称成功或用于科学结论的结果，不把诚实未完成项或单列失败尝试当作伪造成功；未得到的科学结果仍无成果分。

真实历史 report：通过。本包 10 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**末步配平水结合及诊断有真实证据；不是整个反应机理验证。原 ±8.0 kcal/mol 宽容差保留，本轮不重新制定数值标准。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

四套 XYZ 是已修订任务明确给定的验证/性质对象，不将 product_3 文件名一律视为答案泄露。四输入完整、单位/态明示，water 必须独立优化；不评独立发现整个 1→3 反应。源题已公开配平和四种标准态算式，不回退旧未配平版本。

Gaussian 16 PBE1PBE/def2-TZVP，Mo 28 核 ECP，IEFPCM water，四个中性单重态 Opt/Freq。反应为 Im5 + H₂O → product 3；原 complex 1 与 product 3 相差 NH，不得裸减冒充反应能。四个最低点依次为 25/27/24/3 原子、69/75/66/3 个正频率。SI 物理第 5–7 页的 1 atm/1 M 标签不一致；本次采用当前已修订任务明确区分的四种量，不替作者消除冲突。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 4 个关键点、1 个现行结论记录；ID未变。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| pr_r1 | pr_process_endpoints | $.endpoints | condition / expert condition check |
| pr_r2 | pr_process_thermo | $.method; $.thermochemistry; $.delta_g_water_binding_source_recipe_kcal_mol | condition / expert condition check |
| pr_r3 | pr_result_delta | $.delta_g_water_binding_source_recipe_kcal_mol | numeric / absolute difference |
| pr_r4 | pr_result_route | $.diagnostic; $.conclusion; $.limitations | semantic / expert semantic comparison |
| pr_c1 | pr_final | $.conclusion; $.limitations | semantic / expert semantic comparison |

standalone 规则：无。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | True | 仅格式可提交，不代表科学成功 |

AR 缺事前假设不得编造；

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| pr_process_endpoints / process | 全部四个中性单重最低点的69/75/66/3正频；未丢原complex1。 | pr_r1: $.endpoints |
| pr_process_thermo / process | 配平Im5+water→3；从原G复算四个标准态约定。 | pr_r2: $.method, $.thermochemistry, $.delta_g_water_binding_source_recipe_kcal_mol |
| pr_result_delta / result | source_recipe 1.596081539，对现行1.6±8.0。 | pr_r3: $.delta_g_water_binding_source_recipe_kcal_mol |
| pr_result_route / result | 诊断与末步热化学有计算；完整路径/唯一氧化态并未证明。 | pr_r4: $.diagnostic, $.conclusion, $.limitations |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. 保留当前已配平任务及四种标准态，保留原 1.6±8.0。不回退未配平 1→3 或把 source_recipe 更名为一致 1 M。
2. 删除仅要求普通 limitations 表态的规则/必填；端点完整、诊断、标准态区分和不得无证据断言机理属于实质检查，必须保留。统一 PR guidance 与科学结果策略。宽容差若需重定不属本批常规修复。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
