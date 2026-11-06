# Round-one scope notice — 2026-11-03

The existing scientific scope is retained. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## 2026-10-27 V3 final-result migration

Three independent final explanations retain all seven substrates and the carbonyl, side-chain and primary/secondary comparisons. Old geometric, spin and conformer nodes are supporting evidence, not separate process scores. No new quantum-chemistry or HPC jobs were run. Existing native results are reused only for the matching final claims listed in evidence_map.json; historical PASS labels are not transferred. Native eight+1doublet minima support selected-conformer electronic explanations, not full yields/kinetics/HAT/decomposition. Full CREST search not rerun; S1 andS6-c2 rebuilt, source negativeNBO energy definition unresolved, thermal corrections differ and primaryDCM comparison is unmatched. The dated record below is retained verbatim.

## 2026-10-23 科学分V2维护副本

当前私有评分为`paper_science_v2`，共7个二元科学项，中间关键节点55分、最终结论45分，总计100分。全部过程分已删除。新规则不设数值硬窗口，不改变既有定性验收或数值差异记录。公开输入保持原样，题面中旧过程分/60+40措辞不代表本维护副本实际计分，作为专家待审文字遗留披露。科学评分资格与发布资格分开，见`reference_qualification.json`。

## 2026-10-23 当前科学问题验证过程与结果汇总

当前AR状态：`PROVISIONAL_PASS_QUALITATIVE`；这是已完成独立审查后的定性验收，不是尚未验收的候选。严格整题数值复现未登记，数值偏差和实现差异保留供专家判断。本节整合既有实际计算，没有新增量化计算。

### 方法、模型与执行过程

UB3LYP/6-311G(d,p)气相优化/未缩放频率，同几何SMD-MeCN单点，298 K、1 atm，与作者明确设置一致。实际Gaussian16 C.01/NBO3.1；六个身份复用来源坐标，S1补全缺失两H、S6-c2重建；未重跑完整Rowan/CREST筛选。

1. 验证七种身份的+1双重态自由基阳离子及S6第二构象，共8个分子图，全部优化完成且零虚频。
2. 执行8组气相优化/频率和8个同几何溶剂单点，核对C3/O4映射、电荷、自旋分布及S6两构象溶液G。16个阶段正常终止。
3. 对照三组科学比较：羰基类型、甲基/丁基侧链、初级/次级；保留初级DCM与次级MeCN条件差异，未把电荷当势垒或把构象能当HAT速率。

### 论文与计算数值对照

|物理量与参照|论文值|计算值|计算−论文|单位|
|---|---|---|---|---|
|S6 c2−c1的G|2.5|2.862083|+0.362083|kcal/mol|
|S1 C3电荷，对正文|0.06200|0.06362|+0.00162|e|
|S1 C3电荷，对SI|0.07359|0.06362|−0.00997|e|
|初级S19 C3电荷|−0.09979|−0.10894|−0.00915|e|
|S1 O4电荷|−0.37817|−0.34032|+0.03785|e|
|S1气相电子能|−907.307640|−907.298896786|+0.008743214（约+5.49 kcal/mol）|Eh|
|S1溶液电子能|−907.388500|−907.386559943|+0.001940057（约+1.22 kcal/mol）|Eh|

### 定性结论与保留项

羰基相关局部电子差别、丁基侧链构象/自旋差别，以及初级/次级C3极性差异均支持当前题目限定的分子解释。并非完整收率排序、全部HAT或分解机制均得到证明。

- 未重跑完整构象筛选，S1及c2重建不等于找到了作者所有原始构象或全局构象集合。
- S1绝对能和各体系热G修正差异未解释；作者负NBO C3–O4能量缺少无歧义定义/自旋汇总，不能声称该列数值复现。
- 电荷、几何和自旋分布只支持有限解释；未计算完整取代/HAT/分解势能面，不宣称唯一成因或精确收率。
- S6不可逆但无相同TEMPO+返回特征，不能把所有低产体系归为同一种已证明反应命运；初级DCM与次级MeCN不是匹配条件对照。

### 原生结果、独立复核及来源

- [acceptance_audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_ea6/acceptance_audit.md)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [acceptance_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_ea6/acceptance_audit.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [independent_native_checks.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_ea6/independent_native_checks.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_ea6fdc38b4a7f8c7/documents/main.pdf)：PDF页序（1-based）3,4。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_ea6fdc38b4a7f8c7/documents/supplementary_001.pdf)：PDF页序（1-based）73,74,75,76,77,78,79,80,81。

来源方法未报告项、数值差异与题外未计算项目不能混为同一类问题。下方原有记录按日期保留，旧candidate/pending仅表示当时状态，不覆盖本节引用的最新父级验收。

### ea6全部51条已审计来源数值对照

以下直接读取独立审计的51条`author_comparisons`，包含电荷、电子能、热G修正、虚频数和无法无歧义匹配的NBO能量；不省略未匹配项。原子标签依真实分子图映射，S19与正文初级S14对应。SI绝对能/热修正表未打印单位，Eh依据Gaussian量级与物理类型推定；电荷单位e，构象差单位kcal/mol。Eh差乘627.509474仅用于量级展示，不改变参考态。

|物种/构象|物理量|论文值|计算值|计算−论文|单位|能量残差换算(kcal/mol)|
|---|---|---|---|---|---|---|
|S6.+|C3自然电荷（对SI）|0.06247|0.06272|0.00025|e|—|
|S6.+|O4自然电荷|-0.32285|-0.33246|-0.00961|e|—|
|S6.+|气相电子能|-1003.3785|-1003.37852927|-0.00002927|Eh|-0.018367202|
|S6.+|溶液电子能|-1003.4593|-1003.45929764|0.00000236|Eh|0.001480922|
|S6.+|热G修正|0.448358|0.442879|-0.005479|Eh|-3.438124408|
|S6.+|虚频数|0|0|0|count|—|
|S6.+|C3–O4负NBO能量描述符|-603.1|未形成可匹配量|未形成可匹配量|kcal/mol|—|
|S5.+|C3自然电荷（对SI）|0.07777|0.0744|-0.00337|e|—|
|S5.+|O4自然电荷|-0.38048|-0.38072|-0.00024|e|—|
|S5.+|气相电子能|-885.40861|-885.408608575|0.000001425|Eh|0.000894201|
|S5.+|溶液电子能|-885.48502|-885.485016291|0.000003709|Eh|0.002327433|
|S5.+|热G修正|0.368237|0.365541|-0.002696|Eh|-1.691765542|
|S5.+|虚频数|0|0|0|count|—|
|S5.+|C3–O4负NBO能量描述符|-601.6|未形成可匹配量|未形成可匹配量|kcal/mol|—|
|S3.+|C3自然电荷（对SI）|0.06163|0.0585|-0.00313|e|—|
|S3.+|O4自然电荷|-0.36601|-0.3653|0.00071|e|—|
|S3.+|气相电子能|-790.77585|-790.775853235|-0.000003235|Eh|-0.002029993|
|S3.+|溶液电子能|-790.85438|-790.854377812|0.000002188|Eh|0.001372991|
|S3.+|热G修正|0.327272|0.32446|-0.002812|Eh|-1.764556641|
|S3.+|虚频数|0|0|0|count|—|
|S3.+|C3–O4负NBO能量描述符|-615.3|未形成可匹配量|未形成可匹配量|kcal/mol|—|
|S8.+|C3自然电荷（对SI）|0.04869|0.0455|-0.00319|e|—|
|S8.+|O4自然电荷|-0.35999|-0.35894|0.00105|e|—|
|S8.+|气相电子能|-751.46111|-751.46110525|0.00000475|Eh|0.00298067|
|S8.+|溶液电子能|-751.54416|-751.544152972|0.000007028|Eh|0.004410137|
|S8.+|热G修正|0.301591|0.298901|-0.00269|Eh|-1.688000485|
|S8.+|虚频数|0|0|0|count|—|
|S8.+|C3–O4负NBO能量描述符|-622.1|未形成可匹配量|未形成可匹配量|kcal/mol|—|
|S7.+|C3自然电荷（对SI）|0.05062|0.04955|-0.00107|e|—|
|S7.+|O4自然电荷|-0.37007|-0.36941|0.00066|e|—|
|S7.+|气相电子能|-676.18323|-676.18323443|-0.00000443|Eh|-0.002779867|
|S7.+|溶液电子能|-676.26772|-676.267718901|0.000001099|Eh|0.000689633|
|S7.+|热G修正|0.296266|0.29502|-0.001246|Eh|-0.781876805|
|S7.+|虚频数|0|0|0|count|—|
|S7.+|C3–O4负NBO能量描述符|-625.1|未形成可匹配量|未形成可匹配量|kcal/mol|—|
|S19_primary_source_Shash|C3自然电荷（对SI）|-0.09979|-0.10894|-0.00915|e|—|
|S19_primary_source_Shash|O4自然电荷|-0.36046|-0.35979|0.00067|e|—|
|S19_primary_source_Shash|气相电子能|-867.98019|-867.980191181|-0.000001181|Eh|-0.000741089|
|S19_primary_source_Shash|溶液电子能|-868.06238|-868.062380648|-0.000000648|Eh|-0.000406626|
|S19_primary_source_Shash|热G修正|0.347263|0.343824|-0.003439|Eh|-2.158005081|
|S19_primary_source_Shash|虚频数|0|0|0|count|—|
|S19_primary_source_Shash|C3–O4负NBO能量描述符|-623.3|未形成可匹配量|未形成可匹配量|kcal/mol|—|
|S1_complete_graph|C3自然电荷（对SI）|0.07359|0.06362|-0.00997|e|—|
|S1_complete_graph|O4自然电荷|-0.37817|-0.34032|0.03785|e|—|
|S1_complete_graph|气相电子能|-907.30764|-907.298896786|0.008743214|Eh|5.486449618|
|S1_complete_graph|溶液电子能|-907.3885|-907.386559943|0.001940057|Eh|1.217404148|
|S1_complete_graph|热G修正|0.373585|0.368645|-0.00494|Eh|-3.099896802|
|S1_complete_graph|虚频数|0|0|0|count|—|
|S1_complete_graph|C3–O4负NBO能量描述符|-608.3|未形成可匹配量|未形成可匹配量|kcal/mol|—|
|S1_complete_graph|C3自然电荷（对正文）|0.062|0.06362|0.00162|e|—|
|S6_c2_minus_c1|溶液G(c2−c1)|2.5|2.862083262|0.362083262|kcal/mol|—|

七个体系的热G修正残差约−0.78至−3.44 kcal/mol，成因尚未确认；S6为−3.438124、S1为−3.099897 kcal/mol。这些绝对修正残差不等同于S6同分子构象差的误差（+0.362083 kcal/mol）。未引入事后偏移或臆测的准谐校正。NBO原生输出是分自旋轨道本征值与占据数，作者负能量汇总定义不明，因此没有可合法直接相减的配对值；不能将它冒充键解离能或反应势垒。

[完整独立审计及对应原生输出入口](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_ea6/acceptance_audit.json)。


---

## 历史验证记录（原文保留）

<!-- parent-acceptance-20261022T2343Z -->
## 父级独立审查验收（2026-10-23 UTC）

当前模式状态：`PROVISIONAL_PASS_QUALITATIVE`。当前 AR/PR 共享七体系问题的三个必要结论已有有效计算支持，无阻断性科学缺口，无需为当前问题补充新的量化计算。此状态不等于精确数值、完整作者构象搜索协议、官方评分或发布通过。下方候选状态、底层旧的whole_task_pass=false及“缺c2”文字为过程记录；有效c2已核验，当前定性验收以本段为准，不据此改写严格数值状态。

独立复核确认8个完整分子图、8个无虚频极小值、16个正常原生阶段及日志哈希。核心量子方法为UB3LYP/6-311G(d,p)、气相优化/未缩放频率、同几何SMD-MeCN单点，298 K/1 atm，与作者明确设置一致。CREST未重新执行、S1和c2构型重建、具体软件/NBO实现及TCG差异仍须披露。

| 比较量 | 作者 | 计算 | 计算−作者 |
|---|---:|---:|---:|
| S6 c2−c1，kcal/mol | 2.5 | 2.862083 | +0.362083 |
| S1 C3电荷，SI，e | 0.07359 | 0.06362 | −0.00997 |
| S1 C3电荷，正文，e | 0.06200 | 0.06362 | +0.00162 |
| 初级S19 C3电荷，e | −0.09979 | −0.10894 | −0.00915 |
| S1气相电子能，Eh | −907.307640 | −907.298896786 | +0.008743214 |
| S1溶液电子能，Eh | −907.388500 | −907.386559943 | +0.001940057 |

碳酰基比较、侧链构象/电子效应及初级/次级捕获倾向的有限解释均获支持；不把原子电荷当势垒，不把构象能当HAT机制，不声称精确收率排序或所有底物同一反应命运。S6近接c2的O···N为2.545133 Å，远离c1为3.337674 Å，支持近接构象代价的方向。

完整51项来源/原生对照、不能同量比较的NBO能量项及方法差异见独立审查：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/acceptance_audit_ea6/acceptance_audit.json`；父级登记：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/parent_acceptance_decision.json`。当前语义评分没有数值容差，未新增隐藏阈值或调整评分。

保留的限制：

- Author electronic method/model retained: UB3LYP/6-311G(d,p), +1 doublets, gas Opt/Freq, same-geometry SMD-MeCN SP, unscaled frequencies at 298 K/1 atm. Exact unreported revision/grid/SCF/NBO settings identity is not established.
- Rowan/CREST full conformer search was not rerun. Six source identities reused; S1 was rebuilt because printed coordinates omit two aryl H; near-contact S6-c2 was reconstructed and freely optimized. Supports selected minima and paired comparison, not a global conformer ensemble.
- S1 gas/solution electronic energy differences are +0.008743214/+0.001940057 Eh; full source/native thermal-G corrections differ with unexplained cause and are retained in the 51-item independent comparison.
- Author negative NBO C3-O4 energy descriptor lacks an unambiguous spin aggregation/definition; it is not claimed reproduced or interpreted as a bond dissociation energy/kinetic barrier. The current task does not require that particular descriptor.
- The three current conclusions support limited electronic/conformational explanations and experimental constraints. They do not establish HAT/degradation pathways, exact rates/yields, a monotonic seven-system yield law or a single fate for all poor substrates.
- Primary DCM crude-NMR and secondary MeCN isolated-yield observations have different conditions; electrochemical persistence alone does not determine productive capture.
- Historical whole_task_pass=false fields are not numerical strict passes. Older missing-c2 prose is superseded by the independently verified c2 native data and this timestamped acceptance, while original records are retained.

<!-- end-parent-acceptance-20261022T2343Z -->

# Independent computation verification — 2026-10-22 follow-up

Current shared AR/PR status: PROVISIONAL_PASS_QUALITATIVE **candidate, pending independent parent review**; no registered acceptance or strict numeric pass.

Assigned original snapshot: `da527363933e011945917545d7145d6cb75f81b02ad08d4abb69d6e93f60625a`. Evidence directory: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T2343Z`.


结论：当前 AR/PR 共享科学问题已具备 **PROVISIONAL_PASS_QUALITATIVE 候选**证据，待父级独立审查；不是严格数值通过，不改变评分、容差或全局计数。

实际计算覆盖七个 +1 双重态自由基阳离子及一个 S6-c2：UB3LYP/6-311G(d,p) 气相优化/频率，298 K、1 atm；相同几何的 SMD-MeCN 单点及 Gaussian 内置 NBO 3.1 分析。八个优化正常终止、零虚频，八个溶剂单点正常结束，溶液自旋 S² 经消除后均为 0.75。原子图、C3/O4 映射、总 NPA 电荷约 +1 及总自旋约 1 已独立核验。S1 原坐标缺两枚芳环 H，采用已披露的完整分子图独立构型；这不构成精确作者构象复现。

**C_CARBONYL：有条件的碳酰基影响得到实际支持。** S1/S3/S5 的 C3 自然电荷为 +0.06362/+0.05850/+0.07440，均高于 S7 醛 (+0.04955) 与 S8 酸 (+0.04550)，支持后两者在此氧化态中较弱的局部亲电性，符合反应表现变差的方向。该指标不能解释 S1、S3、S5 之间 82%、70%、44% 的精确收率，也不等于取代速率。S3/S5/S7/S8 都具有 O1···N5 近接（2.51–2.69 Å）和可分辨的羰基 O1 自旋；然而醛/酸仍不发生所需产物形成，故五元环近接/自旋分布不是生产性反应的充分条件。S7/S8 不可逆 CV 带 TEMPO+ 返回峰，与后续消耗/断裂相容，但不能唯一指定产物或速控步。保留 E1/2 与不可逆 Ep/2 的区别。

**C_SIDECHAIN：侧链改变构象可及性和电子分布，未确定具体分解命运。** S5 的 O1···N5=2.508 Å、O1 自然自旋 0.07871；S6-c1 为 3.338 Å、O1 自旋约 −0.00003（N5=0.71116），显示羰基参与显著减弱。S6-c2 无约束优化后仍是独立近接构象，O1···N5=2.545 Å、O1 自旋 0.05346，最终完整共价图与 c1 一致；不是结构损坏或坍缩回 c1。按 E_solution+(G_gas−E_gas)，c2−c1=+2.862083 kcal/mol，作者 +2.5，差 +0.362083。这直接支持丁基体系偏好远离构象的解释；仅在两构象模型下 c2/c1≈0.00796，不能当完整构象采样。S6 不可逆 CV 且无 TEMPO+ 返回峰，区别于醛/酸；侧链 HAT/分解仍为假说，没有计算或声称 HAT、取代势垒。

**C_PRIMARY_INTEGRATION：电化学寿命与捕获效率不同。** 初级 S19 的 C3 电荷为 −0.10894，次级 S1 为 +0.06362，支持前者在本模型中对亲核捕获较不有利；其近接构型/较强羰基 O1 自旋并不保证生产性反应。初级与次级表现出相近的 CV 持续性，仍可有不同产物捕获行为。12% 初级值来自 DCM 粗 NMR 筛选（且有10%原料残留），82% 次级值是 MeCN 基准分离收率；MeCN DFT/CV 不消除这一混杂。模型只解释趋向和限制，不预测同条件精确收率，也不把所有失败归为同一化学命运。

数值与模型边界：S1 的 SI C3=+0.07359 与正文 +0.062 本身不一致；计算 +0.06362，两项参照均保留。S1 独立构象、NBO版本、表中 TCG 与原生 RRHO 校正的差异均在 author_comparison.json 报告有符号/绝对偏差。S1 也未呈现 S5 式近接，进一步限制将该构型当普遍必要条件。NBO 负轨道能不是解离能/势垒；不跨不同分子组成相减绝对能量。显式亲核试剂、碱、电极、电解质及动力学未在作者基准中建模，本题不凭空追加这些计算作为验收门槛。

证据：completed_verified_stages.json（八个极小值、16个有效阶段的日志/哈希）、nbo_geometry_analysis.json（映射、距离、二面角、两种自旋分布及构象能）、author_comparison.json（逐项作者差异）。原始作业 bd85e141 与 c2 后继 fee97009 均已完成并释放。当前需要父级审查，不需要新增量化计算。


Native completed stages (final-state validity only; TS reaction interpretation and minima identity are separate):

| Case | Stage | Electronic energy / Eh | Native RRHO G / Eh | Imaginary modes | Wall seconds |
|---|---|---:|---:|---:|---:|
| S6.+ | optfreq | -1003.37852927 | -1002.935651 | 0 | 1693.87 |
| S6.+ | solvent_sp | -1003.45929764 | — | — | 101.89 |
| S5.+ | optfreq | -885.408608575 | -885.043067 | 0 | 937.49 |
| S5.+ | solvent_sp | -885.485016291 | — | — | 73.34 |
| S3.+ | optfreq | -790.775853235 | -790.451393 | 0 | 790.39 |
| S3.+ | solvent_sp | -790.854377812 | — | — | 57.31 |
| S8.+ | optfreq | -751.46110525 | -751.162204 | 0 | 597.25 |
| S8.+ | solvent_sp | -751.544152972 | — | — | 53.25 |
| S7.+ | optfreq | -676.18323443 | -675.888214 | 0 | 643.48 |
| S7.+ | solvent_sp | -676.267718901 | — | — | 48.95 |
| S19_primary_source_Shash | optfreq | -867.980191181 | -867.636367 | 0 | 992.90 |
| S19_primary_source_Shash | solvent_sp | -868.062380648 | — | — | 77.35 |
| S1_complete_graph | optfreq | -907.298896786 | -906.930252 | 0 | 2337.09 |
| S1_complete_graph | solvent_sp | -907.386559943 | — | — | 80.26 |
| S6_c2 | optfreq | -1003.37881232 | -1002.934515 | 0 | 5541.71 |
| S6_c2 | solvent_sp | -1003.45615567 | — | — | 101.64 |

Author comparison (calculated minus author; numerical tolerances unmodified):

| Quantity | Author | Calculated | Signed difference | Absolute difference | Units |
|---|---:|---:|---:|---:|---|
| S6.+ C3_NPA_charge | 0.062470 | 0.062720 | +0.000250 | 0.000250 | e |
| S6.+ O4_NPA_charge | -0.322850 | -0.332460 | -0.009610 | 0.009610 | e |
| S5.+ C3_NPA_charge | 0.077770 | 0.074400 | -0.003370 | 0.003370 | e |
| S5.+ O4_NPA_charge | -0.380480 | -0.380720 | -0.000240 | 0.000240 | e |
| S3.+ C3_NPA_charge | 0.061630 | 0.058500 | -0.003130 | 0.003130 | e |
| S3.+ O4_NPA_charge | -0.366010 | -0.365300 | +0.000710 | 0.000710 | e |
| S8.+ C3_NPA_charge | 0.048690 | 0.045500 | -0.003190 | 0.003190 | e |
| S8.+ O4_NPA_charge | -0.359990 | -0.358940 | +0.001050 | 0.001050 | e |
| S7.+ C3_NPA_charge | 0.050620 | 0.049550 | -0.001070 | 0.001070 | e |
| S7.+ O4_NPA_charge | -0.370070 | -0.369410 | +0.000660 | 0.000660 | e |
| S19_primary_source_Shash C3_NPA_charge | -0.099790 | -0.108940 | -0.009150 | 0.009150 | e |
| S19_primary_source_Shash O4_NPA_charge | -0.360460 | -0.359790 | +0.000670 | 0.000670 | e |
| S1_complete_graph C3_NPA_charge | 0.073590 | 0.063620 | -0.009970 | 0.009970 | e |
| S1_complete_graph O4_NPA_charge | -0.378170 | -0.340320 | +0.037850 | 0.037850 | e |
| S6.+ gas_SCF | -1003.378500 | -1003.378529 | -0.000029 | 0.000029 | Eh |
| S6.+ solution_SCF | -1003.459300 | -1003.459298 | +0.000002 | 0.000002 | Eh |
| S6.+ thermal_G_correction | 0.448358 | 0.442878 | -0.005480 | 0.005480 | Eh |
| S5.+ gas_SCF | -885.408610 | -885.408609 | +0.000001 | 0.000001 | Eh |
| S5.+ solution_SCF | -885.485020 | -885.485016 | +0.000004 | 0.000004 | Eh |
| S5.+ thermal_G_correction | 0.368237 | 0.365542 | -0.002695 | 0.002695 | Eh |
| S3.+ gas_SCF | -790.775850 | -790.775853 | -0.000003 | 0.000003 | Eh |
| S3.+ solution_SCF | -790.854380 | -790.854378 | +0.000002 | 0.000002 | Eh |
| S3.+ thermal_G_correction | 0.327272 | 0.324460 | -0.002812 | 0.002812 | Eh |
| S8.+ gas_SCF | -751.461110 | -751.461105 | +0.000005 | 0.000005 | Eh |
| S8.+ solution_SCF | -751.544160 | -751.544153 | +0.000007 | 0.000007 | Eh |
| S8.+ thermal_G_correction | 0.301591 | 0.298901 | -0.002690 | 0.002690 | Eh |
| S7.+ gas_SCF | -676.183230 | -676.183234 | -0.000004 | 0.000004 | Eh |
| S7.+ solution_SCF | -676.267720 | -676.267719 | +0.000001 | 0.000001 | Eh |
| S7.+ thermal_G_correction | 0.296266 | 0.295020 | -0.001246 | 0.001246 | Eh |
| S19_primary_source_Shash gas_SCF | -867.980190 | -867.980191 | -0.000001 | 0.000001 | Eh |
| S19_primary_source_Shash solution_SCF | -868.062380 | -868.062381 | -0.000001 | 0.000001 | Eh |
| S19_primary_source_Shash thermal_G_correction | 0.347263 | 0.343824 | -0.003439 | 0.003439 | Eh |
| S1_complete_graph gas_SCF | -907.307640 | -907.298897 | +0.008743 | 0.008743 | Eh |
| S1_complete_graph solution_SCF | -907.388500 | -907.386560 | +0.001940 | 0.001940 | Eh |
| S1_complete_graph thermal_G_correction | 0.373585 | 0.368645 | -0.004940 | 0.004940 | Eh |
| S6 c2-c1 solution Gibbs energy | 2.500000 | 2.862083 | +0.362083 | 0.362083 | kcal/mol |
| S1_complete_graph C3_NPA_charge versus main text | 0.062000 | 0.063620 | +0.001620 | 0.001620 | e |

Frozen computational provenance:

- Job `hpc-job-bd85e141-e1c5-46c9-9418-413ebd7f456f`: `SUCCEEDED` at `2026-10-22T23:53:20.353900+00:00`; frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/job_spec.json`; native audit `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T2343Z/job_audits/hpc-job-bd85e141-e1c5-46c9-9418-413ebd7f456f/native_audit.json`.
- Job `hpc-job-fee97009-1af6-4371-b9a4-7ac1d1a4cca4`: `SUCCEEDED` at `2026-10-22T23:53:19.199879+00:00`; frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T1743Z/S6_c2_continuation/job_spec.json`; native audit `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T2343Z/job_audits/hpc-job-fee97009-1af6-4371-b9a4-7ac1d1a4cca4/native_audit.json`.

Completed application logs:

- S6.+/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S6.+/optfreq.log`, SHA256 `bbf0ab001d4d660e9daec96e0fc786f80aa374965d45057a22d0ca3445881404`; return code `0`, normal termination `True`.
- S6.+/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S6.+/solvent_sp.log`, SHA256 `22042cfd2d3e2390919f3a19cff8a76940484c07914cf795a58dfeaa56119388`; return code `0`, normal termination `True`.
- S5.+/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S5.+/optfreq.log`, SHA256 `958f8570b7e157f24c47b698c7bdc4f442f1547a2066c37c3c1a274dc13bc75e`; return code `0`, normal termination `True`.
- S5.+/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S5.+/solvent_sp.log`, SHA256 `19069473f1f5a876add7fb0f0b1b688bdb3ea03cef7d90083bff9c100b090a02`; return code `0`, normal termination `True`.
- S3.+/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S3.+/optfreq.log`, SHA256 `1adf103c877b715927b82d360208dd74122f41e7746aaaedfdf86182a647f89f`; return code `0`, normal termination `True`.
- S3.+/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S3.+/solvent_sp.log`, SHA256 `47e19ba3f9b73235315685894536cf61564e76943169413842e42db952ac012f`; return code `0`, normal termination `True`.
- S8.+/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S8.+/optfreq.log`, SHA256 `1dfe41cd9074b81d007c3d6da2dac8d825f0d137021f7bad4da21b6ca175ae4d`; return code `0`, normal termination `True`.
- S8.+/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S8.+/solvent_sp.log`, SHA256 `a927f767f0374a2033f0c13c5aeabecdb368a412795a0da6be3549cfe363cd84`; return code `0`, normal termination `True`.
- S7.+/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S7.+/optfreq.log`, SHA256 `9c2ee910ac36653d9adaf04be71967d479bac32504d70f08322aad1012d4cb26`; return code `0`, normal termination `True`.
- S7.+/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S7.+/solvent_sp.log`, SHA256 `703352ad3890d4b54aea5342b8dfa1c869694275e8fed5da434a73dc64704f2a`; return code `0`, normal termination `True`.
- S19_primary_source_Shash/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S19_primary_source_Shash/optfreq.log`, SHA256 `75675cd12ab86c19f69b5b6a481cf75d7010dafc993bdb02ac58f96afda662fd`; return code `0`, normal termination `True`.
- S19_primary_source_Shash/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S19_primary_source_Shash/solvent_sp.log`, SHA256 `8fe851a28bdaa4b11b85a696681b0fb00e3ecf9450ef92330778613394bb4b06`; return code `0`, normal termination `True`.
- S1_complete_graph/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S1_complete_graph/optfreq.log`, SHA256 `4b8105fdc1a620a0d8655e0dc609c905ea40962f030df672229ee2b55afc2f41`; return code `0`, normal termination `True`.
- S1_complete_graph/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/new44_20261022/calculation/S1_complete_graph/solvent_sp.log`, SHA256 `a347cc6dfb4f9286f053e44dd0e7e031816c6529a577b657edb8205a873f03e7`; return code `0`, normal termination `True`.
- S6_c2/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T1743Z/S6_c2_continuation/S6_c2/optfreq.log`, SHA256 `b02097299e4303d6e4c15394c63b825b81f5e4cc9a1b164b1652860ea433aa8b`; return code `0`, normal termination `True`.
- S6_c2/solvent_sp: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T1743Z/S6_c2_continuation/S6_c2/solvent_sp.log`, SHA256 `19d158162bc41db2b320e3c3fe2ac74afc5fbc2c632b016bcc9b129d276b5139`; return code `0`, normal termination `True`.

Source/method deviations remain in the frozen specs and `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T2343Z/author_comparison.json`. For optimized final geometries, graph checks, atom maps and hashes see `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_ea6fdc38b4a7f8c7/short_job_followup_20261022T2343Z/completed_verified_stages.json`. Whole-question coverage and pending work: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/new44_group_01/coverage.json`. No task text, scoring, tolerances, expert packages or global counts were modified.
