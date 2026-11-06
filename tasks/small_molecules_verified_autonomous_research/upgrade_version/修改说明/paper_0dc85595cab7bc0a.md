# 第一轮专家反馈调整 — 2026-11-03

提供带前体映射的产物2连接结构和二维SDF，保留自主竞争位点研究；取消已知产物预测分，五项权重25/15/25/15/20。

正文Fig. 2及SI的核心证据是两阶段同组成中间体相对自由能和位点电子结构。提供产物可以减轻结构构建负担，竞争位点及物理解释仍由agent完成。既然产物公开，原15分产物预测项必须删除。产物图由前体映射构造，并与SI Table S13恢复坐标的独立分子图核对一致；仅发布二维图，不发布作者优化几何或中间体。

当前评分：第一次环化的区域异构体热力学偏好 25分；第一次位点区分的电子起源 15分；第二次环化的区域异构体热力学偏好 25分；第二次位点区分的电子起源 15分；连续氧化环化路线的化学解释 20分。

<details>
<summary>此前修改说明（历史）</summary>

# paper_0dc85595cab7bc0a 最终结论分项评分统一（2026-10-29）

逐条核对现有独立最终命题，保留其科学范围与权重，删除人工待定分及旧数值门槛政策。

第一次环化的区域异构体热力学偏好 20分；第一次位点区分的电子起源 15分；第二次环化的区域异构体热力学偏好 20分；第二次位点区分的电子起源 15分；连续氧化环化路线的化学解释 15分；预测的最终产物连接方式 15分。

旧→新规则数：6→6；仅保留独立终答，全部semantic/pass-fail，100分。科学范围不变；公开题面/输入/提交结构字节不变。

相关论文位置：正文第 2 页 Figure 2、第 2–3 页产物；SI 第 9 页方法和 Figure S5，第 14 页起计算坐标及 Table S5/S8。逐项定位与证据身份见 [evidence_map.json](<../tasks/autonomous_research/paper_0dc85595cab7bc0a/evaluation/evidence_map.json>) 及第 4 节的 `evidence_ids`。

逐项问题、独立性、来源与验证映射见[协调进度](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/最终结论分项评分统一_20261029/进度/organic19_a_paper_0dc85595cab7bc0a.json)及[完整审查报告](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料_20261029/剩下的其他评估任务/papers/paper_0dc85595cab7bc0a.md)。

修改文件及原因：

- `paper_route.md`：同步最终结论二态合同、引用或非评分历史证据边界。
- `package_manifest.json`：重建实际内容哈希。
- `evaluation/scoring_rules.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/conclusion_coverage_20261029.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/reference_key_points.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/critical_failures.json`：同步最终结论二态合同、引用或非评分历史证据边界。
- `evaluation/evidence_map.json`：同步最终结论二态合同、引用或非评分历史证据边界。

未运行新量化计算。验证参考SHA256保持`6b382fa7c1152fbe0de29af4c7c3e4a4e046e063bc02de5cba4722d185afda62`，原始接受分类、数值差异和方法限制未升级。rubric/package/runtime加载及源/副本逐文件哈希校验通过。

当前专家事项：

|已知事实／数值|影响的规则或推断|专家需判断及建议处理|
|---|---|---|
|LUMO 球域密度比约 3.345549/2.688558；第一轮两点相位样本同号。|两项独立位点电子解释，尤其 `r_first_site_electronic`。|判断密度／结构证据是否充分区分成键位点；不要把两点采样当成完整节点拓扑复现。|
|本地采用 GD3BJ，来源只说明 D3；两组自由能差偏 −0.239912/−0.296270 kcal/mol。|两轮同组成热力学偏好。|审查方法差异对排序的影响；维持无硬窗现状，不为追值补设窗口。|
|已有氢数映射、同组成端点比较和最终最低点；未认证氧化 ΔG、激发态速率或盲发现。|`r_sequential_chemistry`、产物选择性解释范围。|判断有限序列解释的支持强度，不要求本题外的完整光化学机制；若实际主张超出端点范围，按该主张的证据判断。|

“未计算氧化能就失败”的规则问题已修复；当前未解决的是具体证据能支持多强的科学推断。

汇总入口：[需专家重点审查的问题](<../需专家重点审查的问题.md>)。

---

## 2026-10-29之前的修改历史（非当前评分判据）

# paper_0dc85595cab7bc0a 修改说明

## 科学问题与公开信息
原题为两步Mallory环化的位点选择及产物预测；保留预测类型、52原子C30H22中性单重态前体、孤立分子范围和全部竞争关系。新版明确“端点热力学+位点电子解释”能支持的结论，不把该证据升级为光动力学。未公开产物身份、作者IS序列或能差。XYZ未改；补明一基原子顺序即映射，并说明起点为位移几何而非已验证最低点。

## 文件改动
|文件|改前→改后|为什么|
|---|---|---|
|task.md|宽泛机制与选择性→五节英文、两轮比较/独立电子解释/连续化学/产物四组输出|明确物理量及氢数边界、保留自主发现|
|scoring_rules/reference_conclusions|V2四中间项+30分合并终项→六个最终命题20/15/20/15/15/15|两轮位点偏好是要回答的科学结果；连续化学与终产物分开，避免绑成作者节点大包|
|reference_key_points/evidence_map/critical_failures|旧证据scored=false，新增终答及原生绑定|计算结构和作业不直接计分|
|paper_route、verified_computation_reference|前者明确当前六规则/方法差异；后者只加顶部复用限制|保留历史原文、不继承旧PASS|
|submission_schema、manifest|字段不变，仅说明与哈希同步|原通用candidate接口已足够；不增固定流程|

## 最终规则与状态
|规则|命题|分|状态|
|---|---|---:|---|
|r_first_stage|第一轮同组成区域异构体自由能偏好|20|二态|
|r_first_site_electronic|第一轮位点电子/结构原因|15|二态|
|r_second_stage|第二轮同组成区域异构体自由能偏好|20|二态|
|r_second_site_electronic|第二轮位点电子/结构原因|15|二态|
|r_sequential_chemistry|先环化/芳构化再闭环的连续化学解释|15|有充分真实连接证据的配平替代顺序，若等价性仍科学未决则复核；缺算失败|
|r_product_connectivity|最终选择dibenzo[a,o]picene连接图|15|二态|

合计100，皆required。等价方法/命名可直接通过；无新硬窗。源9.9/11.3 kcal/mol本来无容差，继续作为上下文，绝不追算值调窗口。旧IS节点只支持结论，不按完成数计分。

## 题面→来源→规则→本地证据
原生根`docs/verification/group_4/paper_0dc85595cab7bc0a/`；直接核正文p.2 Fig2、SI p.9方法/FigS5及坐标章节p.14起。正文热力学/轨道是地面态解释，不能等同光激发路径。

|最终输出|来源|规则|实际量/原生文件|缺口|
|---|---|---|---|---|
|第一轮能量偏好|正文p.2、SI p.9|r_first_stage|IS2−IS1=9.660087921 kcal/mol；hpc_runs/author_channel_is1_optfreq_refined_sp_hpc20_p3/stdout.log及is2同类log|源9.9，偏−0.239912；无动力学证明|
|第一位点解释|正文Fig2、SI TableS5|r_first_site_electronic|provenance/1_cis_lumo.cube；C1/C2球域积分0.033433537/0.009993439，ratio3.345549；mapping_audit|两最近网格同号，不能宣称完整相位反转图已复现|
|第二轮能量偏好|正文p.2、SI p.9|r_second_stage|IS5−IS4=11.003730032；is4/is5 native stdout.log|源11.3，偏−0.296270|
|第二位点解释|正文Fig2、SI TableS8|r_second_site_electronic|provenance/is3_lumo.cube；C3/C4积分0.033354883/0.012406234，ratio2.688558|球积分非Multiwfn原子布居；不设比例阈值|
|连续化学解释|正文p.2、SI FigS5/IS坐标|r_sequential_chemistry|refined_profile_audit.json及is1/is3/is4/is6/is7原生log、映射|同氢数竞争可比；跨氢数氧化自由能和光速率未验证|
|产物连接图|正文pp.2–3、SI产物坐标|r_product_connectivity|artifacts/gaussian_batch/author_channel_product_2_optfreq_refined_sp/stdout.log，138正频/0虚频|有最低点，无当前公开起点盲发现回放|

## 方法与自检
源B3LYP/6-31G(d,p)+D3优化/频率，ωB97X-D/def2-TZVP单点；本地明确GD3BJ而源未说明阻尼约定。G=高层E+低层热G校正，本轮直接重读is1/is2/is4/is5日志，分别提取E −1156.38017151/−1156.36273118/−1155.19984106/−1155.18043450 Eh和热修正0.371569/0.369523/0.355160/0.353289 Eh；重算两个差值吻合。九端点最低点是有效局部证据，不能冒称全光机制。

本轮无QM/HPC。原分子与计算条件不改，可复用上述证据；相位全图、氧化动力学和盲发现未覆盖，但不暗加为本题要求。需父级/专家复核连续化学解释的支持强度，不能由产品最低点推出排他产率。JSON、V3及package验证通过，仅合同通过，不声称完整科学PASS。

父级复审：连续化学解释设上述具体need_review出口；已经证实物理等价直接通过。其余五项仍二态，不因光化学边界普遍复核。

末次组内核对：相对v1_backup实际修改10个文件，与上表覆盖一致；未新增/删除文件，agent_input/data原始数据逐字未改，验证参考历史原文完整保留。独立临时仓库加载本篇为paper_science_v3 / final_results_100，权重合计100，包与V3合同通过；公开文本无外部作者/论文/SI依赖及旧过程计分。直接由公开XYZ重建分子图，确认为单组分C30H22并保留两顺式烯基连接；位移几何仍不宣称最低点。 这些检查只确认合同、身份和证据读取，不代表本篇科学结果已全部通过。

## 2026-10-27 已确认问题定向修复（独立交叉复核后）

**确认依据。** 交叉复核直接对照正文 PDF 第 2 页 Figure 2 与 SI 第 9 页 Figure S5。来源参照为映射的 IS1→芳构化 IS3→IS4→产物及同氢数高能 IS6/IS7 对照；这是一组端点/位点解释，不是完整配平氧化自由能。实际证据 `docs/verification/group_4/paper_0dc85595cab7bc0a/report/results.json`、`provenance/refined_profile_audit.json` 和 `provenance/lumo_reactive_site_mapping_audit_20260911.json` 支持 9 个最低点、两组同组成差 9.660088/11.003730 kcal/mol 及局部 LUMO 密度比约 3.345549/2.688558；没有认证独立氧化 ΔG 或激发态速率。因此原 review trigger 的 “Missing oxidation energetics ... fails” 超出当前必要计算边界。

**具体修复与理由。** `r_sequential_chemistry` 的 15 分和原复核开关保持不变，去除“缺氧化能即失败”的暗示，明确证据义务随实际科学主张。已有映射、氢数记账和适当同组成端点比较可支持有限序列化学解释，不自动追加完整氧化自由能、显式碘或反应势垒。若提交者实际声称定量氧化能，需要配平物种及参照；若声称动力学顺序，需要相应路径/动力学证据。只有有效证据下仍未解决的实质序列解释冲突进入复核，已成立等价序列直接通过，实际主张所必需的证据缺失或连接性不成立失败。

**同步与边界。** 规则、reference conclusion、对应 supporting key point、evidence coverage 与私有 route 同步。六项仍为 20/15/20/15/15/15；公开题面已有 iodine 不必显式计算及端点/动力学区分，未再增补路线提示。不同氢库存绝对能不能相减成氧化 ΔG 的限制保留；原始 native 和历史验证文本未改，没有将来源播种验证宣称为盲态自主发现。

**实际修改文件（相对本任务包）。**

- `evaluation/evidence_map.json`
- `evaluation/reference_conclusions.json`
- `evaluation/reference_key_points.json`
- `evaluation/scoring_rules.json`
- `package_manifest.json`
- `paper_route.md`

另追加本篇 `修改说明/paper_0dc85595cab7bc0a.md`。本轮只修改四篇获准升级副本及对应说明；原版、其他任务、README、总体报告与 benchmark 代码均未编辑。

**检查结果与保留边界。** 已重建 manifest；所有包内 JSON 可解析，`validate_rubric` 与 `validate_task_package` 均通过，并将本篇复制到隔离目录后实际执行 `TaskRepository.from_v3` 加载成功。相对修复前快照，6 条 rule_id、reference_id、条数、100 分权重、已有数值 target/tolerance/unit、binding 与证据 ID 保持不变；规则/结论/generated supporting item 的预期和标题一致。`agent_input/data`、提交 schema、来源 evidence 数组及 historical 字段逐字或结构等值核对通过。未新增或删除包内文件。校验记录：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/02/validation.json`；修复前快照：`/tmp/rcb_upgrade19_20261027/confirmed_repairs/before/`。以上确认合同、同步和加载，不代表所有最终科学结论已获验收；没有新 QM/HPC、ARCHE 盲测或发布。

</details>
