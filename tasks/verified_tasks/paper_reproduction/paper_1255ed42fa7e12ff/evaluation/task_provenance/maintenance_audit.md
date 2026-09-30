# 2026-09-29 修后维护审查：paper_1255ed42fa7e12ff / paper_reproduction

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- 公开主数组 O/S/Se 顺序，并让每个位置执行完整行约束；validated 必须有非空 TS/端点/证据、numeric 势垒及正速率。
- 逐分子绑定 barrier 和 k，明确 log10(k) 差值容差 0.25；读取完整频率/状态/连接证据。
- 公开 TD-ωB97X-D/6-311G(d,p)、CPCM MeCN、298.15 K 比较背景但不固定所有方法；失败可省未取得证据，AR 事前假说不补编。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 4→4；结论记录 1→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：p1, p2, p3, p4
- 修后 KP：p1, p2, p3, p4
- 修前结论：c1
- 修后结论：c1

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| p1 / process | Main paper methods frequency validation; ev_doc_d25dd3ea0bfe_000049_6fbc2660a67d | r1: $.results[*].validation, $.results[*].evidence, $.methods | 3个相关单虚频TS+6个105正频最低点，S1态及模式证据。 |
| p2 / process | Main paper methods IRC validation; ev_doc_d25dd3ea0bfe_000049_6fbc2660a67d | r2: $.results[*].validation.connectivity | 六方向路径/终态，Se仅用有效前缀和修复尾段，所有采用点的六根排序复核。 |
| p3 / result | Main paper Table 1 and kinetics text; ev_doc_d25dd3ea0bfe_000121_4d764c388bca | r3_O: $.results[0].barrier_kcal_mol; r3_S: $.results[1].barrier_kcal_mol; r3_Se: $.results[2].barrier_kcal_mol | 原G独立复算三势垒13.426193/7.703934/6.661641，均满足原±1。 |
| p4 / result | Main paper Table 1 and kinetics text; ev_doc_d25dd3ea0bfe_000121_4d764c388bca | r4_O: $.results[0].rate_s_inv; r4_S: $.results[1].rate_s_inv; r4_Se: $.results[2].rate_s_inv | 298.15K普通TST公式复算三个k，原log10容差±.25；非动力学轨迹。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| c1 | p1, p2, p3, p4 | r5: $.conclusion |

## 本包复查结果与科学判断

最后读回 critical_failures：成功所需身份/端点/TS 等证据约束仅用于声称成功或用于科学结论的结果，不把诚实未完成项或单列失败尝试当作伪造成功；未得到的科学结果仍无成果分。

真实历史 report：通过。本包 19 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**作者路线支持三势垒/速率及有限六根顺序；无波函数重叠连续性或非绝热动力学认证。AR 历史 report 缺事前 hypotheses，不伪造补齐；不同协议仍需可比性判断。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

三个 37 atom S1 enol 是明确给定的起始反应物，没有 keto/TS/IRC 答案。注释如实标明 SI 来源。需确认自由溶剂/方法选择与固定 CPCM 数值靶的有效答案范围；不因坐标来源于 SI 自动删除合法起点。

Gaussian 16 ωB97XD/6-311G(d,p)，TD 六个单重激发态、Root=1，CPCM acetonitrile，37 原子中性体系。三个 TS 各一个相关质子迁移虚频，六端点各 105 个正频率。以最低六根中的 S1 接受点审查路径。Se 反向仅采用旧路径 0–17 点，再接 EqSolv/IOp(9/49=5) 修复尾段；排除旧 18–62 点。方法见正文物理第 2–3 页，Table 1 在第 5 页；本次重新解析全部采用路径点的六根能量及 Root1 选择。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 4 个关键点、1 个现行结论记录；ID未变。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| r1 | p1 | $.results[*].validation.minimums | condition / expert |
| r2 | p2 | $.results[*].validation.connectivity | condition / expert |
| r3_O | p3 | $.results[*].barrier_kcal_mol | numeric / select result where compound is 8QBDY-O |
| r3_S | p3 | $.results[*].barrier_kcal_mol | numeric / select result where compound is 8QBDY-S |
| r3_Se | p3 | $.results[*].barrier_kcal_mol | numeric / select result where compound is 8QBDY-Se |
| r4_O | p4 | $.results[*].rate_s_inv | numeric / select result where compound is 8QBDY-O; compare log10 |
| r4_S | p4 | $.results[*].rate_s_inv | numeric / select result where compound is 8QBDY-S; compare log10 |
| r4_Se | p4 | $.results[*].rate_s_inv | numeric / select result where compound is 8QBDY-Se; compare log10 |
| r5 | c1 | $.conclusion | ordering / expert |

standalone 规则：无。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | True | 仅格式可提交，不代表科学成功 |

AR 缺事前假设不得编造；

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| p1 / process | 3个相关单虚频TS+6个105正频最低点，S1态及模式证据。 | r1: $.results[*].validation.minimums |
| p2 / process | 六方向路径/终态，Se仅用有效前缀和修复尾段，所有采用点的六根排序复核。 | r2: $.results[*].validation.connectivity |
| p3 / result | 原G独立复算三势垒13.426193/7.703934/6.661641，均满足原±1。 | r3_O: $.results[*].barrier_kcal_mol; r3_S: $.results[*].barrier_kcal_mol; r3_Se: $.results[*].barrier_kcal_mol |
| p4 / result | 298.15K普通TST公式复算三个k，原log10容差±.25；非动力学轨迹。 | r4_O: $.results[*].rate_s_inv; r4_S: $.results[*].rate_s_inv; r4_Se: $.results[*].rate_s_inv |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. 两模式按 compound 身份绑定每个 barrier/rate，保留 O/S/Se 当前靶和容差，log10(k) 比较显式；通配字段+自然语言选择器当前仅交语义审查。防重复/漏对象，不依赖数组顺序。
2. 公开主比较的溶剂/温度/量定义或明确允许的替代协议，解决自由气相/溶剂与固定源靶的冲突；若限定方法，先批准。
3. AR 历史 report 缺 hypotheses，不能后填一个事前假说声称自主重放已通过；保留作者路线科学证据。普通免责声明改可选，S1 选根/连通性/频率必须保留。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
