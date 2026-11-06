# paper_1bcf80caf9e64d55｜膦催化炔–酯拼接

**当前状态确认（2026-10-23）：用户接受本篇当前科学问题的验证结果，数值差异保留专家审查。** 要求相关结果已实际计算且结论一致；本确认不等于所有数值窗口通过、全文复现或自动发布。下方差值、方法差异和原始证据继续保留。

> **2026-10-21 AR科学分V2迁移。** 仅自主科研现行评分已迁移，100分独立科学项，可运行评分；严格数值整题通过仍为false、出版release_ready=false。PR及既有专家tasks副本保持历史未迁移。以下第1节AR题面与现行任务逐段一致，第4节为现行完整规则；其他节保存真实计算与专家边界。

论文：Phosphine-Catalyzed Alkyne-Ester Stitching for the Construction of Functionalized Cyclopentenones；DOI：10.1021/acs.orglett.5c04843。

当前登记：自主科研（AR）与论文复现（PR）均为 **PROVISIONAL_PASS_QUALITATIVE（暂定定性通过）**，严格数值整题通过为 false。下述任务和评分译文用于专家审查，不替换原文件；科学验证采用获授权的作者路线，不能据此声称完成了参赛 agent 的盲测自主发现。本次仅AR评分迁移V2；发布状态保持待审。

## 1. 当前任务完整中文直译

现行AR英文题面：[task.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_1bcf80caf9e64d55/agent_input/task.md)。

### 1.1 autonomous_research

**科学问题**

三乙基膦如何促进所提供的炔–酯底物与4-氟苯酚转化为所观察到的环戊烯酮？什么控制了该反应在动力学和热力学上的可达性？

完整的反应物图和观察到的产物图在 `data/inputs/reaction_system.json` 中。反应采用氟苯，温度110 °C、20 mol% PEt3，时间12 h。确定一个相连且原子守恒的催化解释，包括催化剂再生及任何副产物。观察到的产物保留肉桂基侧链。未指定引发物种、中间体序列或反应机理。

选择并论证回答问题所需的假说、化学模型、电子态、方法和研究。提供的物种清单和范围定义物理问题；它们不规定机理或搜索程序。

使用 `submission_schema.json` 和 `submission_guide.md`，提交 `report/results.json` 和 `report/report.md`。

### 1.2 历史 paper_reproduction（未迁移）

**科学目标**

独立规划并执行对底物1a与4-氟苯酚（2a）的中性、单重态 PEt3 催化反应的计算研究，检验作者的定性假说：膦对炔的加成引发经两性离子介导的炔–酯拼接级联。确定通向指定环戊烯酮终点的相连催化路径，验证每个报告的极小值和过渡态，并在规定温度下，以无限分离的反应物为参照，报告单位为 kcal/mol 的相对吉布斯自由能。作者假说是待检验的建议路线，不是答案：不得预设任何候选几何、排序、能量或有序操作流程。

**公开输入和科学边界**

使用 `data/inputs/reaction_system.json`。该文件定义三乙基膦、2-肉桂基-2-[3-(4-硝基苯基)丙-2-炔-1-基]丙二酸二乙酯（1a）与4-氟苯酚（2a）的准确 SMILES、名称、中性电荷和单重态多重度，以及氟苯、383.15 K、分离反应物参考和环戊烯酮终点的原子来源／连接关系定义。推导并报告终点结构，解释原子来源；终点描述不是提供好的结果结构。可以生成构象和初始几何，但不得使用论文／SI 或抄用含有结果信息的作者几何。选择并论证计算方法；任务不指定软件或模型化学。

**所需科学验证／研究**

为推进的每个极小值和 TS 定义有限的候选记录，包括候选身份、几何来源、电荷／多重度、方法、构象覆盖、频率结果和连接证据。根据化学等价的连接关系以及明确的几何／能量标准对候选去重。只推进优化已收敛且没有虚频的极小值，以及优化已收敛且恰有一个虚频、其位移符合所提出基元步骤的 TS 候选。通过 IRC 或有明确端点结构、科学上有理据的替代方法，确立每个所声称的基元步骤连接。构建从分离反应物到终点的相连能量剖面，报告所有研究过的候选以及丢弃／失败的候选，并量化方法／构象敏感性。完成要求可复现的相连剖面，以及最终结论使用的每个状态的明确验证记录。当按已述搜索策略继续搜索不再产生新的化学不同且相连的状态时停止，或报告有界失败及其覆盖、失败尝试和缺失的闭合；不得超出研究范围声称唯一性。

**交付物**

提交符合 `submission_schema.json` 的 `report/results.json`。必须包含选定路径、独立推导的终点结构及原子来源解释、各状态能量和验证背景、搜索覆盖以及结论。包含完整相连剖面或如实的有界失败分支；对于有界失败，省略无支持的势垒数值并解释缺失的闭合，不得编造数字。数值必须使用 kcal/mol，并注明参考和温度。不得把论文数值当作独立计算结果报告。

## 2. 作者方法与实际计算过程

作者 SI97–99 的路线为 PEt3 加成形成两性离子、环化、烷氧基离去／质子转移、亲核加成及膦再生；另比较醇辅助连续1,3迁移的 B 分支。作者用气相 ωB97X-D/6-31G(d,p) 优化与频率，再用 ωB97X-D/6-311+G(d,p)、SMD 氟苯单点，配383.15 K 气相谐振热校正。实际沿用该物理路线，使用自身高层电子能与自身热校正；作者 Gaussian16 B.01 与执行 C.01 修订版不同。溶液标准态等未报告细节不能声称完全一致。

实际复用作者结构及已有成功作业，核收 A 的五个鞍点、十个实际端点，以及 B 早期两个迁移鞍点和有限连接。五个 A 鞍点虚频依次为 −234.4652、−220.9772、−104.3437、−182.4433、−163.1945 cm⁻¹。TS1/TS2/TS4 有实际两侧路径和有效端点；TS5 采用每侧一个传播 IRC 点再无约束端点优化，并结合频率、结构谱系和产物身份验证，不能把单点自身称为完整 IRC。

所有步骤显式保持 C37H45FNO7P 库存：79原子体系另加13原子氟苯酚；中段92原子；后段83原子另加9原子乙醇；最终61原子产物、22原子 PEt3 和9原子乙醇。产物保留 E-cinnamyl 侧链。独立审查重新读取62份原生日志，核对哈希、终止、频率和结构；62不是全部历史作业数。失败的 B 端点优化未改标成功；改用独立来源结构 Force/Freq/Stable/高层单点及局部桥接证据，有界支持早期连接。

## 3. 数值比较与定性一致性

以下为同一初始反应复合物1零点的复合自由能，单位 kcal/mol；差值=自算−作者。作者节点复算和实际 IRC 端点构象分列，不能互换。

|量|作者原值|自算值|差值|
|---|---:|---:|---:|
|TS1|18.9|19.054670|+0.154670|
|作者节点2|7.9|8.071567|+0.171567|
|TS2|8.2|8.383081|+0.183081|
|作者节点3|1.9|0.611765|−1.288235|
|实际TS2环化后端点，相比作者3|1.9|−4.850322|−6.750322|
|TS3|3.2|3.385129|+0.185129|
|TS4|2.8|2.973205|+0.173205|
|作者节点7|−8.3|−8.186675|+0.113325|
|TS5|−0.9|−0.746954|+0.153046|
|最终产物9及平衡物料|−24.7|−31.786838|−7.086838|
|B TS1′|8.8|9.000623|+0.200623|
|B TS1″|18.0|18.122584|+0.122584|
|B必要迁移鞍点−A分支后最高鞍点|9.8|9.739503|−0.060497|

产物相对分离反应物为 −14.710615；复合物1相对分离反应物为 +17.076223。两种零点明确分开，未拟合平移。TS3 的高层电子能加低层热校正相对自身前体为 −0.565474；同一实际步骤的低层电子势垒为 +0.221454。前者是浅驻点对在复合方法下重排的差值，不能作为物理负活化势垒或速率常数。作者6的 −8.8 没有同构象精确复现，后续前态是实际计算的离子对安排，不以作者数字填补。

定性支持来自实际键变：TS3 的 C1–O43 从1.658464增至2.541064 Å，H80 从O81转移至O43；TS4 的 C5–O72 从2.398021降至1.438154 Å；TS5 的 C5–P19 从1.959157增至3.823580 Å。它们与频率／端点共同支持环化、乙醇生成、亲核加成和催化剂再生。初始步骤为所考察图中最高鞍点、反应总体放能、A 优于已研究 B 瓶颈的方向保持。产物7.09 kcal/mol偏差的全部成因尚未证明，不能擅自归因于软件或构象。

## 4. 现行自主科研科学分V2完整规则

现行唯一评分源：[scoring_rules.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_1bcf80caf9e64d55/evaluation/scoring_rules.json)。总分100；各叶子规则二元计分。AR已可运行评分；严格数值整题未宣称全通过，publication release仍待专家审查。专家tasks中的既有副本均保持历史未迁移。

### 4.1 规则正文及完整中文译文

以下列出当前活动评分条件、角色和分值。只包含提交者要满足的条件；历史计算结果及设计理由分列于4.2和4.3。

只评价任务范围内有论文来源的科学结果，不评价研究过程、工具次数、成本、格式或失败说明。每个叶子项均为二元：全部条件成立得该项满分，否则得0分；没有临时比例分。先核对分子身份、连接关系、原子库存、电荷/自旋、物理量、单位、能量参照、温度、溶剂和标准态，再比较结果。结果须由提交者真实执行且可链接的计算及原生文件支持；公开观察、抄录论文值、正常退出或正确标签本身不充分。最低点与鞍点须有与其声明相适合的频率/态证据；所声称反应连接须有实际结果支持的IRC或科学等价的端点/连接检验，不指定软件、历史验证轨迹、固定假说数量或任务外计算。数值项由宿主按固定target/tolerance作包含边界的绝对差判定，Judge不得修改；允许明确单位及标准态转换，不允许拟合偏移。没有容差的来源背景值不是隐含数值门槛。实质物理身份或来源参照无法厘清时该项needs_review，不用放宽容差掩盖。各项独立，数值超窗不抹去有真实证据的定性项。最终结论项要求提交者明确选择并以计算证据作综合解释，仅计算出或列出一个候选不算最终选择。伪造和隐藏答案泄漏属于有效性问题，普通失败只影响对应项。本文初步容差是维护者按授权提出的benchmark政策，不是作者误差条或统计置信区间；出版专家复审待定不冻结已定义的现行评分。

所有条目绑定`report/results.json`中`$.models`、`$.operations`、`$.artifacts`、`$.results`、`$.claims`、`$.validations`、`$.conclusion`。每项按自身定义独立判定；伪造证据/已证实隐藏答案泄漏属于有效性问题，普通失败仅影响对应项。

**r_phosphine_addition｜phosphine_addition｜PEt3加成与两性离子｜中间科学发现｜8分｜定性**

真实相连计算支持PEt3亲核加成到炔β-C，形成含P–C键的两性离子中间体2；核对PEt3为C6H15P，C7H17P不等价。该项判定键与电荷重排，不依赖TS1数值命中。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_initiation_energy｜initiation_energy｜初始加成的自由能高度｜中间科学发现｜8分｜数值**

以Fig.S1初始复合物1为零点，TS1相对G目标18.9 kcal/mol、绝对容差1.0 kcal/mol；同时计入所有旁观物料并保持383.15 K。不得将分离反应物零点、异构膦或不同化学组成结果直接比较。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_cyclization｜cyclization｜分子内环化｜中间科学发现｜8分｜定性**

中间体2的真实连接与反应模支持向酯羰基分子内进攻、构筑五元环中间体3；须保持完整侧链和原子映射。来源TS2共同高度8.2、3为1.9 kcal/mol仅作背景，不把8.2当局部活化能。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_alkoxide_proton_transfer｜alkoxide_proton_transfer｜醇盐离去与亲核体生成｜中间科学发现｜8分｜定性**

真实相连计算支持环化后醇盐离去及与4-氟苯酚相关的质子转移，形成可参与后续加成的亲核体，并守恒乙醇当量及全部原子/电荷。不同片段缔合须明确，不能以断开的标量节点代替化学连接。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_nucleophile_incorporation｜nucleophile_incorporation｜亲核体并入产物骨架｜中间科学发现｜8分｜定性**

计算的TS4及相连端点支持4-氟苯氧基亲核体形成产物所需C–O连接，保持五元环与E-cinnamyl侧链。来源TS4 2.8与7 −8.3是共同高度背景，不另设数值阈值。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_phosphine_regeneration｜phosphine_regeneration｜PEt3再生｜中间科学发现｜8分｜定性**

实际后续连接支持C–P断裂、释放正确中性PEt3并形成可循环的催化剂；不得只在反应式两侧写PEt3。保持配平乙醇等旁观物料，来源TS5−0.9共同高度仅作背景。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_product_structure｜product_structure｜完整环戊烯酮产物｜中间科学发现｜8分｜定性**

实际终点分子图为所观察的芳氧基环戊烯酮且保留E-cinnamyl侧链，原子来源能与底物/4-氟苯酚及乙醇副产物对应。不得用删除侧链或改变膦的简化产物替代；仅复述所给产物图不通过。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/main.pdf PDF第2,3页，Scheme1/Table1/Table2；底物与产物/实验范围，SHA-256 `eaac68aa7a050468c491614b0279b11eb56e15d8b5551f80a3db699aa12bad36`；papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_reaction_free_energy｜reaction_free_energy｜配平产物总自由能｜中间科学发现｜8分｜数值**

以Fig.S1复合物1和匹配旁观物料为初始参照，配平产物9、PEt3和乙醇终点相对G目标−24.7 kcal/mol、绝对容差2.0 kcal/mol。保持383.15 K、相容溶剂与标准态，不能用分离反应物值或作者能量填补本地缺失。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_initial_step_order｜initial_step_order｜初始步骤为所考察图最高鞍点｜中间科学发现｜6分｜定性**

在同一完整物料及复合物1零点上，实际A路线各相关鞍点比较支持初始膦加成最高，后续关键鞍点较低。不能以单独一个TS1数字证明全图排序；不声称已建立浓度依赖微观动力学。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_migration_competition｜migration_competition｜直接环化与迁移分支的比较｜中间科学发现｜6分｜定性**

从共同两性离子分叉及统一物料参照比较，实际竞争路径证据支持B的醇辅助连续1,3迁移瓶颈高于A分支后环化路线。无需穷举B全部节点；不可把未经计算的后续B状态称独立证实。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`；papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第98,99页，PDF98 Fig.S2及PDF99路线B比较，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_route_conclusion｜route_conclusion｜最终：选择直接环化催化路线｜最终科学结论｜12分｜定性**

最终明确选择PEt3引发两性离子后直接环化、亲核体并入和膦再生的A路线，综合实际连接、完整观察产物与迁移竞争证据说明为何该路线优先。仅列出A候选不足以得分；结论限于所考察模型，不证明全局唯一机理。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/main.pdf PDF第2,3页，Scheme1/Table1/Table2；底物与产物/实验范围，SHA-256 `eaac68aa7a050468c491614b0279b11eb56e15d8b5551f80a3db699aa12bad36`；papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`；papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第98,99页，PDF98 Fig.S2及PDF99路线B比较，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

**r_accessibility_conclusion｜accessibility_conclusion｜最终：动力学和热力学可达性｜最终科学结论｜12分｜定性**

最终以实际完整自由能图及配平终点解释反应可达性：初始加成构成主要能量代价，后续通向总体下坡产物；联系110°C条件但不把12 h或收率当基本速率常数。不要求精确产物G通过，也不能以负复合局部差宣称负物理势垒。

物理定义：PEt3=C6H15P，完整体系C37H45FNO7P，中性总电荷/单重态；氟苯383.15 K，气相几何/频率热项加SMD高层电子能的作者口径。Fig.S1/S2明确采用初始复合物1零点；分离反应物报告必须明确转换，不能混作局部势垒。

论文依据：papers/paper_1bcf80caf9e64d55/documents/main.pdf PDF第2,3页，Scheme1/Table1/Table2；底物与产物/实验范围，SHA-256 `eaac68aa7a050468c491614b0279b11eb56e15d8b5551f80a3db699aa12bad36`；papers/paper_1bcf80caf9e64d55/documents/supplementary_001.pdf PDF第97,98页，PDF97 Fig.S1及计算方法、PDF98路线A文字；无独立S页偏移，SHA-256 `75dad8708b18f23c64cd6377b4e3d7d89ddaf1958f4df68934565613d7b4ea52`

### 4.2 实际验证结果与边界（不属于新评分要求）

|规则ID|作者结果与物理参照|实际验证结果、偏差与限制|
|---|---|---|
|r_phosphine_addition|作者TS1→2|实际TS1相关虚频−234.4652 cm−1及两侧路径/端点支持。物种2作者7.9、本地8.07156651。|
|r_initiation_energy|作者18.9；本地19.05467031，差+0.15467031，命中±1.0。复合物1相对分离反应物+17.076223，须明确保留而非拟合平移。|作者18.9；本地19.05467031，差+0.15467031，命中±1.0。复合物1相对分离反应物+17.076223，须明确保留而非拟合平移。|
|r_cyclization|作者TS2→3|实际TS2−220.9772 cm−1及端点支持。TS2 8.38308104、来源构象3 0.61176526；独立IRC环化端点−4.850322，是另一个构象，不能互换。|
|r_alkoxide_proton_transfer|作者TS3 3.2、6 −8.8共同高度|实际TS3 3.38512872，C1–O43从1.658464到2.541064 Å，H80由O81转到O43。TS3复合局部差−0.565474而低层电子势垒+0.221454，不称负速率势垒；作者6未精确同构象复现。|
|r_nucleophile_incorporation|实际TS4 2.97320452、7 −8.18667497；反应模−182.4433 cm−1及C5–O72 2.398021→1.438154 Å支持。|实际TS4 2.97320452、7 −8.18667497；反应模−182.4433 cm−1及C5–O72 2.398021→1.438154 Å支持。|
|r_phosphine_regeneration|实际TS5−0.74695402，反应虚频−163.1945 cm−1，C5–P19 1.959157→3.823580 Å。每侧一个IRC传播点再无约束端点优化是有限证据，不称完整IRC。|实际TS5−0.74695402，反应虚频−163.1945 cm−1，C5–P19 1.959157→3.823580 Å。每侧一个IRC传播点再无约束端点优化是有限证据，不称完整IRC。|
|r_product_structure|作者产物3/能量图节点9|实际61原子产物+22原子PEt3+9原子乙醇=92原子完整库存，正确E侧链核验。|
|r_reaction_free_energy|作者−24.7；本地−31.78683754，差−7.08683754，明确超±2.0；相对分离反应物−14.710615为不同零点。偏差成因未完全证明。|作者−24.7；本地−31.78683754，差−7.08683754，明确超±2.0；相对分离反应物−14.710615为不同零点。偏差成因未完全证明。|
|r_initial_step_order|作者TS1/2/3/4/5=18.9/8.2/3.2/2.8/−0.9|实际19.05467031/8.38308104/3.38512872/2.97320452/−0.74695402，排序成立。|
|r_migration_competition|作者B必要TS1″18.0、A分支后最高TS2 8.2，差9.8|实际18.122584与8.383081，差9.739503，偏−0.060497。B两个迁移鞍点/有限端点连接已核收。|
|r_route_conclusion|作者A优于B|实际五个A鞍点、正确产物、PEt3再生及B必要瓶颈支持有界选择。|
|r_accessibility_conclusion|实际初始19.05467031最高，配平终点在复合物及分离反应物零点均下坡；产物绝对误差−7.08683754未解决。|实际初始19.05467031最高，配平终点在复合物及分离反应物零点均下坡；产物绝对误差−7.08683754未解决。|

注意：数值栏仅报告既有计算，不是评分阈值或自动通过声明。qualification中的严格数值整题通过为false；来源冲突、偏差和连接边界不因V2迁移而消失。

### 4.3 设计理由（独立于活动评分要求）

|规则ID|分值|权重及容差设计理由|
|---|---:|---|
|r_phosphine_addition|8|将引发化学身份与能量精确度拆开。|
|r_initiation_energy|8|单个关键局部加成能采用±1.0，足以区分后续约8 kcal/mol高度；非作者误差条。|
|r_cyclization|8|环构建是独立于起始加成的核心中间发现。|
|r_alkoxide_proton_transfer|8|单独评价离去/质子转移这一化学事件；不要求额外连接扫描数。|
|r_nucleophile_incorporation|8|亲核体结合与环形成、催化剂脱离均可独立完成。|
|r_phosphine_regeneration|8|催化剂回收是任务明示的科学结果。|
|r_product_structure|8|真实端点结构与再生催化剂是不同对象，独立评分。|
|r_reaction_free_energy|8|多组分净反应热力学采用±2.0，区别于单TS±1.0；不按7.09偏差扩大。|
|r_initial_step_order|6|全图相对排序独立于绝对TS1窗口。|
|r_migration_competition|6|有限但有辨别力的竞争比较，不奖励搜索次数。|
|r_route_conclusion|12|最终路线选择是结构与竞争结果的综合增量。|
|r_accessibility_conclusion|12|面向题面动力学/热力学问题的综合解释，与A/B路线选择分别评分。|

### 4.4 来源与待专家处理事项

来源页码和哈希如4.1逐项所列；机器可读逐规则记录见`evaluation/science_v2_evidence_review.json`。

- 专家边界：产物共同零点−31.78683754对−24.7的−7.08683754偏差未解释；r_reaction_free_energy不通过±2.0。
- 专家边界：TS3复合局部差−0.565474不是物理负势垒；来源构象6未精确复现，保持实际片段/端点口径。
- 专家边界：有限B分支及TS5端点证据不代表全B或全部构象MEP；源标准态未全报告。

请专家按规则ID记录认可/修改/删除及科学依据，并将科学评分合理性与publication release审查分开。

### 4.5 历史未迁移：paper_reproduction

所有规则均绑定 `report/results.json`。原文件未设置 `target`、数值容差、规则权重、`scoring_policy` 或公共结果政策，不从AR借用这些字段。

|rule_id／类型／reference_id|expected 完整直译|绑定字段；comparison 直译|
|---|---|---|
|pr_rule_ts／条件／pr_process_ts_validation|各状态的 frequency_count 和 connectivity_evidence 绑定到 `$.states[*]` 中每个保留的 transition_state。|`$.states[*].frequency_count`、`$.states[*].connectivity_evidence`；专家验证|
|pr_rule_coverage／条件／pr_process_profile_coverage|覆盖字段记录候选、构象、停止及局限。|`$.coverage`；专家过程比较|
|pr_rule_profile／语义／pr_result_profile|提交路径相连，并终止于明确指定的环戊烯酮终点，带有各状态吉布斯能。|`$.pathway`、`$.system.endpoint_smiles`、`$.states`；专家科学比较|
|pr_rule_conclusion／语义／pr_final_mechanistic_claim|最终声明指出初始步骤势垒最高、热力学方向下坡及模型局限。|`$.conclusion`；专家语义比较|
|pr_result_rate_direction_rule／语义／pr_result_rate_direction|剖面指出初始膦加成步骤势垒最高，且总体反应在热力学上下坡。|`$.conclusion`；专家语义比较|

## 5. 原文件、验收与原生日志入口

- autonomous_research：[agent_input/task.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_1bcf80caf9e64d55/agent_input/task.md)；[evaluation/scoring_rules.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_1bcf80caf9e64d55/evaluation/scoring_rules.json)；[evaluation/verified_computation_reference.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_verified_autonomous_research/paper_1bcf80caf9e64d55/evaluation/verified_computation_reference.md)
- paper_reproduction：[agent_input/task.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/paper_reproduction/paper_1bcf80caf9e64d55/agent_input/task.md)；[evaluation/scoring_rules.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/paper_reproduction/paper_1bcf80caf9e64d55/evaluation/scoring_rules.json)；[evaluation/verified_computation_reference.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/paper_reproduction/paper_1bcf80caf9e64d55/evaluation/verified_computation_reference.md)

[父级验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/parent_acceptance_decision.json)；[独立验收](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/review_1bc/独立验收报告.md)；[机器判定](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/review_1bc/independent_acceptance.json)；[62份原生日志审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/local_preflight_followup_20261020T1430Z/review_1bc/native_independent_audit.json)；[作者路线与连接](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_1bcf80caf9e64d55/author_route_closeout_20261020T1340Z/PE_author_route_connections.json)

原生审计中的直接日志样例（全量62份路径与哈希见原生审计）：

- [  gaussian.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_1/paper_1bcf80caf9e64d55/provenance/qzcli_hpc/path_1_wB97XD_383K_20260923/repair_20260923T155950Z/gaussian.log)
- [  gaussian.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_1/paper_1bcf80caf9e64d55/provenance/qzcli_hpc/path_2_wB97XD_383K_20260923_storage_retry_20260925/repair_20260925T060043Z/gaussian.log)
- [  gaussian.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_1/paper_1bcf80caf9e64d55/provenance/qzcli_hpc/path_3_wB97XD_383K_20260923_storage_retry_20260925/repair_20260925T111437Z/gaussian.log)
- [  gaussian.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_1/paper_1bcf80caf9e64d55/provenance/qzcli_hpc/path_4_wB97XD_383K_20260925/repair_20260925T133409Z/gaussian.log)
- [  gaussian.log](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/group_1/paper_1bcf80caf9e64d55/provenance/remaining_path_20260925/path_5_wB97XD_383K_20260925/gaussian.log)

## 6. 专家需要裁定的边界

审查重点是这些来源辅助的相邻态、显式片段平衡和真实共价连接，是否足够支持当前题目要求的有限催化解释；不能把它们升级为逐构象连续最小能量路径或未计算的全部B路线。TS4前态 P–O 为2.100068 Å，而作者6为3.096979 Å，是不同离子对安排，未独立取得重排势垒。B桥接首点上升0.004198 kcal/mol，不能说严格单调。PEt3参考由小残余力和60个正频支持，不能写成Tight四项均YES。TS4日志实际含 negligible-forces 优化完成语句，旧简单解析误报并非失败证据。

如需数值认证，专家应独立校准尚无窗口的各剖面量，并审查产物差值与浅势垒复合方法的物理含义；现有验收不提供满分或发布批准。当前两模式轻量任务已原样复制，原任务／评分／状态未修改。


轻量审查副本：[autonomous_research轻量副本](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/autonomous_research/paper_1bcf80caf9e64d55)；[paper_reproduction轻量副本](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/handle/小分子有机化学反应_审查材料/tasks/paper_reproduction/paper_1bcf80caf9e64d55)。来源路径与文件哈希见对应任务的 `evaluation/evidence_map.json`；数值、方法偏离和定性结论见[新增8篇核对报告](../数值误差与计算方法及定性结论核对.md)。副本无符号链接，未复制外部QC缓存。

## 8. 本次V2专家复审接口

请按第4节规则ID逐条记录认可/修改/删除、物理定义、目标/容差、分值、来源页与理由。审核科学评分合理性与出版资格分开；不能因既有验证超窗直接扩大门槛。真实计算残差、方法差异及连接边界保留在前文和现行science_v2_evidence_review.json。
