# final 任务科学正确性与验证充分性复审

日期：2026-09-17。状态：**审计结论与处置建议，等待负责人反馈；未修复、未迁移。**

本文集中记录当前 final 全集的重新审计，不替代五个 evaluator JSON，不是新的评分标准。所有验证记录、作者结构及本报告均属于维护者材料，不得进入被评 agent 的输入。本轮没有修改任务包、论文、`docs/verification`、评分代码或既有验证结果，没有新增量化计算、操作 HPC、移动任务或发布。

## 1. 结论、范围与统计

**当前 70 篇、137 个 final 任务不能整体宣布为“科学及发布检查全部通过”。**除了之前发现的评分字段和档案路径问题，本次补查旧批次的科学证据，确认还有对象连接错误、物理量定义不完整和验证结论超出真实输出的问题。

| 当前目录 | 论文数 | AR 自主科研 | PR 论文复现 | 任务包数 |
|---|---:|---:|---:|---:|
| `final_verified_*` | 70 | 67 | 70 | 137 |
| `hold_verified_*` | 4 | 4 | 4 | 8 |
| `verified_tasks` 待处理任务 | 0 | 0 | 0 | 0 |

以下是对 **final 70 篇**的互斥处置建议，按论文计；同一论文两模式已分别查看，可以共用一条有效科学验证链。仅 `6943…`、`d796…`、`44f…` 没有 AR。

| 处置建议 | 论文数 | 任务包数 | 含义 |
|---|---:|---:|---|
| H：建议暂缓，待关键证据或科学边界闭合 | 4 | 8 | `4fa592…`、`51a036…`、`b5c446…`、`d91572…`，均为 AR+PR；不能仅改文字或保留 PASS 标签宣称全部验证 |
| M：核心计算有据，但当前输入、定义或评分需要修订 | 13 | 25 | 大部分无需新量化计算；部分修改涉及计量协议/评分边界，仍需负责人确认 |
| R：主要是参考档案过期或链接错误 | 4 | 8 | `a6e8…`、`fda8…`、`1b285…`、`534ae…`；已有可复用证据，不应直接判为必须补算 |
| S：本次未发现新的核心科学阻塞 | 49 | 96 | 在逐篇列出的有限科学范围内有计算支持；不等于所有过程分、任意方法、全局搜索或部署已验证 |
| 合计 | 70 | 137 | 上述计数不叠加第 7 节的跨包评分接口问题 |

**建议暂缓不等于证明任务在科学上无解。**其中 `4fa…` 已确认现有成功链研究了另一连接异构体；另外三篇是当前材料尚不能支持全部必评科学断言，应先追查已有数据或做已有波函数/轨迹的分析，不能直接要求整篇重算。本轮不执行这些建议。

已有 hold 也不能照搬旧结论：`b815…` 的第二网格与态身份证据已补齐，本次读原始输出复核后，建议进入恢复前维护；其余三篇仍应保留 hold。详见第 8 节。

## 2. 判定口径与实际审计深度

1. **接受作者路线验证。**历史验证使用论文/SI 的作者终态、TS 或已知路线，是允许的。当前 agent 要自行生成 TS 或初始构象，不因此使历史验证失效；不以“当前公开 starter 没有盲跑”为补算理由。
2. **区分对象输入与答案输入。**给定结构的性质任务可以提供该对象；如果任务评的是发现/优化这个结构，作者终态就不能公开。此前批准的五篇给定对象任务 `d2d08…`、`e31…`、`d8e549…`、`c23cf…`、`80cc…` 不重新按几何答案泄露处理。其他已明确限定的给定对象性质任务也按同一原则判断。
3. **按科学量核对，不只查文件。**重点是连接/取代位置、电荷自旋、计算物理量、溶剂/温度/参考零点、频率/电子态身份、量值与结论是否对应。正常退出只能证明程序完成，不能代替这些判断。
4. **不把论文中的断言自动当成验证结果。**真实能量、频率和光谱数值存在，仍可能不能支持所声称的反应连接、跃迁归属或宏观机制。原文有错误或方法描述不唯一时，记录差异，不为了得到 PASS 选择答案。
5. **reference 只是档案。**其旧 `EVIDENCE_COMPLETE`、`APPLICABLE_TO_CURRENT_FINAL` 标签不能覆盖新发现的反例。评分继续以 evaluator 的关键点和结论为准。

本次在此前新批次 17 篇的详细核查基础上，补读了旧 53 篇的当前题面、公开输入、科学评分和验证结果，逐篇判断；对疑点回到正文/SI、原始输出、结构或波函数。对 4fa 做了原始几何连接恢复和振动/TD 输出核对；对 51a/d915 读了真实 IRC 轨迹；对 b5c 重读了 NTO cube；对 b815 从新 OUTCAR/EIGENVAL/PROCAR 重新提取量值。全量字段兼容性检查覆盖了 137 包。

**审计限度：没有重新运行化学计算，也没有逐字精读所有历史失败/重试日志。**70 个 PR reference 直接链接的现存 `.log/.out` 去重有 1121 份，约 3.5 GB；这个数量是档案盘点，不是“1121 份日志已全部科学认证”。此前 17 篇的 98 份原始输出检查已记录在[维护报告第 14 节](MAINTENANCE_REPORT.md#14-对既有审查过程及发布条件的最终复核2026-09-17)，不重复冒称全部重新计算。

此前审查的不足主要是：旧 53 篇沿用较多既有结论；部分检查验证了目录/schema/数值存在，却没有继续核对异构体、同一电子态的证据或有限 IRC 的实际连接。这次发现的问题应覆盖相应旧的“可直接发布”表述，而不是再用旧报告抵消原始证据。

## 3. 建议暂缓的四篇 final 论文

### H1. paper_4fa592965be9841e — group_3，AR、PR

**最关键的问题是研究对象不一致，已确认，不只是怀疑 SMILES 不合法。**

- [正文](../../papers/paper_4fa592965be9841e/documents/main.pdf) PDF p1 的名称、p2 Fig. 1 的合成图一致：苯基和腈基接在丙烯腈双键的同一个碳上，另一个双键碳接噻吩。图示也与由 2-(4-aminophenyl)acetonitrile 缩合的路线一致。
- 当前公开 [compound_I.json](../final_verified_paper_reproduction/paper_4fa592965be9841e/agent_input/data/inputs/compound_I.json) 的名称对应上述对象；但 SMILES 含非法 `N=CH`，且连接写法与名称不一致。
- reference 主链的 [Freq 输入](../../docs/verification/group_3/paper_4fa592965be9841e/artifacts/gaussian/compoundI_author_6311gplus_freq/input.com) 以及实际计算坐标恢复出的非立体连接为 `N#CC=C(c1ccc(N=Cc2cccs2)cc1)c1cccs1`：苯基与噻吩接在同一个双键碳，腈基接在另一侧。
- 论文图的非立体连接应为 `N#CC(=Cc1cccs1)c1ccc(N=Cc2cccs2)cc1`。两者都可有 C18H12N2S2、34 原子，核对分子式不足以区分。
- 本次读取该 group 目录下全部 6 份 `.xyz`，恢复出的连接均为前者，没有发现可替换主链的正确连接 XYZ。这不代表其他未归档位置绝不可能存在正确输出。

此外还有两个独立问题：

1. 任务要求实验比较，却明确把实验数值隐藏，公开输入没有相应观测。只隐藏计算答案是合理的；要求 agent 自己给出实验比较却不给观测则不完整。
2. [汇总脚本](../../docs/verification/group_3/paper_4fa592965be9841e/provenance/materialize_exact_author_route.py) 将最接近两实验峰的 S8/S1 作为两条诊断带。真实 TD 中 S8 为 276.78 nm、f=0.0422，而 S3/S4 分别 f=0.2671/0.2292。靠“离实验最近”不能证明它们是任务要求的两最强/诊断带。原文 Table 4 把约 1450 cm⁻¹ 标为 C–H stretching；真实频率的 1460.7571 cm⁻¹ 确实存在，但该模式沿 C–H 键的伸缩投影很小，本次简单位移检查约 0.0022；实际高频 C–H 伸缩组在约 3013–3243 cm⁻¹，对应同一投影约 1.15–1.19。这是模式归属问题，不能因论文也这么写就略过。该投影只是诊断，不是新的评分阈值。

**已有计算能证明什么：**另一连接异构体的极小值、真实频率和 TD 态确实算出了；四个摘录频率不是凭空编造。但它们不能验证论文指定对象的光谱，也不能凭量值接近排除身份错误。

**建议：**两模式暂缓。先按正文图修正确切连接和 E/E 立体定义，查找是否已有正确对象的计算。若没有，保留原科学目标就必须由验证方处理正确对象；不能把当前错误异构体改名当正确。再解决实验观测输入、模式归属与选带规则，最后更新 reference。仅修 SMILES 语法/注释不足以恢复发布。不能提前保证无需补充计算。

### H2. paper_51a03695e1ccb105 — group_3，AR、PR

**问题是“已经连接到规定反应物/产物盆地”的证据不足，不是使用了 SI TS。**

当前[任务](../final_verified_paper_reproduction/paper_51a03695e1ccb105/agent_input/task.md)要求验证 iminotriazole anion + nitrosotriazole 到中性 azo + OH⁻ 的原子/电荷守恒耦合，包含相关虚频和 IRC 或等价连接检验。

已有证据包括四个端点极小值、一个虚频 −1650.1799 cm⁻¹ 的 TS，以及复合自由能 ΔG‡=13.2521335、ΔG_rxn=−29.5339201 kcal/mol，符合现有 13.35±3、−29.58±5 的数值目标。这部分不撤销。

但是 [IRC 原始输出](../../docs/verification/group_3/paper_51a03695e1ccb105/artifacts/gaussian/azo_TS2_si_cpcm_ts_irc_retry2_unbounded16g/stdout.log) 两方向各走 100 点，均到步数上限结束。按输出中每方向最后一个 `CURRENT STRUCTURE` 读取，使用该 18 原子作业的 1-based 编号：

| 距离 / Å | forward 最后点 | reverse 最后点 | 能说明的内容 |
|---|---:|---:|---|
| N8–N9 | 1.460321 | 1.415034 | 两侧都已有近距离 N–N 连接，不能直接认作分离的两反应物 |
| N9–O18 | 1.374330 | 1.480448 | 两侧 N–O 仍接近成键距离，不能直接认作已经脱离的 OH⁻ |
| N8–H17 | 1.023161 | 2.006356 | 支持质子沿路径发生转移 |
| O18–H17 | 2.125623 | 0.982053 | 与质子转移一致 |

这支持一个真实的质子转移路径片段，但当前 `results.json` / reference 把正常结束直接写成“连接到经验证的 reactant/product basins”，超出了上述记录。已找到的独立 reactant/product 极小值不能自动证明这条 TS 与它们相连；本次未找到相应 IRC 末点后续优化/身份映射的有效链。

**建议：**两模式暂缓该完整“已验证耦合路径”认证。优先请验证方提供已有的末点优化、完整路径或其他等价连接证据；若现有其他输出可以闭合，只需分析与归档。若没有，保留当前完整连接要求就存在最小验证缺口；是否补该环节由负责人另定。不能仅把 `normal termination` 换成更强措辞，也不能私自把任务缩为“已给 TS 上的单点能差”。

### H3. paper_b5c446c7067dd511 — group_3，AR、PR

**能隙与高三重态能量可及性已有计算；必评的附近高三重态混合 LE/CT 特征没有被现有汇总证明。**

[正文](../../papers/paper_b5c446c7067dd511/documents/main.pdf) PDF p3/Fig. 3 对四分子的 S1 以及附近 Tn 做了 NTO/IFCT 解释，明确是同一电子态内部的局域与转移成分。两模式 evaluator 同样要求 relevant low singlet **and nearby triplet states** 的混合特征。

[现有结果](../../docs/verification/group_3/paper_b5c446c7067dd511/report/results.json)包含四分子的极小值、S1/T1 能隙和低十个 singlet/triplet 的能量，支持 An-mP 的最大 S1–T1 gap，并找到了距 S1 较近的 Tn。已保存的 NTO cube 则仅对应 S1/T1。当前论证主要是“S1 有较大质心分离，T1 较局域，因此支持 mixed LE/CT”；不同态分别具有 CT/LE 不能代替同一态的混合特征证明，也不能代替附近 Tn 的空间分析。

本次进一步读取已有 S1 cube，按 `sum(abs(h*e))/sqrt(sum(h*h)*sum(e*e))` 重提取主 NTO 对的空间重叠，Ph/Na/An/Py 分别约 **0.6882/0.6670/0.7166/0.6427**；对应已有质心分离约 **3.08/4.46/4.09/6.18 Å**。这表明 S1 并非完全没有“重叠同时有分离”的证据，可从既有文件补实；这些数不是完整多 NTO 对 IFCT 百分比，也不直接证明整个 hot pathway。

**建议：**两模式暂缓完整 HLCT/hot-channel 结论验收，先从已有 TD 日志、匹配的基态/TD checkpoint 做 S1 与附近 Tn 的同态 NTO/片段分析，保留分子/根/片段身份。原则上可能通过已有波函数后处理解决，**目前不能宣布需要重做四分子 Opt/TD，更不增加 SOC、RISC 速率或动力学要求**。若既有波函数不能恢复该证据，再列最小缺失量。修复 reference 的跨态推理，不能把必评附近 Tn 的特征静默降为 optional。

### H4. paper_d91572979a89303a — group_3，AR、PR

**四个数值能垒有据，但当前要求的完整连通机理没有被同一有效计算链覆盖。**

真实 [strict_v2 汇总及原始路径](../../docs/verification/group_3/paper_d91572979a89303a/provenance/strict_v2_observables.json)给出四个势垒 **29.987730、44.073768、20.068195、32.737759 kcal/mol**，对应 30.4、43.2、19.8、32.7（±2），相关频率/溶液单点存在。

但当前[任务](../final_verified_paper_reproduction/paper_d91572979a89303a/agent_input/task.md)明确要求从 separated reactants 到 product 的 connected profile，包含 [2,3]-Wittig rearrangement。正文 PDF p5 和 SI PDF p51/Table S1 都有 **INT1A → TS2A → INT2A**。现有 strict 链只有九个状态；旧 INT1A 和 3a 的独立计算存在，但本次找到的 TS2A 只有 SI 提取坐标，没有对应已验证的 TS2A 计算输出或等价连接闭合。

IRC 核查也不能支持“全部已连通”的现有说法：

- [TS1A irc2](../../docs/verification/group_3/paper_d91572979a89303a/artifacts/gaussian/TS1A_rerun_retry_irc2_unbounded16g/stdout.log)及 irc3 均正常结束，但每方向只有 **1 个实际点**。Gaussian 提示检测到 PES minimum，这仍需要结构身份验证；irc2 两侧 S12–C33 为 3.069/3.082 Å、C33–C34 为 1.783/1.777 Å，不能仅靠结束字符串认证为两个不同的目标盆地。
- TS3A-TXT、TS4A-TXT 的迁移后成功日志真实存在，不应再沿用旧取消日志说它们没运行；它们与 TS3B 都有两侧各 50 点的有效路径，但到步数上限，需实际末点/连接说明，不能声称均完成了端点极小值优化。
- 当前 `results.json` 中 `connected_state_ids` 都为空，部分连接链接仍指失败/旧运行；新能量和旧候选标签混用。空字段本身不是科学反例，但与上述原始缺口一致。

另一个可直接修订的问题是热力学定义：SI p51 明确半熵约定，实际采用 `Gsol = E_SP + Hcorr − 0.5*(Hcorr−Gcorr)`；task 只要求自选热校正，未公开此主比较量定义。换成常规全熵 G 并不是同一评分量。SI 的泛函/色散简称与实际 Gaussian 路线也应按真实输入区分记载，不能把现存 wB97XD 输入写成未运行的独立 GD3BJ 方案。

**建议：**两模式暂缓完整机理认证。先整理真实已成功的局部能垒、频率和迁移 IRC，查找 TS2A 与端点身份的其他既有证据；公开半熵主比较定义。如果没有，保留完整机理目标就需要验证方补最小缺环节。将任务缩成四局部能垒会改变科学覆盖，必须由负责人明确决定，不能作为普通文字修复。本轮不补算。

## 4. 核心计算有据、建议原地修订的 13 篇

以下均影响两模式，唯 `6943…` 只有 PR。这里“无需新量化计算”指建议的任务修订本身可使用现有输出，不保证所有可选扩展也已有验证。公开实验观测、单位/参考零点与计量协议时，仍不公开待求的作者计算答案。

### M1. paper_60f4c45810428116 — group_1，Fc 标尺及参考结构定义

公开 `species.json` 的 Fc/Fc⁺ SMILES 都有未闭合的 ring `1`，解析失败。更重要的是，[任务](../final_verified_paper_reproduction/paper_60f4c45810428116/agent_input/task.md)允许自行构造 Fc 参考，却没有给固定 gold 所依赖的标尺。

本次目视核对 [SI](../../papers/paper_60f4c45810428116/documents/supplementary_001.pdf) PDF p19/Table S6，确有 **5.36 V** 绝对 Fc 标定。现有 [真实结果](../../docs/verification/group_1/paper_60f4c45810428116/report/results.json)：用此标定得 −1.743824/−2.822484 V，满足 −1.75/−2.81±0.2；独立 LANL08 Fc 参考则得 −0.616311/−1.694970 V，整体相差约 1.1275 V。符合公开题面的一种参考实现会被固定 gold 判错。

**建议：**修复 Fc 身份表示；明确本任务主报告采用 `E_vsFc = −ΔG/(nF) − Eabs(Fc)`，并公开同一参考约定，独立 Fc 计算另列 sensitivity。5.36 是测量标尺而非 1a/1h 的待求答案，但采用固定标尺仍应在负责人批准后同步两模式。若坚持完全自主计算参考，则应另议评分可比性，不能保留未披露标尺的固定绝对目标。已有计算足够，不需重算。

### M2. paper_94e7481ded3b6a75 — group_1，绝对能量与自由方法冲突

任务允许选择任意量化方法，但 evaluator 对 E=−1087.1445139 Eh、G=−1086.786988 Eh 使用 ±0.01 Eh。绝对电子总能/自由能不是方法独立量，仅要求报告方法不能解决可比性。

正文 PDF p5–6 说明 B3LYP/6-31G(d)；现有该路线得 E=−1087.144521883793、G=−1086.786926、ZPE=0.410486 Eh、S=160.846 cal mol⁻¹ K⁻¹，支持原数值。建议公开数值主比较所需的方法/基组/气相/298.15 K/热力学约定，其余探索另列；或者保留方法自由并重新定义方法条件化评分，需负责人选择，不能静默放宽原容差。

reference 的旧非正交 AO 系数平方“局域化百分比”也应更新为现有 native Multiwfn Mulliken 记录，或明确只是旧定性诊断。现有核心 HOMO/LUMO 分区约 86.27%/92.21%，无需新的电子结构计算。

### M3. paper_9a58a1fa6ed7d780 — group_1，H 描述符被写成质心距离

两模式 task 把 H 定义为 `hole centroid distance`，却另有 D 质心分离。实际 Multiwfn H 是空穴/电子分布空间展宽的平均尺度，D 才是质心间距；见本地[官方手册](../../.software_cache/documentation/multiwfn/2026.9.1/Multiwfn_manual_2026.9.1.pdf) PDF p266、p808。已有 S1 D≈0、H=3.954 Å、Sr=0.7802，说明两者不是同一个距离。

建议在两模式定义 H、D、Sr、t、HDI/EDI 的含义和实现约定，不公开目标值；同步 schema 字段说明。已有 S1–S6 TD 和 S1–S4 Multiwfn 可复用；原始日志里的轨道贡献应补入 reference，不能把 parser 未保留写成没有计算。不需新量化计算。

### M4. paper_2f2aa11ea61a32bb — group_2，要求实验比较但缺少公开实验观测

当前只提供 1a–d 四份 XYZ，task/deliverable 要求与甲苯 UV–vis 比较。[结果](../../docs/verification/group_2/paper_2f2aa11ea61a32bb/report/results.json)也明确实验最大峰值未提供。Opt/Freq 与 TD20 存在，已计算波长 361.55/396.34/420.49/405.62 nm；缺的是比较输入，不是整个计算链。

[正文](../../papers/paper_2f2aa11ea61a32bb/documents/main.pdf) PDF p2–3/Table 1 给出甲苯实验带 345/375/383/381 nm；1c 另有更强的约 339 nm 高能带。建议补一个只含实验波长、溶剂、分子/峰身份的表，说明比较最低带还是强带；作者 TD 值、振子强度及轨道结论仍私有。不能把 gas-phase 理论和 solution 实验的差别隐去。不需新量化计算。

### M5. paper_0de37d01e35c27df — group_2，带符号差值与评分目标反号

当前研究对象 C10H14S2/26 原子已修正，本次不再提出旧分子式问题。真实 S···S 为 4.056140073 → 3.983239316 Å，task 定义 cation−neutral，即 **−0.072900758 Å**；scoring 却用 **+0.073 Å**，并把绝对距离字段与差值字段绑在同一 numeric rule。±0.2 的宽容差掩盖了反号，不代表规则正确。

建议把带符号目标统一为 −0.073，单独绑定差值；绝对距离、算术和收缩方向分别核对，保留原容差，不用取绝对值让膨胀也通过。无需补算。

### M6. paper_0a62b797f51de2c0 — group_2，ESP 极性文字冲突

`reference_key_points.json` 的 result-pattern 写 electron-rich thiophene / electron-deficient cyano，另一个 key point 及 scoring 却要求 thiophene 正势、cyano 负势。正文 PDF p5 对 MESP 描述也是后者。把势符号、电子富/缺和 donor/acceptor 混写会导致评委自相矛盾。

建议统一为明确的 MESP 正/负区域及表面约定，以图和输出判定；不要把 donor 角色简单等同于局部负 ESP。已有偶极 1.1744/6.0547/3.3867 D、ESP 差 30.95/68.08/64.43 kcal/mol 可用。当前 evaluator 已允许有据解释非单调，**不重新要求单调排序或补算去追趋势**。

### M7–M8. paper_4e9774f4128551d3、paper_db6c4e0558113873 — group_2 / group_3，溶液自由能条件不完整

| 论文 | 当前缺失与有效证据 | 建议 |
|---|---|---|
| 4e977… | 题面允许自选溶剂/温度，但 gold 为特定溶液 ΔG。SI PDF p71 指定 IEFPCM methanol ε=32.63；真实 Opt/Freq 热修正 0.416764/0.417259 Eh 可在日志找到，与单点组成 ΔG=2.641225 kcal/mol，满足 2.3171919±1 | 公开甲醇、温度、能差方向、热校正/单点组合定义；不能用任意 solvent 去比较同一个固定 gold |
| db6c… | 只说 solution-phase，未给甲腈等主比较条件。SI PDF p65 及真实输入是 gas B3LYP-D3BJ Opt/Freq + M06/SMD(acetonitrile) SP，298.15 K；ΔG=2.292700，角度 121.3175/129.7119° | 公开甲腈、温度/标准态和 anti−syn 的比较定义；采用何种主计量协议与自由探索的关系一并说明 |

两篇都已存在有效两状态计算，不因公开 starter 与作者初态不同要求重算。

### M9. paper_2c439196c2f349c9 — group_3，轨道 gap 不能验证热 NLO 机制

任务核心是 INP 的 HOMO/LUMO/gap；已有 gap≈3.42193 eV 的实算。evaluator 的 limitation/result 却要求承认 “CW NLO response is mainly thermal”。现有孤立分子轨道计算不能证明实验连续光 NLO 主要来自热效应；该句是论文实验解释，不是这条计算得出的结论。有限分子 gap 也不能单独证明宏观绝缘性或定量极化率。

建议保留轨道/gap 科学目标与数值标准；把必评结论限定为所算孤立分子电子结构及不能外推的边界，不要求 agent 从未提供的实验中推出 thermal 主导。原文实验解释可留在 evaluator 私有背景，不能冒充已计算结论。**这涉及语义评分范围，待负责人确认后实施；不建议为保留越界一句话而追加整个 NLO 计算任务。**

### M10. paper_2f302589e5e9e420 — group_3，公开百分比字段与评分字段不一致

两模式 task/schema 要 `percent_change_ePI2_vs_EPI1`，scoring 读取未声明的 `percent_reduction_EPI2_vs_EPI1` 并比正 14.3%。真偶极 2.223986032/1.899046595 D 对应 signed change **−14.610678%**、reduction **+14.610678%**。历史 result 同时带两字段，所以旧检查没有暴露合规 agent 提交会缺字段的问题。

建议保留已有字段并公开补全 reduction 及公式，或一致改绑 signed 字段和相应符号；两种实现二选一同步 task/schema/evaluator。要求百分比与原始偶极一致，不能只做绝对值。无需补算。

### M11. paper_6943bfe5eeaa42b8 — group_3，仅 PR，无效拓扑字符串

公开 [m_nh2_identity.json](../final_verified_paper_reproduction/paper_6943bfe5eeaa42b8/agent_input/data/inputs/m_nh2_identity.json) 的 `CCCCN1C(=O)c2cccc3c(N)cccc3c2C1=O` 无法 kekulize。现有 mNH2 优化几何恢复为 C16H16N2O2/36 原子，连接字符串为 `CCCCN1C(=O)c2ccc3c(N)cccc3c2C1=O`，与 naphthalimide 环大小相符；当前字符串多了一个芳香碳。后者应再按论文位置编号完成明确映射后作为合法拓扑输入，不公开优化坐标。

真实作者 LC-BLYP 路线与 NTO 给出 D≈2.194884 Å，支持当前 2.25±0.35；只需修输入身份描述并把对应关系记录清楚。任务已限定 mNH2，不要求新增 pNH2 来证明两者排序。

### M12. paper_36722b90a0c12825 — group_4，色散列/近简并解释混淆

SI `supplementary_002.pdf` PDF p16/Table S6 的无 GD3BJ PCM 与 PCM+GD3BJ 是不同列：open−close 分别约 **−0.0922 eV** 和 **+0.9970 eV**。正文 PDF p5 的近简并讨论不能直接套到第二列。历史 D3BJ/PCM acetone 算得 **+0.998630664 eV**，约 96.35 kJ/mol；不能把它描述为热意义上的 near-degeneracy。

当前任务可自行选方法/溶剂，固定 gold 却只有 +0.997±0.25。建议明确 primary 比较是含色散、acetone 的那一列，温度按实际主链说明；不含色散列作为不同协议，不能混为一次结果。evaluator 已允许 supports or does not support near-degeneracy，无需强行改成支持；应修 reference/历史结论的过强表述。无需重做现有 D3BJ 链，也不能声称未运行的无色散敏感性已完成。

### M13. paper_eda19e7c8edd4b39 — group_5，空位形成能缺化学势约定

公开 task/system_definition 允许自行声明 elemental reservoirs；固定 gold 是 Ni 0.98、Al 1.20 eV（±0.25）。[实际验证](../../docs/verification/group_5/paper_eda19e7c8edd4b39/report/results.json)采用 Ni-rich β-NiAl equilibrium：`μNi=E(fcc Ni)/atom`，`μAl=E(β-NiAl)/formula−μNi`，得 1.098323/1.188445 eV。若同一缺陷能量改用独立 fcc-Al，Al 空位为 **2.561214 eV**。这不是计算失败，是物理参考不同。

建议公开主比较的形成能公式 `Ef(VX)=Edef−Ebulk+μX` 和一致的 Ni-rich equilibrium 定义，不公开待求 Ef。正文并未唯一披露该完整 reservoir 约定，必须标明它是为使 benchmark 量可比而明确的实现边界，不能写成论文原话。若负责人坚持不作这一边界选择，固定绝对数值评分需要另议。已有能量和超胞敏感性可复用，不需重算。

## 5. 应更新档案、不能据此要求整篇补算的四篇

| 论文/模式 | 确认问题 | 现有可用证据与建议 |
|---|---|---|
| `paper_a6e8c57709329bdb`，AR/PR，g1 | 当前输入已经是正文的 2-OH/4-OMe HL，但 reference 仍列旧位置异构体结果：gap 3.871908 eV 和旧 `corrected_workspace` 链 | 9 月 16 日正确对象已有真实新计算：[source_hl_raw_evidence](../../docs/verification/group_1/paper_a6e8c57709329bdb/provenance/source_hl_raw_evidence_20260916.json)。52 原子、150 实频，HOMO −5.216350、LUMO −1.562400、gap 3.653951 eV，在原 ±0.75 内；native Mulliken 的芳香/亚胺占比 HOMO 67.36%、LUMO 77.82%，LUMO bridge 1.34%，只能称弱参与。重写 reference 成正确对象链，排除旧异构体，不把微弱 bridge 密度宣传成主导局域化 |
| `paper_fda8b9b53f8276db`，AR/PR，g2 | 原 reference 混入原文六对数据与当前七对 benchmark；R² 旧算法是恒等预测而非 OLS；旧“复现 cis”说法过强 | 当前 task **明确七个 CIF-label pairs，未要求 cis**。真实 trans 极小值 87 实频，七对 RMSE=0.002890458 Å，OLS R²=0.998715205；当前核心目标可支持。原文六对的 RMSE=0.004062019、R²=0.99804265，SI 第七个理论值为空，不应补造。更新 reference 区分“当前七对测量定义”和“原文六对”，明确只验证 trans 局部极小值。不能因为另一 agent 追查作者 cis，就自动要求当前任务新增 cis 计算 |
| `paper_1b285cf9f763f2cf`，AR/PR，g5 | reference 仍链接 evaluation 根下 `boundary_repair_evidence.json`，实际已移到 task_provenance | 56 原子固定模型、电子补偿与全壳层几何有对应真实数据；修链接/归档摘要即可。发布时若删除 task_provenance，应先保留 reference 所需有效计算内容，不把修复过程记录误当唯一科学档案 |
| `paper_534ae3b6e2fb695f`，AR/PR，g6 | 同上，两个 reference 的根路径已失效 | 全局 TCE 标尺 N、局域描述符、平面/二面角是不同量，已批准分开；N=4.0898/3.4532/3.3447 有据。修档案位置及关联读取位置，不重新改成任选局域指标与全局 eV gold 比较 |

`a6e8…`、`fda8…` 的问题属于**科学档案内容过期**，严重性高于普通链接；不能只改文件名就写“reference 已准确”。它们已有可替代的有效结果，所以不列入建议 hold。

## 6. 全部 70 篇逐篇判断

AR/PR 共用原始成功链不等于两份题面相同；以下逐篇判断已考虑两模式的现有要求。S 表示未发现新的**核心科学阻塞**，仍须保留表内限制并处理第 7 节适用的接口问题。H/M/R 的具体问题见前文。每个 paper_id 链接至对应 PR reference，AR 同 ID 的判断同步适用，除三篇 PR-only 外。

### group_1：20 篇，40 包

| paper_id | 模式 | 当前有效验证支持及限制 | 判定 |
|---|---|---|---|
| [paper_2f0a4f80a37fbccd](../final_verified_paper_reproduction/paper_2f0a4f80a37fbccd/evaluation/verified_computation_reference.md) | AR/PR | Ir nitrate 有 219 实频、bite angle≈61.599°；实验 XRD/IR 边界可见。只支持当前结构/诊断 IR 范围，不把旧 partial 标签当整篇失败 | S |
| [paper_3a22e838133b906d](../final_verified_paper_reproduction/paper_3a22e838133b906d/evaluation/verified_computation_reference.md) | AR/PR | 两对象 87/75 实频；P–O 差 +0.04126/+0.06412/−0.10939 Å、B–O 差 −0.11646 Å，晶体 O 对应公开 | S |
| [paper_5ea491c741fbd8d4](../final_verified_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/verified_computation_reference.md) | AR/PR | 五候选、三个极小值，代表 gap 3.680068 eV；PR 主基组已消歧；有限构象覆盖，不保证全局最低 | S |
| [paper_60f4c45810428116](../final_verified_paper_reproduction/paper_60f4c45810428116/evaluation/verified_computation_reference.md) | AR/PR | 两反应电位链存在；Fc SMILES 无效、主标尺未公开 | M1 |
| [paper_6e09640463562644](../final_verified_paper_reproduction/paper_6e09640463562644/evaluation/verified_computation_reference.md) | AR/PR | 九个 MP2 端点与 ZPE 存在，A 系列偏好须按电子能/ZPE 区分；旧 4/5 排序误述已澄清，不要求额外全局搜索 | S |
| [paper_6f9a36fff6964313](../final_verified_paper_reproduction/paper_6f9a36fff6964313/evaluation/verified_computation_reference.md) | AR/PR | 完整离子对及 TFAP、45/90/105 实频；四电荷 0.203728/0.198533/0.040059/0.058695 e；一构象不代表全部构象稳健 | S |
| [paper_746e066c163800d8](../final_verified_paper_reproduction/paper_746e066c163800d8/evaluation/verified_computation_reference.md) | AR/PR | 210 实频；五角 mean(abs) 27.096769°，收紧检查 27.096738°；作者终态不在公开输入 | S |
| [paper_80cc1ffb2cf73fc5](../final_verified_paper_reproduction/paper_80cc1ffb2cf73fc5/evaluation/verified_computation_reference.md) | AR/PR | 两态各 75 实频及独立成功 FC；825 点实验 trace。支持 Z1 相对突出峰与模式解释，不是绝对 ADE/全谱逐点吻合 | S |
| [paper_86a0b654270a8ce7](../final_verified_paper_reproduction/paper_86a0b654270a8ce7/evaluation/verified_computation_reference.md) | AR/PR | 两给定对象的 ΔG≈2.901177 kJ/mol、339 K 比例≈2.799095；实验边界文件存在，不宣称构象发现 | S |
| [paper_94e7481ded3b6a75](../final_verified_paper_reproduction/paper_94e7481ded3b6a75/evaluation/verified_computation_reference.md) | AR/PR | 六项 PBNA 量有实算，但任意方法与固定绝对 E/G 不可直接兼容 | M2 |
| [paper_9a58a1fa6ed7d780](../final_verified_paper_reproduction/paper_9a58a1fa6ed7d780/evaluation/verified_computation_reference.md) | AR/PR | TD 六态/四态空穴电子分析存在；H 含义写错 | M3 |
| [paper_9aa6d5655edfeb52](../final_verified_paper_reproduction/paper_9aa6d5655edfeb52/evaluation/verified_computation_reference.md) | AR/PR | 138 实频，gap≈4.35110、S1≈3.9220 eV，支持所选电子结构目标 | S |
| [paper_9f4c259696ad2f87](../final_verified_paper_reproduction/paper_9f4c259696ad2f87/evaluation/verified_computation_reference.md) | AR/PR | 给定结构 TD64，S1=2.2955 eV、H→L≈97.91%；不是几何搜索任务，不补设 Hessian 要求 | S |
| [paper_a0f6b899582cb9f7](../final_verified_paper_reproduction/paper_a0f6b899582cb9f7/evaluation/verified_computation_reference.md) | AR/PR | M3 三极小值各 66 实频；raw Qzz≈−111.07681 DÅ，原点/轴/非 traceless 约定明确 | S |
| [paper_a6e8c57709329bdb](../final_verified_paper_reproduction/paper_a6e8c57709329bdb/evaluation/verified_computation_reference.md) | AR/PR | 正确位置 HL 新链支持核心量；reference 仍列旧位置异构体 | R |
| [paper_d2d08c91f34da1cb](../final_verified_paper_reproduction/paper_d2d08c91f34da1cb/evaluation/verified_computation_reference.md) | AR/PR | 两态 195 实频、24 项实验配对；MAE≈1.262626 cm⁻¹。给定对象/模式交换/例外已说明 | S |
| [paper_d3b4575397179146](../final_verified_paper_reproduction/paper_d3b4575397179146/evaluation/verified_computation_reference.md) | AR/PR | 四分子 Opt/Freq、TD-PBE1PBE 18 态及空间证据；OMe 的 H−3→L 特征不能硬写成全系列同一轨道编号 | S |
| [paper_e31cc7bc7b21b610](../final_verified_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/verified_computation_reference.md) | AR/PR | 两异构体 168 实频，Eβ−Eα=1.438478 kcal/mol；按给定对象性质比较，不宣称全异构体搜索 | S |
| [paper_ef26687d63a37e29](../final_verified_paper_reproduction/paper_ef26687d63a37e29/evaluation/verified_computation_reference.md) | AR/PR | 完整 free/PO/PA 的频率、ADCH/ESP 与接触存在；固定同 O 后取 α/βH 的定义已修；旧进程异常与已完成产物分开 | S |
| [paper_f9d09d28c7d9adaa](../final_verified_paper_reproduction/paper_f9d09d28c7d9adaa/evaluation/verified_computation_reference.md) | AR/PR | 扭转/FMO 支持当前目标；此前批准的 CF3 short-axis migration optional 范围保留，不重新加为必算 | S |

### group_2：14 篇，27 包

| paper_id | 模式 | 当前有效验证支持及限制 | 判定 |
|---|---|---|---|
| [paper_0a62b797f51de2c0](../final_verified_paper_reproduction/paper_0a62b797f51de2c0/evaluation/verified_computation_reference.md) | AR/PR | 三单体偶极/ESP 有据；极性文字自相矛盾，非单调已有解释通道 | M6 |
| [paper_0de37d01e35c27df](../final_verified_paper_reproduction/paper_0de37d01e35c27df/evaluation/verified_computation_reference.md) | AR/PR | 正确 C10H14S2 两态支持收缩；gold 与 signed delta 反号 | M5 |
| [paper_221aafe4bd916a11](../final_verified_paper_reproduction/paper_221aafe4bd916a11/evaluation/verified_computation_reference.md) | AR/PR | 79 原子对象+CO2、TS 唯一虚频、IRC 与产物极小值；barrier≈19.87197 对 21.8±3，支持当前局部步骤 | S |
| [paper_2f2aa11ea61a32bb](../final_verified_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/verified_computation_reference.md) | AR/PR | 四体系 Opt/Freq/TD 成功；缺实验比较数据 | M4 |
| [paper_46f6118697c6397c](../final_verified_paper_reproduction/paper_46f6118697c6397c/evaluation/verified_computation_reference.md) | AR/PR | 完整四 triflate 模型、三几何分支、TD50；3.81–3.84 eV，f≈0.43–0.47；采用 SI 自洽光谱而非正文冲突能量 | S |
| [paper_4e9774f4128551d3](../final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/verified_computation_reference.md) | AR/PR | 两状态与 ΔG=2.641225 有据；甲醇/温度/热力学计量边界未明确 | M7 |
| [paper_641a923cbe5bbc48](../final_verified_paper_reproduction/paper_641a923cbe5bbc48/evaluation/verified_computation_reference.md) | AR/PR | 45 原子 +1，三个 129 实频极小值；ZE<ZZ<EZ，相对 0/1.063629/10.215854 kcal/mol，有限集合排序 | S |
| [paper_72f60526b64ce1b6](../final_verified_paper_reproduction/paper_72f60526b64ce1b6/evaluation/verified_computation_reference.md) | AR/PR | 约束 terminal-S 几何/单点 dipole=2.6765 D；当前允许 fixed-geometry 属性范围，不能宣传成无约束极小值 | S |
| [paper_a3892396b1843698](../final_verified_paper_reproduction/paper_a3892396b1843698/evaluation/verified_computation_reference.md) | AR/PR | 两 TS 各一虚频、双向 IRC 与四端点；势垒 23.505892/26.227908 kcal/mol，相关 qRRHO 定义已明确 | S |
| [paper_b276b18215cba283](../final_verified_paper_reproduction/paper_b276b18215cba283/evaluation/verified_computation_reference.md) | AR/PR | 57 原子给定结构 TD10 两支，约 −0.08 的位移有据；不另加新 Hessian/几何发现要求 | S |
| [paper_c23cfabbd34b087f](../final_verified_paper_reproduction/paper_c23cfabbd34b087f/evaluation/verified_computation_reference.md) | AR/PR | 102 原子、300 实频，735.93 nm/f=1.2539；模型边界已公开，不外推聚集体/实验长链 | S |
| [paper_d7967e22bb965daa](../final_verified_paper_reproduction/paper_d7967e22bb965daa/evaluation/verified_computation_reference.md) | PR | 四 TS 与四局部 barrier 10.2580/12.4255/13.1910/12.0225 kcal/mol，有限 IRC 支持通道；不是完整催化循环认证 | S |
| [paper_d8e5490cd9942f4f](../final_verified_paper_reproduction/paper_d8e5490cd9942f4f/evaluation/verified_computation_reference.md) | AR/PR | 两 La 给定端点各 237 实频，anti−syn=4.393821 kcal/mol，水/温度/电荷/标准态明确 | S |
| [paper_fda8b9b53f8276db](../final_verified_paper_reproduction/paper_fda8b9b53f8276db/evaluation/verified_computation_reference.md) | AR/PR | 当前七对 bond/CIF 范围可由 trans 极小值支持；须纠正 reference 的六/七对、OLS 与 cis 声称 | R |

### group_3：14 篇，27 包

| paper_id | 模式 | 当前有效验证支持及限制 | 判定 |
|---|---|---|---|
| [paper_0dcba54d6a1436bd](../final_verified_paper_reproduction/paper_0dcba54d6a1436bd/evaluation/verified_computation_reference.md) | AR/PR | 两 S0 极小值、S1–S5/NTO，S1=2.9477/2.5851 eV；支持当前态比较 | S |
| [paper_2c439196c2f349c9](../final_verified_paper_reproduction/paper_2c439196c2f349c9/evaluation/verified_computation_reference.md) | AR/PR | gap≈3.42193 eV 可算；热 NLO 主导不是这条计算能证明的结论 | M9 |
| [paper_2f302589e5e9e420](../final_verified_paper_reproduction/paper_2f302589e5e9e420/evaluation/verified_computation_reference.md) | AR/PR | 两偶极有据；signed change 与 reduction 字段/符号未对齐 | M10 |
| [paper_3316e45a74258fb7](../final_verified_paper_reproduction/paper_3316e45a74258fb7/evaluation/verified_computation_reference.md) | AR/PR | S1=2.1404/T1=1.8322/gap=0.3082 eV，NTO D≈4.9043 Å；支持能量/态特征，不证明速率 | S |
| [paper_4fa592965be9841e](../final_verified_paper_reproduction/paper_4fa592965be9841e/evaluation/verified_computation_reference.md) | AR/PR | 主链是另一连接异构体；另有实验输入、IR/UV 归属问题 | H1 |
| [paper_51a03695e1ccb105](../final_verified_paper_reproduction/paper_51a03695e1ccb105/evaluation/verified_computation_reference.md) | AR/PR | 端点及两自由能有据；有限 IRC 未证明规定的分离反应物到 azo+OH⁻ 盆地连接 | H2 |
| [paper_6943bfe5eeaa42b8](../final_verified_paper_reproduction/paper_6943bfe5eeaa42b8/evaluation/verified_computation_reference.md) | PR | mNH2 的真实 NTO 距离支持 gold；公开 SMILES 多一个芳香碳并解析失败 | M11 |
| [paper_94b0a8ae694590ea](../final_verified_paper_reproduction/paper_94b0a8ae694590ea/evaluation/verified_computation_reference.md) | AR/PR | 三个极小值和 frontier 量，C8Ph 的对应排序有据；限定孤立电子结构 | S |
| [paper_988bc12ae3768679](../final_verified_paper_reproduction/paper_988bc12ae3768679/evaluation/verified_computation_reference.md) | AR/PR | +2 acid/−2 base 给定对象 S1–S4；acid bright S3、base S1，身份/选态须保留 | S |
| [paper_9d091f4337662e78](../final_verified_paper_reproduction/paper_9d091f4337662e78/evaluation/verified_computation_reference.md) | AR/PR | 三个不同极小值和单点，Grel 0/0.602653/0.682592，population≈59.609/21.556/18.835%；新 starter 未盲跑不撤销该验证 | S |
| [paper_b5c446c7067dd511](../final_verified_paper_reproduction/paper_b5c446c7067dd511/evaluation/verified_computation_reference.md) | AR/PR | gaps/高态能量有据；缺必评附近 Tn 的混合态空间证据，先做已有波函数分析 | H3 |
| [paper_d91572979a89303a](../final_verified_paper_reproduction/paper_d91572979a89303a/evaluation/verified_computation_reference.md) | AR/PR | 四局部能垒有据；完整机理缺 TS2A/连接闭合、半熵主定义未公开 | H4 |
| [paper_db6c4e0558113873](../final_verified_paper_reproduction/paper_db6c4e0558113873/evaluation/verified_computation_reference.md) | AR/PR | 两 Cu 态能差/角度有据；甲腈等主比较条件未公开 | M8 |
| [paper_e2d9397dff2a3f0f](../final_verified_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/verified_computation_reference.md) | AR/PR | 参考态零虚频、TS 一虚频 −82.8205，barrier≈6.47915 kcal/mol；当前局部势垒不强制 IRC，不以单一能垒证明全循环 rate control | S |

### group_4：12 篇，24 包

| paper_id | 模式 | 当前有效验证支持及限制 | 判定 |
|---|---|---|---|
| [paper_0dc85595cab7bc0a](../final_verified_paper_reproduction/paper_0dc85595cab7bc0a/evaluation/verified_computation_reference.md) | AR/PR | 九端点极小值/单点；两差≈9.6601/11.0037、LUMO 位点比≈3.346/2.689；有限热力学对象支持，不因新 starter 缺盲跑判未验证 | S |
| [paper_3235db287859287e](../final_verified_paper_reproduction/paper_3235db287859287e/evaluation/verified_computation_reference.md) | AR/PR | Z/E 已按真实结构校正标签，两者 105 实频；E−Z≈1.63278 kcal/mol | S |
| [paper_36722b90a0c12825](../final_verified_paper_reproduction/paper_36722b90a0c12825/evaluation/verified_computation_reference.md) | AR/PR | D3BJ/acetone 差≈0.99863 eV 有据；方法列与近简并表述需修订 | M12 |
| [paper_3c058fa17fa7c54e](../final_verified_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/verified_computation_reference.md) | AR/PR | 两最低点、S/T 能量支持所选两个不等式；来源 S/T 标签冲突不能覆盖真实自旋标签 | S |
| [paper_3e4cad1d1d650d0c](../final_verified_paper_reproduction/paper_3e4cad1d1d650d0c/evaluation/verified_computation_reference.md) | AR/PR | 两阴离子极小值、frontier≈−4.92336/−5.07166 eV；系数平方图示仅作定性，不是严格 population | S |
| [paper_430b9cbe83c2c203](../final_verified_paper_reproduction/paper_430b9cbe83c2c203/evaluation/verified_computation_reference.md) | AR/PR | cis/trans 各 69 实频，ΔG≈0.756776 kcal/mol；77Se 只按当前半定量、允许有据偏差的范围，不宣称精确谱重现 | S |
| [paper_46a9ca0dab36dd9e](../final_verified_paper_reproduction/paper_46a9ca0dab36dd9e/evaluation/verified_computation_reference.md) | AR/PR | 最高 f 为 state20，IFCT LMCT/MLCT≈63.541%/3.820%；AR 选态矛盾已修，不能再用旧 state22 替代主态 | S |
| [paper_5d94285cfbd51973](../final_verified_paper_reproduction/paper_5d94285cfbd51973/evaluation/verified_computation_reference.md) | AR/PR | AZ9 多轮有限构象/九盆地及敏感性；gap≈4.421578 eV、dipole=6.0404 D；非全局最优证明 | S |
| [paper_b1467cd61ca8022d](../final_verified_paper_reproduction/paper_b1467cd61ca8022d/evaluation/verified_computation_reference.md) | AR/PR | 五 Li 取向/碎片、各 42 实频，Eb≈−2.190457 eV，Li–O/F≈1.853/1.845 Å；支持有限候选结合比较 | S |
| [paper_b33676a2051f5e91](../final_verified_paper_reproduction/paper_b33676a2051f5e91/evaluation/verified_computation_reference.md) | AR/PR | Int-3 裂解 barrier≈8.897457 kcal/mol、TS −474.9764；产物侧有限 IRC 已有断键/自旋证据，当前不声称单独产物极小值 | S |
| [paper_c625cba3ce868eb1](../final_verified_paper_reproduction/paper_c625cba3ce868eb1/evaluation/verified_computation_reference.md) | AR/PR | 给定构象的 MK 水相电荷，C=C Δq≈−0.484368/−0.054945；单点属性范围成立，不追加 TS 任务 | S |
| [paper_fcc3c7f2c46a0fbe](../final_verified_paper_reproduction/paper_fcc3c7f2c46a0fbe/evaluation/verified_computation_reference.md) | AR/PR | 正确 4b 图、全实频、29 个 XRD 比较量；bond MAE≈0.01462 Å、angle≈0.6567°/torsion≈1.5356° | S |

### group_5：4 篇，8 包

| paper_id | 模式 | 当前有效验证支持及限制 | 判定 |
|---|---|---|---|
| [paper_08c040bf4e456891](../final_verified_paper_reproduction/paper_08c040bf4e456891/evaluation/verified_computation_reference.md) | AR/PR | 已有 CCSD(T) 量 11.8187/12.12848/13.37486 及 Cl scan/F NEB 等有效证据；保留批准的有限路径范围，不外推所有分支 | S |
| [paper_1b285cf9f763f2cf](../final_verified_paper_reproduction/paper_1b285cf9f763f2cf/evaluation/verified_computation_reference.md) | AR/PR | 已批准 56 原子中性电子补偿模型、全壳层观测支持；reference 旧文件路径需修 | R |
| [paper_5286f393dfa5a49a](../final_verified_paper_reproduction/paper_5286f393dfa5a49a/evaluation/verified_computation_reference.md) | AR/PR | 固定 wB97M-V 主协议已批准；RRRR−SSSS≈−6.569004 的比较有据，限定该协议 | S |
| [paper_eda19e7c8edd4b39](../final_verified_paper_reproduction/paper_eda19e7c8edd4b39/evaluation/verified_computation_reference.md) | AR/PR | 缺陷及超胞敏感性有据；Ni-rich reservoir 必须公开或重新决定评分口径 | M13 |

### group_6：6 篇，11 包

| paper_id | 模式 | 当前有效验证支持及限制 | 判定 |
|---|---|---|---|
| [paper_44f9727c4e9a4b6f](../final_verified_paper_reproduction/paper_44f9727c4e9a4b6f/evaluation/verified_computation_reference.md) | PR | 两自旋 ORCA 链、Fe–Fe≈3.08643 Å、δ≈0.517809/0.523604 mm/s；261 打印模式含 6 零+255 正，不把零模式算作正振动 | S |
| [paper_534ae3b6e2fb695f](../final_verified_paper_reproduction/paper_534ae3b6e2fb695f/evaluation/verified_computation_reference.md) | AR/PR | 全局 N、局域指标、几何已区分且有实算；reference 旧路径需修 | R |
| [paper_63a9254b8e68a23c](../final_verified_paper_reproduction/paper_63a9254b8e68a23c/evaluation/verified_computation_reference.md) | AR/PR | 连续介质求解 r≈2.5239449734 nm，两数值解差约 6.3e−8 nm、极小性有据；不是分子动力学验证 | S |
| [paper_84efbea3ab8e6e20](../final_verified_paper_reproduction/paper_84efbea3ab8e6e20/evaluation/verified_computation_reference.md) | AR/PR | 三分子 SOC/态分析存在；CZ2B 的作者特定 HLCT 解释未重现，但现行评分已批准接受有据替代解释，不能又以此擅自暂缓 | S |
| [paper_98b6f8a0352f72c2](../final_verified_paper_reproduction/paper_98b6f8a0352f72c2/evaluation/verified_computation_reference.md) | AR/PR | 正确 C24H19N3，两 S0/TD40；3.664926 eV、f=0.638447、Einstein 关系寿命约 2.688686 ns；不是实验实际发光寿命证明 | S |
| [paper_9ec8c4761c4f171b](../final_verified_paper_reproduction/paper_9ec8c4761c4f171b/evaluation/verified_computation_reference.md) | AR/PR | 35 原子 gas/CHCl3 gap≈3.105/3.044 eV；明确不等于 2.42 eV optical gap，支持当前区分而非数值冒配 | S |

## 7. 不能遗漏、但不属于化学补算的问题

### 7.1 评分字段数组简写仍与读取器不兼容

本次直接检查所有 scoring bindings：共 **1415 个字段引用，116 处 `[]` 简写解析失败，涉及 15 篇、28 包**。之前只数绑定 `report/results.json` 的子集为 108 处，两数字口径不同，不是新增 8 篇论文问题。

`evaluation/scoring/evidence_reading.py` 的 `read_registered_evidence` 仍直接调用 JSONPath parser；`$.molecules[].id` 抛解析异常，`$.molecules[*].id` 正常。审计工具能自行理解简写，不代表实际评分读取器也能理解。不能因此说这些化学任务不可行，也不能说 28 包必然全评分失败；当 judge 原样使用该 selector 时确会失败。

- AR/PR 两模式均受影响：`0a62…`、`1b285…`、`2f2aa…`、`3c058…`、`430b9…`、`46a9…`、`86a0…`、`94b0…`、`b5c…`、`d3b…`、`d8e549…`、`db6c…`、`f9…`。
- 仅 AR：`b336…`；仅 PR：`d796…`。

建议在统一的读取入口兼容既有简写，或把规则同步为标准 `[*]`，保持“全部对象/指定状态/任一候选”的原语义，做离线字段读取验证。无需计算。此问题可与 H/M/R 重叠，不重复计入论文总数。

### 7.2 reference 的可靠性不是“文件存在”

本轮需要明确修复的档案内容包括 H1–H4 的过强验证声明、a6e 的错误异构体链、fda 的指标口径、367 的近简并表述、94e 的轨道诊断来源，以及 1b285/534 的真实断链。修复时只记录真正有效的步骤：输入身份、方法/环境、上一步产物、原始输出、提取量及能支持的结论；失败/重试无需写进成功主链，但不能将其输出嫁接到另一成功端点。

`1b285/534` 共 4 个 reference 断链不是数据遗失；真实数据仍在 `evaluation/task_provenance/`。此前的测试旧路径问题也应一并改，但本轮没有改代码或重复执行旧失败测试。SMILES 被 Markdown 误识别为链接属于排版问题，不计为缺失计算文件。

### 7.3 输入泄露与发布隔离

本次没有确认新增“当前 agent_input 又放回待求作者 TS/最终优化几何”的实例。4fa 是对象错误，60f/694 是拓扑输入错误，不能统一叫数据泄露。已批准的给定结构属性任务继续保留其对象；只证明这些量可以在指定结构/方法下算出，不宣传成独立几何发现。

目录层面，作者终态、reference 与修复记录放在 evaluation 私有侧是合理的；**真正评测必须只让 agent 读取公开包**。本次没有实际部署沙箱，因此没有依据宣称已发生越权泄露，也不能保证共享路径/网络完全隔离。此前运行入口还存在默认扫描 canonical 而非 final 的问题，发布时应明确选定的 final 清单，排除 hold 和源任务。这里只记录发布条件，未执行发布或移动。

## 8. 已有四篇 hold 的最新判断

| paper_id | group/模式 | 本次判断 | 依据与后续 |
|---|---|---|---|
| `paper_a3968806251093cd` | g2，AR/PR | 继续 hold | 旧 7a 计算是错误位置异构体；当前正确图不能由旧几何改名验证。此前逐结构证据见[7a 复审](POST_REPAIR_REAUDIT_20260916.md#3-paper_a3968806251093cd为什么确认暂缓)。本次未找到新的正确对象完成链；先向验证方查既有正确输出，再定缺口 |
| `paper_6492e1e5d38d23ae` | g5，AR/PR | 继续 hold | 新[模型/功函数复核](../../runs/hold_verification/group_5/paper_6492e1e5d38d23ae/20260915_handoff/report/supplementary_verification.md)说明表面终止/作者晶格仍不唯一；主 anatase W=6.369999788 eV，略低于原 6.371 下界，不能四舍五入判通过；另一 termination 的 7.173123 不能按答案择优替换。更主要是模型与差值幅度未闭合，不是 0.001 eV 一项就否定整篇 |
| `paper_8b7bf002cc6a4ba9` | g5，AR/PR | 继续 hold，更新理由 | 新[有效链核查](../../runs/hold_verification/group_5/paper_8b7bf002cc6a4ba9/20260915_handoff/report/supplementary_verification.md)已记录 8 个真实收敛且保留两性离子身份的 50 水簇，不再说全部只有失败 xTB。20/24 单点完成；两 AL 种子 open−compact≈−5.392/−9.994 kcal/mol，不支持 folded AL；AB 链未齐，最终 SP/水网络/偶极约定不唯一。先确定边界，不能继续挑种子追答案 |
| `paper_b815e2622b0d6085` | g6，AR/PR | 可进入恢复前维护，暂不移动 | 新三晶体 3×3×1 HSE06 投影已真实完成。本次直接读取新 OUTCAR/EIGENVAL/PROCAR，独立按 Pb-p-leading 组分选出框架候选，没有用预设 band 序号/目标能量选择。原第二网格缺口已得到实证支持 |

其中 6492/8b7 的表述基于新逐原始文件复核报告及本轮任务对照，本轮没有重新读取其所有大型 VASP/ORCA 历史输出。b815 则进行了本轮原始量的独立重提取：

| 晶体，新 3×3×1 网格 | fundamental edge / eV | fundamental same-k / eV | framework edge / eV | framework same-k / eV |
|---|---:|---:|---:|---:|
| Cl | 3.080154 | 3.102962 | 4.649296 | 4.674125 |
| Br | 3.101139 | 3.119048 | 4.651595 | 4.669504 |
| I | 3.122884 | 3.126038 | 4.463777 | 4.469149 |

证据：[补充报告与原始路径](../../runs/hold_verification/group_6/paper_b815e2622b0d6085/20260915_kmesh_identity/report/supplementary_verification.md)，原始文件在其上层 `production/{Cl,Br,I}/`。三者有 SCF 达 EDIFF、正常结束，HSE06/固定几何/no-SOC 分支；新旧四类 gap 的最大变化约 0.019514 eV。最低八条未占据候选的边缘均为 organic:C:p-leading；框架候选由投影独立识别后才得到序号 133。I 边缘 Pb-p≈0.3448、领先次组≈0.1241，虽然总有机权重大于一半，仍符合已批准的 Pb-p-leading 定义；不能另加 >50% 无机门槛。

恢复前应把新步骤、态身份/全部较低候选、两网格差值写入 hold 包的 reference，保留有限采样、混合态、未证明 optical allowedness/未算 SOC 的边界；再核对包内引用。该目标目前没有显示必须追加本范围量化计算的理由。恢复仍等待负责人反馈，**没有自动移回 final**。

## 9. 等待反馈后的最小处理顺序

1. **先决定 H1–H4 的处置。**建议两模式一并暂缓。维护报告应分别写清“错误对象”“规定连接未证明”“附近 Tn 特征缺证据”“完整网络缺 TS2A/连接”，不能统一写成“需要重算”。保留已有有效局部量，给验证方精确缺口。
2. **处理 M 的输入/计量/评分一致性。**拓扑语法、H 定义、差值符号、公开实验观测、字段命名可做确定性修订。60f 的 Fc 标尺、94e 的绝对 E/G 协议、367 的方法列、eda 的化学势以及 2c439 的评分范围必须作为明确边界选择，不由 agent 偷改科学目标/容差。
3. **更新 reference。**先替换 a6e 的错误异构体链、修 fda 的计算量口径，再修档案路径；对 H 的未闭合范围诚实标注。reference 不承担新增评估职责，不建立额外哈希评分制度。
4. **处理统一评分读取接口。**修数组 selector 兼容性，用现成有效结果和符号/状态错误反例做离线检查，不跑化学任务。
5. **维护 b815 的新成功链。**在现有 hold 包内补档案和一致性检查，经负责人决定后恢复。
6. **发布选择应依据最终修订后的清单。**即使某篇记为 S，也只承诺表中所列目标有作者路线计算支持；不承诺任意模型都能复现、所有过程分都已验证或 agent 一定成功。发布前按实际运行入口检查公开/private 分区，不能把目录名 final 当科学验收结论。

本轮实际新增文件只有本报告。任务、评分标准、验证档案与目录位置均未据此改变；等待负责人反馈后再决定修复、移入 hold 或恢复任务。
