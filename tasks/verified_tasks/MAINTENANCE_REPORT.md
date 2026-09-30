# 新验证任务修复记录与逐篇审查报告

> **2026-09-29 新八篇修后状态：见第30节。**按负责人最新指令完成本批 8 篇、16 包的常规修复与复查，全部保留 `verified_tasks`，没有迁移 final/hold。第29节为修前初审历史。Au 两项 DI 字面越界和 rho 比较定义仍待科学决定；作者路线计算不等于自主盲测。

> **2026-09-27 最新修复：见第27节。**负责人已批准修复两篇指令/评分冲突；d83两模式的极小点证据分支及1a47 PR的主计算协议已统一，原科学目标、数值靶/容差和输入数据未改。专项120项、整批863项离线检查通过；现有真实计算继续支持对应科学目标，本轮没有新增量化计算或完整LLM评分。当前 **8篇15包（AR7、PR8）** 仍留verified_tasks，没有迁入final。2a71 PR仍在hold，其Group 4交接指令已另写好。

> **2026-09-27 前次复核：见第26节。**已确认 `paper_2a71ffa4b0a90809` 的论文为31 kcal/mol，且SI要求SMD18，而历史验证实际用了普通SMD；尚未定量解释差额。本PR包已移入 `hold_verified_paper_reproduction`，原评分未改，未启动计算。第26节中的d83/1a47“待处理”状态已由第27节获准修复覆盖；第25节“2a71仅评分边缘问题”的历史建议已撤回。

> **2026-09-26 新批次：见第 23 节。**对六个 group 的最新记录与 final/hold 去重，再逐模式核对真实计算及 evaluator 后，新增复制 **9 篇、16 包（AR 7、PR 9）**到 verified_tasks，各包已新增详细计算 reference；不是迁入 final 或发布批准。`paper_2a71ffa4b0a90809` 的 AR 未纳入，理由见第 23.3 节。之前 15 篇/29 包的迁移状态不变。

> **2026-09-24 最新状态：见第 21 节（整批迁入 final 与迁移后检查）。**负责人明确要求将调整好的任务移入 final；本批 **15 篇、29 包（AR 14、PR 15）已全部迁入对应 final 目录**，verified_tasks 不再留有本批任务包。第 15–20 节保留审查和获批修复的历史记录，其中“待批准/仍在 verified_tasks/没有迁移”描述的是当时状态；第 1–14 节属于更早批次。当前迁移清单、检查范围与未实测事项以第 21 节为准。

> **SI 补充更新：见第 22 节。**43d/c28 两份 SI 已由负责人提供并归档；前文“SI 缺存”现为历史状态。新原文核对发现 43d 坐标表编号与正文身份不符，并纠正 c28 私有说明中“图无可读数值”的判断。当前四个任务包的科学内容未修改，具体影响与后续建议见第 22 节。

日期：2026-09-16。范围：本批 **18 篇论文、34 个任务包（AR 16、PR 18）**。
当前状态：**获准修复、最终审查和本批迁移已完成。7a 两模式因正确对象的验证证据不足保留在对应 hold；其余 17 篇/32 包（AR 15、PR 17）已按负责人明确授权迁入 `tasks/final_verified_*`。随后获准的 ef266 接触定义及 Cat1 AR 选态措辞修复、最终 reference 档案清理均已完成；迁移前 62 项回归通过，迁移后专项复核见第 13.4 节。**
本报告替代本文件前轮的“23 个 final / 11 个 hold 已完成分流”结论；前轮迁移不是负责人验收，已经撤回。

**阅读顺序：先看本文件第 13 节的最终审查、迁入清单及发布边界；[修复后逐篇复审报告](POST_REPAIR_REAUDIT_20260916.md)第 7 节及本文件第 12 节记录两项后续修复；第 11 节记录再次复审/7a 迁移，第 10 节是迁移前修复记录；第 1–9 节保留退回、审查、审批前方案历史，其中“待确认/未修改/暂缓”等措辞不代表当前状态。文中的任务链接随最终位置更新，历史判断保留。**负责人随后明确暂停自主科研能力分类统计，将其交由其他 agent；本轮不做该报告、不修改第一批 final。

## 1. 先纠正目录和确认流程

本次已执行负责人明确授权的两项操作：

1. 更新[维护流程](../../docs/verification/final_verified_tasks/final_verified_task_maintenance_workflow.md)，加入两个独立确认点：**先批准具体修改方案；在 verified_tasks 修复、复查并汇报后，再确认调整结果及具体 final/hold 迁移清单。**“继续处理”、审查完成或批准修法均不自动授权迁移；有问题也不能自行移入 hold。
2. 将前轮移出的本批 34 个完整任务包全部移回 `verified_tasks/<mode>/<paper_id>`，保留已做的修复，没有拿 canonical 原包覆盖，没有删除计算档案。相对链接、目录状态及包 manifest 随位置更新。第一批任务的科学内容未改。

| 目录 | 退回后的论文任务目录数 | 说明 |
|---|---:|---|
| `verified_tasks/autonomous_research` | 16 | 本批全部 AR，含待处理问题 |
| `verified_tasks/paper_reproduction` | 18 | 本批全部 PR，含待处理问题 |
| `final_verified_autonomous_research` | 52 | 第一批数量；本轮不重新认证第一批 |
| `final_verified_paper_reproduction` | 53 | 同上 |
| `hold_verified_autonomous_research` | 3 | 第一批暂缓包 |
| `hold_verified_paper_reproduction` | 3 | 同上 |

**本次未再次修改 task.md、科学输入、提交 schema、task_info、paper_route 或五个 evaluator JSON。**未改 reference 的真实计算事实；只调整它的位置链接/当前待确认状态。除了获准的流程文档，没有写入 `docs/verification/`；没有修改论文、原始任务或 group 原始验证记录，没有运行新的量化计算或操作 HPC 作业。

可恢复历史：修复前 `e67441a9`，格式整理 `42970e03`，前轮修复及已撤回迁移 `22d440f8`。这些版本可查前后变化，不作为科学正确性的证明。

## 2. 本轮如何判断，不再把几种问题混为一谈

- **作者路线验证允许知道论文路线、作者几何/TS和结果。**只要真实计算的是正确对象、物理量和条件，就可证明相应 evaluator 科学结论可算得。不要求历史计算模拟未知答案的 agent；未从当前 starter 盲跑本身不是失败，也不自动要求补算。
- **可算得不等于输入无泄露。**几何或 TS 本身是待求结果时，作者终态不能公开；有真实验证也不能抵消这一点。
- **单体系数值成功不自动证明更强结论。**例如任意方法的相同 Mulliken 电荷、任意激发态的相同 IFCT、所有模式同向变化、所有构象都稳健、没有观测数据却声称实验吻合。
- **reference 是真实计算档案，不是评分规则。**最终仍核对五个 evaluator JSON 的中间关键点与结论；旧 PASS、schema 通过、数值碰巧在容差内均不能代替对象和证据核对。
- 区分“确认的缺陷”“存在歧义、建议澄清”“没有发现新的实质性缺口”。下表和逐篇段落不是新的自动 final/hold 分类，更不是负责人批准。

最重要的发现：

1. 前轮所称暂缓的 **7 篇、11 个任务**的问题仍需处理：6f（仅 PR）、746、ef、a396、46a9（两模式），d796、44f（仅 PR）。其中 **746、ef、d796、44f 共 4 篇/6 个任务**存在作者答案结构公开的问题。
2. `paper_a3968806251093cd` 是最明确的**验证对象错误**：两条成功 Opt/Freq 不等于正确论文 7a 已被验证。其余论文存在可追溯的相应作者路线核心计算，但不能因此一概保证现有全部措辞/评分分支正确。
3. 前轮建议 final 的任务也有新发现或遗漏：Z1 的实验输入与 final 评分分支、isoxazole 的失败候选 schema、egan-IrCl 的能差正负号、Int-3 AR 的通道条件，以及 Rh101 趋势解释的歧义。均在下文写明具体位置和最小修法。
4. 给定结构性质任务中的作者优化几何需要**你确认任务范围**，而不是维护者自行批准例外；这与已经明确的待求几何/TS答案泄露分别讨论，见第 4 节。

## 3. 全部 18 篇的逐篇复审

表中的 AR/PR 链接为当前暂存任务指令；同篇不同模式分别核对。每包仍有 `evaluation/verified_computation_reference.md` 记录真实有效链，`evaluation/task_provenance/maintenance_audit.md` 顶部标明本次复审状态，保留前轮历史但不再视为验收结论。

| group / 论文 | 当前任务 | 本次主要判断（均待确认，不迁移） |
|---|---|---|
| group_1 / [`paper_d2d08c91f34da1cb`](#paper_d2d08c91f34da1cb) | [AR](../final_verified_autonomous_research/paper_d2d08c91f34da1cb/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_d2d08c91f34da1cb/agent_input/task.md) | 两态频率链成立；PR 红/蓝移应允许混合、交换和反例；两态作者几何的角色待确认。 |
| group_1 / [`paper_6f9a36fff6964313`](#paper_6f9a36fff6964313) | [AR](../final_verified_autonomous_research/paper_6f9a36fff6964313/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_6f9a36fff6964313/agent_input/task.md) | PR 自选方法与固定 Mulliken 数值不匹配；AR 不应把有限覆盖说成构象不敏感。 |
| group_1 / [`paper_746e066c163800d8`](#paper_746e066c163800d8) | [AR](../final_verified_autonomous_research/paper_746e066c163800d8/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_746e066c163800d8/agent_input/task.md) | 72 原子作者优化终态公开；signed/absolute 与正值 gold 不一致；失败 schema 强制虚频数。 |
| group_1 / [`paper_5ea491c741fbd8d4`](#paper_5ea491c741fbd8d4) | [AR](../final_verified_autonomous_research/paper_5ea491c741fbd8d4/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_5ea491c741fbd8d4/agent_input/task.md) | 五起点/三极小值成立；未计算 Hessian 的失败候选不能如实填 schema；自由方法数值比较需说明。 |
| group_1 / [`paper_a0f6b899582cb9f7`](#paper_a0f6b899582cb9f7) | [AR](../final_verified_autonomous_research/paper_a0f6b899582cb9f7/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_a0f6b899582cb9f7/agent_input/task.md) | 独立 M3 starter；原始二阶矩/轴/单位已有明确约定；现有三极小值支持目标。 |
| group_1 / [`paper_ef26687d63a37e29`](#paper_ef26687d63a37e29) | [AR](../final_verified_autonomous_research/paper_ef26687d63a37e29/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_ef26687d63a37e29/agent_input/task.md) | 46/56/61 原子模型验证有效，但作者终态及 PA 的部分终态仍在公开输入。 |
| group_1 / [`paper_e31cc7bc7b21b610`](#paper_e31cc7bc7b21b610) | [AR](../final_verified_autonomous_research/paper_e31cc7bc7b21b610/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_e31cc7bc7b21b610/agent_input/task.md) | 各 168 实频，ΔE=1.43848；1.44±1.5 允许负值，需显式与能序联合判定。 |
| group_1 / [`paper_80cc1ffb2cf73fc5`](#paper_80cc1ffb2cf73fc5) | [AR](../final_verified_autonomous_research/paper_80cc1ffb2cf73fc5/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_80cc1ffb2cf73fc5/agent_input/task.md) | 只有实验窗口，没有峰表/trace；PR mode 条款允许质疑，final 条款却强制肯定解释。 |
| group_2 / [`paper_a3892396b1843698`](#paper_a3892396b1843698) | [AR](../final_verified_autonomous_research/paper_a3892396b1843698/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_a3892396b1843698/agent_input/task.md) | 只公开反应物 3a，不公开 TS/产品；两通道 TS/IRC/端点链完整。 |
| group_2 / [`paper_46f6118697c6397c`](#paper_46f6118697c6397c) | [AR](../final_verified_autonomous_research/paper_46f6118697c6397c/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_46f6118697c6397c/agent_input/task.md) | CIF 自包含，三分支 Opt/Freq+TD50 成立；正文/SI 数值冲突和因果范围需明示。 |
| group_2 / [`paper_a3968806251093cd`](#paper_a3968806251093cd) | [AR](../hold_verified_autonomous_research/paper_a3968806251093cd/agent_input/task.md)、[PR](../hold_verified_paper_reproduction/paper_a3968806251093cd/agent_input/task.md) | 7a 位置异构体算错；隐藏实验列却要求 MAE；标签映射、方法胜负与失败 schema 未对齐。 |
| group_2 / [`paper_d8e5490cd9942f4f`](#paper_d8e5490cd9942f4f) | [AR](../final_verified_autonomous_research/paper_d8e5490cd9942f4f/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_d8e5490cd9942f4f/agent_input/task.md) | 两端点各 237 实频，ΔG=4.393821；不是完整构象搜索，作者端点保留边界待确认。 |
| group_2 / [`paper_c23cfabbd34b087f`](#paper_c23cfabbd34b087f) | [AR](../final_verified_autonomous_research/paper_c23cfabbd34b087f/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_c23cfabbd34b087f/agent_input/task.md) | 102原子截短模型，300实频+TD20有据；不得外推实验长链/聚集体系。 |
| group_2 / [`paper_d7967e22bb965daa`](#paper_d7967e22bb965daa) | [PR](../final_verified_paper_reproduction/paper_d7967e22bb965daa/agent_input/task.md) | 四个68原子SI TS公开；四局部势垒真实有据，不能用给定TS替代TS搜索。 |
| group_4 / [`paper_5d94285cfbd51973`](#paper_5d94285cfbd51973) | [AR](../final_verified_autonomous_research/paper_5d94285cfbd51973/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_5d94285cfbd51973/agent_input/task.md) | SMILES自包含；9极小值与9敏感性单点支持；按公开conventional公式评分。 |
| group_4 / [`paper_b33676a2051f5e91`](#paper_b33676a2051f5e91) | [AR](../final_verified_autonomous_research/paper_b33676a2051f5e91/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_b33676a2051f5e91/agent_input/task.md) | 反应物输入合法；TS/IRC支持指定通道；AR 条件仅写validated_result，未显式限制数值的通道。 |
| group_4 / [`paper_46a9ca0dab36dd9e`](#paper_46a9ca0dab36dd9e) | [AR](../final_verified_autonomous_research/paper_46a9ca0dab36dd9e/agent_input/task.md)、[PR](../final_verified_paper_reproduction/paper_46a9ca0dab36dd9e/agent_input/task.md) | 正确离子对已算LMCT；任择激发态/分区却要求62.4/4.3%，MeCN边界也不清。 |
| group_6 / [`paper_44f9727c4e9a4b6f`](#paper_44f9727c4e9a4b6f) | [PR](../final_verified_paper_reproduction/paper_44f9727c4e9a4b6f/agent_input/task.md) | 87原子作者终态泄露几何答案；校准常数是必要输入应保留；BS/HS/位移真实成立。 |

<a id="paper_d2d08c91f34da1cb"></a>

### group_1 / paper_d2d08c91f34da1cb — Rhodamine101 两态低频振动

模式：AR、PR。**当前判断：AR/PR 的振动数值有真实支持；优化坐标的给定对象边界需验收，PR 模式趋势措辞建议收紧。**

**原文依据。**正文 PDF p3 计算方法、p6 模式解释、p7 Table 1；SI PDF p1–4 两电子态坐标。实验 SLT 峰是允许的观测输入，不是作者计算频率。 [正文](../../papers/paper_d2d08c91f34da1cb/documents/main.pdf)、[SI](../../papers/paper_d2d08c91f34da1cb/documents/supplementary_001.pdf)。

**真实计算支持。**真实 S0/S1 Opt/Freq 均有 195 实频、0 虚频；窗口内模式完整归档，24 个实验有效配对，MAE 1.262626 cm⁻¹，最大误差 3.097158 cm⁻¹。位移匹配和片段动能分析保留模式交换/混合、正移和近乎不变的例外。evaluator 是有不确定性的语义比较，不硬性要求所有模式红移或 max<3。

计算归档：[AR reference](../final_verified_autonomous_research/paper_d2d08c91f34da1cb/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_d2d08c91f34da1cb/evaluation/verified_computation_reference.md)。已有证据：[provenance/mode_closure_audit_20260915.json](../../docs/verification/group_1/paper_d2d08c91f34da1cb/provenance/mode_closure_audit_20260915.json)；[artifacts/mode_identity_complete_20260914.json](../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/mode_identity_complete_20260914.json)；[artifacts/mode_character_review_20260915.json](../../docs/verification/group_1/paper_d2d08c91f34da1cb/artifacts/mode_character_review_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**两模式的 S0/S1 XYZ 都与 SI 优化结构一致。当前题面把目标限定为给定两态对象的振动性质，未公开频率、位移向量或 MAE，因此不能与“直接给待求 TS”一概等同；但前轮由我自行将这一范围认定为可放行，不能代替你的验收。PR `reference_key_points.json::pr_result_state_shifts` 写 xanthene-associated 红移、carboxyphenyl-associated 蓝移，`expected` 虽有 assignment uncertainty，仍可能被理解为所有相应模式都应同方向。真实位移审查保留 1/2 模式交换，模式 4、13、14 等正移，以及模式 8 约 +0.005802 cm⁻¹ 的近乎不变；不能删去这些例外来满足泛化结论。AR 允许从证据解释，未发现同等程度的强制趋势要求。

**建议修改（待确认）。**若你接受给定两态结构的振动子问题，保留必要几何但把 task、XYZ 注释、task_info 的来源说法统一；不宣称结构发现。PR 评分明确按位移/局部坐标对应比较，允许混合模式、交换、近零位移及反例，以有限趋势和不确定性计分，不要求每个模式都红移或蓝移。实验 CSV 的缺测项继续为空，不填作者计算值。

**对现有验证结论的影响。**无需因此重算。现有 24 个配对及全窗口模式足以支持限定的振动比较；不支持“所有骨架模式都红移”、唯一片段标签或超快能量流机制。

<a id="paper_6f9a36fff6964313"></a>

### group_1 / paper_6f9a36fff6964313 — 三体系 Mulliken 电荷

模式：AR、PR。**当前判断：PR 的方法—电荷评分协议未对齐；AR 的单构象覆盖/稳健性措辞需要澄清，而不是重新判为未验证。**

**原文依据。**SI S16 的两层级路线与 Fig. S7 的 Mulliken 电荷；原文图示阳离子片段，而当前任务明确的完整离子对必须保留 OTf。 [正文](../../papers/paper_6f9a36fff6964313/documents/main.pdf)、[SI](../../papers/paper_6f9a36fff6964313/documents/supplementary_001.pdf)。

**真实计算支持。**B3LYP-D3BJ/6-31G(d,p)/IEFPCM(MeCN) 三次 Opt/Freq 分别 45/90/105 实频；同几何 M062X-D3/def2TZVP/SMD(MeCN) 单点给出 qC(TFAP)=0.203728、qC(TMT)=0.198533、qN(PTMA)=0.040059、qN(TMT)=0.058695 e；四值落在 PR 现行 ±0.02 e 内。SP/优化几何依赖已核对。实际只有每体系一个验证构象。

计算归档：[AR reference](../final_verified_autonomous_research/paper_6f9a36fff6964313/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_6f9a36fff6964313/evaluation/verified_computation_reference.md)。已有证据：[provenance/charge_closure_audit_20260915.json](../../docs/verification/group_1/paper_6f9a36fff6964313/provenance/charge_closure_audit_20260915.json)；[artifacts/complete_author_charges_20260915.json](../../docs/verification/group_1/paper_6f9a36fff6964313/artifacts/complete_author_charges_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**输入三套 SMILES、OTf、电荷/自旋、MeCN、目标原子环境完整，无作者坐标或电荷答案。PR 允许自行选方法/基组/离子对构象，却以四个固定 Mulliken 电荷及 ±0.02 e 比较；这种量强烈依赖协议，不是唯一实验真值。验证的 TMT 氮电荷 0.058695 e 距当前上限仅约 0.001305 e。AR 不硬比四个数值，但 task 要求单起点时说明更广覆盖为何 immaterial，并评估敏感性/达到结论不随新增构象改变的停止条件；现有真实链每体系仅一个已验证构象，私有字段映射也明确没有建立广泛稳健性。四电荷及差值可计算已获支持，不能据此证明构象不变性。

**建议修改（待确认）。**PR 建议公开无答案的 SI 主比较协议：B3LYP-D3BJ/6-31G(d,p)/IEFPCM(MeCN) 优化频率，M062X-D3/def2TZVP/SMD(MeCN) 的对应几何 Mulliken 单点；定义原子环境、完整离子对和合法的构象选择/覆盖报告。额外方法可作敏感性，不用它的数值直接套主协议 gold。AR 保留自主路线与证据型比较，把单构象限制写成必须披露的不确定性，不要求未经证据的“广泛覆盖无影响”。如要继续允许 PR 任意方法作主结果，则需要你另行认可方法匹配的评分规则，而非私自放宽容差。

**对现有验证结论的影响。**现有作者路线足以证明这三个正确模型能得到当前参考量附近的结果；需修比较与覆盖表述，不自动追加计算，也不把 AR 自主探索步骤未被历史验证逐条执行视为失败。

<a id="paper_746e066c163800d8"></a>

### group_1 / paper_746e066c163800d8 — compound 5 螺烯内缘扭转

模式：AR、PR。**当前判断：AR/PR 均有待求几何答案泄露，另有二面角正负约定与失败分支问题。**

**原文依据。**正文 PDF/印刷 p4 给出实验约 27.0° 和优化结构讨论；SI PDF p45–46 为 compound 5 优化坐标。 [正文](../../papers/paper_746e066c163800d8/documents/main.pdf)、[SI](../../papers/paper_746e066c163800d8/documents/supplementary_001.pdf)。

**真实计算支持。**作者路线优化/频率 210 实频，实际平均扭转 27.09676855°；紧收敛复核 27.09673780°。这些确实支持论文结果，但不能授权公开其终态。

计算归档：[AR reference](../final_verified_autonomous_research/paper_746e066c163800d8/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_746e066c163800d8/evaluation/verified_computation_reference.md)。已有证据：[provenance/inner_rim_closure_audit_20260915.json](../../docs/verification/group_1/paper_746e066c163800d8/provenance/inner_rim_closure_audit_20260915.json)；[artifacts/inner_rim_complete_20260915.json](../../docs/verification/group_1/paper_746e066c163800d8/artifacts/inner_rim_complete_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**`agent_input/data/inputs/compound5.xyz` 的 72/72 坐标对应 SI p45–46 的优化结构；目标正是该结构五个 inner-rim torsion 的平均值，不能靠 starting 注释解除答案泄露。task 允许 signed 或 absolute convention，但数值评分直接对正 27.1°，手性/原子排列导致的符号翻转可能被误罚。两模式 schema 的失败分支仍要求 `validation.imaginary_modes` 为整数；优化失败而尚未求 Hessian 时，既不能如实填 null/缺省，也不能伪填 0。本轮用纯软件样例确认了该 schema 冲突。

**建议修改（待确认）。**批准后用经过正文/SI 核对的连接图独立构建同身份初始几何，保留原子映射；作者终态移至 `evaluation/author_results/`，不微扰终态冒充独立构建。建议主评分统一为五个扭转绝对值的算术平均，同时保留五个带符号原值与原子四元组；若选有符号定义，应明确手性/方向等价变换。仅失败分支允许未计算的虚频数为 null 并强制原因，成功分支仍严格验证。实验 27.0° 是实验校准，不是计算终态坐标，可按已声明用途保留。

**对现有验证结论的影响。**210 实频和约 27.09677° 的作者路线验证有效；问题是公开答案和评分口径，不是科学量算不出来。更换初始结构不自动要求重做历史验证。

<a id="paper_5ea491c741fbd8d4"></a>

### group_1 / paper_5ea491c741fbd8d4 — isoxazole 1a 五候选轨道

模式：AR、PR。**当前判断：AR/PR 的身份、无泄露输入及成功计算成立；需修失败候选 schema，并确认方法自由与轨道数值的比较口径。**

**原文依据。**正文 PDF p3–5 的对象/计算方法、p7 Table 2 的 isoxazole 1a 前线轨道参考。 [正文](../../papers/paper_5ea491c741fbd8d4/documents/main.pdf)、[SI](../../papers/paper_5ea491c741fbd8d4/documents/supplementary_001.pdf)。

**真实计算支持。**五条独立起始候选 Opt/Freq 均 75 实频，几何去重为 3 个不同极小值；selected seed 303 的 HOMO −6.56393059 eV、LUMO −2.88386271 eV、gap 3.68006788 eV，与 −6.3362/−2.7171/3.6191 的 AR、PR 既定容差均相容，gap 为实际差值。

计算归档：[AR reference](../final_verified_autonomous_research/paper_5ea491c741fbd8d4/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/verified_computation_reference.md)。已有证据：[provenance/orbital_closure_audit_20260915.json](../../docs/verification/group_1/paper_5ea491c741fbd8d4/provenance/orbital_closure_audit_20260915.json)；[artifacts/author_orbitals_20260915.json](../../docs/verification/group_1/paper_5ea491c741fbd8d4/artifacts/author_orbitals_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**公开 E-SMILES 而非作者 3D，未发现答案泄露。真实五起点计算得到三个不同极小值，数值在当前容差内。两模式 task 明确允许 `bounded_failure`，但 schema 对每个候选都要求整数 `stationary_point_test.imaginary_frequency_count`（minimum=0），并非仅成功候选才必填；尚未完成 Hessian 的失败候选不能如实表示 unknown。这一缺口在软件样例中可复现。此外 PR 还写“without attempting to identify the paper's method”，却按特定计算来源的 HOMO/LUMO/gap 评分；一次作者路线算中容差证明可行，不证明所有合理方法都应过分数线。

**建议修改（待确认）。**先修小范围数据契约：失败/未计算候选允许 null，并要求明确状态与诊断；成功选中候选仍必须有真实频率证据，不把 0 当占位符。轨道评分建议在你确认后给 PR 明确主比较方法，其他方法作补充；AR 仍保留自主路线，明确模型相关量的比较限制。保留既有目标、容差和正确 E 身份，不为了通过改参考值。

**对现有验证结论的影响。**不是需要补算的结论；已有结果支持当前分子轨道子问题。schema 修复不会改变成功任务的科学目标。方法公平性属于待确认边界，不宜写成“所有方法必然可复现”。

<a id="paper_a0f6b899582cb9f7"></a>

### group_1 / paper_a0f6b899582cb9f7 — M3 身份、几何与多极矩

模式：AR、PR。**当前判断：AR/PR 未发现新的直接泄露或必需数据缺失；前轮张量定义修复需由你验收。**

**原文依据。**正文 M3 定义及 N···S/平面性讨论；SI PDF p7 Table S1，M3 三个对角元 −83.67/−103.14/−108.35。表头 Debye 对二阶矩量纲不完整，且非零迹说明不能套 traceless 张量。 [正文](../../papers/paper_a0f6b899582cb9f7/documents/main.pdf)、[SI](../../papers/paper_a0f6b899582cb9f7/documents/supplementary_001.pdf)。

**真实计算支持。**三个真实优化极小值，66 实频；选定结构 dipole=0 D、平面 RMS 0.00025046 Å、N···S=2.99065 Å，旋转后的原始张量 Qzz=−111.07681064 DÅ，处于 −108.35±5 既有范围。不是 traceless 或乘三的另一 convention。

计算归档：[AR reference](../final_verified_autonomous_research/paper_a0f6b899582cb9f7/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_a0f6b899582cb9f7/evaluation/verified_computation_reference.md)。已有证据：[provenance/correct_m3_closure_20260915.json](../../docs/verification/group_1/paper_a0f6b899582cb9f7/provenance/correct_m3_closure_20260915.json)；[artifacts/correct_identity_multipoles_20260915.json](../../docs/verification/group_1/paper_a0f6b899582cb9f7/artifacts/correct_identity_multipoles_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**当前 `m3_identity.json` 与独立 ETKDG/MMFF starter 一致，非作者终态。当前 task/schema 已明确核+电子的 raw Cartesian charge second moment、声明原点、Debye Å、拟合分子面法向和完整张量旋转。前轮改过这些定义说明，移动回来时全部保留，没有再改。SI p7 Table S1 的单位写 Debye 不完整，且对角元非零迹，不应换成 traceless quadrupole；这是需要验收的来源解释，而非放宽评分。与其他轨道/多极矩任务相同，方法自由不意味着每种泛函/构象都必须产生相同数值。

**建议修改（待确认）。**建议验收并保留已有物理量定义、完整张量/原点/轴证据和独立 starter；不缩放原 gold、不改容差、不把初始实验室 z 轴当 stacking 法向。若将来统一主比较协议，按本篇单独确认，不批量换方法。

**对现有验证结论的影响。**三条真实极小值、零偶极、平面性/N···S 和 Qzz 都有输出支持。未发现需要新增量化计算的缺口；孤立分子多极矩不能外推为固体结合能或器件性能证明。

<a id="paper_ef26687d63a37e29"></a>

### group_1 / paper_ef26687d63a37e29 — free / PO / PA 接触、电荷与 ESP

模式：AR、PR。**当前判断：AR/PR 仍使用作者优化几何；前轮补齐身份并没有消除答案信息。**

**原文依据。**正文 Fig. 6（PDF p8，相关解释 p10）；SI PDF p35–40 的 free/PO/PA 优化坐标及接触量。 [正文](../../papers/paper_ef26687d63a37e29/documents/main.pdf)、[SI](../../papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf)。

**真实计算支持。**完整正确 46/56/61 原子模型已有真实极小值验证；P 的 ADCH 电荷 −0.018993/0.447060/0.455684 e，PO/PA 六个 O···P/H 接触均通过现有 ±0.25 Å，MEP 链可追溯。旧截断模型不是本次采纳的科学证据。

计算归档：[AR reference](../final_verified_autonomous_research/paper_ef26687d63a37e29/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_ef26687d63a37e29/evaluation/verified_computation_reference.md)。已有证据：[provenance/complete_pa_closure_20260915.json](../../docs/verification/group_1/paper_ef26687d63a37e29/provenance/complete_pa_closure_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**前轮将 AR 的缺 P/O 截断 free/PO 补齐至正确 46/56 原子，应保留这一修复，不能用原包覆盖回去。当前 free/PO 全部坐标、PA 的 51/61 坐标来自 SI p35–40 的作者优化结构；PA 后补 10 个芳环原子不使整个结构独立。目标同时评几何接触、ADCH 电荷和 MEP，故仍有答案结构信息。不能把“来自终态”夸大成“每个输入距离都等于最终 gold”：本轮测得公开 PO 的 P46–O49 约 2.8 Å，而作者路线后续优化才得到目标附近 O···P；来源及收敛盆地提示风险仍在。公开图的 P46–C50≈1.922 Å、O49–C47≈1.430 Å，支持 ring-opened 描述，未确认新的 PO 身份错误。

**建议修改（待确认）。**在正确完整分子图基础上独立构建 free/PO/PA 初始结构，保留 charge/spin、P–N–ethyl αH/βH 角色、PO/PA 氧的明确映射；原坐标只留 `evaluation/author_results/`。PA 必须提供完整结构定义，不能再次丢芳环。保持接触/电荷/MEP 的既有目标；不同于密度的 signed ESP 解释和局部模型结论界限继续保留。不要只删 provenance 或改注释。

**对现有验证结论的影响。**完整三模型已有有效优化、频率及性质分析；不能把历史截断输入或未修复结构作为证据。没有因泄露修复本身要求重新计算，也未擅自改非共价/成键的科学解释。

<a id="paper_e31cc7bc7b21b610"></a>

### group_1 / paper_e31cc7bc7b21b610 — egan-IrCl cis-α / cis-β 相对能

模式：AR、PR。**当前判断：AR/PR 的电子能比较可计算；有数值容差与排序的一致性风险，给定终态边界待验收。**

**原文依据。**SI PDF p24–27 的 cis-α/cis-β egan-IrCl 完整优化坐标；原文电子能比较（1.44 kcal/mol）。 [正文](../../papers/paper_e31cc7bc7b21b610/documents/main.pdf)、[SI](../../papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf)。

**真实计算支持。**Gaussian B3LYP、Ir SDD/其余 6-31G(d)，气相两条 Opt/Freq 均 168 实频；Eα=−2204.52499151、Eβ=−2204.52269915 Eh，(Eβ−Eα)×627.5094740631=1.43847762 kcal/mol，满足现行 1.44±1.5。

计算归档：[AR reference](../final_verified_autonomous_research/paper_e31cc7bc7b21b610/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/verified_computation_reference.md)。已有证据：[provenance/correct_identity_closure_20260915.json](../../docs/verification/group_1/paper_e31cc7bc7b21b610/provenance/correct_identity_closure_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**两份 58 原子 XYZ 为作者 cis-α/cis-β 优化结构，当前目标是给定异构体电子能比较，不是搜索异构体。坐标没有直接存储 ΔE，但不应未经你的验收就宣布这是可公开的固定对象边界。`scoring_rules.json` 的目标 1.44±1.5 kcal/mol 允许区间 [−0.06,2.94]，而 `reference_key_points.json` 要求 ΔE=Eβ−Eα>0、α 较低。当前独立语义评分可能排除错误排序，但数值项自身不能保证，不能把容差内等同于结论正确。AR 的 status 只允许 complete 是当前既定契约，task 也未承诺 bounded-failure 分支，未把这一点误报为新冲突。

**建议修改（待确认）。**你确认给定异构体比较范围后，保留必要结构但统一来源描述。数值比较增加明确的定义、正号和 lower_energy_identity 联合核对；保持现有 1.44 和 1.5，不自行缩容差或把负能差算作正确论文排序。仍区分 electronic energy 与自由能/动力学。

**对现有验证结论的影响。**真实 Eα/Eβ 及两极小值直接支持当前正能差；不需要重新计算。需修的是评分可读性/一致性，不是已有计算反号。

<a id="paper_80cc1ffb2cf73fc5"></a>

### group_1 / paper_80cc1ffb2cf73fc5 — Z1 Franck–Condon 谱与模式归属

模式：AR、PR。**当前判断：AR/PR 的 FC 和模式计算成立；实验比较的输入/职责未闭合，PR 还有允许质疑与强制支持的评分冲突。**

**原文依据。**SI PDF p6 的 Z1 anion 坐标与正文 FC 解释；实验窗口/电子脱附背景与任务 problem_definition 一致。 [正文](../../papers/paper_80cc1ffb2cf73fc5/documents/main.pdf)、[SI](../../papers/paper_80cc1ffb2cf73fc5/documents/supplementary_001.pdf)。

**真实计算支持。**anion/neutral 各 75 实频，FC 四个实际成功段及模式后处理完整；scale 0.9566、T=6 K、HWHM=2 cm⁻¹、grid=1 cm⁻¹ 的历史谱，主导面内 mode 3：85.9573 cm⁻¹、HR 1.20932，约占选定强度 99.63%。上述设置只在 private reference 记录，不强迫 AR 路线。

计算归档：[AR reference](../final_verified_autonomous_research/paper_80cc1ffb2cf73fc5/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_80cc1ffb2cf73fc5/evaluation/verified_computation_reference.md)。已有证据：[provenance/fc_closure_audit_20260914.json](../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/provenance/fc_closure_audit_20260914.json)；[artifacts/fc_closure_20260914/fc_analysis.json](../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/fc_closure_20260914/fc_analysis.json)；[artifacts/fc_closure_20260914/modes_full.json](../../docs/verification/group_1/paper_80cc1ffb2cf73fc5/artifacts/fc_closure_20260914/modes_full.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**`problem_definition.json` 只给 19400–20100 cm⁻¹ 窗口和物理通道，没有可比的实验峰位/逐点谱；task/schema 又明确允许缺测时 MAE=null、不得编造观测。因此计算端确实可执行，但不能让 agent 证明未提供的实验突出峰是否被解释。PR `pr_r_mode` 允许用计算证据争议 mode 3 指认，`reference_conclusions.json::pr_c_final` 和 `scoring_rules.json::pr_r_final` 却要求正面支持 prominent-feature FC 解释及 mode 3；两分支不一致。AR 的 expected 已允许支持或否定，较宽，但 statement 仍有 spectral agreement，建议避免把未测比较当已验证。公开作者 anion 几何没有同时给 neutral、FC 强度或模式结果，其给定初态边界单列验收。

**建议修改（待确认）。**推荐保留实验解释目标：从正文/SI提取仅实验观测的峰表或可用 trace、单位/不确定性和统一对齐规则，不能夹带计算模式归属/作者结论；若原文不足以形成可靠可用观测，再请你决定是否把当前必评范围限制为 FC 模式/强度的内部解释，实验一致性明确 unavailable。同步 task/schema、关键点、final 规则，不能一处允许有证据的反驳、另一处又强制支持。mode 3 用位移/物理身份匹配，不硬把任意方法下的第 3 个编号当同一振动。

**对现有验证结论的影响。**两态 75 实频、成功 FC 段、85.9573 cm⁻¹/HR 1.20932 等已有真实记录；它们证明内部 FC 结论可计算，不替代缺失的实测比较。优先补观测/利用已有谱后处理，不自动增加电子结构计算。

<a id="paper_a3892396b1843698"></a>

### group_2 / paper_a3892396b1843698 — 3a [3,3] / [5,5] 重排势垒

模式：AR、PR。**当前判断：AR/PR 当前 TS 子问题的身份、公开输入和作者路线证据一致；未发现新的实质性缺口。**

**原文依据。**正文 PDF p4 的 [3,3]/[5,5] 势垒；SI PDF p6 热化学、p11 反应物 3a 坐标。 [正文](../../papers/paper_a3892396b1843698/documents/main.pdf)、[SI](../../papers/paper_a3892396b1843698/documents/supplementary_001.pdf)。

**真实计算支持。**ωB97XD/def2SVP Opt/Freq→def2TZVPP 单点及一致的 entropy-only Grimme qRRHO；两个 TS 各一虚频，双向 IRC 和四个后续端点极小值闭合。ΔG‡为 23.50589160、26.22790785 kcal/mol，分别符合 23.5/26.2±3。构型/通道映射支持势垒顺序。

计算归档：[AR reference](../final_verified_autonomous_research/paper_a3892396b1843698/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_a3892396b1843698/evaluation/verified_computation_reference.md)。已有证据：[AUTHOR_ROUTE_FINAL_AUDIT_20260914.md](../../docs/verification/group_2/paper_a3892396b1843698/AUTHOR_ROUTE_FINAL_AUDIT_20260914.md)；[provenance/author_route_evaluation_audit.json](../../docs/verification/group_2/paper_a3892396b1843698/provenance/author_route_evaluation_audit.json)；[provenance/independent_author_route_numeric_20260914.json](../../docs/verification/group_2/paper_a3892396b1843698/provenance/independent_author_route_numeric_20260914.json)；[provenance/endpoint_minima_audit_20260914.json](../../docs/verification/group_2/paper_a3892396b1843698/provenance/endpoint_minima_audit_20260914.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**25 原子公开 3a 虽源于 SI 优化结构，但在本题是反应物；待求对象是 [3,3]/[5,5] TS、势垒及其比较，不是发现反应物的几何。不能把合法反应物与待求 TS 混同。两个命名通道是 task 已声明的比较范围，AR 不应额外输入谁更优。现有热化学、单位和温度边界与验证的 entropy-only Grimme qRRHO 处理对应，未发现隐藏必需实验数据。

**建议修改（待确认）。**建议保留现有目标、输入、两个通道和评分；验收时注明历史验证可用作者信息，实际评测仍须 agent 自行构建 TS。只需确认迁回后的结构来源说法一致及私有文件隔离，不为“公开起点没有盲跑”新增计算要求。

**对现有验证结论的影响。**两条真实 TS（各一虚频）、双向 IRC、四个后续端点极小值以及 23.50589/26.22791 kcal/mol 支持当前比较；不宣称模型盲测已完成。

<a id="paper_46f6118697c6397c"></a>

### group_2 / paper_46f6118697c6397c — compound 2 三分支 TD50

模式：AR、PR。**当前判断：AR/PR 的 compound-2 TD 子问题已获支持；保留 SI 数值与局部解释界限，不扩张为全取代基因果验证。**

**原文依据。**SI PDF p18 Table S3 给出 3.8436 eV/322.58 nm/f=0.4243；正文 p4 的 4.33 eV 与其 323 nm 不自洽。当前源 evaluator 本来采用 SI 数值，本轮不择值或改目标。 [正文](../../papers/paper_46f6118697c6397c/documents/main.pdf)、[SI](../../papers/paper_46f6118697c6397c/documents/supplementary_001.pdf)。

**真实计算支持。**三条 CIF 派生分支 B1_op2/B2_A_op5/B2_B_op5 均 198 实频，分别 TD50；三条最大 f 均为当次第 5 态。E/f=3.8445/0.4733、3.8138/0.4255、3.8208/0.4292，全部在现行 ±0.15 eV/±0.05 内。代表支 217→222 映射 HOMO−4→LUMO，有轨道性质依据。

计算归档：[AR reference](../final_verified_autonomous_research/paper_46f6118697c6397c/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_46f6118697c6397c/evaluation/verified_computation_reference.md)。已有证据：[provenance/author_route_evaluation_audit.json](../../docs/verification/group_2/paper_46f6118697c6397c/provenance/author_route_evaluation_audit.json)；[provenance/compound2_cif_preprocessing.json](../../docs/verification/group_2/paper_46f6118697c6397c/provenance/compound2_cif_preprocessing.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**实验 CIF 是身份/起点，不是作者计算激发态答案。三条对称/无序分支均给正确 68 原子四 triflate 模型；数值支持当前 SI 来源的 3.8436 eV/f=0.4243。正文 p4 写 4.33 eV 又写 323 nm，二者不自洽；现行 evaluator 从一开始取 SI Table S3，不能说两处原文完全一致，也不能按本地值改 gold。两模式 final 解释含 triflate 稳定 N6 轨道；现行措辞是 consistent with 且限定范围，故不直接判为验证失败。但本批只算 compound 2，不证明全部 1/3/4 替代物的对照因果结论。态/轨道编号随分支和方法变化，不能把第 5 态或 217→222 固定为公开答案。

**建议修改（待确认）。**建议保留 SI 的既有目标，记录正文冲突依据；保持现有完整 CIF 及可复现的分子提取要求。若再澄清文字，只把 final 限定为 compound-2 的跃迁性质与“和吸电子解释相容”，不能要求未计算的其他取代基顺序或唯一因果证明；轨道/态按物理性质和证据匹配，不按程序编号。

**对现有验证结论的影响。**三分支各 198 实频、TD50 的 E/f 均满足现有容差；现有单体系目标无新增量化计算缺口。未将历史代表分支选择冒充面向 agent 的强制规则。

<a id="paper_a3968806251093cd"></a>

### group_2 / paper_a3968806251093cd — compound 7a 两种泛函几何

模式：AR、PR。**当前判断：AR/PR 当前分子图与论文对象不一致；现有验证不能认证正确 7a。另有缺实验数据/映射及方法比较问题。**

**原文依据。**正文 PDF p4 / Fig. 3：pyrazole N1–N2–C9–C8–C7，N1 连 phenyl，C7 连 O1-chlorophenyl ether，C8 接 imine，C9 接 methyl；SI 几何比较表与此标签体系对应。 [正文](../../papers/paper_a3968806251093cd/documents/main.pdf)、[SI](../../papers/paper_a3968806251093cd/documents/supplementary_001.pdf)。

**真实计算支持。**两条 B3LYP/CAM-B3LYP Opt/Freq 确实成功，各 132 实频，但同为上述错误图。B3LYP 末态 N1–C7=2.196492 Å，N1–C8=1.376571 Å，O1–C7=1.368864 Å。CAM 和现存生成 SDF/7a_repaired.xyz 同样错误。原几何 MAE 包含不应作键角的非键合三元组，无法证明正确论文 7a 的结论。

计算归档：[AR reference](../hold_verified_autonomous_research/paper_a3968806251093cd/evaluation/verified_computation_reference.md)、[PR reference](../hold_verified_paper_reproduction/paper_a3968806251093cd/evaluation/verified_computation_reference.md)。已有证据：[provenance/author_route_evaluation_audit.json](../../docs/verification/group_2/paper_a3968806251093cd/provenance/author_route_evaluation_audit.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**`molecule.json::smiles` 与名称/正文 Fig.3 不同：论文五元环为 N1–N2–C9–C8–C7，O1-phenoxy 接 C7，imine 接 C8；当前图使 O-bearing 碳不邻接 N1，交换了取代位置。两个历史 Opt/Freq 均132实频，却沿相同错误图优化，不能靠相同分子式 C20H17ClN6OS 或 normal termination 认证。B3LYP 终态 N1–C7=2.196492 Å（非预期环键），N1–C8=1.376571 Å。`atom_map.json` 仅列标签组合，缺 label→图原子映射，且 Cl1/Cl2 在仅一个氯的体系中未公开解释。task 要求对 withheld SCXRD 算 MAE/RMSE，实验列却未给；PR 任择 conventional/range-separated 模型却按 B3LYP/CAM-B3LYP 的优劣评分。历史每模型48行含重复 C6-N1-C7，当前去重47行。失败 schema 仍强制非空数值 metrics，无法如实记录无可比较数据。

**建议修改（待确认）。**优先按正文结构图/SI重建并人工复核正确连接性，给完整原子标签映射/别名规则，绝不凭公式或擅猜 SMILES。建议公开仅 SCXRD 的观测列（13键/23角/11扭转），保留计算列和模型优劣私有；这样 agent 才能自行算误差。若要隐藏实验数据，则把比较职责整体移至 evaluator，并同步改 task/schema 的交付，不能两边都要求。PR 若继续评论文 B3LYP 对 CAM-B3LYP，公开该方法对作为路线但不告知谁更好；AR 保留自主方法不强制同一胜负。统一47行并修失败分支。以上均需你先确认。

**对现有验证结论的影响。**这是本批最明确的科学身份验证缺口，不是旧 schema 名称不同。当前检查的两条主链、CAM/B3LYP 输出及 7a_repaired.xyz/SDF 都未找到正确位置异构体证据；先请对应 group 核对是否另有正确图的存量结果。找得到则重提取/重映射，找不到才由你决定最小补充验证，不能把错误分子日志重标为正确，也不在本轮重算。

<a id="paper_d8e5490cd9942f4f"></a>

### group_2 / paper_d8e5490cd9942f4f — syn / anti La-KHQ 热化学

模式：AR、PR。**当前判断：AR/PR 的指定 syn/anti 自由能比较成立；给定作者端点的范围仍应由你验收。**

**原文依据。**正文 PDF p5；SI PDF p21–22 Eq. S2 / Table S2 的 ΔG 定义与 4.2 kcal/mol，p85–91 syn/anti 优化结构。 [正文](../../papers/paper_d8e5490cd9942f4f/documents/main.pdf)、[SI](../../papers/paper_d8e5490cd9942f4f/documents/supplementary_001.pdf)。

**真实计算支持。**ωB97XD、La LCRECP46MWB、SMD(水) 两 Opt/Freq 均 237 实频；ΔG=4.393821 kcal/mol，在4.2±1内。相同分子数的1 M标准态校正相消，不把1 atm单个绝对 G直接冒称不经校正的1 M绝对值。

计算归档：[AR reference](../final_verified_autonomous_research/paper_d8e5490cd9942f4f/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_d8e5490cd9942f4f/evaluation/verified_computation_reference.md)。已有证据：[provenance/author_route_evaluation_audit.json](../../docs/verification/group_2/paper_d8e5490cd9942f4f/provenance/author_route_evaluation_audit.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**公开两份81原子作者优化结构，未提供能序/能差；题面本来限定指定 syn/anti 对象比较，不能宣传完整构象发现或溶液平衡。与待求几何直接被给出不同，ΔG 仍需实际算，但保留作者端点作为公开对象的范围不能由维护 agent 单方面确认。部分 XYZ/task_info 仍称 starting，若验收为给定对象，来源应统一说清而不是暗示独立生成。

**建议修改（待确认）。**建议按当前指定两个异构体的水连续介质、298 K、1 M 自由能子问题验收，保持 ΔG=Ganti−Gsyn 和 La 的正确模型。统一来源/范围，不删必要 La 结构；若你要求本篇也评独立构象生成，再单独批准从连接性构建 starter，不临时扩展既有目标。

**对现有验证结论的影响。**两条237实频及4.393821 kcal/mol支持当前两个端点；相同分子数的标准态修正相消。有局部验证，不把它夸成全构象/形成反应/完整溶液平衡验证。

<a id="paper_c23cfabbd34b087f"></a>

### group_2 / paper_c23cfabbd34b087f — 1M-TIPS D3 / PCM TD20

模式：AR、PR。**当前判断：AR/PR 的固定模型吸收成立；作者优化几何作为已给定模型的角色待验收。**

**原文依据。**正文 PDF p4 的模型近红外吸收与跃迁指认；SI PDF p42 计算方法、p44–46 的 1M-TIPS 模型坐标。 [正文](../../papers/paper_c23cfabbd34b087f/documents/main.pdf)、[SI](../../papers/paper_c23cfabbd34b087f/documents/supplementary_001.pdf)。

**真实计算支持。**真实显式 D3/PCM(CHCl3) 模型 Opt/Freq 有 300 实频，TD20 得到 735.93 nm/f=1.2539；209→210 为 HOMO→LUMO，系数0.69912，支持 π–π* 指认。与735±25 nm、1.24±0.25相容。

计算归档：[AR reference](../final_verified_autonomous_research/paper_c23cfabbd34b087f/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_c23cfabbd34b087f/evaluation/verified_computation_reference.md)。已有证据：[provenance/author_route_evaluation_audit.json](../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/author_route_evaluation_audit.json)；[provenance/1m_tips_td_state_parse.json](../../docs/verification/group_2/paper_c23cfabbd34b087f/provenance/1m_tips_td_state_parse.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**102原子 `1M-TIPS.xyz` 为作者优化几何；当前目标是给定 C58H42Si2 模型的垂直吸收及电子指认，不是发现该几何，所以未直接公开波长/振子强度答案。此固定模型范围仍需由你验收，不应由我自行宣布可迁 final。XYZ 注释仍有 SI-derived initial，来源口径可统一。task 与 schema 都要求成功结果，并未承诺 bounded-failure JSON；本轮未将“无失败分支”误判为两者互相矛盾。

**建议修改（待确认）。**建议保留已限定的固定分子模型、CHCl3 边界及波长/f/电子性质目标，统一来源声明，不补成实验 dodecyl/聚集模型。若另要所有任务都有规范失败出口，可另行小范围批准，但不是现有成功计算不足，也不应伪造 NTO 或新数据。

**对现有验证结论的影响。**300实频、TD20、735.93nm/f=1.2539、HOMO→LUMO 展开支持当前任务；未计算的 NTO、全实验体系及聚集光谱不作为已验证事实。

<a id="paper_d7967e22bb965daa"></a>

### group_2 / paper_d7967e22bb965daa — 四个 quartet 插入 TS 的局部自由能势垒

模式：PR。**当前判断：仅 PR；四个作者 TS 答案直接公开，必须先确认候选定义与去除坐标的修法。**

**原文依据。**正文 PDF p10；SI PDF p92–97 的 M06L 路线/熵处理，INT2A p141–144、INT2B p149–151，四 TS p156–180。 [正文](../../papers/paper_d7967e22bb965daa/documents/main.pdf)、[SI](../../papers/paper_d7967e22bb965daa/documents/supplementary_001.pdf)。

**真实计算支持。**20条已归档成功阶段覆盖六物种优化/频率和单点、八条IRC。M06L气相Opt/Freq→THF单点，2/3熵修正；A/B以INT2A、C/D以INT2B为零点，10.258029/12.425524/13.190985/12.022525 kcal/mol均符合10.2/12.4/13.2/12.0±1。

计算归档：[PR reference](../final_verified_paper_reproduction/paper_d7967e22bb965daa/evaluation/verified_computation_reference.md)。已有证据：[provenance/final_closure_20260916/FINAL_AUDIT.md](../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/FINAL_AUDIT.md)；[provenance/final_closure_20260916/independent_report.json](../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/independent_report.json)；[provenance/final_closure_20260916/author_route_evaluation_audit.json](../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/author_route_evaluation_audit.json)；[provenance/chemical_mode_projection_20260914.json](../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/chemical_mode_projection_20260914.json)；[provenance/IRC_chemical_assignment_20260915/independent_IRC_assignment.json](../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/IRC_chemical_assignment_20260915/independent_IRC_assignment.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**`TS3A_quartet.xyz` 至 `TS3D_quartet.xyz` 的68/68坐标均对应 SI p156–180 的作者 TS；即使当前 task 称给定候选比较、文件称 starting，也已经给出了关键驻点答案。`INT2A/B` 为另两个作者定义的协调反应物，并非同一角色。现有局部零点 A/B 对 INT2A、C/D 对 INT2B 是明确且经验证的定义，应保留，不改成分离物总体高度。历史20个成功阶段有8条IRC，但每支40步到 MaxPoints，不是全部产物/反应物极小值都已收敛。

**建议修改（待确认）。**建议保留四个待比较迁移插入路线的化学定义、成/断键原子映射及 quartet边界，用非终态的反应物/独立生成初始模型让 agent 自行构建 TS；作者 TS移 `evaluation/author_results/`。四标签必须有不依赖答案坐标的清楚定义，不能只删文件留下 TS3A/B/C/D 空标签。INT2是否作为已给定反应物保留需你确认；局部势垒零点不变。不得为保留坐标把它偷偷降成给定TS的能量算术题；如需那种子基准，应另立范围。

**对现有验证结论的影响。**10.25803/12.42552/13.19099/12.02253 kcal/mol 和一虚频/化学位移证据支持既有四候选比较。不能据40点IRC宣称全部端点极小值或完整机制已证实；当前任务只要求位移证据，不以额外端点要求自动触发重算。

<a id="paper_5d94285cfbd51973"></a>

### group_4 / paper_5d94285cfbd51973 — AZ9 九构象电子描述符

模式：AR、PR。**当前判断：AR/PR 的 AZ9 身份、无泄露输入、构象/灵敏度链和描述符定义相容；未发现新的实质性缺口。**

**原文依据。**SI PDF p7 方法、p41 Table S12 的 AZ9 轨道/描述符。任务已有 conventional μ/ω 定义，不套用 SI 的非标准/有符号问题派生行。 [正文](../../papers/paper_5d94285cfbd51973/documents/main.pdf)、[SI](../../papers/paper_5d94285cfbd51973/documents/supplementary_001.pdf)。

**真实计算支持。**九条B3LYP/6-31G(d)构象极小值均153实频；12轮611候选池的TFD去重覆盖9盆地，最低basin04 E=−1719.93864109 Eh。HOMO−5.59139565、LUMO−1.16981749、gap4.42157815 eV、dipole6.0404 D均满足目标；九条更大基组单点形成敏感性链。

计算归档：[AR reference](../final_verified_autonomous_research/paper_5d94285cfbd51973/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_5d94285cfbd51973/evaluation/verified_computation_reference.md)。已有证据：[provenance/author_descriptor_closure_20260914.json](../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/author_descriptor_closure_20260914.json)；[provenance/evaluation_task_qualification.json](../../docs/verification/group_4/paper_5d94285cfbd51973/provenance/evaluation_task_qualification.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**公开 SMILES/名称/中性单重态，无作者3D或目标数值。现有 task 使用 conventional IP/EA/η/μ/χ/ω 定义，不照搬 SI 的异常有符号派生行；前轮报告已经说明，不能再当成未修泄露。真实12轮611候选池覆盖9盆地并有9个更大基组单点，与有限构象+敏感性需求匹配；不将有限池说成全局最小。主方法与敏感性分支的 HOMO/LUMO 改变量必须如实保留，不按更接近 gold 选分支。

**建议修改（待确认）。**建议保留正确身份、公开公式和现有成功证据；按已公开 conventional 定义核对派生算术。方法自由与固定数值比较如果要统一政策，需逐篇批准，不能把任何敏感性变化判为验证失败或改容差来隐藏。

**对现有验证结论的影响。**四主描述符和有界敏感性已有真实支持；无需新增计算，也不能据此宣称生物活性、靶点结合或实验氧化还原量已验证。

<a id="paper_b33676a2051f5e91"></a>

### group_4 / paper_b33676a2051f5e91 — Int-3 β-scission TS / IRC

模式：AR、PR。**当前判断：PR 指定断裂通道有真实支持；AR 的9.07数值适用条件需要明确绑定到正确通道。**

**原文依据。**正文 PDF p8 Int-3 β-scission势垒9.07及比较13.39；SI PDF p23作者方法、p33反应物坐标。 [正文](../../papers/paper_b33676a2051f5e91/documents/main.pdf)、[SI](../../papers/paper_b33676a2051f5e91/documents/supplementary_001.pdf)。

**真实计算支持。**BHandHLYP/aug-cc-pVDZ/SMD(MeCN)真实reactant 66实频，TS一虚频−474.9764 cm⁻¹，ΔG‡8.89745683 kcal/mol符合9.07±2。正向IRC64点回到Int-3；反向80点到MaxPoints，C12–C13=3.658492 Å、C12=O24=1.213425 Å，片段图acetophenone/ethyl，ethyl自旋和0.998047。证据足以支持指定断裂通道，不冒称无限远解离收敛。

计算归档：[AR reference](../final_verified_autonomous_research/paper_b33676a2051f5e91/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_b33676a2051f5e91/evaluation/verified_computation_reference.md)。已有证据：[provenance/author_channel_closure_20260915.json](../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/author_channel_closure_20260915.json)；[provenance/evaluation_task_qualification.json](../../docs/verification/group_4/paper_b33676a2051f5e91/provenance/evaluation_task_qualification.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**输入只给24原子 Int-3反应物，没有 TS、产物坐标或势垒；不构成待求TS泄露。真实三候选是同一乙基断裂通道的三个猜测，不是三条竞争机理，历史记录已明确；这不妨碍证明至少一个要求的成功通道可计算。AR `scoring_rules.json::ar_r4` 的 comparison 文字说仅对 acetophenone 通道使用9.07，但 `binding.applies_when` 仅判断status=validated_result；公开任务允许独立提出/选择其他合理通道，存在规则解读歧义。没有实测 LLM judge 对反例的评分，故这里只确认契约歧义，不声称运行时代码已必然误罚。

**建议修改（待确认）。**建议保留AR自主通道选择，把数值规则的适用范围显式写成已验证的 acetophenone+ethyl 通道，并核对 selected_channel、原子守恒、TS与参考反应物属于同一支。其他合理通道按证据型规则处理，不对所有通道套9.07；若你希望主成功必须得到论文通道，应先批准相应的目标/完成条件调整。PR保持明确作者假设与现有科学目标。不要把仅一个验证通道宣传为全通道最优。

**对现有验证结论的影响。**一虚频TS、8.89746 kcal/mol、双向IRC及断裂片段支持规定通道；反向80点到MaxPoints但片段/自旋证据存在，不伪称无限距离极小值。无须为本次条件澄清自动计算其他通道。

<a id="paper_46a9ca0dab36dd9e"></a>

### group_4 / paper_46a9ca0dab36dd9e — Cat1 六重态 TD / IFCT

模式：AR、PR。**当前判断：AR/PR 的目标激发态、溶剂和 IFCT 定义没有与单值评分充分对齐。**

**原文依据。**SI PDF p34–35 的态/IFCT资料，p37计算条件；正文的62.4% LMCT /4.3% MLCT来自特定所选态与分析口径。 [正文](../../papers/paper_46a9ca0dab36dd9e/documents/main.pdf)、[SI](../../papers/paper_46a9ca0dab36dd9e/documents/supplementary_001.pdf)。

**真实计算支持。**ground-state96实频、TD30；历史选择state22（非最大f，最亮为state20）。state22 Hirshfeld LMCT62.060/MLCT4.103%；Mulliken-like62.492/4.351%；state20/21对照也有真实输出。支持作者所选态的LMCT结论，不能证明任选态都应满足同一gold。

计算归档：[AR reference](../final_verified_autonomous_research/paper_46a9ca0dab36dd9e/evaluation/verified_computation_reference.md)、[PR reference](../final_verified_paper_reproduction/paper_46a9ca0dab36dd9e/evaluation/verified_computation_reference.md)。已有证据：[provenance/ifct_closure_20260915.json](../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/ifct_closure_20260915.json)；[provenance/evaluation_task_qualification.json](../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/evaluation_task_qualification.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**TEA+·FeCl4−中性sextet身份自包含且没有作者3D泄露。AR写 excluding solvent，PR只排除溶剂分子；真实验证用SMD(MeCN)，需明确隐式溶剂而非让agent猜。两模式允许自行选代表低激发态和 fragment partition，但按62.4% LMCT/4.3% MLCT比；这些值属于具体态/分区/分析口径，不是任意态的性质。历史选state22，而最大f为state20；state20/21的实际IFCT也存在，不能由“选了22才过”推出公开固定22。把整个FeCl4−当一个片段则根本无法以相同含义区分Cl→Fe/Fe→Cl。

**建议修改（待确认）。**建议按正文/SI明确隐式MeCN、Cl配体/Fe/TEA+分区、LMCT/MLCT方向与归一化；确定不使用参考百分比挑态的谱带/态选择规则，PR可给主比较分析协议，附其他态/分区作敏感性。AR若继续开放选择，评分必须按可比态身份/分区有条件比较，而非任意态套同一gold。先用现有TD30、state20/21/22与波函数核查这些规则能否选出同类物理态；若原文未唯一说明，报告待决，不凭数字最接近者定规则。

**对现有验证结论的影响。**state22的Hirshfeld62.060/4.103%、Mulliken-like62.492/4.351%确有真实输出，支持相应态的作者结论。需补任务比较定义，不是“没有算过IFCT”，也不自动补算。

<a id="paper_44f9727c4e9a4b6f"></a>

### group_6 / paper_44f9727c4e9a4b6f — 1H Fe 几何、自旋与 Mössbauer

模式：PR。**当前判断：仅PR；公开作者1H终态直接暴露Fe–Fe距离，其他计算及必要Mössbauer校准均有支持。**

**原文依据。**SI S5–S6的TPSSh/ZORA/校准说明，S32–S33 Table S10的1H优化坐标；Fe–Fe几何和Mössbauer是当前必评。 [正文](../../papers/paper_44f9727c4e9a4b6f/documents/main.pdf)、[SI](../../papers/paper_44f9727c4e9a4b6f/documents/supplementary_001.pdf)。

**真实计算支持。**正确broken-symmetry极小值零虚频；Fe–Fe3.086431831 Å，E(BS)−E(HS)=−0.026282803515 Eh；SARC/J/DefGrid3的Fe密度经δ=A(ρ0−C)+B得到0.517809/0.523604 mm/s，符合0.52±0.07。

计算归档：[PR reference](../final_verified_paper_reproduction/paper_44f9727c4e9a4b6f/evaluation/verified_computation_reference.md)。已有证据：[provenance/FE_ROUTE_AND_CLOSURE_20260915.md](../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/FE_ROUTE_AND_CLOSURE_20260915.md)；[provenance/corrected_mossbauer_evidence_20260915.json](../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/corrected_mossbauer_evidence_20260915.json)；[provenance/evaluator_crosscheck_20260915.json](../../docs/verification/group_6/paper_44f9727c4e9a4b6f/provenance/evaluator_crosscheck_20260915.json)。这里的审查 JSON 只是输出索引，科学判断还核对相应真实结构/输出，不把旧“通过”标签直接当作本轮结论。

**具体问题与模式差异。**`1H_start.xyz` 的87/87坐标来自SI TableS10，待求Fe1···Fe2≈3.086Å直接包含在输入；task guidance还声称未提供优化后的结构，与文件来源不符。`mossbauer_protocol.json`中的A/B/C、SARC/J、DefGrid3等则是密度→位移所需的计算定义，不是目标Fe密度/位移，不应为“防泄露”一并删掉。ORCA输出261个频率槽不等于261个内部振动模式；有效事实是相应结构零虚频、真实最小值测试及版本适配。

**建议修改（待确认）。**批准后由明确susan配体、桥氧/过氧连接图、+2和自旋边界独立构建完整初始几何；保留Fe1/Fe2及桥氧映射，不照抄/微扰作者终态。作者结构放 `evaluation/author_results/`，同步去除题面错误无终态声明。保留与相应方法匹配的Mössbauer校准和高自旋/BS比较定义，不能改gold来回避模型依赖。

**对现有验证结论的影响。**零虚频、Fe–Fe3.086431831Å、BS−HS=−0.026282803515Eh和0.517809/0.523604mm/s支持当前作者路线结论。问题是公开答案，不是谱学结果未算出；本轮未做任何新电子结构求解。

## 4. 需要你明确验收的“给定结构”边界

以下五篇共 10 个任务与第 2 节的四篇几何/TS答案任务不同：当前题面原本把结构作为给定对象，待算的是能量/振动/光谱，并非声称独立发现那个几何。但该范围此前由我直接判定并移 final，不符合你的确认流程；本次全部留在 verified_tasks，等待你验收。

| 论文（均 AR/PR） | 公开了什么作者结构 | 当前待求量 | 建议及不能声称的能力 |
|---|---|---|---|
| `paper_d2d08c91f34da1cb` | S0/S1 两个优化结构 | 两态频率、振动对应/解释 | 可考虑保留为给定两态振动题；不能声称独立发现两态几何 |
| `paper_e31cc7bc7b21b610` | cis-α/cis-β 优化结构 | 电子能差/最小值验证 | 可考虑保留为指定异构体比较；不能声称异构体发现 |
| `paper_d8e5490cd9942f4f` | syn/anti 两个优化端点 | 水介质自由能差 | 可考虑保留为两个指定端点比较；不是全构象/溶液平衡题 |
| `paper_c23cfabbd34b087f` | 1M-TIPS 优化模型 | 垂直吸收与跃迁性质 | 可考虑保留为固定模型性质题；不评价几何生成 |
| `paper_80cc1ffb2cf73fc5` | anion 优化初态，没有 neutral终态 | neutral、FC响应/模式 | 可考虑保留为给定初态问题；仍须单独解决实验比较/评分问题 |

建议你批准的是**具体科学范围**，不是“所有 SI 坐标一律安全”。若你希望这五篇也评从独立初始几何构建，则另批准对应 starter 改法；不能只改文字掩盖原输入来源。反应物 3a 和 Int-3 则是反应问题的已知对象，与公开待求 TS 不同，当前未发现这两份反应物本身泄露 TS 答案。

## 5. 按最小影响顺序执行的修法建议（尚未实施）

### 5.1 先修不应再带入评估的结构/输入问题

1. **a396：先对象，后评分。**按正文/SI核对正确连接图和标签映射；明确实验比较由谁负责。建议公开纯实验列、隐藏计算结果，避免要求 agent 计算未知观测的 MAE。随后查 group 是否存在正确对象的旧输出；当前错误对象不能重标或复制为正确 reference。
2. **746、ef、d796、44f：去掉答案结构，保留身份。**批准后生成独立初始模型，完整化学图、charge/spin、原子映射、必要校准/参考反应物不丢失；原终态仅存 evaluation/author_results。对 d796 先把四候选的化学定义写清，再去坐标；不能删到任务只剩无法理解的标签。
3. **Z1：补必要观测或明确比较职责。**优先从原文提取不含计算指认的实验峰/trace；若资料不足，先请你决定限定实验结论范围，不私自降级必评项。

### 5.2 再使指令允许的工作与评分范围一致

1. **6f PR、46a9 两模式：**明确方法相关测量/态/片段边界。PR 可以公开不含数值答案的作者主比较协议；AR 的必要测量定义不能顺带泄露作者结论。不能要求任意选择都命中同一个隐藏答案。
2. **e31：**数值容差与正号/能序联合判定，不改变目标/容差。
3. **b336 AR：**显式限定9.07规则的通道；保留自主探索与规定通道结果的区别。
4. **Rh101 PR、6f AR、compound2 两模式：**把已有计算支持的有限趋势、有限构象与解释范围写准；不把有限验证升级成普适结论。compound2现有“consistent with”已经有限定，可仅验收范围，不必硬改目标。
5. **746、5ea、a396 两模式的失败分支：**未获得 Hessian/误差指标时允许明确的 null/未算状态和诊断；成功分支仍要求真实完整结果。不得以0虚频、0误差占位。
6. **其余 M3、AZ9、吸收/能量子问题：**保留已有正确科学定义；对自由方法与来源模型数值的公平比较作明确约定，不因为某个敏感性分支变动就判科学任务不可行，也不批量改gold。

### 5.3 修复后的确认仍分两步

- 你先确认上述**逐篇修法和科学边界**；有争议的只暂停该篇/该项，其他获准修改仍在 verified_tasks 完成。
- 修完后复查指令—公开输入—schema—关键点/结论—真实计算支持，汇报实际改动及剩余问题。
- **再由你确认调整完成以及逐篇/逐模式移入 final 或 hold 的清单。**此前全部保留 verified_tasks，不以问题类型、检查通过或“继续”替代迁移授权。

### 5.4 哪些不需要补算，哪个仍不能凭旧结果认证

- 坐标私有化、独立starter构建、测量定义、评分条件、schema失败分支、来源/范围说明，优先用已有资料解决；本次不下发重算。
- 实验峰表、原子标签/指标重提取、既有 TD/FC/轨道/IRC 输出分析属于现有证据整理；不能伪装为新计算完成。
- **a396 的正确分子验证证据目前没有在已检查的主链中找到。**这是要交对应 group 先查清的明确缺口；只有确认没有正确对象的存量结果，才由你决定是否补最小验证。这里不再把其他论文仅因“没有从公开起点自主探索”归入需重算。

## 6. 技术检查及其限度

- 目录退回后逐包校验：34 个包；JSON/schema、37个 XYZ、18个 SMILES记录和2份 CIF副本检查；相对链接、evaluation目录布局及软链接检查。最终运行结果见本节末。
- 前轮31份真实结果直接匹配当前 schema；AR 6f/e31/b336 的3份仅在私有维护资料中作无损字段映射，本轮任务科学内容未再变化，复核仍成立。它只证明格式可对应，不证明盲测过程发生过。
- 前轮61项现行数值比较均在容差内。此次复审说明为什么不能把这一数字当放行标准：a396无硬数值规则却有错分子；泄露坐标可能让数值更容易过；符号、物理态、条件与较强结论另需审查。
- 新增只读的软件反例检查（不是量化计算）：746失败且未算Hessian时虚频数null被拒；5ea失败候选的未知虚频数null被拒；a396失败且无可比较量时空metrics被拒。两模式都有相应契约问题；未把软件样例写入reference或真实结果。
- 保留前轮已做的软件证据：任务包测试10 passed，34包 materialize_agent_files仅复制agent_input。**没有新增模型盲测、完整LLM evaluator重跑或真实共享环境的隔离测试。**对b336等只确认文字/条件歧义，不编造实际错误评分结果。

最终实际检查结果：**34/34 包校验通过，37/37 XYZ、18/18 SMILES记录、2/2 CIF可解析；本批包内及本报告的相对文件链接无断链，evaluation布局无额外杂项，包内无软链接。**与迁移前 `22d440f8` 的对应内容逐文件比较，排除本轮获准变更的 manifest/reference链接与状态/维护审查记录后，**380个任务科学文件完全未变，无缺失**；原 final/hold 的本批34个旧位置均已不存在，退回数量与第1节一致。6个任务的失败分支软件反例均确认上述限制，留待批准后修复。包校验通过不能抵消这些科学/契约问题。

发布前仍需确保运行环境无法读取 `evaluation/`、`task_provenance/`、本报告、论文、group日志和其他任务答案；“只复制agent_input”不自动保证共享挂载、父目录和网络不可访问。此处记录风险，本轮未修改运行器、挂载或网络策略。

本报告的结论是**逐篇问题和修法待确认**，不是“34个都已发布就绪”。第一批 final/hold 没有在本轮重新逐篇认证，不把本批检查结论外推到整个旧benchmark。

## 7. 逐篇详细修复方案（2026-09-16，待负责人批准，未实施）

本节回应“对发现的问题分别给出详细解决方案，确认后再修改”。第 3 节保留问题和证据，第 7–9 节集中给出实施步骤、验收办法和需要负责人决定的边界，不再另建一批方案文件。本文中的“拟修改”“建议保留”都不是已获批准或已完成。

### 7.1 本轮范围与不可越过的边界

- 本轮只补充本报告；不改任何任务包的 task、输入、schema、evaluator、reference、manifest 或目录位置，不写入 docs/verification，不提交计算任务。
- 当前任务内容的 Git 基线为 `7aecf414`。未来获准实施时先核对本批是否被其他人修改，只保存/修改获准的包，不纳入仓库其他未提交工作。
- 科学证据优先顺序仍是：**正文/SI 的对象、研究问题和量的定义 → 真实计算对该对象/量的支持 → 当前任务包的一致表达**。不按“哪组数最接近旧结果”倒推目标，不因历史脚本方便而重定义研究对象。
- 历史验证可以使用作者结构、TS、方法和已知路线；不要求它重演未知答案 agent 的独立搜索。更换公开 starter 本身不自动触发重算。
- 作者结果进入 `evaluation/author_results/` 后只是私有材料，**不会自动新增坐标 RMSD、结构匹配等评分**。如要用这些结构打分，另行批准指标、原子映射、对称性/手性处理和容差。
- reference 只如实记录成功计算链及其适用范围；不改成 agent 必须遵循的步骤，也不替代五个 evaluator JSON。错对象计算不能在修正输入后直接改名成为正确对象的成功链。
- 两次确认继续分开：**先批准修复内容；修后再次批准结果及逐篇/逐模式 final 或 hold 去向**。本方案获准也不授权迁移。

### 7.2 获准后的共同实施与检查方式

1. **先固定本篇科学合同。**逐项列清研究对象、总电荷/自旋、环境、待求量、关键定性结论、原有数值/容差和成功证据要求，区分哪些是本次批准改变的定义、哪些必须保持。
2. **再修改最小文件集合。**公开科学说明主要在 `agent_input/task.md` 和必要输入中；交付在 `agent_input/submission_schema.json`；五个 evaluator 文件只改受影响的关键点、结论、规则及证据引用。相应 task_info、私有 paper_route 中若有冲突也同步修正，但不把整份私有路线公开。未受影响的 gold、容差、评分项不顺手改动。
3. **检查输入自包含及模式差异。**AR 不公开作者答案/结论或把作者全路线作为隐含必读；PR 可公开经批准的假设和方法路线，但同样不公开优化终态、目标数值、排序和已经判定的赢家。输入数据、注释、schema 示例和文件名一起查。
4. **重用真实输出做对照。**允许解析已有结构、频率、TD/FC、IFCT 和几何表；必要时补齐来源/单位/映射。这是存量证据整理，不是新增量化计算，更不能写成新的从公开 starter 成功复现。
5. **软件验收覆盖正反例。**成功记录仍须有实际科学证据；失败记录可如实表达 unknown；错误身份、符号、物理态、通道或无数据时的零误差不得被当成成功。软件样例与真实计算分开，不写进成功 reference。
6. **最后交负责人复核。**列出实际改动、旧验证仍支持的结论、不能证明的范围、尚需决定的问题和候选去向。只有在负责人另行批准后才迁移。

**关于评分实现的特别说明。**已读 [adapter](../../evaluation/scoring/adapters.py)、[judge prompt](../../evaluation/scoring/prompts.py) 及 [prompt 选择逻辑](../../evaluation/scoring/service.py)。本批五文件适配器输出 dual-axis 合同；结论轴与过程轴分开，最终分数为二者乘积除以 100。规则及适用条件被交给 judge，不是任意新添一个 `applies_when` 就有了确定性的条件执行器。因此：

- 下文“加通道条件”“联合核对能序”首先指在现有受支持的合同字段和明确文字中消除歧义，并检查实际渲染给 judge 的内容；不能承诺一个新 JSON 谓词已经改变运行时代码行为。
- 成功、诚实失败、支持相反结论是不同状态。允许报告反例，不等于自动获得“已复现论文结论”的分数；也不应把诚实反例本身当成伪造。
- 若需要修改通用 scorer、重新分配权重或新增确定性门控，另列最小代码方案请负责人批准。本轮不动通用评分策略，也没有执行新的 LLM 评分试验。

**独立 starter 的统一处理。**先核对完整连接图、原子角色、立体化学、配位/桥联、质子化、电荷和自旋，再从图独立嵌入；金属体系可用通用配位几何模板。不能用作者终态坐标、小扰动、终态距离约束、作者目标角度或能序来生成/挑选 starter。先做图/式/原子数/映射/近接检查，能可靠应用时才用明确记录的非量化预处理；配位力场不适用时不得强行宣称预优化成功。几何构建不等于新的 DFT 验证，不以“保证收敛”描述结果。生成信息记入已有 task_provenance 维护记录，公开侧只留下必要的身份/映射/起点使用说明。

**失败分支的统一处理。**746、5ea、a396 的问题按候选和整体状态分别修复：没有求过 Hessian/没有可比较观测时才允许 null 或明确未计算；已有实测虚频/误差即使失败也保留，不抹掉。成功选中候选仍必须有对应验证值和证据；不能用 0 虚频、0 MAE 占位。允许诚实失败提交只是修正数据契约，不降低科学成功标准。

以下各篇文件路径均相对 `tasks/verified_tasks/<mode>/<paper_id>/`，AR/PR 表示分别核对两包，不用一次全文替换强行变成同一模式。

### 7.3 P01 — group_1 / paper_d2d08c91f34da1cb（AR、PR）

**需解决什么。**两态作者优化坐标的公开角色未获验收；PR 的片段红/蓝移概括可能误罚混合、模式交换和真实反例。不是频率没算成功。

**拟实施步骤。**

1. 先请负责人确认：本篇是否接受“给定 S0/S1 两态对象，计算振动并进行位移匹配”的范围。接受后保留 `rhodamine101_S0.xyz`、`rhodamine101_S1.xyz`，统一 task、XYZ 注释、task_info 的真实来源，不称它们是独立初始构建，也不评价两态结构发现能力。若不接受，单独设计从正确图生成两态 starter 的方案，不直接删坐标。
2. task 明确先按原子映射和位移/局部坐标对应振动，再比较频移；同一整数编号不自动代表同一物理模式。不能把正常的模式换序记成物理结论错误。
3. 重点修改 PR `reference_key_points.json::pr_result_state_shifts` 及其关联规则/结论：论文的红/蓝移是带适用范围的趋势，允许混合模式、方向反例和近零变化。私有证据保留已知 1/2 换序、正移例外和模式 8 约 +0.005802 cm⁻¹，不要求 agent 猜这些私有编号。
4. `experimental_slt_peaks.csv` 只保留实验观测；缺失峰留空并明确配对数量。不得用作者计算频率补成“实验值”，不得把未配对峰计成零误差。

**保持不变。**两态频率与模式解释目标、实验单位、现有定量范围；不新增超快动力学或“每个模式必须同向”的评分。

**验收与已有支持。**复核两态各 195 实频、24 个有效配对的 MAE 1.262626 cm⁻¹；测试“编号交换但位移正确”“混合/近零模式”不会按普遍红移规则误判。最大误差 3.097158 cm⁻¹ 不能被改写成小于 3。无需新频率计算。

**待确认边界。**保留作者两态几何为公开固定对象；若要求几何独立发现，则本项改法必须另批。

### 7.4 P02 — group_1 / paper_6f9a36fff6964313（AR、PR）

**需解决什么。**PR 允许任意方法作为主结果，却用固定 Mulliken 电荷 ±0.02 e 比较；AR 的有限构象覆盖被写成需要证明广泛覆盖无影响，强于已有证据。

**拟实施步骤。**

1. 保留 `systems.json` 的完整三体系、OTf、原子环境、MeCN、电荷和自旋；不删除阴离子，不提供作者坐标或四个电荷。
2. PR 建议将无答案的 SI 两层级路线写为主比较协议：B3LYP-D3BJ/6-31G(d,p)/IEFPCM(MeCN) 优化/频率，再对对应几何做 M062X-D3/def2TZVP/SMD(MeCN) Mulliken 单点。软件可替代，但需同一理论定义、完整系统和可核查原子映射。删除与此直接矛盾的“任意主方法都和同一 gold 等价”的含义。
3. 构象按预先声明的能量/覆盖标准选择，不能按电荷最接近私有值选择。额外方法/构象保留为敏感性结果，主值与敏感性值分开标识；±0.02 e 不自行放宽。
4. AR 保留自主设计方法和当前证据型差值/趋势目标，不塞入 PR 协议或四个答案。将“只用一个起点须证明更广覆盖 immaterial”改为“报告为何使用这一覆盖、已做的检验及未解决的不确定性”；停止条件是已声明预算/覆盖下的证据状态，不要求证明数学意义上的构象不变性。
5. **不默默删除敏感性要求。**建议实际做过的敏感性照常评分；未完成则明确标为证据不足/限制，不能因披露限制就自动获得稳健性分数。若负责人希望主成功只要求单构象四电荷，应单独批准缩小成功范围。

**涉及文件。**两模式 task/schema 中主结果、构象/敏感性及停止说明；PR 相关 numeric 规则的协议适用文字；AR 覆盖关键点和关联结论；冲突的 task_info/paper_route。

**验收与已有支持。**真实四电荷 0.203728、0.198533、0.040059、0.058695 e 可继续证明作者路线的量可算得；最后一项接近上界的事实保留。检查 SP 确实依赖对应优化几何；单构象结果不能被报告为多构象稳健。无需重算来完成这些定义修复。

**待确认边界。**PR 限定主比较协议；AR 将过强的覆盖证明改为实际覆盖和不确定性陈述，但不自动免除原有敏感性得分要求。

### 7.5 P03 — group_1 / paper_746e066c163800d8（AR、PR）

**需解决什么。**`compound5.xyz` 公开 72 原子的作者优化终态，直接带出目标扭转；signed/absolute 任取与正 27.1° gold 不一致；失败且未做 Hessian 无法如实提交。

**拟实施步骤。**

1. 从正文/SI 核定 compound 5 的图、立体化学和五组 inner-rim 原子四元组；建立图原子、公开 starter 与提交坐标之间的映射，不靠优化终态中的角度定义身份。
2. 按 7.2 独立生成同身份 starter，替换两模式的 `compound5.xyz`；作者终态仅放 `evaluation/author_results/`。不能随机抖动终态，不用实验 27.0° 或计算 27.1° 作为构建约束。两模式共享公平的基础输入，不在 AR 中透露 PR 的路线结论。
3. 建议公开并统一测量定义为五个扭转的 `mean(abs(phi_i))`，同时保留每个带符号角及四元组。先从旧成功几何重新提取五角，确认这一定义仍对应现有 27.1±2°；若原金标实际上用了别的聚合，先汇报，不能静默换定义或改 gold。
4. `experimental_torsion_boundary.json` 的实验观测可作为比较背景保留，但须标明实验/计算区别；本题因此包含已知实验约束信息，不宣传“完全未知实验结构的盲预测”。如负责人不希望提供该实验量，需同时调整相应公开比较职责，而非只删数值。
5. schema 的 `validation.imaginary_modes` 对未计算失败分支允许 null 并强制诊断；成功分支仍要求真实 Hessian/最小值证据。关联关键点/规则使用同一个角度约定。

**验收与已有支持。**图、72 原子和手性核对通过；生成没有使用终态模板/目标扭转；镜像/原子次序带来的纯符号变化按批准的绝对值定义处理，而化学身份/错误四元组不能豁免。210 实频和约 27.09677° 的历史成功链保留，注明不是从新 starter 验证。

**待确认边界。**独立 starter 替换、绝对值平均作为主评分量、保留实验比较背景。不能未经批准把对映体身份也一并放宽。

### 7.6 P04 — group_1 / paper_5ea491c741fbd8d4（AR、PR）

**需解决什么。**失败候选的未知虚频数不能填 null；PR 不让识别论文方法但又按方法相关轨道数值评分。当前正确 E 身份及五起点/三极小值证据保留。

**拟实施步骤。**

1. 修 `submission_schema.json` 中候选级 `stationary_point_test.imaginary_frequency_count`：按候选是否实际做过 Hessian 区分整数与 null，不只看顶层 complete/bounded_failure；失败候选保留日志、未完成阶段及诊断。成功选中候选仍须有相应站点证据。
2. PR 建议主比较采用气相 B3LYP/6-311+G(d,p)，其他方法单列敏感性；不公布 HOMO/LUMO/gap，不将验证中 seed 303 作为必选起点。保留 E 身份和按能量/有效极小值选择代表构象的逻辑，不能挑最贴近金标的构象。
3. 方法依据以正文 p3 §2.4 的实际优化描述和 p4 §3.4 为主。p3 后文确有一句泛泛的 B3LYP/6-31+G(d,p) 表述，须私有记录为来源内部不一致；选择 6-311+G(d,p) 的理由是两处直接描述本研究的计算，而不是本地结果更合适。若负责人不接受这一取舍，先暂停方法限定。
4. AR 不自动加入作者方法，也不把现有定量规则降为 optional。建议明确“路线自由不等于改变轨道定义或自动豁免定量准确性”，如实提交方法/构象依赖；是否进一步限定公共读出协议或改变定量计分，属于另需确认的政策选择，不能混入 schema 修复。
5. 同步 task、相关 process key points、主/敏感性字段与 numeric 规则适用说明；HOMO/LUMO/gap 的原 gold 和容差不变。

**验收与已有支持。**检查“一个候选失败未求 Hessian、另一个成功”可如实提交；成功但虚频信息全空不能通过成功证据检查。对现有成功分支重核 gap=LUMO−HOMO；−6.56393059/−2.88386271/3.68006788 eV 的真实结果仍有据。该修法不要求新增轨道计算。

**待确认边界。**PR 主方法和原文冲突取舍；AR 保留现有自主路线及准确性目标，不宣称所有合理方法都必然命中同一容差。

### 7.7 P05 — group_1 / paper_a0f6b899582cb9f7（AR、PR）

**当前不是新的缺口。**M3 独立 starter、完整 24 原子身份、raw Cartesian charge second moment 的定义已修。需要验收已有修复，而不是再次改科学目标。

**拟处理。**逐一核对 task/schema/evaluator 均使用核+电子原始二阶矩、声明原点、Debye Å、拟合分子面法向及完整张量旋转。SI Table S1 的非零迹不支持 traceless 解释，表头 Debye 的不完整单位说明保留在私有记录。若现有文件已一致，不做无意义改写。

**保持与验收。**不缩放 −108.35、不换容差、不把实验室 z 轴当 stacking 法向；检查单位转换和张量旋转重提取即可。已有 66 实频、Qzz=−111.07681064 DÅ、零偶极/平面性/N···S 证据有效。不能扩展为凝聚态堆积能或器件性能验证。

**待确认边界。**验收现有原始二阶矩解释。若要改成 traceless 张量，需要另立目标/金标方案，不能作为文字修复。

### 7.8 P06 — group_1 / paper_ef26687d63a37e29（AR、PR）

**需解决什么。**正确完整的 46/56/61 原子模型已有验证，但公开 free/PO 全部、PA 部分作者终态仍泄露几何信息；补原子不等于去泄露。

**拟实施步骤。**

1. 先核定三个完整图，保留前轮补齐的 P/O 和 PA 芳环；为 P、N–ethyl 的 α/β-H、PO/PA 各氧与接触选择器建立明确映射。不能只按元素数重建另一种连接体。
2. 从完整图分别独立生成 free、PO、PA；替换 `Et2N3P.xyz`、`Et2N3P_PO.xyz`、`Et2N3P_PA.xyz`，不用 SI 坐标拼接或约束原接触距离，旧结果放 author_results。
3. 输入应足以自包含说明 PO 的 ring-opened 化学身份及 PA 完整片段，而不是让 agent 从不合理距离猜连接性。现有证据未确认新的 PO 图错误，不借机改变成键/非共价解释。
4. 同步 task/schema/关键点中的 atom selectors、公开身份和来源说明，维持现有 O···P/H 接触、ADCH 和 signed ESP 定义，不把 ESP 与电子密度混为一谈。
5. 私有 reference 只明确历史用的是作者路线完整模型，保留真实数值，不声称新 starter 曾经 Opt/Freq 成功。

**验收与已有支持。**完整图、46/56/61 原子、角色和电荷/自旋一致；公开侧没有终态片段、目标接触约束或作者排序；旧 P-ADCH −0.018993/0.447060/0.455684 e 及接触/MEP 证据仍有效。公开 PO 的 P–O 约 2.8 Å 不等于所有目标距离已给出，问题陈述不夸大。

**待确认边界。**批准三个独立起点替换，科学目标和完整分子模型保持。若图中桥联/质子化不能从原文唯一确定，先报告该具体键/原子，不凭经验改化学身份。

### 7.9 P07 — group_1 / paper_e31cc7bc7b21b610（AR、PR）

**需解决什么。**给定 cis-α/β 作者几何范围待验收；1.44±1.5 kcal/mol 允许小负值，单独数值达标不代表论文能序正确。

**拟实施步骤。**

1. 若批准给定异构体能量比较，保留两份 58 原子输入，明确来源和固定对象，不新增异构体全局搜索。公开只给 `ΔE=Eβ−Eα` 的定义、单位、电子能/自由能区别，不告诉 agent 哪个更低。
2. 在私有能差关键点、数值规则与最终结论中明确联合核对：原容差内、ΔE 正号、提交的 lower-energy identity 与其原始能量一致。各项分数仍按既有规则分别解释，不私自更改权重。
3. task/schema 若已经能表达两个能量、差值和身份则保留字段；只有存在实际缺字段才最小补充。不额外引入原本未承诺的失败分支。

**验收与已有支持。**历史 168+168 实频、Eα/Eβ 与 ΔE=1.43847762 kcal/mol 继续有效。软件反例 −0.02 kcal/mol 虽在区间内，也不能被认为已恢复 α 较低的结论；+1.44 却在文字写 β 较低也不应通过一致性检查。无须重算或缩窄容差。

**待确认边界。**保留两给定几何；批准将已有定性排序与数值条件写成一致合同，而非公开能序答案。

### 7.10 P08 — group_1 / paper_80cc1ffb2cf73fc5（AR、PR）

**需解决什么。**实验比较只有窗口没有可比观测；PR“可质疑模式指认”与“最终必须支持”没有区分提交合法性和科学结论得分；anion 几何范围待验收。

**拟实施步骤。**

1. 保留 Z1 单体系 FC 问题，建议接受作者 anion 为给定初态；neutral 几何、频率/位移、FC 强度和答案均不公开。若不接受初态范围，再独立生成对应身份 starter，不加入 Z2/E 异构体作为未经批准的新任务。
2. 从正文/SI补充**纯实验**观测：优先原始峰表/数据，其次可清楚分离的实验曲线。拟放 `agent_input/data/inputs/experimental_spectrum.csv` 及最小单位/来源说明；不能附带作者理论曲线、计算峰、mode-3 标签或“已经解释哪些峰”的结论。只有图片时说明数字化分辨率/读数限制，不能称原始 trace，不能编造实验误差条。
3. 建议当前 Z1-only 子问题采用正文 Fig.3a 的比较定义：以实验最低观测峰作为相对零点，对齐计算的 0–0 原点，再比较峰间距/突出特征。正文明确的 19444 cm⁻¹ 是实验观测，可作为零点；**512 cm⁻¹ 是作者计算后得到的平移量，不作为输入常数**。不把 Fig.3b 的双异构体拟合、19748 cm⁻¹ 归属和两个平移量混进此任务。
4. 在 `problem_definition.json`、task/schema 明确实验单位、观测通道、对齐后比较与绝对能量预测的区别；不能把拟合平移后的吻合算成绝对脱附能被准确预测。数据覆盖不足的区域不得填 0 MAE。
5. 重点对齐 `pr_r_mode`、`pr_c_final`、`pr_r_final`。建议允许提交有证据的异议，按物理位移识别对应面内模式，不硬要求软件编号=3；但保留作者 FC 解释作为当前复现结论。诚实反例可有过程分，不能仅凭“允许反驳”就判该结论已复现。AR 也保持其现有证据型范围，不能把没做实验比较写成已完成 spectral agreement。
6. 优先用现有 FC 谱和实验观测做对齐/后处理核查。若可可靠提取的观测不足以支持原必评项，或对齐后实际不支持原结论，返回负责人决定；**不自行删除实验吻合评分、不放宽阈值、不借机新增电子结构计算**。

**验收与已有支持。**已有 anion/neutral 各 75 实频、真实 FC 段、85.9573 cm⁻¹/HR=1.20932 支持内部 FC 结论；这不是现成的实验逐峰验证。新观测逐条能回到原文，峰匹配规则预先定义，不只挑对得上的峰；未分配峰和 Z1-only 限制保留。

**待确认边界。**给定 anion；公开纯实验观测；Fig.3a 相对谱比较而非双异构体拟合；“可报告异议”与“复现结论成功”分开。若数据不能闭合原目标，先再次询问。

### 7.11 P09 — group_2 / paper_a3892396b1843698（AR、PR）

**当前未发现新的实质性缺口。**公开 3a 是已知反应物，不是待求 TS；[3,3]/[5,5] 两条 TS/IRC/端点和势垒均有有效证据。

**拟处理。**保留 `3a.xyz`、两个命名比较通道、单位/温度及现有 entropy-only Grimme qRRHO 边界。仅核查来源说明、同一原子映射和无私有 TS/产品信息进入公开侧；不公开谁势垒较低，不为了说明来源把私有文件设为 agent 必读。

**验收与已有支持。**两个 TS 各一虚频、双向 IRC 和四个端点极小值；23.50589160/26.22790785 kcal/mol 与现有目标一致。核对热校正与电子能来自正确物种/层级，不把 qRRHO 换成另一套校正。这里不需要新增计算或额外“公开起点盲跑”证据。

**待确认边界。**建议保留当前研究对象和成功标准；若目标改为发现全部未知通道，属于另一项任务，非本方案内容。

### 7.12 P10 — group_2 / paper_46f6118697c6397c（AR、PR）

**需处理的是来源冲突和解释范围，不是换金标。**当前 SI 来源的 3.8436 eV、322.58 nm、f=0.4243 自洽；正文 4.33 eV/323 nm 不自洽。现有完整 CIF 和三分支计算保留。

**拟实施步骤。**

1. 在私有 evidence_map/来源说明保留正文冲突的具体位置和现行 SI Table S3 依据，不把正文写成和 SI 一致，不按本地计算选值。原目标/容差不变，agent 侧不公布这些目标数。
2. 核对 CIF 的对称/无序分支提取说明能够得到同一 68 原子、四 triflate 模型；分支选择按结构有效性和预先声明标准，不能按哪个 E/f 接近 gold 选择。已有输入自包含时不重建新的模型。
3. 若需要澄清 task/evaluator，限定为 compound 2 的跃迁、轨道性质与吸电子解释相容，不要求未计算的 compound 1/3/4 取代基因果对照。现有“consistent with”已经恰当的条目保持不变。
4. 态和轨道按物理性质、占据情况、贡献及振子强度关联；不将“第 5 态”“217→222”硬编码成任何方法下的答案。

**验收与已有支持。**三分支各 198 实频、TD50，三组 E/f 均在原容差内。重核 SI 的 eV/nm 换算及跃迁身份即可；不追加其他取代物计算，不把局部解释升级为唯一因果结论。

**待确认边界。**继续采用源任务本来的 SI 金标，并保留局部解释范围。若要覆盖其他取代基，需另批目标和证据要求。

### 7.13 P11 — group_2 / paper_a3968806251093cd（AR、PR）

**这是本批必须优先解决的对象错误。**当前成功日志属于错误位置异构体；与“验证用了作者信息”无关。另有实验列缺失、标签映射不完整、PR 方法对不明确、失败 schema 和整体比较定义问题。

**拟实施步骤。**

1. **先核对并修正身份。**按正文 Fig.3、名称和 SI 标签共同确定 pyrazole 环 N1–N2–C9–C8–C7：N1 接 phenyl，C7 接 O1-chlorophenyl，C8 接 imine，C9 接 methyl；核对 thione、E/Z 或其他立体约定。手工复核正确 mapped SMILES/连接表，再改 `molecule.json`；不在未检查前猜一条新 SMILES，不用分子式相同代替图同构。
2. **补可执行原子映射。**将 `atom_map.json` 扩成 source label→图原子→提交原子映射的明确合同，逐条核对 13 键、23 角、11 扭转。Cl1/Cl2 在单氯体系中的来源别名必须有原文依据；证据不足时先停该行并报告，不能擅自当成两个氯或静默丢行。
3. **建议给 agent 纯 SCXRD 比较数据。**增加只含上述 47 行实验量、单位、来源和原文给出的不确定度的输入表；不包含 B3LYP/CAM 计算列、差值、模型排名或“哪个更好”。仅公开实验选择量，不直接给作者 DFT 终态。这样 task 要求 agent 计算 MAE/RMSE 才有数据依赖基础。
4. **明确误差和模型比较。**长度、角、扭转分别统计；扭转采用最小圆周差。重复 C6–N1–C7 只计一次，不混用历史 48 行和当前 47 行。不得直接把 Å 和度相加构造一个未声明的“总体误差”。若来源不足以确定整体优劣的合成规则，先给分项指标并请负责人确定整体判据；不能选一个恰好让 CAM 赢的权重。
5. **分别处理模式。**PR 若保留“CAM-B3LYP 相对 B3LYP”的论文结论，公开两者同为气相/6-311+G(d,p) 的主路线，隐藏赢家；其他方法仅补充。进一步核查确认：**当前 AR 五文件并没有强制 CAM 获胜**，其目标是自选模型的有效比较；保留这个区别，不把 PR 胜负条件复制到 AR。所有模式均不能只因结果叙述合理就忽略错误分子。
6. **修失败数据契约。**失败模型/无数据的 metrics 允许空或 null，并有具体失败原因、已完成行和证据；只有成功模型要求相应数值和完整比较。未提供/未提取的实验量不得生成 0 MAE。对有缺行但称完成的情况，明确其是有限比较而非全 47 行成功，按批准合同处理。
7. **再查正确对象的既有证据。**先遍查 group_2 的成功输出、结构和映射，不能只看旧 PASS。现已核查的两条主 Opt/Freq、CAM/B3LYP 末态及 7a_repaired.xyz/SDF 都是错图；若找到另一个正确图成功链，重提取频率、47 行几何和分项误差，再对照 evaluator。
8. **没有证据时如实停下。**只在任务 reference 中明确“这两条历史计算不能验证修正后的 7a”，将诊断说明与可采纳成功链分开；原 group 记录保持原样，不能把错误对象链冒充正确链。若无正确对象的存量计算，向负责人报告最小缺口：正确 7a 在两主方法下的有效优化/站点证据及几何比较。是否安排额外验证由负责人决定，本方案不授权任何重算。

**涉及文件。**两模式 molecule.json、atom_map.json、拟新增纯实验表、task、schema、身份/误差/模型结论对应的五文件条目、task_info/paper_route、reference 的证据适用说明。先身份后指标；不能只改说明或 evaluator 名称就宣布修复完毕。

**验收。**正确连接图和标签逐条符合原文；正确 N1–C7 环键在模型图中真实存在；提交映射不会把非键合三元组算成键角；47 行去重和圆周差可复核；PR 数值比较来自同对象同方法边界；参考链必须属于正确图。132 实频和 normal termination 本身不满足此验收。

**待确认边界。**批准正确图修复及公开纯实验 47 行；若负责人要求实验列仍保密，就需另批“由 evaluator 计算误差、agent 只交几何”的职责重分配，不能保留当前不可能完成的交付。PR 方法对、整体优劣规则不足时的处理、正确对象无存量结果时的下一步，均不能擅自决定。

### 7.14 P12 — group_2 / paper_d8e5490cd9942f4f（AR、PR）

**需确认什么。**两份 81 原子作者优化结构是否作为已给定 syn/anti 对象公开。当前研究的是指定两个端点的自由能差，不是全构象发现。

**拟处理步骤。**批准该范围后保留两 XYZ，统一 task/注释/task_info 的来源；固定水连续介质、+1/单重态、298 K、1 M 和 `ΔG=Ganti−Gsyn`。保留 La 的正确模型，不把配位体/离子状态重新推断成另一种体系。公开符号定义，不公开谁更低或目标 4.2。

**验收与已有支持。**各 237 实频、ΔG=4.393821 kcal/mol；同一分子数下的标准态校正相消必须说明。若提交绝对 G，则说明其标准态而非把 1 atm 值直接称为 1 M；不额外要求未声明的结合反应或溶液平衡计算。

**待确认边界。**建议保留固定端点比较。若要求独立构象生成，另批完整图、配位和 starter 方案；本篇不因保留给定对象而获得“全构象搜索已验证”的标签。

### 7.15 P13 — group_2 / paper_c23cfabbd34b087f（AR、PR）

**需确认什么。**作者 102 原子 `1M-TIPS.xyz` 是否可作为已给定 C58H42Si2 计算模型；待求是吸收和跃迁性质，而不是结构发现。

**拟处理步骤。**批准后保留 `system.json` 和此模型，统一来源说法，保持 CHCl3 边界；task/evaluator 都只讨论截短单分子模型，不换成实验长链 dodecyl、不加入聚集体系。按物理轨道/跃迁贡献核查 HOMO→LUMO 和 π–π*，不强制原程序 209→210 编号，也不追加未做过的 NTO 作为成功先决条件。

**验收与已有支持。**300 实频、真实 TD20、735.93 nm/f=1.2539、系数 0.69912 对应既定窗口。保持735±25 nm、1.24±0.25，不用新方法分支更接近 gold 为理由换代表结果。task/schema 都是成功型合同，不把没有 promised failure branch 当作新错误。

**待确认边界。**建议接受固定模型性质范围；如想统一增加失败出口，另行批准，不与本篇科学可行性混淆。

### 7.16 P14 — group_2 / paper_d7967e22bb965daa（仅 PR）

**需解决什么。**四个 TS3A–D 的 SI 优化 TS 坐标直接公开。当前四路线比较可以保留，但不能只删除四文件而让标签失去科学含义。

**拟实施步骤。**

1. 先按正文机理图/SI 确定 A/B/C/D 各自的化学路线：所属 INT2A/B、烯炔/氢迁移原子映射、成断键关系、区域异构/接近方向的区别和 quartet 边界。拟用不含终态距离/扭转、能量或排序的 `reaction_channels.json` 表达；没有来源依据的标签定义不凭印象补齐。
2. 建议保留 `INT2A_quartet.xyz`、`INT2B_quartet.xyz` 作为已给定协调反应物，要求按同一模型化学细化/频率验证；这是反应物角色，不是允许保留待求 TS 的例外。是否保留这两个作者几何需负责人明确同意。
3. 从公开侧撤下 `TS3A_quartet.xyz` 至 `TS3D_quartet.xyz`，原件进入本包 author_results。agent 根据四路线定义自行构建猜测并寻找 TS；如确需附一个粗初猜，只能由反应物/图及通用几何独立生成，不能抖动或截取作者 TS。
4. 修改 task、schema 说明和对应过程关键点：输入是四个**待检验路线定义**而非四个已经给定的驻点；每支仍要优化、恰一相关虚频和位移性质证据。保留固定四路线范围，不扩大为无限制机理发现，也不缩成给定 TS 的能量算术题。
5. 原局部零点保持 A/B→INT2A、C/D→INT2B，原目标 10.2/12.4/13.2/12.0±1 kcal/mol 与熵/溶剂边界不变。不能改成相对分离 INT1A-sextet+2a 的总体高度后仍套同一金标。
6. 按路线身份合并真正重复的驻点，但保留 A/B/C/D 的映射和覆盖记录，不能删掉难收敛标签；失败支不编势垒或排序。若四标签无法不借助精细 TS 几何而唯一界定，报告具体歧义并请负责人决定，不能静默改为两条路线。

**验收与已有支持。**四路线无需打开 SI/author_results 即可明确要变哪些键、用哪个零点；公开无 TS 终态坐标或答案几何参数；68 原子、neutral/quartet 和原子映射保持。历史 20 个成功阶段及 10.25803/12.42552/13.19099/12.02253 支持作者路线。八条 IRC 到 40 点 MaxPoints 的事实照实保留，不新增“所有端点必须收敛极小值”来人为触发补算。

**待确认边界。**四 TS 私有化、明确路线后由 agent 搜索 TS、保留两个已给定 INT2 反应物。若需要改变四路线范围或要求额外端点验证，必须再次确认。

### 7.17 P15 — group_4 / paper_5d94285cfbd51973（AR、PR）

**当前未发现新的实质性缺口。**正确 53 原子 SMILES、有限构象/灵敏度证据和 conventional 描述符公式自洽。

**拟处理。**保留 AZ9.smi、system.json、当前 IP/EA/η/μ/χ/ω 定义和目标。复核 task/schema/evaluator 的符号、单位和派生算术；不为迎合 SI 异常有符号派生行修改公开正确定义，也不把更大基组敏感性支换成主结果以接近 gold。

**验收与已有支持。**9 个 153 实频极小值、12 轮611候选覆盖、9 个更大基组单点继续支持有限构象与敏感性。主 HOMO/LUMO/gap/dipole 均有真实输出；不将有限搜索叫作全局最小证明，不推导未验证生物活性。

**待确认边界。**建议维持现有任务，只验收已有定义；不在本轮给所有自由方法任务统一追加作者方法或批量改容差。

### 7.18 P16 — group_4 / paper_b33676a2051f5e91（AR、PR）

**需解决什么。**AR 的 9.07±2 规则在文字上限定 acetophenone 通道，条件字段却只有 validated_result；另需负责人决定“其他有效通道”在科学结论轴的地位。

**拟实施步骤。**

1. 保留公开 Int-3 反应物、不公开 TS/产物几何/势垒/赢家。PR 继续明确作者待检验路线，AR 继续自主提出候选。
2. 将 AR `ar_r4` 的适用范围在规则、关键点、最终结论中明确关联到**经证据验证的 acetophenone+ethyl 断裂通道**，核对产物图、断裂键和原子守恒，而不是只看用户填了一个同名 channel_id。
3. 势垒必须取所选通道的对应 TS 和同一个参考反应物/热化学边界；不能从 A 支选通道、B 支取能量，也不能把其他通道不在9.07附近本身当成数值错误。
4. **先请求科学成功边界。**推荐继续以论文支持的 acetophenone+ethyl 结果作为这一来源任务的科学结论基准，同时保留其他通道的有效探索、真实结果和过程得分。当前 AR final 措辞较开放，若采用这一建议，会收紧其主成功判据，必须由负责人批准；不能当作 JSON 条件小修。若负责人希望任一充分验证的最优通道可得科学满分，需要明确改成开放结论合同，并相应设计比较证据要求，不能未经确认默认实施。
5. 按实际 adapter 检查渲染结果；只添加未经实现的嵌套 `applies_when` 不能作为已修好证明。写清专家判断条件并做源内正反例检查；如需通用代码支持再单独申请。

**验收与已有支持。**错误通道即便数值9.07也不得冒充作者通道；作者通道8.89746应按既有容差；其他通道不得套此数值规则。既有一虚频TS、双向IRC与 ethyl 自旋支持指定通道，不证明三种竞争机理或无限远解离极小值。无须自动计算其他通道。

**待确认边界。**最重要的是 AR 主成功是否必须支持论文通道；数值规则限定通道可先提出，但不能替负责人决定开放探索与论文结论的计分关系。

### 7.19 P17 — group_4 / paper_46a9ca0dab36dd9e（AR、PR）

**需解决什么。**溶剂表达、代表态选择、片段/布居定义不清，导致任意态/分区都可能被套 62.4/4.3% 金标。真实 IFCT 已存在，不是需要从零计算。

**本轮新增核实，修正“原文可能没有选态规则”的不确定性。**SI S34 明确：计算 30 个六重态激发态，查看最大 f 的三个，以其中最高 f 为代表。S35 Table S4 的作者 state20/21/22 的 f 为0.0306/0.0232/0.0340，故作者选22。现有真实 [TD30 原始输出](../../docs/verification/group_4/paper_46a9ca0dab36dd9e/hpc_runs/cat1_m06_gd3_source_parent_td30_20260914_hpc20_p6/stdout.log) 的三者为0.0415/0.0299/0.0237，最亮是20；已有 [IFCT 输出索引](../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/ifct_closure_20260915.json) 中 state20 的 Mulliken-like LMCT63.541%/MLCT3.820% 也在现有容差内。依据是原文选择原则和真实输出，不是固定编号22或寻找最贴近62.4的态。

**拟实施步骤。**

1. 保留正确 34 原子 TEA+·FeCl4−、总电荷0/六重态和无作者3D的输入。将“exclude solvent”澄清为不显式引入溶剂分子，研究环境是隐式MeCN；核对优化和TD的实际溶剂响应说明，原文未展开的技术细节如属验证适配应照实标识。
2. 建议两模式都把“这组低激发态中最亮的物理态”作为待测对象：报告覆盖和前三个最大 f 的态，按最高 f 选主态，不预告该态的编号、能量或 LMCT比例。PR 可提供 SI 的 TD30 路线；AR 仍可自主选择适合的电子结构方法，但共同的被测对象定义需负责人批准。出现近简并/态混合时先报告同一小组的证据，不能按 gold 挑态。
3. 定义 Cl配体整体、Fe中心、TEA+三个片段；公开原子角色到坐标映射，LMCT=Cl→Fe、MLCT=Fe→Cl，列出所有通道和归一化。其他片段划分可以作为敏感性，不能主结果把 FeCl4 整体设为一个片段却仍宣称算出了同定义的LMCT。
4. PR 主计算协议建议依据 SI S37：B3LYP-D3BJ/Fe-SDD/其余6-31G(d)/SMD(MeCN)优化频率，M06-D3/Fe-SDD/其余6-311+G(d,p) TD；不要求相同商业程序品牌。波函数/溶剂/布居细节必须足以定义同一个量，不能只贴方法名称。
5. **布居口径单独批准。**现读原文明确 Multiwfn IFCT，但尚不足以认定某一种人口/布居方案是作者唯一指定。建议将本benchmark主比较口径显式定为现有真实输出支持的 Mulliken-like IFCT，另存Hirshfeld/态20–22对照；这是可追溯的任务协议适配，不声称 SI 明文唯一规定。负责人若不认可，则先共同确定允许的口径和相应可比性，不因为不同分区恰好命中容差就算已解决。
6. 同步 task、catalyst_system.json、schema 的 state/ifct identity、主/敏感性字段、`pr_r_states`/`pr_r_ifct`/LMCT与MLCT numeric规则及 AR 对应条目；state_id、坐标/波函数和IFCT记录必须指向同一支。原 gold 62.4±10、4.3±5 不自动改动。
7. reference 保留实际曾分析state22的历史，补充明确“按最高f规则应对照已完成的state20结果”，不能把22日志改名20。原文“其余态f<0.01”是该次计算结果，现有输出state4–6超过此值，不把这句话增为普适门槛或强行删除真实态。

**验收与已有支持。**从30态表不看IFCT百分比即可选20；其既有63.541/3.820满足目标。对“选暗态后硬比金标”“LMCT/MLCT倒置”“Fe和Cl同片段”“仅报告部分通道后重新归一成100%”做反例检查。当前证据可支持所提主规则，不需新增电子结构计算；布居适配和AR对象限定仍需同意。

**待确认边界。**两模式共同以最高f态为主对象、PR主方法、MeCN和片段定义、Mulliken-like主口径。若希望任意态/分区都能成为主目标，应另批相应评分范围，不能保留现有单值无条件比较。

### 7.20 P18 — group_6 / paper_44f9727c4e9a4b6f（仅 PR）

**需解决什么。**`1H_start.xyz` 的87原子 SI终态直接带出Fe–Fe目标；Mössbauer校准是必要定义，不属于应一起删除的答案。

**拟实施步骤。**

1. 先按正文/SI核定完整susan配体、μ-O、μ-1,2-peroxo及金属配位连接图、+2电荷、Fe1/Fe2和桥氧映射。PR可以给作者的配位/自旋假设，但不能给最终Fe–Fe距离或终态局部坐标。
2. 从配体图和通用配位模板独立构建完整87原子初始模型，替换1H_start.xyz，作者终态仅存author_results。不用Fe–Fe≈3.086或其他目标键长作约束、不用原终态抖动。如果模板不能可靠表达桥联/配位，先提交具体疑点让负责人定，不能靠错误力场“优化成功”掩盖身份改变。
3. 更新system.json、task/source说明和必要映射；保持BS/HS分支、自旋耦合和能差定义，不把BS解混成普通单一多重度闭壳层。
4. 保留mossbauer_protocol.json的A/B/C、对应密度定义、单位、SARC/J与DefGrid3等校准适用条件，保留δ=A(ρ0−C)+B；不公开作者Fe密度、δ或BS−HS答案。软件/方法变更若使校准不适用，必须报告，不自行沿用另一方法常数。
5. reference 保留真实BS极小值、高自旋比较与校准单点依赖；修文字时严格区分ORCA输出的261频率槽与非线性87原子分子的内部振动数，不把平动/转动槽算为内部模式。

**验收与已有支持。**新起点的图/配位/原子数/映射成立且不依赖终态坐标；公共测量定义足以计算δ。旧零虚频、Fe–Fe=3.086431831Å、BS−HS=−0.026282803515Eh、0.517809/0.523604mm/s仍是有效作者路线证据，不声称已从新starter完成验证。

**待确认边界。**批准独立金属初始模型替换并保留必要校准。任何桥联、质子化或BS目标定义的不确定之处，都先询问，不改变科学对象。

## 8. 需要负责人明确确认的边界（全部待答复）

下面是对第7节方案的**确认清单**，不是已经作出的决定。一般同意“修复”时，仍须明确是否包含这些科学范围；有未确认项，只暂停受影响的论文/子项。不会自动切换到备选方案。

| 编号 | 涉及论文/模式 | 推荐确认的处理边界 | 影响与不能越过的线 |
|---|---|---|---|
| D1 | d2d08、e31cc、d8e54、c23cf、80cc，两模式 | 保留作者几何作为指定对象/初态，范围分别为两态振动、cis能差、syn/anti自由能、固定模型吸收、给定anion的FC | 不声称几何发现；不是“所有SI坐标都能公开”。若不接受，另设计独立starter，不仅改注释。 |
| D2 | 746、ef，两模式；d796、44f，仅PR | 四篇待求终态/TS全部撤出公开输入；从完整身份独立构建起点；d796保留INT2A/B给定反应物及四条路线定义 | 不微扰答案、不减少原子或改变配位/反应范围；author_results不自动变成新的结构评分。 |
| D3 | 6f、5ea、a396、46a9的PR | 采用第7节的无答案作者主比较协议，其他方法作为敏感性；5ea选6-311+G(d,p)并记录正文内部冲突 | 这是主方法自由度的实际调整，需批准。AR不同时套作者全路线；M3/AZ9等不批量修改方法/金标。 |
| D4 | a396，两模式 | 按正文/SI修正7a图及映射，公开纯SCXRD的47行观测，让agent可计算MAE/RMSE；先查正确对象存量结果 | 不公开DFT列和赢家；无正确图证据就保留验证缺口。是否补验证另由负责人决定，不自动运行。 |
| D5 | 746，两模式 | 五个inner-rim扭转以平均绝对值主评分、保留带符号原值；已有实验量仍作比较背景 | 先重提旧结构确认定义等价；不改gold迁就约定，不用实验/计算目标角度构建starter，不放宽化学手性身份。 |
| D6 | 80cc，两模式 | 补纯实验谱/峰；采用Fig.3a的Z1-only、0–0相对对齐比较；诚实异议可提交但不自动视为复现成功 | 不公开作者512cm⁻¹等拟合移位、不混入Fig.3b双异构体拟合。原文无法提供可靠数据时再次请示，不擅删实验目标。 |
| D7 | 46a9，两模式 | 以低激发态中最大f物理态作为共同被测对象，明确隐式MeCN、Cl/Fe/TEA分区；主IFCT采用明确的Mulliken-like任务口径 | 原文有最高f选态依据，但布居口径的固定属于benchmark适配，需同意。不能固定state22、按百分比挑态或承诺任意分区都等价。 |
| D8 | b336的AR；同时涉及80cc的PR评分表述 | b336建议保留论文通道作为科学结论基准，其他通道保留有效探索/过程得分；80cc区分反例合法性与论文结论得分 | b336现有AR措辞较开放，收紧主成功标准是实质决定；若要开放结论满分，必须另明确合同。两者均不改全局scorer或自动重分权重。 |
| D9 | 6f的AR；5ea的AR方法解释 | 6f把“证明广泛覆盖无影响”改为有限覆盖/真实敏感性/残余不确定性；5ea保留自主路线与现有准确性目标 | 不把没有敏感性证据写成稳健、不默默删除必评实验、不把自由方法解释为任何数值都可过。若要改定量评分强度，需另批。 |

其余建议如失败分支允许真实unknown、能差符号一致性、模式对应和例外处理、正文/SI冲突注记，都依第7节具体范围等待批准；**也不会因为被称作“小修”就先动手**。P05/M3、P09/3a、P15/AZ9等建议保留的项目，验收已有修复即可，不为显得“每篇都处理”制造新改动。

**执行中遇到以下任一情况，立即记录并询问，不自行选择科学结果：**

1. 原文结构图、名称、SMILES、质子化/配位或原子标签不能相互唯一对应，或者拟生成starter改变了化学身份。
2. 原文未指定的布居、态混合、总体误差加权、失败/成功界限需要新增判断，且超过已批准的具体定义。
3. 新定义重提既有输出后改变原gold含义、得分关键点、论文定性结论或必要数据范围。
4. 实验图无法可靠分离/读出，47行存在无法解释的标签，或四条TS路线无法离开终态几何自包含定义。
5. 找不到正确对象的成功验证链，或者真实结果与原必评结论相反。不能通过改reference叙述、改目标值、调容差、删评分项或重贴PASS解决。
6. 需要新增量化计算、调用外部付费评分、改变执行器/网络/挂载权限，或发现其他人的重叠修改。

## 9. 批准后的顺序、验收交付和本轮停点

### 9.1 推荐实施顺序

1. **对象和输入依赖优先：**先处理a396正确图/映射及证据检索，Z1实验资料；同时按已批准范围准备746/ef/d796/44f的独立结构/路线。不能先删输入再决定任务如何可做。
2. **公共测量定义及PR路线：**对齐6f/5ea/a396/46a9的主比较协议、helicene角度、FC对齐、IFCT态/片段定义；仍不公布计算答案。
3. **任务与评分同步：**完成Rh101例外、e31符号、b336通道及获准的成功范围、6f覆盖措辞、Z1合法异议与结论得分区分，以及746/5ea/a396失败schema。必须逐篇检查实际judge合同，不能只改单份task.md。
4. **保留项定向复核：**M3、3a、AZ9以及批准固定对象范围的热化学/吸收任务只做必要核对；无问题不改。
5. **整批技术复查后汇报：**检查34包结构、输入/链接、schema正反例、evaluator绑定、原目标/单位/容差差异、公开侧答案残留和reference证据适用性。只刷新实际发生变更的包manifest，不建立新哈希体系，不用校验值证明科学正确。
6. **等待负责人第二次确认：**给出逐篇/逐模式的实际改动及未解决项；即便建议通过，也继续保留verified_tasks，直到负责人明确批准迁移清单。

### 9.2 最低验收清单

| 方面 | 修复完成时必须能回答的问题 | 不能用来替代的证据 |
|---|---|---|
| 研究对象 | 分子图/立体化学/原子映射/电荷/自旋与正文/SI或获准模型一致吗？ | 分子式相同、能收敛、旧PASS |
| 输入充足 | 不读论文、evaluation或group记录，能知道要研究什么、观测什么、交付什么吗？ | 私有reference里“其实写过了” |
| 无答案输入 | 待求结构、TS、结果值、排名、作者已经判定的结论是否仍可从公开数据/注释/样例直接读出？ | 删除“SI”字样、改starting文件名、只做坐标微扰 |
| 模式区分 | AR保留自主路线，PR仅增加获准的研究假设/路线，二者均不公开答案吗？ | 两模式机械复制全部私有路线 |
| 提交合同 | 成功要求真实完整证据，未计算/失败能如实表达，且null不能冒充成功吗？ | JSON可解析、所有未知数填0 |
| 评分一致 | 方法/态/分区/通道/符号/单位/选择范围与具体参考量相同吗？ | 一个数字碰巧在容差内、加了未实现的条件字段 |
| 计算支持 | 已有真实成功链确实算的是当前正确对象及必评量吗？ | reference很长、normal termination、换名字后的错分子日志 |
| 结论范围 | 有限构象/两端点/局部模式的证据有没有被写成全局或普适结论？ | 过程合理就宣称所有paper结论已复现 |
| 存档 | reference能找到成功阶段输入依赖、设置、输出和对应关键点，且无新计算被凭空加入吗？ | 用新评分文件倒写历史计算 |

**需要单独检查的部署边界。**包内只复制agent_input，与执行环境真正不能读到私有材料，是两件事。正式评测前应在实际agent工作区检查父目录/绝对路径/软链接/共享挂载是否能触及evaluation、papers、group日志或其他任务答案，以及联网工具是否受既定禁止查答案策略约束；测试只确认访问边界，不把私有答案输出给被测agent。若运行器仍暴露仓库，需要单独批准最小隔离修复，本次任务包修改不包含平台权限变更。没有该检查不能声称“绝对无泄露”，也不因部署未测就反推论文科学量不可算。

### 9.3 各类问题最终交付什么

- **泄露修复：**旧终态仍可追溯但仅私有，公开身份和独立starter/路线自包含，明确不声称新starter已被重算验证。
- **数据缺失修复：**新增的是可溯源的实验观测/原子映射/必要测量定义，不是从计算答案派生出的伪输入；无法补齐时给出具体缺口和待决项。
- **方法和评分修复：**一张篇内简明对照说明“同一个量如何由task定义、schema交付、evaluator判定”；不是另造大型管理系统，也不改global权重。
- **reference修正：**仅处理真实链适用范围和确有依据的遗漏/引用；a396错误链不再被用来认证正确7a，但原始group资料不动。其他历史使用作者结构的成功链不能因输入去泄露被否定。
- **最终汇报：**本报告内更新实际修改、验收结果、仍待负责人决定的具体科学问题和候选迁移清单；不把建议迁移写成已迁移。

### 9.4 本轮执行记录与停点

本轮已补充18篇逐篇方案，并做必要的只读复核，尤其确认了Cat1的SI最高f选态原则、现有state20输出，7a的AR并未强制CAM胜负，以及当前dual-axis评分的实际适配方式。**本轮仅更新本报告；未实施第7节任何任务修复，未改docs/verification，未移动任何任务，未提交任何新科学计算。**

所有任务仍在verified_tasks。本方案不把此前“建议final/暂缓”恢复成验收状态；等待负责人对本方案及第8节边界逐项或明确整体确认后，再开始获准的修复。

## 10. 已批准实施记录（2026-09-16 起）

本节是获准修复完成、7a 尚未获准迁移时的记录；后续复审和迁移以第 11 节为准。第 3–9 节保留为审批前分析历史，不代表修复已经执行。负责人明确批准了随后对话中的八项推荐边界，并曾要求修复后分析本批及第一批 final 自主任务的科研自主性；该统计随后交由其他 agent。

批准范围：保留五篇给定结构性质任务和已知反应物；公开必要纯实验观测，746 的实验角度转私有；四篇 PR 主比较协议；746 平均绝对扭转；Z1-only 相对 FC 比较；Cat1 最高 f 选态及 Mulliken-like IFCT；b336 AR 保持开放通道而非强制作者通道；7a 按物理量分别统计误差，未定义的总体加权不擅造。

本节特别覆盖旧方案的两个不同建议：746 实验 27° 不再公开；b336 AR 不收紧为必须找到作者通道。其他获准修复以最近一次完整方案为准。任何新增科学边界仍需询问。

基线：`ed724c76` 保存本批实施前的完整方案；此前任务内容基线 `7aecf414`。提交时仓库 pre-commit 对缺失 `sbin/copyright` 给出警告，但 Git 提交成功；未改动该钩子或纳入其他工作。

- [x] 保存实施前基线，核对本批 18 篇 / 34 包。
- [x] 补齐身份/实验/路线输入，并替换直接泄露待求结果的结构。
- [x] 同步受影响的 task、schema、私有路线和五文件 evaluator；无冲突的条目保留。
- [x] 用已有计算输出、软件正反例和公开输入审查复核；结果与科学证据缺口分别报告。
- [x] 逐篇记录完成项、证据缺口及需确认事项；不迁移、不重算。
- 已按最新指令取消本轮自主科研能力分类统计，由其他 agent 负责；未生成该报告，未以统计为由改任务目标。

后续记录均追加实际操作及验证结果，不能将计划勾选为完成而不留对应依据。`docs/verification`、canonical 源任务、第一批 final 的科学内容在本轮保持只读。

### 10.1 实际完成顺序

1. **固定审批边界和版本。**在 `ed724c76` 基线之上，仅处理本批 AR16/PR18；既有仓库其他未提交工作不纳入修复提交。
2. **修复公开数据依赖。**先修正 7a 的完整原子映射连接图、47 行纯实验观测；从 Z1 SI Fig S1 单独的黑色实验向量曲线提取 825 个窗口内顶点（与 metadata 的 point_count 和 CSV 数据行数一致），排除蓝色拟合及红色背景；保留 Rh101 原有纯实验峰表和缺测。
3. **处理待求结构泄露。**compound 5、free/PO/PA、1H 共 9 份包内 XYZ 换成完整拓扑独立嵌入起点；保留源原子编号和离散身份，不使用作者终态距离、目标角度或能序选点。双铁初次嵌入出现不合理近 O···O，复查后用通用非键合排斥边界重新生成，通过后才保留当前版本。4 份 TS3A–D 从公开侧移入 `evaluation/author_results/`；两个 INT2 反应物保留，新建四路线/成断键/原子角色定义。以上原坐标均可从私有归档恢复，未丢弃。
4. **对齐测量与方法。**四篇 PR 明确已批准的主协议；d796 补源方法及 2/3 熵表达式以明确原局部势垒的计算定义。AR 没有机械复制 PR 作者全路线。明确五角 mean(abs)、物理模式对应、e31 正号/能序联合判定、Cat1 最高 f 及 IFCT 片段/口径、b336 开放通道的数值适用范围。
5. **修复真实失败出口。**746/5ea/7a 的未知频率、无几何/无误差数据可以如实报告，不能以零占位。d796 同时修复未得到 Hessian 的失败候选；成功 TS 仍须一个相关虚频。测试发现并修正了 7a CSV 来源含逗号未加引号，以及 d796 顶层与 result_schema 重复定义不同步两处技术错误。5ea 成功至少须含一个有真实零虚频的候选，选中 ID 与证据的对应仍由 evaluator 查验。
6. **复查存量证据。**Z1 的旧 FC 与新增实验数据进行相对对齐诊断，全部 11 条窗口内已存跃迁均保留；Cat1 最高 f 对应已有 state20，不将 state22 更名冒充；7a 扩大检索含被 Git 忽略的日志，67 份有可恢复几何的记录无一匹配修正后的正确图。
7. **整批软件及公开侧复查。**34 包通过现有包校验、schema 检查、adapter 合同与 agent_input 物化；原金标/数值容差/单位/显式权重未改；33 份当前公开 XYZ 可解析，新 9 份的图映射/式/近接通过。沿用项目现有 manifest 机制同步文件清单，不把校验值当作科学证据。

上述脚本位于 `scripts/*staged*20260916.py`，只生成待审 apply_patch 或解析已有文件；不是计算作业提交脚本，不应盲目重跑已实施批次。维护证据仍在每包 `evaluation/task_provenance/`，计算结果/原坐标在 evaluator 私有侧，未新建外部 evaluator_private 目录。

### 10.2 逐篇实际结果

“包层修复完成”表示本次获准的信息、定义和一致性修复已经执行，不表示所有可能方法都会命中同一数字，不表示自主 agent 已盲测成功。历史作者路线使用作者结构是合法验证；更换公开 starter 本身不要求重算。

| group / paper_id | 模式 | 已执行的处理 | 既有验证与当前状态 |
|---|---|---|---|
| 1 / paper_d2d08c91f34da1cb | AR、PR | 保留获准的两态给定几何；明确物理位移对应、交换/混合/近零例外和实验缺测，不要求普遍红/蓝移 | 两态各195实频、24有效配对 MAE 1.262626；原作者子任务支持保留，包层修复完成 |
| 1 / paper_6f9a36fff6964313 | AR、PR | PR 固定两层级 Mulliken 主协议；AR 改为有限覆盖/真实敏感性/残余不确定性 | 四电荷和两差值真实有据；不能把单构象验证外推为全构象稳健，未做敏感性不得自动得分 |
| 1 / paper_746e066c163800d8 | AR、PR | 独立72原子 starter及映射；五角平均绝对值；实验27°私有、由 evaluator 比较；失败 schema | 历史 mean(abs)=27.09676855°及收紧检查支持原金标；未宣称新 starter 已优化验证 |
| 1 / paper_5ea491c741fbd8d4 | AR、PR | 失败候选可填null并说明；PR B3LYP/6-311+G(d,p)，记录原文另一基组表述冲突；AR保留路线自由和准确性要求 | 五起点/三极小值与真实轨道值保留；成功须对应有证据候选，不因允许null而降低标准 |
| 1 / paper_a0f6b899582cb9f7 | AR、PR | 复核既有M3身份、raw二阶矩、原点/完整旋转/DÅ/面法向；科学内容无须再改 | 已有66实频、Qzz=-111.07681064 DÅ等支持当前孤立分子目标 |
| 1 / paper_ef26687d63a37e29 | AR、PR | 46/56/61原子三完整图独立嵌入；所有作者坐标片段私有化；更新来源说明 | 完整模型的接触、ADCH、ESP历史证据保留；不声称新起点收敛已测 |
| 1 / paper_e31cc7bc7b21b610 | AR、PR | 保留给定cis对象；私有评分联合核对 ΔE=Eβ−Eα、正号、绝对能及能序 | 各168实频和1.43847762 kcal/mol支持；−0.02虽在数值区间也不满足作者能序 |
| 1 / paper_80cc1ffb2cf73fc5 | AR、PR | 保留给定anion；补纯实验曲线；按自算0–0/实验最低峰相对对齐；物理模式与诚实异议/复现得分分开 | 旧FC支持有限突出特征及进动；后处理保留未解释峰/强度差异，不声称全谱或绝对脱附能验证 |
| 2 / paper_a3892396b1843698 | AR、PR | 复核3a是合法反应物，两通道身份、TS/IRC及entropy-only qRRHO；未改目标 | 两条TS、双向IRC和四端点有据，23.50589160/26.22790785 kcal/mol保留 |
| 2 / paper_46f6118697c6397c | AR、PR | 复核完整CIF/四triflate；保留已记录的正文/SI冲突和物理态/轨道解释范围 | SI 3.8436eV/322.58nm/f0.4243自洽，三分支Opt/Freq+TD50有据；未新增其他化合物因果对照 |
| 2 / paper_a3968806251093cd | AR、PR | 修正7a图、完整标签映射及Cl别名；补13/23/11纯实验行；PR明确方法对；分项误差和失败schema | **包层修复已做，但正确对象验证尚未闭合：67份历史几何均不匹配。两模式都不能标为已验证通过；PR总体赢家也不能由旧错对象误差认证** |
| 2 / paper_d8e5490cd9942f4f | AR、PR | 保留获准给定La两端点；核对+1/singlet、水/298K/1M、anti−syn，统一来源 | 两端点各237实频、4.393821 kcal/mol支持；不是全局构象搜索证明 |
| 2 / paper_c23cfabbd34b087f | AR、PR | 保留获准C58H42Si2给定模型/CHCl3；按物理跃迁解释，不固定轨道号，不强加NTO | 300实频、TD20、735.93nm/f1.2539支持既定模型吸收，不外推长链/聚集体系 |
| 2 / paper_d7967e22bb965daa | PR | 四TS私有化；两INT2+四路线公开，原子角色/反应面/局部零点自包含；同一热化学定义 | 20个成功阶段及10.25803/12.42552/13.19099/12.02253支持；历史IRC的MaxPoints限制保留，不额外要求端点优化 |
| 4 / paper_5d94285cfbd51973 | AR、PR | 复核53原子图、conventional描述符、有限构象和敏感性；不新增目标 | 9极小值/611候选及基组敏感性有据，不声称全局证明/生物活性 |
| 4 / paper_b33676a2051f5e91 | AR、PR | AR保持开放通道；9.07±2仅用于对应化学通道，按图/断键而非标签判断；PR原路线保留 | 历史指定通道有真实TS/有限IRC证据；不能声称验证了所有AR备选通道，其他通道按自身证据评价 |
| 4 / paper_46a9ca0dab36dd9e | AR、PR | 明确MeCN、最高f物理态、Cl/Fe/TEA及Mulliken-like全通道；PR主协议 | 既有最高f state20的63.541%/3.820%支持原容差；state22及Hirshfeld记录保留为历史/敏感性 |
| 6 / paper_44f9727c4e9a4b6f | PR | 87原子独立配位图starter；明确O3–O4 peroxo/O5 μ-oxo、无Fe–Fe共价键；保留BS/HS及校准 | 历史Fe–Fe=3.086431831Å、BS−HS=-0.026282803515Eh、δ=0.517809/0.523604支持；未重算新starter |

### 10.3 不能宣称已经解决的事项，以及交接建议

**明确的论文级验证缺口只有本轮确认的7a：`paper_a3968806251093cd`，AR和PR共2包。**其余17篇32包的相应作者路线核心计算支持仍可使用，未发现需要因本轮输入去泄露而自动重算的理由。这里不是对所有自主探索分支、所有合理方法、全部过程得分或所有实验峰的满分保证。

7a不是“验证者看了作者答案”导致无效，而是实际分子图不同。任务当前要求 pyrazole 环 N1–N2–C9–C8–C7：N1接phenyl、C7接O1-chlorophenyl、C8接imine、C9接methyl。历史末态把这些取代位置放错；正常终止/132实频/同分子式均无法修复这一点。当前公开图与全部47个选择器的连续成键关系已核对成立。

建议：先请验证负责人确认是否还有**未放入当前group_2目录**的正确7a既有输出。如有，提供位置后可继续只读提取，核对身份、两种泛函下的优化/站点证据和47行分项误差；如无，补正确对象验证需要另行授权/交给验证agent。本轮没有运行、提交或安排该计算。PR源论文的总体CAM优劣只是待正确对象证据支持的结论，不能用不同单位随意加权制造赢家；若正确分项结果仍混合，届时再由负责人决定总体结论边界，当前不擅改。

另外保留三类正常范围声明，而非要求现在追加计算：

- 4篇几何/TS泄露修复后，旧作者路线仍证明该科学终点可算；**未声称当前独立starter的盲跑已通过**。新starter拓扑/近接检查不是DFT收敛保证。
- 6f的构象/布居敏感性、b336其他开放通道、Z1未归属峰等，必须按已有证据的范围说明；不能因为任务允许报告限制就宣称已经取得稳健性或全部结论分数。
- 实际评测环境的父目录、共享挂载、软链接、网络/检索访问隔离仍须发布前在部署端检查。包物化测试只证明复制内容限于agent_input，不等于运行中的agent绝对读不到整个仓库；本轮没有授权修改平台隔离或执行器。

### 10.4 验收记录与本轮停点

- `python -m pytest tests/test_task_package_v19.py tests/test_staged_repairs_20260916.py -q`：**55 passed**（原包测试10项，本批专项45项）。
- 34/34现有包验证及JSON Schema定义通过；34包的runtime adapter确实包含修订后的规则，物化仅复制agent_input；全部原numeric targets/tolerances/units/显式weights与`ed724c76`一致。
- 33/33公开XYZ可解析；新独立起点9份的完整图/原子映射/式及近接检查通过；7a全部47选择器的连续键均存在于修正图。通过不等于已做新的Opt/Freq。
- 1066个包内Markdown相对链接检查无断链（排除行内SMILES的伪链接）；`git diff --check`通过。evaluation仅保留五核心JSON、reference及author_results/task_provenance等已约定子目录。
- 未执行新的LLM评分或量化计算。错误符号/通道/片段的测试检查的是规则承载和软件/数学反例，不冒称真实judge行为已通过端到端评分试验。
- 所有任务仍在verified_tasks。当前停点为交付修复结果和7a证据缺口，等待负责人复核与**另行**批准去向；本次不移动final/hold、不写docs/verification、不改canonical/论文/第一批final、不进行已取消的自主科研分类统计。

## 11. 修复后再次逐篇复审与 7a 授权迁移（2026-09-16）

负责人随后明确要求再次确认 7a，若确实不能直接修复则移入 hold，并对其余论文逐篇复审。完整当前分析集中在 [POST_REPAIR_REAUDIT_20260916.md](POST_REPAIR_REAUDIT_20260916.md)，不再用上文审批前问题列表代表现状。

- 7a 两包已完整移入 `tasks/hold_verified_autonomous_research/paper_a3968806251093cd`、`tasks/hold_verified_paper_reproduction/paper_a3968806251093cd`。正文连接图、67 份篇内旧几何、额外两份队列初态、去氢图同构及真实键距共同确认：旧验证对象是另一位置异构体。任务身份修正不能把该旧链变成正确 7a 验证。未删除原始计算，也未重算。
- 其余 17 篇/32 包保留在 verified_tasks；98 份 reference 所链原始日志可访问，核心作者路线结果仍支持所选科学目标，未发现另一篇同等级错误对象。作者路线验证使用已知终态不构成验证无效；独立 starter 未盲跑也不是自动重算理由。
- 新发现的主要待澄清项是 ef266 的主 O/接触 H 汇总规则（两模式，PR 评分影响更直接）和 Cat1 AR 的泛化选态话语与最高 f 主规则冲突。还有 reference 历史时态、3 处 canonical 链接语义错位及 44f 证据索引旧公开坐标措辞。详见新报告逐篇证据和最小修法；本轮没有改动这 17 篇的科学内容。
- 包/schema/物化及专项测试 **55 passed**；测试仅证明软件契约，不等于 DFT、当前 starter 盲测或真实 LLM judge 已新跑通过。
- 未写 `docs/verification`、papers、canonical 或第一批 final；没有新量化计算/HPC操作。只有 7a 的迁移、状态/链接/包清单、回归测试和两份本批报告发生本轮变更。

## 12. ef266 / Cat1 两项澄清获准实施（2026-09-16）

负责人随后明确批准修复第 11 节两项指令问题。本轮只修改 ef266 AR/PR、Cat1 AR 的相关任务定义，Cat1 PR 复核后保持原样。详细改动/证据见 [复审报告第 7 节](POST_REPAIR_REAUDIT_20260916.md#7-两项澄清问题的获准修复结果)。

- ef266：固定指定 O49/P46，按同一 O 分别选全部 graph-defined alphaH/betaH 中最近 H；同一映射约束主接触电荷，禁止跨 O 拼值/隐藏作者 H 标签。同步题面、schema、关键点、评分比较及元数据；AR summary 可选，不强加 PR 数值输出。旧成功几何后处理准确重现六个距离及所选 H 电荷。
- Cat1 AR：目标、要求、schema、coverage 评分统一最高 f 主态；其他选态准则只作辅助/敏感性；主 state_selection/ifct 同态，隐式 MeCN/无显式溶剂清晰。保留自主设计，不给固定作者态号/结果。
- 数值目标、容差、权重、单位和现有输入结构均不变；62 项回归通过。仅做已有几何后处理，未新增量化计算/LLM评测，未写原始验证目录，也未迁移任何任务。

## 13. 最终包审查与本次迁移授权（2026-09-17）

### 13.1 范围、授权和判定

负责人最新明确要求：**“最后一次检查，如果 verified_tasks 中的任务都没有问题的话，就帮我移动到 final 文件夹中。”**这次是对本批剩余包的条件迁移授权，不是把此前泛泛的“继续”当作授权。按既定科学范围完成最终核对后，拟迁入清单为下表 **17 篇、32 包（AR15、PR17）**；7a 已在 hold，不在此次清单内。先记录这项授权和逐篇结论，再完整迁移；实际执行与迁后检查在第 13.4 节记录。

结论是：本批所选科学子目标有适用的历史作者路线成功计算支持；未发现尚未解决的必要输入缺失、包内答案泄露、任务/评分定义冲突或当前必评结论无据的问题。这个结论不等于验证了每个自主探索分支、所有方法、全部敏感性过程分或所有可能起点；不将 bounded_failure 当作成功证据。论文/SI、旧计算及逐条评分的证据承接[逐篇复审第 4 节及后续修复第 7 节](POST_REPAIR_REAUDIT_20260916.md)，此次特别复核了有限搜索、有限 IRC、相对谱和 Cat1 主态的适用范围。

### 13.2 逐篇迁入清单与证据边界

下表 AR/PR 均单独核对题面、输入、schema、评分与相应 reference；两模式共用一条历史作者路线，不冒称做了两次不同盲测。链接指向迁入后的完整任务包，计算步骤与原始输入/输出索引均在包内 `evaluation/verified_computation_reference.md`。

| group / paper_id | 通过的模式及目标位置 | 支持当前关键点/结论的真实证据 | 必须保留的边界 |
|---|---|---|---|
| 1 / paper_d2d08c91f34da1cb | [AR](../final_verified_autonomous_research/paper_d2d08c91f34da1cb)、[PR](../final_verified_paper_reproduction/paper_d2d08c91f34da1cb) | S0/S1 各195实频；位移匹配、24实验配对，MAE 1.262626 cm⁻¹ | 给定对象性质；允许模式混合/交换，不要求普遍同向位移或所有误差<3 |
| 1 / paper_6f9a36fff6964313 | [AR](../final_verified_autonomous_research/paper_6f9a36fff6964313)、[PR](../final_verified_paper_reproduction/paper_6f9a36fff6964313) | 三完整系统Opt/Freq及同几何电荷单点；四电荷0.203728/0.198533/0.040059/0.058695 e及两差值 | 单构象只证明该比较；AR未测试的敏感性不得获稳健性分，PR按公开两层主协议 |
| 1 / paper_746e066c163800d8 | [AR](../final_verified_autonomous_research/paper_746e066c163800d8)、[PR](../final_verified_paper_reproduction/paper_746e066c163800d8) | 210实频；五角平均绝对值27.09676855°及收紧条件检查 | 独立公开初态；作者终态/实验目标私有；不声称新初态已盲跑 |
| 1 / paper_5ea491c741fbd8d4 | [AR](../final_verified_autonomous_research/paper_5ea491c741fbd8d4)、[PR](../final_verified_paper_reproduction/paper_5ea491c741fbd8d4) | 五候选、三极小值各75实频；轨道−6.56393059/−2.88386271 eV | 有限构象；PR采用已批准主基组，原文冲突保留；未知频率不能填零 |
| 1 / paper_a0f6b899582cb9f7 | [AR](../final_verified_autonomous_research/paper_a0f6b899582cb9f7)、[PR](../final_verified_paper_reproduction/paper_a0f6b899582cb9f7) | 正确24原子M3，三个66实频极小值；raw Qzz=−111.07681064 DÅ | 相同原点/旋转/法向/raw定义；不外推器件性能 |
| 1 / paper_ef26687d63a37e29 | [AR](../final_verified_autonomous_research/paper_ef26687d63a37e29)、[PR](../final_verified_paper_reproduction/paper_ef26687d63a37e29) | 46/56/61原子完整模型，Opt/Freq、ADCH、ESP；同O49选出的六接触及H电荷一致 | 三独立初态；同O最近αH/βH，不跨O拼最小值；旧后处理有效产物与进程异常分开 |
| 1 / paper_e31cc7bc7b21b610 | [AR](../final_verified_autonomous_research/paper_e31cc7bc7b21b610)、[PR](../final_verified_paper_reproduction/paper_e31cc7bc7b21b610) | 两态各168实频；Eβ−Eα=+1.43847762 kcal/mol | 给定异构体；容差之外必须联合正号/能序，非全构象或溶液平衡证明 |
| 1 / paper_80cc1ffb2cf73fc5 | [AR](../final_verified_autonomous_research/paper_80cc1ffb2cf73fc5)、[PR](../final_verified_paper_reproduction/paper_80cc1ffb2cf73fc5) | 两态各75实频，独立成功FC、HR=1.20932；11跃迁与825点实验trace相对对齐 | Z1-only有限突出特征/进动；保留未解释峰，非全谱/绝对ADE准确性；理论平移量私有 |
| 2 / paper_a3892396b1843698 | [AR](../final_verified_autonomous_research/paper_a3892396b1843698)、[PR](../final_verified_paper_reproduction/paper_a3892396b1843698) | 两TS各一个相关虚频、双向IRC及四端点；23.50589/26.22791 kcal/mol | 合法反应物公开，TS/产物答案不公开；历史作者TS起点不使验证无效 |
| 2 / paper_46f6118697c6397c | [AR](../final_verified_autonomous_research/paper_46f6118697c6397c)、[PR](../final_verified_paper_reproduction/paper_46f6118697c6397c) | 自包含68原子完整四triflate模型；三分支Opt/Freq+TD50 | 采用SI自洽3.8436eV/322.58nm，不混用正文4.33eV；按物理跃迁而非固定编号 |
| 2 / paper_d8e5490cd9942f4f | [AR](../final_verified_autonomous_research/paper_d8e5490cd9942f4f)、[PR](../final_verified_paper_reproduction/paper_d8e5490cd9942f4f) | 81原子La、+1/伪单重态/水，两端点各237实频；anti−syn=4.393821 kcal/mol | 给定两端点、相同ECP/自由能定义，不宣称穷尽搜索 |
| 2 / paper_c23cfabbd34b087f | [AR](../final_verified_autonomous_research/paper_c23cfabbd34b087f)、[PR](../final_verified_paper_reproduction/paper_c23cfabbd34b087f) | C58H42Si2模型，300实频、TD20；735.93nm/f=1.2539及轨道证据 | 给定102原子截短模型，非长链/聚集；未另行扩充通用失败schema |
| 2 / paper_d7967e22bb965daa | [PR](../final_verified_paper_reproduction/paper_d7967e22bb965daa) | 6 Opt/Freq+6单点+8 IRC；四局部势垒10.25803/12.42552/13.19099/12.02253，A<D<B<C | 公开两INT2+四通道，四作者TS私有；MaxPoints不是产物极小值，非整个循环 |
| 4 / paper_5d94285cfbd51973 | [AR](../final_verified_autonomous_research/paper_5d94285cfbd51973)、[PR](../final_verified_paper_reproduction/paper_5d94285cfbd51973) | 611候选/12轮/9盆地各153实频，9组敏感性单点；轨道和偶极支持 | 有限构象，使用公开conventional描述符公式，非全局/生物活性证明 |
| 4 / paper_b33676a2051f5e91 | [AR](../final_verified_autonomous_research/paper_b33676a2051f5e91)、[PR](../final_verified_paper_reproduction/paper_b33676a2051f5e91) | Int3极小值、TS−474.9764cm⁻¹、IRC几何/自旋；势垒8.89745683 kcal/mol | 产物侧IRC有限；AR其他有效通道不按9.07错罚，未验证全部可选通道 |
| 4 / paper_46a9ca0dab36dd9e | [AR](../final_verified_autonomous_research/paper_46a9ca0dab36dd9e)、[PR](../final_verified_paper_reproduction/paper_46a9ca0dab36dd9e) | 96实频、TD30最高f为state20；真实Mulliken-like IFCT=63.541%/3.820% | 主态不固定编号；Cl/Fe/TEA全通道归一化，state22/Hirshfeld仅对照 |
| 6 / paper_44f9727c4e9a4b6f | [PR](../final_verified_paper_reproduction/paper_44f9727c4e9a4b6f) | HS/BS及正确核密度单点；FeFe=3.08643Å、BS−HS=−0.0262828Eh、δ=0.517809/0.523604 mm/s | 独立87原子初态；校准常数合法，作者几何私有；261打印项非261个物理振动 |

### 13.3 本轮实际清理与没有改变的内容

- 清理 ef266、746、d796、80cc reference 的历史输入/当前输入时态；修正 PR d2d08、6f9a、746 的 canonical 链接。
- Cat1 两份 reference 将已存在的 state20 主链直接写进步骤、结果和比较段；保留真实 state21/22 和 Hirshfeld 对照，不再让读者从文末猜哪个结果有效。再次读取原始TD及IFCT表确认 f=0.0415、0.63541/0.03820；没有新TD或IFCT计算。
- Z1 将既有实验选峰、相对对齐和最近突出峰比较步骤写入 reference，避免将来删除 task_provenance 后丢失这段有效后处理定义；没有把它新增为评分阈值。
- 44f evidence_map 仅更正作者坐标的私有历史证据身份；不改变证据编号或科学结果。
- 题面、公开数据、schema、task_info、paper_route、评分关键点/结论、失败规则、目标值/容差/权重均保持上一轮修复版本 `8feb10f5`；迁移只维护档案、路径、状态和manifest。未修改 docs/verification、papers、canonical、原有第一批 final 或 hold，未重算/操作HPC，也未做科研自主性分类。

### 13.4 迁移与发布前边界

迁移前：32/32 包校验通过；迁移前回归为 `python -m pytest tests/test_task_package_v19.py tests/test_staged_repairs_20260916.py -q`，取得 **62 passed in 20.41s**。迁移后专项测试已明确枚举这32个 final 包，并使用标准模式目录的临时发布副本检查真实 TaskRepository/adapter/物化；`python -m pytest tests/test_task_package_v19.py tests/test_staged_repairs_20260916.py -q` 取得 **65 passed in 20.17s**，加入既有 final 结构修复回归后，`python -m pytest tests/test_task_package_v19.py tests/test_staged_repairs_20260916.py tests/test_remaining_final_task_repairs.py -q` 取得 **83 passed in 19.61s**。没有因 verified_tasks 为空而漏测本批。

实际迁移结果：`tasks/verified_tasks/autonomous_research` 与 `tasks/verified_tasks/paper_reproduction` 均已清空；本批新增 `final_verified_autonomous_research` 15 包、`final_verified_paper_reproduction` 17 包。连同原有 final，当前统计为 AR **67**、PR **70**；hold 保持 AR **4**、PR **4**。

迁移收尾复核：32 份 `evaluation/task_provenance/maintenance_audit.md` 已在顶部注明当前 final 位置与批准状态，旧的退回/待审批语句明确作为历史保留；两个模式的 final 入口摘要追加本批迁入状态，没有重新认证第一批。两份本批报告的 84 处旧暂存目录链接更新到实际 final 位置，报告链接也纳入回归检查；32 份 manifest 同步重建。收尾后的同组命令分别取得 **65 passed in 42.42s** 和 **83 passed in 20.70s**。本次只补齐归档状态、链接和回归覆盖，未改变获准的科学目标、输入、schema 或评分。

**包层通过不等于部署或论文投稿验收。**正式运行时只提供 agent_input；不得让agent访问evaluation、reference、论文/SI、group输出、task_provenance或后台任务元数据API。现行提示词构造未注入paper标题/DOI，但通用 `load_public_task`/Web info API仍能返回完整task_info，不能将这些后台接口当作agent安全输入白名单。共享挂载、父目录/绝对路径、网络和检索隔离须在真实部署上确认，本轮不改通用执行器/平台权限。

正式评估应使用仅包含获准final版本的标准 `autonomous_research/`、`paper_reproduction/` 发布根或明确适配。当前 TaskRepository 默认不会把 `final_verified_*` 目录自动当标准模式，不能直接沿用canonical根而误测旧包，不能索引hold或同题多个版本。本轮不上传、不正式运行benchmark、不声称当前starter盲测、真实LLM judge行为或期刊发表标准已端到端验证。

## 14. 对既有审查过程及发布条件的最终复核（2026-09-17）

### 14.1 结论与实际覆盖范围

**本批 17 篇、32 个任务的作者路线核心计算支持仍成立；此前迁入 final 的科学判断没有被本轮原始证据推翻。但不能把当前整个 final 工作区宣布为“全部没有问题、可直接正式发布”。**扩大到旧批次后，确认漏检了一篇任务的公开输出字段与评分字段不一致，以及两篇计算档案的链接/测试路径遗漏；另有评分选择器兼容性和实际发布入口需要处理。以下明确区分任务问题、档案问题与部署尚未验收的事项，不把它们统称为“需要补算”。

本轮按溯源复核口径区分原始事实、既有审查结论及未验证的范围；只读检查任务、论文和原始输出，仅在本报告追加结果。没有修改任何任务包、运行器、测试或 `docs/verification`，没有量化重算、HPC 操作、迁移或发布。

| 范围 | 当前数量 | 本轮实际检查 |
|---|---:|---|
| final 全集 | 70 篇，AR 67 / PR 70，共 137 包 | 逐包结构、manifest、必需数据路径、evaluation 布局、reference 存在性；全量评分字段与 schema 声明、reference 本地文件链接、相关回归 |
| 最近迁入的本批 | 17 篇，AR 15 / PR 17，共 32 包 | 在上项基础上，逐篇复核两模式题面/评分/公开边界及成功链；回查 98 份直接链接的原始输出，并重点核对原论文方法与易混淆物理量 |
| 既有 final 批次 | 53 篇，AR 52 / PR 53，共 105 包 | 复核既有发布报告及限定、上述全量接口/档案检查；针对新发现问题和 `84ef` 查回原始记录。不能把它写成此次重新完整精读全部 53 篇正文/SI 和全部日志 |
| hold | 4 篇、8 包 | 不在发布集合内；已有实质性缺口没有因 final 校验通过而自动消失 |
| verified_tasks | AR 0 / PR 0 | 本批已迁出，仅保留维护报告等文件 |

### 14.2 此前科学审查中仍然成立的判断

1. **作者路线验证可以使用作者终态或 TS。**验证的是当前科学对象/物理量存在有依据的成功计算，不要求验证 agent 当时遵守被评 agent 的信息受限探索。更换公开 starter 本身不使这条验证无效，也不自动要求再计算。
2. **给定结构性质任务不能被一概判为答案泄露。**用户批准的 d2d08、e31、d8e549、c23cf、80cc 保留给定对象/初态；其待求量是频率、相对能、光谱等。结构/TS 发现任务的待求终态则仍须留在 evaluator 私有侧。
3. **reference 是有效计算档案，不是新的评估标准。**评分仍以五个 evaluator JSON 为准；不能通过删掉未通过的关键点、改容差或给 reference 贴 PASS 标签解决任务问题。
4. **不能只看正常结束或文件名。**本轮直接检查的 92 个 `.log` 加 6 个 Multiwfn `.out` 均存在，与此前所称 98 份输出相符。EF 的三份 ADCH 原始表确有 P 电荷 −0.018993、0.447060、0.455684 e，三份 ESP 输出有完成的表面分析；旧 free/PO 进程结束异常与已经完成的科学产物在 reference 中有区别。Z1 旧组合日志中的失败 FC 没有替代另外的成功 FC。44f 两份 ORCA 频率表各有 261 个打印项，其中 6 个零模式、255 个正振动、0 个负模式，没有把平移/转动计为正振动。
5. **有限证据仍需限定。**6f 单构象不证明所有构象稳健性；b336 产品侧有限 IRC 不证明产品极小值；d796 四局部通道不等于完整循环；Z1 的相对突出谱峰比较不等于绝对脱附能/全谱；Cat1 采用真实最高 f 态，不能用固定 state22 代替；独立 starter 没有盲跑记录不应被宣传成已经盲测成功。第 13.2 节的逐篇边界继续有效。

因此，本轮没有发现第二个类似 7a“历史计算对象是错误异构体”的新批次问题；也没有确认本批新增了待求 TS/最终结果直接暴露的输入。这个结论不覆盖共享文件系统、联网检索和后台 API 的实际访问隔离。

### 14.3 确认漏检的任务问题：paper_2f302589e5e9e420，两模式

**位置：group_3；旧批次 final AR/PR 各一包。问题是公开输出约定与 evaluator 不一致，不是缺少历史计算。**

| 层 | 当前事实 |
|---|---|
| 两模式 task.md | 要求 EPI2-minus-EPI1 的带符号百分比变化 |
| 两模式 submission_schema.json | 必填 `percent_change_ePI2_vs_EPI1`，未声明 `percent_reduction_EPI2_vs_EPI1` |
| 两模式 scoring_rules.json，`r_result_percent` | 读取 `$.percent_reduction_EPI2_vs_EPI1`，目标为正值降幅 14.3%，容差 ±2 个百分点 |
| 原始 group_3/report/results.json | 两个字段均存在：signed change = −14.6106779595%，reduction = +14.6106779595%；偶极分别 2.223986032、1.899046595 D |

后果：遵守公开 schema 的 agent 可以只提交带符号的变化率，但评分所绑定的另一字段缺失。即使人工/LLM 可能补作换算，当前任务也不应依赖评委猜测；更不能把负的变化率直接与正的降幅比较后扣分。schema 默认允许额外字段，不代表 agent 已被告知必须提交那个额外字段。

此前为什么没发现：旧审查主要核对历史 results 是否包含评分字段，而这份历史结果恰好同时含两个字段；包校验器并不验证 `binding.fields` 是否在公开 schema 中声明。**“历史结果能通过”不能替代“按公开约定提交也能被正确评估”。**本轮对全部 137 包中绑定到 `report/results.json` 的 1,390 个字段引用展开 `$ref`、条件分支及数组声明后，仅此两包出现未声明字段；数组简写的另一兼容问题见下一节。

建议修法：保留原 signed-change 字段，公开补充 reduction 的定义和 schema 字段，明确

`signed_change = 100 × (mu_EPI2 − mu_EPI1) / mu_EPI1`

`reduction = 100 × (mu_EPI1 − mu_EPI2) / mu_EPI1 = −signed_change`。

不要取绝对值把极性增加也算成降低；失败/零分母时诚实报告不可用。让 evaluator 联合核对两个百分比与原始偶极的一致性，保留既有目标和容差。该修复不改变科学目标，也不需新量化计算。随后用已有两偶极和一个符号错误反例验证接口。**本轮仅报告，尚未实施。**

### 14.4 评分接口兼容问题：15 篇、28 包的数组简写

1,390 个字段引用中有 108 处使用 `$.molecules[].id` 一类 `[]` 简写。它们在逻辑上对应 schema 中的数组字段，不能当作 108 个缺数据问题；但当前两处实现使用了不同的解析约定：

- `scripts/audit_final_verified_tasks.py` 的 `json_path_exists` 明确接受 `[]` 与 `[*]`。
- `evaluation/scoring/evidence_reading.py` 的 `read_registered_evidence` 直接调用 `jsonpath_ng.parse`；实际离线解析 `$.molecules[].id` 抛出 `JsonPathParserError`，`$.molecules[*].id` 则正常。

这说明此前“审计字段可定位”没有覆盖实际证据读取器的兼容性。若 judge 原样请求这样的 selector，会读失败。多数复杂评分仍由语义判断完成，因此**不能夸大为 28 包必然无法评分，也不能声称这些字段已全部机器验证通过**。

受影响范围：

| 模式 | paper_id |
|---|---|
| AR、PR 均有 | `paper_0a62b797f51de2c0`、`paper_1b285cf9f763f2cf`、`paper_2f2aa11ea61a32bb`、`paper_3c058fa17fa7c54e`、`paper_430b9cbe83c2c203`、`paper_46a9ca0dab36dd9e`、`paper_86a0b654270a8ce7`、`paper_94b0a8ae694590ea`、`paper_b5c446c7067dd511`、`paper_d3b4575397179146`、`paper_d8e5490cd9942f4f`、`paper_db6c4e0558113873`、`paper_f9d09d28c7d9adaa` |
| 仅 AR | `paper_b33676a2051f5e91` |
| 仅 PR | `paper_d7967e22bb965daa` |

其中最近迁入批次涉及 4 篇、6 包：Cat1（46a9）和 La（d8e549）的两模式、b336 的 AR、d796 的 PR。其科学计算支持仍成立，但迁入时的字段逻辑检查没有证明这些简写可由新读取器原样执行。

建议在评分读取入口兼容该既有简写，或统一改为标准 `[*]`，并确保“多条结果、身份匹配、全部/任一”的科学语义仍由原规则明确，不因字符串替换改变评分。用一条和多条数组的离线证据读取检查即可，无需化学计算。此项属于规则与执行器的接口修复，未在本轮实施。

### 14.5 档案整理遗漏：两篇、四个 reference 链接及四项回归

涉及 `paper_1b285cf9f763f2cf`（group_5）和 `paper_534ae3b6e2fb695f`（group_6），均为两模式。其 `boundary_repair_evidence.json` 已按用户要求移到 `evaluation/task_provenance/`，但：

- 1b285 两份 reference 第 47 行、534 两份 reference 第 56 行仍链接 evaluation 根下的旧路径，共 **4 个真实文件断链**。
- `tests/test_three_boundary_repairs.py` 第 100、149 行仍读旧路径，两个论文各触发两项失败，共 **4 项测试失败**。

本轮直接读取新位置中的四份 JSON，重新从现存原始输出提取旧 `replay_*` 和 `release_*_details`：两篇两模式的科学内容均吻合，记录也明确没有新增量化计算。因此，这里不能报告成“验证结果遗失”或“论文未算通”；是文件整理之后未同步所有使用位置。

建议改 reference 链接和测试读取路径。发布时如果按用户意愿删除 `task_provenance/`，需先把 reference 仍依赖的有效计算步骤/必要结果摘要保留在 reference 或私有 `author_results/`，再去掉维护记录链接。无需保留整份修复历史，也不需重算。直接删除后仍保留指向它的计算证据链接，不符合“reference 记录可查”的目标。

全量 reference 解析还发现 5 篇、10 份文档的未加代码格式 SMILES 被 Markdown 解释成 38 个化学片段伪链接：`0de37…`、`2c439…`、`3235…`、`3a22…`、`430b9…`。这属于显示问题，不能计为 38 份原始文件缺失；可给相关 JSON/SMILES 加代码格式。与上述四个真实文件断链分开处理。

### 14.6 发布入口、版本与实际隔离仍需验收

**当前默认任务根会加载源任务，不是 final。**在项目正式 Python 环境中，`TASK_ROOTS` 实际为仓库 `tasks/`；`TaskRepository` 只扫描其下标准模式目录。直接初始化时，在 canonical `autonomous_research/paper_0bea8aa6bfd57e65` 因 evidence/manifest 等错误失败。该错误不在 final，不应据此误判 final 论文科学失败；但也说明不能直接用当前默认配置开始正式评估。应建立仅包含已选 final 版本的标准模式发布根并明确配置，确认 hold、canonical 和重复版本均不进入运行清单。

**工作区内容与 Git 发布版本尚未统一。**本轮检查时，final 路径仍有既有未提交修改，另有 57 个未跟踪文件，其中 12 个在 `author_results/`、45 个在 `task_provenance/`。这不影响本地存在性检查，却意味着只发某个旧 commit 不一定包含眼前审核过的文件布局。不要清理或整体暂存其他人的工作；发布前应由负责者定向保存选定任务版本。删除维护目录后按项目现有规则重建 manifest，再验证发布副本；manifest 包含维护文件，不能删完后沿用旧清单。本轮没有替用户提交这些既有变更。

**未发现包内泄露不等于部署隔离已经通过。**`materialize_agent_files` 只复制 `agent_input`；现行 prompt 构造没有直接注入论文标题/DOI，这两点成立。但 `load_public_task` 和 Web info API 仍能返回完整 `task_info`，运行设置也允许网络；本轮没有真实受限 agent 的父目录/绝对路径、共享挂载、后台 API 和论文检索访问测试。不能声称已经发生泄露，也不能仅凭提示词中的禁止条款保证不泄露。正式评估前须在实际部署中确认 agent 读不到 evaluator、reference、作者结构、论文/SI 和 group 输出。

**评分规则传入不等于科学评分行为已验证。**当前适配器保留完整规则及其结论关联；简单单数值检查与复杂语义判断分开。身份、条件适用性、正负号联合判定等复杂规则仍需 judge 解释。建议用已有成功结果及少量错误符号/错原子/错电子态反例检查最终评分行为，不能把离线 mock judge 或 JSON 校验称为真实科学评分已验收。这是评分运行检查，不是重新进行量化验证。

### 14.7 既有科学限定和 hold 清单不变

`paper_84efbea3ab8e6e20` 两模式仍在 final；当前 evaluator 允许有证据的替代解释。原始分子计算/SOC/三重态后处理支持该范围，但不支持“作者 CZ2B/T4-HLCT 特定解释已经复现”的发布用语。它的历史 results 使用 `bounded_failure` 也不能单独推导出当前允许 alternative 的任务不可算；应按实际对象、证据和当前规则判断。此次回读 reference、task 和 evaluator 后，继续保留这项限定，不擅改目标或要求补算。

以下 **4 篇、8 包仍在 hold**，不因本轮报告自动恢复：

| 论文 / group | 保留的实质性缺口 |
|---|---|
| `paper_6492e1e5d38d23ae` / group_5 | 功函数的表面/终止模型边界及现有主分支与数值规则的对齐尚未解决 |
| `paper_8b7bf002cc6a4ba9` / group_5 | 现有显式水链的几何收敛/化学身份不足以支持指定优选构象，不能用后续成功单点补救失败前驱 |
| `paper_b815e2622b0d6085` / group_6 | 第二网格缺少独立投影/波函数，不能仅按 band ordinal 证明同一框架态的稳定性 |
| `paper_a3968806251093cd` / group_2 | 已检查的历史 7a 几何属于错误位置异构体；正常终止不使其成为正确对象验证 |

前三篇的已有交接见 [HOLD_VERIFICATION_HANDOFF.md](../HOLD_VERIFICATION_HANDOFF.md)，7a 见本报告第 10.3、11 节。本轮没有重新全面审查 hold 的后续新进展，不把旧缺口判断冒充新计算结论。

### 14.8 测试记录与此前结论应如何表述

审查期间公共评分代码有并行提交；最后一轮相关回归运行于 `5462cba4` 代码及当时工作区。任务批次提交仍为 `689ef73b`，不能把它理解成当前所有旧 final 整理都已提交。

- 全部 **137/137** final 包结构/manifest、必需输入路径、evaluation 根布局和 reference 存在性通过；这一校验不会发现科学错误、未声明评分字段或 reference 中的断链。
- 11 个相关测试文件共 **168 passed、4 failed（30.94s）**。失败全部是第 14.5 节的旧档案路径；不能再写成全量回归无失败。
- 新评分请求/续评协议的 `tests/test_judging.py`：**7 passed（1.72s）**，使用离线 fixture，没有真实 LLM 科学判分。
- 因使用 base Python 曾出现 `jsonpath_ng` 缺依赖；项目文档指定的 `.envs/researchchembench/bin/python` 已具备 `jsonpath_ng` 和 `ijson`。以上结果均用正式项目环境取得。**不把 base 环境误用当作正式项目缺依赖或任务失败。**

可复查的回归命令：

```bash
.envs/researchchembench/bin/python -m pytest \
  tests/test_task_package_v19.py tests/test_staged_repairs_20260916.py \
  tests/test_remaining_final_task_repairs.py tests/test_final_release_remediation.py \
  tests/test_three_boundary_repairs.py tests/test_agent_geometry_audit.py \
  tests/test_scoring_rules.py tests/test_evidence_reading.py \
  tests/test_evidence_archive.py tests/test_agent_events.py tests/test_rescore_archive.py -q
.envs/researchchembench/bin/python -m pytest tests/test_judging.py -q
```

此前第 13 节关于本批的原始成功输出和条件迁移有依据；其测试结果也是对应版本/范围的真实记录。但它没有覆盖旧批次的百分比字段冲突、文件整理后所有引用者，以及审计解析器与新评分读取器的语法差异。**如果把那些记录概括成“137 个任务全部科学与运行端到端验收完成”，就是过度结论，应以本节校正。**

### 14.9 建议完成的最小收尾

1. 修复 `2f302` 两包的 signed-change/reduction 公开约定与绑定；不改科学目标/数值标准，不补算。
2. 统一数组 selector 在任务审计和实际评分读取中的解析，验证数组多项身份匹配；不改评分科学含义。
3. 修复两篇四个 reference 链接及测试路径；保留有效计算摘要后，维护记录仍可按用户计划删除；顺手处理 SMILES 显示问题。
4. 在正式环境中固定选定任务/评分版本，建立仅指向 final 的发布根，复跑受影响回归及发布清单检查。
5. 确认真实运行访问隔离，并对代表性现有结果/错误反例做评分检查；发布说明保留 `84ef` 及有限构象、有限 IRC、相对谱等边界。

这些新发现的收尾问题没有提出新增量化计算的必要性。完成后可据对应验收证据判断发布；当前应称“有历史科学验证支持的发布候选，仍有明确接口/档案及部署验收事项”，不应给出“已保证所有任务无问题”的承诺。本轮只提交分析报告，未实施上述修复。

## 15. 2026-09-23 当前暂存批次：审查与待确认修复方案

### 15.1 范围、授权和计划

本批实际为 **15 篇论文、29 个任务包（AR 14、PR 15）**，与前文历史 18 篇批次不同。全部任务仍在 `tasks/verified_tasks`；`paper_ffa556cc3acdf0bc` 只有 PR，缺 AR 本身不是缺陷。

按负责人确认的 [2026-09-23 维护流程](../../docs/verification/final_verified_tasks/final_verified_task_maintenance_workflow.md)，先核实当前问题并给出逐篇方案；未获具体修法确认前，不改任务、输入、schema、evaluator 或 reference，不自动迁移或新增计算。论文/SI、原 group 及 runs 验证产物均只读。本轮不重复审查既有 final/hold 全部任务，不统计自主科研能力类别。

修复前 Git 基线已保存为 **`6756212e`**，仅收录本批两个模式目录中的 365 个既有文件；未夹带原有 MAINTENANCE_REPORT、流程文档或其他工作区改动。提交成功，但仓库 pre-commit 提示 `sbin/copyright` 不存在；该提示不是科学/软件测试通过记录，未擅改 hook。

执行计划：盘点和保存基线 → 逐论文/模式读取题面、输入、schema、五个评分文件和 reference → 对照正文/SI及当前成功计算证据 → 区分确定问题、需补档和待科学决策 → 汇报修法与验收标准 → 获批后在暂存区实施及复查 → 另等迁移确认。

### 15.2 已确认的共性问题（不等于化学计算失败）

1. 29 个包的 `validate_task_package` 均只报告 `manifest_entries_mismatch`、`package_content_hash_mismatch`。进一步逐项比较确认：每个清单都只漏列 `evaluation/verified_computation_reference.md`，其余已列文件没有缺失或内容变动；不是发现了 29 处不明数据损坏。当前不能通过正式包加载校验；获批修复文件后应逐包刷新现有清单并复验，不能用新 hash 代替科学验收。
2. 15 个 PR 题面均未将已有作者假设/指导分离为 `Author-provided scientific guidance` 章节；8d894、9455 两模式采用二级标题，其余采用一级标题。应统一版式并保留模式差异，不能借排版公开作者答案。
3. 本批 29 份 `verified_computation_reference.md` 均只有 9 行摘要，缺按步骤的输入/输出定位、关键参数与依赖关系、各必评量的完整证据对应。必须从已经成功的原始记录补档，不能再写一句“all rules supported”替代核对，也不需为补文档重跑计算。
4. 35a674、3d1d9 两模式合计 18 个 JSONPath 选择器采用 `[]` 简写，实际 `jsonpath_ng.parse` 不接受。改为受支持写法并测试完整数组语义、对象/态绑定；不能改成只取首元素。
5. 628af8、8d894、c28b0、c72179 两模式共 8 条独立 limitation 结论仍参与设计；更多包在 required、规则或关键点中保留普通免责声明。须逐项分离真实科学条件与纯表态要求，再清理关联，不整条批量删除混合科学规则。当前 29 包均未显式选择 `dual_axis_100.scientific_results.v1`，需同步审查实际策略。

本批审查使用 `provenance-review` 区分原始证据/归档陈述/尚未核实，并按 `research-lit` 的本地论文阅读方式回查正文/SI；没有扩展外部文献检索。下面逐篇记录具体依据、验证支持范围和拟修改文件；第 15.4–15.7 节汇总计数、实际检查、批准事项和本轮停点。

### 15.3 逐篇证据与修复方案

以下路径默认相对于仓库根；AR/PR 各自的任务、schema 和评分都需同步核对。暂不以“已验证”目录名或旧报告标签做发布承诺。

#### Group 1 — paper_43d74f8a469d9ad3（AR、PR）

**当前目标与依据：**从实验 CCDC 2441197 单分子结构研究芳基–B 键的刚性旋转能量曲线，不是复现论文全部光稳定性实验。正文 PDF p7 的晶体结构及 p11 的 PBE0/def2-SVP 旋转扫描与当前子目标相符。公开 CIF 是实验起点，不能仅因其中有坐标就判为优化答案泄露。

**确定问题：**两模式 `agent_input/data/inputs/ccdc_record.json:scan_object` 让四原子二面角由 B、ipso C 和两个相邻芳环 C 组成；这样的描述没有提供 B 侧邻原子，不能清楚定义以 B–ipso C 为中轴的连续四原子扭角。实际验证采用 N1–B1–C1–C2（结构索引 2,4,3,6），与错误文字不同。题面同时含停止/局限性模板；不得把没写免责声明当成科学失败。现有 reference 未列完整扫描证据。

**验证覆盖：**`docs/verification/group_1/paper_43d74f8a469d9ad3/report/results.json`、`artifacts/absolute_torsion_profile_20260916.json` 及 `provenance/torsion_current_contract_audit_20260921.json` 记录基态极小值（48 原子、138 个正振动频率）、0–345° 每 15° 的 24 个刚性单点及几何旋转检查，能垒 18.266546 kJ/mol。0/360° 的几何闭合与 E(345°)=E(0°) 不是一回事，不要求最后一个采样点和首点能量相等。它支持两模式的 `*_process_identity`、`*_process_coverage`、`*_result_profile` 和 `*_result_interpretation`，不证明动力学速率或另一化合物的完整对比。

**修法：**统一 task 格式；在 task/ccdc_record 中写清“B 侧邻原子–B–ipso C–芳环相邻原子”及整支芳基刚性旋转，提供合法原子标号约定，不公开能垒/最低角度。schema 保留真实失败诊断及已计算点，取消普通免责声明门槛；核对完整曲线两数组等长、4 原子定义及扫描点身份。reference 补基态→24 点→相对能量→周期性处理的实际链。不新增数值 gold，不改变现有科学目标，无需据此提出重算。

#### Group 1 — paper_9455a82229de2427（AR、PR）

**当前目标与依据：**SiN + isoprene 的 H 脱除产物身份及能量兼容性。正文 PDF p3 方法、p4 实验反应能 −162±27 kJ/mol、p5 两种环状产物；SI 产物/能量表支持现有私有参考。公开输入只有反应物和组成，未给出目标产物坐标。

**确定问题：**AR 明说不公开实验放热窗口，却要求逐候选比较该窗口，`ar_rule_energy` 也要求这个比较；其 `reactants.json` 只有碰撞能 25±1 kJ/mol，不能替代反应能。PR 已提供正确实验窗口，不存在此项缺失。AR `submission_schema.json` 的 `oneOf` 错放在 `result_schema.properties`，`jsonschema` 的 metaschema 检查直接失败；不是单纯风格问题。两模式还要求普通 limitations。反应能公式应明确包含脱出的 H，不能只用产物减两反应物。

**验证覆盖：**`docs/verification/group_1/paper_9455a82229de2427/provenance/independent_cbs_raw_audit_20260918.json` 和 `independent_cbs_closure_audit_20260918.json` 指向两种独立生成的 14 原子中性单重态产物、SiN/isoprene/H 的真实 CBS-QB3 计算；两产物各 36 个正振动模。`E0(product)+E0(H)−E0(SiN)−E0(isoprene)` 得 −156.453523 / −150.522520 kJ/mol，均落在实验区间。支持当前产物极小值、身份、兼容性和最终结论；不是 TS/IRC、完整 PES 或分支比验证，这些也不应临时加入当前任务。

**建议决定与修法：**推荐把 PR 已有的**实验观测窗口**同样作为 AR 公共数据，它不是作者算出的产物答案；保留产物结构和计算能量私有。替代方案是改为 evaluator 独立比较、agent 不负责未知观测，但会改变比较职责，因此不擅自采用。修正 AR schema 层级并分别测试完整/部分/失败提交；明确 0 K/ZPE 及 H 参考口径、删除纯免责声明、补完整 reference。目标、产物参考和容差不变；修输入和接口不需新量化计算。

#### Group 2 — paper_35a6749f3bae345b（AR、PR）

**当前目标与依据：**计算 DBC-Ph/DBC-Nap 的 S0/S1 几何扭转、跃迁和轨道解释，非“直接读取给定几何的性质”任务。正文 PDF p3 方法/p6 扭转解释，SI S11–S14 的跃迁与轨道、S22 Table S15 和 S24 Table S17 的优化坐标为主要依据。

**确定泄露：**公开 `dbc_ph_s0.xyz` 的全部 54 个原子坐标与 SI Table S15 数值一致；`dbc_nap_s0.xyz` 的 60 个原子坐标与 Table S17 相同，只重排了原子顺序。本轮实际比较完整坐标集合，不只依据文件注释判断。两份都是 SI 标明的 S0 fully optimized geometry，直接暴露本题待优化并比较的部分结构结果；两模式都受影响。另 `system_definition.json` 用一个 `source_formula=C32H21N` 概括两分子，需分别写 DBC-Ph C32H21N、DBC-Nap C36H23N；两模式合计 10 个 `molecules[]` 选择器不被现有 JSONPath 解析器接受。

**验证覆盖：**`docs/verification/group_2/paper_35a6749f3bae345b/report/results.json` 含四个真实 Opt/Freq 端点（Ph S0/S1 各 156、Nap S0/S1 各 174 个振动模）、S0 TD10 与 S1 计算、两条扭角和轨道分析；最新 Nap S1 是 `author_DBC_Nap_SI_S18_S1_checked_root_optfreq_20260921`，不可复用旧未闭合分支。Ph S1 412.06 nm 与 SI 441.44 nm 不完全相同；当前 evaluator 为扭转/电子结构的语义比较，不是该波长的数值硬门槛，不能声称逐项数值完全复现，也不应据此擅改 gold。

最新态分析还显示：S0 的 Ph/Nap 平面扭转约 64.68°/64.88°，S1 分别约 54.69°/81.69°。因此不能要求“两个分子的两个态一律 moderate twist”；现有 `r2/ar2` 允许根据逐分子证据支持或限定该解释，但 key point/结论摘要过于笼统。建议明确分别评价分子和电子态，并保留根据结果修正定性解释的空间，不把近正交的 Nap S1 改写成中等扭转，也不新增波长或固定 CT 百分比硬评分。

**待批准修法：**保留两分子的连接性、立体/电子态、溶剂及原子映射，以不以作者终态为模板的独立构建初始结构替换两份公开优化坐标；作者结构如需保留转到本包 `evaluation/author_results/`。不改成固定结构任务，不以小扰动或改注释冒充消除泄露。同步原子索引/扭角定义与两分子 formula；将 `[]` 改为 `[*]`，测试两对象、两态及全部跃迁而非只取第一项；清理 limitation，reference 写四端点及最新选态证据。作者路线验证继续有效，不把不同 starter 当作必须重新验证的理由，也不声称完成了新 starter 的盲测回放。

#### Group 2 — paper_c7217910ecbee1d9（AR、PR）

**当前目标与依据：**孤立 PAl12[B(C6F5)3]2 的绝热电子亲和能和金属核框架保留，不是整篇 graphene/AIMD/全部超原子轨道研究。正文 PDF pp2–4 与本地 `supplementary_001.docx` 的 Computational details 支持 PBE0/def2-SVP、不同位点/自旋、频率及 ZPE。公开组成/拓扑没有提供优化终态或 AEA 数值。

**确定问题：**`*_result_framework` 有规则但未关联任何最终结论，现行运行端将其标为 standalone；不能说完全不评，却需明确结构结果的成果评分职责。两模式 `*_limit_claim` 是单独得分的 limitation，删除时不能同时丢掉真实覆盖、端点验证和能量定义。PR “charge-1”应明确排成 charge −1，避免读成 +1。`metal-core/superatomic framework` 应按现有 expected 的“结构保留”解释，不能要求未计算的电子壳层证明。

**验证覆盖：**`docs/verification/group_2/paper_c7217910ecbee1d9/provenance/final_closure_20260919/independent_results.json` 和 `report/results.json` 有 2 位点×2 电荷×2 自旋共 8 个真实 Opt/Freq（各 237 个正振动模）。所选中性 doublet/阴离子 singlet 电子 AEA=3.945536 eV，加 ZPE 后 3.959169 eV，对 3.93±0.30 eV；两端金属核及配体连接保持。非优选候选中的接触脱离没有被当作合格 endpoint。有限作者路线计算足以支撑现有子任务，不等于已证明数学全局最小。

**修法：**统一格式和 −1 文字、明确能量/ZPE 记录；移除普通 limitation 结论及声明要求，将真实框架结果关联到主科学结论，保留身份/频率/位点自旋数据。reference 记录独立构建→8 端点→按电荷选最低→AEA/ZPE→框架检查；保留失败历史于原目录而不混进成功链。目标及数值不变，无需新增计算；关联变更和 limitation 清理随本批方案批准后执行。

#### Group 4 — paper_628af8d0bf0a1bfe（AR、PR）

**当前目标与依据：**4a/4c 中央 pentalene 的 NICS(1.7)zz 比较；正文 PDF p5 Fig.5、SI S14 的方法和 Table S11/S13 的对象（SI PDF pp51/53）支持该子问题。公开为完整化学名称/取代基，不含优化结构或 NICS 答案。

**确定问题与边界：**两模式各有一条单独 limitation 结论，相关规则同时承载真实敏感性检查，不能整条抹掉。正文标 NICS 方法为 M06-2X/6-31++G(2d,p)，SI S14 写 6-311+G(2d,p)，确有源内基组标签差异；历史验证沿 SI，不应把差异归因于 agent 或静默要求唯一未公开协议。公开定义已说明两环均值与负屏蔽号，不能重复报成“完全没定义 NICS”。

**验证覆盖：**`docs/verification/group_4/paper_628af8d0bf0a1bfe/report/results.json` 及 `provenance/corrected_nics_results_20260916/results.json` 记录完整 4a/4c 的 M06-2X/6-31++G(d) Opt/Freq（186/174 个正振动模）、SI 基组的 ghost-point shielding。均值 23.1738/19.1577 ppm，对私有 23.6/19.2±2 ppm；实际张量投影换为各环法向的控制给 23.171769/19.159065 ppm，排序不变。已读四个计算日志的正常结束与两个完整频率块。该控制是**轴定义敏感性**，不等于做过新基组或另一侧探针计算。

**修法：**保留两环/共同核心平面/1.7 Å/负张量投影及均值，补上可复核的原子选择和坐标旋转等价定义；删除纯 limitation 结论，将有效几何/敏感性规则接到 NICS 比较的科学职责。PR guidance 可列真实 SI 路线；AR 不因归档需要被强制照抄作者方法。reference 明写两种来源标签及实际采用者。建议认可“沿 SI 的已验证路线作为私有参考链，其他允许方法仍依原规则评价”，不冒充作者勘误、不改数值/容差。若要统一两模式为唯一基组，则需另外明确批准，当前不据此要求重算。

#### Group 4 — paper_80441aced6051d86（AR、PR）

**当前目标与依据：**G1 单体扭转及二聚体堆积几何。正文 PDF p3 给 B3LYP-D3/6-31G(d)、PCM water，p4/Fig.4 给几何描述。`papers/` 本地只有正文；本轮额外读了 group 缓存的 SI 原文转录 `provenance/recovery27_20260915/sources/1-s2.0-S0143720825008265-mmc1.txt`，Section D/S13 起、Table S2 后明确写 Cartesian coordinates of **optimized** monomer/dimer，不把缓存转录冒充重新读取了 SI 原件。

**确定泄露及档案错误：**公开 `g1_monomer.xyz` 64 原子和 `g1_dimer.xyz` 128 原子均与缓存 SI 优化坐标完整逐原子数值匹配；而任务要确定的就是这些单体/堆积几何。所谓“starting only”不消除泄露。reference 把 32.4094°写作 dimer twist，实际是**单体 pyridinium–naphthalene 两角均值**。题面对溶剂/方法开放，但私有紧容差来自水模型，需明确主比较介质，不能默认任何介质结果都该匹配。AR 目标预先说 twisted/offset 的措辞也应改为中立提问，PR 可保留待检验假设。schema 在失败分支仍要求整数 `imaginary_frequency_count`，未完成频率时不能如实填 null；且同一系统成功字段加失败记录可能同时匹配两个 oneOf 分支。

**验证覆盖：**`docs/verification/group_4/paper_80441aced6051d86/report/results.json`、`provenance/conclusion_reaudit_20260921.json` 及其两个日志支持 186/378 个正振动模；二聚体原日志明确有 `Optimization completed on the basis of negligible forces` 和 `Stationary point found`，不是仅有单点成功。单体两种均角 51.977518°/32.409382°；二聚体平面间距 3.778995 Å、滑移角 44.901541°，均满足现有容差。完整质心距离是 5.353514 Å，不能拿它对 3.63 Å 评分；当前 task/evaluator 已区分，不再改回旧错误定义。

**待批准修法：**按原有 C34H28N2(+2)/两单体(+4) 化学身份独立生成中立单体初始构象和非答案式二聚体起始配置，或给完整映射的结构图让 agent 组装；不能保留 SI 二聚体位置关系或用其小扰动。旧终态仅放私有 author_results。推荐公开水介质作为主比较条件，方法自由度不另收窄；修 schema 的状态/未知频率与额外尝试记录；修 reference 的量归属，补优化→频率→平面/角度后处理。不新增 SOC/光谱/聚集自由能任务，不需因 starter 替换重跑作者路线。迁移前建议补存 SI 原件或可定位原件来源，增强来源可复核性。

#### Group 4 — paper_a21b91f97ce3c68f（AR、PR）

**当前目标与依据：**给定 axial 1a 的三个 Sn–butyl C 单键耦合及带符号均值。SI S2 的几何/NMR 方法、S5 的 −217 Hz 行、S10–S11 的 1a 坐标支持；不是重做 77 个骨架、axial/equatorial 全部比较或证明超共轭因果。该包已有给定构象性质范围，公开坐标本身不等于待求 J 答案，本轮不建议一律删除。

**问题：**主要是 limitation/固定重试措辞及 reference 不完整；`TZP-ZORA` 在实际 Gaussian 输入中是基组名称，不能在档案中杜撰一个未使用的 ZORA Hamiltonian。保留公开 Sn=1、butyl C=2/3/7 的映射和完整 signed J 定义；未计算的 anomeric C 不计为缺目标。

**验证覆盖：**`docs/verification/group_4/paper_a21b91f97ce3c68f/provenance/sn_coupling_closure_20260918.json` 记录 62 原子、180 个正振动模的真实优化频率，匹配同几何的 B3LYP-GD3/TZP-ZORA、Mixed/ReadAtoms/NoXCTest NMR。三个全贡献 J 为 −249.688、−223.744、−205.060 Hz，均值 −226.164 Hz，对 −217±15 Hz。closure 还区分 FC/SD/PSO/DSO 和原子同位素；不是取绝对值、只取 FC 或套用论文实验缩放因子得到通过。

**修法：**保留固定对象、三个键和 raw signed mean，统一格式；删纯免责声明及“一次恢复尝试”等模板门槛，保留具体失败原因。reference 逐步列基态检查→NMR 输入/同位素→总 J 取值→均值，不误写未做的 CREST/NBO/其他异构体。无需新增量化计算，也不新增单构象任务没有要求的构象发现能力。

#### Group 4 — paper_c28b0a1c549f4575（AR、PR）

**当前目标与依据：**三种离子–PC 孤立对的电子结合能及 DED2+ 对 TEA+ 的相对结合趋势。正文 PDF pp3–4/Fig.2d–f 支持；公开图/SMILES、电荷及能量方程足以构建，未给优化复合物或结合能答案。此次本地 `papers/` 未有 SI 原件，SI §5 的方法出处还依赖 group 的源记录，不能说已独立读遍全部 SI。

**问题：**两模式的独立 limitation 结论会给普通边界说明计分；AR `ar_kp_scope` 亦为纯边界表态，不是新的计算发现，应去除其独立成果职责。`r3` 将 bounded failure 的诚实覆盖写进结果排序条款，易把“如实未得到排序”与“已算出正确排序”混淆；应明确未算出的结果不得给成果分，而过程分按真实工作评价。两种主张不能只改字段名继续扣免责声明分。

**验证覆盖：**`docs/verification/group_4/paper_c28b0a1c549f4575/report/results.json`、`provenance/binding_progress_20260916/results.json` 有 4 单体及 6 复合物的有效 Opt/Freq→匹配单点链；六复合物日志均有全频率且无负模，能量来自共同的 B3LYP/6-311+G(2d,p) 层次。最强代表 DED2_PC/TEA_PC/BF4_PC 的结合能为 −30.088727/−13.187403/−16.540811 kcal/mol；多起始取向及已有敏感性证据支持现行相对结论。没有用孤立对能量证明宏观电极表现。

**修法：**统一方程与“越负越强”的解释；保留三对身份、实际取向/去重记录、极小值、共同单体零点和已要求的敏感性，不把它们当作 limitation 一并删除。去掉两条普通 limitation 结论和 AR 纯 scope 得分；结果/过程失败分支分别说明。reference 补每个复合物对应前驱和配套单体，不把旧失败几何拼到成功 SP 前。原目标和排序不变，无需因此重算；SI 原件的来源存证与任务计算缺输入是两件事。

#### Group 4 — paper_e0791c047a731974（AR、PR）

**当前目标与依据：**Cy2 的垂直 S1/T1/T2 与弛豫 T1 能量。正文 PDF p5、SI S7 方法/S12 Table S3/S24 基组标注支持 B3LYP、CHNO 6-31G(d,p)/Se def2TZVP、SMD chloroform。公开为给定 Cy2 的 S0 起始几何，最终目标是激发态能量而非发现 Cy2 连接性；没有给 T1 终态或能量，不能与上述结构发现泄露混为一谈。

**需澄清：**题面需要更明确地区分同一 S0 几何的垂直量和两态优化几何的绝热**电子**能差，以及比较式中的 T1 取哪一类能量；不把 ZPE/G 或 T1 几何上的基态 SCF 能混进原定 1.09 eV 目标。PR 最终结论的 SOC/ISC 原文背景容易被读成未公开的必算目标，应把成果验收聚焦现有能量条件，不删真实科学结论，也不额外要求 SOC 计算。普通 method limitations 不再单独计分。

**验证覆盖与方法差异：**`docs/verification/group_4/paper_e0791c047a731974/report/results.json` 的四份原日志支持 S0/T1 各 180 个正振动模、S0 上的 singlet/triplet TD 根及 TD triplet Root1 弛豫；1.8909/1.0555/2.1220 eV 与绝热 1.010301 eV 在原 0.15 eV 容差内。`2*T1_vertical−S1=0.2201 eV`、`T2−S1=0.2311 eV`。正文 PDF p6 明确将作者的 1.09 eV 绝热 T1 归于 UDFT；本地原始链则是 singlet-reference TD triplet，不是另做 unrestricted triplet determinant。因此可记作**当前开放方法的能量子任务已有独立计算支持**，不能记作“按相同 UDFT 方法逐项复现作者”。两模式当前均允许自选方法，此差异本身不证明任务失败；但若以后把 UDFT 指定为唯一必用方法，现有这条 TD 链不能证明该新增要求已经验证。

**修法：**task/schema 给统一能量零点、电子/热能区分及主比较式；PR guidance 与成果评分分别表述假设和实际检验量；保持原态/数值/容差，清理免责声明，补 S0→TD→T1 opt/freq→能差链。给定 S0 坐标保留，不以“没有 SOC”否定已经验证的能量子任务。

#### Group 4 — paper_ffa556cc3acdf0bc（仅 PR）

**当前目标与依据：**在两个指定相对构型候选之间，用 30 个实验 13C 位移作量化/统计区分。正文 PDF pp2–3/Fig.1–2、SI `supplementary_002.pdf` S4 Table S1/S5 Table S2、S12 方法、S26–S32 候选构象支持。给定两组候选几何是现有比较任务的合法对象，不应因来源为 SI 就删除；公开没有 DP4+ 获胜概率或计算位移。

**确定必要信息缺失：**`input_manifest.json` 只说自行将 XYZ 原子对应到 C-1、C-3a 等 30 个实验标签；四份 XYZ 仅含元素/坐标，公开包无带这些标签的连接图或映射。分子连接性可从坐标推导，但任意论文编号和成对甲基的图示立体标签不能由元素序列唯一推出。真实验证专门使用正文 Fig.1 的图/楔键建立映射（`provenance/carbon_mapping_20260918/result.json`），这份必要非答案信息还在私有侧。盲目按 XYZ 前 30 个 C 或按位移最贴合去配对都不正确。

**验证覆盖：**`docs/verification/group_4/paper_ffa556cc3acdf0bc/provenance/nmr_subproblem_closure_20260918.json` 与 `carbon_mapping_20260918/{nmr_results,dp4_results}.json` 对两候选各 2 构象完成 M06-2X-D3/def2-SVP 筛选、B3LYP/6-31G(d) 优化频率和 mPW1PW91/6-311G(d,p)/PCM NMR；本轮读取 12 份主链日志，8 个优化/频率均 237 个正振动模，4 个 NMR 正常结束。真实 Student-t DP4+ 对 8S*,9aR*,12aR* 得 99.999956799%，E/G 权重控制均保持同一胜者。不是用 R² 冒充 DP4+；题面允许有依据的其他统计法，不应反向强制唯一算法。

**修法：**补四个输入构象各自的稳定 atom-index→实验标签映射及必要相对构型图示约定，只发布身份信息，不发布 shielding/权重/概率/胜者。保留两候选同口径比较、归一化概率和真实方法证据，取消普通 limitations 必填。reference 写清映射→4 构象计算→加权/屏蔽转位移→两候选统计，而非只记最终百分比。只需已有数据提取与契约修复，无需重跑整套 NMR。

#### Group 5 — paper_3d1d9b7f6df049da（AR、PR）

**当前目标与依据：**给定 Ih/D5h 两种 96 原子中性 doublet 几何，计算/识别 Y2 横向低频模式并讨论弛豫趋势。SI S2 的 PBE/def2-TZVP 与 Y 的 Dolg ECP、S16–S19 模式/坐标以及正文的模式–弛豫讨论支持；当前任务已明确 fixed geometry，不要求重新优化，也不要求数值计算 T1。

**问题：**两模式各 4 个 `modes[]` 选择器非法。模式频率结果绑定最终结论，但 `kp_input`/`kp_assign` 为 standalone，应明确它们是同一组频率获得成果分的有效性前提；不得仅挑最接近 gold 的四个频率。公开“substantial Y2 lateral”有物理含义，但不同软件模式混合时操作定义较宽，可给质量加权 Y 参与率/相对 Y–Y 轴横向分量的报告公式，不秘密把历史的 0.5/0.8 阈值当唯一标准。两个结论 `c_trend`、`c_relax` 都有科学内容，**不能把含 with limitations 的整条 `c_relax` 删除**。

**验证覆盖：**采用最新 `runs/hold_verification/group_5/closure_20260921/paper_3d1d9b7f6df049da/report/results.json`，不是旧不全的 group 摘要。本轮直接读两个主 Hessian：各 288 项，6 个平动/转动零模、282 正模、无负频；日志正常，固定几何并无新增 Opt 声称。按位移身份先选模式，Ih 38.569422/44.952490/56.192315/60.850646 cm⁻¹，D5h 66.703314/73.094561/82.391991/87.430579 cm⁻¹，均满足现有逐项 ±12 cm⁻¹，D5h 平均高 27.263893 cm⁻¹。支持频率与定性弛豫解释，不是独立算出实际 T1。

**修法：**保留两份合法给定结构，明确模式判据及物理身份优先、排序仅用于配对；修合法 JSONPath，接回模式身份检查，删除纯免责声明而保留两项科学结论。reference 补固定几何/Hessian→模式向量→预先定义的横向筛选→逐项比较，不误写“优化全局最低构象”。无需新增量化计算；若要强制具体阈值，先另行批准，不在格式修复中加入。

#### Group 5 — paper_3deba7268b769ce6（AR、PR）

**当前目标与依据：**正确 Dye3 phenolate 的最低可见单重激发能及 ICT 性质。正文 PDF p2 Scheme/Fig.1、p4 Fig.5 与 59.44 kcal/mol 理论结果、p5 §4.4 方法支持。当前公开 SMILES 是含 nitrothiophene 的 C17H11N2O3S−、**34 原子**、E-imine、−1/单重态；不是旧 37 原子 Dye4。SI S5 实验表也恰有 59.44，但在别的染料/溶剂行；当前理论 target 的正确依据是正文 p4，不能误引该实验格。

**本轮判断：**未发现当前输入仍有旧身份错误、优化坐标泄露或遗漏显式溶剂参数（ε=9.08、n=1.424 已公开）。需清理 task/结论/AR critical failure 中的 limitation/停止表态门槛。建议把“lowest visible”的操作选择说明清楚：先按能量/光谱区域和跃迁证据识别，不按接近 gold 选根；不新增“粒子 NTO 必须超过 50% 位于受体”的隐藏要求。这里是清晰度建议，不宣称现有 S1/S2 无法区分。

**验证覆盖：**`runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/report/supplementary_verification.md`、对应 results 和原生 NTO 分析完整；r2SCAN-3c 优化、102 个频率条目中的 96 个正振动模→ω-B97X-D4/def2-TZVP 完整响应 TDDFT 的 10 根/NTO。最低 S1=2.471173 eV=56.986603 kcal/mol、501.7 nm，S2 在 356.1 nm；与 59.44±3 的差 2.453397。NTO 支持 donor→acceptor 且有 bridge 离域（粒子桥布居约 0.483、受体约 0.369）。本轮回读主 Opt/Freq、TD 两份日志；未发现需要用错误 Dye4 结果兜底的情况。

**修法：**保留正确当前 SMILES/电荷/溶剂、既有 CT 证据接受规则及数值目标；整理 PR guidance、去普通 limitation，reference 明确五个 MMFF 初猜中只有一个进入有效量化链，逐根保留选态依据，不写“五个 DFT 极小值”。修法主要是格式/档案，不需补算。若要求固定可见窗口数值或亮态阈值，先确认；本方案不擅加此类新筛选门槛。

#### Group 5 — paper_8d8940710de08f7f（AR、PR）

**当前目标与依据：**两分子各 V+/V−/Z 三种中性构象的相对 Gibbs 能和稳定性解释。正文 PDF p5 §2.8 方法、p9–10 构象讨论及 SI S8 Table S8 起的几何/能量支持；公开只有身份与扭转区域，没有优化坐标/能序。Z 已涵盖 ±180°两侧，不能再误报成缺负角。

**确定科学边界问题：**task/`systems.json` 要 Gibbs 比较，却未指定用于主比较的介质、温压与热校正口径。SI 表题确写 in vacuo，正文写 CPCM 并列甲醇等溶剂；当前成功链是甲醇。这个差异不能靠改参考摘要或默认 gas phase 解决。两模式各有一条纯 limitation 结论；PR 氢键解释 `kp_pr_result_hbond` 是 standalone，AR 的结构解释只连在 limitation 结论，删除前必须重新接回科学结果。现有数值规则一个 2.57±0.8 值绑定所有六态，虽 comparison 写了 molecule-specific Z-minus-lowest，仍宜按系统/态清楚表达，而非对 V± 的 0 值也套同一 target。

**验证覆盖：**最新 `runs/hold_verification/group_5/closure_20260918/paper_8d8940710de08f7f/report/results.json` 的六份日志均正常 Opt/Freq，298.15 K/1 atm/quasi-RRHO。SNaft Z−最低=2.638125、SAntr=2.763389 kcal/mol，两 V 间隙 0.227309/0.210636；支持当前排序与容差。六源几何的既有真空/甲醇 SP 对照显示甲醇绝对能量与源表在 4×10⁻8 Eh 内，而真空差约 0.029–0.032 Eh；这支持“SI 介质表题可能误标”的推断，但不是作者正式勘误。不能把旧 group 中真空六态与新甲醇结果拼接。

**待批准修法：**推荐在两模式公开明确**中性单体、甲醇连续介质、298.15 K/1 atm、主比较的 G 校正口径**，把这是根据正文及配对验证作的 benchmark 解释写在私有档案；保留原分子、六态、排序、target 和容差。PR 给作者的定性氢键假设，AR 不预告 V 胜出。清理 limitation 后保留真实最低点/相对能/相互作用证据，修数值对象绑定，补六态成功 reference。若负责人坚持按 SI 字面真空定义，则现有甲醇链不能证明那个新限定下的数值结果，需先讨论既有真空证据而不是自动重算。

#### Group 6 — paper_0cd74ae20ab933f3（AR、PR）

**当前目标与依据：**三种孤立 Cu2(AnCOO)4(4-RPy)2 的 J 和 300 K triplet population。正文 PDF p6、SI S5–S6 方法、S35 敏感性及 S36 Table S3 明确计算值与实验值是两组不同数据。公开配体图/组装规则为输入；历史使用作者 triplet 几何不构成验证无效，更不意味着必须公开这些终态给 agent。

**确定问题：**两模式 task 让 agent 自报 J 符号约定，而 evaluator 固定比较负 J；应公开主报告约定。`r_j_h/me/ome`、`r_pop_h/me/ome` 固定取 `systems[0/1/2]`，但 task/schema 没规定顺序和三个唯一 ID；schema 只要求数组至少三项，合法乱序或重复对象可能导致错误绑定。也需明示 triplet 三重简并及百分比单位。这里不是要求 agent 猜标准答案，而是公布被比较物理量的定义。

**验证覆盖：**`runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260921_acceptance/report/results.json` 回链 09-15 作者几何的真实 multicollinear SF-TDA/PySCF 三体系输出、态 S² 检查及 H 体系 full-SF 控制。本轮读三份 PySCF 日志的 SCF 收敛和对应态结果来源；这些日志没有 Gaussian/ORCA 的 normal-termination 字样，本身不是失败。J=−334.373525/−341.412046/−344.582322 cm⁻¹，triplet%=37.63623/36.84729/36.49420，满足 −335/−342/−345±20 及 37.6/36.8/36.4±2。敏感性只实际覆盖 H，不在 reference 写成所有衍生物全部做了控制。

**修法：**公开 `J=E_S−E_T` 及 `P_T=100×3 exp[J/(k_B T)]/(1+3 exp[J/(k_B T)])`（J 与 kBT 同单位），不公开数值。优先按稳定对象 ID 绑定，若现行接口只支持索引，则在 task/schema 明确 H→CH3→OCH3 主数组且各一次，额外尝试独立存放；同时测试乱序/缺失/重复对象。删停止/免责声明模板但保留态和敏感性证据。reference 分清作者几何输入、参考 triplet 与 spin-flipped singlet/triplet，不新增全系列控制或量化计算。

#### Group 6 — paper_a45d7e9815bcf075（AR、PR）

**当前目标与依据：**PDB 3I40 的局部片段 AMI/FMI 重建、三对二硫键和盐桥半径响应。正文 PDF pp1–3 Eq.(1)–(3)、SI p1 Eq.(3)–(7) 及系统准备支持。已核公开 A/B 序列长度 21/30，总计 51，与本地真实 `inputs/3I40.pdb` 的 SEQRES 相符；不能凭“看起来像其他胰岛素序列”修改对象。

**确定问题：**AR `system_spec.json` 写 `I=s2−s1−s1`，PR 写非负 `I=s1+s1−s2`；SI Eq.(5) 本身确印负号方向，不能伪称两模式都抄错。作者公开正值矩阵、正文解释及现有真实后处理采用正 MI，需明确 benchmark 的正值约定并记录源公式冲突。PR 输入称 4/6 Å optional，而 evaluator p4 明确要 4 对 5/6 Å；AR 又允许任意 radius/overlap、没有公开要求这些半径。当前必评项与公开工作量有冲突。`author_release_verified` 分支仍允许作者产物核查，不能让复述已有矩阵获得独立新计算的成果分；新验证已不只是这个分支。公开仅 PDB 编号，题面明确允许 RCSB 获取，因此不是必然缺数据，但离线发布不自包含。

**reference 的确定过时：**当前 9 行说“author-released data/postprocessing，不是全 51 片段新计算”，已落后于 `runs/hold_verification/group_6/paper_a45d7e9815bcf075/20260921_global_closure/report/results.json` 和 09-23 状态。新记录有 51/51 实际片段 DFT、Löwdin/RDM 分析、排 cap、所有重叠原子对贡献先平均再聚合残基；本轮读其中 50 份生产日志及复用 sphere51 的 `stdout.log`，51 份均有 SCF 收敛和 ORCA 正常结束，而不是只信 PASS 标签。覆盖 130721 原子对；AMI 对 full-reference r≈0.995600、FMI≈0.999378，三二硫键 FMI≈4.3740/4.4707/4.3127 nat；盐桥 5/6 Å 为 1.148988/1.167032 nat，4 Å 无共同覆盖，不当作严格零值。符合当前定性目标，不冒称所有绝对矩阵元素与作者完全相同。

**建议决定与修法：**统一正 MI 定义、nat/对角/对称/原子归属/重叠平均约定；保留源式符号差异于私有 reference。建议把现有 p4 的主检查半径 4/5/6 Å 明确公开（只是比较对象，不给哪一个恢复盐桥），并保留其他半径探索；如要保持 AR 自选半径而改 p4 接受任意足以检验半径效应的方案，需要另批评分变更，不能自行二选一。建议随包提供已有原始 PDB 和身份映射，不提供作者 AMI/FMI 答案；预处理/片段波函数不作为公共答案。移除普通 limitation 得分，作者产物核查只记录来源而不得冒充真实计算完成；全体系比较是否 optional 与成功状态需明确，不能一边写 when feasible、一边暗中要求复现私有全体系矩阵。reference 以真实 51 片段链及盐桥/二硫键控制更新，保留历史产物核查为旧分支。已有计算可支持上述定性目标，不需要为文档更新重新跑 51 份 DFT。

### 15.4 本批清单与评分数量

下表是**修改前的当前包计数**，不是修复完成记录。`K/C/L` 分别为中间关键点总数、结论总数、其中独立 limitation 结论数；普通免责声明也可能混在其他项里，所以 L=0 不代表完全无需清理。逐篇科学依据和详细修法见第 15.3 节。

| group | paper_id | AR K/C/L | PR K/C/L | 当前需要处理的重点 |
|---|---|---:|---:|---|
| 1 | paper_43d74f8a469d9ad3 | 4/1/0 | 4/1/0 | 修正 B–C 四原子扭角定义；完整扫描档案 |
| 1 | paper_9455a82229de2427 | 3/1/0 | 3/1/0 | AR 缺实验比较窗口且 schema 无效；明确 H/ZPE 能量口径 |
| 2 | paper_35a6749f3bae345b | 2/1/0 | 2/1/0 | 两份 SI 优化坐标泄露、双分子 formula、非法选择器、逐态解释 |
| 2 | paper_c7217910ecbee1d9 | 4/2/1 | 4/2/1 | 框架结果关联；结构框架与电子壳层区分；limitation 清理 |
| 4 | paper_628af8d0bf0a1bfe | 4/2/1 | 4/2/1 | 正文/SI 基组差异记录；保留 NICS 定义及真实敏感性检查 |
| 4 | paper_80441aced6051d86 | 4/1/0 | 4/1/0 | 单体/二聚体优化坐标泄露、水介质、失败分支及 reference 量归属 |
| 4 | paper_a21b91f97ce3c68f | 3/1/0 | 3/1/0 | 已有 signed J 科学链成立；清理模板、补全实际方法和三键档案 |
| 4 | paper_c28b0a1c549f4575 | 4/2/1 | 3/2/1 | 纯 scope/limitation 清理；失败过程证据与结果排序得分分开 |
| 4 | paper_e0791c047a731974 | 4/1/0 | 4/1/0 | 垂直/绝热电子能定义；如实区分作者 UDFT 与验证 TD 路线 |
| 4 | paper_ffa556cc3acdf0bc | — | 3/1/0 | 补四构象的实验碳编号映射；保留统计区分而不公开胜者 |
| 5 | paper_3d1d9b7f6df049da | 4/2/0 | 4/2/0 | 非法选择器、横向模式身份/评分关联；保留两项实质结论 |
| 5 | paper_3deba7268b769ce6 | 4/1/0 | 3/1/0 | 当前对象正确；明确选态、清理模板、记录实际单条量化链 |
| 5 | paper_8d8940710de08f7f | 4/2/1 | 4/2/1 | 主比较介质/温压/G 定义待确认；六态数值与相互作用关联 |
| 6 | paper_0cd74ae20ab933f3 | 4/1/0 | 4/1/0 | J 符号/热布居公式和三对象绑定；最新成功链归档 |
| 6 | paper_a45d7e9815bcf075 | 4/1/0 | 4/1/0 | MI 源式符号、半径职责、作者产物分支、离线 PDB；更新 51 片段档案 |
| 合计 | 15 篇 / 29 包 | 52/19/4 | 53/20/4 | AR 14 包、PR 15 包；全部仍在 verified_tasks |

当前总计 **105 个中间关键点、39 个结论项，其中 31 个为科学结论、8 个为独立 limitation**。这里按每个模式分别计，不把同论文两个模式合并成一条评分。

已实际调用当前 `evaluation/scoring/adapters.py:_runtime_contract` 核对：29 包都未写 `scoring_policy`，也没有自定义 `scientific_rubric`，因此采用 `dual_axis_100.v1` 和等分结论权重。628af8、8d894、c28b0、c72179 的两模式都为“一条科学结论 + 一条 limitation”，对应**科学结论轴中各占 50 分**；不是说普通 limitation 固定占最终总分 50 分，最终总分还乘研究过程轴。移除它们后应让真实成果承担科学评分，不能保留免责声明来补数量。

若仅删除上述 8 条纯 limitation，保留其他科学目标，仍有 31 条科学结论：27 个任务包各 1 条、3d1d9 两个任务包各 2 条。这并不表示 27 包只能二元评分；一个结论可以由多个实质结果和规则贡献部分分。获批后应明确如“多个对象/多个能量/多个键/多个模式”的部分完成职责，不擅自平均拆权重、不新造论文结论、不改双轴乘法。3d1d9 的 `c_relax` 是科学解释，不因含 limitation 用词而删除。c28b0 AR 的 `ar_kp_scope` 是另一个纯表态项，拟删除其独立评分职责；最终关键点数量以逐项获批并修复后的实际结果再统计。

### 15.5 实际软件检查、证据深度和未检查项

本轮只做已有材料读取、结构解析、规则适配和本地只读诊断；没有提交新计算，也没有调用正式模型评测或 LLM judge。临时诊断脚本放在 `/tmp/rcb_verified_review_20260923.iGo26i/`，不加入发布包；下列计数亦已用当前仓库实现再次核对。

| 已执行检查 | 实际结果 | 可以与不可以得出的结论 |
|---|---|---|
| 逐包 `evaluation.contracts.validate_task_package` | 29 包均仅有两个 manifest findings | 当前完整性门槛未通过；不是 29 个科学问题 |
| `package_payload_entries` 与原 manifest 逐项比较 | 每包只漏列 reference；其他条目无缺失、内容变化 | 获批修改完成后刷新现有 manifest 即可；未在本轮刷新 |
| `jsonschema.validators.validator_for(...).check_schema(...)` | 28 个有效，9455 AR 无效 | 已定位 `oneOf` 层级错误；valid schema 不等于所有分支语义正确 |
| 对所有规则的 `binding.fields` 调用 `jsonpath_ng.parse` | 18 个不支持的 `[]`，位于 35a674/3d1d9 的 4 包 | 必须改为合法选择器并验证身份/数组语义；不能宣称 18 项科学成果失败 |
| 直接读取包文件并调用 `_runtime_contract` | 29 包均能生成旧策略评分描述；8 包 limitation 50/50 | 这是绕开 manifest 做的**诊断适配**，不是正式加载成功或真实 judge 得分 |
| 最新历史 `report/results.json` 直接对各包有效 schema 校验 | 22 包格式通过；6 包历史格式不匹配；1 包 schema 本身无效 | 不能把这 7 个不通过项统计成“7 个任务计算未验证” |
| 9455 实际共用 `validate_output_contract` | PR 通过，AR 返回 `invalid_contract` | 真实 runner 使用的检查同样会遇到 AR schema 错误 |
| 80441 monomer 分支，真实完整结果及私有合成格式反例 | 真实结果通过；未做频率却填 null 被拒；完整主结果附同层早期失败说明时 oneOf 冲突 | 要分开主结果与尝试记录，并让失败路径可如实提交；合成反例不是科学验证结果 |
| 公开目录软链接检查 | 本批 agent_input 未发现软链接 | 不代表宿主挂载、网络、检索和 API 已完成隔离验收 |
| 源码可见性检查 | `materialize_agent_files` 复制 agent_input；`load_public_task` 返回 task_info，含论文题名/DOI | 需单独确认真实运行是否暴露元数据及可访问原论文；没有据此改通用运行器 |
| 与 Git 基线比较两个模式目录 | 本轮结束前 365 个文件与 `6756212e` 一致，无新包文件 | 本轮仅审查并更新本集中报告，没有实施包内修复 |

上述 6 个历史格式不匹配具体是：628af8 AR 的共享验证结果缺 AR `hypotheses`；c28b0 AR 缺 AR 探索/路线字段；0cd74 和 a45d7 两模式的最新 results 是**计算审计汇总**而非 agent 提交对象。应从真实产物做私有、无损字段映射来检查结果规则，不把缺失的自主探索过程编写成已经做过，也不删除任务要求迁就归档格式。9455 AR 则是独立的真实 schema 错误。

科学阅读覆盖第 15.3 节的全部 15 篇和 29 个包。除了摘要，本轮还回读了 150 余份已有应用日志中的终止、收敛、频率及关键能量片段，以及 Hessian、映射、轨道/后处理产物的相关内容；不是只看平台 SUCCEEDED。基础脚本先读取 145 份日志，再补查 a45 sphere51、a21 NMR、43d 基态和 c28 单体前驱链。Gaussian 的 `Optimization completed on the basis of negligible forces` 已结合 `Stationary point found` 判读；PySCF 以其自身的 SCF/科学输出判读，不因缺 Gaussian/ORCA 结束标记误报失败。

**阅读边界必须保留：**这是任务相关科学链和评分量核对，不是每行日志的全面量化软件审计，不保证任意方法、任意软件或任意公开 starter 都收敛。80441 的 SI 使用 group 已有原文缓存，43d/c28 本地缺 SI 原件的部分已分别说明；未声称这些 SI 原件已独立核验。未检查真实部署的挂载/网络权限，未执行正式 LLM judge、全量 agent 盲测或新 starter 回放。既有成功作者路线可以支持当前科学可计算性，但不能把它宣传为两模式的独立探索成功率。

### 15.6 待负责人批准的修复范围和科学决定

**常规部分建议一次批准：**在本批 29 包内按第 15.3 节先统一 task 章节，分开 PR guidance；取消纯 limitation/停止表态门槛并接回实质科学检查，显式接入已有 `dual_axis_100.scientific_results.v1`；修正已证实的 schema/选择器/字段关联和量定义，补必要且不含答案的原子映射；补完整 reference、归位确有需要的私有文件，最后刷新各包 manifest。保留真实失败提交但不给未完成成果分。不改通用评分默认、双轴公式或其他批次，不改原 group 结果。

以下事项不能只以“格式整理”实施，建议采用的选项和影响逐项列明：

| 决策 | 涉及论文/模式 | 推荐方案 | 保持不变 / 需要接受的影响 |
|---|---|---|---|
| D1 答案结构替换 | 35a674、80441，两模式 | 用独立构建且身份完整的初始结构替换 SI 优化终态；作者终态仅作 evaluator 私有参考 | 保留原结构/性质探索目标、对象和科学结论；不更名为给定结构任务，不宣称新 starter 已实算回放 |
| D2 实验比较职责 | 9455 AR | 公开已有的 −162±27 kJ/mol 实验反应能窗口，不公开产物身份/几何/计算能量 | agent 才能完成题面已要求的实验兼容性比较；PR 已有此信息，无需新增。若改 evaluator 独自比较则需另选修法 |
| D3 必需介质 | 80441，两模式 | 将水介质列为主比较条件，保留软件/方法选择 | 与正文及已验证紧容差目标对齐；不是任意溶剂结果都必须落在同一容差内 |
| D4 热化学协议 | 8d894，两模式 | 明确甲醇连续介质、298.15 K、1 atm 及当前验证的主 G 校正口径；公开条件而非能序 | 保留原六态和数值目标；承认是依据正文/配对输出的 benchmark 解释，不伪称作者已更正 SI 的 in vacuo 标签 |
| D5 MI 定义 | a45d7，两模式 | 采用非负 `I=s1(i)+s1(j)−s2(i,j)`，统一 nat 和聚合约定；保留 SI 负号冲突记录 | 与作者正值矩阵及当前有效后处理一致；不把源公式错误静默归咎于 agent |
| D6 半径与比较职责 | a45d7，两模式 | 公开主检验半径 4/5/6 Å，允许额外设计；由真实片段计算支持结论，作者产物核查不替代完成；按题面现有 when feasible 将额外 full-system 比较明确为 optional | 4/5/6 从隐藏评分条件转为公共比较范围，会收窄 AR 的主比较自由度；不用再跑全蛋白作新的硬门槛。若不接受限定半径，须另批放宽 p4 的评价方式 |
| D7 源方法差异记载 | 628af8、e0791，两模式 | 628af8 私有链如实采用 SI 基组，不强迫 AR 唯一方法；e0791 写清作者 UDFT 与验证 TD 路线差异，保留当前开放方法 | 不改 target/容差，不把独立方法支持说成作者路线完全相同；若要指定唯一作者方法，需重新判断已有证据覆盖，不能悄悄加要求 |

ffa556 的碳标签映射、43d 的扭角定义、0cd74 的符号及对象绑定，均是现有科学目标必需的信息，不应把公开这些定义视为公开答案。保留 a21/3d1d9/ffa 等当前合法给定对象，不一刀切删除所有 SI 坐标。35a674 对不同态扭转的澄清保留“支持或限定假设”的现有接受空间，不强行把验证的 Nap S1 判为 moderate、不新增私有数值硬门槛。

**本轮未识别出必须立即新增量化计算才能处理上述推荐方案的确定缺口。**这不是无条件认证 29 包可发布：D1–D7 未获决定、泄露/缺输入未修、评分/档案/包契约未收尾，发布条件仍不成立。若负责人选用不同科学边界（例如 8d894 固定真空、e0791 强制 UDFT），需针对该选择重新判断已有输出是否足够；不能以原有通过标签代替判断，也不能擅自重算。

### 15.7 获批后的执行顺序及本轮交付状态

1. **先确认范围。**负责人批准常规修复及 D1–D7 的选择后，重新确认当前包未被他人更新；在既有 Git 基线上继续，不覆盖并行改动。
2. **先改格式。**只在 verified_tasks 调整章节，保留每篇的科学身份、目标和两模式边界，单独检查格式 diff。
3. **再改实质问题。**优先处理两篇坐标泄露、实验窗口/碳编号/介质输入，再修公式和对象绑定、schema 分支、评分关联与 limitation。逐篇记录实际批准范围和改动，不用批量模板重写科学内容。
4. **补成功计算档案。**利用第 15.3 节已定位证据，将全部 29 份 reference 从摘要补为实际输入→有效步骤→关键结果→当前 evaluator 对应关系；只记真实成功链和已确定方法差异，不新增评分或填造 AR 探索经历。
5. **验收。**按实际改动测试真实结果、少一个对象/错单位/数组乱序、去免责声明、完整主结果加额外失败、部分/失败提交等；保留科学目标和未批准变更的数值容差。刷新受影响包 manifest 后再做正式包校验，并分开报告静态检查与真正运行测试。
6. **交付后再决定迁移。**汇报每篇改动、剩余边界、检查结果及 final/暂缓建议；负责人另行确认具体论文/模式/去向后才能移动。本轮不提前迁入 final 或 hold。

**本轮实际完成：**当前清单与 Git 基线、15 篇逐模式审查、论文/现有真实计算对照、上述软件诊断、逐篇修复方案及决策汇总；新增内容集中在本报告第 15 节。**未完成且未冒充完成：**任务格式修订、泄露/输入修复、schema/evaluator 修改、reference 补档及迁移，均尚待本批方案确认。没有新计算、HPC 操作、对外发布，也没有改 `docs/verification`、papers、canonical、final 或 hold 的科学内容。

## 16. 2026-09-23 获批修复与验收结果

### 16.1 范围、依据与完成状态

负责人已批准上述方案，特别要求将答案性优化结构替换为初始化结构，原优化结果仅用于私有评估。本次已实施第 15.3 节常规修法及 D1–D7，覆盖 **15 篇论文 / 29 个任务包（AR 14、PR 15）**。没有把合法的给定对象性质任务一律改成结构发现任务；没有扩大论文选定的科学目标。

修复以论文正文和可取得的 SI 为首要依据，结合实际验证输入、原始输出和后处理校准可行性。溯源审查只记录已发生的成功计算，不用格式样例补造科学结果。没有新量化计算、HPC 操作或正式模型评测；没有修改 `docs/verification`、论文、canonical、final、hold 或通用评分/运行器实现；本批全部留在 `verified_tasks` 等待负责人验收。

版本：修复前批次基线 `6756212e`；单独的格式整理提交 `87bce55c`。质量修复及本节另作限于本批路径的 Git 提交，提交号随交付说明报告；不打包无关工作区改动。

### 16.2 答案结构的实际处理

| 论文 | 涉及模式 | 替换的公开文件 | 新输入与私有结果的职责 |
|---|---|---|---|
| `paper_35a6749f3bae345b` | AR、PR | `dbc_ph_s0.xyz`、`dbc_nap_s0.xyz` | 分别为 C32H21N / 54 原子、C36H23N / 60 原子中性 singlet；公开为独立图嵌入的未优化起点，原 SI 终态放 `evaluation/author_results/` |
| `paper_80441aced6051d86` | AR、PR | `g1_monomer.xyz`、`g1_dimer.xyz` | 64 原子/+2 单体与 128 原子/+4 二聚体；独立构建单体，再以非来源取向作无碰撞二聚体装配，原优化单体/堆积终态仅作私有参照 |

合计 **4 个任务包中的 8 份公开 XYZ** 已替换。使用 RDKit ETKDGv3 从没有 conformer 的完整显式氢化学图生成；未读入作者端点距离/扭角作为约束、未对终态作小扰动、未按目标能量或堆积值筛选。原坐标只用于核对离散连接性和恢复既有原子编号，不用于新几何嵌入。二聚体以两个独立单体和通用旋转/无碰撞规则装配，未保留 SI packing。

每份 starter 配有公开的 `*_identity.json`，明确映射 SMILES、原子数、分子式、电荷、自旋及二聚体分片；映射编号对应 XYZ 的 1-based 原子行。两模式采用相同起点，避免额外输入不公平。已核对新旧连接图一致、坐标有限、键长合理、无严重碰撞、原文件逐字节完整归档，以及新结构不只是终态的旋转/平移。

`evaluation/author_results/README.md`、`evidence_map.json` 和相应评分描述已明确私有终态可支持原有身份、扭角、平面/堆积描述符核对。**没有新增未经批准的 RMSD 阈值、要求同坐标系，或把 reference 变成新的评分轴。**当前仍由五个 evaluator JSON 的关键点、结论和规则评分；保留私有坐标不等于已经开发了一套新的自动坐标评分程序。

合法固定对象继续保留：如 a21 的指定构象耦合、3d1d9 的固定几何振动、ffa 的给定候选 NMR 区分。其坐标不是本任务要求发现的最终答案；不能仅因来自 SI 就删除必要对象。

### 16.3 逐篇已执行修改及验收结论

下表 K/C 为修复后的中间关键点/科学结论数，按每个模式分别列出；具体输入、真实步骤和来源差异见各包 reference，改动依据见本节及 `evaluation/task_provenance/maintenance_audit.md`。

| group | paper_id | 本轮完成的主要修改 | AR K/C | PR K/C |
|---|---|---|---:|---:|
| 1 | `paper_43d74f8a469d9ad3` | 统一 X–B–Cipso–Cortho 四原子扭角及整支芳基旋转；24 个唯一角度、0/360 几何回闭与 345/0 能量连续性分开，不要求两采样点能量相同；补基态与扫描成功链 | 4/1 | 4/1 |
| 1 | `paper_9455a82229de2427` | AR 补现有实验 −162±27 kJ/mol 比较窗口；明确 product+H−SiN−isoprene 的电子+ZPE 反应能和 H doublet；修 AR 无效 schema、至少两个候选及 H 能量字段；不公开产物几何/计算值 | 3/1 | 3/1 |
| 2 | `paper_35a6749f3bae345b` | 独立 starter 与私有终态分离；修分子式/映射；S0/S1 分态评价扭转及轨道证据，不强迫 Nap S1 也是 moderate；合法 JSONPath、身份唯一性、失败格式 | 2/1 | 2/1 |
| 2 | `paper_c7217910ecbee1d9` | PR 52→81 原子元数据纠正；AEA 的电荷态/能量/ZPE 定义清楚；将结构框架保持与额外电子壳层证明分开；删除纯 limitation；成功结果可附早期失败记录 | 4/1 | 4/1 |
| 4 | `paper_628af8d0bf0a1bfe` | 公开 NICS=−nᵀσn、公共平面/两环/平均值定义；保留真实敏感性检查，删除无依据的 opposite-face 相等要求；PR 路线与正文/SI 基组差异如实记载；失败不等价于最低点成功 | 4/1 | 4/1 |
| 4 | `paper_80441aced6051d86` | 独立单体/二聚体 starter；公开主水介质；区分平面间距、完整质心距离和 slip；成功对象/所有观测量与失败路径对齐；32.409° 归回第二种单体扭角，非二聚体扭角 | 4/1 | 4/1 |
| 4 | `paper_a21b91f97ce3c68f` | 三个 Sn–C 原子对唯一映射及 raw signed total J 算术均值；不取绝对值、不只取 FC、不乘经验修正；清理停止/免责声明门槛，补真实 NMR 与频率链 | 3/1 | 3/1 |
| 4 | `paper_c28b0a1c549f4575` | 删除 AR 纯 scope 关键点及两模式 limitation 结论；能量排序结果与诚实失败过程分开；`pair_results`/`pair_attempts` 明确为状态相关分支，修 schema 局部 `$defs` 引用 | 3/1 | 3/1 |
| 4 | `paper_e0791c047a731974` | 区分同 S0 几何的垂直能与两极小点的绝热电子能，不混 ZPE/G；比较式明确用 vertical T1；记录作者 UDFT 与实际 TD-triplet 验证路线不同，不增 SOC 必算项 | 4/1 | 4/1 |
| 4 | `paper_ffa556cc3acdf0bc` | 公开四构象对应的 30 个实验碳标签—XYZ 原子映射；仅身份信息，不含计算位移/DP4+ 概率或胜者；成功分支要求两个候选实际结果，补 12 个候选作业及 TMS 参考链 | — | 3/1 |
| 5 | `paper_3d1d9b7f6df049da` | 公开质量加权 Y 参与度/横向分量的定义，四模式记录与选择器正确关联；不隐设 >0.5/>0.8 阈值；保留固定几何 Hessian 范围，不加优化或定量 T1 要求 | 4/2 | 4/2 |
| 5 | `paper_3deba7268b769ce6` | 以最低可见态及物理身份选态，不按靠近答案或最亮态挑选；允许实际 bridge/acceptor 分布，不加 acceptor>50% 的隐藏门槛；保留原能量目标与容差 | 4/1 | 3/1 |
| 5 | `paper_8d8940710de08f7f` | 公开甲醇连续介质、298.15 K、1 atm、100 cm⁻¹ Grimme quasi-RRHO 熵参考；每分子单独置零，仅将各 Z 的 gap 绑定数值评分；保留六态/相互作用证据，不泄露能序 | 4/1 | 4/1 |
| 6 | `paper_0cd74ae20ab933f3` | 公开 J=ES−ET、triplet 三重简并及 300 K 布居公式；三个唯一 ID/主数组顺序与索引规则一致；一项真实敏感性足够，不改成每衍生物都必做；补 SF 根赋值成功链 | 4/1 | 4/1 |
| 6 | `paper_a45d7e9815bcf075` | 补原始实验 PDB；统一正 MI/nat、正交轨道归属、排 cap、原子对先平均再聚合；主 5Å map 与指定接触的 4/5/6Å 对照公开一致；全蛋白另算 optional；删除作者产物核查冒充完成分支；补真实 51 片段 DFT 档案 | 4/1 | 4/1 |
| 合计 | 15 篇 / 29 包 | 保留原有科学问题；纯声明不计成果 | **51/15** | **53/16** |

合计由 **105 K / 39 C** 变为 **104 K / 31 C**：删除 8 个纯 limitation 结论和 c28 AR 的 1 个纯 scope 关键点，保留所有原有科学结论。29 包显式采用已有 `dual_axis_100.scientific_results.v1`；没有改通用双轴公式。27 包各 1 条科学结论、3d1d9 两包各 2 条；没有为了增加数量而拆造结论。多对象/多观测量按真实完成证据评价，不给未计算的结果分。

既有 numeric 规则的所有 target/tolerance 已与格式提交 `87bce55c` 逐项比较，**均未改变**。必要科学检查、对象身份、频率/态检查和真实敏感性仍保留。普通 limitation/stopping 字段可留作可选文字，但无独立成果分或必填声明门槛；末轮还定向清除了少数 expected 中残留的“必须说明 limitation”和题面“失败即完成”矛盾。

### 16.4 计算 reference 的实际完善和阅读边界

29 份 `evaluation/verified_computation_reference.md` 均已从摘要补为：源论文与实际范围→真实有效步骤→关键结果→原始输入输出链接→当前关键点和结论对应→实际方法/来源差异。仍然只是计算档案，不作为新增 evaluator，不编造独立 AR 探索经历。

档案共链接并复核 **157 份不同原始计算日志**；按 Gaussian/ORCA 正常终止及 PySCF 自身 SCF 收敛标记核验，均可定位。必要频率/能量/对象和关键后处理已依第 15.3 节的逐篇证据核对；这里不是声称对全部日志每一行做了独立软件审计，也不把“终止标记存在”等同科学结论自动正确。

特别更正：80441 的原始 SI DOCX 已在 group 4 的 `artifacts/source_downloads/1-s2.0-S0143720825008265-mmc1.docx` 找到并核读，更新了第 15 节当时“仅缓存”的阅读边界；同论文旧审计 JSON 的 slip_definition 元数据把法线/平面写反，本批按实际数值和几何定义澄清，未改历史文件。a45 的 reference 现记录 51 份真实片段 DFT 及另 4 份 6Å 接触日志，不再沿用“只有作者产物后处理”的旧说法。8d894 使用最新甲醇六态链，不混入旧真空结果。

仍如实保留的出处差异：628af8 正文/SI 基组不一致；e0791 作者 UDFT 与历史 TD-triplet 方法不同；8d894 SI 的 in-vacuo 表题与正文/配对结果冲突；35a 的 Ph S1 波长与 SI 不逐值一致、Nap S1 接近正交。它们已经按获批边界写入任务或私有档案，不隐瞒、不通过改宽数值容差来消除。43d/c28 的本地 SI 原件仍未取得，相应部分只引用可定位的历史方法来源，未虚称亲读 SI；现有正文、完整公开定义和真实输入输出支持其当前子目标，原件补存属于来源存证后续事项。

### 16.5 实际验收结果

| 检查 | 结果 | 检查职责 |
|---|---|---|
| 29 包 schema、真实结果字段映射、正反例、JSONPath/数字规则、来源链接等回归 | **409/409 通过** | 覆盖无免责声明、成功附额外失败、早期/部分失败、空结果拒绝、相关对象重复/乱序、原 target/tolerance 不变；不等于新科学计算 |
| 加上刷新后的逐包完整性校验 | **438/438 通过**（含上一行） | 29 个 manifest 已只在本批定向刷新；没有改默认 final 脚本入口 |
| 实际 `validate_output_contract` 共用检查函数 | **116/116 通过** | 29 包各测完整、额外失败尝试、早期失败、无效空对象四类；失败可提交但不可伪装完整成果 |
| 新 starter / 映射 / PDB 专项 | **74/74 通过** | 8 XYZ 的身份/归档/几何与跨模式一致性、四构象各 30 个唯一 C 标签、两模式实验 PDB 与原件/21+30 残基一致 |
| 真实 `TaskRepository` + `load_runtime_evaluation` | **29/29 通过** | 使用本批根目录正规加载，每包实际策略均为 scientific_results；不是绕开包校验的诊断适配 |
| 共用提交检查现有单元测试的相关子集 | **9 passed，6 deselected** | 测 schema 错误、真实局部引用、非有限 JSON、路径/外部引用拒绝、失败分支和工具共用逻辑；未运行其余生命周期测试 |
| 原始成功日志与 reference 链接 | **157 日志可定位且存在相应结束/收敛标记，链接无缺失** | 属于已有证据回读，无新 HPC/量化验证 |
| Git diff 空白/补丁检查 | 普通文件通过；原样 PDB 保留固定列宽尾部空格 | 两份实验 PDB 与源文件逐字节一致，未为消除文本警告破坏原文件；此检查不是科学验收 |

测试样例保留于私有临时区 `/tmp/rcb_verified_review_20260923.iGo26i/`；逐包检查结果记录在 `evaluation/task_provenance/contract_regression_20260923.json`，不放到公开输入或历史原结果中。628af8 AR、9455 AR 的假设字段及 c28 AR 的路线字段，在共享作者验证记录中原本不存在，格式测试使用明确标注的 **synthetic format-only** 字段。它们仅检查契约，不是“历史已完成自主探索”的证据，也未写进科学 reference。0cd/a45 的审计结果到提交格式使用已披露字段映射，不改变科学数值。

### 16.6 当前结论与交付边界

**已完成批准范围内的任务内容修复和回查，没有留置已确认但未处理的本批修复项。**在当前科学目标和获批条件下，既有作者知情的真实验证计算可以支持这些子问题及所保留 evaluator 科学成果的可计算性；这不要求向 agent 提供作者终态，也不因替换初始结构自动要求重算作者路线。

尚不能把本轮说成“已经无条件正式发布/完成盲测”，原因需分清：

1. 新公开 starter 做了身份和几何合理性检查，**没有从这些具体初猜再做量化收敛回放**。不保证任意初猜/方法必定收敛；这是一项未执行测试，不是把原作者路线验证改判失败。
2. 没有正式 LLM judge 运行或全量 agent 盲测。当前确认的是原始科学证据、任务契约、数字关联和正式加载；不冒称已经验证实际评分器的每种语义判断。
3. 私有目录名不是隔离措施。发布/运行必须只向 agent 提供批准的 `agent_input` 与工具，不能开放整个仓库、evaluation/reference/author_results/paper_route、原论文/SI或 group 输出。源码中的 `load_public_task` 还会返回含论文题名/DOI 的 `task_info`，实际使用路径/检索与网络权限需发布方另行核验；本轮没有修改通用运行环境，不能据此保证部署侧无泄露。
4. 迁移需负责人另行确认具体清单。全部 29 包仍留在 `verified_tasks`；本轮未代为 final/hold 分流。后续删除 `task_provenance` 等维护文件后，须用既有机制刷新 manifest；核心评分不依赖这些维护文件。

详细问题依据继续见第 15.3 节，当前已修状态以本节及各包维护记录为准。后续无需再把本轮已修问题当成尚待决定事项；若要求唯一作者算法、新增科学目标、量化验证新 starter 或改造通用隔离/评分运行器，应另行明确范围。

## 17. 2026-09-23 二次回查后的定义与契约修复

### 17.1 本次授权、范围和结论

负责人批准：“问题真实存在，且修改方案符合论文核心主张，则按方案修复。”本次对上一轮指出的问题逐项核对本地正文/SI、实际后处理和真实验证产物，实施 **7 篇 / 13 包（AR 6、PR 7）** 的修改。其余 16 包未更改任务内容；完整回归覆盖全部 15 篇 / 29 包。修复前 Git 基线为 `e0721ff2`。

第 16.6 节的“没有留置本批修复项”只对应当时已发现并检查的范围，不能解释为永远不会发现其他定义或契约缺陷。本次确实发现并修复了新的具体问题，当前状态以本节为准；不重复宣称无条件发布已获保证。

本次没有新量化计算、HPC 操作、正式 LLM judge 或盲测，没有修改 `docs/verification`、papers、canonical、final、hold 或通用评分器。没有移动任何任务。所有包仍留在 `verified_tasks`。本批数值 target/tolerance、最终科学结论文件及关键点/结论数量均未改变；总量仍为 **104 个关键点 / 31 条结论**。没有新增 limitation 评分。

### 17.2 逐篇问题、论文依据和实际修法

| 论文 | 模式 | 确认的问题及依据 | 已执行修改；与论文核心思想的关系 |
|---|---|---|---|
| `paper_a45d7e9815bcf075` | AR、PR | 题面限定 4/5/6 Å，但未统一中心和残基纳入方式，评分又使用作者的固定半径响应。正文 PDF p2 为 51 个 Cα 球心；SI p1 §1.3 给 cap 和受限准备。对公开产物逐一核实，153/153 个片段恰为“任一准备后原子（含 H）进入半径即纳入整残基”。 | 补 Cα、完整残基纳入、统一准备结构、NH2/COOH cap/排除及主/额外设计职责。r4/p4 要核对真实覆盖与计算；作者 4 Å 无覆盖、5/6 Å 有覆盖是该准备结构的参考现象，不是所有合法准备必须复述的口号。仍评局域片段能否重建关联及半径/覆盖效应，不把源矩阵或准备结构公开给 agent。 |
| `paper_80441aced6051d86` | AR、PR | 单体主评分值对应最小二乘环平面的 0–90° 急角，而题面未限定该口径；还允许 inline coordinates，与成功 schema 的 structure_path 要求不一致。正文 p3–4 为水中构型/堆积，真实后处理 `group_4/finalize_paper_804.py:124–153` 明确 SVD 平面和 acos(abs(dot))。 | 公开原子环集合及急角公式，区别带符号四原子扭角；统一交付为非空结构文件路径。保留二聚体平面间距、完整质心距与相对平面的 slip 定义，保留独立 starter。仍检验扭曲单体/偏移堆积的几何基础，没有扩大到整篇发光机制计算。 |
| `paper_35a6749f3bae345b` | AR、PR | “至少五态或给定窗口全部态”中的窗口没有定义；schema 允许只有 S0 几何的跃迁，也可能把 S1 标签误读为激发态吸收。SI pp11/13 Tables S5/S7 分别给出两种优化几何各五个 singlet 根。 | 明确每分子在 S0/S1 优化几何分别报告根 1–5，state 是几何标签，不是 S1→Sn 吸收。validated 分支要求两几何各五个唯一主根，额外高根允许，失败分支不强制编造结果；两模式评分说明同步。既有 Ph 根数 10/5、Nap 10/10，已覆盖该定义。仍是取代基—构型—光谱/轨道关联比较。 |
| `paper_3d1d9b7f6df049da` | AR、PR | schema 允许主 modes 超过四项，numeric selector 却把全部项与四参考频率配对。SI pp21–22 Tables S3a/b 对应每异构体四个主横向模式。 | 完整结果的 modes 恰四项；额外/混合候选放 additional_modes，不限制探索数量。规则先核对物理身份和重复 mode_id，再比较主四项，禁止按参考频率反选。保留四频率目标、±12 cm⁻¹ 容差及原定性 T1 解释，不新增 T1 实算。 |
| `paper_8d8940710de08f7f` | AR、PR | 一处把 torsions 列为 optional，与 V(+)/V(−)/Z 身份、后文及 schema 冲突。正文的 C–S–N–C 构象研究及现有六态结果均需要带符号扭角区分状态。 | 统一六态 signed torsion 必报；electronic energy 仍可选。保留相互作用证据与自由能比较，不新增 QTAIM 或额外机理计算。 |
| `paper_3deba7268b769ce6` | AR、PR | “lowest visible”没有可操作窗口。正文 p4 区分低能可见 ICT 和高能 UV 局域跃迁。 | 公开 400–700 nm 主比较窗口，明确它是 benchmark 操作约定而不是作者报告的阈值；按最低能而非最亮/最近答案选态。没有窗口内态应报告缺失主结果及已计算根，不能拿 UV 根顶替。现有 S1≈501.7 nm、S2≈356.1 nm，选态与能量 target/tolerance 均不变。保留自主模式对电子性质的独立判断。 |
| `paper_c7217910ecbee1d9` | 仅 PR | 首句 “Compute its...” 没有先行对象。 | 明确主语为 PAl12[B(C6F5)3]2；不改 AEA、结构框架比较或所需计算。AR 无此问题，未改。 |

其中 a45 的“任一原子整残基”规则是根据作者公开几何产物核实的操作细节，不冒充正文逐字写明；3de 的可见窗口是公开的 benchmark 定义，不冒充论文发现。公开新增的其余内容为身份/测量/提交定义，未加入作者结果数值、胜者、参考矩阵或优化终态坐标。没有更换任何 XYZ/PDB/SMILES，也没有把此前移入私有目录的答案重新公开。

### 17.3 实际检查结果

| 检查 | 结果 | 能证明什么 |
|---|---|---|
| 全批原有回归及 manifest | **438/438 通过，29 包** | schema、历史结果字段映射、现有 numeric 算术比较、JSONPath、reference 链接、包完整性；目标和容差不变 |
| 本次新增反例和定义检查 | **91/91 通过，13 包** | 缺 S1、缺根 5、重复主根、缺 root 编号、空/缺结构路径、负的主平面角、第五主模式、仅三主模式等不能冒充完整；额外候选和合法失败仍可提交 |
| 实际共享提交检查函数 | **116/116 通过，29 包** | 完整、成功附额外失败、早期失败和非法空对象四类；不是仅检查 JSON 能解析 |
| 独立 starter/映射/PDB 检查 | **74/74 通过** | 上轮替换的结构与身份及跨模式一致性未被破坏；不等于从新起点量化收敛 |
| 作者片段构造核实 | **153/153 完整匹配** | 作者 full_protein.pdb 全局原子 serial 与全部 nocap 残基集合一致，且无部分截断残基；只做几何/集合分析，未做新 QM |
| 正规 repository 与 runtime 加载 | **29/29 通过** | 实际加载当前包与 scientific_results 双轴策略 |
| 共用提交检查相关单元测试 | **9 passed，6 deselected** | schema/失败格式/非有限数字/路径和外部引用等；没有运行其余生命周期测试 |
| Git 补丁检查和历史测试档案保留 | **通过** | 修改范围限本批，原私有检查记录保留，新增 follow-up 结果不冒充科学计算 |

针对性测试和补丁生成脚本在本地临时目录 `/tmp/rcb_contract_followup_20260923.sCjiQZ/`；原有回归脚本在 `/tmp/rcb_verified_review_20260923.iGo26i/`。正式留存依据和检查摘要仍使用逐包现有 `evaluation/task_provenance/maintenance_audit.md`、`contract_regression_20260923.json`，没有另建报告体系。10 份相关 reference 只追加测量定义与历史结果的对应解释，不改写成功计算，也不增加评分轴。

### 17.4 当前可作出的判断与仍需区分的事项

上述七篇已确认问题已经按批准方案解决，所保留的是论文中既定科学子问题，不是凭空扩大的新目标。既有作者知情计算记录仍支持这些子问题存在真实有效的计算路线；本次不要求历史验证从当前公开初始结构盲跑一遍。

这不等于宣称整个运行系统已经完成发布级端到端验证。以下仍沿用第 16.6 节边界：没有新 starter 量化回放、没有全量 agent 盲测或实际 LLM judge 稳定性评测；语义模式身份、不同记录是否重复同一物理模式、方法差异及基于证据的定性解释，仍依赖 evaluator 正确执行，而不是 schema 自动证明。没有通过目录名字验证部署侧隔离；evaluation、author_results、reference、原论文/SI和 group 产物不得向被评 agent 开放。43d/c28 本地 SI 原件缺存、以及已披露的源方法/数值差异没有因本轮措辞修复而消失，也未被新增为评分限制。

**本轮没有新增需要负责人决定的科学边界；没有自动迁入 final。**若下一步希望宣称“实际运行与判分稳定性也已验证”，应单独安排小批量端到端试评及部署隔离核验，不能把本节静态/既有结果回归说成已经完成这些测试。

## 18. 2026-09-24 依维护流程逐篇重新审查：发布建议，不执行修复或迁移

### 18.1 本轮范围、判定口径和结论

依据当前 `docs/verification/final_verified_tasks/final_verified_task_maintenance_workflow.md`，重新审查 `tasks/verified_tasks` 的 **15 篇 / 29 包（AR 14、PR 15）**。`paper_ffa556cc3acdf0bc` 只有 PR，不补造 AR。本轮任务内容基线为 Git `bb2ed74f`；工作区原有的流程文档修改与 `SCIENTIFIC_REAUDIT_20260917.md` 未跟踪文件不属于本次修改，保持原状。

本轮仅在本文追加审查结论，未修改任何任务包、通用代码、论文、历史验证或 final/hold 文件，未迁移、提交新量化计算、操作 HPC 或启动模型评测。逐篇以正文/SI、当前公开任务、实际评分文件和真实输出交叉核对，不以上一轮报告的 PASS 代替本轮证据。

**总体判断：现有真实计算支持这 15 篇当前已选定的科学子问题；本轮未确认新的科学身份错误、必需计算缺口或包内待求终态泄露。不能因此称为“29 包已无条件正式发布”。**具体分为：

| 任务内容层面的建议 | 论文 / 包数 | 含义 |
|---|---:|---|
| 当前科学设计、输入及契约可接受 | 11 篇 / 22 包 | 本轮未发现新的必须修改项；现有来源差异及适用科学范围见逐篇表，不扩大为整篇论文全部结论 |
| 科学设计可接受，建议同步非实质性信息 | 3 篇 / 5 包 | 9455 的必做/可选元数据、3d1 的来源摘要、ffa 的输入简介；不属于计算不可行或应迁 hold 的证据 |
| 科学计算有支持，发布前应修提交契约 | 1 篇 / 2 包 | 35a 两模式的 validated 分支仍接受轨道失败对象或空证据；详见 18.3，不是已证明可获得高分 |
| 因本轮新增科学缺口建议 hold | 0 | 不把作者知情验证、公开初猜未重放、只有一个结论或非必评工作未算当作 hold 理由 |

上述均为审查建议，**所有 29 包仍在 verified_tasks**。任务内容通过与运行部署验收分开；共用部署边界见 18.5。

### 18.2 逐篇、逐模式判断及计算支持

下表页码均指本地 PDF 文件页；DOCX 单独说明。每行分别复核 AR/PR 指令及评分差异，共享作者知情计算仅支持科学可计算性，不冒充独立 AR 发现经历。K/C 表示中间关键点数/科学结论数。

| Group / paper_id | AR 判断；K/C | PR 判断；K/C | 原文、输入与实际计算核对；当前范围和剩余事项 |
|---|---|---|---|
| 1 / `paper_43d74f8a469d9ad3` | 可接受；4/1 | 可接受；4/1 | 正文 p11 §3.5 支持 PBE0/def2-SVP、15° 扭转扫描。公开实验 CIF 对应完整 48 原子对象，不是待求扫描能量。真实 1 个 Opt/Freq 前驱及 24 个单点覆盖完整周期，前驱 138 个正频；势垒约 18.26655 kJ/mol。AR 自行解释轮廓，PR 检验位阻假说；现目标为 compound 1 的电子能轮廓，不要求未验证的 compound 1/3 对照或光漂白速率。SI 原件本地缺存，正文和原始计算支持当前子题，补存属于来源完善，不据此否定已完成计算。 |
| 1 / `paper_9455a82229de2427` | 可接受，元数据待同步；3/1 | 可接受，元数据待同步；3/1 | 正文 pp3–5、SI p3 支持反应对象与 CBS-QB3/0 K 比较。公开只有反应物身份、电子态和实验窗口，没有候选产物答案。实际两个独立构建的 SiNC5H7 singlet 产物各 36 个正频，反应能约 −150.52252、−156.45352 kJ/mol；H doublet 及电子能+ZPE 记账一致。两模式均明示 TS/intermediate optional，当前产物/反应能结论不要求补 TS/IRC。AR 需独立提出解释，PR 给 terminal-addition/cyclization 假说；没有把历史知情路线写成 AR 盲测。`task_info.difficulty_reasons` 仍将中间体写成必做，详见 18.3。 |
| 2 / `paper_35a6749f3bae345b` | 发布前修契约；2/1 | 发布前修契约；2/1 | 正文 p6 Table 2/Fig.5 与 SI 几何/跃迁表支持所选 DBC-Ph/Nap 比较。公开为独立嵌入的 54/60 原子 starter 和完整身份图，作者优化坐标在私有侧。四态 Opt/Freq 均有正频，两个 S0 的 TD10 及 S1 各至少五根覆盖当前要求，另有对应波函数的 Mulliken/SCPA 分析。Nap S1 约 81.69°、Ph S1 412.06 nm 与 SI 441.44 nm 的差异已披露，现行逐态语义评分允许有据限定假说，不声称逐值复现。AR 不预给轨道定位结论，PR 把它作为待检验假说。科学链有支持，但成功分支仍可只交轨道 failure_report，详见 18.3。 |
| 2 / `paper_c7217910ecbee1d9` | 可接受；4/1 | 可接受；4/1 | 正文 pp2–4 与原始 SI DOCX 直接核对。完整对象为 81 原子 PAl12[B(C6F5)3]2；两位点、相关电荷/自旋共 8 个 Opt/Freq，各 237 个正频。AEA 含 ZPE 为 3.959169 eV、纯电子差为 3.945536 eV，对应 3.93±0.30 eV 靶。公开图和状态定义足够，任务区分电子与绝热量并检查框架保持；不额外强求整篇壳层/AIMD。AR 自选路线、PR 有作者框架指导，均无待求能量公开。 |
| 4 / `paper_628af8d0bf0a1bfe` | 可接受；4/1 | 可接受；4/1 | 正文 p5 Fig.5、SI p14 与 pp51/53 对应 4a/4c。公开完整图、两环身份、1.7 Å 探针及 −nᵀσn/均值定义，不给答案。两 Opt/Freq 和两 shielding 原始作业支持 NICS 23.1738/19.1577 ppm，与 23.6/19.2±2 ppm 一致；既有张量的局部法向控制差异最大约 0.004635 ppm。AR 的假设比较与 PR 的作者假说不同，但必要计算量均被支持。正文/SI 基组差异已如实披露，不宣称两者相同，不改靶或容差。 |
| 4 / `paper_80441aced6051d86` | 可接受；4/1 | 可接受；4/1 | 正文 pp3–4/Fig.4；原 SI DOCX 在 group_4 的 source_downloads 中找到并直接核读。公开独立 64 原子 +2 单体、128 原子 +4 二聚体 starter，作者终态仅私有保存。两 Opt/Freq 分别 186/378 个正频；单体急角平面角 51.9775°/32.4094°，二聚体平面距 3.778995 Å、完整质心距 5.353514 Å、slip 44.9015°。现题面明确环集合和测量定义，不混淆论文 3.63 Å 平面距与 5.09 Å 质心距。AR 独立判几何关系，PR 检验 J-like packing 假说；只评几何基础，不硬评未算的体相发光机制。 |
| 4 / `paper_a21b91f97ce3c68f` | 可接受；3/1 | 可接受；3/1 | SI p2 方法、p5 表及 pp10–11 结构核对。给定 axial 62 原子对象是本任务合法已知对象，不是待评的轴/赤道构型发现结果。真实 Opt/Freq 180 正频与后续 NMR 支持三个指定 Sn–C 的完整 signed J：−249.688/−223.744/−205.060 Hz，均值 −226.164 Hz，对应 −217±15 Hz。原子映射、同位素、总耦合/符号和均值定义完整。PR 的超共轭背景不变成额外 equatorial/NBO 硬评分；TZP-ZORA 基组名不被误称为已使用 ZORA Hamiltonian。 |
| 4 / `paper_c28b0a1c549f4575` | 可接受；3/1 | 可接受；3/1 | 正文 pp3–4/Fig.2 支持 DED2–PC 相对 TEA–PC 的更强结合。公开四个完整分子图；真实四单体/六复合物共 10 个 Opt/Freq 和 10 个单点覆盖三 pair、每 pair 两初始方向。DED2–PC 约 −30.0887/−29.6475、TEA–PC −13.1874/−12.8220、BF4–PC −16.5408/−16.5395 kcal/mol；最弱 DED2 仍强于最强 TEA，构成实际敏感性支持。AR 独立设计路线，PR 检验给定相互作用假说。评孤立电子结合能，不把它当体相自由能。SI 原件本地缺存，未冒称已亲读；正文、公开定义及真实计算支持当前子题。 |
| 4 / `paper_e0791c047a731974` | 可接受；4/1 | 可接受；4/1 | 正文 pp5–6、SI p7 方法及 p12 Table S3。合法给定 Cy2 S0 几何用于电子态性质，仍需 T1 弛豫；两最低点各 180 个正频，另有两组 TD。垂直 S1/T1/T2=1.8909/1.0555/2.1220 eV，绝热 T1=1.010301 eV，对应 1.09±0.15 eV；垂直/绝热及电子能零点定义正确。作者 UDFT 与验证 TD-triplet 路线差异已披露，现任务允许方法选择。PR 的 heavy-atom 背景不能解释为已验证 SOC/ISC 因果；两模式当前只要求指定 energetics。 |
| 4 / `paper_ffa556cc3acdf0bc` | 无此模式 | 可接受，输入简介待同步；3/1 | 正文 p2/Fig.1、SI supplementary_002 p5、pp12–13、pp26–32 核对相对构型与 NMR 工作。任务已批准为两给定候选的性质区分，不考察独立发现这两种几何。实际四份 81 原子构象、30 实验碳位移、四份标签映射均齐；8 个优化/频率、4 个 NMR 加 TMS 共 13 原始作业。DP4+ Student-t 结果 B(8S*)=99.999956799%，两种能量权重同一胜者。schema/评分不要求未算的绝对构型/ECD。`task_info.data` 仍称 two geometries，详见 18.3。 |
| 5 / `paper_3d1d9b7f6df049da` | 可接受，出处摘要待同步；4/2 | 可接受，出处摘要待同步；4/2 | 正文 p8、SI pp21–22 Tables S3a/b 核对。两固定 96 原子 doublet 几何是获批的 Hessian 性质任务输入，不评几何发现。两 ORCA PBE/def2-TZVP、Y ECP、DEFGRID3/VeryTightSCF Hessian 均 282 个正振动模；未误加 D3。Ih 四模 38.5694/44.9525/56.1923/60.8506，D5h 66.7033/73.0946/82.3920/87.4306 cm⁻¹；均在当前 ±12 范围，均值差 27.2639 cm⁻¹。物理向量先选模，非按接近答案选模；当前任务 Y–Y 横向指标与历史 cage-radial 分析均有现成结果支持。不必新算定量 T1。evidence_map 漏 68.9，但主评分/reference 已完整四项。 |
| 5 / `paper_3deba7268b769ce6` | 可接受；4/1 | 可接受；3/1 | 正文 p4 Dye3 的 59.44 kcal/mol 为正确对象来源。公开身份为 34 原子 C17H11N2O3S−、E-imine，不提供目标跃迁。真实 r2SCAN-3c 最低点 96 正频，后续 full-TDDFT 十根/NTO 给 S1=2.471173 eV=56.9866 kcal/mol、约 501.7 nm，处于原 ±3 kcal/mol 范围；桥/受体 NTO 贡献约 48.3%/36.9%，不用隐藏 >50% 阈值。400–700 nm 是已披露 benchmark 操作窗口，不冒充论文结论；选最低可见态，不按最亮或最接近 gold 选态。 |
| 5 / `paper_8d8940710de08f7f` | 可接受；4/1 | 可接受；4/1 | 正文 p5 §2.8、SI pp8–11/Table S8 核对。公开为两分子图、V±/Z 区域与甲醇、298.15 K/1 atm/100 cm⁻¹ QRRHO 约定，无终态或能序。最新六态 R2SCAN 甲醇 Opt/Freq 均有效，Z gap=2.638125/2.763389 kcal/mol，V pair gap=0.227309/0.210636；与两 Z 的 2.57±0.8 靶一致。SI in-vacuo 表题与正文/配对证据的差异已披露并按批准协议处理，未混旧真空结果。PR 可给氢键假说，AR 自行解释；现有 signed torsion/接触证据足够，不新增 QTAIM 硬要求。 |
| 6 / `paper_0cd74ae20ab933f3` | 可接受；4/1 | 可接受；4/1 | 正文 p6、SI pp5–6/p35/p36。公开三种 Cu2 体系的完整身份图，不给作者 triplet endpoint。历史 PySCF SF/TDA 真实链给 J=−334.3735/−341.4120/−344.5823 cm⁻¹，300 K 三重态布居 37.6362/36.8473/36.4942%；S/T 根按 S²赋值，符号/三重简并公式一致。H 的 full-SF 控制 −344.221852 cm⁻¹ 有 result/checkpoint 证据，一项实际方法控制满足现题面。任务允许优化或以合理方式建立 reference，不因复用作者几何而虚报缺优化验证。 |
| 6 / `paper_a45d7e9815bcf075` | 可接受；4/1 | 可接受；4/1 | 正文 pp1–3 与 SI p1 支持局部片段 MI/FMI 思路。公开原始实验 PDB 3I40 的 A21/B30，不公开准备后量化片段、密度或答案矩阵。51 个 5 Å 片段 DFT 及 4 个 6 Å 接触计算为真实有效量化，合计 55 日志；作者全残基纳入规则与 153/153 原始 nocap 成员集吻合。正 MI/nat、排 cap、先原子对均值再残基汇总已统一；AMI/FMI 相关分别约 .99560/.99938，三 S–S 与指定盐桥半径响应有计算支持。4 Å 无共同覆盖用 null，不伪称实算零。AR 可自行制定额外设计，PR 给局部片段路线；不硬绑所有合法准备都必须出现作者同一覆盖阈值，不要求新的全蛋白 DFT。 |

每篇当前 reference 第 3 节可直接定位原输入/输出，group 5/6 的最新 closure 路径也已列入 reference；不是只依据旧 group 汇总表判断。两模式合计 **104 K / 31 C**，其中 AR **51/15**、PR **53/16**，本轮未改变数量或任何评分参数。

### 18.3 已确认但本轮未修改的问题及最小修法

#### A. 35a 两模式：成功状态可混入轨道失败对象

位置：两包 `agent_input/submission_schema.json` 的 `result_schema.anyOf[0].properties.molecules.items.properties.orbital_evidence`，以及相邻 `status=validated` 的 `allOf/if/then`。题面要求成功结果包含轨道定位及 S0/S1 状态证据；当前成功分支收紧态、扭角和根覆盖，却没有收紧轨道字段。

以真实有效 `report/results.json` 为基础，**仅在内存**更换一个分子的字段，两模式均复现：

| 测试内容 | 当前结果 | 是否符合完整成功的题意 |
|---|---|---|
| 保持真实结果不变 | schema 接受 | 是 |
| 保持 `status=validated`，`orbital_evidence={"failure_report":"SYNTHETIC CONTRACT TEST: no orbitals computed"}` | schema 接受 | 否；轨道必需量尚未完成 |
| 保持 validated，criterion/HOMO/LUMO 都为空字符串 | schema 接受 | 否；没有必需证据 |
| 保持 validated，S0/S1 state_checks.evidence 为空字符串 | schema 接受 | 否；状态标签不能替代证据 |

影响：**成功/部分完成的提交契约没有完全对齐**。不能据此声称模型一定能骗到高分：当前 r2/ar2 和 scientific_results 策略仍要求真实轨道与计算证据，尚未运行真实 LLM judge 来证明误判。

最小修法：仅在 validated 分支要求完整轨道对象及非空 criterion/HOMO/LUMO、非空状态证据；缺轨道或缺态证据仍可走现有 partial/bounded_failure 并提交已有成果，不封死失败出口。新增“成功标签+失败轨道/空证据被拒、真实完整结果仍可提交、部分失败仍可提交”的反例回归。**不改科学目标、参考数值、容差或结论，不需新量化计算。**非空只能排除明显空壳，不能代替 evaluator 的科学核查。

#### B. 9455 两模式：中间体的元数据职责未同步

位置：`task_info.json` 的 `difficulty_reasons[0]`。PR 写 `must generate ... mechanistic intermediates`；AR 写必须搜索 `product and intermediate space`。当前两份 task.md 已明确两产物必需、TS/intermediate optional；评分也只对“声称得到的 TS”要求连接验证。

最小修法：元数据改为“至少两种不同产物的生成、最低点验证和反应能比较；中间体/TS 仅在使用其支撑机理时要求相应证据”，不改变现科学范围、不补算 TS。当前 `_build_instructions` 不注入 difficulty_reasons，因此尚未证实实际 runner 已据此错误要求中间体；问题仍影响包级介绍和其他元数据消费者，应同步。

#### C. 3d1 两模式：evidence_map 的四模来源摘要少一项

位置：`evaluation/evidence_map.json` 的 SI Table S3a 条目仍为 `Ih 49.9,54.9,65.2 cm-1`。直接读 SI PDF p21，第四个对应模式为 **68.9 cm⁻¹**。现行 numeric target、关键点、四项 schema 和 reference 已有全部四项，真实计算亦覆盖四项。

最小修法：补齐该来源摘要的 68.9，不改任何评分靶、容差或选模规则。属于出处摘要不完整，不是漏算第四模，也不应重算 Hessian。

#### D. ffa 仅 PR：输入简介没有反映四份几何

位置：`task_info.json` 的 `data[0].description` 写 `two complete candidate XYZ geometries`，而实际为 **两个相对构型候选、每个两个构象，共四份 XYZ**。题面、manifest 和 carbon_label_mapping 已清楚列出四份，所有实际输入均存在。

最小修法：同步简介为两候选各两构象，并保留四份碳标签映射说明。`data.description` 会进入当前 runner 说明，虽然详细题面可消歧，仍建议避免首层简介冲突。不改候选、几何、实验数据或统计目标，不需补算。

### 18.4 输入、reference 与评分检查的实际结论

**输入与泄露：**重新检查公开 task、JSON/schema、结构角色及公开/私有引用，未发现本轮新的已确认答案泄露或必需基础数据缺失，公开 agent_input 无软链接。35a/804 的独立初始结构保留完整身份，原作者终态仍在私有侧。a21、e079、3d1、ffa 中获批的给定对象/几何用于性质计算，不把合法已知对象误报为待求结构答案；a45 的原始实验 PDB 也不等于作者准备后量化结果。输入能自包含定义对象，不等于任何初猜/方法都保证收敛。

**reference：**29 份均能定位成功步骤、主要条件、关键结果和原始证据；共享科学链合计 **157 份不同计算日志**全部存在，并有相应 Gaussian/ORCA 结束或 PySCF 收敛标记。逐篇另核对相关前驱、频率/态、后处理及当前必评量，不用“正常结束”代替科学验证。未发现必须补录一个新量化阶段才能支持当前目标的新增缺口。reference 是档案，不是评分输入；作者路线可知情，不要求变成 AR 盲跑记录。

**来源覆盖：**本轮读取本地 15 篇正文；43d/c28 的 SI 原件未能取得，未将历史方法索引冒充亲读原件。804 的 SI 使用 group 已有原始 DOCX，c721 的 SI 使用 papers 下原始 DOCX。43d/c28 当前靶依正文和真实计算已能检查，缺 SI 存档单独披露，不自动转成科学 hold。628 的基组、e079 的 T1 求解方法、8d8 的溶剂表题、35a 的逐态差异均保持已批准且公开/私有适当分离的说明，不为消差而调容差。

**评分：**29 包经正规 repository/runtime 加载均使用 `dual_axis_100.scientific_results.v1`；普通 limitation 已不作为独立成果或必填声明计分。27 包只有一条结论、3d1 两包各两条，不因此判任务不合理。当前指令允许按真实完成的不同观测量给部分评价，不是天然“一个结论只能 0/100”；但真实 judge 的部分分稳定性本轮未实测，不能用静态契约结果冒充该测试。必要的对象/态/频率/量定义与实际证据检查仍保留。

### 18.5 共用运行边界：单列，不误报成 15 篇科学问题

当前 `evaluation/repository.py:219` 的 `materialize_agent_files` 只复制 agent_input；`evaluation/execution/workspace.py:85` 的 `_build_instructions` 从题面及选择的任务字段构造输入，没有注入 paper.title、DOI 或 difficulty_reasons。

但 `evaluation/repository.py:202` 的 `load_public_task` 返回完整 task_info，内含来源论文题名/DOI。若别的 UI/API/检索路径将其整体传给 agent，会形成答案检索线索；9455 来源论文题名甚至直接命名产物族。**代码出口存在风险，不等于已证实当前标准 runner 将整份元数据泄露。**发布方应核对实际入口，仅将批准公开字段提供给 agent，论文元数据留维护/evaluator 侧。本轮未改通用入口。

真实运行的文件挂载、父目录权限、共享搜索和网络访问仍未实测。不能向 agent 开放整个仓库、evaluation、author_results、reference、paper_route、论文/SI或 group 输出；目录名称本身不是权限隔离。正式发布前应完成该共用边界核验。没有新增“必须重放所有 starter”的发布门槛；本轮也不声称实际 LLM judge、全量 agent 运行或新 starter 已完成端到端验收。

### 18.6 本轮实际重跑的检查与未执行项

以下为 2026-09-24 实际读回/执行结果，不照搬前一日测试记录：

| 检查 | 本轮结果 | 解释 |
|---|---|---|
| `regression_audit.py --manifest` | 29 包，438/438 | schema、历史结果字段映射、数字规则/选择器、来源链接、manifest；不覆盖所有可能反例 |
| `final_checks.py` | 116 runner checks + 74 输入/几何 checks 通过 | 实际提交校验函数及原有成功/失败样例、starter 身份、映射和 PDB；没有生成新科学结果 |
| `test_followup.py` | 13 包，91/91；153/153 作者片段成员集匹配 | 上轮改动的专项反例和几何/集合关系回归 |
| `TaskRepository(['tasks/verified_tasks'])` + `load_runtime_evaluation` | 29/29；全部 scientific_results 策略 | 仅审计加载，不是将暂存根配置为正式发布根 |
| 本轮新增 35a 内存反例 | 两模式均接受 validated+失败轨道/空证据 | **确认未关闭问题**；原有全通过测试没有覆盖它，不能拿 438/438 否定它 |
| reference 原始日志与链接 | 157 份不同日志可定位、有对应结束/收敛标记；所查链接无缺失 | 科学是否有效另外按逐篇对象、上游链和量定义判断 |
| 包内公共 symlink | 0 | 不代替真实部署权限检查 |

只读脚本位于 `/tmp/rcb_verified_review_20260923.iGo26i/` 与 `/tmp/rcb_contract_followup_20260923.sCjiQZ/`；本轮不运行其 emit/fixtures 写入选项。AR 的 628/945 假设字段、c28 路线字段在格式回归中仍是明确标注的 synthetic format-only 样例，不作为历史自主探索或科学计算证据。

本轮**未执行**新量化计算、public-starter 收敛重放、HPC 操作、正式 LLM judge、全量 agent 盲测或 pytest；第 16/17 节的 `9 passed` 是历史测试，不计入本轮。未调整任务、评分、reference 或 manifest，未作 final/hold 迁移。

**建议下一步：**先按 18.3 的最小范围修复 35a 成功契约，同时同步三处轻量信息；相应包刷新 manifest 并做针对性正反例。无需更换研究目标、削减必评科学内容或新增量化验证。然后由负责人确认具体任务清单；在实际部署隔离核验完成后才可作正式发布声明。没有新增需要科学边界选择的事项，也没有本轮必须迁入 hold 的论文。

## 19. 2026-09-24 四项问题复核与获准修复结果

### 19.1 授权、版本与实际范围

负责人要求先确认第18节所列问题真实存在，再依据论文和验证过程修复。本轮重新读取相关正文/SI、现行 task/schema/evaluator 及已有成功结果，四项均确认存在；完成 **4 篇 / 7 包（AR 3、PR 4）** 的定向修复。修复前任务包与 Git `bb2ed74f` 一致，可由该提交恢复；本轮不重写第18节历史审查结论，当前处理状态以本节为准。

仅修改七包各一份任务内容文件、各包已有 `evaluation/task_provenance/maintenance_audit.md` 和对应 manifest，另追加本报告并新增一份定向回归测试。未修改 `docs/verification`、论文、canonical、final、hold、通用运行器或评分器；未启动新量化计算、HPC 作业或实际 LLM judge，所有任务仍在 verified_tasks。

### 19.2 问题是否真实、依据及已实施修复

| 论文 / 模式 | 重新确认的问题与依据 | 实际修改 | 保持不变的内容 |
|---|---|---|---|
| `paper_35a6749f3bae345b` / AR、PR | 正文 PDF p6/Fig.5 和 SI pp11/13 的态/轨道分析是现题面必需工作。group_2 真实结果中两分子的 criterion、HOMO、LUMO 与 S0/S1 evidence 均完整。修复前再次实测：仅将一个分子的轨道对象改成 failure_report，保持 validated，仍通过 schema。此前空白证据问题也由同一条件缺口导致。 | 只在顶层 `status=validated` 的条件内要求完整轨道对象，criterion/HOMO/LUMO 和两态 evidence 均须为非空、非纯空白字符串。历史真结果仍可提交；缺轨道走已有 detailed bounded_failure 或 compact failure/partial_results，成功附带额外失败尝试仍接受。 | 不新加定量轨道比例、不固定 population 算法，不改科学目标、评分或原结果。格式非空不代替 evaluator 的科学证据核查，不声称已测出 LLM judge 错判。 |
| `paper_9455a82229de2427` / AR、PR | 正文 pp3–5/SI p3 确有产物及 TS/PES 研究，但当前获批任务明确产物最低点/0 K 反应能必做、TS/intermediate optional；真实两独立产物链支持该子目标。旧 difficulty_reasons 将中间体列为必须，和当前任务不一致。 | 同步 `task_info.difficulty_reasons[0]`：至少两种产物、最低点验证、0 K 反应能比较；中间体/TS 可选，声称的对象需相应证据。AR 保留独立机理解释职责。 | 不删除现有关键点，不将可选 TS 改为必做，不伪称论文没有 TS/IRC；task.md、evaluator 和成功计算均不变。 |
| `paper_3d1d9b7f6df049da` / AR、PR | 直接核读 SI PDF p21/Table S3a 第4–7行，四频率为 49.9/54.9/65.2/68.9 cm⁻¹。现行主评分、reference 及实际四模结果完整，只有 evidence_map 摘要少第四项。 | 在 `evaluation/evidence_map.json` 原条目 text 补入 68.9。 | 不改变参考靶、±12 cm⁻¹ 容差、物理选模规则或输入结构；不是补算遗漏模式。 |
| `paper_ffa556cc3acdf0bc` / 仅 PR | SI supplementary_002 p5/Table S2、pp12–13 方法和 pp26–32 构象，与当前四份 XYZ、碳映射及历史 NMR 链一致：两个候选各两构象。旧 data 简介误写成两份几何。 | `task_info.data[0].description` 明确两候选各两构象，共四份完整 XYZ。 | 不新增/替换结构，不公开计算位移、概率或胜者，不改相对构型判别目标或统计评分。 |

没有把论文全部计算扩大成当前任务必需工作，也没有为适配旧验证缩减当前科学目标。四项均可由已有证据和契约修复解决，无需补做量化计算。

### 19.3 修复后实际检查

新增 [定向回归测试](../../tests/test_verified_task_contract_repairs_20260924.py)，测试只使用原结果的只读载入及明确标注的临时格式反例，不把人工反例写入 reference 或 group。两模式、两个分子分别检查五个证据字段的空串、纯空白、null 和缺失；使用 JSON Schema 与 runner 共用 `validate_output_contract` 双重核验。

| 检查 | 本轮修复后结果 |
|---|---|
| 新增定向 pytest | **108 passed**：真实完整结果、无普通免责声明、成功附额外失败、validated+轨道失败拒绝、五类证据字段异常拒绝、详细部分失败与早期失败可提交、三项信息同步、七包正式加载 |
| 原有全批回归 `regression_audit.py --manifest` | **438/438 通过，29 包** |
| 实际提交函数与输入检查 `final_checks.py` | **116/116 提交检查 + 74/74 输入/几何检查通过** |
| 前轮专项 `test_followup.py` | **91/91 通过，13 包；153/153 作者片段成员集匹配** |
| 正规 repository/runtime 全批加载 | **29/29，通过；均为 dual_axis_100.scientific_results.v1** |
| 七包 manifest 刷新及包校验 | **7/7 通过**；仅对本次修改包调用 rebuild(package)，未调用默认 final 全局入口 |
| 差异范围与科学内容不变检查 | 两份 schema 除 validated 条件外完全等于修复前；任务说明、公开结构/实验数据、scoring_rules、reference_key_points、reference_conclusions、critical_failures 和 verified_computation_reference 均未改动 |

新增完整结果测试直接使用 group_2 真结果，没有给轨道/态证据补造内容。其余全批格式回归沿用已说明的 AR synthetic process 字段，只验证格式；不是本轮进行了 AR 自主探索。测试数量代表所覆盖的检查，不是对所有可能科学/评分错误的数学保证。

### 19.4 当前结论和仍未执行事项

**第18.3节四项已确认问题全部修复并通过针对性回归；没有遗留本轮获批但未处理的任务内容问题。**本次修复没有改变原有科学结果或验证路径，因此上一轮逐篇关于现有真实计算支持当前子目标的结论仍成立。当前仍为 **15 篇 / 29 包，104 个关键点 / 31 条科学结论**，未增加 limitation 评分。

第18.5节的共用部署事项仍单独保留：没有测试实际文件挂载/网络隔离，没有修改返回论文元数据的共用 API，也没有实测 LLM judge 的部分分稳定性；它们不是本轮七包内容修复已解决的事项。43d/c28 的 SI 原件缺存亦未因本次修改而消失。本轮不据这些未执行项要求重算既有量化验证，也不宣称已完成无条件对外发布。**未迁入 final/hold，待负责人确认具体发布/迁移清单。**

## 20. 2026-09-24 末轮三项问题的获准修复与回归

### 20.1 授权、基线和范围

负责人明确批准：先确认末轮提出的问题真实存在，修改应符合论文核心内容，并使评估任务前后一致。本轮重新核对原文、当前文件和原始验证结果后，完成 **3 篇 / 5 包（AR 2、PR 3）** 的定向修复。修复前这些任务包与 Git `5aa0821c` 一致；未将工作区其他人的改动纳入修复，也未处理未获授权的其他论文。

改动限于 a21 两模式的编号说明、e079 两模式的能量解释与来源归属、ffa 仅 PR 的计算档案，以及五包现有维护记录和 manifest。本节集中记录结果，新增一份针对性测试，不新建科学报告。未修改 `docs/verification/`、papers、canonical、final、hold、原始计算结果或通用执行/评分代码；没有新增量化计算、HPC 操作、LLM judge 调用或任务迁移。

### 20.2 原文证据、实际修复和科学影响

| 论文 / 模式 | 再次确认的问题及依据 | 实际处理 | 不变的内容与验证支持 |
|---|---|---|---|
| `paper_a21b91f97ce3c68f` / AR、PR | SI PDF S2 明确 Bu 是三个 Sn–丁基碳的平均，S5 给 1a 理论值 −217 Hz。当前 task 允许完整 remapping，却另写 atom order fixed；schema 固定 Sn=1、碳=2/3/7。只改工作编号并提供映射、保持所有物理结果不变的反例被拒绝，证明提交约定存在歧义。 | 明确程序内部可以重排，但 `results.json.sn_bu_pairs` 必须映射回公开 XYZ 原始 1-based 编号；重排时附完整原始→工作编号映射。同步 task、schema 的说明和 pairs 规则，不放宽身份校验。 | 分子/结构、方法自由度、三项 full signed J、均值、−217±15 Hz 和所有 schema 校验条件不变。真实 −249.688/−223.744/−205.060 Hz 的均值 −226.164 Hz 仍支持目标。 |
| `paper_e0791c047a731974` / AR、PR | 正文 PDF pp5–6、SI §2.8/Table S3 确认：2T1>S1 是 rubrene 湮灭剂条件，不是 Cy2 敏化剂条件；单靠 Cy2 四能量不能确定 SOC/ISC 增强。旧任务和 PR 结论将不同对象的判据串联。此外后台 `paper_route` 将本地 TD triplet-root 方法写进作者路线，但正文 p6 写 UDFT。 | 保留四能量，统一用 Cy2 态序及垂直 S1−T1、T2−S1 能隙解释；Cy2 的 2T1−S1 仅可选诊断、不独立计分。同步 task、schema 说明、最终结论/规则、证据摘要、reference 和 PR 元数据。后台作者路线恢复 UDFT，单独记录真实验证采用 TD triplet-root。AR 不加入作者机理或数值答案。 | 四目标 1.8909/1.0556/2.1221/1.09 eV、各 ±0.15 eV 和全部数值规则、原输入/身份/态验证不变。既有实际值 1.8909/1.0555/2.1220/1.010301083 eV 继续有效；.8354/.2311 eV 仅由已有能量相减，无新 QM、阈值或独立评分项。不要求肯定 SOC 因果、补 rubrene/速率计算或填写普通 limitation。 |
| `paper_ffa556cc3acdf0bc` / 仅 PR | SI S12–13 是作者流程；真实 group_4 记录明确四个 B3LYP 最低点为既有成功结果复用，并非从后来 M06 筛查输出重新串接。`dp4_results.json.primary_TMS_calibration` 为 188.48755 ppm，自算 189.1954 ppm 只作对照。原 reference 没有清楚区分这些关系，但 99.999956799% 主概率真实存在。 | 只澄清 reference：十二项候选作业的依赖/复用关系、298.15 K E 主权重/G 对照、DP4+ 方法软件参数库主 TMS 与历史自算 TMS 的角色、`author_standard_computed` 与 `computed` 分支及证据链接。 | task、全部公开输入、schema、五个 evaluator JSON、构型答案完全不变。E/G 主校准的 B 概率分别 99.999956799%/99.999937279%，各候选概率和为 100%，控制分支不改变胜者；不需要重新计算。 |

e079 原 group `results.json` 中不严谨的敏化解释保留为历史原文，不改写证据；当前 reference 已明确该解释不再用于证明 rubrene 判据或 SOC 因果，继续使用真实能量、频率/态身份等有效计算证据。这是解释校正，不是将未执行计算宣称为已执行。

### 20.3 本轮实际检查结果

新增 [针对性回归测试](../../tests/test_verified_task_interpretation_repairs_20260924.py)。测试使用只读历史结果、原子编号的等价变换、明确标注的格式反例与能量直接相减，不将临时样例写进 reference 或 group。JSON Schema 和 runner 共用 `validate_output_contract` 均执行。

| 检查 | 实际结果 |
|---|---|
| 本轮针对性 pytest 与前轮契约 pytest | **160 passed（本轮 52 + 前轮 108）**：完整/早期失败、无普通免责声明、合法重排回映、原子对乱序、重复/缺失/错碳拒绝、四能量必需、无可选诊断可提交、主校准分支和五包 runtime 加载 |
| 全批 `regression_audit.py --manifest` | **29 包，438/438 检查通过**；数值结果、绑定、引用、schema 和包清单无新增异常 |
| 全批 `final_checks.py` | **116/116 runner 检查 + 74/74 输入/几何检查通过** |
| 五个修改包 manifest 刷新及正式包校验 | **5/5 通过**；仅定向 `rebuild(package)` |
| 全批正式包校验及 repository/runtime 加载 | **29/29 通过**，均使用 `dual_axis_100.scientific_results.v1` |
| 与修复前 Git `5aa0821c` 比较 | 全批所有数值规则、公开 data 文件、关键点/结论 ID 不变；未涉包无改动；a21/e079 schema 仅描述变化、校验条件不变；ffa 题面/schema/数据/五 JSON 完全不变 |

本轮仍为 **15 篇 / 29 包、104 个关键点 / 31 条科学结论**；a21 每模式 3/1、e079 每模式 4/1、ffa PR 3/1，未增加或删除关键点/结论，也未增加普通 limitation 评分。e079 的最终结论职责从含混的因果假设检验统一到其既有四能量科学结果。

全批历史格式测试中的 628/945 AR 假设、c28 AR 路线仍是已披露的 synthetic 格式样例，不能当作自主验证历史。旧 group 文件能通过格式校验不代表其中每句旧机制解释都获认可；本轮未运行真实 LLM judge，未宣称测得实际得分或部分分稳定性。

### 20.4 当前处理结论

**本轮获准的三项问题已修复，相关联文件已同步，现有真实计算继续支持修订后的科学子目标，无需新增量化验证。**本节修复完成时，五包及其余任务仍在 `tasks/verified_tasks`，尚未获得或执行 final/hold 迁移；之后负责人明确授权整批迁移，实际结果见第 21 节。

此前单列的两篇 SI 原件缺存（43d/c28）、实际部署挂载/网络隔离、真实 judge 稳定性不属于这三项修复的已完成内容；本轮不据此要求重算，也不将本次软件回归称为全部任务无条件正式发布认证。没有新增需要负责人决定的科学边界。

## 21. 2026-09-24 整批迁入 final 与迁移后检查

### 21.1 授权、范围与版本

负责人明确要求：“帮我把这些调整好的评估任务移动到 final 文件夹中，同时确保这些论文的评估任务没有什么问题。”据第 15–20 节实际修复范围，本批为 **15 篇 / 29 包（AR 14、PR 15）**，不只包含最后修复的三篇。先前已经迁入 a21/e079 两模式及 ffa 的 PR 共五包；本次继续核验其余十二篇、二十四包，并完成整批迁移。

迁移前已修复内容的可恢复版本为 Git **`73ee040b`**。迁移只使用完整目录的 `git mv`，所有目标事先确认不存在，没有覆盖既有 final 包。原始任务、论文/SI、docs/verification、历史计算文件和 hold 均未改动；工作区他人的未提交改动及 `SCIENTIFIC_REAUDIT_20260917.md` 未纳入本次修改。

整批迁移和测试路径更新已保存为 Git **`8e363b72`**；提交后本批路径无未提交差异。仓库原有 OpenMolcas pre-commit 钩子引用的 `sbin/copyright` 不存在，因而该版权检查未执行，钩子仍返回成功。本次没有绕过或修改钩子；下列任务校验和 160 项 pytest 是实际单独执行的结果，不由该钩子的退出码推断。

当前对应路径为 `tasks/final_verified_autonomous_research/<paper_id>/` 和 `tasks/final_verified_paper_reproduction/<paper_id>/`。每包原有的五个评分 JSON、公开输入、reference、author_results（原有时）和 task_provenance 都随包保留；未提前删除维护记录。verified_tasks 保留汇总文档，两个模式目录中本批任务包均已迁出。

### 21.2 逐篇迁移清单及复核结论

以下结论承接第 18 节的论文/真实计算逐篇核对，并以第 19、20 节修复后的实际文件为准。本次比较确认所有科学内容与已审查版本一致；没有因为迁移而改目标、输入、评分参数或历史计算事实。

| Group | paper_id | 已迁入模式 | 当前科学支持与修复确认 |
|---|---|---|---|
| 1 | `paper_43d74f8a469d9ad3` | AR、PR | 完整实验结构、优化/频率及 24 点刚性扫描支持现行电子能轮廓；未发现新增输入或评分缺口。SI 原件缺存继续如实披露。 |
| 1 | `paper_9455a82229de2427` | AR、PR | 两个独立产品最低点及 0 K 反应能支持必评量；元数据已与 TS/中间体可选职责同步。 |
| 2 | `paper_35a6749f3bae345b` | AR、PR | 独立公开 starter 与私有作者终态分离；两分子四态及轨道/光谱计算支持当前定性比较。成功分支不能再以失败轨道对象或空证据冒充完成。 |
| 2 | `paper_c7217910ecbee1d9` | AR、PR | 完整分子身份、相关电荷/自旋及八个 Opt/Freq 支持电子亲和能和框架保持；量与单位定义未变。 |
| 4 | `paper_628af8d0bf0a1bfe` | AR、PR | 两体系优化、屏蔽张量和局部法向后处理支持 NICS；原文方法差异已有说明，未改靶或容差。 |
| 4 | `paper_80441aced6051d86` | AR、PR | 单体/二聚体独立 starter 完整；平面角、平面距、质心距和 slip 定义明确，既有有效优化及后处理支持评分。 |
| 4 | `paper_a21b91f97ce3c68f` | AR、PR | 三个 signed Sn–C 耦合及均值已有真实结果；内部重排后须回映至公开编号的规则已统一。 |
| 4 | `paper_c28b0a1c549f4575` | AR、PR | 四单体、六复合物的优化/频率和单点支持三对结合能及方向敏感性；SI 原件缺存继续披露。 |
| 4 | `paper_e0791c047a731974` | AR、PR | 四能量及态身份验证有效；已消除 Cy2/rubrene 判据混用，区分作者 UDFT 与历史 TD-triplet 路线，不硬评未算的 SOC/ISC。 |
| 4 | `paper_ffa556cc3acdf0bc` | 仅 PR | 两候选各两构象、实验碳映射及 NMR/DP4+ 链完整；reference 已区分最低点复用、后补筛查和主/对照 TMS 校准。 |
| 5 | `paper_3d1d9b7f6df049da` | AR、PR | 两 Hessian 和物理选模后处理支持全部四模及模式差异；evidence_map 的第四个来源频率已补齐。 |
| 5 | `paper_3deba7268b769ce6` | AR、PR | 正确 phenolate 对象的最低点、TD/NTO 支持最低可见态和电荷转移解释；不按最接近答案或最亮态替代选态。 |
| 5 | `paper_8d8940710de08f7f` | AR、PR | 六态甲醇优化/频率及已约定的热修正支持相对自由能；未混入旧真空结果。 |
| 6 | `paper_0cd74ae20ab933f3` | AR、PR | 三体系 SF/TDA、自旋根及已有方法控制支持 J 与热布居；公开仅提供完整身份，作者端点不作为待评输入。 |
| 6 | `paper_a45d7e9815bcf075` | AR、PR | 原始实验 PDB、片段定义及 55 份有效量化日志支持所选 MI/FMI 和接触检查；153/153 作者片段成员集匹配回归通过。 |

四篇给定对象的任务继续按既有批准范围处理：a21 的 axial 对象、e079 的给定 S0、3d1 的固定 Hessian 几何，以及 ffa 两给定候选用于性质计算/比较。它们不被宣称为独立几何发现任务；待求性质和候选胜者未放进公开输入。35a/804 的待优化结果仍位于私有侧，公开使用独立初始结构。没有将作者知情验证或公开 starter 未盲跑误判为验证无效。

### 21.3 本次实际执行的检查

使用仓库现有 `.envs/researchchembench/bin/python`；系统 Python 缺少 jsonpath_ng 的初次检查未开始任务校验，不作为任务失败，也未为此安装或修改环境。

| 检查 | 本次结果与范围 |
|---|---|
| 剩余二十四包迁移前检查 | 文件逐个与 `73ee040b` 比较一致；24/24 无目标冲突、无软链接、包校验通过。 |
| 迁移前已有结果/规则回归 | `regression_audit.py --manifest` 对剩余 24 包 **360/360**；字段映射、数字比较和规则关联通过。AR 缺少历史过程字段的格式样例仍标明为 synthetic，不是新增自主探索记录。 |
| 迁移前公开输入及提交检查 | `final_checks.py` 对剩余 24 包 **96/96 runner 检查、70/70 输入/几何检查**；`test_followup.py` **91/91**，包含 153/153 片段成员集匹配。 |
| 迁后针对性 pytest | `.envs/researchchembench/bin/python -m pytest tests/test_verified_task_interpretation_repairs_20260924.py tests/test_verified_task_contract_repairs_20260924.py -q`：**160 passed in 15.74s**。两测试文件改为显式加载 final 包，不因暂存目录已空而漏测，也不回退到 canonical。 |
| 全部迁后文件完整性 | **29 包、454 文件**与迁前清单一致；内容变化仅为 reference 相对链接少一层 `../` 及相应 manifest 更新。公开输入、task/schema、五个评分 JSON 和数值目标均未在迁移时改变。 |
| JSON、包清单与实际加载 | **300 个 JSON 可解析；29/29 正式包校验通过；TaskRepository.from_final 显式清单及 load_runtime_evaluation 29/29 通过**，均使用 `dual_axis_100.scientific_results.v1`。 |
| reference 引用与原始日志 | **703 个本地相对链接有效**；29 份 reference 引用 **157 份不同原始日志**，均可读取且有对应正常结束/收敛标记。科学含义沿用逐篇核对，不把结束标记单独当作全部结论成立的证明。 |
| 标准公开输入导出 | 对显式 final 清单运行 `materialize_agent_files`，**29 包、115 个公开文件**与 agent_input 逐个一致；没有复制 evaluation、reference、paper_route 或 task_info。临时检查产物位于 `/tmp/rcb_promoted_public_20260924_rcdmq3xl/`。 |
| 关键点与结论计数 | 保持 **104 K / 31 C**；AR 51 K / 15 C，PR 53 K / 16 C。没有新增 limitation 得分或修改部分完成职责。 |

未在迁后再运行只扫描 verified_tasks 的旧临时脚本并把零任务视为通过。最后一轮在 final 实际路径进行全包清单/链接/加载检查及针对性测试，保证检验对象是迁入后的任务版本。

### 21.4 当前判断与未实测事项

**本批任务内容层面未发现新的阻断项，已按授权全部迁入 final。**此前确认的问题均已修复，已有真实作者路线计算继续支持当前必评科学量；本次没有新增量化计算、HPC 操作或模型评测，也没有更改科学目标来迁就旧结果。

两篇 `paper_43d74f8a469d9ad3`、`paper_c28b0a1c549f4575` 的 SI 原件在本地仍缺存；当前所选子题可由正文、完整输入和真实计算检查，不宣称已经亲读缺失 SI。现有方法差异、候选范围及性质任务范围保持第 18–20 节的明确口径。

标准文件导出已检查，但实际部署的父目录/共享盘/网络权限与真实 LLM judge 部分分稳定性没有实测。`load_public_task` 返回完整论文元数据的共用 API 风险仍在第 18.5 节记录；标准输入导出没有复制该文件，并不自动证明所有其他入口都安全。正式运行应继续只向 agent 提供批准的公开输入，不把私有答案或论文材料一同挂载。这些未实测项不被写成本轮已完成的对外发布认证，也不据此要求重算所有论文。

## 22. 2026-09-24 两份新增 SI 的归档与任务影响核对

### 22.1 实际归档及检查范围

负责人提供两份 PDF，要求按现有目录格式移动并检查对任务的影响。已核对首页题名、作者与 paper_info 中的论文身份，按 `documents/supplementary_001.pdf` 归档，并在对应 `paper_info.json.documents` 中补充 supplementary_information 条目、原文件名和既有格式要求的 SHA-256。移动前目标不存在，移动后文件字节保持不变，tasks/tmp 中这两个源文件已迁出。

| 原 tasks/tmp 文件 | 论文及现归档位置 | 页数 |
|---|---|---:|
| organoboron_heterocycles_mmc1.pdf | [paper_43d74f8a469d9ad3 / supplementary_001.pdf](../../papers/paper_43d74f8a469d9ad3/documents/supplementary_001.pdf) | 47 |
| solvation_structure_supercapacitors_mmc1.pdf | [paper_c28b0a1c549f4575 / supplementary_001.pdf](../../papers/paper_c28b0a1c549f4575/documents/supplementary_001.pdf) | 16 |

阅读两份 SI 的文本，并直接查看关键图表页面；对照正文、AR/PR 的 task、公开输入、五个 evaluator 文件、paper_route、reference 以及原验证结果。几何核对仅解析坐标、计数和比较元素标记的连接图，能量核对仅从已存输出作差；本次没有新量化计算。本次只执行归档、论文索引更新和本节分析记录，没有修改四个任务包、docs/verification 或历史输出，也没有把 SI/作者结果加入 agent_input。

### 22.2 paper_43d74f8a469d9ad3（Group 1；AR、PR）

**当前任务仍有计算支持，但 SI 本身的结构表标题不可直接采信。**当前公开输入是实验 CCDC 2441197 的 48 原子 C23H20BNO3，研究 compound 1 的 B–3,5-dimethylphenyl 扭转轮廓。正文 p2/Scheme 1、p3/§2.4.1 与 SI pp21–22/Table S1–S2 支持这一身份。公开 CIF 的晶胞 a/b/c、三角度及选定 B–O/B–N/B–C 距离也与 Table S1–S2 一致；没有证据要求把它换成其他化合物。

直接提取 SI 四个坐标表并逐一统计：

| SI 表及 PDF 页 | 表标题标注 | 实际坐标组成 | 与当前 compound 1 的关系 |
|---|---|---|---|
| S5，pp32–34 | compound 1 | C25H25BN2O3，56 原子 | 不同对象；存在第二个 N 及二乙氨基连接，和正文 compound 4 的结构类型相符，不能用作 compound 1 输入。 |
| S6，pp34–35 | compound 2 | C23H20BNO3，48 原子 | 与当前实验 CIF 的元素标记连接图同构；组成及连接支持实际为正文 compound 1 类型。 |
| S7，pp35–36 | compound 3 | C23H20BNO5，50 原子 | 与正文 compound 3 的组成相符；不是当前任务对象。 |
| S8，pp36–38 | compound 4 | C24H22BNO4，52 原子 | 与正文 compound 2 的组成相符；不是当前任务对象。 |

计数来自每个表完整坐标行；S5/S6 表格也作了图像检查，排除仅由文本标题串接造成的误判。连接图比较不是键级、绝对构型或全部作者计算归属的认证；S5/S8 的具体错位对应属于结合正文结构图的判断，不替作者改写原 PDF。另，Table S1 的 formula weight 写 396.21，而同式 CIF 为 369.21；当前任务不以分子量作为评分量。

**扭转图及验证的影响：**SI p46/Fig. S57 确实是 compound 1/3 的 E(θ) 和积分曲线；当前 paper_route 对“扭转图是 S57”的纠正有直接原件支持。S58/S59 图像实际是平面/角度示意，图注却重复 S57，不能据图注把它们当另外两套扭转数据。S57 没有配套逐点数值表，也未给出可直接对应现有有序四原子编号的完整角度零点/方向定义。

历史有效链仍为正确 48 原子对象的 PBE0/def2-SVP Opt/Freq（138 个正模）加 24 个刚性单点，局部验证的采样能垒为 18.266546 kJ/mol。图中蓝色曲线与历史计算均呈有有限势垒的双峰轮廓，但本次没有数字化、相位拟合或对 SI 每一点作数值复现认证。不同角度零点/方向的曲线不能按横坐标直接逐点判错。compound 1 与 3 的差值、积分能、光漂白速率仍不属于当前只算 compound 1 的必评量。

**建议处理：**保持当前 task、实验 CIF、科学目标和评分范围；不将 S5/S6 的作者计算坐标替换成公开输入，不因 SI 到位自动增加 compound 3 或 TD/光漂白计算。后续定向更新两模式的 `paper_route.md`、`evaluation/evidence_map.json`、`evaluation/verified_computation_reference.md`，写明归档位置、SI 表题错位和 S57 的证据范围。`scoring_rules.json` 中仍有 “Missing source SI curves” 的过时原因说明，可改为“现评分未定义逐点图像数字化数值靶”，保留规则实际科学要求。该说明更新不需要新增量化计算；若另行要求精确复现作者整张曲线，应先解决角度/对象映射和参考数值口径，不能直接套用存在错标的坐标表。

### 22.3 paper_c28b0a1c549f4575（Group 4；AR、PR）

**SI 支持当前对象和作者路线，未发现需要更换任务输入的内容。**SI pp2–3 的合成及 p8/Fig. S1–S2 确认 DEDABCO 是两端 N 均乙基化的 DABCO 二价阳离子，与公开分子图、+2 电荷一致；TEA+、BF4−、PC 的身份也一致。SI pp5–6/§5 明确 Gaussian16、B3LYP-D3BJ/def2-SVP 优化/频率、B3LYP/6-311+G(2d,p) 离子–溶剂结合能。现有十份单点的真实输入均使用后者，前驱频率/对象和 component bookkeeping 已核对；正文–SI–验证的方法主线可直接对上。

**需纠正上一轮私有说明的一处判断：正文 Fig. 2d 有明确数值标签。**直接查看正文 p4 图像可读到下表数值，之前 paper_route 的“qualitative, not machine-readable / without a recoverable numerical table”不应被解释为原图没有数值。它是图中标签，不是 SI 新增表，也不能因文字抽取漏字而当作不存在。

| 对象 | 正文 Fig. 2d 标注 / kcal mol−1 | 历史验证两个取向 / kcal mol−1 |
|---|---:|---:|
| TEA_PC | −17.46 | −13.187403、−12.821987 |
| BF4_PC | −20.09 | −16.540811、−16.539528 |
| DED2_PC | −35.49 | −30.088727、−29.647527 |

当前两模式 evaluator 的必评结果为 DED2_PC 比 TEA_PC 结合更强，并检查三对体系、有效最低点、能量记账和至少一项敏感性；**没有以 Fig. 2d 三个数值设置 numeric 硬靶**。既有计算对已检两个取向均得到同一强弱排序，因此继续支持当前任务的科学结论；不能据此宣称三项绝对能量已逐值复现。SI 未提供这些配对结构的 Cartesian 坐标、完整 Gaussian 输入、逐对象总能表或 BSSE 等全部细节，当前证据不能唯一确定数值差异来自哪个因素；不得归咎于某个参数或用验证值覆盖论文值。

**建议处理：**保留当前科学任务和排序标准；在后续私有来源说明/reference 更新中把 Fig. 2d 标签值与本地验证值并列，明确“排序得到验证，逐值复现未成立”，补上 SI §5 的直接页码和链接。当前范围无须因 SI 到位自动增加数值硬评分或重算。如果未来改成精确绝对能量复现任务，则是新的评估边界，须先解释上述差异。

SI 的 electrode adsorption、frontier orbitals 与 MD 属于该论文其他计算分支，不能因文件完整就自动加入这次已批准的孤立对结合能子题。MD 段写“step size of 2 nm”、正文所引模拟盒表号与实际 Table S2 不符等源文问题，不影响当前量子化学结合能任务；若以后扩展 MD 应单独澄清。

### 22.4 整体影响和本轮边界

两篇 SI 已归档，前文缺存事项关闭。以当前已选科学目标和 evaluator 为准，**没有发现因新增 SI 而必须更换公开输入、改变结论、迁入 hold 或新增量化验证的依据**。新增 SI 使原件依据更完整，同时明确暴露了来源表题错位和旧私有说明错误；不能简单汇报为“全部原文无矛盾”。

推荐的下一步是上面列出的私有来源说明同步，保留任务目标、评分强弱顺序和真实历史输出；本次请求为归档与影响分析，四个任务包及评分文件保持原版本。归档 PDF 保留在 papers 私有论文库，不进入任何 agent_input。现有输入包校验与显式 final 加载另行检查，不以 SI 存在替代实际运行隔离或 LLM judge 检验。

归档后收尾检查已完成：两份 PDF 均可读取，页数、首页题名、索引路径与文件完整性一致，两个 tasks/tmp 源路径已迁出；四包 `validate_task_package` 及显式 `TaskRepository.from_final` / `load_runtime_evaluation` 加载均通过，评分 policy 仍为 `dual_axis_100.scientific_results.v1`。四包相对当前 Git 版本无内容差异，本节两处本地 PDF 链接有效，维护报告差异格式检查通过。这些检查确认归档和任务加载正常，不代表新增科学计算或绝对能量逐值复现。

## 23. 2026-09-26 新通过验证任务的去重、证据核对与复制归档

### 23.1 本轮范围与接收标准

本轮按负责人的要求，先检查 `docs/verification/all_verified_tasks/group_1.md` 至 `group_6.md`，再与两模式的 `final_verified_*`、`hold_verified_*` 及现有 verified_tasks 比对。不是把历史文档出现过“通过”的论文全部当新增，也不是把一个模式的资格自动扩展到另一模式。此次识别的 9 个 paper_id 在核对时均未进入任一 final/hold，且不存在要覆盖的 staging 包；已有 final/hold 的论文不重复复制。Group 6 本轮没有新增接收项。

对候选逐一阅读当前 canonical 的 task、公开对象定义、提交 schema 和五个 evaluator 文件，对照正文/SI、最新 qualification/closeout、结构化实算结果及 Gaussian/ORCA 原生输入输出。检查了研究对象、电荷/自旋、方法与温度/溶剂、能量零点、最低点/TS/受限状态、必要路径及最终评分量。采用正文/SI 为科学依据、真实验证输出为可计算性证据；遵照负责人的口径，允许验证者知晓作者路线和 SI 结构，不要求已有验证必须是公开输入盲测。

在证据支持的模式中，从 `tasks/autonomous_research/<paper_id>` 或 `tasks/paper_reproduction/<paper_id>` **完整复制**到 `tasks/verified_tasks/<mode>/<paper_id>`。源文件保留，目标事先不存在。复制时的 Git 基线为 **`92647470`**，便于将后续修复与本次原样接收区分。本轮只新增 `evaluation/verified_computation_reference.md` 并刷新对应 manifest，未修订科学目标、公开结构、task/schema、paper_route 或五个 evaluator 文件。

### 23.2 逐篇接收清单与实际计算支持

AR=自主科研；PR=论文复现。表中模式链接直接指向该包新增的 reference；详细方法、原始输入/日志、能量账本、评分项对应和证据边界均在 reference 中。

| Group | 论文 | 已复制模式 / reference | 实际计算对当前子目标的支持 |
|---|---|---|---|
| 1 | `paper_d83e607f125440cc` | [AR](autonomous_research/paper_d83e607f125440cc/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_d83e607f125440cc/evaluation/verified_computation_reference.md) | 2g/2a 母体与脱 H 片段最低点、H 单点和 Hirshfeld 分析；硫自旋 0.400976，电子 BDE 198.527743/172.594617 kJ/mol，满足现有数字靶及 2g 较高的结论。历史正式提交为 PR，AR 只共享同一科学子问题的实算支持，不虚构自主过程。 |
| 2 | `paper_2877efc02814175d` | [AR](autonomous_research/paper_2877efc02814175d/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_2877efc02814175d/evaluation/verified_computation_reference.md) | 三个 65 原子 +2 配合物的最低点及 Co 波函数稳定性；DMSO 模型的 gap/硬度 Cd>Co>Ni、亲电性 Ni>Co>Cd，与新找到的正文 Table 1 一致。使用实际可读正文，未把旧损坏 main.pdf 当作有效依据。 |
| 2 | `paper_8fefc96b015c4577` | [AR](autonomous_research/paper_8fefc96b015c4577/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_8fefc96b015c4577/evaluation/verified_computation_reference.md) | 中性 doublet 的 B 与两个 TS，最低点/唯一相关虚频及同零点 Gibbs 比较；两势垒 13.253000/19.257011 kcal/mol、差 6.004011，满足原 13.08/19.25/6.17 的容差。提供虚频位移证据，不冒称已算 IRC。 |
| 3 | `paper_9ec32e81e2826041` | [AR](autonomous_research/paper_9ec32e81e2826041/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_9ec32e81e2826041/evaluation/verified_computation_reference.md) | 两套正确 80 原子构象在 300 K 同层级优化/频率，各 234 正模；coplanar−perpendicular 为 −0.047259 kJ/mol，支持 SI −0.1 所表达的近等能比较。 |
| 3 | `paper_1a47bc00fd63b2f5` | 仅 [PR](paper_reproduction/paper_1a47bc00fd63b2f5/evaluation/verified_computation_reference.md) | 两条环化通道的 TS/最低点、同几何高层单点、真实 IRC 已接受路径及后继自由优化；para−ortho 势垒差 +7.528200 kcal/mol，符合 +7.6±1.5。源库本来没有 AR 包，未自行创建。 |
| 4 | `paper_9132719dbf91c978` | [AR](autonomous_research/paper_9132719dbf91c978/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_9132719dbf91c978/evaluation/verified_computation_reference.md) | INT-G→TS6 的完整 77 原子最低点/TS、高层单点、双向 IRC、后继最低点及 H2 释放/片段验证；势垒 0.764432 kcal/mol，满足 0.9±2.0。区分初始结合 H2 与最终分离 H2。 |
| 4 | `paper_0e835b370ddd37b6` | [AR](autonomous_research/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md) | 正确 silylene 1/V′、H2、两 TS、实际双向 IRC/四个直接端点及波函数检查；分离反应物零点势垒 33.065984/47.132237 kcal/mol，与作者 32.9/47.4 的比较和排序一致。未使用旧错误 61 原子对象。 |
| 4 | `paper_2a71ffa4b0a90809` | 仅 [PR](paper_reproduction/paper_2a71ffa4b0a90809/evaluation/verified_computation_reference.md) | 连续 15 个有效电子扫描几何、6 个 Gibbs 状态、受限切向曲率与敏感性；原生热化学口径势垒 30.003738 kcal/mol，落在 31±1 内但非常靠近下界。AR 的定义/频率要求未与该证据对齐，未复制。 |
| 5 | `paper_72822e4ddb5d9b11` | [AR](autonomous_research/paper_72822e4ddb5d9b11/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_72822e4ddb5d9b11/evaluation/verified_computation_reference.md) | 165 原子 complex 4 的 singlet 优化和独立 Hessian、相同网格/基组的 triplet Opt/Hessian；两态均无负模，triplet−singlet 为 +32.219903 kcal/mol，支持现有正 gap / singlet 更低的评分，不改成新数值硬靶。 |

共 **9 篇、16 包：AR 7、PR 9**。本批按原包保留 **52 个关键点、22 个结论**；其中仍存在旧 limitation 类评分，不把它们算成已完成发布清理。原始步骤记录只纳入有效计算及形成有效端点所必需的真实结构传承；失败扫描/IRC 日志只引用明确已接受的前缀，不把失败尾部能量、频率或“达到最大步数”冒充收敛最低点。原始失败日志没有删除或改写。

### 23.3 没有直接通过、仍需后续整理的事项

**1. `paper_2a71ffa4b0a90809` AR 不接收。**当前 AR 把 F 定义在芳环上并与特定环碳键连，而成功源路线使用 F27–C10–C13–I28，F 在中央 linker；同时 AR 要求所有做频率检查的推进态无虚频。实际连续受限剖面的三个状态各有一个完整 Hessian 负模，真正验证的是剩余自由方向的正切向曲率。当前 PR 已明确区分受限状态与自由最低点，故 PR 可归档，而 AR 尚不能由同一链证明满足其全部原文字要求。[09-26 当前资格处置](../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/current_target_disposition_20260926.json)也只选择 PR。本轮没有复制 AR、没有把它移入 hold，也没有代改其任务。

此外，PR 主值 30.003737993 距下界仅 0.003737993 kcal/mol；独立近零起点为 29.946634631，50/100 cm⁻¹低频处理诊断为 29.731694702/29.327035556。这些真实敏感性不推翻原生约定下已有的通过结果，但说明不能宣称硬评分对所有合理热化学实现都稳定。发布整理应明确口径并审查现有容差的稳定性，不能通过四舍五入、隐藏对照或自行扩容差来处理。

**2. `paper_d83e607f125440cc` AR 没有历史独立提交格式。**两模式研究对象、三个必评科学关键点及数值目标相同，真实计算可支持 AR 的科学可行性，符合负责人允许作者知情验证的要求；但历史 JSON 只符合 PR schema，缺少 AR 成功分支的 `investigation` 对象（`plan / models_or_conformers / coverage / stopping_rule`）。这不是新的量化计算缺口，也不是可以伪造的历史自主轨迹。reference 已明确说明，不把“可支持科学子问题”写成“已有 AR 盲测成功”。

**3. 两篇私有 paper_route 的旧方法文字需要后续修复。**d83 仍有 `HF-based BDE`，而 SI 和真实计算是 B3LYP；8fef 仍有 `neutral closed-shell`，而真实三个对象为 neutral doublet，当前公开指令已如此定义。这些是已定位的私有说明不一致，未据此更改当前数值结果，也未在本轮复制归档中擅自修改原任务。reference 已记录真实方法，下一轮按维护流程同步对应说明。

**4. 论文库原件及公开输入边界仍需整理。**2877 的可读正文位于 group2 的 `source_data/user_supplied_20260925/`，原 `papers/.../documents/main.pdf` 仍损坏；reference 链接到真正可读文件，不声称已修复原库。9ec 的两个 process 项绑定相近驻点证据，后续应检查重复计分。8fef/9ec/728 等给定作者对象的性质比较任务，仍须在发布整理时围绕待求科学目标判断坐标信息边界；仅复制和证明结果可计算，并不等于完成了无泄漏审计。1a47 的共同能量零点不能误解成两条反向 IRC 必须进入同一构象盆地，其路径证据和真实软模修复已明确记录。

**5. 本轮不做科学扩题或强制新计算。**未增加论文其他分支，不要求从公共初始结构重新盲跑，不要求重现所有论文数字，也未把 reference 改成主要评分手段。作者结果与本地结果有差异时按现有 evaluator 的实际定性/定量要求判断，并分别记载，未拿本地值覆盖作者值。已入 verified_tasks 表示有可追溯科学计算支持、可继续整理，不等于可直接发布。

### 23.4 归档完成后的实际检查

使用本仓库环境进行逐包检查，未调用 LLM judge 或新增量化计算。

| 检查 | 结果 |
|---|---|
| 复制完整性及范围 | 16 包，176 个非 manifest 原有文件与 canonical 源逐字节相同；无覆盖、无软链接；新增只有各自 reference，另刷新 manifest。候选在 final/hold 无重复。 |
| 计算档案 | 16/16 已写入；全部逐项映射当前关键点、结论及评分规则；408 个本地文件链接均存在。原始日志能量、频率数及正常结束/仅有效前缀状态已按步骤核对。 |
| JSON / 包校验 | 129 个 JSON 均可解析；`validate_task_package` 16/16 通过。 |
| 暂存库实际加载 | 显式 `TaskRepository(roots=[tasks/verified_tasks])` 加载 16 包，`load_runtime_evaluation` 16/16 通过；原 policy 为 `dual_axis_100.v1`，未冒称已迁到 final 的 scientific_results 新政策。 |
| 历史结果 schema | 15/16 与当前模式 schema 相符；唯一例外 d83 AR 为上述已披露的 PR-to-AR 格式差异，没有编造字段以凑齐通过数。 |
| 当前数值评分绑定 | 15/15 numeric 规则以真实历史结果按现有字段和容差检查通过；这不是全部 LLM/语义规则已运行的满分声明。 |
| 最后参数及汇总链接复核 | 117 处 reference 中的 Gaussian route 与对应原始日志逐项一致；本节 17 个文件链接均有效，差异格式检查通过。 |

收尾时还逐项比较了 reference 所链接 Gaussian 输入与实际输出回显。9132 的 5 个步骤、0e835 的 6 个步骤在留存输入中设 MaxCycles=300/400，实际有效日志为 MaxCycles=8；它们均有 Optimization completed、后续频率分析和正常结束，route 的其他关键词相同。两论文两模式的 reference 已按实际日志记载该参数，并披露留存输入版本差异，避免把输入模板当成真实执行记录；没有更改原始输入、日志或科学结果。

本轮没有移动任何 final/hold 包，没有写入 `docs/verification`、论文/SI或历史计算文件，没有提交/停止 HPC 作业。接下来的任务规范化、limitation 清理、输入泄漏/缺失和评分清晰性修复，仍应依照维护流程在 verified_tasks 中进行；是否迁入 final/hold 另待负责人确认。

## 24. 2026-09-26 本批 9 篇 / 16 包的首次发布维护审查与待确认修订方案

### 24.1 范围、授权与当前结论

本节接续第 23 节的接收记录，不覆盖之前批次。当前工作包为 **9 篇、AR 7 包、PR 9 包**，具体清单见下表。修复前版本已包含于 Git **`940d3d04e237cc5410a5613a673f4f32bed5407e`**；审查开始时这 16 包无未提交修改。已有未跟踪的 `SCIENTIFIC_REAUDIT_20260917.md` 和仓库其他工作不属于本次，保留不动。

负责人本轮要求按维护流程逐包处理。流程第 2.2.1、2.4、2.5 节要求先交付有原文和真实输出依据的具体修法，再取得修改批准；迁移另行确认。因此**本轮完成首次逐篇科学、输入、评分、提交契约和档案审查，只追加本节报告，尚未改 task/schema、输入、evaluator 或 reference**。下面所有“拟改”“建议”均为待批准方案，不能当成已经修复。全部仍在 verified_tasks，未移入 final/hold。

总体判断：已有作者知情验证对这 9 篇的选定科学子目标提供真实计算支持，本轮没有据此判定必须新增量化计算。但 **16 包尚不能直接签发可发布结论**：普通 limitation 门槛仍在，若干成功/失败分支与对象覆盖存在可复现的格式漏洞，部分任务的公开条件和私有评分预期未对齐；`8fef…` 的给定 TS 边界和 `2a71…` 的数值接受稳定性必须明确。作者知情验证成立，不等于公开输入、评分和部署隔离已经全部合格。

以下 PDF 页码均为文件的 1-based 页序；计算链及其原始输入输出链接沿用各包的 reference，未以摘要中的 PASS 标签替代输出检查。科学过程的历史事实不因当前格式问题而失效。

| Group | 论文 | 工作包 / 计算档案 | 当前 K / C（每模式） | 拟清理后 K / C（每模式） | 首次审查判断 |
|---|---|---|---|---|---|
| 1 | `paper_d83e607f125440cc` | [AR](autonomous_research/paper_d83e607f125440cc/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_d83e607f125440cc/evaluation/verified_computation_reference.md) | 3 / 1 | 3 / 1 | 实算支持；需明确电子 BDE 口径、清理声明及提交契约 |
| 2 | `paper_2877efc02814175d` | [AR](autonomous_research/paper_2877efc02814175d/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_2877efc02814175d/evaluation/verified_computation_reference.md) | 4 / 2 | 4 / 1 | 实算支持；需修对象覆盖、状态绑定及 limitation 关联 |
| 2 | `paper_8fefc96b015c4577` | [AR](autonomous_research/paper_8fefc96b015c4577/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_8fefc96b015c4577/evaluation/verified_computation_reference.md) | 4 / 1 | 4 / 1 | 实算支持给定三结构比较；TS 输入角色须确认，不能称为独立 TS 搜索 |
| 3 | `paper_9ec32e81e2826041` | [AR](autonomous_research/paper_9ec32e81e2826041/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_9ec32e81e2826041/evaluation/verified_computation_reference.md) | 3 / 1 | 3 / 1 | 实算支持；近等能判据与方法自由冲突，过程项重复 |
| 3 | `paper_1a47bc00fd63b2f5` | [仅 PR](paper_reproduction/paper_1a47bc00fd63b2f5/evaluation/verified_computation_reference.md) | 4 / 2 | 4 / 1 | 实算支持；共同能量零点、实验观测角色及分支需澄清 |
| 4 | `paper_9132719dbf91c978` | [AR](autonomous_research/paper_9132719dbf91c978/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_9132719dbf91c978/evaluation/verified_computation_reference.md) | 3 / 1 | 3 / 1 | 实算支持；计算条件需与数值评分一致，修 success 分支 |
| 4 | `paper_0e835b370ddd37b6` | [AR](autonomous_research/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md) | 3 / 2 | 3 / 1 | 实算支持；私有最终规则缺明确正确方向，失败不应等同成果成功 |
| 4 | `paper_2a71ffa4b0a90809` | [仅 PR](paper_reproduction/paper_2a71ffa4b0a90809/evaluation/verified_computation_reference.md) | 4 / 2 | 4 / 1 | 受限剖面实算成立；硬数值评分稳健性待决定，暂不建议无条件发布 |
| 5 | `paper_72822e4ddb5d9b11` | [AR](autonomous_research/paper_72822e4ddb5d9b11/evaluation/verified_computation_reference.md)、[PR](paper_reproduction/paper_72822e4ddb5d9b11/evaluation/verified_computation_reference.md) | 2 / 1 | 2 / 1 | 实算支持；明确绝热电子能差，补上结果字段与评分绑定 |

当前合计 **52 个关键点、22 个结论条目**，其中 6 个结论为纯 limitation。按下面方案取消这 6 项后预计为 **52 个关键点、16 个科学结论**；`2a71` 的混合 `kp_limits` 中真实敏感性工作保留，不删除实质计算。该计数是拟改结果，不是本轮已完成变化。每包剩一个综合科学结论不自动说明任务简单，也不自动等于二元评分；其已要求的独立成果应在规则中可区分完成程度。不新增计算目标来凑结论数，不改双轴公式。

### 24.2 已完成的实际检查与适用范围

1. 逐模式读取公开 task、schema、数据、task_info、五个 evaluator JSON、后台 paper_route 和现有 reference；核对正文/SI 的对象、方法和对应图表，不把另一模式的题面当成相同文件。
2. 重新解析 **129 个 JSON、31 个 XYZ**；XYZ 核对声明原子数、完整坐标、有限数值和元素组成。全批 **64 个 agent_input 文件**；没有包内软链接。`2877` 的 XYZ 使用原子序数而非元素符号，公开说明已声明，不能直接判为错误元素；后续可做等价格式规范化，但不能顺带改变坐标。
3. `validate_task_package` **16/16 通过**；显式 `TaskRepository(roots=[tasks/verified_tasks])` 和 `load_runtime_evaluation` **16/16 加载成功**。实际 policy 全部为 **`dual_axis_100.v1`**，并未完成 scientific_results 策略接入。
4. 当前 schema 的合法性检查通过。将真实历史结果分别交给当前模式 schema 及实际 `validate_output_contract` 检查，均为 **15/16 通过**；唯一不匹配是 d83 AR 缺 `investigation`，而同一份历史 PR 输出有效。未伪造一个不存在的自主搜索过程来补齐。
5. 数值规则共 **15 条**，按其当前字段、单位解释和容差用真实结果核对，算术上全部落入范围。当前运行时 `check_rule` 直接处理其中 **11 条**；d83 两个 spin 规则因单位字符串不是简化白名单中的 `dimensionless`，1a 和 2a 两条因条件规则，返回 `requires_semantic_review`。因此不是“全部自动评分已通过”，更不是 LLM judge 已给满分。当前规则关联未发现悬空 reference_id；关联存在也不能排除下述语义/字段缺陷。
6. 对 9 条共享作者路线重新读取 reference 表内 **73 个原始输出条目**：其中 67 个终态/单点/路径步骤的 E、适用 G、频率数与表值一致并具有相应正常结束记录；其余 6 项按档案限定只使用已接受 IRC/扫描前缀，不拿尾部失败量计入结果。2a 扫描日志前段虽有正常结束字样，末尾仍明确 `Disk quota exceeded`，未误报全日志成功。ORCA 的 495 个模式包含整体平移/转动零模，未把这些零模当成虚频。没有新增电子结构求解。
7. **408 个 reference 本地链接均存在**。现有记录已列必要步骤、方法、数值、成功前缀及限定范围，故本轮不重复覆盖档案。未来修复 evaluator ID/量定义后，只同步当前对应关系，保留历史真实计算和论文/验证值区别。
8. 重新检查公开拷贝实现：`materialize_agent_files` 仅拷贝 agent_input，runner 的任务提示使用题面及明确的 data/deliverables 字段，没有把本批 reference 自动列为输入。**这只是包内与代码路径检查，不是实际容器、挂载、网络和工具权限隔离认证。**正式发布部署仍应按维护流程检查，不在本轮启动模型或 judge。

下表是**在内存中修改既有结果构造的格式反例**，仅用于软件诊断，不是科学计算，不写入 group/reference。ACCEPTED 只表示 schema 接受，不代表语义 judge 必然给分；问题在于提交契约没有兑现公开完整性约束。

| 包 / 模式 | 已实际测试的反例 | 当前行为 | 拟修复 |
|---|---|---|---|
| 所有 15 份本来能通过 schema 的模式结果 | 递归去掉普通 `limitations` / `stopping_rule` | 全部被拒绝；d83 AR 原本已有别的格式不匹配，不凑成第 16 份新反例 | 普通声明变 optional；保留真实失败原因和实质性科学检查 |
| 2877 AR/PR | 三份相同对象替代 Cd/Co/Ni；或 `completed` 对象只留 `failure_reason` 无观测值 | 两类均被接受 | 唯一身份覆盖；成功状态要求实际 gap/硬度/亲电性，失败分支独立 |
| 0e AR/PR | 两份同一 silylene 替代两体系 | 被接受 | 按已公开身份固定必需覆盖；不能把重复对象当另一体系 |
| 0e AR/PR | 无频率结果的早期失败不填 `imaginary_frequencies` | 被拒绝 | 只在成功最低点分支必需；失败允许缺失且有诊断 |
| 8fef AR/PR | `complete` 配失败 comparison；早期失败不填 energy / 虚频数 | 前者接受、后者拒绝 | 顶层/逐态/比较状态绑定，保留完整成功要求，允许真实缺失值 |
| 9ec AR/PR | 重复一个构象；`complete` 配无 ΔG 的失败 comparison | 均接受 | 两构象稳定身份、成功必须有同口径 G 和有符号 ΔG |
| 913 AR/PR | `success` 仅含合法 failure_report、移除驻点/势垒/连接信息 | 被接受 | success 必须包含实际结果及证据；failure_report 不能替代成果 |
| 728 AR/PR | `completed` 移除两个总能和 gap | 被接受 | completed 必需两态能量、gap、lower_state 及有效性字段 |
| 1a PR | completed 只保留一个通道 candidate | 被接受 | 两通道分别有合法主结果，失败尝试另列，不要求失败尝试提供未生成 IRC |
| 2a PR | complete 只有一个 scan state，barrier_result 选无数值的失败对象 | 被接受 | complete 必需至少五个不同有效状态、区间覆盖及真实 barrier；其余为部分/失败 |

### 24.3 获批后共同执行的整理内容

**格式：**先单独把 task.md 统一成 Scientific objective → PR 独有 Author-provided scientific guidance → Public inputs and scientific boundaries → Required scientific validation/investigation → Deliverables。AR 不新增作者路线；PR 把现有合法假设移到独立节，不借格式化增加已知答案。2877 统一现有二级标题，其他任务按实际缺节调整。

**limitation 与失败：**取消普通声明的必填、独立成果分和“没说局限就失败”；不删除频率、TS 连接、物理量定义或原本要求的定量敏感性。移除 2877 两包 `c_limits`、0e 两包 `c_limit`、1a PR/2a PR 的 `c_limitation` 及纯声明规则；把它们原来承载的有效检查接回科学成果。失败可以合法提交已有成果，但不因描述失败完整就得到未算出的科学成果分。固定搜索轮次和无依据的强制停止论述移除，主结果与额外失败尝试分开。

**契约和运行策略：**逐包修成功/部分/失败分支、身份覆盖与字段绑定，成功分支不通过整体放松来兼容失败；原有字段尽可能保留，必要的重命名无损映射。五个 JSON、task_info、schema、paper_route 按影响同步；每包明确使用已有 `dual_axis_100.scientific_results.v1`，不改全局默认或总分公式。数值目标/容差除另获具体批准外保持原值。

**档案和验收：**reference 已完整则不重写；只更新受影响 ID/物理量说明，把旧 limitation 对照标为历史。实际修复记录放本包 `evaluation/task_provenance/maintenance_audit.md`（如需），不另开散落文件；若公开答案结构需移私有，使用 `evaluation/author_results/`。仅重建改动包 manifest，再跑真实结果、边界反例和运行时契约检查。全部在 verified_tasks 完成，不触碰原任务、正文/SI或 group。

### 24.4 paper_d83e607f125440cc：AR / PR

**原文与实算。**[SI](../../papers/paper_d83e607f125440cc/documents/supplementary_001.pdf) pp34–36 的 S6、Tables S8/S10/S13/S16 对应真空 B3LYP/6-311+G(d)、Hirshfeld 和电子 BDE。Table S16 的 “HF based” 是取总电子能的表述，不能据此把方法解释为 Hartree–Fock。真实链是两母体 +1 doublet、脱 H 后 +1 singlet 片段的 Opt/Freq，另加中性 doublet H 单点和 Hirshfeld；四个分子频率分别 54/54/51/51 个正模。S 自旋 **0.400976**，BDE **198.527743115 / 172.594617223 kJ/mol**，差 **25.933125892**。对应 `kp_minimum / kp_spin / kp_bde → conclusion_mechanism`。

**确切问题。**当前 task 要求同口径 BDE，但没有明确现行 198.5/173.7 金标准是电子绝热解离能，而非加 ZPE/热校正后的焓/自由能；字段能容纳不同定义，评分却只认这一组值。后台 paper_route 仍可误导成 HF 方法。schema 还强制普通 limitation；AR 额外 investigation 中的 stopping_rule 也需区分真实过程说明和声明门槛。源科学计算并不缺少 AR 所评量，历史缺 AR 格式不能变成“需重新盲跑”。

**拟改。**明确主量 `D_e = E(relaxed dehydrogenated cation) + E(H radical) − E(relaxed radical-cation parent)`，采用现有 kJ/mol 单位和正确片段电荷/自旋，ZPE/热校正仅可另报，不混入主 BDE；论文电子量不等于强迫逐条照抄 reference 搜索轨迹。修 paper_route 方法说明，数值、容差与科学结论不改。`r_minimum` 绑定实际频率数及证据，不只读一句 validation_statement；spin 的单位可规范为 `dimensionless`，物理定义仍为 Hirshfeld 原子自旋，避免白名单退回但不改变数值。AR 保留独立计划/模型选择这一模式区别，去除泛泛停止/局限必填；不伪造历史 investigation。核对模板内成功结果量类型和有限值。

**输入判断与待确认。**公开母体是已知化学对象，未知的是自旋及两 BDE；仅发现它来自优化坐标不足以认定这些结果已泄露。保留给定对象，不宣称独立构象发现。将含糊 BDE 明确为电子量会改变有效答案集合的歧义，须批准此量定义后实施。已有真实结果直接支持该修法，无新增量化计算理由。

### 24.5 paper_2877efc02814175d：AR / PR

**原文与实算。**真正可读正文为 [用户补充的正文](../../docs/verification/group_2/paper_2877efc02814175d/source_data/user_supplied_20260925/1-s2.0-S0022286025023567-main.pdf)，§2.3 / p2 和 Table 1 / p8；论文库旧 main.pdf 损坏，不将其当证据。[SI](../../papers/paper_2877efc02814175d/documents/supplementary_001.pdf) Tables S1–S3（pp11–13）给三个 65 中心 +2 配合物，Cd/Ni singlet、Co doublet。真实五步含 Co 起始稳定行列式、重新 Opt/Freq 和终态 Stable；三个最低点各 189 正模。gap **Cd 1.980716805、Co 1.515946328、Ni 1.238934416 eV**；硬度同序，亲电性反序，符合正文 Table 1。无需用更接近论文的值替换实算。

**确切问题。**`complexes.minItems=3` 不保证三个不同金属；completed 与 failure-only observables 未绑定。`c_limits` 占一个成果且单独关联 `p_state/p_converge`，直接删会削弱有效性关联。公开末句要求报告 “legacy uniform-singlet metadata” 是维护残留；当前对象自旋已经正确，不应让 agent 寻找不存在的旧材料。标题/PR guidance 尚未规范。

**拟改。**按 Cd/Co/Ni 唯一身份绑定，并核对 metal、charge、multiplicity 一致；三对象完整才是完整比较，个别失败按实际完成部分提交。明确 frontier 选择和公式需要一致、开放壳层必须说明同一自旋通道/适用定义，不给获胜排序。保留现有允许优化或有依据单点的性质任务，不附加全局构型搜索。删除 `c_limits` 及泛泛声明，把 `p_state/p_converge` 接回 `c_trend`；保留 `p_gap/p_desc` 与现有定性排序，不新增正文逐数值硬靶。修完整输入路径、去掉旧 metadata 追问；私有来源链接指向可读正文，不擅改论文库。

**输入判断。**已明确是三个给定配合物的电子描述符比较，结构不是当前待发现答案；不能因 SI 来源就全部删除。实际排序、轨道能量、硬度和亲电性没有写入公开数据。保留这一选定目标后，修复主要属于契约/文字和已批准类型的 limitation 清理。

### 24.6 paper_8fefc96b015c4577：AR / PR（输入角色须决定）

**原文与实算。**[SI](../../papers/paper_8fefc96b015c4577/documents/supplementary_001.pdf) p34 明确所有几何优化；本轮逐原子对照确认公开 B 与 pp36–37、TS2 与 p38、TS2′ 与 pp40–41 的坐标相同（逐坐标差低于 1e−7 Å）。所以“作者优化 TS 作为公开输入”是事实，不是仅根据文件名推断。三者 C21H24F2NO4S、中性 doublet；B 无虚频、TS 各一相关虚频 **−470.6863 / −476.5989 cm⁻¹**。B3LYP-D3/def2-TZVPP/SMD(DMSO) 实算势垒 **13.253000092 / 19.257010740**、差 **6.004010648 kcal/mol**，满足现有参考 **13.08/19.25/6.17 ±1.5**。正文 p4 的能量是相对分离反应物，reference 已正确减去 B 的 −13.13，没有零点错误。

**必须区分的目标。**当前 AR task 已明确 “supplied fixed model geometries”、有限重优化 optional；PR 也给定 B/TS2/TS2′。因此本包目前不是独立 TS 搜索题。给定 TS 的验证/热化学比较有真实计算支持，但若发布说明称其测独立 TS 构建/发现能力，便不成立。不能通过把文件名改成 candidate 或加 starter 注释掩盖这个事实。

**建议与替代。**建议保持当前已选目标，明确它是给定三个结构的驻点/自由能性质比较，保留必要几何，但不得作为独立 TS 搜索基准；AR 自主性仅在计算方案和结果判断。若负责人要求它成为 TS 搜索题，则应把作者 TS 移到私有 `author_results`，公开足够的反应物/中间体身份与中立初态，agent 自建 TS，并重新检查目标、schema、所有评分项；这是实质重设计，不能在本次常规清理中默认实施，也不能据旧固定结构验证宣称已有新题面的盲测通过。

**其他确定修法。**DMSO 是本通道论文/验证条件，当前却准许任意隐式溶剂同时按固定数字评分；建议主比较明确 DMSO 及共同 Gibbs/温度/标准态口径，其他条件另报，不提供势垒答案。是否固定更多方法需单独决定，不默认剥夺所有方法自由。修后台 closed-shell 为 doublet；修 complete/逐态/比较绑定，失败允许没有能量或频率的真实状态，完整结果必须齐全。取消声明门槛和任意搜索禁令；现有 IRC 是增强验证而非硬必评，不因历史没有 IRC 增加补算。四个关键点和 c_final 保留；AR/PR guidance 区别保留。

### 24.7 paper_9ec32e81e2826041：AR / PR

**原文与实算。**[SI](../../papers/paper_9ec32e81e2826041/documents/supplementary_001.pdf) p3 计算方法、Tables S1/S2（pp13–15）和 Table S7（p21）。两个 C35H43NZn、中性 singlet、80 原子构象在 PBE0-D3BJ/6-311+G**、300 K 分别优化/频率，均 234 正模；`G_coplanar−G_perpendicular = −0.047258993 kJ/mol`，对应 SI 含 D3BJ 的 −0.1。

**确切问题。**SI 同表还给不含 D3BJ 的 **+4.8 kJ/mol**；这证明近等能是方法相关结论，不是给定任何“defensible method”都必须命中的普适答案。当前 task 保留方法自由，私有 final 却要求 near-isoenergetic，公开/私有约定不完整。两个 process 关键点文字相同，规则均读驻点验证，未清楚区分对象核对和最低点有效性。schema 可以用重复构象或 complete+failure comparison 通过。AR 两套不同文件名实为同两种几何，不是四候选。

**拟改。**优先建议主比较沿用论文含色散的口径，明确 300 K、有符号定义和色散处理；若要唯一数值可比，再批准源 PBE0-D3BJ/6-311+G** 主协议，其他方法作为另报对照，不强行按同一 near-isoenergetic 文字判错。另一可选修法是保留方法完全自由但改成条件化科学验收，不能一边自由一边藏唯一答案。两者影响接受范围，须先决定，**不私自新增 −0.1 的数值硬靶**。

两个 process 项分别承担对象/标签/电荷自旋核对和优化/频率/G 证据，仍维持 3 个 K，不重复计同一表述。按 coplanar/perpendicular 唯一身份核对两份主结果，G/单位/温度一致且 ΔG 可重算；失败比较不能搭配 complete。AR 删除重复别名或明确唯一规范入口，不改变两个已给定构象的性质比较范围。去除普通 limitation；已有作者路线足以支持上述源协议，没有据此要求新增计算。

### 24.8 paper_1a47bc00fd63b2f5：仅 PR

**原文与实算。**[SI](../../papers/paper_1a47bc00fd63b2f5/documents/supplementary_001.pdf) pp59–61 的方法、Fig. S3、Table S5 与正文 p4 对应。公开 SMILES 定义 substrate 1a 和 bis(4-nitrophenyl) phosphate，中性 singlet 1:1 体系；验证 54 原子。两 TS 虚频 **−267.4872 / −285.8447 cm⁻¹**，INT1 和有效路径后继端点为最低点；低层 Opt/Freq 加高层单点组合给 **19.35518 / 26.88338 kcal/mol**，para−ortho **+7.528199785**，符合 **+7.6±1.5**。历史 IRC 已接受前缀后接真实自由优化端点，未将达到步数上限称为端点收敛；软模修复链已记录，不能仅因日志有失败就否定后续有效计算。

**确切问题和边界。**“共同 catalyst-bound precursor”可被误解为两条反向 IRC 必须终止在同一几何盆地，实际论文/计算可有 INT1/INT1′ 等不同前驱构象；真正需要相同的是势垒能量记账的零点。公开 `system.json.experimental_boundary` 直接给“主要生成 4-hydroxybenzofuran”；它明确标成实验观测，不是偷放计算势垒。但如果宣称本题测试未知选择性发现，就已经给出待判断方向；若题目是解释已知实验选择性，这属于合法问题条件，不能一概定性为计算结果泄露。

**建议。**维持原来的“解释已知实验观测、计算比较两通道”PR 范围，明确实验观测不是可替代计算的成果，也不给数值势垒；定性 hypothesis 放 guidance。若负责人希望连方向也未知，应批准删除观测并改成中立比较，不能偷偷改变职责。明确两条势垒都用相同参考 G；IRC 可以到达各自对应的前驱构象，但需解释与共同参考的关系，禁止各减自己的 G 后冒称共同零点。

修完整结果两通道覆盖；候选中失败/未做到频率或 IRC 时允许报告已有证据和原因，不逼填虚假路径。成功主候选仍需要单一相关虚频及连接证据；额外失败尝试不使已验证主候选失效。删除 `c_limitation`，保留 `kp_process_stationary / kp_process_irc / kp_result_order / kp_result_delta → c_final_kinetic`；不放宽 +7.6±1.5，不改变两通道。源库无 AR，不新造模式。

### 24.9 paper_9132719dbf91c978：AR / PR

**原文与实算。**[SI](../../papers/paper_9132719dbf91c978/documents/supplementary_001.pdf) p10 方法及 p12 终端 H2 释放路线。对象 C39H34OP2Pd、77 原子、中性 singlet；源路线气相 PBE0-D3BJ/def2-SVP Opt/Freq，MN15/def2-TZVP/SMD(DMAc) 高层单点。实算 INT-G 和 TS6、双向 IRC、后继最低点、结合 H2 的后续释放及分离片段均有记录，主势垒 **0.764432041 kcal/mol**，TS 虚频 **−478.5853 cm⁻¹**，满足 **0.9±2.0**。结合 H2 中间态不能当成已分离 H2；现有 reference 已区分。

**确切问题。**公开任务要求报告溶剂/自由能 convention，却未指定该定量目标对应的 DMAc、温度/标准态口径；隐藏金标准不是任意条件都应得出的值。schema 的 oneOf 只区分 success 字段集合和 failure_report 字段集合，未与 `status` 绑定，实测 `success + failure_report` 无任何势垒也合法。普通 limitations 和停止陈述是强制字段。

**拟改。**明确终端通道的主物理环境和 Gibbs 定义、INT-G 零点；不要把整套催化循环塞进 AR，也不要给 TS 坐标/势垒。主方法是否唯一固定另按可比性决定；至少不能把不同温度/溶剂与同一窄靶混在一起。success 要求有真实 TS、势垒和连接证据，失败分支允许缺失但不得获未完成结论分；主链与额外尝试分开。保留三个 K 与 `c_final_barrier` 和现有数值容差。现有宽容差包含略负热自由能势垒，不凭正负号单独追加新失败判据；TS 身份、零点和连接仍须核查。公开 INT-G 是已给反应物，不是待求 TS；保持这一范围无需自动替换所有反应物坐标或重算。

### 24.10 paper_0e835b370ddd37b6：AR / PR

**原文与实算。**[正文](../../papers/paper_0e835b370ddd37b6/documents/main.pdf) pp3–5 的方法和 Table 2：H2 活化势垒 **1 为 32.9、V′ 为 47.4 kcal/mol**。当前公开对象分别 55 原子 C18H33NSi3、36 原子 C17H16N2Si 及 H2，旧 61 原子对象未混入。真实 PBE0-D3BJ/def2-TZVP、苯 SMD、298 K/1 atm 的最低点、两 TS、双向 IRC/四端点和波函数检查支持 **33.065984223 / 47.132236592**，方向与论文一致。

**确切问题。**`c_final` 和 `r_final` 只要求“supported relative conclusion or honest unresolved outcome”，并未把 **1 的势垒低于 V′** 明确写成主科学验收方向。`r_barriers` 要求有数值及零点，但缺方向也可能让相反排序仅凭报告自圆其说；这不是断言现 judge 必然误判，而是标准不够明确。`c_limit` 另占成果分。schema 可重复同一体系填满两项；早期失败却仍必须填数值虚频数。题面固定两轮搜索等停止要求不属于该论文科学结论。

**拟改。**私有 `c_final/r_final` 明确两体系、正确方向和由真实 TS/能量支持的条件；失败可以提交但不能视同得到正确排序。保留现行定性比较职责，不擅加 32.9/47.4 的硬数值容差。公开只要求求出排序，不提前告知谁更低；明确分离 silylene+H2 零点及共同方法/条件。按 system_id 唯一绑定两体系，成功主分支需有效最低点/TS/连接/势垒，失败不强制不存在的频率；取消固定轮次/泛泛声明。删除 `c_limit`，三 K 继续支持 `c_final`。作者路线实算直接支持拟明确的方向，无新增计算要求。

### 24.11 paper_2a71ffa4b0a90809：仅 PR（数值评分决定前不建议发布）

**原文与实算。**[SI](../../papers/paper_2a71ffa4b0a90809/documents/supplementary_001.pdf) p60 方法、pp68–69 的 ModRedundant 说明和图给 69°→0° 受限旋转、约 **31 kcal/mol**；文字内引用 S53/S54/S55 与实际邻近图题编号有错位，必须结合图内容定位。当前 PR 的 C18F12I2、32 原子、F27–C10–C13–I28 定义、SMD(THF)/193.15 K 与成功路线一致，AR 尚不在本批，不借 PR 整理自动修 AR。

真实连续扫描有 **15 个有效电子几何、6 个 Gibbs 状态**；起点最低点和后续自由方向收敛检查存在。受限点的全 Hessian 可有负扭转模，切向自由方向曲率为正，不能按自由最低点零虚频强行否定。主原生 Gaussian 热化学势垒 **30.003737993**，现行 31±1 的下界为 30，仅留 **0.003737993 kcal/mol** 裕量；独立近零控制为 **29.946634631**（只差 0.057103362 却落出阈值），50/100 cm⁻¹低频处理分别 **29.731694702 / 29.327035556**。这些不是缺少计算，而是接受规则对实现选择敏感。

**不能做的“修复”。**不能四舍五入控制结果冒充通过，不能隐藏它们，不能按接近目标挑某条扫描分支，不能因主分支过线就宣称评分稳定，也不能直接把 31 改成本地值或放宽容差。源 SI 未完整说明受限负模/低频热化学的所有处理细节，固定一个主协议能减少歧义，但**单靠固定协议仍不能证明 31±1 边缘判分稳健**。

**可先批准的确定修法。**保留原有受限剖面科学目标，成功分支落实至少五个不同已收敛主状态、覆盖起点到近零、有效最大值和真实能垒；实质 sensitivity 检查保留，把混合 `kp_limits` 改写为具体敏感性/稳定性证据并关联 c_final，删除独立 c_limitation 和泛泛必填。受限状态和自由最低点分别验收；失败/部分分支不造值。

**需要负责人定的发布方案。**建议先保留论文 31 和现有主/控制实算，不宣告本包可发布；在不补算前提下，用已有六点能量、原生热化学、近零控制及低频诊断明确主比较协议和条件化评分方案，再批准是否采用有依据的边界部分分/误差处理，或明确采纳本地 benchmark 参考（须保留论文对照和差异，不能称作者逐值复现）。后者涉及目标来源/评分边界，不在本轮默认执行。若负责人坚持对所有公开允许的方法只用原来的 31±1 硬判，本轮证据不足以认证其稳定性，保持工作区暂缓状态，不自动移 hold。没有因此提交新的量化计算。

### 24.12 paper_72822e4ddb5d9b11：AR / PR

**原文与实算。**[SI](../../papers/paper_72822e4ddb5d9b11/documents/supplementary_001.pdf) p10 方法明确两态分别优化：Ni 与第一配位圈用 def2-TZVP，其余 def2-SVP，比较 B3LYP/BP86；BP86 的 triplet 高 25.1，正文 p4 支持 >20。165 原子 complex 4 是 C87H72Cl2N2NiO，公开 O 原子没有缺失。真实同设置 B3LYP singlet 优化/独立 Hessian 与 triplet Opt/Hessian 共三原生日志，两态无负模，**Et−Es = +32.219903 kcal/mol**，支持当前“正 gap、singlet 更低”的定性评分；不要求与 BP86 数字相同。

**确切问题。**公开“common footing / consistent geometries”没有直接定义绝热（两态各自弛豫）而非垂直能差；当前实算和论文路线是前者。`r_gap` 没绑定数值 gap / lower_state / 两总能，而只看 status、结论文字与 limitations。schema 实测允许 completed 但不含 gap 和两能量，违背题面成功要求。

**拟改。**明确主结果为两态分别弛豫后的电子能差 `Et(relaxed)−Es(relaxed)`、正值含义及 kcal/mol，不混入热自由能或同一几何垂直差；可另外报告控制，但不取代主量。成功必须有两态收敛/驻点证据、各电子能、gap、lower_state，评分实际绑定这些字段并检查相减/单位/身份一致。失败仅报真实可用部分和原因；普通 limitation optional。仍保留 2K/1C 和正负排序标准，不新增作者某一数值硬靶。论文另有 open-shell singlet 初猜，不据此擅自把现有 singlet/triplet 子题扩成全部电子态发现；本题只能报告该比较支持的判断。已给 complex 4 几何用于性质比较，不宣称未知几何发现，实算支持此目标。

### 24.13 修改批准、实施顺序与下一步

请负责人确认后再实施以下具体范围：

1. **共同常规修订：**按 24.3 统一格式、清除普通 limitation、修提交状态/对象覆盖、接回科学证据关联、使用已有 scientific_results 策略；保持所选科学子目标、原数值/容差（除另批）和真实档案。不扩题、不重算、不迁移。
2. **量与条件：**同意 d83 以电子绝热 BDE、728 以绝热电子 gap 为主；8fef/913 明确源物理条件和主 Gibbs 口径；9ec 建议明确含色散的源主比较协议，其他方法另报。将这些从含糊自由选择转为明确主比较，须认可其对接受范围的影响。
3. **输入角色：**8fef 建议保留现有给定 TS 性质比较，不将其列入独立 TS 搜索；若不同意，应另定 TS 搜索重设计。1a 建议保留解释已知实验观测的现范围，不把实验方向的存在误写成未知选择性盲测。
4. **2a 数值边界：**确定性的格式/声明修复可做，但评分稳健性仍单独待决定；当前不自动改 31±1、不自动换本地答案，不宣告发布，也不移动到 hold。

获准后顺序为：保存本报告与批准范围 → 单独格式修订 → 逐包科学/契约清理 → reference 当前关联和 manifest 同步 → 使用真实历史结果及上述反例验收 → 汇报实际变更、未解决项和建议 final 清单。最后再等负责人批准具体迁移。历史作者路线已成功是支持可计算性的证据，**不是允许跳过当前输入和评分问题直接迁入 final 的理由**。

本轮没有修改 `docs/verification`、`papers`、canonical、final/hold 或任何历史输入/日志；没有提交/停止 HPC，没有新增 QM、没有调用 LLM judge、没有实际发布。截止本节写入，变更只有本维护报告；全部任务内容保持上述基线。

## 25. 2026-09-26 获准实施本批修复（工作记录）

负责人已要求按流程完成修复，并明确作者优化 TS 不得出现在公开输入，可保留为私有评估参考。这一决定覆盖第 24.6/24.13 节此前建议保留公开固定 TS 的方案：8fef 两模式改为从中立反应物身份/独立初始几何构建并验证环化驻点，不公开作者 TS 或获胜通道。历史作者知情计算仍用于证明相应科学量可以计算，不声称独立 starter 已盲测成功。

实施顺序：①保存现有审查和任务基线；②单独统一标题/章节格式；③逐包修正量定义、必要条件、输入/提交契约及 limitation 评分；④补充当前证据映射、刷新 manifest、对真实结果和格式正反例回归；⑤汇报剩余边界。所有工作留在 verified_tasks，不修改论文、原始任务、docs/verification 或历史计算，不重算、不迁移、不发布。2a71 的 31±1 数值容差暂保留，评分稳健性另列待决定，不能用格式修复掩盖。

### 25.1 本轮实际完成与发布前判断

本批 **9 篇、16 包（AR 7 / PR 9）** 已逐包完成本次获准修复和验收。**8 篇、15 包可提交负责人作发布前验收；2a71 的 1 个 PR 包仍有下述数值评分边界，不能列入无条件发布清单。**“可验收”不是已经发布或完成了公开输入的独立 agent 盲测；本轮没有启动模型、调用 LLM judge 或作量化补算。

| Group | 论文 / 模式 | 实际修复重点 | 历史计算对当前目标的支持 | 当前建议 |
|---|---|---|---|---|
| 1 | `paper_d83e607f125440cc`，AR / PR | 明确电子绝热 BDE、母体/片段电荷自旋、Hirshfeld 定义；修正 HF 方法误写和证据绑定 | S 自旋 0.400976；2g/2a 电子 BDE 198.527743115 / 172.594617223 kJ/mol；母体/片段 Opt/Freq、H 单点及自旋输出可追溯 | 2 包可验收；AR 历史输出缺自主计划字段不等于缺科学验证，未伪造自主过程 |
| 2 | `paper_2877efc02814175d`，AR / PR | Cd/Co/Ni 唯一覆盖、正确 +2/自旋、DMSO 和一致描述符定义；成功不能仅填失败原因 | 三个对象真实收敛与频率，Co 含稳定性检查；gap/硬度 Cd>Co>Ni，亲电性反序 | 2 包可验收；给定结构的性质比较，不宣称未知几何发现 |
| 2 | `paper_8fefc96b015c4577`，AR / PR | **作者 B/两 TS 全部移私有；公开独立自由基初态和完整连接图，agent 自建 TS**；按通道而非数字/能量映射身份 | 原 B/两 TS 的 Opt/Freq 和负模位移支持同一科学对象、13.253000092 / 19.257010740 kcal/mol 势垒及排序 | 2 包可验收；不宣称新初态已完成盲测，不强加缺失的 IRC |
| 3 | `paper_9ec32e81e2826041`，AR / PR | 明确 PBE0-D3BJ/6-311+G(d,p)、300 K 气相主协议；两个独立构象身份与有效性分开检查 | 两构象各 234 正模；ΔG(coplanar−perpendicular)=−0.047258993 kJ/mol，支持含色散近等能结论 | 2 包可验收；不把无色散控制硬判为错误主结果；仅删 AR 重复文件别名 |
| 3 | `paper_1a47bc00fd63b2f5`，仅 PR | **纠正 ortho/para 参照为游离酚 OH，而非醚氧**；共同能量零点与反向 IRC 前驱构象区分；成功必须两通道 | 15 个有效步骤含真实 IRC 前缀及后继端点优化；两势垒 19.355178322 / 26.883378107，差 7.528199785 kcal/mol | 1 包可验收；已知实验选择性用于解释，不冒充未知方向盲测 |
| 4 | `paper_9132719dbf91c978`，AR / PR | 明确 DMAc / 298.15 K / 1 atm、INT-G 零点；success 必须真实驻点、数值及连接，区分结合 H2 与分离 H2 | 14 个有效步骤含终端释放证据；0.764432041 kcal/mol，符合原 0.9±2.0 | 2 包可验收；不扩成完整催化循环 |
| 4 | `paper_0e835b370ddd37b6`，AR / PR | 两 silylene 唯一对象、苯/298 K/1 atm 和分离反应物零点；私有规则写清正确方向；取消两轮停止要求 | 17 个有效步骤含两 TS/IRC/端点；33.065984223 / 47.132236592 kcal/mol，支持 1 低于 V′ | 2 包可验收；未公开排序或 TS |
| 4 | `paper_2a71ffa4b0a90809`，仅 PR | 修扫描覆盖、真实数值/敏感性、成功/失败分支；保留真实受限曲率检查，删除纯声明分 | 15 电子点、6 个完整 Gibbs 点及控制；主结果 30.003737993，但合理变化可跨现行 30 下界 | **暂不建议发布；原 31±1 未擅改，详见 25.4** |
| 5 | `paper_72822e4ddb5d9b11`，AR / PR | 明确分别弛豫的电子 Et−Es；成功必需两态电子能、gap 和 lower_state，实际绑定数值 | 3 份原生 ORCA 输出，两态无负模，+32.219903 kcal/mol 支持 singlet 较低 | 2 包可验收；不以 BP86 25.1 硬判 B3LYP，也不扩为全部电子态搜索 |

### 25.2 输入、指令、评分和档案的实际变更

- **输入分层：**8fef 两模式共 6 份原作者 XYZ 从 `agent_input` 移入本包 `evaluation/author_results/`，与基线逐字节核对一致；并未删除原参考数据。新公开 XYZ 独立由正确自由基 SMILES 生成，ETKDGv3 固定 seed=20260926，再做 UFF 初态整理；没有用作者坐标作模板、扰动或按答案挑构象。该操作不是量化验证计算。两模式共享相同中立初态，PR 才给两通道的作者指导。
- **新初态检查：**53 原子，C21H24F2NO4S，中性、223 电子、一个自由基电子在第 10 原子；SMILES、显式键表、XYZ 推断连接及元素顺序一致，最短原子间距约 1.0802 Å。与作者 B 的独立连接核对通过。后验重原子对齐 RMSD 约 2.375 Å 仅作来源诊断，不作评分阈值、不作为科学正确性的证明。输出要求明示原子映射和成键原子对；成键索引是该输出坐标的 1-based 行号，不能混为公开初态的行号。AR 候选名可交换，必须先按化学连接确认通道，不能按哪个能量更近来匹配答案。
- **其他输入：**保留已经确定为给定反应物/给定性质对象的完整结构，不因为它曾被优化就一律删除；这与公开最终 TS 答案不同。d83、2877、9ec、728 不被包装成未知几何发现题。1a 的已知实验现象是计算解释对象，并不替代计算证据。9ec AR 的两份重复别名移除，`coplanar.xyz` / `perpendicular.xyz` 均完整保留，Git 可恢复别名。
- **题面与契约：**16 包按统一章节整理；物理量、单位、符号、温度/溶剂、状态和对象覆盖与 evaluator 同步。保留完成与未完成分支，允许真实缺失值，但“能提交失败报告”不等于“完成科学目标”。重复对象、只有失败字段却声明成功、缺少必需计算值等反例被拒绝。额外失败尝试不破坏有效主结果。
- **契约旧层同步：**0e 两包还保留了一份与实际 `result_schema` 不同的旧顶层对象 schema，包含旧的失败频率必填；现已移除这份重复旧层，统一以 `result_schema` 约束 `results.json`。没有改变运行器接口或放宽当前成功分支。
- **limitation：**删除 6 个纯声明结论及相应得分/门槛；最终为 **52 个关键点、16 个科学结论**。每包 1 个真实综合结论，未用空洞条目凑数量；其有效支持项全部可达。普通说明字段允许缺失或为空。2a 的 `kp_limits` 保留为实质数值敏感性工作。进一步清除了“算出结果或解释失败即可”的关键点措辞，失败说明不能替代未计算出的结果。原科学目标数值和容差未改变，spin 仅将单位文字规范成 dimensionless。
- **评分接入：**16 包显式使用已有 `dual_axis_100.scientific_results.v1`，未改全局默认或双轴公式。语义规则仍需基于真实文件判断身份、有效性、结论与部分完成程度，不能仅看 schema 合法或数值接近便给分。
- **计算档案：**原始有效计算链、输出链接和数值保留；旧 evaluator/待修快照标为历史，在每包 reference 第 7 节写入当前关联及适用边界。逐包维护事实集中于 `evaluation/task_provenance/maintenance_audit.md`，8fef 另有独立初态准备记录。reference 依然不作为新评分轴，不导出给 agent。

### 25.3 验收记录与不能夸大的范围

最终离线回归入口为 [test_20260926.py](maintenance_tools/test_20260926.py)。脚本只读当前包与历史结果，使用自动清理的临时格式测试目录；不调用模型、网络、QM 或 HPC。

2026-09-26 收尾运行：**918 项检查通过、0 项失败，退出码 0**；其中包含下述 104 个正反提交案例的两层验证。此数量是软件/文件/映射检查数，不是918次科学计算，也不是对918个科学结论判分。

- 共 16 包、9 篇；包校验及实际运行时加载全部通过。公开文件为 60 个（含 25 个 XYZ），本批包内 JSON 为 133 个，私有作者 XYZ 为 6 个。
- 104 个提交正反案例分别经 JSON Schema 和实际 `validate_output_contract` 检查，均符合预期：真实结果映射、空/缺失普通声明、早期失败、额外失败尝试、合法数组倒序、重复对象和伪完整分支。**格式样例不是新科学验证。**13 包历史结果可按当前格式直接核对；8fef 两包只无损补几何字段和旧/新原子映射；d83 AR 的 investigation 用明确标注 synthetic 的外壳测试格式，未声称历史存在该自主轨迹。
- 实际调用 `materialize_agent_files` 导出 16 包，文件集合逐包严格等于 `agent_input`；无包内软链接，未导出 author_results、evaluator、paper_route、reference 或 provenance。这不是实际容器的挂载/网络隔离实测，部署时仍不得让 agent 访问整个仓库。
- 全部保留规则关联、JSONPath 和科学结果策略可加载；15 条数值规则中简化运行时核对器直接通过 9 条，其余 6 条因化学身份映射或条件分支要求语义审查，**不是 6 条计算失败**。历史主值按原目标/容差的人工算术核对已完成；8fef 另以反应物图和成键对核对映射、相减和 AR 换标签不变性。没有宣称完整 LLM 自动评分已给分。
- 原 reference 的 408 个本地链接有效；初审核过 73 个原始输出条目，67 个适用终态/单点步骤，6 个明确限定的有效路径前缀。尾部失败没有改写成全日志成功，也没有纳入最终数值。当前修订没有篡改历史结果。
- 这组作者知情验证支持“对应科学目标存在真实可计算结果”，不证明任意方法、任意搜索初猜或任意 agent 必定成功。新的自由基初态没有盲测不构成自动补算要求，也不能反过来宣称已经盲测通过。

### 25.4 唯一未关闭的本批科学评分边界：paper_2a71ffa4b0a90809 / PR

> **2026-09-27更正：本节为历史建议，已被第26.1节覆盖。**SI明写SMD18，历史验证为普通SMD，不能称为同一作者协议；因此撤回“仅评分边界、可直接用本地30替换”的建议。以下保留便于追溯，不再作为实施依据。

**不是缺计算，也不是结论被推翻。**SI pp60、68–69 描述 M06-2X-D3 / 6-311+G(d,p)-SDD、SMD(THF)、193.15 K 的受限旋转剖面和约 31 kcal/mol；历史主剖面、独立近零控制与低频诊断均支持高旋转阻力。问题在于当前题面允许选择模型和热化学处理，而 evaluator 用 31±1 作为硬数值标准：主值 **30.003737993** 仅高于下界 **0.003737993**；独立近零控制 **29.946634631** 只变化 **0.057103362** 却会越界；低频 50/100 cm⁻¹处理为 **29.731694702 / 29.327035556**。这些控制不能被偷换成主结果，也不能无视其揭示的判分敏感性。

**建议交负责人确认后再实施：**保持同一分子、F–C–C–I 坐标、连续受限剖面、势垒和刚性解释；把主比较协议明确为已验证的论文方法和原生 harmonic 热化学口径，其他处理作为控制单列；将同一主协议的本地验证值约 **30.00 kcal/mol** 作为 benchmark 计算参考，保留原 **1.0 kcal/mol** 容差，SI 约 31 继续列为论文来源对照而非声称逐值完全复现。这样不扩大科学目标，也不把实验活化能与受限剖面混淆。但它涉及公开方法约定和参考答案来源的实质修改，**本轮没有实施**。若不接受本地参考，应先另定并批准有依据的论文参考评分口径；不建议只把31±1照搬给所有可选协议。

本次已修格式和契约，原靶仍为31±1；继续留在 verified_tasks、标记待决定，不自动移 hold、不补算。负责人只需就上述协议/参考来源作决定，而不是再次审批整个批次的确定性修复。

### 25.5 文件与版本边界

修前任务基线 `940d3d04`；本轮审查/授权记录 `4de62564`；格式单独提交 `5d18a199`。科学修复及最终回归按本批明确路径独立提交，提交说明为 `Repair and validate nine staged research task packages`，不混入其他工作区改动。`maintenance_tools/repair_20260926.py` 和 `finalize_20260926.py` 是一次性补丁生成过程记录，**不可覆盖性重跑**；后续复核使用测试脚本和当前文件。

没有修改 docs/verification、papers、canonical、final/hold 或历史计算文件；没有提交、停止或干预任何 HPC 作业；没有移动任务到 final/hold。既有无关的 `SCIENTIFIC_REAUDIT_20260917.md` 保持未动。该批能否正式迁移和发布由负责人按当前验收结果另行确认。

## 26. 2026-09-27 31 kcal/mol 来源、SMD18 路线及同批八篇重新核查

### 26.1 paper_2a71ffa4b0a90809：原值31正确，验证漏了SMD18，暂缓发布

**结论：不是论文把30写成31，也不能只视为容差边缘；已确认作者方法与验证方法不同。**本次没有用30替换evaluator，没有扩大容差，没有提交任何新的量化计算。本PR包已经从verified_tasks移到[hold包](../hold_verified_paper_reproduction/paper_2a71ffa4b0a90809/agent_input/task.md)，AR未纳入此批、未移动。原因不是断言论文结论错误，而是作者协议的数值验证尚未完成，约1 kcal/mol的偏差不能仅靠文档修订认定已解决。

直接来源：[正文](../../papers/paper_2a71ffa4b0a90809/documents/main.pdf) PDF第5页；[SI](../../papers/paper_2a71ffa4b0a90809/documents/supplementary_001.pdf) S-60、S-66、S-68、S-69、S-85；[实际起点输入](../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_gd3_193K_start_constrained_optfreq_20260914_hpc20_p6/input.com)及[输出](../../docs/verification/group_4/paper_2a71ffa4b0a90809/hpc_runs/1a_s129_gd3_193K_start_constrained_optfreq_20260914_hpc20_p6/stdout.log)；[近零点fchk](../../docs/verification/group_4/paper_2a71ffa4b0a90809/provenance/constrained_curvature_20260925/1a_s129_sequential_endpoint_freq_diskrepair_20260925.fchk)的`PCM-NOrd`与`PCM-SphereRadii`，约869–883行。完整原始链和本次审计见[reference第8节](../hold_verified_paper_reproduction/paper_2a71ffa4b0a90809/evaluation/verified_computation_reference.md)。

| 核对项 | 正文/SI | 历史实际计算 | 判断 |
|---|---|---|---|
| 旋转势垒 | 正文31.0，SI S-68约31；S-69 Gibbs剖面 | 主连续分支30.003737993；独立近零29.946634631 kcal/mol | 原31有原文依据，差异真实存在 |
| 溶剂模型 | 正文略写SMD，SI S-60/S-66/S-69明确SMD18(THF) | `SCRF=(SMD,Solvent=THF)`，未读入修订半径 | **确认不一致**；应优先以SI详细方法为准 |
| 碘腔体半径 | SMD18采用修订Br/I Coulomb半径；准确数值须从S24参数原件核实 | 五份频率fchk的I23/I28均为3.74165773 bohr，即1.98 Å | 不是仅凭名称推测实际用了普通SMD |
| 对象与扫描坐标 | 1a-syn，C18F12I2，0/1；约69°趋向0° | 同对象32原子；F27–C10–C13–I28；69.563620°到0.000243° | 未发现身份错配；该受限终点不等于无约束TS |
| 方法/温度 | M06-2X-D3、C/F 6-311+G(d,p)、I SDD、193.15K | 相应泛函、GD3、基组/ECP、温度、THF一致 | 不宜笼统称“整条路线不同”，明确缺的是SMD18参数 |
| syn起点电子能/G，Eh | −1906.5806471 / −1906.469033 | −1906.58615522 / −1906.474795 | 实际减作者为−3.456397484 / −3.615709589 kcal/mol，电子能已不同 |

SMD18不是“SMD加第18条引用”。SI S24是Engelage等2018年论文 *Refined SMD Parameters for Bromine and Iodine Accurately Model Halogen-Bonding Interactions in Solution*，DOI `10.1002/chem.201803652`；本次也读取了Crossref中出版者提交的摘要，明确其重新参数化Br/I Coulomb半径，其他参数保持SMD。本次未取得该文参数表，不猜填数值，也未将下载失败的HTML当PDF依据。

本地主势垒可拆为电子部分29.449339645与G−E修正差0.554398345 kcal/mol。50/100 cm⁻¹低频控制得到29.731694702/29.327035556，未使结果回到31；只用低频、四舍五入或版本解释缺乏依据。Gaussian A.03/C.01版本、精细网格、近线性相关、精确步长及作者未详细给出的热化学约定可继续核查，但不能冒称已经证明它们是根因。尤其不能把作者起点G与本地终点G拼接相减。

**因果强度：已定位确定的方法缺项；尚未证明该缺项解释全部约1 kcal/mol。**SMD18可能改变不同构象的溶剂化能及优化几何，因而是优先检查的原因，不是已经完成的定量归因。现有高势垒趋势与“1a刚性较高”一致，但“趋势一致”不替代31的作者协议核对。既有15个电子扫描点、6个G点、受限切向曲率分析仍是真实有效结果，不因hold被删除或说成未做过计算。

建议后续：先核实S24准确参数及是否已有真正SMD18输入/输出；若没有，先由获准的计算agent做同几何、同其他参数的普通SMD/SMD18成对单点诊断，再按需要完成统一SMD18下的起点、连续扫描和频率热化学链。单点只能解释电子差异，不能冒充完整Gibbs复现。对照Table S21与剖面后再判断能否恢复验收；仍有差异须报告而非自动换gold。本轮未执行这些计算。

### 26.2 其余八篇：原文、有效计算与当前任务的逐篇结论

本次重新读了各包公开task、数据定义、schema及evaluator，逐篇核对正文/SI相关方法和表格，并回查reference链接的原生日志。以下“支持”指现有作者知情真实计算支持该科学子目标；不是要求从新公开starter完成同一路径的盲测，不是证明任意方法/初猜都成功，更不等于已经获得完整LLM自动判分。

| group / 论文 / 模式 | 原文与实际验证的关键核对 | 本次结论与待处理项 |
|---|---|---|
| G1 `paper_d83e607f125440cc` AR/PR | SI S34–S36的表S8/S10/S13/S16；gas B3LYP/6-311+G(d)，2g为20原子C8H10OS、+1 doublet。母体/碎片有真实Opt/Freq，H原子和Hirshfeld单点。S自旋0.400976对0.401；电子BDE 198.527743/172.594617 kJ/mol对198.5/173.7，原容差±8，排序一致。 | 数值、对象与科学结论有支持；**两包仍有“等效极小点证据”与虚频数必填矛盾，PR混入AR句子**，见26.3。给定母体用于描述符，不是公开待求TS。 |
| G2 `paper_2877efc02814175d` AR/PR | 可读正文Table1与SI对象、B3LYP/LANL2DZ比较；当前PCM(DMSO)验证，Cd/Co/Ni为+2且多重度1/2/1。5步骤含Co波函数稳定性与189正模。gap 1.980716805/1.515946328/1.238934416 eV，对文中1.997/1.511/1.243；硬度与亲电性相应排序一致。 | 未发现新增阻断；准确说明作者溶剂描述与本地PCM实现，不称原文给齐所有隐含设置。公开给定配合物不是自主几何发现；原子序数XYZ已说明。可读正文来源保存在group2 source_data，papers中的坏PDF未被本次改写。 |
| G2 `paper_8fefc96b015c4577` AR/PR | SI S34方法与S36–S41能量/坐标；53原子C21H24F2NO4S、0 doublet。B3LYP-D3/def2-TZVPP、SMD(DMSO)；B/两TS三份有效Opt/Freq为0/1/1虚频。两势垒13.253000092/19.257010740 kcal/mol对13.08/19.25，差6.004010648对6.17。负模成键方向可核对。 | 未发现新增阻断。原B/TS坐标共6份仅在evaluation/author_results；公开为独立SMILES生成初态与键图，无TS答案。AR按化学通道识别，不按能量接近程度换标签。已有链证明同一科学目标可算，不冒称新starter已盲测。 |
| G3 `paper_9ec32e81e2826041` AR/PR | SI S3方法/S21 TableS7；80原子、0 singlet，PBE0-D3BJ/6-311+G(d,p)、300K气相。两构象各234正模，G差(coplanar−perpendicular)=−0.047258993 kJ/mol，对含色散−0.1。 | 未发现新增阻断。题面已有主协议；无色散+4.8是另一控制，不混入主评分。给定两构象是待比较对象，不评价从零发现全局最低构象。 |
| G3 `paper_1a47bc00fd63b2f5` 仅PR | SI S59方法、S60图、S61 TableS5；54原子中性1:1复合物，B3LYP-D3低层Opt/Freq+高层SP、SMD(toluene)。15有效步骤含IRC前缀与后继端点；共同零点势垒19.355178322/26.883378107，para−ortho=7.528199785 kcal/mol，对7.6。 | 当前主计算真实且对齐；**方法自由度与固定数值硬评分不匹配**，见26.3。OH位置参照已纠正；公开SMILES而非作者TS。已知实验选择性只是解释对象，不能替代计算。 |
| G4 `paper_9132719dbf91c978` AR/PR | SI S10/S12；77原子INT-G，PBE0-D3BJ/def2-SVP gas Opt/Freq + MN15/def2-TZVP SMD(DMAc) SP。14有效步骤含TS、IRC两向54/8点、端点及H2释放与独立片段。势垒0.764432041 kcal/mol对0.9±2。 | 未发现新增阻断。结合H2与分离H2在任务和计算链中已区分。公开INT-G为起始反应物，不含TS6。仅支持终端H2还原消除，不外推整循环。 |
| G4 `paper_0e835b370ddd37b6` AR/PR | 正文方法与Table2；55/36原子硅烯体系，PBE0-D3BJ/def2-TZVP SMD(benzene)、298K、分离反应物零点。17有效步骤含TS/IRC/端点；势垒33.065984223/47.132236592 kcal/mol，对32.9/47.4，1低于V′。 | 未发现新增阻断。当前对象、单位、零点及排序一致，输入为反应物/H2，不是答案TS；不以失败说明代替成功通道。 |
| G5 `paper_72822e4ddb5d9b11` AR/PR | SI S10方法/S11 TableS1；165原子complex4，ORCA B3LYP混合def2-TZVP/SVP，分别优化singlet/triplet，3份有效输出与无真实负模。Et−Es=+32.219903 kcal/mol，SI B3LYP31.4、BP8625.1。 | 未发现新增阻断。当前evaluator评电子能比较及singlet更低，不硬性要求25.1或精确31.4，因此32.22支持当前结论但不得写成数值逐位复现。不是要求未知几何发现或全部自旋态搜索。 |

逐包证据入口均为 `tasks/verified_tasks/{mode}/{paper_id}/evaluation/verified_computation_reference.md`，保留原输入/输出链接。此次发现的两篇契约问题须解决后再批准相关三包；其余六篇十二包未发现新的实质性发布阻断，但本轮没有迁入final，也不作“绝对无误”保证。

### 26.3 两处确认的指令/评分契约问题及最小修法（本轮仅报告）

**A. d83，两模式：允许等效证据，但schema强迫填写频率。**

- [AR题面](autonomous_research/paper_d83e607f125440cc/agent_input/task.md)第11行、[PR题面](paper_reproduction/paper_d83e607f125440cc/agent_input/task.md)第15行允许“frequency or justified equivalent evidence”；`r_minimum`也接受等效证据。然而成功schema要求 `minimum_validation.imaginary_frequencies`，类型限定integer；reference_key_points的expected仍只写零虚频。PR题面还复制了“The AR investigation records its plan …”一句。
- 本次用历史真实结果作格式底本，仅在标明SYNTHETIC的测试对象中去掉未计算的频率数并留下等效证据说明，两模式均拒绝：`'imaginary_frequencies' is a required property`。这只是证实契约矛盾，**不是宣称构造了新的科学等效证据**；历史频率结果本身合法且没有失效。
- 建议保留已经公开允许的等效证据入口，使schema明确区分 `frequency` 与 `equivalent` 验证：前者必需真实非负整数虚频数及输出证据，后者必需能证明极小点的可检查证据、无需捏造频率数；普通“优化收敛”不能自动当成等效极小点证据。同步关键点措辞及绑定，不变更BDE、自旋标准；删PR中的AR专属句子。现有频率分支继续兼容，无需为这个格式修复重新做量化计算。

**B. 1a47，PR：未声明量化比较方法，却硬判7.6±1.5。**

- [当前题面](paper_reproduction/paper_1a47bc00fd63b2f5/agent_input/task.md)说明SMD(toluene)、温度/零点、复合能，但没有明确主泛函/基组；[规则r_delta](paper_reproduction/paper_1a47bc00fd63b2f5/evaluation/scoring_rules.json)对完成结果直接用7.6±1.5，即接受区间6.1–9.1 kcal/mol。
- [SI](../../papers/paper_1a47bc00fd63b2f5/documents/supplementary_001.pdf) PDF第61页TableS5给出的B3LYP、BLYP、HF替代单点方法，换成当前para−ortho正号后分别为 **5.95、5.19、5.62**，全部在硬区间外，而方向仍正确；作者主方法B3LYP-D3为7.53，本地为7.528199785。这是原文自带的反例，不是假设“随便一种方法可能不准”。
- 推荐在PR作者路线/主定量比较里明确 SI S59 的 B3LYP-D3/6-31+G(d) Opt/Freq、B3LYP-D3/6-311+G(d,p) SP、Ultrafine、SMD(toluene)、298.15K、共同热化学定义；其他方法允许作控制，不将其硬塞入主方法数值门槛。不给作者TS或结果。现有验证对应这一主协议，无需新增量化计算。该修改收紧了当前未限定的方法选择，**本轮先报告，不擅自改题面**；如果负责人希望继续完全自由选法，则需另行批准方法感知的评分设计，而非简单放大容差。

### 26.4 公开输入、验证适用范围与离线检查

- 重新检查范围为本批9篇16包，非全benchmark。没有在当前公开输入中发现另一处作者待求TS泄露；8fef的作者端点仍私有。d83/2877/9ec/728的给定性质对象，以及913/0e/2a的给定起始反应物，按既定科学目标分别判断，不因曾优化就一概删除，也不把它们宣传为未知几何发现能力测试。此判断仅针对当前包及公开文件导出；运行环境仍必须隔离论文、evaluator和验证档案。
- 重读原文的目的包括核对不同协议、零点、态、温度、修正项和单位，而不只看数值是否进容差。728的32.22与31.4并非完全相同，但当前评分只评有明确证据的能序；2a则有主模型缺项，不能类比为已对齐。
- 移动前原离线回归为918检查/16包/0失败；移动后重新运行同一测试脚本为 **860检查/15包/0失败**。测试没有覆盖所有科学假设，本次针对性检查依然证实d83与1a47问题，不能把860通过解释为15包全部可发布。
- hold包单独 `validate_task_package` 通过；迁移后30个Markdown本地链接存在，公开导出严格只有`task.md`、`submission_schema.json`和`data/inputs/1a_syn.xyz`；当前evaluator适配成功，历史结果仍能通过提交schema。普通TaskRepository不会把hold目录当标准mode目录自动发现，本次使用内存中的单包测试适配器，不改运行器或任务索引，不把hold重新加入可运行清单。
- 相对修前提交 `5dd1e1b8ea1f7efa1a4029834e4a7188ade8d0e8`，hold包只有private paper_route、reference、maintenance_audit和manifest变更；**公开指令、输入、schema、task_info和五个evaluator逐字节保持原样**。没有删除计算数据。其余15包本轮未写入。

### 26.5 本轮实际处理与剩余事项

已完成：原文31与SMD18核实、实际输入/五份fchk/能量重读、同批八篇逐篇对照、两处新契约问题的可复核证据、2a PR可恢复迁入hold、私有记录纠错/链接和manifest维护、本报告更新。

尚未完成：2a在真正SMD18下对偏差的定量解释及作者协议验收；d83两模式的等效证据契约统一；1a47PR的主量化方法约定。后两项可通过任务文档/规则修复，不需要新增科学计算；前一项先找匹配的既有计算，找不到时才提出获准的针对性计算，不将本轮审计冒充重算。

未做：修改docs/verification或论文原件、修改其他任务科学目标/数值评分、启动或停止HPC作业、把任何本批任务移入final、删除任何作者或验证数据。原未跟踪 `SCIENTIFIC_REAUDIT_20260917.md` 保持未动。

## 27. 2026-09-27 两篇指令评估冲突的获准修复与 Group 4 交接

### 27.1 范围与确认结果

负责人要求先复核问题，再依据论文正文/SI/实际验证修复。实际修改仅涉及 `paper_d83e607f125440cc` AR/PR及 `paper_1a47bc00fd63b2f5` PR三个暂存包，以及本批测试/维护记录和Group 4交接指令。修前这三个包与基线提交 `5dd1e1b8ea1f7efa1a4029834e4a7188ade8d0e8` 一致，可查看精确前后差异。

两处问题均已证实，不是仅凭旧报告判断：d83旧schema明确拒绝题面允许的无频率数等效分支；1a47的SI Table S5中不同方法结果保留相同方向，却确实落在主方法硬数值区间之外。原文和原始计算依据仍见第26.2/26.3节、各包reference及本次补记。

### 27.2 实施内容与真实计算对应

| 论文/模式 | 确认的冲突 | 实际修复 | 既有验证是否仍适用 |
|---|---|---|---|
| `paper_d83e607f125440cc` AR/PR | task/r_minimum允许等效极小点证据，但成功schema必需频率数，kp_minimum只写频率；PR误含AR调查句子 | task/schema/关键点/规则统一频率与等效分支；旧频率格式兼容，等效分支允许省略未计算的频率数，但必须给真实证据及解释；不把普通优化收敛或若干方向采样当成完整极小点证明。PR删除AR专属句子，AR保留 | 是。再次核对SI S6及真实2g频率：54正模、0虚频。原6步计算、自旋0.400976、BDE 198.527743115/172.594617223 kJ/mol未变。没有宣称历史采用过等效分支或存在AR盲测轨迹 |
| `paper_1a47bc00fd63b2f5` PR | 未指定主泛函/基组，却以7.6±1.5评分；SI不同方法的5.95/5.19/5.62不能统一受此标准约束 | 公开明确B3LYP-D3低层Opt/Freq、高层同几何SP、UltraFine、SMD(toluene)及一致复合G口径；GD3零阻尼、298.15K/1atm、未缩放harmonic为与实际验证一致的任务实现约定。完整结果必须报告实际method及能量证据，其他方法可单列控制、不替代主结果也不牵连正确主结果 | 是。再次核对三份Opt/Freq和三份SP的真实方法/能量；原19.355178322/26.883378107及差7.528199785 kcal/mol不变。历史method已经包含成功分支所需字段，无需补造结果。原15步链及有效IRC前缀→真实后继端点保留 |

1a47的复合公式为 `G = E_high + (G_low - E_low)`，不重复加ZPE；私有paper_route/reference区分SI明确内容与benchmark实施细节，没有声称作者逐字披露了全部默认设置。没有提供任何待求TS、能量或最终数值到agent_input。

三个包的原始公开数据逐字节与修前基线一致；只修改公开task/schema，私有规则/关键点和维护说明，并刷新manifest。d83仍为每模式3个关键点、1个结论；1a47仍为4个关键点、1个结论，ID及所有数值靶/容差不变。reference第8节和当前规则索引同步更新，历史科学数据没有重写。

### 27.3 修改后检查

- [专项回归](maintenance_tools/test_contract_fixes_20260927.py)：**120项通过，0失败**，涉及三包44个正反提交样例，每个均通过JSON Schema与真实 `validate_output_contract` 双重检查。覆盖旧频率兼容、等效分支缺证据/空证据、错误频率计数、真实早期失败、缺失主协议字段、可选控制和历史结果的数值不变性。合成样例明确标为格式测试，不是新计算证据。
- [整批既有回归](maintenance_tools/test_20260926.py)：**15包863项通过，0失败**。包括包/manifest、历史结果契约、失败分支、科学规则加载和关联、原数值靶/容差、公开文件导出及本地引用。相较前次860项，额外3项来自新增的逐包维护记录链接，不代表新科学结果。
- d83历史科学结果保持原样；AR格式测试仅补明确标记synthetic的investigation外壳，未将未记录的自主轨迹编造为验证事实。1a47历史结果可直接通过新schema，无需改写计算数值。
- 主协议声明不等于已执行相应方法。1a47 `r_delta` 仍为7.6±1.5，评分同时读取差值、method和candidates并要求核对实际输入/输出及能量账本；条件规则交科学语义审查。当前离线检查没有调用完整LLM judge，也没有假称schema能鉴定量化化学方法真伪。d83等效分支同理，不因证据路径非空就认定科学上成立。
- 已读回修改内容并检查局部diff；未改docs/verification、论文原件、canonical、其他暂存包或已有final任务。未运行新QM/HPC，未做实际容器挂载/网络隔离实测。科学可行性来自已核实的真实历史计算，不能由离线检查数量代替。

### 27.4 Group 4 交接与当前状态

交接指令已写到[Group 4 paper_2a71验证差异排查指令](../../docs/claude/group4_paper_2a71_verification_handoff_20260927.md)，可直接交对应agent。它明确：论文31正确；普通SMD与SMD18差异已确认，但尚未证明其解释全部数值偏差；先核实原参数及匹配的已有计算，必要时在获准范围内补针对性诊断和一致的Gibbs链；不把单点诊断当完整验证，不把受限最大点当无约束TS，不直接换gold或放宽容差。

本轮两处已确认的任务契约冲突已经关闭，三个修复包仍在verified_tasks供负责人验收，不自动迁入final。其余六篇十二包本轮没有改动，上一轮逐篇核对见第26.2节，不把本轮软件回归冒称重新完成全部科学审计。`paper_2a71ffa4b0a90809` PR仍在hold，本轮没有进一步改写该包；它的作者协议数值对齐尚待Group 4处理，不能以本轮三个包修复完成代替其验收。

## 28. 2026-09-27 负责人确认后的 final 迁移

负责人确认继续按最后一条有效指令复查并处理。本批复查范围为 8 篇论文、15 个任务包：自主科研 7 个（`paper_0e835b370ddd37b6`、`paper_2877efc02814175d`、`paper_72822e4ddb5d9b11`、`paper_8fefc96b015c4577`、`paper_9132719dbf91c978`、`paper_9ec32e81e2826041`、`paper_d83e607f125440cc`），论文复现 8 个（上述 7 个及 `paper_1a47bc00fd63b2f5`）。

### 28.1 迁移前结论

- 15/15 暂存包通过 `validate_task_package`，manifest、JSON、schema、运行时评分策略和公开导出检查通过。
- `test_20260926.py`：**863/863** 通过；`test_contract_fixes_20260927.py`：**120/120** 通过。两者均为离线契约/字段绑定/公开输入回归，不是新量化计算或 LLM judge。
- 逐篇核对确认：现有真实验证计算支持各包当前限定的科学子目标；`paper_8fefc96b015c4577` 的作者 B/TS 坐标只保留在 evaluator 私有 `evaluation/author_results/`，公开输入是独立生成的自由基初始结构；其余给定结构均按“性质比较/起始反应物”边界判断，不把已知对象误称为待发现答案。
- `paper_2a71ffa4b0a90809` 的 PR 仍有 SMD18 与普通 SMD 的已确认协议差异，约 31 与约 30 kcal/mol 的偏差尚未完成作者协议验收，因此继续留在 `tasks/hold_verified_paper_reproduction/`。

### 28.2 迁移与迁移后检查

按负责人确认清单，完整目录已迁移到 `tasks/final_verified_autonomous_research/` 和 `tasks/final_verified_paper_reproduction/`。迁移只改位置和 reference/maintenance 记录中的相对链接及状态说明；没有改任务输入、schema、五个 evaluator JSON、科学目标、评分数值/容差或历史计算档案。

迁移后逐包检查结果：

- final 目录中的本批 15 个包契约全部通过；
- 显式 `TaskRepository.from_final` 加载本批 15/15 成功，均使用 `dual_axis_100.scientific_results.v1`；
- 迁移后的 15 个 manifest 已定向重建，agent-visible manifest 条目与 `agent_input` 文件逐项一致；
- 迁移后本批 413 个相对 Markdown 链接全部有效；
- `tasks/verified_tasks/autonomous_research/` 和 `tasks/verified_tasks/paper_reproduction/` 已不再保留本批副本；
- final 汇总中的本批计数和迁移日期已更新。

### 28.3 发布边界

这些任务已按负责人确认迁入 final，表示当前包版本完成本流程的内容审查和目录分流。它不表示已经完成新公开 starter 的量化收敛回放、正式 LLM judge、全量 agent 盲测或部署侧父目录/网络隔离实测。正式运行时仍只能向 agent 提供 `agent_input`，不能挂载 evaluation、reference、author_results、paper_route、论文/SI 或 group 输出。


## 29. 2026-09-29 新八篇：原始计算复核、参考归档与暂存审查

> 本节为修前初审记录；修复实施后的当前状态见第30节。

### 29.1 范围与执行结论

负责人本轮明确要求亲自核对八篇真实计算、先写 evaluation/verified_computation_reference.md、再从 canonical 复制并按维护流程处理。依据当前通过登记并排除已在 final/hold 的同论文：本批 8 篇、AR 8 + PR 8=16 包，复制前 staging 0，final/hold 0。不是从修改时间推断新增。

**已完成真实证据核查、16份源 reference、16份完整暂存副本及逐包初审；未修改 task/schema/五个 evaluator，未迁移 final/hold。** 7篇核心限定数值和科学趋势得到既有作者路线支持；Au1 的计算链及定性成键有支持，但两项 DI 原始字面范围未命中，不能说八篇所有定量关键点均严格通过。Au1 按登记语义QUALIFIED接收为有待决定的审查包；`verified_tasks` 是流程接收区，不等于批准发布，reference只记录已证实部分。

| 论文ID | 任务 | 本次重读原始量化日志数 | 完整计算档案 | 审查状态 |
| --- | --- | --- | --- | --- |
| paper_589f72ac15eb7acd | Fe(II) 三组赝卤配体的六自旋态 | 6 | [AR参考](autonomous_research/paper_589f72ac15eb7acd/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_589f72ac15eb7acd/evaluation/verified_computation_reference.md) | 作者路线核心量有支持；任务包待修复 |
| paper_3c3d73b8715d5fcd | Rh 催化 1D 环异构化及竞争 [2+2] 路径 | 73 | [AR参考](autonomous_research/paper_3c3d73b8715d5fcd/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_3c3d73b8715d5fcd/evaluation/verified_computation_reference.md) | 作者路线核心量有支持；任务包待修复 |
| paper_c49993ae88ffa0e3 | H₂PQ/PyO 干燥/水合首次 PT/ET 热力学 | 58 | [AR参考](autonomous_research/paper_c49993ae88ffa0e3/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_c49993ae88ffa0e3/evaluation/verified_computation_reference.md) | 作者路线核心量有支持；任务包待修复 |
| paper_c56ec62e92dbdfbc | CBSCA 催化异色满反应的 R/S 选择性 | 24 | [AR参考](autonomous_research/paper_c56ec62e92dbdfbc/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_c56ec62e92dbdfbc/evaluation/verified_computation_reference.md) | 作者路线核心量有支持；任务包待修复 |
| paper_1e3a1d290a02e5f0 | JY1–JY3 孤立分子轨道与空穴重组能 | 12 | [AR参考](autonomous_research/paper_1e3a1d290a02e5f0/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_1e3a1d290a02e5f0/evaluation/verified_computation_reference.md) | 作者路线核心量有支持；任务包待修复 |
| paper_9e7293af88532cd4 | Mo 体系配平末步水结合 | 4 | [AR参考](autonomous_research/paper_9e7293af88532cd4/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_9e7293af88532cd4/evaluation/verified_computation_reference.md) | 作者路线核心量有支持；任务包待修复 |
| paper_1255ed42fa7e12ff | O/S/Se 的 S1 ESIPT 势垒与 TST 速率 | 16 | [AR参考](autonomous_research/paper_1255ed42fa7e12ff/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_1255ed42fa7e12ff/evaluation/verified_computation_reference.md) | 作者路线核心量有支持；任务包待修复 |
| paper_3c89b494a1645491 | Au1 四金接触的 QTAIM/DI | 1 | [AR参考](autonomous_research/paper_3c89b494a1645491/evaluation/verified_computation_reference.md) / [PR参考](paper_reproduction/paper_3c89b494a1645491/evaluation/verified_computation_reference.md) | 定性支持；DI字面区间2项偏差待决定 |

合计194份Gaussian/ORCA原始日志；逐份能量/原生结束/态/频谱核对。83组优化父几何→下游单点或IRC输入，元素/原子顺序与配对距离无不符；37份低层日志用GoodVibes4.3重新后处理，c499的29个和c56的8个与归档校正值一致。所有最终能差、四点λ、TST与Au原始矩阵由日志重提复算。未新做QM或提交/停止HPC；194是采用链涉及的日志数，不意味着所有历史日志或Se混合日志的全部点均有效。

### 29.2 每篇核心结果与边界

**paper_589f72ac15eb7acd — Fe(II) 三组赝卤配体的六自旋态**

六态 E(HS)−E(LS)×2625.499638 分别为 −33.764571、−28.500043、−21.415006 kJ/mol。三者均 HS 电子能较低；C3>C2>C1 是 LS 相对稳定化趋势，不是 C3 的 LS 已成为基态。LPh-TDA 为 C21H19N5S，两个辅助配体经 N 配位，cis 六 Fe–N 位点保持。既有六态身份/图/自旋检查及 97 次尝试审计见来源记录，失败不混入六个采用态。本次独立重读能量、频率、态与输入路线；图同构检查沿用并审阅原档，未冒称重新做全局构象搜索。

**paper_3c3d73b8715d5fcd — Rh 催化 1D 环异构化及竞争 [2+2] 路径**

采用 Gsol=Ehigh+Gcorr_low+(ESMD_low−Egas_low)+ΔG_RRHO(298→298.15)+RT ln(CRT/p0)。统一参照 0.5 Rh_dimer+1D，对 28 原子缺 CO 物种补上游离 CO。复算总体势垒 TS1endo−INT11=22.739173663，TS1exo−TS1endo=7.558219734 kcal/mol。六 TS、十二全实频连接端点：TS1endo: INT1↔INT2；TS1exo: 开链配位构象↔exo 环化物；TS2: INT2↔有机片段为 4D 的 Rh 配合物；TS3: INT2↔INT3+CO；TS4: INT3↔INT4；TS5: INT4↔INT5，有机片段为 3D。五个 TS 的十方向有限 IRC（各 50 点）后继续端点优化；TS3 原生 IRC 未成功，采用负模双向位移+优化的 QRC 替代。exo 开链端点不等同 endo INT1；endo/exo 标签由来源 SI 几何支持，不伪称无作者信息的立体搜索。

**paper_c49993ae88ffa0e3 — H₂PQ/PyO 干燥/水合首次 PT/ET 热力学**

G_i=E_high,i+(G_qRRHO,low,i−E_low,i)，每个外部旋转对称数只除一次；构象去重后 G_ensemble=Gmin−RT lnΣexp[−(Gi−Gmin)/RT]。采用 .001_dedup0.1（对称性位移诊断 0.001 Å、去重 RMSD 0.1 Å），完整代表构象见系综表。反应差由指定产物系综之和减反应物；水合双方总水数均为 2。四个 ΔG(kcal/mol)：pt_dry −0.922738715、et_dry −1.844558545、pt_hydrated −2.197728103、et_hydrated −8.029374079。水对 PT/ET 的位移分别约 −1.274989/−6.184816。干态轻度有利，水更强稳定 ET 端点。水合 PT 对应 SI −2.2，正文措辞/数值不完全一致，保留差异；不是从正文挑最近 gold。当前来源 JSON 的旧 evaluation_match=false 不能替代后续逐项审计，反之最新 PASS 也不能证明独立搜索。无速率/第二次转移/PCET-HAT 排除结论。

**paper_c56ec62e92dbdfbc — CBSCA 催化异色满反应的 R/S 选择性**

G_i=E_high,i+(G_qRRHO,low,i−E_low,i)。所有 TS 的配平参照为 G(TS)+2G(MeOH)−G(4i)−G(1a)−G(2a)，不能遗漏 2 MeOH。四个共同参照高度：CC_R 11.760297125、CC_S 13.738713650、dep_R 7.430898304、dep_S 9.564634049 kcal/mol；ΔΔG‡=S−R=1.978416525（源 2.0±1.0），支持 R 与 C–C 形成决定选择性。四个 TS 的虚频依次 −345.8570、−410.3163、−1030.3150、−973.0562 cm⁻¹。有机片段的连接与产物 CIP 溯源见独立立体化学档；不能用中间体局部 CIP 字母直接替代最终 R/S。两个步骤各 TS→端点有证据，但完整催化剂复合物盆地同一性及宏观动力学网络没有认证。有限四个作者最低代表 TS 及来源构象筛选，不认证重新执行 CREST 或独立搜索收敛。

**paper_1e3a1d290a02e5f0 — JY1–JY3 孤立分子轨道与空穴重组能**

每分子 λh=[E+(R0)−E+(R+)]+[E0(R+)−E0(R0)]；Hartree→eV 用 27.211386245988。六个 cross-SP 输入逐原子对应正确优化父几何。HOMO 从中性态最后完整 Alpha occupied 本征值、LUMO 从首个 virtual 提取。结果表中的 9 个数值分别满足原 HOMO/LUMO ±0.15 eV、λ ±0.03 eV：HOMO 逐渐降低，JY2 的 λ 最小。只证明孤立分子量，不证明器件性能。

**paper_9e7293af88532cd4 — Mo 体系配平末步水结合**

raw=(G3−GIm5−Gwater)×627.5094740631=3.974017499 kcal/mol；source_recipe=raw−RT ln55.34=1.596081539；all1M=raw−RT ln(Rgas·T·1 M/1 atm)=2.079689054；bulk=all1M−RT ln55.34=−0.298246907。R=0.00198720425864083 kcal mol⁻¹ K⁻¹，Rgas=0.08205736608096 L atm mol⁻¹ K⁻¹，T=298.15 K，Δn=−1。当前 source_recipe 与 1.6±8.0 比较，其余三值不能替换该靶。直接从最终几何得到 Mo–N–O=178.213119°、N–O=1.197462 Å，频率第 64 模 1698.7976 cm⁻¹；NO 主伸缩指认的位移投影由既有诊断提供。这支持末步热化学及键合诊断，不证明完整机理或唯一氧化态。

**paper_1255ed42fa7e12ff — O/S/Se 的 S1 ESIPT 势垒与 TST 速率**

ΔG‡=(G_TS−G_enol)×627.5094740631；k=(kBT/h)exp(−ΔG‡·4184/(RT))，T=298.15 K、kB=1.380649e−23 J/K、h=6.62607015e−34 J s、R=8.31446261815324 J mol⁻¹ K⁻¹。O/S/Se 势垒 13.426192707/7.703933813/6.661640577 kcal/mol；速率 894.941234/1.400359025e7/8.132903866e7 s⁻¹，均在原势垒 ±1、log10(k) ±0.25 容差内。采用前/反向点数为 O 73/101、S 68/121、Se 96/178；Se 18 点前缀+161 点尾段减一个共享连接点，连接 TD 能差约 2e−8 Eh。六根最低间隙依次 0.2334/0.3674/0.4484/0.0225/0.4653/0.0174 eV。只核验有限六根排序；没有波函数重叠连续性或非绝热动力学证明。

**paper_3c89b494a1645491 — Au1 四金接触的 QTAIM/DI**

四 BCP 的 ∇²ρ>0、H<0、|V|/G=1.165961–1.167434；平均 ρ=0.036440290765，在现行 0.036475±0.001 内。由原始 CPprop 与两份 LIDI 矩阵重新提取，0.10-Bohr DI=0.37506794/0.37627436/0.37365572/0.37591119；对应 0.20-Bohr=0.37548906/0.37717135/0.37501872/0.37676476。细网格 Au 原子 1/2/3/4→basin 91/123/114/57，不能按 basin 顺序误认原子。BCP 5/6/7/8 各有两条 94 点路径，末点与对应 Au 距离 <7e−7 Å。定性上支持以闭壳层为主且有少量共享的 metallophilic 接触。两项原始 DI 不在字面 [0.374,0.376]；按正文三位小数显示为 .375/.376/.374/.376，但这不是新容差。SI 八位值及细微接触排序未精确复现，两档网格差也不是严格误差界。登记的有限模型语义 PASS 与当前 PR 关键点窄区间措辞存在需确认的接受精度边界；本次不把它写成全部定量点严格通过。

### 29.3 公开输入与具体修复建议（均待批准）

**paper_589f72ac15eb7acd（AR/PR）**

公开输入只有中立系统定义，C21H19N5S、三种辅助配体、cis 与 0/(5,1) 齐全，未含作者末态坐标或参考能量。来源旧 C21/C22 疑点已按当前真实身份更正，不照抄旧待修列表。

1. 两模式 submission_schema.json：将实际使用的 $defs 放进 result_schema（或内联等价定义），用真实 report 经 validate_output_contract 复核；当前 PointerToNowhere 是框架故障，不是 Fe 算错。
2. reference_key_points/reference_conclusions 与现行 semantic rules 对齐方法自由度：保留能差定义/态/趋势，不把隐藏作者数值当任何方法唯一答案。清除普通 uncertainty/limitations 表态必填及扣分，保留真实物理边界。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_589f72ac15eb7acd/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_589f72ac15eb7acd/evaluation/task_provenance/maintenance_audit.md)。

**paper_3c3d73b8715d5fcd（AR/PR）**

完整 substrate 1D(24 atom)/Rh dimer(12 atom) 是当前给定反应物，合法；另有未在 task 中说明的 README_coordinates.xyz(14 atom)。其第 1 个 C 坐标来自 SI INT1（物理第 46 页），其余 13 行来自 TS1endo 尾部（第 47 页），是混拼的作者答案结构片段，不是第二个完整底物。两模式均将此文件公开；建议经批准移入 evaluation/author_results 并注明作废/不用，而非继续导出。

1. 两模式移出上述 14 atom 的 README_coordinates.xyz 至私有 author_results 并注明错误混拼；不改变合法底物与催化剂坐标或增加 TS 给 agent。
2. 删除 conclusion_limitations 普通免责声明得分；先将 kp_process_energy_assembly 重新接到 conclusion_mechanism，再更新规则/证据/策略。拆分 22.8 势垒与 7.5 选择性或采用明确部分成果 rubric 的权重方案另行批准。
3. 公开可比较的温度/标准态/能量定义与隐藏目标一致；如限制方法须明确批准，不声称任意方法必达同一数值。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_3c3d73b8715d5fcd/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_3c3d73b8715d5fcd/evaluation/task_provenance/maintenance_audit.md)。

**paper_c49993ae88ffa0e3（AR/PR）**

两模式公开分子图/状态/水数定义齐全；AR 只给起始/event 边界，PR 给 PT/ET 路线。没有把私有 29 个优化构象或参考能量公开。条件与两水计量可复算。PR task.md 重复一整套四节指令。

1. PR task.md 去掉重复指令，按流程设置 PR guidance；不改分子/水数或范围。
2. AR 历史 states 对象→带 state_id 的列表可无损映射且真实 runner 通过；仅用于私有验证，不补写事前自主假设。当前 schema 可以保留，后续规则须按实际 state_id 稳定绑定。
3. c_ar_limits/c_pr_limits 混有普通免责声明与实质水模型/候选敏感性：取消纯声明门槛并把必要敏感性接回真正热力学成果；PR 独立状态身份过程规则不能因重接漏评。
4. 正文/SI 水合 PT 差异继续单列，不新增固定水合 PT gold；有限来源构象与 task 独立收敛搜索的区别保留，不将作者参考当盲测完成。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_c49993ae88ffa0e3/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_c49993ae88ffa0e3/evaluation/task_provenance/maintenance_audit.md)。

**paper_c56ec62e92dbdfbc（AR/PR）**

公开 4i、1a、2a 的 82/20/26 atom XYZ 及 system.json 为分离反应物输入，均可解析；没有给最终 TS、R/S 能差或优胜路径。催化剂构型/键表由系统文件定义。既有作者 TS 只出现在私有验证档；本次没有新增到 agent_input。

1. 两模式 schema.oneOf 显式按 status=success/bounded_failure 分支；实测 success 加空 unresolved_blockers 被两分支同时匹配而拒绝；更严重的是 success 无势垒但有 blocker 反被接受。
2. 候选 validation 按 validated/failed disposition 分支，真实早期失败允许没有 TS 几何/虚频/映射；主成功与额外失败 attempts 分开，不伪造成功字段。
3. 保留 TS/模式/连接/配平参照与原 ΔΔG 2.0±1.0。作者有限候选覆盖已支撑可计算性，未认证 task 要求的自主采样收敛；不以删除 coverage 关键点换通过。方法段 6-31G(d)/6-31+G(d) 与 GoodVibes 替代如实记录。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_c56ec62e92dbdfbc/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_c56ec62e92dbdfbc/evaluation/task_provenance/maintenance_audit.md)。

**paper_1e3a1d290a02e5f0（AR/PR）**

molecules.json 唯一命名 JY1/2/3，电荷/态/元素式一致，JY3 是 3′,4′,5′ 三氟；无轨道能与 λ 答案。自由选方法且允许多种 λ 定义与隐藏四点靶存在协议歧义。

1. 两模式 scoring_rules 为 HOMO/LUMO/λ 显式绑定 JY1/2/3 的稳定 ID，补齐源中已存在的 JY2/3 数值绑定；当前只有 JY1 标量 target 搭配通配数组，自动 checker 交语义审查，不能声称九个自动数值已比较。数值/容差不改。
2. LUMO 结果关键点目前 standalone，不关联最终结论；提出完整分子性质结果的部分成果计分或在现有结论关联中补接 LUMO，具体权重/结论改动先确认。身份/能量循环过程仍保留。
3. 明确主比较采用原四点 λ 定义；task 可选 adiabatic/其他定义与 gold 不等价。若限制方法或比较职责，须批准后再改公共协议，不向 AR 注入作者答案。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_1e3a1d290a02e5f0/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_1e3a1d290a02e5f0/evaluation/task_provenance/maintenance_audit.md)。

**paper_9e7293af88532cd4（AR/PR）**

四套 XYZ 是已修订任务明确给定的验证/性质对象，不将 product_3 文件名一律视为答案泄露。四输入完整、单位/态明示，water 必须独立优化；不评独立发现整个 1→3 反应。源题已公开配平和四种标准态算式，不回退旧未配平版本。

1. 保留当前已配平任务及四种标准态，保留原 1.6±8.0。不回退未配平 1→3 或把 source_recipe 更名为一致 1 M。
2. 删除仅要求普通 limitations 表态的规则/必填；端点完整、诊断、标准态区分和不得无证据断言机理属于实质检查，必须保留。统一 PR guidance 与科学结果策略。宽容差若需重定不属本批常规修复。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_9e7293af88532cd4/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_9e7293af88532cd4/evaluation/task_provenance/maintenance_audit.md)。

**paper_1255ed42fa7e12ff（AR/PR）**

三个 37 atom S1 enol 是明确给定的起始反应物，没有 keto/TS/IRC 答案。注释如实标明 SI 来源。需确认自由溶剂/方法选择与固定 CPCM 数值靶的有效答案范围；不因坐标来源于 SI 自动删除合法起点。

1. 两模式按 compound 身份绑定每个 barrier/rate，保留 O/S/Se 当前靶和容差，log10(k) 比较显式；通配字段+自然语言选择器当前仅交语义审查。防重复/漏对象，不依赖数组顺序。
2. 公开主比较的溶剂/温度/量定义或明确允许的替代协议，解决自由气相/溶剂与固定源靶的冲突；若限定方法，先批准。
3. AR 历史 report 缺 hypotheses，不能后填一个事前假说声称自主重放已通过；保留作者路线科学证据。普通免责声明改可选，S1 选根/连通性/频率必须保留。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_1255ed42fa7e12ff/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_1255ed42fa7e12ff/evaluation/task_provenance/maintenance_audit.md)。

**paper_3c89b494a1645491（AR/PR）**

真实 CIF 为 CCDC 2500223，保留完整出处/占据/晶胞及原子标签；system_definition 指定仅移除阴离子和溶剂、+4 单重态及四边。实验晶体是任务给定结构证据，不是计算 BCP/DI 答案，DOI/CCDC 号不单独构成答案泄露；未向 agent 提供 fchk 或拓扑计算结果。

1. 当前 PR pr_result_aim 要求 DI 位于 reported narrow range；原始两项字面越界，三位有效显示与定性分类支持不能自动当数值严格通过。负责人先决定接受正文约三位精度的有限分类，还是维持原始字面区间并保留待定；不自行扩大容差、改 DI、删必评量或开新网格计算。
2. rho 规则 target/单位写四边均值，但字段绑定四个位置且 comparison 写逐接触；需决定均值还是 SI 逐接触比较后按 contact ID 绑定，不能默选对过关有利的一边。当前二者都满足现有 ±0.001 仅是证据，不是新定义授权。
3. AR 历史 report 缺 hypotheses；只认作者路线验证，不能补编事前自主轨迹。清除普通 limitations 得分而保留四边身份、+4/1、BCP、真实定量证据与物理范围。

逐项映射及当前规则读取：[AR审查](autonomous_research/paper_3c89b494a1645491/evaluation/task_provenance/maintenance_audit.md) / [PR审查](paper_reproduction/paper_3c89b494a1645491/evaluation/task_provenance/maintenance_audit.md)。

### 29.4 提交/评分软件核查及适用边界

16个修前 package validator 均通过，但实际 runner 只验证result_schema，不能由包通过推断能提交：Fe两个包均出现内部$defs引用失败；c499 AR历史对象states无损映射为带state_id列表后可通过；ESIPT/Au AR缺hypotheses，未补编。其余真实报告本轮实测可按当前schema提交。c56两模式还出现 success+空blockers被拒、success缺全部结果反被接受、早期失败被迫填TS数据三类可复现问题。

16包仍用dual_axis_100.v1。本轮未获得具体评分修订方案批准，故不静默切换；建议按流程清理普通免责声明后显式选既有scientific_results策略。Rh纯limitation单列得分；c499 limits含实质敏感性需拆分；JY LUMO缺成果关联，需具体计分决定。checker对多字段/通配/自然语言条件numeric返回requires_semantic_review，非自动比较成功。记录实际规则职责，未调用LLM judge，不提供虚构100分。

各包任务/schema中的成功、部分、失败、额外尝试问题已列具体审查；后续获准修复必须用真实主结果、错误身份、乱序/重复/漏对象、诚实早期失败和成功附额外失败的正反例验证。当前未修复包不具发布资格。原公开导出边界和修改后manifest/引用检查结果见29.6；运行环境挂载/网络隔离没有实测。

### 29.5 基线、文件范围与需要的具体决定

Git HEAD `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`；精确修前基线 tar（含隐藏/未跟踪文件）：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`，同目录 baseline.json/path_status.txt。此次没有git add、commit、reset，保留既有未提交工作。源包只新增reference和刷新manifest；staging完整复制后只新增维护记录、调整reference相对链接并刷新manifest。docs/verification、papers、原始结果、final/hold均未改。

审查/复算证据：[本批机器可读核查结果](maintenance_tools/audit_evidence_20260929.json)；[源/暂存32包定向校验](maintenance_tools/package_checks_20260929.json)。原始记录直接链接在每份reference，不复制大型日志。复算程序在同一maintenance_tools目录，默认只读既有科学档、输出/tmp审计结果；GoodVibes脚本使用general-modern-openmpi5环境，contract/runtime脚本使用researchchembench环境。

需要负责人决定：①批准29.3中格式、公开Rh片段私有化、Fe/c56格式契约、身份字段绑定及普通limitation清理的具体范围；②对JY/ESIPT自由协议与固定源靶、JY LUMO部分计分和其他实质结论/权重变动逐项确认；③Au DI精度接受方式及rho均值/逐接触定义。没有决定时保留当前原科学文件，继续留staging，不把新计算当默认补救。

停点来自用户指定的[维护流程 §2.2.1、§2.5](../../docs/verification/final_verified_tasks/final_verified_task_maintenance_workflow.md)：“先提供每篇/模式的问题、原文及真实输出依据、现有验证覆盖、建议改哪些文件/字段及科学影响”；实质必评量、有效答案范围、权重/分支等“须先向负责人说明并获得具体决定”。因此本批已交付具体证据和方案，未把泛泛按流程处理当作批准改变科学验收标准。修改批准与final/hold迁移批准仍是两个独立步骤。

### 29.6 写入后复核与交付状态

- 32/32 个本次源/暂存任务包完成定向 manifest 重建和 `validate_task_package` 校验。计算参考均覆盖当前 KP/结论 ID、完整采用链及实际版本/路由；不是以包通过代替科学复核。
- 对修前 tar 逐文件比较：186 个原有任务内容文件保持字节不变；暂存同样有186个内容文件与源相同。差异仅为 reference、逐包维护记录和相关 manifest。完整目录复制包含隐藏文件，没有覆盖已有暂存包。
- 本批所有新增/更新文档的本地相对链接均可定位；Se 混合日志索引明确使用有效点17的TD能量，未把被排除的日志尾部值当采用结果。
- 实际 `TaskRepository` 从暂存根加载本批16包，运行策略仍是 `dual_axis_100.v1`。`materialize_agent_files` 实测导出74个公共文件，内容与agent_input一致，未导出reference/evaluation/paper_route。**这是文件边界通过，不代表公开内容已完全清洁：Rh混拼14原子片段仍在待批修复项内。**
- 26份公开XYZ、全部公开JSON可解析；Au两模式相同原始CIF可由pymatgen解析，CCDC2500223、晶胞28.18290/23.54710/16.47430 Å及90/98.3230/90°，238个原子位点记录，occupancy含1、0.698(13)、0.302(13)，不能忽略晶体无序。有限分子抽取仍按原几何审计。未实测部署容器挂载/父目录/网络隔离。
- 逐项读回核查记录见[写入后检查](maintenance_tools/write_verification_20260929.json)，复核程序见[本批只读验证脚本](maintenance_tools/rcb_verify_writes_20260929.py)。这些是离线文件/提交契约检查，不是新QM、LLM评分或AR盲测。

截至本轮交付，本批仍为8篇16包的待修订暂存接收区。科学与软件缺口已逐包给出具体证据和改法；不声称维护修复已执行，更没有迁入final/hold。Au的参考记录保留部分定量支持状态，等待科学接受边界决定。

## 30. 2026-09-29 新八篇：获准修复与暂存复查完成

### 30.1 授权、工作范围与结论

负责人明确要求“继续按照这个流程，完成这些论文的处理，但是先不要移动到 final 或者 hold，先留在 verified_tasks 中，跟我汇报一下处理情况，等我确认后再去移动”。本轮据此接续第29节已汇报方案，在 8 篇 × AR/PR 两模式共 **16 个暂存包**中完成常规修复。先独立保存格式阶段，再修输入边界、提交格式、评分关联和普通免责声明，并同步 16 份计算 reference 及 16 份维护审查。

**处理完成不等于八篇所有科学问题全部关闭。**7 篇核心限定数值/趋势有既有真实计算支持；Au 有真实计算和定性支持，但两项 DI 未满足原字面区间，rho 比较定义也未统一。其他来源冲突、方法可比性和自主搜索证据边界如下表。所有 16 包仍在 `tasks/verified_tasks/<mode>/<paper_id>/`；final/hold 迁移数为 0。

### 30.2 逐篇实际改动与当前证据边界

| 论文 | 已实施的主要修复 | 当前证据和未闭合项 | 逐包记录 |
| --- | --- | --- | --- |
| Fe 六自旋态 / `paper_589f72ac15eb7acd` | 将 $defs 放入 runner 实际使用的 result_schema，消除无法解析引用的错误；成功的六个选中态必须保留电荷/多重度、能量、几何、频率及自旋/收敛证据；诚实失败不必填未完成方法；保留 HS−LS 定义及方法自由度；AR 的物理量边界项改为过程有效性检查，不把普通 uncertainty 作为成果。 | 现有六态支持限定孤立电子能比较；未认证自主事前计划或全局构象穷尽。合理替代方法按实际电子态和能量证据判断，不强制复现作者每个数值。 | [AR](autonomous_research/paper_589f72ac15eb7acd/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_589f72ac15eb7acd/evaluation/task_provenance/maintenance_audit.md) |
| Rh 环异构化 / `paper_3c3d73b8715d5fcd` | 原 14 原子混拼 README_coordinates.xyz 原字节移入 evaluation/author_results，并注明不能作为合法计算结构；24 原子 1D 与 12 原子 Rh 二聚体未变；移除 conclusion_limitations/rule_limitations；将能量组装关键点接回 conclusion_mechanism；公开 298.15 K、1,4-dioxane、溶质 1 M/CO 8.5 mM、配平和 exo−endo 符号；完成与早期失败分支分开。 | 六 TS、十二连接端点和势垒有作者路线证据；TS3 是 QRC 替代有限 IRC，exo 开链端点不等同 endo INT1。替代协议应单独判断可比性，未认证自主盲搜索。 | [AR](autonomous_research/paper_3c3d73b8715d5fcd/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_3c3d73b8715d5fcd/evaluation/task_provenance/maintenance_audit.md) |
| H₂PQ/PyO / `paper_c49993ae88ffa0e3` | 删除两模式 task.md 重复的整套指令，PR 单列作者指导；删除 c_ar_limits/c_pr_limits 普通声明结论及 AR 纯边界 KP；保留状态、覆盖、水模型敏感性并接回真实热力学结论；PR 按四种既有状态及各自标量比较；AR 按唯一 state_id 进行语义身份匹配，不按数组位置猜。历史 states 字典仅在私有测试中无损映射为数组。 | 水合 PT 的正文/SI 冲突保留，未新增固定 gold。29 构象与对称/去重敏感性支持有限来源系综；不宣称排除 PCET/HAT、得到速率或认证独立搜索收敛。 | [AR](autonomous_research/paper_c49993ae88ffa0e3/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_c49993ae88ffa0e3/evaluation/task_provenance/maintenance_audit.md) |
| CBSCA 选择性 / `paper_c56ec62e92dbdfbc` | success/bounded_failure 按 status 互斥，修复成功无结果误收及成功带空 blocker 被拒的问题；额外失败候选可报告实际 disposition/failure_reason，不强造 TS；主结果仍必须有完整 saddle/模式/连接证据；明确选中 R/S ID 必须唯一指向正确且已验证的候选，动态关联由语义审查承担；保留候选覆盖、敏感性和配平共同参照要求。 | 现有四个作者代表 TS 支持有限路线的 R/S 能差与步骤比较；不能据此认证所有竞争家族的自主采样已收敛，也未认证完整催化剂复合物盆地连接或全局动力学网络。现行 coverage 要求未降级。 | [AR](autonomous_research/paper_c56ec62e92dbdfbc/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_c56ec62e92dbdfbc/evaluation/task_provenance/maintenance_audit.md) |
| JY1–JY3 / `paper_1e3a1d290a02e5f0` | 公开三条主结果的 JY1/JY2/JY3 顺序，并将每个位置绑定完整行约束，拒绝只有身份或空 λ 的完成结果；每模式从 3 条含混 numeric 规则补成 9 条身份明确的比较，保留原 JY1 rule ID；JY2/3 目标来自既有 KP，未改既有目标/容差；将 LUMO 及过程关键点接回原有唯一科学结论；明确同一个四点 λ 物理量，公开 B3P86/6-311G(d,p) 比较背景，保留合理方法自由度。 | 九个验证值均满足原容差；不同方法与 B3P86 源靶是否可比仍须科学判断。现有源值/容差未放宽，也未将分子量推广为器件性能。 | [AR](autonomous_research/paper_1e3a1d290a02e5f0/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_1e3a1d290a02e5f0/evaluation/task_provenance/maintenance_audit.md) |
| Mo 水结合 / `paper_9e7293af88532cd4` | 保留四端点和独立诊断；清理普通免责声明而不删端点/最低点/标准态检查；保留 raw 1 atm、source-recipe、all-solute 1 M、bulk-water 四种量及原 1.6±8.0 kcal/mol；成功证据非空、失败可诚实报告。 | 末步配平水结合及诊断有真实证据；不是整个反应机理验证。原 ±8.0 kcal/mol 宽容差保留，本轮不重新制定数值标准。 | [AR](autonomous_research/paper_9e7293af88532cd4/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_9e7293af88532cd4/evaluation/task_provenance/maintenance_audit.md) |
| O/S/Se ESIPT / `paper_1255ed42fa7e12ff` | 公开主数组 O/S/Se 顺序，并让每个位置执行完整行约束；validated 必须有非空 TS/端点/证据、numeric 势垒及正速率；逐分子绑定 barrier 和 k，明确 log10(k) 差值容差 0.25；读取完整频率/状态/连接证据；公开 TD-ωB97X-D/6-311G(d,p)、CPCM MeCN、298.15 K 比较背景但不固定所有方法；失败可省未取得证据，AR 事前假说不补编。 | 作者路线支持三势垒/速率及有限六根顺序；无波函数重叠连续性或非绝热动力学认证。AR 历史 report 缺事前 hypotheses，不伪造补齐；不同协议仍需可比性判断。 | [AR](autonomous_research/paper_1255ed42fa7e12ff/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_1255ed42fa7e12ff/evaluation/task_provenance/maintenance_audit.md) |
| Au₄ 接触 / `paper_3c89b494a1645491` | 四条 contact 按身份唯一覆盖，允许乱序；validated 八个描述符必须为数字，complete 必须四条均成功且有四个 BCP；缺描述符用 null 和真实 notes，早期失败不强造收敛或 BCP；成功不要求普通 notes/limitations；保留 +4 单重态和原始 CCDC 2500223；未改 DI/rho 数值标准，rho 原均值/逐接触冲突明确交科学审查。 | DI=0.37627436 和 0.37365572 分别越过字面 [0.374,0.376] 上/下界 0.00027436 和 0.00034428；另两项在界内。rho 均值靶与逐接触措辞未统一。定性成键有支持，但不能宣称全部定量点严格通过；AR 历史 report 也缺 hypotheses。 | [AR](autonomous_research/paper_3c89b494a1645491/evaluation/task_provenance/maintenance_audit.md) / [PR](paper_reproduction/paper_3c89b494a1645491/evaluation/task_provenance/maintenance_audit.md) |

### 30.3 关键点、结论与数值标准

| 论文 / 模式 | KP 修前→修后 | 结论修前→修后 | 当前结论 ID |
| --- | --- | --- | --- |
| Fe 六自旋态 / AR | 4→4 | 1→1 | ar_final |
| Rh 环异构化 / AR | 4→4 | 2→1 | conclusion_mechanism |
| H₂PQ/PyO / AR | 5→4 | 2→1 | c_ar_final |
| CBSCA 选择性 / AR | 4→4 | 1→1 | c_final_selectivity |
| JY1–JY3 / AR | 5→5 | 1→1 | ar_final_trend |
| Mo 水结合 / AR | 4→4 | 1→1 | ar_final |
| O/S/Se ESIPT / AR | 4→4 | 1→1 | c1 |
| Au₄ 接触 / AR | 4→4 | 1→1 | ar_final |
| Fe 六自旋态 / PR | 4→4 | 1→1 | pr_final |
| Rh 环异构化 / PR | 4→4 | 2→1 | conclusion_mechanism |
| H₂PQ/PyO / PR | 5→5 | 2→1 | c_pr_thermo |
| CBSCA 选择性 / PR | 4→4 | 1→1 | c_final_selectivity |
| JY1–JY3 / PR | 5→5 | 1→1 | pr_final_trend |
| Mo 水结合 / PR | 4→4 | 1→1 | pr_final |
| O/S/Se ESIPT / PR | 4→4 | 1→1 | c1 |
| Au₄ 接触 / PR | 4→4 | 1→1 | pr_final |

- Rh 移除独立 limitation 结论，energy_assembly 接回 mechanism。H₂PQ/PyO 移除两个模式的 limits 结论，AR 纯边界 KP 删除，但水模型/候选/状态敏感性仍由保留的科学项承担。Fe AR 原边界 KP 保留 ID，角色改为过程有效性检查。
- JY 的 LUMO 与身份/能量循环过程接回原有科学结论；9 个目标均来自修前已有的 KP/原论文，不新造科学成果或任意分配权重。公开主数组顺序与 schema 身份同时固定，单值 selector 不再依赖隐含顺序。ESIPT 同理。
- 全部 16 包显式使用既有 `dual_axis_100.scientific_results.v1`。没有改变全局默认，没有新增 rubric；普通 limitations/uncertainty 可省略或留空，真实身份/态/优化/频率/路径/覆盖/参考态要求保留。
- 修前存在的 numeric 规则目标和容差逐条对照备份保持一致。H₂PQ PR 水合 ET 原规则容差为 ±1.5 kcal/mol，reference 初审表误写 ±1.0，现仅改正该档案文字；数值规则未变。JY 新增的 JY2/3 显式绑定继续使用原每类容差。
- 未新增水合 PT 固定 gold；未把本地验证值替换为论文目标；Au 原 DI/rho 接受标准未决定，不能靠四舍五入或选择有利平均口径判定严格通过。

### 30.4 实际检查及其边界

- **1012 项针对性检查通过，0 失败**，覆盖 232 个逐包提交场景，每场景同时经过 JSON Schema 与真实 `validate_output_contract`。包括真实历史结果兼容性、空值/错身份/重复/缺对象、成功/失败互斥、额外失败尝试、运行策略、评分 ID 关联、原数值容差和源文件不变性。[程序](maintenance_tools/test_eight_repairs_20260929.py) / [结果](maintenance_tools/repair_checks_20260929.json)。
- 既有相关测试 `test_output_contract.py`、`test_task_package_v19.py`、`test_scoring_rules.py`：**28 passed**。未运行完整 benchmark 或 LLM judge；没有启动新的 QM/HPC。
- 已发现并修复 JY/ESIPT 新数组约束中的 prefixItems 漏洞：此前只有名称被验证，前三条数值可能绕过 items。现每个 prefix 同时引用完整行定义，空势垒/λ、无 TS、错误单位及零/负速率不能冒充 validated。
- 历史结果在 14 个模式包中可进行格式兼容检查（含 H₂PQ AR 的无损 states 映射）；ESIPT/Au 两个 AR 历史 report 缺 hypotheses，保留失败结果。用于验证 AR schema 正例的明确合成假说只是软件样例，不写进计算 reference，不作为自主轨迹或新科学验证。
- **1918 项文件/导出核查通过，0 失败；16/16 包校验通过。**实际导出 72 个公共文件，24 份 XYZ、2 份 CIF 可解析，1048 处本地链接可定位，218 个 canonical 源文件保持不变。私有 reference/evaluation/paper_route 和 Rh 作废片段不进入导出。本批16包 manifest 已刷新。[最终文件检查](maintenance_tools/final_checks_20260929.json)。
- 通用 numeric checker 不支持所有复杂条件及 log 比较，明确标为 requires_semantic_review；ESIPT TST/log-rate 已做独立离线算术核对。H₂PQ AR 重复 state_id、CBSCA 所选 ID 与有效候选的动态关联、方法可比性须按科学规则审查，schema 通过不能证明它们成立。
- 本轮包内及导出文件边界检查不覆盖部署环境挂载、父目录或网络可见性；未认证正式部署隔离，也未认证从公开起点重新完成自主发现。

最终人工读回还修正了 Fe PR 的普通边界表态失败条件、CBSCA 成功分支被误要求失败 blocker 的旧措辞，以及 Fe/CBSCA/Mo/ESIPT/Au 的部分 critical_failures 将成功所需身份、端点、TS 或收敛证据误套到诚实早期失败/单列失败尝试的冲突。约束继续用于声称成功或支持科学结论的结果；未得到的成果不得分。这些只对齐现有科学要求和提交分支，不改接受数值。

### 30.5 保留的科学决定及下一步

1. **Au（两模式）：**原 DI 范围 [0.374,0.376] 中，0.37627436 超上界 0.00027436，0.37365572 低于下界 0.00034428。定性分类与三位显示接近不能代替现行字面标准。rho 需决定比较四边均值还是逐接触 SI 值；本轮只记录问题，维持原标准。
2. **方法和科学覆盖：**JY/ESIPT 已公开源数值的比较背景并保留合法方法自由；不同方法/环境不自动等价。H₂PQ 水合 PT 正文/SI 冲突未消除，未新增固定靶。CBSCA 有限四 TS 不能充当完整自主收敛搜索；这些边界已写入每包记录，不擅自降低必评要求。
3. **处理建议：**已实施的常规修复及当前可验证的限定科学结果可交负责人审阅；Au 的窄数值定义、超出现有作者路线的覆盖及不同协议适用性不作无条件通过结论。负责人确认调整结果及具体论文/模式/去向前，16 包均留 verified_tasks。

### 30.6 可恢复版本和保护范围

修前 Git HEAD `b6c0f50825638e9c6149595581734bb674fbd66c`。`.git/maintenance_backups/20260929_eight_papers_repair/` 保存 `before_repair.tar.gz`、`after_format.tar.gz`、`after_quality.tar.gz`、baseline.json 和路径状态；包含未跟踪包，不依赖 Git 已提交文件。逐包实际修复与 ID 前后表见[改动记录](maintenance_tools/repair_changes_20260929.json)。

本轮不覆盖 canonical、不改 papers 或 group 原始输入/输出、不操作其他批次 final/hold；不提交 Git、不清理他人工作区。源 218 个文件保持修前哈希。未迁移、未发布，后续移动须由负责人确认。
