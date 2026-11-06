# Second expert review — 2026-10-28

The reverse-scope rule now judges the submitted mapped endpoints and consistent energy references. Historical chair product mismatches are examples, not mandatory pathways or unique acceptable endpoints. Four forward targets/windows and other final conclusions remain unchanged. No new scientific calculations were run.

# V3 final-result evidence reuse — 2026-10-28

Preserve the full neutral-singlet C11H14 3a problem: four common-reference forward free-energy barriers, the two double-boat mechanisms, molecular organization and the distinction between forward and reverse/local and global references. Explicitly name the four neutral channel/geometry candidates already required by the old hidden rubric; no new channel, derivative or dynamics task is added.

Four final barrier rules reuse 23.505891604, 26.227907856, 38.209382937 and 36.931566173 kcal/mol for boat[3,3], boat[5,5], chair[3,3] and chair[5,5], preserving targets 23.5/26.2/38.2/36.9 and inclusive ±1.0 kcal/mol. Two final double-boat mechanism assignments reuse mapped endpoint and fixed-geometry electronic-stability evidence (minimum stability eigenvalues 0.0272093/0.0072799). The structural explanation reuses mapped angle/torsion and preparation energies. The final applicability result reuses the actual chair55 E3Z1 versus source3c E2Z2 mismatch and chair33 local/global conformer mismatch. Ordering and dominant-path synthesis are required in the answer but receive no second score on top of their numerical and explanatory propositions.

Limitations: Author thermochemical temperature and cutoff were not recovered. Existing verification declares 298.15 K, 1 atm, scale 1 and Grimme 100 cm−1; five tested thermal schemes preserve the boat gap (2.65159–2.884 kcal/mol). Chair55 local reverse 35.471401 differs from TS-minus-source-global3c 45.106927 kcal/mol; chair33 local reverse 16.325500 differs from global3d height 45.059106. No full chair55-to-source3c reverse path, exhaustive global conformer search, rates, trajectory branching or negative-activation-energy behavior is certified. Historical strict acceptance is frozen-scope evidence, not current V3 validation.

The current policy is paper_science_v3 / final_results_100. The text below is an unchanged historical record; its old policies, scores and PASS labels are not current V3 certification. No new calculation was run.

---

# V2 验证计算参考：Cope / 3a 重排

论文：`paper_a3892396b1843698`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：Five same-object source E/H/G rows agree with their printed SI values; valid saddles, true IRC segments plus independently relaxed/frequency-verified endpoints, atom/stereo maps, and invariant qualitative ordering support the required scientific result.

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/verification_forward_20261014T1430Z/coordinator_review/paper_a3892396b1843698/DECISION.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/verification_forward_20261014T1430Z/papers/paper_a3892396b1843698/W08_SCOPE_DECISION.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

冻结 V2 的完整 3a/C11H14 静态重排科学问题：主 boat 路径、四正向基线、构象与电子解释、参考/稳健性和结论边界。

冻结题面中的科学目标：

What rearrangement behavior is supported for the specified dibutadienylcyclopropane3a, and how do its accessible molecular geometries and electronic structure constrain the mechanistic interpretation?

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_a3892396b1843698/documents/supplementary_001.pdf](../../../../papers/paper_a3892396b1843698/documents/supplementary_001.pdf) | `d70347560db74d188f67b4507f632405908a9b8e8ef217e96519d8f4381ae7ea` |
| [papers/paper_a3892396b1843698/documents/main.pdf](../../../../papers/paper_a3892396b1843698/documents/main.pdf) | `fae49816db907e5dce86872c757d439fca946b2721e5af626900a04e54c98f57` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

```json
{
  "preserved": [
    "full C11H14 graph and specified starting stereochemistry",
    "Gaussian omegaB97X-D/def2SVP Opt/Freq and IRC",
    "omegaB97X-D/def2TZVPP single points",
    "GoodVibes Grimme entropy correction",
    "finite xTB-CREST and an independently verified DFT conformer",
    "native wavefunction stability tests"
  ],
  "declared_settings": "298.15 K, gas 1 atm, scale 1.0, Grimme cutoff 100 cm^-1 are frozen verifier conventions, not recovered private author settings. Existing 50/200, RRHO and Truhlar controls assess conclusion sensitivity.",
  "software_version_exception": "Installed Gaussian C.01 versus source B.01 follows the user-authorized installed-version policy; this is not used to excuse a numerical mismatch.",
  "equivalence_basis": "Five same-object source E/H/G rows agree with their printed SI values; valid saddles, true IRC segments plus independently relaxed/frequency-verified endpoints, atom/stereo maps, and invariant qualitative ordering support the required scientific result."
}
```

1. 由正文 Fig5、SI FigS1 和坐标核对完整中性单重态 C11H14/3a，保存原子映射、起始立体图及候选产物立体身份。已正式通过的是 upgrade_version2 两模式 14 个冻结文件，未分版本 upgrade_tasks 的 14 文件不匹配。

2. 按 Gaussian ωB97X-D/def2SVP 实际完成全局 3a、四个 boat33/boat55/chair33/chair55 鞍点的优化和频率；在对应同几何执行 ωB97X-D/def2TZVPP 单点。四鞍点均有一个与成断键对应的负模，不以仅正常结束代替鞍点有效性。

3. 读取四鞍点的双向真实 IRC 和随后独立松弛的八个端点，各端点 69 正模；配合负模方向、键变化及立体映射确认真实连接。boat33/55 与源 3a、3b/3c 对应；chair55 实际产物 E3Z1 与源 3c E2Z2 不同，分别保留。

4. 以同一个全局 3a 为零点，GoodVibes Grimme 熵修正合并电子能与热项；明确验证者约定 298.15 K、气相 1 atm、比例 1.0、100 cm⁻¹ cutoff。作者私人温度/cutoff 未唯一恢复；50/200 cm⁻¹、RRHO 和 Truhlar 共五种处理已实际比较，主要排序保持。

5. 实际得到四正向 ΔG‡ 23.505891604/26.227907856/38.209382937/36.931566173 kcal/mol，对源 23.5/26.2/38.2/36.9；逐对象五组 E/H/G 共 15 个分量恢复 SI p6 显示精度。该联合证据支持有据等价路线，无参数贴值或新容差。

6. 两 boat 的原生波函数 Stable 检查最低本征值 0.0272093/0.0072799；有限 xTB-CREST 加一个独立 DFT 构象未推翻当前 3a 参考。chair 构象准备成本约 3.47818/3.50052 kcal/mol；结构组织/环角与能垒并读，未冒称孤立张力能分解或全局穷尽搜索。

7. 完整记录非必要源配对例外：chair55 真实局部逆高度 35.471401 与相对源全局 3c 高度 45.106927 kcal/mol 不同；chair33 局部逆高度 16.325500 与源产物参考高度 45.059106 也不同。冻结题面要求四正向基线及所主张连接的证据，不宣称所有反向连接、动力学分支、实测速率或其他桥联骨架已复现。

### 原生有效性和依赖绑定

四鞍点、八个自由端点、单点与曲率均在正式回读中逐文件核对；四正向比较不以非必要反向配对为前提。冻结任务 14 项、历史证据 46 项以及 30 个 Gaussian 原生日志和 2 个其他分析日志已由协调者核对。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Main boat ΔG‡ (kcal/mol) | {"33":23.5,"55":26.2} | {"33":23.505891604202496,"55":26.227907856185293} | source3a commonreference;wB97XD/def2TZVPP//def2SVP;Grimme100 declared convention。 Source species/method/forward references and raw modes agree; actual scalar residuals +0.005892/+0.027908kcal/mol accompany a positive boat gap in all five thermal treatments. No old±3kcal/mol band or blanket printed-digit tolerance is used. |
| Chair forward ΔG‡ (kcal/mol) | {"33":38.2,"55":36.9} | {"33":38.20938293743572,"55":36.931566173034554} | 共同3a零点；actualchairreactantpreparationcostincluded。 Actual forward residuals +0.009383/+0.031566kcal/mol and sourceE/H/G components support four forward saddles. This does not validate the distinct source-product connection or reverse barrier. |
| Chair55 local/source product identity | source3cE2Z2 | {"localE3Z1":true,"stereo_preserving_maps":0,"nonstereo_maps":2} | sourceSI2diagram andSI12coordinate vs actualIRC freeendpoint。 The mismatch is explicit and remains relevant to a complete strict path certificate; it is not dismissed solely as a secondary source exception. No source3c is substituted for the actual chair55 endpoint.；这是保留的非必要源差异，不作为已复现量。 |
| Chair55 reverse reference (kcal/mol) | 45.1 | {"TS_minus_local":35.47140136417132,"TS_minus_source3c_global":45.10692672413737,"local_minus_global":9.635525359966046} | Localreturn和globalproductheight不同reference。 45.106927 is a separately calculated source-product reference height;35.471401 is the actual local-return height. Their different stereochemical references preclude treating them as the same measured/reproduced barrier.；这是保留的非必要源差异，不作为已复现量。 |
| Electronic stability and conformational control | 未给出／不适用 | {"boat33_stable_eigenvalue":0.0272093,"boat55_stable_eigenvalue":0.0072799,"extra_3a_conformer_G_kcal_range":[0.4297503022459868,0.4991380777034553]} | NativeStable扰动检查及finiteCREST/oneDFTdistinctconformer。 支持所验证闭壳层/参考态的有限解释，非所有自旋/构象全球证明；解释证据超过图像或两标量。 |
| Chair33 local versus source3d reference (kcal/mol) | 45.0 | {"local_reverse":16.325499736785723,"source_product_reference_height":45.05910563398684} | Local endpoint has the3d stereo graph but is a different high-energy conformation; parity-mapped mirror3d global energy is separately validated. Same molecular stereograph is not proof of the conformational path or its barrier. No conflation with chair55 stereoisomer mismatch.；源定位：mainp4/SI2 |

### 五个源对象的 E/H/G 分量

| 对象 | SI E/H/G（Eh） | 实算 E/H/G（Eh） | 来源与判定 |
|---|---|---|---|
| global_3a | ["-427.506278","-427.277479","-427.327967"] | [-427.50627838,-427.2774793539152,-427.3279672342465] | SI 物理 p6 §5，三分量均恢复显示精度；不是通用物理误差界 |
| boat33 | ["-427.471391","-427.244003","-427.290508"] | [-427.471390698,-427.24400347052864,-427.290508211593] | SI 物理 p6 §5，三分量均恢复显示精度；不是通用物理误差界 |
| boat55 | ["-427.468193","-427.240758","-427.286170"] | [-427.468192547,-427.2407578868461,-427.2861704025806] | SI 物理 p6 §5，三分量均恢复显示精度；不是通用物理误差界 |
| chair33 | ["-427.447669","-427.220603","-427.267077"] | [-427.447669473,-427.220602894361,-427.26707670666605] | SI 物理 p6 §5，三分量均恢复显示精度；不是通用物理误差界 |
| chair55 | ["-427.450440","-427.223619","-427.269113"] | [-427.450439591,-427.22361899424044,-427.26911303729884] | SI 物理 p6 §5，三分量均恢复显示精度；不是通用物理误差界 |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Mapped substrate and valid rearrangement identities

冻结要求：PreserveC11H14 and the specified starting stereochemistry; define proposed bond changes, charge/spin and conformers explicitly. A constrained geometry is not automatically an independently stable species. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：完整C11H14/q0/M1和3a起始立体图保留；boat33连接3a/3b，boat55连接3a/3c；chair反应物是3a构象，chair55产物E3Z1另列。 没有换物种或把几何约束当新稳定物种。真实chair55产物的立体诊断满足“定义对象”的要求；本节点不要求把它伪装成3c。

源定位：mainFig5/SI2,SI11–12coordinates。源一致性：Source3a及两boat产物立体身份匹配。chair55次级配对不匹配已明确，不参与boat身份验收。

### kp_rearrangement — Quantitative connected rearrangement evidence

冻结要求：New auditable calculations/analysis must address the claimed rearrangement behavior and mechanistic scope. Claimed saddles and endpoint connections need corresponding evidence. Do not require both author-named channels, a fixed multistart count or a prescribed intervention when an adequate alternative argument is supplied. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：四个源正向鞍点均重现：boat33/55 23.505891604/26.227907856，chair33/55 38.209382937/36.931566173kcal/mol；双向路径和自由端点给出实际连接。 不是只对上四个标量：四鞍点各一相关虚频，断1–2及成10–13或16–20的模向量/IRC一致；8自由端点各69正模。boat两路线与源主机制一致。chair55的声明限定为实际E3Z1分支，未宣称其连接源3c。冻结PR四正向基线及KP对已声明连接的证据均具备；未强加所有反向连接。

源定位：mainp4 Fig5;SI2FigS1/SI6。源一致性：四正向同定义匹配；源chair55→3c不复现，为非必需的附加配对例外，不豁免或改写该源断言。

### kp_explanation — Molecular geometry and electronic interpretation

冻结要求：Support the role assigned to geometry/electronic structure with discriminating evidence, not only structural pictures or source barrier repetition. Document observed collapse or indistinguishability honestly; missing paths alone do not prove their absence. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：几何组织及构象准备影响3a势垒；两boat波函数在实际Stable测试中稳定。不能把单一环角当作定量张力因果分解。 有判别量而非图片：3a环角61.1983°，boat33/chair33相近89.7975/89.6549°而势垒差别大；chair准备成本3.47818/3.50052kcal/mol独立保留。两boat最低稳定性本征值0.0272093/0.0072799且与父几何/能量相同。有限CREST及额外DFT构象对照未推翻3a参考。该证据支持源的几何组织解释，同时明确不提供孤立张力能或别的骨架radical/pancake结论。

源定位：mainp4 ring/geometry role;SI2overlays。源一致性：源boat较低和chair较高的结构组织结论有支持；源其他骨架加速倍数/精确4–9kcal张力分解不作为3a已复现量。

### kp_references — Correct energetic definitions and robustness

冻结要求：Separate electronic energy, enthalpy and free energy; use compatible reactant references, temperatures and correction conventions. Account for preparation costs if an imposed conformation is used. Investigate uncertainty that matters to the conclusion without mandatory±120 degree restraints. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists. The source identifies GoodVibes and Grimme quasi-RRHO entropy corrections (SI physical p6), but does not explicitly identify the low-frequency cutoff or thermochemical temperature in the reviewed method statements. Declare the chosen temperature, standard state and correction settings and assess uncertainty relevant to the claimed comparison; transparent justified substitutions are allowed. No undisclosed author setting is a required numerical target. The existing verifier used a 100 cm^-1 cutoff and 298.15 K (with declared standard-state and sensitivity conventions); these are verifier choices, not recovered author facts. Agreement with four source barriers cannot establish that the original authors used those settings.

当前复审：所有正向值以同一3a为零点，G=Ehigh+(Gcorrected_low−Elow)只加一次热项；T298.15K/1atm/Grimme100是声明约定，非猜中的源设置。 源SI中3a与四TS的E/H/G分量分别匹配其打印表示，支持同量组装而非只比较一个能垒。已算5种热处理的boat差2.651590881–2.883998800保持同号；额外3a构象高0.429750–0.499138；准备成本未删除。局部回程与全局产物参考已经分开，满足而非违反本节点对正确定义的要求。

源定位：SI6Grimme;mainmethodspp3–4。源一致性：source4forward同参考一致；声明未披露热参数符合冻结例外。35.471401与45.106927分别属于不同立体产品，均不互换。

### kp_scope — Static conclusion with appropriate bounds

冻结要求：Answer the3a question with supported, revised or investigated unresolved conclusions. A static barrier difference does not establish a trajectory branching ratio or the dynamic behavior of another bridged scaffold. Partial coverage and unsuccessful searches must remain explicit. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：指定3a的两个boat静态重排受支持且[3,3]较低；两个chair源正向高度也支持。chair55实际产物修正和全部有限性写入结论。 覆盖原问题的对象、重排行为、几何和电子解释，并非仅缩成一条成功路径。没有把静态能垒变成动力学分支、实验速率或其他桥联骨架的负活化能。chair55已有数值/立体诊断，不是缺失调查被改名为未决。

源定位：current3a finiteintramolecular question。源一致性：源任务内主boat机制、四正向基线、相对组织趋势保持；完整论文每个局部反向/标注均复现的说法不成立。

### conclusion_investigation — What rearrangement behavior is supported for the specified dibutadienylcyclopropane3a, and how do its accessible molecular geometries and electronic structure constrain the mechanistic interpretation?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list. Assess completion against the original public scientific question, not a self-narrowed addressed_scope. Missing necessary investigation, a failed calculation, copied public source values or a statement of source ambiguity earns no credit for the missing work and cannot yield whole-task full credit. Preserve credit for independently valid completed parts and accept sufficiently supported non-author conclusions without a fixed route or extra method matrix.

当前复审：对冻结3a问题，现有证据完整支持作者基线的四正向高度、两boat主连接和几何/电子约束；保留chair55附加产物配对的已证差异。 批准候选所依据的是已匹配的必要基线加完整物理判别证据，不是“允许反驳”一句话。所有5KP有直接证据且无已识别必要漏算；chair55→source3c的真实性不在冻结必需量中。将其作为全题硬门会额外增加“所有源反向连接须闭合”的要求。

源定位：currentobjective;mainFig5/SI1 route exceptions。源一致性：建议PASS_CANDIDATE针对完整冻结任务科学问题；不宣称源chair55配对已复现，不自动授中央PASS。

## 5. 实际计算时长与资源

本次直接从正式裁定引用的 32 个原生输出提取计时：正常结束且去重后的 Gaussian 阶段累计 33486.200 秒；其他可计时阶段 0.000 秒。这是部分归档累计，不是完整项目耗时或最小复现成本。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/COPE_RUNTIME_READBACK.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [global_3a_low.log · source_four_path_analysis/a01/global_3a_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/global_3a_low.log) | Gaussian:9800.8；Gaussian:8994.2 | 正常；正常 | {"threads":[2],"Gaussian_mem":["12000MB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat33_reverse.log · source_four_path_analysis/a01/boat33_reverse.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_reverse.log) | Gaussian:283；Gaussian:62.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat55_reverse.log · source_four_path_analysis/a01/boat55_reverse.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_reverse.log) | Gaussian:213.5；Gaussian:61.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair55_forward.log · source_four_path_analysis/a01/chair55_forward.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_forward.log) | Gaussian:104.8；Gaussian:58.9；Gaussian:87.5 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat33_low.log · source_four_path_analysis/a01/boat33_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_low.log) | Gaussian:70.2；Gaussian:61.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat33_forward_irc.log · source_four_path_analysis/a01/boat33_forward_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_forward_irc.log) | Gaussian:1327.7 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat33_reverse_irc.log · source_four_path_analysis/a01/boat33_reverse_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_reverse_irc.log) | Gaussian:1105 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat33_forward.log · source_four_path_analysis/a01/boat33_forward.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_forward.log) | Gaussian:161.5；Gaussian:57.4 | 正常；正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat55_low.log · source_four_path_analysis/a01/boat55_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_low.log) | Gaussian:98.4；Gaussian:88.8 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat55_forward_irc.log · source_four_path_analysis/a01/boat55_forward_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_forward_irc.log) | Gaussian:1310.1 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat55_reverse_irc.log · source_four_path_analysis/a01/boat55_reverse_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_reverse_irc.log) | Gaussian:1035.5 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat55_forward.log · source_four_path_analysis/a01/boat55_forward.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_forward.log) | Gaussian:184.7；Gaussian:54.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair33_low.log · source_four_path_analysis/a01/chair33_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_low.log) | Gaussian:68.1；Gaussian:59.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair55_low.log · source_four_path_analysis/a01/chair55_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_low.log) | Gaussian:71.6；Gaussian:62.1 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [gaussian.log · boat33_source_fixed_stability/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat33_source_fixed_stability/a01/gaussian.log) | Gaussian:49.3 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [gaussian.log · boat55_source_fixed_stability/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat55_source_fixed_stability/a01/gaussian.log) | Gaussian:49.3 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [global_3a_high.log · source_four_path_analysis/a01/global_3a_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/global_3a_high.log) | Gaussian:70 | 正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat33_high.log · source_four_path_analysis/a01/boat33_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_high.log) | Gaussian:101.1 | 正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [boat55_high.log · source_four_path_analysis/a01/boat55_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_high.log) | Gaussian:161.3 | 正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [gaussian.log · source_SI3c_exact_optfreq_SP/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_SI3c_exact_optfreq_SP/a01/gaussian.log) | Gaussian:75；Gaussian:59.8；Gaussian:87.8 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [gaussian.log · source_3a_crest_c02_optfreq/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_3a_crest_c02_optfreq/a01/gaussian.log) | Gaussian:109.4；Gaussian:46.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [analysis.log · source_four_path_analysis/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair33_forward.log · source_four_path_analysis/a01/chair33_forward.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_forward.log) | Gaussian:150.2；Gaussian:57.7；Gaussian:93.1 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair33_forward_irc.log · source_four_path_analysis/a01/chair33_forward_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_forward_irc.log) | Gaussian:1355.4 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair33_high.log · source_four_path_analysis/a01/chair33_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_high.log) | Gaussian:101 | 正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair33_reverse.log · source_four_path_analysis/a01/chair33_reverse.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_reverse.log) | Gaussian:478.9；Gaussian:50.3；Gaussian:74 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair33_reverse_irc.log · source_four_path_analysis/a01/chair33_reverse_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_reverse_irc.log) | Gaussian:1292.9 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair55_forward_irc.log · source_four_path_analysis/a01/chair55_forward_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_forward_irc.log) | Gaussian:1641 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair55_high.log · source_four_path_analysis/a01/chair55_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_high.log) | Gaussian:115.7 | 正常 | {"threads":[20],"Gaussian_mem":["90GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair55_reverse.log · source_four_path_analysis/a01/chair55_reverse.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_reverse.log) | Gaussian:363.9；Gaussian:49.8；Gaussian:74.1 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [chair55_reverse_irc.log · source_four_path_analysis/a01/chair55_reverse_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_reverse_irc.log) | Gaussian:1294.4 | 正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [runner.log · source_four_path_analysis/a01/runner.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/runner.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

```json
{
  "chair55_source_pairing_reproduced": false,
  "difference": "实际 chair55 局部产物 E3Z1 与源图 3c E2Z2 不同；35.471401 kcal/mol 局部逆高度不等于 45.106927 kcal/mol 相对源全局产物的高度。",
  "why_not_a_required_source_result_waiver": "冻结题面明列的是四个正向基线和 3a 静态机理问题；没有要求所有源反向配对成立。主 boat33/55 的 source endpoints 已匹配，四正向高度与 SI 分量匹配，chair 实际连接也已调查并如实报告。该例外不用于任何必要源一致性论证。",
  "not_established": [
    "作者为何将 chair55 与 3c 配对",
    "chair55 到源 3c 的直接完整连接",
    "所有源反向路径或所有论文结果",
    "动力学分支/实测速率/其他桥联骨架的行为",
    "构象搜索的全局穷尽性"
  ],
  "would_invalidate_claim": "若把 chair55→3c 或 45.1 kcal/mol 当作已经复现的实际局部逆路径，该声称不通过；当前参考结论必须保留上述区分。"
}
```

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_a3892396b1843698.json)

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| N0001 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/global_3a_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/global_3a_low.log) | `bbf485cb6af3068dd4c945ad5677d48efd66232b8bea7e07c5af85499d368e01` | coordinator_checked_native_or_analysis |
| N0002 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_reverse.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_reverse.log) | `473d61d2ddeda3a50201da6697c4ae94361fb180203f4a80791e7be699b78a62` | coordinator_checked_native_or_analysis |
| N0003 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_reverse.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_reverse.log) | `c57801b48a6bd857647342dce9c1899d4a5eb7f71c2897f2586e05f336c44567` | coordinator_checked_native_or_analysis |
| N0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_forward.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_forward.log) | `f10225a8537f4bcdd5f561d389dc7f663b3cc55417130c49a1b3b6b27c45de5c` | coordinator_checked_native_or_analysis |
| N0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/strict_endpoint_identity_readback_parserfix/a01/results/cope_endpoint_identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/strict_endpoint_identity_readback_parserfix/a01/results/cope_endpoint_identity.json) | `aadc7e56b1a5194bf93d4a11ce56db19556e30bec9cfd30a9b4d905cadb828b9` | coordinator_checked_native_or_analysis |
| N0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_three_products_common_reference_analysis/a01/endpoint_identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_three_products_common_reference_analysis/a01/endpoint_identity.json) | `aadc7e56b1a5194bf93d4a11ce56db19556e30bec9cfd30a9b4d905cadb828b9` | latest_review_evidence |
| N0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_low.log) | `b4d7b4910767466f3c0a019f9295cfc909b960eb9853b427f490e0716c5d0393` | coordinator_checked_native_or_analysis |
| N0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_forward_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_forward_irc.log) | `05d4df6cdc4e402e224e16e45ad7e6e5834e025dded6469e5a32d66879238453` | coordinator_checked_native_or_analysis |
| N0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_reverse_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_reverse_irc.log) | `6c963abf5534efb2dbf3186f95ad428eff94c3c718ad6b2afd0d9a6f8c1b8d45` | coordinator_checked_native_or_analysis |
| N0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_forward.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_forward.log) | `2a3c2ed4041e93170d7c129a09b57d1c2765ebcd9ec73454c07ff32ce3875507` | coordinator_checked_native_or_analysis |
| N0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_low.log) | `bbbadc7d2f65510a45a5d99eb19e12bff5229bb6534c105e08f723363e411803` | coordinator_checked_native_or_analysis |
| N0012 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_forward_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_forward_irc.log) | `7489ff6f534ace8832e8f12eb44d805d29e03607e9a67a9d0b607b6f8e52e303` | coordinator_checked_native_or_analysis |
| N0013 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_reverse_irc.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_reverse_irc.log) | `48a321800cfc3c51fd8dbde44f495c0b86fdd924f2eadfd57185ee5d168eb259` | coordinator_checked_native_or_analysis |
| N0014 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_forward.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_forward.log) | `155517fc3a9cafe5d90e668db3e11d9cd4d7450f950180683b531a7bddc1185f` | coordinator_checked_native_or_analysis |
| N0015 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair33_low.log) | `c867992e2186b2b85f7f8b998f43b3d98a497e66c1c684ff39f38519e444a22c` | coordinator_checked_native_or_analysis |
| N0016 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/chair55_low.log) | `e446732632942b76e34908617433ec10cc12003df45460c87e495059c293b667` | coordinator_checked_native_or_analysis |
| N0017 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/results/analysis_summary.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/results/analysis_summary.json) | `f5c3fc865305e16d72df40ab1024405025930b5fb3945eb1fec6da8405044a02` | coordinator_checked_native_or_analysis |
| N0018 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat33_source_fixed_stability/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat33_source_fixed_stability/a01/gaussian.log) | `a44a593c3922906165808ecf45df7892cfe039081089b47175f9c7bc046e0da7` | coordinator_checked_native_or_analysis |
| N0019 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat55_source_fixed_stability/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat55_source_fixed_stability/a01/gaussian.log) | `62a5310abdbe2f3aece7c32fa9a004b2972f450b75cc5e6da420421235bfaf39` | coordinator_checked_native_or_analysis |
| N0020 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/data/geometry_reference_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/data/geometry_reference_review_20260930.json) | `5b891bdb4fc9f922dd27b1cb14116f857e189a24843b677247449a55def723dc` | coordinator_checked_native_or_analysis |
| N0021 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/boat33_source_fixed_stability_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/boat33_source_fixed_stability_review_20260930.json) | `08bae4c798f110ef02e3adf0007d8b2223070463d12df020df192fa03e171d9c` | latest_review_evidence |
| N0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/boat55_source_fixed_stability_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/boat55_source_fixed_stability_review_20260930.json) | `584c0943d2ca8fd3e4261a4a2192f4b7fc9f7811aa63192cf53bc37d7ea23456` | latest_review_evidence |
| N0023 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/global_3a_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/global_3a_high.log) | `f7b0a12e3c6fbc2903d626e56937e611bd3043a5c9e5f2d1ed1c1a9915a9ff0c` | coordinator_checked_native_or_analysis |
| N0024 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat33_high.log) | `092ada202e07aae4b83dbca4403bd72e328498a070b418f3f4535377c93ed1a5` | coordinator_checked_native_or_analysis |
| N0025 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_high.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/boat55_high.log) | `fb946f50ac110b961ef8cd168239cd0faf074804b2554a7b5b991341f91996d4` | coordinator_checked_native_or_analysis |
| N0026 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_SI3c_exact_optfreq_SP/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_SI3c_exact_optfreq_SP/a01/gaussian.log) | `c0b0499b8668c4880de721100e7bce27ff290dc1f11a45a1f0762bbd8498fa46` | coordinator_checked_native_or_analysis |
| N0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_3a_crest_c02_optfreq/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_3a_crest_c02_optfreq/a01/gaussian.log) | `9910e3c8c33267834c746be171c40a1558b447222e7f126e6303d733bad11218` | coordinator_checked_native_or_analysis |
| N0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/data/source_3a_c02_composite_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/data/source_3a_c02_composite_review_20260930.json) | `9c27fcc05409fc2ee1ad9e6c60bd7bbd586082ac37d7f11ed9a015cd023f6956` | coordinator_checked_native_or_analysis |
| N0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_three_products_common_reference_analysis/a01/results/source_product_common_reference.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_three_products_common_reference_analysis/a01/results/source_product_common_reference.json) | `4e77f38384f89192273570a99d83d40168c44ee82a6af7885179ef450be8a7e0` | coordinator_checked_native_or_analysis |
| N0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/data/source_3a_crest_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/data/source_3a_crest_review_20260930.json) | `752d96f970b5e1c86b6def5441f1dbd24c7580ee03f6d5d4baa41c0114ac55ad` | coordinator_checked_native_or_analysis |
| N0031 | [papers/paper_a3892396b1843698/documents/supplementary_001.pdf](../../../../papers/paper_a3892396b1843698/documents/supplementary_001.pdf) | `d70347560db74d188f67b4507f632405908a9b8e8ef217e96519d8f4381ae7ea` | coordinator_checked_native_or_analysis |
| N0032 | [docs/v2_verification/history/verification_forward_20261014T1430Z/intakes/W08_SCOPE_CONTRACTS.json](../../../../docs/v2_verification/history/verification_forward_20261014T1430Z/intakes/W08_SCOPE_CONTRACTS.json) | `d88d6cc0c5dfea42b0884c9b092aca62081ea7db8cf5ba8a696b644644343ab7` | latest_review_evidence |
| N0033 | [docs/v2_verification/history/verification_forward_20261014T1430Z/intakes/W08_SCOPE_NATIVE_AND_RECEIPTS.json](../../../../docs/v2_verification/history/verification_forward_20261014T1430Z/intakes/W08_SCOPE_NATIVE_AND_RECEIPTS.json) | `ccdbbbce8b80c84e94648732033c2851534db9ae2db8b650a5c9740b61558a22` | latest_review_evidence |
| N0034 | [tasks/final_verified_paper_reproduction/paper_a3892396b1843698/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_a3892396b1843698/evaluation/scoring_rules.json) | `12e0c7cc8f85e2469b9441f9d4c0c601f3bff45d6d8bd579f5deabef780bfdd9` | coordinator_checked_native_or_analysis |
| N0035 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_a3892396b1843698/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_a3892396b1843698/NATIVE_READBACK.json) | `7bfc32efa6284537b5f89456b8891ef1e1148fac65ac9831df90f18704fa37e4` | coordinator_checked_native_or_analysis |
| N0036 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W08_RETURN_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W08_RETURN_INTAKE.json) | `ffcd8d44104220283be1f0de54d1fe9782f69ac6f5a70d93251052e05204f265` | coordinator_checked_native_or_analysis |
| N0037 | [tasks/final_verified_paper_reproduction/paper_a3892396b1843698/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_a3892396b1843698/evaluation/verified_computation_reference.md) | `38e143756763952280d6afd61cd23332bcce80de1444d20f4474d85f3ad65d39` | coordinator_checked_native_or_analysis |
| N0038 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/agent_input/task.md) | `e5c5ecc87febe8f32e7145d814e8877b30bdb3e8f7350eb42501a96f6ea6b6a9` | coordinator_checked_native_or_analysis |
| N0039 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/reference_key_points.json) | `86654c73f88b52af70656849ca978f7e06f97813d19ea9dc51eb0d9bb647bc7f` | coordinator_checked_native_or_analysis |
| N0040 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/reference_conclusions.json) | `9819b49877a2869410acc5d0f4bdfb2aa5c70261e4a18040e79277465dc32d4f` | coordinator_checked_native_or_analysis |
| N0041 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/scoring_rules.json) | `413c29914a6801737983d526bfb914b7849e4d51fffa36f6c7e029c0e4d298c5` | coordinator_checked_native_or_analysis |
| N0042 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/evaluation/critical_failures.json) | `83bdc2cce6dba7b1e0aa5c1fc61488315b60a29be11d2779aa100c05618bf843` | coordinator_checked_native_or_analysis |
| N0043 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_a3892396b1843698/package_manifest.json) | `9938d2219b57af7737aaea313344c4d7ba39149e2f4106ce187352ce1b0ea318` | coordinator_checked_native_or_analysis |
| N0044 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/agent_input/task.md) | `d0a3d9fedcb29d7d1a1e948eb59ddd1c5aacdd5ce411ac8c694480c0410f6f92` | coordinator_checked_native_or_analysis |
| N0045 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/reference_key_points.json) | `86654c73f88b52af70656849ca978f7e06f97813d19ea9dc51eb0d9bb647bc7f` | coordinator_checked_native_or_analysis |
| N0046 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/reference_conclusions.json) | `9819b49877a2869410acc5d0f4bdfb2aa5c70261e4a18040e79277465dc32d4f` | coordinator_checked_native_or_analysis |
| N0047 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/scoring_rules.json) | `413c29914a6801737983d526bfb914b7849e4d51fffa36f6c7e029c0e4d298c5` | coordinator_checked_native_or_analysis |
| N0048 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/evaluation/critical_failures.json) | `83bdc2cce6dba7b1e0aa5c1fc61488315b60a29be11d2779aa100c05618bf843` | coordinator_checked_native_or_analysis |
| N0049 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_a3892396b1843698/package_manifest.json) | `d1d9dbe3772d6e8a1c8aeb377c10a6303b7bd54166d2c7a50610cd8d9c6503da` | coordinator_checked_native_or_analysis |
| N0050 | [papers/paper_a3892396b1843698/documents/main.pdf](../../../../papers/paper_a3892396b1843698/documents/main.pdf) | `fae49816db907e5dce86872c757d439fca946b2721e5af626900a04e54c98f57` | coordinator_checked_native_or_analysis |
| N0051 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/events_20261007/PUBLIC_SOURCE_RECHECK_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/events_20261007/PUBLIC_SOURCE_RECHECK_20261007.json) | `b6791f0ceb0562a7fce789546e252f2937021b57b8a7bca3c15d35a716c2e01b` | coordinator_checked_native_or_analysis |
| N0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/analysis.py) | `ac5a4b8087cc2e5afd8ec2e5a57cd6719d56a4c93c14750ec9bc44cec5ee0997` | saved_input_or_driver_adjacent_to_verified_output |
| N0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/native_gaussian.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/native_gaussian.py) | `b6adb055f8133e4e7baf6cb93e581b94a75409ef1698ff167b1bb9363c8ad5d9` | saved_input_or_driver_adjacent_to_verified_output |
| N0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | saved_input_or_driver_adjacent_to_verified_output |
| N0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/inputs.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_four_path_analysis/a01/inputs.json) | `2b18d1e3432198bca316dbe555573ed2280c533e2ad4782468386c0a5dd87259` | saved_input_or_driver_adjacent_to_verified_output |
| N0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat33_source_fixed_stability/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat33_source_fixed_stability/a01/input.com) | `32b6ce6d24e630ab1f70ef71de883061489ca00d59c43a17f3a5b22a7cb37ee1` | saved_input_or_driver_adjacent_to_verified_output |
| N0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat33_source_fixed_stability/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat33_source_fixed_stability/a01/run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | saved_input_or_driver_adjacent_to_verified_output |
| N0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat55_source_fixed_stability/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat55_source_fixed_stability/a01/input.com) | `171866804ade65f192b596f242059cad2a27c84bc4b70f3108caed6201590e39` | saved_input_or_driver_adjacent_to_verified_output |
| N0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat55_source_fixed_stability/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/boat55_source_fixed_stability/a01/run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | saved_input_or_driver_adjacent_to_verified_output |
| N0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_SI3c_exact_optfreq_SP/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_SI3c_exact_optfreq_SP/a01/input.com) | `482ad42fd6c5fd11d4d85d0a380d8b5806ddb418edf55e8f9c5850de24d9ae7a` | saved_input_or_driver_adjacent_to_verified_output |
| N0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_SI3c_exact_optfreq_SP/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_SI3c_exact_optfreq_SP/a01/run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | saved_input_or_driver_adjacent_to_verified_output |
| N0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_3a_crest_c02_optfreq/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_3a_crest_c02_optfreq/a01/input.com) | `80ff367d003b68742bf396487e17f54612ef018cec11ff6d347600bbcea7ade2` | saved_input_or_driver_adjacent_to_verified_output |
| N0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_3a_crest_c02_optfreq/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/v2_execution_20260929/outputs/source_3a_crest_c02_optfreq/a01/run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | saved_input_or_driver_adjacent_to_verified_output |
| N0064 | [docs/v2_verification/history/verification_forward_20261014T1430Z/coordinator_review/paper_a3892396b1843698/DECISION.json](../../../../docs/v2_verification/history/verification_forward_20261014T1430Z/coordinator_review/paper_a3892396b1843698/DECISION.json) | `0ddb993f3e02cd2a01fdceed5a53d8d29ce5edba8844d2034ec69e8308c62701` | authoritative_current_review |
| N0065 | [docs/v2_verification/history/verification_forward_20261014T1430Z/papers/paper_a3892396b1843698/W08_SCOPE_DECISION.json](../../../../docs/v2_verification/history/verification_forward_20261014T1430Z/papers/paper_a3892396b1843698/W08_SCOPE_DECISION.json) | `dc46bbe807bac4a8786088bfb0abcc0ce7f9b034911ede974707eea4882a3826` | authoritative_current_review |
| N0066 | [docs/v2_verification/history/verification_forward_20261014T1430Z/coordinator_review/paper_a3892396b1843698/ROOT_NATIVE_READBACK.json](../../../../docs/v2_verification/history/verification_forward_20261014T1430Z/coordinator_review/paper_a3892396b1843698/ROOT_NATIVE_READBACK.json) | `9808757e7c54976209613aa26b7ebea18a86c4b023feb6c0f67d79389d8e30de` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_a3892396b1843698/agent_input/task.md](../agent_input/task.md) | `e5c5ecc87febe8f32e7145d814e8877b30bdb3e8f7350eb42501a96f6ea6b6a9` |
| [tasks/v2_autonomous_research/paper_a3892396b1843698/evaluation/reference_key_points.json](reference_key_points.json) | `86654c73f88b52af70656849ca978f7e06f97813d19ea9dc51eb0d9bb647bc7f` |
| [tasks/v2_autonomous_research/paper_a3892396b1843698/evaluation/reference_conclusions.json](reference_conclusions.json) | `9819b49877a2869410acc5d0f4bdfb2aa5c70261e4a18040e79277465dc32d4f` |
| [tasks/v2_autonomous_research/paper_a3892396b1843698/evaluation/scoring_rules.json](scoring_rules.json) | `413c29914a6801737983d526bfb914b7849e4d51fffa36f6c7e029c0e4d298c5` |
| [tasks/v2_autonomous_research/paper_a3892396b1843698/evaluation/critical_failures.json](critical_failures.json) | `83bdc2cce6dba7b1e0aa5c1fc61488315b60a29be11d2779aa100c05618bf843` |
| [tasks/v2_autonomous_research/paper_a3892396b1843698/evaluation/evidence_map.json](evidence_map.json) | `31d4e788be2d6635d478c892118c2de1daed5b386fe61766d8790d6def97c46e` |
| [tasks/v2_autonomous_research/paper_a3892396b1843698/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `704c8be3969f40e9b581f9259ff65c7921efd964093fbd21d8739e8851a9cb19` |

## Current scoring migration — 2026-10-19
Active policy: paper_science_v2, 100 binary scientific-result points with intermediate and final conclusions. Active rule/reference files supersede historical scoring weights or freezes. No process score or multiplier remains. This migration is not new computation or new chemical acceptance; independently strict frozen-scope status remains unchanged. Preserved limitations: Verified four forward G barriers23.505891604,26.227907856,38.209382937,36.931566173kcal/mol versus23.5,26.2,38.2,36.9. FiveE/H/G rows recover printed precision; verifier thermochemical settings are not recovered private author settings. Chair55 local E3Z1 differs from source3c E2Z2:35.471401 local reverse versus45.106927 TS-minus-source-global3c. Chair33 local reverse16.325500 differs from45.059106 source-global3d height; same stereograph does not make conformers identical. No complete chair55-to-source3c path, all reverse pathways, global conformer exhaustion or dynamics validated.

## Scoring-contract repair — 2026-10-19, round 3

- Confirmed independent saddle states were bundled: split closed-shell evidence into boat[3,3] and boat[5,5] leaves (3+3). Preserve the source forward-barrier references and local-versus-global product stereochemistry/conformer distinction; no new reverse-path validation.

The source and native calculations above remain unchanged historical evidence. Active mode-specific rules govern current scoring; this edit does not certify a new chemistry run or alter strict acceptance.
