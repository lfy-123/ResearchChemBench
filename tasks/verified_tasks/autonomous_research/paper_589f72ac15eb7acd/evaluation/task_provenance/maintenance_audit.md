# 2026-09-29 修后维护审查：paper_589f72ac15eb7acd / autonomous_research

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- 将 $defs 放入 runner 实际使用的 result_schema，消除无法解析引用的错误。
- 成功的六个选中态必须保留电荷/多重度、能量、几何、频率及自旋/收敛证据；诚实失败不必填未完成方法。
- 保留 HS−LS 定义及方法自由度；AR 的物理量边界项改为过程有效性检查，不把普通 uncertainty 作为成果。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 4→4；结论记录 1→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：ar_process_plan, ar_process_validation, ar_result_values, ar_result_limit
- 修后 KP：ar_process_plan, ar_process_validation, ar_result_values, ar_result_limit
- 修前结论：ar_final
- 修后结论：ar_final

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| ar_process_plan / process | Paper/SI workflow evidence: geometry optimization and energy calculation.; Paper p.11: computational method is a concrete reference route, while autonomous task does not prescribe it. | ar_r1: $.plan, $.coverage | 六个采用态及尝试档；作者辅助有限计划，未认证自主事前计划。 |
| ar_process_validation / process | Paper p.3: pseudohalide identities.; Paper p.5: octahedral cis coordination. | ar_r2: $.systems | 六个优化/频率输出、身份/自旋诊断；3N−6 全部实频。 |
| ar_result_values / result | Paper Table 2: C1 isolated E_el^iso = −34 kJ/mol.; Paper Table 2: C2 isolated E_el^iso = −28 kJ/mol.; Paper Table 2: C3 isolated E_el^iso = −21 kJ/mol. | ar_r3a: $.systems.C1, $.method, $.gaps_kj_mol, $.partial_gaps_kj_mol; ar_r3b: $.systems.C2, $.method, $.gaps_kj_mol, $.partial_gaps_kj_mol; ar_r3c: $.systems.C3, $.method, $.gaps_kj_mol, $.partial_gaps_kj_mol | 六个 E_SCF 的 HS−LS 独立换算，见结果表；现行 semantic 规则允许方法合理差异。 |
| ar_result_limit / process | Paper discussion: isolated values establish ligand-field trend.; Paper abstract: solid-state packing changes SCO behavior. | ar_r4: $.conclusion | 三者 HS 较低、仅孤立电子能的相对 LS 稳定化；无晶体 T1/2。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| ar_final | ar_process_plan, ar_process_validation, ar_result_values, ar_result_limit | ar_r5: $.conclusion |

## 本包复查结果与科学判断

真实历史 report：通过。本包 20 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**现有六态支持限定孤立电子能比较；未认证自主事前计划或全局构象穷尽。合理替代方法按实际电子态和能量证据判断，不强制复现作者每个数值。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

公开输入只有中立系统定义，C21H19N5S、三种辅助配体、cis 与 0/(5,1) 齐全，未含作者末态坐标或参考能量。来源旧 C21/C22 疑点已按当前真实身份更正，不照抄旧待修列表。

Gaussian 16 C.01，CAM-B3LYP/CEP-31G，D3；孤立气相、总电荷 0，HS 多重度 5、LS 多重度 1。正文 Table 2（main PDF 物理第 8 页）报告 −34/−28/−21 kJ mol⁻¹。验证采用作者 cis 起始框架，逐态重新优化/频率；不是把作者能量当输出。与作者 G16 A.03 存在版本差异。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 4 个关键点、1 个现行结论记录；ID未变。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| ar_r1 | ar_process_plan | $.plan; $.coverage | semantic / expert process comparison |
| ar_r2 | ar_process_validation | $.systems | semantic / expert process comparison |
| ar_r3a | ar_result_values | $.systems.C1; $.method; $.uncertainty | semantic / expert scientific comparison against source sign/object and internally supported result |
| ar_r3b | ar_result_values | $.systems.C2; $.method; $.uncertainty | semantic / expert scientific comparison against source sign/object and internally supported result |
| ar_r3c | ar_result_values | $.systems.C3; $.method; $.uncertainty | semantic / expert scientific comparison against source sign/object and internally supported result |
| ar_r4 | ar_result_limit | $.conclusion; $.uncertainty | semantic / expert semantic comparison |
| ar_r5 | ar_final | $.conclusion | semantic / expert semantic comparison |

standalone 规则：无。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | False | invalid_contract_reference: PointerToNowhere: '/$defs/system' does not exist within {'type': 'object', 'required': ['status', 'plan', 'method', 'systems', 'co |

AR 缺事前假设不得编造；

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| ar_process_plan / process | 六个采用态及尝试档；作者辅助有限计划，未认证自主事前计划。 | ar_r1: $.plan, $.coverage |
| ar_process_validation / process | 六个优化/频率输出、身份/自旋诊断；3N−6 全部实频。 | ar_r2: $.systems |
| ar_result_values / result | 六个 E_SCF 的 HS−LS 独立换算，见结果表；现行 semantic 规则允许方法合理差异。 | ar_r3a: $.systems.C1, $.method, $.uncertainty; ar_r3b: $.systems.C2, $.method, $.uncertainty; ar_r3c: $.systems.C3, $.method, $.uncertainty |
| ar_result_limit / result | 三者 HS 较低、仅孤立电子能的相对 LS 稳定化；无晶体 T1/2。 | ar_r4: $.conclusion, $.uncertainty |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. 两模式 submission_schema.json：将实际使用的 $defs 放进 result_schema（或内联等价定义），用真实 report 经 validate_output_contract 复核；当前 PointerToNowhere 是框架故障，不是 Fe 算错。
2. reference_key_points/reference_conclusions 与现行 semantic rules 对齐方法自由度：保留能差定义/态/趋势，不把隐藏作者数值当任何方法唯一答案。清除普通 uncertainty/limitations 表态必填及扣分，保留真实物理边界。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
