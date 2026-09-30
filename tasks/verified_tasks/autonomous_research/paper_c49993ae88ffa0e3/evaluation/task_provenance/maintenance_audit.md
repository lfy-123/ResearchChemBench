# 2026-09-29 修后维护审查：paper_c49993ae88ffa0e3 / autonomous_research

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- 删除两模式 task.md 重复的整套指令，PR 单列作者指导。
- 删除 c_ar_limits/c_pr_limits 普通声明结论及 AR 纯边界 KP；保留状态、覆盖、水模型敏感性并接回真实热力学结论。
- PR 按四种既有状态及各自标量比较；AR 按唯一 state_id 进行语义身份匹配，不按数组位置猜。历史 states 字典仅在私有测试中无损映射为数组。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 5→4；结论记录 2→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：kp_ar_process_inventory, kp_ar_process_validation, kp_ar_dry, kp_ar_water, kp_ar_limits
- 修后 KP：kp_ar_process_inventory, kp_ar_process_validation, kp_ar_dry, kp_ar_water
- 修前结论：c_ar_final, c_ar_limits
- 修后结论：c_ar_final

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| kp_ar_process_inventory / process | Main paper p. 4, first-transfer PT/ET discussion and Figure 2B.; Main paper p. 4, explicit-water effect and PCET/HAT limitation. | r_ar_inventory: $.hypotheses | 源 PT/ET 四类别有明示候选及29构象；不认证独立提出/排除 PCET/HAT。 |
| kp_ar_process_validation / process | SI p. S38, optimization, frequencies and thermochemical temperature.; SI p. S38, conformational and interaction-motif search. | r_ar_validation: $.candidates, $.coverage; r_ar_limits: $.coverage, $.sensitivity, $.method, $.states, $.conclusion | 29最低点全实频、29相同父几何SP、状态/水数/对称性/去重档。 已有对称数/去重参数变体支持所记录的敏感性，不认证新自主穷尽。 |
| kp_ar_dry / result | Main paper p. 4, first-transfer PT/ET discussion and Figure 2B.; SI p. S40, dry relative free energies. | r_ar_dry: $.states | pt/et dry −0.922739/−1.844559，分别对 −0.9/−1.6±1.0。 |
| kp_ar_water / result | Main paper p. 4, explicit-water effect and PCET/HAT limitation.; SI p. S40, hydrated relative free energies. | r_ar_water: $.water_effect, $.states | et hydrated −8.029374，水位移 −6.184816，源约−8.2。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| c_ar_final | kp_ar_process_inventory, kp_ar_process_validation, kp_ar_dry, kp_ar_water | r_ar_final: $.conclusion |

## 本包复查结果与科学判断

真实历史 report：通过（仅将 states 字典无损映射为带 state_id 的数组）。本包 13 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**水合 PT 的正文/SI 冲突保留，未新增固定 gold。29 构象与对称/去重敏感性支持有限来源系综；不宣称排除 PCET/HAT、得到速率或认证独立搜索收敛。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

两模式公开分子图/状态/水数定义齐全；AR 只给起始/event 边界，PR 给 PT/ET 路线。没有把私有 29 个优化构象或参考能量公开。条件与两水计量可复算。PR task.md 重复一整套四节指令。

Gaussian 16，M06-2X/6-31+G(d,p) Opt/Freq → 同几何 def2-TZVPP 单点，SMD acetonitrile。H₂PQ/HPQ 阴离子采用明示的最低单重激发态 TD 总能；H₂PQ 阳离子自由基与 PyO 阴离子自由基采用 S0 双重态；其他组分为相应基态单重态。29 个低/高层配对。SI 物理第 38 页：298.15 K、1 M、100 cm⁻¹ Grimme 熵插值、构象系综及对称性。GoodVibes 4.3 独立重读全部 29 个低层日志，避免对称数重复相除。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 5 个关键点、2 个现行结论记录；ID未变。c499含以limits命名且混有敏感性边界的记录，不能将其机械计为第二个独立科学成果。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| r_ar_inventory | kp_ar_process_inventory | $.hypotheses | semantic / expert semantic comparison |
| r_ar_validation | kp_ar_process_validation | $.candidates; $.coverage | semantic / expert semantic comparison |
| r_ar_dry | kp_ar_dry | $.states | semantic / expert semantic comparison |
| r_ar_water | kp_ar_water | $.water_effect; $.states | semantic / expert semantic comparison |
| r_ar_limits | kp_ar_limits | $.sensitivity; $.conclusion | semantic / expert semantic comparison |
| r_ar_final | c_ar_final | $.conclusion | semantic / expert semantic comparison |
| r_ar_limits_conclusion | c_ar_limits | $.sensitivity; $.conclusion | semantic / expert semantic comparison |

standalone 规则：无。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | False | schema_validation: {'pt_dry': {'delta_g_kcal_mol': -0.9227387150233828, 'products': ['S1-HPQ-anion', 'PyOH-cation'], 'reactants': ['S1-H2PQ', 'PyO'], |
| private_lossless_states_array_mapping | True | 仅格式可提交，不代表科学成功 |

AR 缺事前假设不得编造；c499 states 无损重排不改变数值或科学记录。

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| kp_ar_process_inventory / process | 源 PT/ET 四类别有明示候选及29构象；不认证独立提出/排除 PCET/HAT。 | r_ar_inventory: $.hypotheses |
| kp_ar_process_validation / process | 29最低点全实频、29相同父几何SP、状态/水数/对称性/去重档。 | r_ar_validation: $.candidates, $.coverage |
| kp_ar_dry / result | pt/et dry −0.922739/−1.844559，分别对 −0.9/−1.6±1.0。 | r_ar_dry: $.states |
| kp_ar_water / result | et hydrated −8.029374，水位移 −6.184816，源约−8.2。 | r_ar_water: $.water_effect, $.states |
| kp_ar_limits / result | 热力学端点证据；无速率/PCET-HAT排除证据，不把边界声明作为独立科学结果。 | r_ar_limits: $.sensitivity, $.conclusion |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. PR task.md 去掉重复指令，按流程设置 PR guidance；不改分子/水数或范围。
2. AR 历史 states 对象→带 state_id 的列表可无损映射且真实 runner 通过；仅用于私有验证，不补写事前自主假设。当前 schema 可以保留，后续规则须按实际 state_id 稳定绑定。
3. c_ar_limits/c_pr_limits 混有普通免责声明与实质水模型/候选敏感性：取消纯声明门槛并把必要敏感性接回真正热力学成果；PR 独立状态身份过程规则不能因重接漏评。
4. 正文/SI 水合 PT 差异继续单列，不新增固定水合 PT gold；有限来源构象与 task 独立收敛搜索的区别保留，不将作者参考当盲测完成。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
