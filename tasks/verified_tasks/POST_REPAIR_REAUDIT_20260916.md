# 新批次任务修复后的逐篇复审与 7a 暂缓说明

**当前状态更新（2026-09-17）：下文为迁移前的复审历史；ef266 / Cat1 两项澄清已获准修复，reference 的档案标注和链接也已清理。其余 17 篇、32 包（AR 15、PR 17）完成最终包审查后，已按负责人明确授权迁入对应 final；7a 两模式继续保留在 hold。当前清单和发布边界见[维护总报告第 13 节](MAINTENANCE_REPORT.md)。下文旧目录/待办措辞不代表当前状态，任务链接已更新至实际位置。**

日期：2026-09-16。对应负责人要求：再次确认 7a 是否能直接修复；确认不能后移入 hold；逐篇检查其余任务的验证有效性、输入和指令，提供分析报告。

**后续获准修复更新：负责人随后明确批准处理 ef266 接触定义与 Cat1 AR 选态冲突，这两项现已修复并通过 62 项回归测试，详见第 7 节。第 1–6 节保留初次复审的证据与当时状态；其中这两项“未实施”已由第 7 节取代，其他建议没有在本轮扩大实施。**

## 1. 结论与本轮实际操作

审查范围是本轮新验证批次 **18 篇论文、34 个任务包**，不是第一批 final 的重新认证。按正文/SI、真实输出、当前任务及 evaluator 逐项对照，不把旧 PASS 标签或 reference 标题当作验证结论。

1. **`paper_a3968806251093cd` 不能仅通过改标签、改描述或整理旧输出补齐验证。**当前任务的分子图已修正，但检索到的旧计算做的是另一位置异构体，不能证明正确 7a 的 evaluator 结论可算得。两模式已按本次明确授权完整移入对应 hold，详见第 3 节。
2. **其余 17 篇、32 包（AR 15、PR 17）的核心作者路线计算均有实际输出支持。**本轮未发现第二篇同等级的“错误研究对象导致验证无效”，也没有发现必须仅因更换公开初始结构而重新做量化计算的理由。这不是“任意方法、任意构象、全部开放分支或全部过程分均已验证”的保证。
3. **不能宣布所有任务已没有问题。**`ef266…` 两模式仍应明确接触量的选择/汇总定义，主要影响 PR 固定数值评分；`46a9…` 的 AR 有前后选态措辞冲突。此外，有数处 reference/证据索引仍把历史输入写成当前输入，以及 3 处 canonical 链接指回当前包。这些不是缺少真实计算，但应在验收前澄清。
4. 公开内容复查未发现此前四篇的待求作者几何/TS 又进入 `agent_input`。五篇获准的“给定对象性质计算”保留结构，按负责人已确认的范围处理，不再把这类合法条件输入重新列为泄露。

**本轮只实施了 7a 迁移、迁移后的链接/状态/包清单维护、回归测试及本报告。其余 17 篇的 task、输入、schema 和 evaluator 未再改动，仍留在 verified_tasks，未移入 final/hold。**没有新增量化计算、HPC 操作或 LLM 评分；没有修改 `docs/verification`、论文、canonical 任务或第一批 final。没有开展已交其他 agent 的科研自主性统计。

## 2. 审查口径与总体证据

### 2.1 什么算验证成立

- 验证者可以知道作者路线、终态坐标和 TS；只要对象、物理量和条件正确，真实结果支持 evaluator 核心结论，就能说明该科学目标有可计算路径。不要求历史验证模拟未知答案 agent。
- 独立 starter 未盲跑，不等于科学目标未验证；但是不能把已有作者终态验证说成“当前 starter 已独立收敛成功”。
- reference 仅记录有效历史计算。评分仍以五个 evaluator JSON 为准；不将 reference 作为新的标准答案匹配器。
- 纯实验观测、合法反应物/给定对象、方法参数和校准常数不自动等于结果泄露。待求几何、待求 TS、计算频率/电荷/能垒等终值则不能公开给 agent。
- 没做过的敏感性、全局搜索或额外通道，不能因有一条成功链就获得相应过程分。允许报告限制并不等于验证了该额外要求。

### 2.2 做了哪些交叉检查

逐包对照 `task.md`、实际公开文件、submission schema、五个 evaluator JSON、运行器使用的 `task_info` 描述，以及两模式 reference；阅读正文/SI 对应计算段落和已记录的有效输出。重新核查了 17 篇 reference 链接的 **98 份不同原始日志，均存在**；这些文件包含组合任务及后处理日志，98 不是独立量化计算次数。没有把 Multiwfn 不含 Gaussian 终止标记当作失败，也没有把旧 FC 失败段当作有效步骤。

历史 `report/results.json` 可直接对应当前 **61 条数值规则（AR 20、PR 41）**，标量均处于现有容差内。这只是数值交叉检查，必须结合身份、单位和条件使用。特别是 Cat1 的旧总结果对应旧选态，不能直接作为当前主结果；本轮另读最高 f 的 state20 原始 TD/IFCT 输出，确认当前主协议的 63.541%/3.820% 同样满足原有界限。

运行器包物化检查仅复制 `agent_input`，不复制 author_results/reference/provenance；当前相关元数据描述也未发现答案数值。这证明包内分区按预期工作，**不代表已验证部署时的共享父目录、挂载、网络和文件访问隔离**。

## 3. paper_a3968806251093cd：为什么确认暂缓

模式：AR、PR；来源 group_2。

### 3.1 不只是原子编号不一样

[正文](../../papers/paper_a3968806251093cd/documents/main.pdf) PDF p4 §3.2/Fig. 3 定义 pyrazole 环为 **N1–N2–C9–C8–C7**：N1 接 phenyl，C7 接 O1–chlorophenyl，C8 接 imine，C9 接 methyl。当前修正后的公开分子图与这些连接以及 47 个实验比较选择器一致。

历史 [B3LYP 优化末态](../../docs/verification/group_2/paper_a3968806251093cd/artifacts/generated_structures/7a_author_B3LYP_optimized.xyz) 按旧标签映射却有：

| 检查 | 历史真实距离 | 含义 |
|---|---:|---|
| N1–C7，XYZ 4–21 | 2.19649222 Å | 论文要求的环内连接不存在 |
| N1–C8，XYZ 4–11 | 1.37657131 Å | 实际接到了另一个取代碳 |
| O1–C7，XYZ 22–21 | 1.36886356 Å | 苯氧基取代位置关系与正确环图不一致 |

两条 B3LYP/CAM-B3LYP 作业正常终止、各 132 实频，但这是错误位置异构体的正常计算。相同分子式 C20H17ClN6OS、相同 46 原子数，不能抵消连接图错误；重命名也不能改变化学图。

### 3.2 有没有可直接替换进来的正确旧结果

再次检查 group_2 本篇目录的 **67 份可恢复几何，匹配正确图的为 0**；额外检查 [author_route_queue 目录](../../docs/verification/group_2/author_route_queue/paper_a3968806251093cd) 的两份作者级起始 XYZ，仍不匹配。独立的去氢重原子图同构检查也不通过，排除了仅氢原子或编号造成的误判。跨现有验证/运行目录检索未找到另外可用于本题的正确对象成功链；这不等于断言负责人其他存储位置也不存在。

因此，可直接修的是公开身份、实验表和映射，前轮已做；**不能直接补成“已经验证”的是正确对象的两条计算及有效几何误差比较**。不能用错对象的旧 MAE/RMSE 宣布 CAM-B3LYP 对正确 7a 更优，也不能通过放宽容差或更换科学对象掩盖缺口。

### 3.3 已执行和后续交接

已完整移动：

- [AR hold 包](../hold_verified_autonomous_research/paper_a3968806251093cd)，保留[历史计算归档](../hold_verified_autonomous_research/paper_a3968806251093cd/evaluation/verified_computation_reference.md)。
- [PR hold 包](../hold_verified_paper_reproduction/paper_a3968806251093cd)，保留[历史计算归档](../hold_verified_paper_reproduction/paper_a3968806251093cd/evaluation/verified_computation_reference.md)。

只更新位置链接、当前状态及包清单，科学输入/evaluator 未因迁移改写，原始验证文件未删除。重新纳入前，优先向验证负责人索取正确对象既有输出；若确实没有，则交验证 agent 单独处理正确对象，不是本轮重算。核对连接图后，再核对两泛函的有效站点、13 键长/23 键角/11 二面角分项误差，以及 PR 总体结论是否真的有依据。不能将 Å 和角度任意加权来制造一个赢家。

## 4. 其余 17 篇逐篇结论

下文“支持”指当前科学目标的核心作者路线存在真实计算证据；不是迁移或发布授权。两模式分别检查，仅 d796、44f 没有 AR。

### 4.1 group_1 / paper_d2d08c91f34da1cb — Rhodamine101 两态低频振动（AR、PR）

**验证。**[正文](../../papers/paper_d2d08c91f34da1cb/documents/main.pdf) 的方法/模式讨论及 Table 1、SI 两态对象，与当前任务一致。S0/S1 各 195 实频；24 项实验配对的 MAE 1.262626、最大误差 3.097158 cm⁻¹。位移匹配保留模式交换、混合和正移例外。见 [reference](../final_verified_paper_reproduction/paper_d2d08c91f34da1cb/evaluation/verified_computation_reference.md) 及其原始频率/位移输出。

**输入和评分。**按已批准的给定两态对象范围保留坐标；公开实验 SLT 峰，不公开作者计算频率/位移/误差。PR 现行评分不再要求所有片段模式统一红/蓝移，也没有硬性 max<3 的错误门槛；AR 根据自算模式解释。

**判断/建议。**核心可计算性有据，未发现新的数据缺失或答案输入；不能外推全谱逐项吻合。PR reference 的 canonical 链接标签有错（第 5 节），只需档案清理，不需要新计算。

### 4.2 group_1 / paper_6f9a36fff6964313 — 三体系 Mulliken 电荷（AR、PR）

**验证。**[SI S16](../../papers/paper_6f9a36fff6964313/documents/supplementary_001.pdf) 给出优化/频率与单点两层路线；完整离子对/TFAP 各有 45/90/105 实频。四个目标电荷实际为 0.203728、0.198533、0.040059、0.058695 e；相关差为 −0.005195、+0.018636 e。见 [reference](../final_verified_paper_reproduction/paper_6f9a36fff6964313/evaluation/verified_computation_reference.md)。

**输入和评分。**公开图、OTf、原子角色、电荷/自旋和 MeCN 完整，无作者电荷或几何终值。PR 已公开 B3LYP-D3BJ/6-31G(d,p)/IEFPCM 优化频率，再 M062X-D3/def2TZVP/SMD 的主比较协议；原四个 ±0.02 e 目标不变。AR 不机械锁定这些数值。

**判断/建议。**支持电荷比较这一核心目标；每体系一个已验证构象不能证明构象无关。任务现允许有限覆盖并报告限制，未做的敏感性不给相应分，不因此要求本轮重算。PR canonical 链接标签待清理。

### 4.3 group_1 / paper_746e066c163800d8 — helicene 5 扭转（AR、PR）

**验证。**[正文](../../papers/paper_746e066c163800d8/documents/main.pdf) PDF p4 报计算平均角 27.1°、实验 27.0°。既有 72 原子极小值有 210 实频；五个局部角的平均绝对值为 27.09676855°，收紧条件检查为 27.09673780°。见 [reference](../final_verified_paper_reproduction/paper_746e066c163800d8/evaluation/verified_computation_reference.md)。

**输入和评分。**当前公开为完整化学图独立生成的未优化初态，原作者终态和实验目标角私有。公开链索引 `[1,66,65,64,63,62,61,59]` 及五角 `mean(abs(phi))` 约定，不给五角数值。失败分支允许 Hessian 未取得时如实填未知。

**判断/建议。**目标几何量有真实作者路线支持；没有再公开该待求几何。新初态没有盲跑记录，但不据此撤销旧作者路线验证。reference 的“公开实验边界页码”旧话和 PR canonical 链接应标明历史/改正。

### 4.4 group_1 / paper_5ea491c741fbd8d4 — isoxazole 1a 构象及轨道（AR、PR）

**验证。**[正文](../../papers/paper_5ea491c741fbd8d4/documents/main.pdf) 中基组表述有冲突，当前已显式采用支持现有结果的 B3LYP/6-311+G(d,p) 主比较定义。五个候选均有 75 实频，去重后 3 个极小值；代表 seed303 的能量 −744.463909848 Eh，HOMO −6.56393059、LUMO −2.88386271、gap 3.68006788 eV，满足原 PR 容差。见 [reference](../final_verified_paper_reproduction/paper_5ea491c741fbd8d4/evaluation/verified_computation_reference.md)。

**输入和评分。**身份输入不含作者轨道值或最优构象。PR 主协议清楚；AR 保持方法探索。失败候选现在能填 null 并说明，不能用虚构 0 虚频伪装通过。

**判断/建议。**既有有限构象覆盖与电子结构结果足以支持所选目标，未发现新的缺失/泄露；不声称已证明全局构象最低点或任意方法数值相同。

### 4.5 group_1 / paper_a0f6b899582cb9f7 — M3 四极矩（AR、PR）

**验证。**[SI Table S1](../../papers/paper_a0f6b899582cb9f7/documents/supplementary_001.pdf) 的 M3 Qzz 是比较依据。正确 24 原子对象已有 3 个极小值、各 66 实频；raw Qzz −111.07681064 DÅ，落在 −108.35±5；偶极约 0，面 RMS 0.00025046 Å，N···S 2.99065047 Å。见 [reference](../final_verified_paper_reproduction/paper_a0f6b899582cb9f7/evaluation/verified_computation_reference.md)。

**输入和评分。**独立 M3 初态，目标值私有；task 明确 raw 二阶矩而非 traceless 四极矩、原点、完整旋转、平面法向和 DÅ，避免用另一张量定义比较。

**判断/建议。**未发现新的必要数据缺失或测量定义冲突。支持孤立 M3 的所选量，不是验证整个太阳能电池性能或界面机制。

### 4.6 group_1 / paper_ef26687d63a37e29 — P 体系接触、电荷、ESP（AR、PR）

**验证。**[正文 Fig. 6 及 p10 讨论](../../papers/paper_ef26687d63a37e29/documents/main.pdf) 的完整 free/PO/PA 模型，分别 46/56/61 原子、132/162/177 实频；P-ADCH −0.018993/0.447060/0.455684 e，六项接触均在原容差内，实际 MEP/ADCH 后处理存在。见 [reference](../final_verified_paper_reproduction/paper_ef26687d63a37e29/evaluation/verified_computation_reference.md)。没有采用旧截断模型作为当前证据。

**输入。**前轮已将三个体系全部换成独立完整图初态，作者坐标片段私有；mapped graph 指定 P、O、N-ethyl α/βH，0/1 及 isolated 状态明确。未发现待求距离、电荷或几何终态公开。

**仍有实际歧义。**[PR task](../final_verified_paper_reproduction/paper_ef26687d63a37e29/agent_input/task.md) 与 [AR task](../final_verified_autonomous_research/paper_ef26687d63a37e29/agent_input/task.md) 都只写 PA “carboxylate group”的 O···P/αH/βH；schema 却要求每类单个汇总值。PA 有两个羧酸根 O、多组 α/βH，未明确应固定哪个 O、是否取最近 H、三个数能否来自不同 O。PR `r_pr_H_charge` 还写 “source-selected contact-H”，而 agent 无法看 SI。

从[真实 PA 末态](../../docs/verification/group_1/paper_ef26687d63a37e29/report/structures/PA_optimized.xyz) 只读重提取：

| 固定同一氧后取各角色最近 H | O···P / Å | 最近 αH / Å | 最近 βH / Å |
|---|---:|---:|---:|
| O49（既有主结果采用） | 2.652210310 | 2.311797025，H27 | 2.363290557，H29 |
| O50（同属羧酸根） | 4.517730444 | 3.871389670，H6 | 2.280825829，H15 |

可见并非填“一个合理接触”就必然与私有比较量相同。**影响两模式的可重复汇总，PR 因固定数值评分更应先澄清；不是核心量没有算过。**

**建议修法。**不公开上述结果；公开一个由化学角色/映射定义的主 O 及同一 O 下的最近 αH/βH 选择规则，允许等价原子映射并要求报告证据；另列所有候选 O/H 接触作为辅助，不跨 O 拼三个最小值。主 O 定义应和历史 O49 的物理角色对应，不按“最接近 gold”选择。同步 task、schema 的字段说明及 evaluator comparison；将 source-selected H 改为公开规则选出的 H，同时保留全部角色电荷。无需新的量化计算，可用现有坐标/波函数后处理核对。**本轮未擅自实施此定义调整。**

### 4.7 group_1 / paper_e31cc7bc7b21b610 — egan-IrCl 两异构体（AR、PR）

**验证。**[SI S24–S25](../../papers/paper_e31cc7bc7b21b610/documents/supplementary_001.pdf) 的 cis-α/cis-β 对象与当前任务一致；58 原子，各 168 实频。Eα −2204.52499151、Eβ −2204.52269915 Eh，Eβ−Eα=+1.43847762 kcal/mol。见 [reference](../final_verified_paper_reproduction/paper_e31cc7bc7b21b610/evaluation/verified_computation_reference.md)。

**输入和评分。**按已确认的给定异构体性质边界保留结构，不给总能/能差/能序。现有数值 1.44±1.5 之外另要求正的 Eβ−Eα 与能序、绝对能自洽，不能让微负值凭宽容差通过结论。

**判断/建议。**两对象能差可计算有据，未发现新的信息缺口；不宣称完整异构体搜索或实验溶液平衡均被验证。

### 4.8 group_1 / paper_80cc1ffb2cf73fc5 — Z1 相对振动精细谱（AR、PR）

**验证。**27 原子阴离子/中性体各 75 实频，独立 FC 成功输出可查。主物理 in-plane mode 的频率 85.9573 cm⁻¹、HR 1.20932，模式回收约 99.63%；11 个窗口跃迁和筛选敏感性有记录。见 [reference](../final_verified_paper_reproduction/paper_80cc1ffb2cf73fc5/evaluation/verified_computation_reference.md) 和 [SI Fig. S1](../../papers/paper_80cc1ffb2cf73fc5/documents/supplementary_001.pdf)。组合旧日志中后续失败的 FC 段不替代独立成功日志。

**输入和评分。**给定 anion 范围已获批准；当前公开 825 点纯黑色实验 trace，非作者理论/拟合曲线。任务规定自算 0–0 与实验 19444 cm⁻¹ 原点相对对齐，不提供作者计算平移量。模式按物理位移识别，不强制软件编号。

**判断/建议。**支持 Z1-only 相对谱的有限突出特征及进动，不是绝对 ADE 或全谱精确复现；19748/19844/19920 cm⁻¹ 等未解释特征必须保留。诚实异议可得证据/过程分，不自动等于复现结论。没有理由仅因这些已披露边界要求新增量化计算；reference 前段“无实验数据”旧话应时态化。

### 4.9 group_2 / paper_a3892396b1843698 — 两通道 sigmatropic TS（AR、PR）

**验证。**[正文](../../papers/paper_a3892396b1843698/documents/main.pdf) 的 [3,3]/[5,5] double-boat 通道，对应 25 原子反应物、69 实频；两 TS 各一虚频 −364.361/−320.5474 cm⁻¹，双向 IRC 和四个端点各 69 实频。ωB97X-D 小基组几何/大基组能量加 entropy-only qRRHO 给出 23.50589160/26.22790785 kcal/mol，满足 23.5/26.2±3。见 [reference](../final_verified_paper_reproduction/paper_a3892396b1843698/evaluation/verified_computation_reference.md)。

**输入和评分。**只公开已知反应物 3a；没有给产物或 TS 终态。PR 提供作者路线，AR 自行研究通道；身份、温度/溶剂及热化学口径可查，评分需几何/虚频/连通证据而非只报能垒。

**判断/建议。**两条核心搜索终点及连通性有充分历史支持，未发现本轮新的缺失、泄露或指令冲突。作者验证使用 TS 起点不使该验证无效，也不授权把 TS 公开。

### 4.10 group_2 / paper_46f6118697c6397c — 晶体对象的 UV–vis（AR、PR）

**验证。**68 原子、完整四 triflate 模型，3 个几何分支各 198 实频加 TD50。代表主跃迁为 3.8445/3.8138/3.8208 eV，f=0.4733/0.4255/0.4292，均满足现有界限。见 [reference](../final_verified_paper_reproduction/paper_46f6118697c6397c/evaluation/verified_computation_reference.md)。[SI](../../papers/paper_46f6118697c6397c/documents/supplementary_001.pdf) 的 3.8436 eV、322.58 nm、f=0.4243 自洽；正文 4.33 eV 与 323 nm 冲突，不能同时当正确金标。

**输入和评分。**CIF 自包含，四个阴离子及电荷/自旋齐全；没有公开 TD 值。已有说明采用 SI 自洽定义，以物理跃迁解释而非死认 state5 或固定轨道编号。

**判断/建议。**所选模型吸收性质有实际支持，未发现新的数据/泄露问题。此单体系不能证明系列配体因果效应或全部材料光学性能；任务当前限制范围应保留。

### 4.11 group_2 / paper_d8e5490cd9942f4f — La syn/anti 自由能（AR、PR）

**验证。**81 原子 La 体系，+1/singlet，water 中 ωB97X-D/def2-SVP/La ECP46MWB；两端点各 237 实频。Gsyn −1941.937433、Ganti −1941.930431 Eh，anti−syn=4.393821 kcal/mol，与 4.2±1 一致。见 [reference](../final_verified_paper_reproduction/paper_d8e5490cd9942f4f/evaluation/verified_computation_reference.md)；[SI](../../papers/paper_d8e5490cd9942f4f/documents/supplementary_001.pdf) p21 给出大芯赝势/伪单重态等方法，p22 Table S2 的 La 行明确 ΔGconf=+4.2 kcal/mol。

**输入和评分。**保留已批准的给定两端点范围；电荷、多重度、水/298 K/1 M、能差方向清楚，不给自由能结果。论文几何作为给定对象，不再声称本题评独立发现这两种构象。

**判断/建议。**支持两对象的所选能差，未发现新的必要信息缺失；不把两局部端点验证说成全局构象搜索。按当前范围无需新增计算。

### 4.12 group_2 / paper_c23cfabbd34b087f — 1M-TIPS 模型吸收（AR、PR）

**验证。**[正文](../../papers/paper_c23cfabbd34b087f/documents/main.pdf) 的 1M-TIPS 计算吸收对应当前 C58H42Si2、102 原子模型。300 实频，PCM(CHCl3) TD20，735.93 nm/f=1.2539，对应 735±25/1.24±0.25；209→210 的主贡献约 0.69912，有 π→π* 物理解释。见 [reference](../final_verified_paper_reproduction/paper_c23cfabbd34b087f/evaluation/verified_computation_reference.md)。

**输入和评分。**获准给定模型，无光谱/轨道答案；溶剂和化学身份清楚，按跃迁物理性质评分，不固定轨道号，也不额外强制 NTO。

**判断/建议。**核心模型计算有据，无新的答案泄露/关键输入缺失。不得外推为实验长链或聚集体系。其 schema 主要描述成功提交，未像部分其他任务那样提供结构化 bounded-failure 分支；这是失败上报一致性的可选改进，不是现有成功路径不可完成的证据，也不应私自降低成功判据。

### 4.13 group_2 / paper_d7967e22bb965daa — 四条 Fe 插入 TS（仅 PR）

**验证。**[正文](../../papers/paper_d7967e22bb965daa/documents/main.pdf) 对应四种路线和各自 INT2 局部零点。现有 20 个成功阶段：6 Opt/Freq、6 单点、8 IRC；两个 INT2 各 198 实频，四 TS 各一虚频 −851.0093/−835.2003/−827.7649/−829.663 cm⁻¹。四局部势垒 10.258029/12.425524/13.190985/12.022525 kcal/mol，在各自 ±1 内，排序 A<D<B<C。见 [reference](../final_verified_paper_reproduction/paper_d7967e22bb965daa/evaluation/verified_computation_reference.md)。

**输入和评分。**四个作者 TS 现只在 author_results，公开为两 INT2、映射后的四通道、加成面、氢迁移角色、方法/局部参考能及同一热化学定义，未公开 TS 坐标/能垒。

**判断/建议。**核心四 TS 与局部势垒已得到真实验证，不能因验证者使用作者 TS 就否定可计算性。IRC 达到 MaxPoints 的分支不冒称优化产物极小值；当前限定路径证据应保留。reference 早段仍称“公开四 TS/原样复制”，应标历史，但实际公开目录没有这些 TS。

### 4.14 group_4 / paper_5d94285cfbd51973 — AZ9 构象/前线轨道（AR、PR）

**验证。**[SI 描述符表](../../papers/paper_5d94285cfbd51973/documents/supplementary_001.pdf) 与当前 AZ9 身份一致。53 原子，611 候选/12 轮/9 个不同盆地各 153 实频，9 组关联单点敏感性结果可追溯。basin04 HOMO −5.59139565、LUMO −1.16981749、gap 4.42157815 eV，dipole 6.0404 D，满足原目标。见 [reference](../final_verified_paper_reproduction/paper_5d94285cfbd51973/evaluation/verified_computation_reference.md)。

**输入和评分。**SMILES 自包含、不含最低构象/电子结构值。公开 conventional 描述符公式，未沿用 SI 不一致的符号/异常公式；任务和 evaluator 口径一致。

**判断/建议。**当前有限构象与电子结构目标支持充分，未发现新的缺失/泄露；不据此声称全局最低构象证明或生物活性验证。

### 4.15 group_4 / paper_b33676a2051f5e91 — Int-3 自由基裂解（AR、PR）

**验证。**[正文](../../papers/paper_b33676a2051f5e91/documents/main.pdf) 中 acetophenone+ethyl radical 通道，24 原子 doublet Int-3 有 66 实频，TS 唯一虚频 −474.9764 cm⁻¹，ΔG‡=8.89745683 kcal/mol，满足 9.07±2。反应物侧 IRC 64 点到极小值；产物方向 80 点达 MaxPoints，C–C 3.65849 Å、C–O 1.21343 Å、ethyl spin 0.998047，支持既定断键归属。见 [reference](../final_verified_paper_reproduction/paper_b33676a2051f5e91/evaluation/verified_computation_reference.md)。

**输入和评分。**公开 Int-3 合法反应物，不公开 TS。PR 指定路线；AR 保持开放通道，数值 9.07 仅在映射产品/断键确属该通道时适用，不能惩罚另一个有效通道的不同能垒。

**判断/建议。**该核心通道可算有据，不宣称验证了所有 AR 可选通道；产物极小值未单独优化也不能假装做过，但不是该局部活化自由能尚无验证。无需因开放探索范围要求本轮补算。

### 4.16 group_4 / paper_46a9ca0dab36dd9e — Cat1 IFCT（AR、PR）

**验证。**[SI S34–S35](../../papers/paper_46a9ca0dab36dd9e/documents/supplementary_001.pdf) 支持 30 个低激发六重态中最高 f 选态，而非固定 state22。34 原子基态 96 实频；现有 [TD30 输出](../../docs/verification/group_4/paper_46a9ca0dab36dd9e/hpc_runs/cat1_m06_gd3_source_parent_td30_20260914_hpc20_p6/stdout.log) 中最亮为 state20，f=0.0415，state21/22 为 0.0299/0.0237。其 [Mulliken-like IFCT 原始表](../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state20_mulliken/stdout.log) 给出 Cl→Fe 0.63541、Fe→Cl 0.03820，即约 63.541%/3.820%，支持 62.4±10/4.3±5。旧 state22/Hirshfeld 不是当前主态证据。

**输入和评分。**完整离子对/隐式 MeCN/Cl、Fe、TEA+ 三片段/全部通道归一化明确；无 IFCT 结果公开。PR 主协议和最高 f 定义清楚；[reference](../final_verified_paper_reproduction/paper_46a9ca0dab36dd9e/evaluation/verified_computation_reference.md) 保留旧选态历史并附当前主态。

**仍有措辞冲突。**[AR task 第 11 行](../final_verified_autonomous_research/paper_46a9ca0dab36dd9e/agent_input/task.md#L11) 仍举例可按 energetic accessibility 或任意合理标准选态；第 13 行却规定主分析必须最高 f。后条较具体，能解释主次，但不应让 agent 猜；同段“Do not assume ... target state”也宜明确为不能预设编号/结果，而非取消已定义的物理选态准则。

**建议修法。**将前段改成“自主设计足够的几何/态覆盖；主分析按下述最高 f 规则；其他标准选出的态只作辅助/敏感性”，统一隐式溶剂措辞。保持分区、金标和科学目标不变，不需要新计算；本轮仅报告，未改任务。

### 4.17 group_6 / paper_44f9727c4e9a4b6f — 1H Fe 几何/自旋/Mössbauer（仅 PR）

**验证。**[SI S5–S6](../../papers/paper_44f9727c4e9a4b6f/documents/supplementary_001.pdf) 的 HS→BS 和核密度校准路线。87 原子 +2 模型的 HS/BS 正常结束；完整频率表 261 项是 3N 笛卡尔打印项，不全是物理振动模。BS Fe···Fe=3.086431831 Å，EBS−EHS=−0.026282803515 Eh。采用 SARC/J、DefGrid3 的正确密度单点得到 13784.379018901/13784.360314861，按公开源校准得 δ=0.5178094024/0.5236036402 mm/s，满足 0.52±0.07。见 [reference](../final_verified_paper_reproduction/paper_44f9727c4e9a4b6f/evaluation/verified_computation_reference.md)。

**输入和评分。**现为独立 87 原子完整配位图初态；O3–O4 peroxo、O5 μ-oxo、无 Fe–Fe 共价键定义明确，待求作者几何私有。校准公式/常数是必要方法输入，保留不构成目标密度或位移泄露。

**判断/建议。**已有计算支持所选几何、自旋与位移。ORCA 版本、解析/数值 Hessian 适配、未作自旋投影已披露，不是整篇形成机制验证。`evidence_map` 最后一条仍写 SI Table S10 “public ... coordinates”，应更新成私有历史参考；实际当前公开文件已替换，不是泄露仍存在。

## 5. 剩余问题及最小处理清单

| 问题 | 包/位置 | 对当前评估的影响 | 建议处理 | 需要新量化计算？ |
|---|---|---|---|---|
| 正确 7a 没有匹配的旧验证链 | a396，AR/PR，已 hold | 不能认证正确研究对象的结论 | 找正确对象既有输出；没有则交验证 agent，不能改名套用错对象结果 | 若无既有输出才需要另行安排；本轮未做 |
| 接触选择/汇总规则不完整 | ef266，AR/PR task/schema；PR H-charge/comparison | 同一结构可能报不同且都看似合理的 O/H 接触，PR 错罚风险 | 公开无答案的 O/H 选择定义，统一字段/评分 | 否；用现有几何/波函数核对 |
| 自选态与主分析选最高 f 的残留冲突 | 46a9，AR task 前后段 | 不清楚哪个选择标准优先 | 明确最高 f 是主结果，其他态只辅助 | 否 |
| 历史输入叙述未完全改为过去时 | ef266、746、d796、80cc reference；44f evidence_map | 审计者会误以为仍公开作者结果或仍缺实验输入 | 保留历史事实，注明当时/当前；不改原始 group 记录 | 否 |
| 3 处 canonical 链接语义错位 | PR d2d08、6f9a、746 reference 第 15 行 | `[canonical 源任务](..)` 实际打开暂存包，不是 canonical | 改到 `../../../../paper_reproduction/{paper_id}` | 否 |
| 成功/失败提交格式未完全统一 | c23cf 两模式 schema | 失败情形不如其他包方便结构化报告，不影响已有成功路径 | 可另做通用失败上报规范，不改成功科学标准 | 否 |
| 部署隔离尚非本轮验证对象 | 运行环境 | 若 agent 可读整个仓库，私有答案仍可能被访问 | 发布/运行端只给公开任务目录，限制父目录和共享挂载等访问 | 无需量化计算，但需部署测试 |

reference 的历史选态、未测试新 starter、有限 IRC 长度、有限构象/谱峰覆盖等不能简单删掉以取得“完全一致”。应准确表达：**同一科学子目标的真实可计算证据成立，同时保留验证边界**。这和“缺数据导致死胡同”是不同问题。

除迁移 7a 所需的文档/包维护外，上述清理建议尚未实施；没有以本轮报告替代负责人对具体任务调整及迁移的确认。

## 6. 验收记录与交付边界

- 7a 两个完整包已从 verified_tasks 移入对应 hold；其余 32 包仍在 verified_tasks，没有移动 final。
- 7a 的科学输入、schema、task_info、paper_route、五核心 evaluator 与迁移前版本一致；只维护 reference/provenance 状态、相对链接及包清单。
- `python -m pytest tests/test_task_package_v19.py tests/test_staged_repairs_20260916.py -q`：**55 passed**。包括 32 个暂存包、两个迁移后 hold 包及 schema/运行器物化/专项回归；这些软件检查不替代本报告的化学身份/原始计算检查。
- 138 份包内及本批报告 Markdown 中的 1265 个相对链接均可定位；3 处 canonical 标签错位属于“目标存在但含义不对”，并未被机械链接检查掩盖。限定本轮路径的 `git diff --check` 通过。
- 与修复提交 `db98ad0c` 比较，其余 32 个任务包没有本轮改动；7a 除上述迁移维护文件外没有内容变化。
- 作为发布准备，建议先清理 ef266 的量定义、Cat1 AR 的冲突措辞和上述档案标注，再由负责人确认迁移；无需将其余 17 篇打回重新进行作者路线量化验证。
- 本轮没有给第一批 final 出具新的整体无泄露保证，也没有进行当前公开 starter 的端到端盲测或真实 LLM judge 一致性试验。

本报告按论文阅读与计算溯源审查的方式，将正文/SI 事实、真实输出、维护记录和当前任务边界分开，避免把历史标签当科学证据。后续处理本批只需以本报告为当前复审入口，不必再从旧报告的每一轮建议推断状态。

## 7. 两项澄清问题的获准修复结果

负责人明确要求修复第 4.6、4.16 节所述两处问题。实际修改 **3 包**：ef266 的 AR/PR，Cat1 的 AR。Cat1 PR 已一致，仅复核、不改动；所有包仍留在 verified_tasks，没有 final/hold 迁移。

### 7.1 ef266 两模式：固定主 O，按角色分别选最近 H

- 主 O 固定为输入 atom-map 49；PO 是链端 O，PA 是公开图中 C48=O49 的指定羧酸根 O，不是 O50 或 acyl O51。P 固定为 map 46。允许坐标重编号，但必须保留输入原子追踪，不能交换两个氧来改善数值。这是观察量定义，不约束优化后的距离、键级或电荷。
- 同一优化结构、同一主 O 分别取 O-P、到全部 N-ethyl alphaH 集合的最近距离、到全部 betaH 集合的最近距离；不能平均或跨 O 拼最小值。精确并列时用最小输入 atom-map ID，并报告并列及映射。
- 主接触对和距离保存在 `species[].distances`。PR 的原 `contact_summary` 三值明确对应这些接触；AR 仍可只交原有逐原子距离，summary 仅新增可选定义，没有强加 PR 数值评分。
- 主接触 H 的 ADCH 必须来自距离规则选中的相同 H；所有 N-ethyl H 的逐原子电荷仍保留。其他 O/H 接触作为辅助，不再要求 agent 猜私有的 “source-selected H”。
- 同步修改 task、schema 描述、相关关键点和评分 comparison、task_info。没有新增/删除评分规则，没有改变数值、容差、单位或权重；所有公开 XYZ/身份图保持不变，没有把下表的计算结果放入 agent_input。

从公开图独立解析 12 个 alphaH、18 个 betaH，再读取旧成功优化末态后处理：

| 体系 | O49-P46 / Å | 最近 alphaH / Å | 最近 betaH / Å |
|---|---:|---:|---:|
| PO | 1.8292620004 | H5，2.1250927092 | H45，2.4404698771 |
| PA | 2.6522103098 | H27，2.3117970249 | H29，2.3632905567 |

全部六值及其接触 H 电荷与旧 `results.json` 一致；不需要新的量化计算。两包 reference 追加了这项测量定义/后处理核对，原始 group 计算文件未写入。辅助接触表是由已存在几何得到的后处理，不冒称新做了优化。

### 7.2 Cat1 AR：主选态规则前后一致

- 目标、过程要求和 schema 均明确：低激发六重态中有覆盖证据的最高振子强度物理态为主对象，不预设软件编号或电荷转移答案。
- 其他理由选出的态只作辅助/敏感性，不替代主态；`state_selection` 与顶层 `ifct` 必须对应同一主态，其他态保留在带身份的 `ifct_records`。
- 将模糊的“排除溶剂”统一为隐式 MeCN、无显式溶剂；保留自主方法、几何和态空间设计，没有给 AR 注入 PR 全套计算路线。
- 同步覆盖关键点、coverage 评分文字和 task_info。既有最高 f 的 state20 真实 IFCT 仍支持原比较，原数值/容差不变；PR 无改动。

### 7.3 检查结果与范围

- 包校验、schema、运行器评分承载及公开文件物化、历史几何接触/电荷回归：`python -m pytest tests/test_task_package_v19.py tests/test_staged_repairs_20260916.py -q`，**62 passed**。
- 额外结构化前后比较确认：规则 ID/type/target/tolerance/unit/weight 不变；schema 除 AR 新增可选 contact_summary 定义外，只新增解释性 description，不改既有成功/失败验证条件。历史 EF 结果继续满足两模式 schema，合成 bounded-failure 样例可如实保留未知值。
- 回归检查的是软件契约及旧输出的几何后处理，不冒称真实 LLM judge 已执行新评测，也没有进行新的量化计算或当前 starter 盲跑。
- 各包 `evaluation/task_provenance/maintenance_audit.md` 记录了修复依据和范围。未改 docs/verification、papers、canonical、第一批 final，也没有顺带处理本报告其他论文的档案清理建议。
