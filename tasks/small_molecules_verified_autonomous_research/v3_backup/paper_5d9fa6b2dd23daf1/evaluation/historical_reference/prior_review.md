# paper_5d9fa6b2dd23daf1：金刚烷基化反式成环与酸/磺酰胺能量比较

**当前状态确认（2026-10-23）：用户接受本篇当前科学问题的验证结果，数值差异保留专家审查。** 要求相关结果已实际计算且结论一致；本确认不等于所有数值窗口通过、全文复现或自动发布。下方差值、方法差异和原始证据继续保留。

更新：2026-10-22。当前自主科研范围定性验收通过；本页对应现行科学分V2私有规则。

## 1. 科学问题和范围

### 科学目标

什么分子路径可以解释指定内部E-烯基酸形成所观察到的反式金刚烷基化内酯？在TfOH/HFIP中，相应反应的能量学与指定磺酰胺连接的E-烯烃相比如何？

使用`data/inputs/system.json`获取(E)-己-3-烯酸、E-烯基磺酰胺、金刚烷-1-醇、TfOH、HFIP及两种已观察到的反式产物的完整结构。在HFIP、293.15 K下比较反应能量。制备实验的室温观察应与精确指定的计算温度区分。

研究一条有化学证据支持、通向所观察到产物连接关系和相对反式立体化学的路径，并比较两种转化的能量可及性和热力学。任一互为镜像的反式产物均可接受。产物身份是需要解释的观察结果。定量反式/顺式势垒差、穷尽排除所有机理、端烯化学及论文完整的1,1/1,2底物范围不属于本任务。验证通向反式产物的路径，本身并不能量化它相对于未计算顺式路线的选择性。

### 研究与交付

提出可检验的解释，选择能够提供信息的分子模型和方法，并实际执行支持你的主张所需的研究。假设和计算方法由你选择。将实际输入、输出、日志和分析保存在`research/`下；仅有方案或给定观察不能解决问题。不要求固定工具顺序、构象数量或完整催化网络。

说明结构、立体化学映射、质子化状态、总电荷和多重度、溶剂、温度、能量定义以及参考态记账。有关过渡态的主张需要适当的频率和化学连接验证。定量动力学主张需要方程、假设以及与可观测量的对应关系。根据实际提出的主张选择可靠性检查，并区分得到支持的内容和仍未解决的内容。

遵循`submission_schema.json`和`submission_guide.md`。提交`report/results.json`、`report/report.md`和`research/`，将假设、研究、证据、结论和实际产物关联起来。将数值结果及其定义和条件写入`evidence[].quantities`。报告实际资源使用及尚未确定的来源或实现选择。研究状态和问题解决状态相互独立。诚实的部分工作或失败可以获得过程分，但不能确立未计算的科学结果。在所主张的范围得到支持，或有记录的限制阻止进一步合理推进时停止；不设固定资源配额。

## 2. 输入、交付与来源索引

- [公开英文完整任务指令](../tasks/autonomous_research/paper_5d9fa6b2dd23daf1/agent_input/task.md)。第1节为该文件完整中文直译，不插入分析。
- [agent_input/data/inputs/system.json](../tasks/autonomous_research/paper_5d9fa6b2dd23daf1/agent_input/data/inputs/system.json)
- [agent_input/submission_guide.md](../tasks/autonomous_research/paper_5d9fa6b2dd23daf1/agent_input/submission_guide.md)
- [agent_input/submission_schema.json](../tasks/autonomous_research/paper_5d9fa6b2dd23daf1/agent_input/submission_schema.json)

论文目标和验证结果属于私有审查材料，不能随公开输入发给被评估Agent。正文/SI在单独来源ZIP内，按`papers/<paper_id>/documents/`排列。来源文件SHA-256和1-based PDF页序见任务的`evaluation/evidence_map.json`。

## 3. 计算验证、论文对照与误差

### 方法、模型与计算步骤

论文：*Catalytic 1,2- and 1,1-Carbocyclization of Alkenes Employing Adamantanols as Tertiary Carbocation Precursors*，DOI：10.1002/anie.202524449。正文PDF第8–9页Scheme 7及其讨论，SI PDF/印刷S79–S81的§7.3、Figure S3、Table S21是主要来源。全论文另有端烯和其他醇底物，不作为本题的额外要求。

|项目|作者说明|验证实际处理|一致性与限制|
|---|---|---|---|
|结构/频率|B3LYP/def2-TZVP|同方法，来源结构和必要的驻点/端点核验|核心物种完整；不是从头盲搜全部构象|
|单点与G构造|M06/def2-TZVP；M06溶剂电子能+B3LYP热项|逐物种用自身电子能与热项组合|未借用作者热项填补失败计算|
|溶剂|SMD HFIP，ε=16.70，其余参数取2-propanol|沿用同一构造|相同连续介质重构，不是显式HFIP溶剂壳|
|温压|293.15 K、1 atm|相同|室温制备观察不等于精确计算温度|
|热项环境|方法文字描述溶剂优化/频率，S21脚注却称气相热项|明确采用HFIP谐频热项|**来源内部歧义未消除，不能称所有隐藏设置完全相同**|
|软件|Gaussian16 A.03|Gaussian16 C.01|修订版不同；不能将残差全归因为版本|
|连接|作者协同亲电环化；TS保留O–H/N–H|源TS反应模、有限下坡和有效产物/片段|未重做完整全IRC或去质子化势垒；未收敛反向超分子不作热化学最低点|

独立核收读取29份原生日志并复算8个原参考量。新增磺酰胺路径质子化产物为61原子/+1单重态、177个正频率，最低22.5973 cm⁻¹；源TS唯一虚频−138.5952 cm⁻¹，局部反向得到正确Ad+和E-磺酰胺片段。移除保留N–H质子后的重原子连接与中性trans产物对应。反向超分子优化不收敛的日志仍是失败，使用独立合格片段的热项；酸路径和已有中性trans产物证据复用。

### 数值误差

单位kcal/mol，差值为实算−作者。两条TfOH构象参照均保留；不挑选更接近作者的一条。

|量及参照|作者|计算|差值|
|---|---:|---:|---:|
|醚形成完整profile|1.4|1.455474841|+0.055474841|
|Ad+形成profile，TfOH minus|2.7|4.221605001|+1.521605001|
|Ad+形成profile，TfOH plus|2.7|4.221618179|+1.521618179|
|酸环化TS完整profile，minus|15.7|17.194380069|+1.494380069|
|酸环化TS完整profile，plus|15.7|17.194393247|+1.494393247|
|磺酰胺环化TS完整profile，minus|12.9|14.422993262|+1.522993262|
|磺酰胺环化TS完整profile，plus|12.9|14.423006440|+1.523006440|
|酸局部环化势垒|13.0|12.972775068|−0.027224932|
|磺酰胺局部环化势垒|10.2|10.201388261|+0.001388261|
|中性内酯净生成G|−12.3|−12.309483874|−0.009483874|
|中性含氮环净生成G|−12.1|−12.116446272|−0.016446272|

完整起点为G0(X)=G(AdOH)+G(X)+G(TfOH)+G(HFIP)。醚、离子、TS和产物均使用相同原子/质子/电荷账本。局部势垒是TS−Ad+−X；净产物量为产物+H2O−AdOH−X。自算完整图采用自身离子参考4.221605/4.221618，未把作者2.7拼入自算图。旧8项窗口均为±2.0，全部通过；这说明当前量值比较成立，不消除方法歧义。

### 定性结论与验收

|来源科学判断|独立计算|当前判断|
|---|---|---|
|协同亲电环化可生成指定trans五元产物|两类TS/局部连接、有效端点及trans映射支持|支持有限trans成环路径；不证明相对于cis的定量选择性|
|磺酰胺比酸更易环化|局部势垒10.201388 < 12.972775，差2.771387|方向一致|
|两净成环反应放能|−12.309484及−12.116446|方向一致；不把两者约0.2差当可靠产物排序|

AR/PR共享科学问题均登记PROVISIONAL_PASS_QUALITATIVE；当前核心数值也落在原窗。没有宣称全文所有步骤、催化循环、cis竞争、精确速率或收率复现。

原生输入/输出及哈希可由[独立审查](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_progress_resume_20261022T013509Z/5d9_parent_review/独立验收.md)定位；[随包验证参考](../tasks/autonomous_research/paper_5d9fa6b2dd23daf1/evaluation/verified_computation_reference.md)保留最新验收与全部历史。此次整理复用已验收计算，没有新提交HPC计算。

## 4. 逐项评分

### 通用科学要求（现行原文）

只评价公开任务范围内的科学结果。每个叶子项满足全部条件得满分，否则为0，不即兴按比例给分。中间发现与最终解释独立评价；最终项要求明确采用且有计算支持的综合结论，不能仅列出候选。先核分子连接、原子库存、电荷/自旋、物理量、单位、参照、温度、溶剂与标准态。结果须有可定位的实际计算及原生产物支持；题面给定观察、复制论文数字、正常退出或正确措辞本身不能得分。最低点、过渡态及连接的证据要求以实际主张为准，允许科学等价的连接检验和计算方法；不强制复刻验证者软件、搜索轨迹、构象数量或全IRC。普通失败及缺失只影响对应项，不清零独立有效结果；伪造或隐藏答案泄漏按有效性规则处理。不奖励过程、调用数、效率、资源投入或失败诊断。定量项按固定目标和包含边界的绝对容差判断，Judge不得临时调整；定量不通过不自动否定独立定性项，定性方向不能代替定量命中。无容差的上下文数字不是额外门槛。真实物理不可比且无法澄清时需复核。所有规则仅在evaluator侧，不向agent泄漏作者机理或数值。

### 证据无效条件（现行原文）

**fabricated_evidence**：伪造计算执行或数值证据。 触发：有明确证据确认伪造计算执行、日志或结果，或将复制的私有参考值冒称独立实算；普通误判、收敛失败或缺失本身不等于伪造。 处理：确认伪造时按invalid_submission处理，提交无效；诚实失败只使受影响科学项失分，其他独立有效项保留。

**hidden_answer_leakage**：将未公开的答案或私有参考冒充独立发现。 触发：确认提交依赖未经公开提供的evaluator答案或隐藏原生参考，并冒称自主计算结果。 处理：确认未经授权使用隐藏答案时按invalid_submission处理；公开PR指导本身不构成泄漏。物种/单位错误、普通缺项只影响对应项，不自动全题清零。

### 1. acid_trans_connection — 15分（中间关键节点）

**评分项：** 酸底物的C–C成键和内酯trans闭环

**完整规则（r_acid_trans_connection）：** 实际分子结构与反应连接证据支持指定E-己-3-烯酸与金刚烷基亲电中心形成C–C键，并由羧基氧闭合为给定五元内酯，乙基/金刚烷基为trans相对构型。作者参考为保留酸性质子、总电荷+1单重态的协同环化TS；反应模和局部连接需对应这些成键事件，并将质子化端点与中性目标产物按原子/质子配平对应。允许科学等价的连接证据，不强制完整IRC或去质子化TS；题面给定产物、单一正确距离或正常结束本身不够。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_MAIN, E_PROFILE, E_COORD`。

### 2. sulfonamide_trans_connection — 15分（中间关键节点）

**评分项：** 磺酰胺底物的C–C成键和trans含氮闭环

**完整规则（r_sulfonamide_trans_connection）：** 实际结构与局部反应连接支持完整指定E-烯基磺酰胺的C–C成键及N–C五元环闭合，得到给定N-对甲苯磺酰基吡咯烷的trans乙基/金刚烷基关系。作者TS保留N–H质子、总电荷+1单重态，必须合理对应质子化端点与中性产物；未收敛超分子不能冒充最低点，但有效反应模、有限下坡及独立合格片段可构成相称证据。不要求完整催化循环或cis竞争。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_MAIN, E_PROFILE, E_COORD`。

### 3. acid_local_barrier — 10分（中间关键节点）

**评分项：** 酸底物局部环化Gibbs势垒

**完整规则（r_acid_local_barrier）：** G(TS1–3a)−G(Ad+)−G(1a)=13.0 kcal/mol，绝对容差2.0，边界包含。核对HFIP、293.15 K、1 atm及+1单重态反应组分、保留酸质子；TS必须具有对应成键的鞍点/连接证据。此量不是完整AdOH起点图的15.7；不能混入作者离子能2.7与自算局部量拼接。溶剂热项重构需明确，物理等价标准态/单位换算允许，不接受拟合偏移。

**数值合同：** target=13.0；tolerance=2.0；unit=kcal/mol；边界包含。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_MAIN, E_PROFILE, E_METHOD, E_ENERGY`。

### 4. sulfonamide_local_barrier — 10分（中间关键节点）

**评分项：** 磺酰胺底物局部环化Gibbs势垒

**完整规则（r_sulfonamide_local_barrier）：** G(TS1–3s)−G(Ad+)−G(1s)=10.2 kcal/mol，绝对容差2.0，边界包含。核对HFIP、293.15 K、1 atm、完整E-磺酰胺和保留N–H质子的+1单重态TS及其实际鞍点/连接证据。此量不是完整AdOH起点图的12.9；能量全部来自一致的自算账本，不混用作者离子形成能与自算局部能。透明物理等价换算允许。

**数值合同：** target=10.2；tolerance=2.0；unit=kcal/mol；边界包含。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_MAIN, E_PROFILE, E_METHOD, E_ENERGY`。

### 5. acid_product_energy — 5分（中间关键节点）

**评分项：** 内酯净生成Gibbs自由能

**完整规则（r_acid_product_energy）：** G(trans内酯3a)+G(H2O)−G(AdOH)−G(E-烯基酸1a)=−12.3 kcal/mol，绝对容差2.0，边界包含。使用HFIP、293.15 K、1 atm的有效中性单重态最低点及一致热项；完整账本中TfOH/HFIP作为守恒旁观组分相消。质子化产物、离子对能或任意较低构象不能未经身份说明替代该净反应量。

**数值合同：** target=-12.3；tolerance=2.0；unit=kcal/mol；边界包含。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_PROFILE, E_METHOD, E_ENERGY`。

### 6. sulfonamide_product_energy — 5分（中间关键节点）

**评分项：** 含氮环产物净生成Gibbs自由能

**完整规则（r_sulfonamide_product_energy）：** G(trans N-对甲苯磺酰基吡咯烷3s)+G(H2O)−G(AdOH)−G(E-烯基磺酰胺1s)=−12.1 kcal/mol，绝对容差2.0，边界包含。使用HFIP、293.15 K、1 atm的有效中性单重态最低点；保留完整底物、原子和质子账本，不能用保留额外N–H的阳离子端点直接替代中性净产物。

**数值合同：** target=-12.1；tolerance=2.0；unit=kcal/mol；边界包含。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_PROFILE, E_METHOD, E_ENERGY`。

### 7. trans_pathway_answer — 20分（最终结论）

**评分项：** 最终：以亲电成环解释两类trans产物

**完整规则（r_trans_pathway_answer）：** 最终以实际连接和结构证据，将金刚烷基亲电成键、羧基氧或磺酰胺氮闭环与两给定trans产物联系为化学配平的路径解释。作者协同亲电环化是参考答案；科学等价且有实际证据的物理解释可接受，不能只复述产物或罗列候选。需要解释相对trans构型，不能由仅有trans路线声称已量化trans/cis选择性，也不要求证明唯一机制或完整催化循环。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_MAIN, E_PROFILE, E_COORD`。

### 8. energetic_comparison_answer — 20分（最终结论）

**评分项：** 最终：磺酰胺较易环化且两净转化放能

**完整规则（r_energetic_comparison_answer）：** 最终在一致物理参照下，由实际势垒和净反应热力学判断磺酰胺局部环化比酸底物更容易、两类净产物形成均放能，并把该比较用于回答给定体系的可及性问题。数值是否落入独立窗口不代替排序与符号；数值超窗也不自动取消有证据的定性结论。不把完整曲线高度当局部势垒、离子形成能当活化势垒，或把小的0.2 kcal/mol产物差当鲁棒排序；不由此推断精确实验速率/产率。

**绑定：** `report/results.json, report/report.md`；字段`$`。核对实际分子/电子态、参照、单位与执行证据；仅评价本项科学命题，满足全部条件得满分，否则0。 关联证据：`E_MAIN, E_PROFILE, E_ENERGY`。

## 5. 分值理由、版本变化与专家待审

两种成环连接各15分，强调是否真正解释了所给trans产物；局部势垒各10分，直接服务于底物可及性比较；净产物能各5分，提供热力学尺度。最终路径解释与跨底物能量解释各20分，要求采用并整合实际结果，而非仅算出候选。4个定量项共30分，定性结构/最终解释共70分。

旧8个量中，醚/离子形成能和完整profile继续保存在验证表，未被隐藏或改数；它们不是额外过程分。相对于本题核心比较，局部势垒与净产物G更直接；同时评分局部值、离子参照和派生TS图高度会重复奖励同一账本。本版不再将这些派生/前置量各自设独立分。原±2.0窗口未扩大，不按实算残差拟合。

待专家判断：HFIP/气相热项文字冲突对数值可比性的影响；有限连接是否足以支持题面的trans路径；当前权重和±2.0是否合理；不能将trans路径支持误解为cis排除。题面原文中的“论文”“过程分”在本轮按迁移指南逐字保留，译文忠实反映；现行评分无过程分。若未来清理公开措辞，应单独授权版本修订，不能改本次受保护输入。

当前可按V2规则评分；不代表实际Agent已获100分或专家已批准发布。第4节直接列出现行中文规则原文，分析只放本节与第3节。

## 6. 论文—验证—评分对应表

|科学评分项|分数|论文证据ID|验证支持与物理限制|
|---|---:|---|---|
|acid_trans_connection：酸底物的C–C成键和内酯trans闭环|15|E_MAIN：main.pdf PDF 8,9；E_PROFILE：supplementary_001.pdf PDF 80；E_COORD：supplementary_001.pdf PDF 81,82,83,84,85,86,87,88,89,90,91,92|既有酸环化有效TS/局部连接与trans内酯图；不声称计算cis路径。|
|sulfonamide_trans_connection：磺酰胺底物的C–C成键和trans含氮闭环|15|E_MAIN：main.pdf PDF 8,9；E_PROFILE：supplementary_001.pdf PDF 80；E_COORD：supplementary_001.pdf PDF 81,82,83,84,85,86,87,88,89,90,91,92|TS唯一−138.5952 cm⁻¹；新质子化产物177正模；反向片段核实，失败超分子不作最低点。|
|acid_local_barrier：酸底物局部环化Gibbs势垒|10|E_MAIN：main.pdf PDF 8,9；E_PROFILE：supplementary_001.pdf PDF 80；E_METHOD：supplementary_001.pdf PDF 79,80；E_ENERGY：supplementary_001.pdf PDF 81|12.972775068对13.0，差−0.027224932；Ad+加酸的局部参照，不用17.194380完整高度。|
|sulfonamide_local_barrier：磺酰胺底物局部环化Gibbs势垒|10|E_MAIN：main.pdf PDF 8,9；E_PROFILE：supplementary_001.pdf PDF 80；E_METHOD：supplementary_001.pdf PDF 79,80；E_ENERGY：supplementary_001.pdf PDF 81|10.201388261对10.2，差+0.001388261；完整含N–H的+1 TS。|
|acid_product_energy：内酯净生成Gibbs自由能|5|E_PROFILE：supplementary_001.pdf PDF 80；E_METHOD：supplementary_001.pdf PDF 79,80；E_ENERGY：supplementary_001.pdf PDF 81|−12.309483874对−12.3，差−0.009483874；中性产物加水的净G。|
|sulfonamide_product_energy：含氮环产物净生成Gibbs自由能|5|E_PROFILE：supplementary_001.pdf PDF 80；E_METHOD：supplementary_001.pdf PDF 79,80；E_ENERGY：supplementary_001.pdf PDF 81|−12.116446272对−12.1，差−0.016446272；不以质子化端点代替中性产物。|
|trans_pathway_answer：最终：以亲电成环解释两类trans产物|20|E_MAIN：main.pdf PDF 8,9；E_PROFILE：supplementary_001.pdf PDF 80；E_COORD：supplementary_001.pdf PDF 81,82,83,84,85,86,87,88,89,90,91,92|两类成键/闭环及trans构型支持所选亲电成环解释；不证明机理唯一、cis排除或精确选择性。|
|energetic_comparison_answer：最终：磺酰胺较易环化且两净转化放能|20|E_MAIN：main.pdf PDF 8,9；E_PROFILE：supplementary_001.pdf PDF 80；E_ENERGY：supplementary_001.pdf PDF 81|局部酸−磺酰胺=2.771387；两净G均负。两产物约0.2差不作为鲁棒排序。|


## 7. 输入保护与副本一致性

本轮仅修改新维护副本的私有evaluator和包清单，源任务未修改，`agent_input/**`、`task_info.json`、`paper_route.md`逐字节保持。专家任务副本与维护目录逐文件一致。受保护文件SHA-256：

- `agent_input/data/inputs/system.json` — `684b42dc520e3a18134a9ee0a097dfd72054c5d3a45cef07f24713e87cb58383`
- `agent_input/submission_guide.md` — `d7566f930a431e635f12527754c70fe5105265823a4f043a4e26a8e1d87f65d6`
- `agent_input/submission_schema.json` — `5987725856edc7bd37248523d779e2793b7be64758917f3bd40babc8a3bb91de`
- `agent_input/task.md` — `70f9ebb26cab0adfce847fdba7dcb0edbfbdea2aca64b027a3ec2239a115b6f7`
- `paper_route.md` — `4e843281401eb927c1189eb076347016206deb07ae82f64c6388fc0624e41eda`
- `task_info.json` — `25595b0e4052d3093e63f10a1fdab4d8d735af4be1c8b8c617b09099a28ff665`
