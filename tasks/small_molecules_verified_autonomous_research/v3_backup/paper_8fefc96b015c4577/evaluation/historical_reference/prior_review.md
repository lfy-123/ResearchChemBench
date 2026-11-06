# paper_8fefc96b015c4577｜评估任务说明

更新：2026-10-21，任务指令采用人工审定最终英文卡；评分保持 2026-10-20 专家第一轮修订。论文：Unified Photoredox Strategy for Selective Access to Hydroisoquinoline and Benzosultam via Tether Modulation of Allylamine。DOI：10.1021/acs.orglett.5c04344。

政策：`paper_science_v2`；满分 100。中间科学结果 70 分、最终结论 30 分；数值规则 70 分、定性规则 30 分；共 3 个二元评分项。

## 1. 科学问题和范围（现行任务指令中文全文）

#### 科学问题

确定所给自由基的两条相互竞争的分子内芳基环化路径、它们相对于未环化最低点的吉布斯活化势垒及其能量排序。

#### 输入与范围

`data/inputs/system.json` 定义了 C21H24F2NO4S 自由基的完整身份与映射。`data/inputs/radical_starter.xyz` 是 53 原子的起始几何构型（单位 Å），不是优化后的最低点或过渡态。指定电荷为 0，多重度为 2。主模型使用隐式 DMSO、298.15 K 与 1 atm 下的谐振吉布斯自由能，势垒以 kcal/mol 为单位、相对于同一未环化自由基最低点。

光催化剂、乙酸锌、显式溶剂以及后续的氧化/芳构化被排除。其它条件为可选对照。私有评估方文件、历史验证存档以及通用网络检索被排除。

#### 所需结果

提供参照最低点以及两个经化学指认的环化过渡态、它们的吉布斯势垒与通道比较。有效性证据要求：参照为零个虚频模，每个过渡态为恰好一个与反应相关的虚频模；该反应相关模必须支持所指认的闭环。IRC 为可选。每个几何构型都要求其公开输入的原子映射；每个过渡态几何构型还要求其正在形成的 C–C 原子对与通道身份。

#### 提交

按 `submission_schema.json` 提交 `report/results.json`，并附所引用的原生计算与几何证据。`state_reference` 为未环化最低点；`state_candidate_1` 与 `state_candidate_2` 为未排序的通道标签。`barrier_difference` 为 candidate_2 减去 candidate_1。`atom_mapping` 对每个输出行给出一个从 1 开始的公开输入原子索引；成键索引指向输出行。报告软件、方法、基组、色散与热化学设置。`complete` 要求全部三个已验证状态与两个数值势垒；否则报告 `bounded_failure`，并指出可用证据与不可获得的结果。

## 2. 输入与交付

| 当前文件 | 内容/作用 |
|---|---|
| [agent_input/data/inputs/radical_starter.xyz](../tasks/autonomous_research/paper_8fefc96b015c4577/agent_input/data/inputs/radical_starter.xyz) | 公开输入文件，详见文件内容 |
| [agent_input/data/inputs/system.json](../tasks/autonomous_research/paper_8fefc96b015c4577/agent_input/data/inputs/system.json) | 公开输入文件，详见文件内容 |
| [agent_input/submission_schema.json](../tasks/autonomous_research/paper_8fefc96b015c4577/agent_input/submission_schema.json) | 机器可读交付合同 |
| [agent_input/task.md](../tasks/autonomous_research/paper_8fefc96b015c4577/agent_input/task.md) | 当前公开任务指令英文原文 |

必须交付：`report/results.json`。

## 3. 本轮评分调整

专家三项全部保留，35/35/30 分及原有容差不变。

各新权重采用本轮确认的实施方案。本轮未改变保留数值项的目标与容差。

## 4. 现行逐项评分

只对任务范围内的论文科学发现评分，绝不对研究过程、工具调用次数、成本、格式或失败说明评分。每一项均采用二元计分：有证据支持且相符时获得该项全部分值；结果错误或缺失时为零分。比较前，先确定分子、连接关系、原子组成、电荷/自旋、观测量、单位、参考态和条件。要求真实且已关联的受管理计算及原生文件；仅有所提供的观察结果、抄录的论文数值或正常终止标志是不够的。按未更改的公开任务要求验证最低点和过渡态。在物理结果可比较时，允许采用其他软件、方法和候选标签。不要求沿用历史验证轨迹、固定假设数量，也不要求开展公开范围之外的新计算。数值目标和已有容差不可调整。来源背景中没有给出容差的数字不构成新的数值门槛。不得自行设定容差，也不得将仅符号或排序一致视为定量幅度一致。必要的参考可比性尚未解决时，须标记为 needs_review。各独立项目分别评估；某个数值项目失败，不会自动取消有独立证据支持的定性结论。结论分要求明确、有证据支持的最终推断或选择，而不只是计算或列出一个相符的候选。

下列中文要求对应现行规则；[完整可执行评分文件](../tasks/autonomous_research/paper_8fefc96b015c4577/evaluation/scoring_rules.json)为英文原文。

| 评分项 | 类别 | 判定 | 分值 |
|---|---|---|---|
| 苄基连接芳环闭合势垒 | 中间结果 | 数值 | 35 |
| 芳磺酰侧芳环闭合势垒 | 中间结果 | 数值 | 35 |
| 最终：苄基侧环化更有利 | 最终结论 | 定性 | 30 |

每项具体要求：

### benzyl_barrier：苄基连接芳环闭合势垒（35 分）

规则：`r_benzyl_barrier`。

通过连接关系以及成键/负频模证据，识别苄基连接的芳基闭环，对应来源中的 TS2。计算 G(TS)−G(未环化自由基最低点)，条件为 298.15 K/1 atm、隐式 DMSO、电荷 0、双重态。验证最低点和相关的一阶鞍点；来源中的 −0.05 使用了不同的绘图能量零点，并非此处的能垒。

数值目标：`13.08`；容差：±1.5；单位：kcal/mol。

论文依据：`main.pdf` PDF 第 4 页；`supplementary_001.pdf` PDF 第 34、36、37、38 页。

### sulfonyl_barrier：芳磺酰侧芳环闭合势垒（35 分）

规则：`r_sulfonyl_barrier`。

通过连接关系以及成键/负频模证据，识别芳基磺酰基中的芳基闭环，对应来源中的 TS2-prime。采用相同的自由基参考态定义，并提供有效的鞍点证据。任意候选编号或最接近的能量不能用于确定身份。

数值目标：`19.25`；容差：±1.5；单位：kcal/mol。

论文依据：`main.pdf` PDF 第 4 页；`supplementary_001.pdf` PDF 第 34、36、40 页。

### cyclization_conclusion：最终：苄基侧环化更有利（30 分）

规则：`r_cyclization_conclusion`。

最终答案依据两个已映射且可比较的计算通道及其差值，选择苄基连接的芳基闭环作为比芳基磺酰基替代通道能垒更低的路径。排序相反、未作出选择或仅列出两者，均未得到该结论。不要求研究下游氧化/芳构化或催化剂循环。

论文依据：`main.pdf` PDF 第 4 页；`supplementary_001.pdf` PDF 第 36、38、40 页。

## 5. 论文与已有验证依据

B/TS2/TS2′三组B3LYP-GD3/def2TZVPP、SMD(DMSO)Opt/Freq，153模式分别0/1/1负模。势垒13.253000092/19.257010740对13.08/19.25；差+0.173000092/+0.007010740；共同参照差6.004010648。

[完整验证参考](../tasks/autonomous_research/paper_8fefc96b015c4577/evaluation/verified_computation_reference.md)保留实际方法、原生日志索引和历史。历史冻结/旧分值不覆盖现行规则。

PDF 页序从 1 开始。论文正文和补充材料保存在仓库 `papers/paper_8fefc96b015c4577/documents/`，不复制到本审查目录。原生日志索引保留在验证记录中；本次没有重新进行量子化学计算。

## 6. 物理定义与验证边界

两势垒保留 ±1.5 kcal/mol 窗口。必须有有效鞍点及相关模式/连通性证据，共同参照为未环化自由基；源坐标或计算正常结束不等于发现通道。

当前判据以本页和任务副本的评分文件为准，历史验证中的旧分值/规则不追加为要求。中间科学节点与最终结论都属于科学分，不包含过程分。

[参考关键点](../tasks/autonomous_research/paper_8fefc96b015c4577/evaluation/reference_key_points.json) · [参考结论](../tasks/autonomous_research/paper_8fefc96b015c4577/evaluation/reference_conclusions.json) · [来源映射](../tasks/autonomous_research/paper_8fefc96b015c4577/evaluation/evidence_map.json)

## 7. 验证结果、误差与专家待审事项（2026-10-21汇编）

**验收口径：** 本包人工审定窄版的两竞争势垒在原±1.5窗口内。另有主队列两底物升级AR于10月20日暂定定性通过；两个版本不可混为同一评分任务。

**实际计算链：** 本包B/TS2/TS2′均由Gaussian16、B3LYP-D3/def2-TZVPP、SMD(DMSO)Opt/Freq所得，153模分别0/1/1虚频，检查连接身份与负模反应方向。主队列扩展验证还覆盖长链SMD(DCE)，共14份日志，8最低点/6TS；不是新增完整光循环或全部IRC。

下表差值统一为计算值减论文值；保留原单位、物理定义与参照。没有作者对应标量的分析不编造误差。

| 对比量 | 论文/来源值 | 真实计算/分析值 | 差值及说明 |
|---|---:|---:|---|
| 本包苄基闭环势垒 / kcal/mol | 13.08 | 13.253000092 | +0.173000092 |
| 本包芳磺酰闭环势垒 / kcal/mol | 19.25 | 19.257010740 | +0.007010740 |
| 本包竞争势垒差 / kcal/mol | 6.17 | 6.004010648 | −0.165989352 |
| 扩展AR长链芳磺酰势垒 / kcal/mol | 17.44 | 17.440998 | +0.000998 |
| 扩展AR长链苯乙基势垒 / kcal/mol | 17.96 | 17.948026 | −0.011974 |

**请专家判断：** 该篇不是大数值偏差案例；扩展版四势垒最大差0.173、12量最大差0.419963 kcal/mol。长链只有0.507028 kcal/mol小偏好，不支持排除另一途径或精确产率。本包仍保留人工审定的单底物窄版及三条评分；扩展结果仅补充归档，不增加本包必评项。

本节是验收事实与审查意见，不修改第4节的评分规则，也不代表新增量化计算或专家发布批准。当前任务副本沿用人工审定版本；旧日志中的pending/冻结须按其日期、任务范围和评分版本阅读。

证据入口：[本包原计算参考](../tasks/autonomous_research/paper_8fefc96b015c4577/evaluation/verified_computation_reference.md)（含原始输出、参数及历史验收索引）。

[专项验收/独立审查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/closeout_followup_20261020T1530Z/review_8fef/独立验收审查.md)。
