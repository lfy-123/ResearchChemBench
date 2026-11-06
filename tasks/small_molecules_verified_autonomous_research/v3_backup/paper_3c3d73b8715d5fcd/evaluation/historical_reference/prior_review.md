# paper_3c3d73b8715d5fcd｜评估任务说明

更新：2026-10-21，任务指令采用人工审定最终英文卡；评分保持 2026-10-20 专家第一轮修订。论文：Mechanistic Study of Cycloisomerization of 1,7-Allenenes and Guidance to Develop a [2 + 1 + 2] Reaction of 1,7-Allenenes with CO for Accessing cis- and trans-5/5 Skeletons。DOI：10.1021/jacs.5c17013。

政策：`paper_science_v2`；满分 100。中间科学结果 80 分、最终结论 20 分；数值规则 20 分、定性规则 80 分；共 8 个二元评分项。

## 1. 科学问题和范围（现行任务指令中文全文）

#### 科学问题

哪些催化过程解释了由所给 1,7-联烯-烯烃（allenene）模型与 Rh 催化剂生成环异构化产物及分子内 [2+2] 产物的过程，又是什么控制着二者的竞争？

#### 输入与范围

`data/inputs/system.json` 包含底物与产物的分子图、催化剂身份、溶剂与浓度约定。`data/inputs/rhodium_catalyst.xyz` 是催化剂的起始几何构型。产物图定义了需要解释的转化。简化的 O-连接底物没有实验产率数据集。

所需范围为这两类产物。不需要 CO 插入羰基化以及完整的实验催化剂物种分布。允许使用所给公开输入与通用科学/软件文档；私有评估方或计算参考、先前运行存档以及另一模式的指引被排除。

#### 所需结果

提供有计算支持、化学上相互连接的催化路径，在平衡参照上的定量能量比较，以及关于该竞争的结论。报告所提交结构、转化与动力学论断的化学身份、电子态、条件、单位、参照定义与可复现的有效性证据。指出不完整或未解决的结果。

#### 提交

按 `submission_schema.json` 与 `submission_guide.md` 提交 `report/results.json` 与 `report/report.md`，并附原生输入、输出、结构、执行记录与分析。

## 2. 输入与交付

| 当前文件 | 内容/作用 |
|---|---|
| [agent_input/data/inputs/rhodium_catalyst.xyz](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/agent_input/data/inputs/rhodium_catalyst.xyz) | 公开输入文件，详见文件内容 |
| [agent_input/data/inputs/system.json](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/agent_input/data/inputs/system.json) | 公开输入文件，详见文件内容 |
| [agent_input/submission_guide.md](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/agent_input/submission_guide.md) | 交付内容与证据要求 |
| [agent_input/submission_schema.json](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/agent_input/submission_schema.json) | 机器可读交付合同 |
| [agent_input/task.md](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/agent_input/task.md) | 当前公开任务指令英文原文 |

必须交付：`report/results.json`；`report/report.md`。

## 3. 本轮评分调整

endo/exo 差异项改为定性排序，仍为 10 分；不再强制命中 7.5±2.0 kcal/mol。

各新权重采用本轮确认的实施方案。endo/exo 项按专家意见取消原数值窗口，其余数值目标与容差保留。

## 4. 现行逐项评分

只对任务范围内的论文科学发现评分，绝不对研究过程、工具调用次数、成本、格式或失败说明评分。每一项均采用二元计分：有证据支持且相符时获得该项全部分值；结果错误或缺失时为零分。比较前，先确定分子、连接关系、原子组成、电荷/自旋、观测量、单位、参考态和条件。要求真实且已关联的受管理计算及原生文件；仅有所提供的观察结果、抄录的论文数值或正常终止标志是不够的。按未更改的公开任务要求验证最低点和过渡态。在物理结果可比较时，允许采用其他软件、方法和候选标签。不要求沿用历史验证轨迹、固定假设数量，也不要求开展公开范围之外的新计算。数值目标和已有容差不可调整。来源背景中没有给出容差的数字不构成新的数值门槛。不得自行设定容差，也不得将仅符号或排序一致视为定量幅度一致。必要的参考可比性尚未解决时，须标记为 needs_review。各独立项目分别评估；某个数值项目失败，不会自动取消有独立证据支持的定性结论。结论分要求明确、有证据支持的最终推断或选择，而不只是计算或列出一个相符的候选。

下列中文要求对应现行规则；[完整可执行评分文件](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/evaluation/scoring_rules.json)为英文原文。

| 评分项 | 类别 | 判定 | 分值 |
|---|---|---|---|
| endo 氧化环金属化中间节点 | 中间结果 | 定性 | 10 |
| 环异构化总活化自由能 | 中间结果 | 数值 | 20 |
| CO 解离连接节点 | 中间结果 | 定性 | 10 |
| β-H 消除节点 | 中间结果 | 定性 | 10 |
| 还原消除与产物释放节点 | 中间结果 | 定性 | 10 |
| 竞争 [2+2] 产物通道 | 中间结果 | 定性 | 10 |
| endo 起始过渡态低于 exo 的能量排序 | 中间结果 | 定性 | 10 |
| 最终：endo 起始及两种产物的竞争机制 | 最终结论 | 定性 | 20 |

每项具体要求：

### endo_ocm：endo 氧化环金属化中间节点（10 分）

规则：`r_endo_ocm`。

通过相互连接、组成及 CO 平衡的结构和有效的驻态证据，得到底物配位及 endo 氧化环金属化生成 η3 有机铑中间体的过程。INT1/INT2 是来源标签，并非强制要求的输出 ID。

论文依据：`main.pdf` PDF 第 3 页；`supplementary_001.pdf` PDF 第 39、41 页。

### overall_barrier：环异构化总活化自由能（20 分）

规则：`r_overall_barrier`。

得到相对于正文讨论中标识为 INT11 的实际静息态参考的环异构化总活化自由能。不得以相对于 INT1 的局部能垒 12.9 kcal/mol 或 CO 不平衡的参考态替代。

数值目标：`22.8`；容差：±2.0；单位：kcal/mol。

论文依据：`main.pdf` PDF 第 3 页；`supplementary_001.pdf` PDF 第 41、42 页。

### co_loss：CO 解离连接节点（10 分）

规则：`r_co_loss`。

建立从氧化环金属化中间体到下一催化剂状态的有效 CO 解离连接。在组成和能量参考中计入交换的 CO。已得到证明的等效连接可以接受；不要求沿用历史上失败的 IRC/QRC 轨迹。

论文依据：`main.pdf` PDF 第 3 页；`supplementary_001.pdf` PDF 第 41 页。

### beta_h：β-H 消除节点（10 分）

规则：`r_beta_h`。

在论文的环异构化通道内，建立相连的 β-H 消除过程，并具有适当的鞍点/振动模式或等效连接证据，以及一致的物种清单。来源中的局部值 6.0 kcal/mol 为背景信息，不构成新的数值门槛。

论文依据：`main.pdf` PDF 第 3 页；`supplementary_001.pdf` PDF 第 41 页。

### product_release：还原消除与产物释放节点（10 分）

规则：`r_product_release`。

得到生成环异构化产物的还原消除过程，以及化学上一致的催化剂再生/配体交换。来源中的局部值 8.9 kcal/mol 为背景信息；不得施加未经校准的幅度目标。

论文依据：`main.pdf` PDF 第 3 页；`supplementary_001.pdf` PDF 第 41 页。

### competing_22：竞争 [2+2] 产物通道（10 分）

规则：`r_competing_22`。

通过相连的分子证据和共同能量参考，得到从 OCM 中间体直接还原消除生成不同的 [2+2] 产物的过程。仅有产物存在是不够的。局部值 17.1 kcal/mol 不是环异构化总能垒。

论文依据：`main.pdf` PDF 第 3 页；`supplementary_001.pdf` PDF 第 41 页。

### endo_exo_gap：endo 起始过渡态低于 exo 的能量排序（10 分）

规则：`r_endo_exo_gap`。

比较同一底物/催化剂体系中正确归属的 endo 与 exo 氧化环金属化过渡结构，证明 endo 鞍点的吉布斯自由能更低。要求有效的鞍点/连通性证据，以及可比的组成、电荷/自旋、条件、热化学定义与能量参照。该项评价有证据支持的排序，不要求命中特定数值差；正文 7.5 和补充材料 7.2 kcal/mol 的讨论仅作背景。比较无关最低点或不守恒状态不能证明该排序。

论文依据：`main.pdf` PDF 第 3 页；`supplementary_001.pdf` PDF 第 35、41 页。

### competition_conclusion：最终：endo 起始及两种产物的竞争机制（20 分）

规则：`r_competition_conclusion`。

最终选择的机理采用 endo OCM，随后进入相连的环异构化和 [2+2] 分支，并通过平衡的自由能剖面解释两者的竞争可行性。Endo 起始步骤控制主路线；不得混淆局部能垒和总能垒，也不得从这个有限模型推断实验产物收率。不得将范围扩展至 CO 插入的 [2+1+2] 反应。

论文依据：`main.pdf` PDF 第 3 页。

## 5. 论文与已有验证依据

17物种、6鞍点、12端点；总体势垒22.739174对22.8差−0.060826；exo−endo鞍点差7.558220对7.5差+0.058220 kcal/mol，这是历史数值核对；现行仅总势垒保留 ±2 窗口，endo/exo 改为定性排序。TS3原生IRC失败，以双向QRC/端点证据验收。

[完整验证参考](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/evaluation/verified_computation_reference.md)保留实际方法、原生日志索引和历史。历史冻结/旧分值不覆盖现行规则。

PDF 页序从 1 开始。论文正文和补充材料保存在仓库 `papers/paper_3c3d73b8715d5fcd/documents/`，不复制到本审查目录。原生日志索引保留在验证记录中；本次没有重新进行量子化学计算。

## 6. 物理定义与验证边界

TS3 原生 IRC 曾失败，历史验证依靠双向 QRC/端点证据，不能表述为全部 IRC 成功。总体势垒 22.8±2.0 kcal/mol 的参照及 CO 组成守恒不变；endo/exo 现在只要求可比鞍点的正确排序，来源 7.5/7.2 不再形成数值门槛。

当前判据以本页和任务副本的评分文件为准，历史验证中的旧分值/规则不追加为要求。中间科学节点与最终结论都属于科学分，不包含过程分。

[参考关键点](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/evaluation/reference_key_points.json) · [参考结论](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/evaluation/reference_conclusions.json) · [来源映射](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/evaluation/evidence_map.json)

## 7. 验证结果、误差与专家待审事项（2026-10-21汇编）

**验收口径：** 当前有限反应网络的既有验收保留；关键能量差小。

**实际计算链：** 低层Gaussian 16 PW6B95-D3，非Rh 6-311G(d,p)、Rh def2-TZVP/ECP；气相Opt/Freq、同几何SMD(1,4-dioxane)单点、ORCA ωB97M-V/def2-QZVP高层单点。17物种、6鞍点，10条有限IRC与12端点；TS3用双向负模位移/QRC后优化。以E_high+Gcorr_low+(E_solv_low−E_gas_low)组装，并保持CO计量及浓度一致。

下表差值统一为计算值减论文值；保留原单位、物理定义与参照。没有作者对应标量的分析不编造误差。

| 对比量 | 论文/来源值 | 真实计算/分析值 | 差值及说明 |
|---|---:|---:|---|
| 总活化自由能 / kcal/mol | 22.8 | 22.739174 | −0.060826 |
| exo−endo / kcal/mol | 7.5 | 7.558220 | +0.058220 |
| [2+2]局部势垒 / kcal/mol | 17.1 | 17.053933 | −0.046067 |
| β-H局部势垒 / kcal/mol | 6.0 | 6.020002 | +0.020002 |
| 还原消除局部势垒 / kcal/mol | 8.9 | 8.915452 | +0.015452 |

**请专家判断：** 数值支持endo起始和两类产物竞争；总势垒在现行±2.0内，endo/exo在新规则中按排序。请专家按真实证据范围判断TS3替代连接证据；不得描述为所有IRC成功或全部催化循环、产率已复现。

本节是验收事实与审查意见，不修改第4节的评分规则，也不代表新增量化计算或专家发布批准。当前任务副本沿用人工审定版本；旧日志中的pending/冻结须按其日期、任务范围和评分版本阅读。

证据入口：[本包原计算参考](../tasks/autonomous_research/paper_3c3d73b8715d5fcd/evaluation/verified_computation_reference.md)（含原始输出、参数及历史验收索引）。
