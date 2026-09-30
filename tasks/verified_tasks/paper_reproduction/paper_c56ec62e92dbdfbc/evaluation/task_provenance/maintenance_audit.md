# 2026-09-29 修后维护审查：paper_c56ec62e92dbdfbc / paper_reproduction

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- success/bounded_failure 按 status 互斥，修复成功无结果误收及成功带空 blocker 被拒的问题。
- 额外失败候选可报告实际 disposition/failure_reason，不强造 TS；主结果仍必须有完整 saddle/模式/连接证据。
- 明确选中 R/S ID 必须唯一指向正确且已验证的候选，动态关联由语义审查承担；保留候选覆盖、敏感性和配平共同参照要求。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 4→4；结论记录 1→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：kp_process_ts, kp_process_coverage, kp_result_ordering, kp_result_mechanism
- 修后 KP：kp_process_ts, kp_process_coverage, kp_result_ordering, kp_result_mechanism
- 修前结论：c_final_selectivity
- 修后结论：c_final_selectivity

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| kp_process_ts / process | Supporting Information, computational details p. 74: stationary points were frequency validated; transition structures had one imaginary frequency and qRRHO free energies at 298.15 K.; Supporting Information, reaction-pathway discussion p. 75: four distinct C–C pathways and lowest pathways to R/S products. | r_ts: $.candidates, $.selected_R_pathway_id, $.selected_S_pathway_id | 四个一虚频鞍点+八个QRC优化正频端点；R/S取最终产物片段CIP映射，不按文件名猜。 |
| kp_process_coverage / process | Supporting Information, conformational analysis p. 75: catalyst and transition-state CREST sampling, candidate advancement and conformer analysis.; Supporting Information, reaction-pathway discussion p. 75: four distinct C–C pathways and lowest pathways to R/S products. | r_coverage: $.coverage, $.status | 四个作者最低TS代表覆盖两配置和两步；有高层/热化学敏感性，未认证自主CREST或采样收敛。 |
| kp_result_ordering / result | Main paper computational results: R-forming C–C transition state barrier 12.2 kcal/mol relative to separated starting materials.; Main paper computational results: S-forming C–C transition state barrier 14.2 kcal/mol relative to separated starting materials. | r_delta: $.selected_R_pathway_id, $.selected_S_pathway_id, $.barrier_R_kcal_mol, $.barrier_S_kcal_mol, $.delta_delta_G_dagger_kcal_mol, $.method.reference_definition, $.method.temperature_K | 共同分离反应物并补2MeOH的CC_R/S=11.760297/13.738714，差1.978417；原2±1。 |
| kp_result_mechanism / result | Main paper computational results: DeltaDeltaG double dagger 2.0 kcal/mol, predicted approximately 93% ee versus experimental 91% ee; C–C formation is enantiodetermining and rearomatization barriers are lower. | r_mechanism: $.step_comparison, $.candidates, $.method | 共同参照dep_R/S=7.430898/9.564634低于各CC分支，支持有限路线C–C决定选择性；非完整动力学网络。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| c_final_selectivity | kp_process_ts, kp_process_coverage, kp_result_ordering, kp_result_mechanism | r_final: $.conclusion, $.selectivity_determining_event |

## 本包复查结果与科学判断

最后读回 critical_failures：成功所需身份/端点/TS 等证据约束仅用于声称成功或用于科学结论的结果，不把诚实未完成项或单列失败尝试当作伪造成功；未得到的科学结果仍无成果分。

critical failure 与 success/bounded_failure 分支同步：成功不要求失败 blocker；未解竞争候选不能被伪称成功。

真实历史 report：通过。本包 14 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**现有四个作者代表 TS 支持有限路线的 R/S 能差与步骤比较；不能据此认证所有竞争家族的自主采样已收敛，也未认证完整催化剂复合物盆地连接或全局动力学网络。现行 coverage 要求未降级。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

公开 4i、1a、2a 的 82/20/26 atom XYZ 及 system.json 为分离反应物输入，均可解析；没有给最终 TS、R/S 能差或优胜路径。催化剂构型/键表由系统文件定义。既有作者 TS 只出现在私有验证档；本次没有新增到 agent_input。

Gaussian 16，气相 B3LYP-D3BJ/6-31G(d) Opt/Freq，ωB97XD/6-311++G(d,p) PCM Xylene-mixture 高层单点；各模型中性单重态。GoodVibes 4.3，298.15 K、1 M、Grimme 100 cm⁻¹ 熵修正、无准谐焓修正、频率比例 1。四个来源 TS 各 116 原子、342 模，分别只有一个负频率；八个 QRC 优化端点全为 342 个正频率。另有 catalyst 4i、1a、2a、MeOH 四个已验证参照组分及单点。正文物理第 5 页 Figure 2、SI 74–75、85 页；SI 普通方法 6-31G(d) 与构象段 6-31+G(d) 不同，未静默合并。作者 Perl 热修正实现未取得，GoodVibes 是明确替代实现。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 4 个关键点、1 个现行结论记录；ID未变。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| r_ts | kp_process_ts | $.candidates; $.selected_R_pathway_id; $.selected_S_pathway_id | condition / expert validation of each candidate record |
| r_coverage | kp_process_coverage | $.coverage; $.status | condition / expert comparison of coverage and stopping record |
| r_delta | kp_result_ordering | $.selected_R_pathway_id; $.selected_S_pathway_id; $.barrier_R_kcal_mol; $.barrier_S_kcal_mol; $.delta_delta_G_dagger_kcal_mol; $.method.reference_definition; $.method.temperature_K | numeric / absolute difference; applies when status is success |
| r_final | c_final_selectivity | $.conclusion; $.selectivity_determining_event | semantic / expert semantic comparison |
| r_mechanism | kp_result_mechanism | $.step_comparison; $.limitations | semantic / expert semantic comparison |

standalone 规则：无。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | True | 仅格式可提交，不代表科学成功 |
| successful_result_plus_empty_blockers | False | schema_validation: {'status': 'success', 'evaluation_match': True, 'author_route_complete': True, 'validation_mode': 'Author-informed task-scoped ver |
| success_without_scientific_results | True | 仅格式可提交，不代表科学成功 |
| honest_early_failure_no_TS | False | schema_validation: 'ts_geometry_file' is a required property; schema_validation: 'charge' is a required property; schema_validation: 'multiplicity' is a required property; schema_validation: 'imaginary_frequency_count' is a required property |

成功+空blockers、早期失败等 synthetic 样例仅用于揭示格式问题，不作为历史计算证据。AR 缺事前假设不得编造；

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| kp_process_ts / process | 四个一虚频鞍点+八个QRC优化正频端点；R/S取最终产物片段CIP映射，不按文件名猜。 | r_ts: $.candidates, $.selected_R_pathway_id, $.selected_S_pathway_id |
| kp_process_coverage / process | 四个作者最低TS代表覆盖两配置和两步；有高层/热化学敏感性，未认证自主CREST或采样收敛。 | r_coverage: $.coverage, $.status |
| kp_result_ordering / result | 共同分离反应物并补2MeOH的CC_R/S=11.760297/13.738714，差1.978417；原2±1。 | r_delta: $.selected_R_pathway_id, $.selected_S_pathway_id, $.barrier_R_kcal_mol, $.barrier_S_kcal_mol, $.delta_delta_G_dagger_kcal_mol, $.method.reference_definition, $.method.temperature_K |
| kp_result_mechanism / result | 共同参照dep_R/S=7.430898/9.564634低于各CC分支，支持有限路线C–C决定选择性；非完整动力学网络。 | r_mechanism: $.step_comparison, $.limitations |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. 两模式 schema.oneOf 显式按 status=success/bounded_failure 分支；实测 success 加空 unresolved_blockers 被两分支同时匹配而拒绝；更严重的是 success 无势垒但有 blocker 反被接受。
2. 候选 validation 按 validated/failed disposition 分支，真实早期失败允许没有 TS 几何/虚频/映射；主成功与额外失败 attempts 分开，不伪造成功字段。
3. 保留 TS/模式/连接/配平参照与原 ΔΔG 2.0±1.0。作者有限候选覆盖已支撑可计算性，未认证 task 要求的自主采样收敛；不以删除 coverage 关键点换通过。方法段 6-31G(d)/6-31+G(d) 与 GoodVibes 替代如实记录。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
