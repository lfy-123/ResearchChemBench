# 2026-09-29 修后维护审查：paper_3c89b494a1645491 / autonomous_research

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- 四条 contact 按身份唯一覆盖，允许乱序；validated 八个描述符必须为数字，complete 必须四条均成功且有四个 BCP。
- 缺描述符用 null 和真实 notes，早期失败不强造收敛或 BCP；成功不要求普通 notes/limitations。
- 保留 +4 单重态和原始 CCDC 2500223；未改 DI/rho 数值标准，rho 原均值/逐接触冲突明确交科学审查。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 4→4；结论记录 1→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：ar_process_hypothesis, ar_process_validation, ar_result_aim, ar_result_class
- 修后 KP：ar_process_hypothesis, ar_process_validation, ar_result_aim, ar_result_class
- 修前结论：ar_final
- 修后结论：ar_final

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| ar_process_hypothesis / process | Main paper, DFT/AIM discussion: four Au···Au BCPs and quantitative interpretation. | ar_r1: $.hypotheses, $.provenance | 作者路线做了结构/拓扑/双网格检验；历史report没有事前自主hypotheses，未认证AR探索。 |
| ar_process_validation / process | SI §3.1, computational model and molecular boundary.; SI Figure S17 caption: four Au···Au bond critical points. | ar_r2: $.system, $.validation, $.provenance | 184atom +4/1最低点、546正频，四BCP八条真实路径。 |
| ar_result_aim / result | SI Table S2: source per-contact AIM and DI values. | ar_r3: $.contacts[0].rho, $.contacts[1].rho, $.contacts[2].rho, $.contacts[3].rho | rho及定性AIM模式支持；两项DI字面区间越界，当前精度接受边界待确认。 |
| ar_result_class / result | Main paper: source classification using \|V\|/G and DI range. | ar_r4: $.classification, $.conclusion | 四个1<\|V\|/G<2、正laplacian、负H及非零DI，支持有限模型成键分类。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| ar_final | ar_process_hypothesis, ar_process_validation, ar_result_aim, ar_result_class | ar_r5: $.hypotheses, $.conclusion |

## 本包复查结果与科学判断

最后读回 critical_failures：成功所需身份/端点/TS 等证据约束仅用于声称成功或用于科学结论的结果，不把诚实未完成项或单列失败尝试当作伪造成功；未得到的科学结果仍无成果分。

真实历史 report：未通过：原历史结果缺 AR hypotheses；保持原样，不补编事前记录。本包 14 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**DI=0.37627436 和 0.37365572 分别越过字面 [0.374,0.376] 上/下界 0.00027436 和 0.00034428；另两项在界内。rho 均值靶与逐接触措辞未统一。定性成键有支持，但不能宣称全部定量点严格通过；AR 历史 report 也缺 hypotheses。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。Au DI 的定量边界（适用时）仍未关闭。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

真实 CIF 为 CCDC 2500223，保留完整出处/占据/晶胞及原子标签；system_definition 指定仅移除阴离子和溶剂、+4 单重态及四边。实验晶体是任务给定结构证据，不是计算 BCP/DI 答案，DOI/CCDC 号不单独构成答案泄露；未向 agent 提供 fchk 或拓扑计算结果。

Gaussian 16 C.01 BP86-D3BJ/def2-TZVPP，Au 60 核 ECP；184 原子 C76H88Au4N16、+4 单重态、546 正频率。由 CCDC 2500223 晶体删除阴离子/溶剂，保留完整四配体及环状 Au 标号。fchk 导出后 Multiwfn 2026.7.15 计算四个 BCP、八条连接路径、0.20/0.10 Bohr 两档 DI 网格；源用 G16 C.02/Multiwfn 3.8。SI 物理第 27 页方法、第 28 页拓扑图、第 29 页 Table S2，正文第 4 页近似 DI 区间及分类。软件/网格差异已知，但不能无证据认定其解释所有 DI 差异。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 4 个关键点、1 个现行结论记录；ID未变。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| ar_r1 | ar_process_hypothesis | $.hypotheses; $.provenance | semantic / expert process comparison |
| ar_r2 | ar_process_validation | $.system; $.validation; $.provenance | semantic / expert process comparison |
| ar_r3 | ar_result_aim | $.contacts[0].rho; $.contacts[1].rho; $.contacts[2].rho; $.contacts[3].rho | numeric / absolute difference to source values per contact |
| ar_r4 | ar_result_class | $.classification; $.conclusion; $.limitations | semantic / expert semantic comparison |
| ar_r5 | ar_final | $.hypotheses; $.conclusion | semantic / expert semantic comparison |

standalone 规则：无。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | False | schema_validation: 'hypotheses' is a required property |

AR 缺事前假设不得编造；

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| ar_process_hypothesis / process | 作者路线做了结构/拓扑/双网格检验；历史report没有事前自主hypotheses，未认证AR探索。 | ar_r1: $.hypotheses, $.provenance |
| ar_process_validation / process | 184atom +4/1最低点、546正频，四BCP八条真实路径。 | ar_r2: $.system, $.validation, $.provenance |
| ar_result_aim / result | rho及定性AIM模式支持；两项DI字面区间越界，当前精度接受边界待确认。 | ar_r3: $.contacts[0].rho, $.contacts[1].rho, $.contacts[2].rho, $.contacts[3].rho |
| ar_result_class / result | 四个1<\|V\|/G<2、正laplacian、负H及非零DI，支持有限模型成键分类。 | ar_r4: $.classification, $.conclusion, $.limitations |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. 当前 PR pr_result_aim 要求 DI 位于 reported narrow range；原始两项字面越界，三位有效显示与定性分类支持不能自动当数值严格通过。负责人先决定接受正文约三位精度的有限分类，还是维持原始字面区间并保留待定；不自行扩大容差、改 DI、删必评量或开新网格计算。
2. rho 规则 target/单位写四边均值，但字段绑定四个位置且 comparison 写逐接触；需决定均值还是 SI 逐接触比较后按 contact ID 绑定，不能默选对过关有利的一边。当前二者都满足现有 ±0.001 仅是证据，不是新定义授权。
3. AR 历史 report 缺 hypotheses；只认作者路线验证，不能补编事前自主轨迹。清除普通 limitations 得分而保留四边身份、+4/1、BCP、真实定量证据与物理范围。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
