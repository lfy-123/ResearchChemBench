# 第 4 批：局部竞争路径与动力学——开发升级交付报告

交付日期：2026-09-27；封存核对时间：2026-09-27T13:42:30.945666+00:00。

本批 16 篇、32 个 AR/PR 开发包已完成实质升级并通过官方包、运行时、公开导出和提交契约检查。升级后为 9 篇 B、7 篇 C；15 篇状态为 `implemented_pending_expanded_reference`，1 篇动力学任务 `paper_60f4c45810428116` 保持 `blocked`。这些状态是开发交付状态，不表示扩展科学目标已经验证通过。

本轮新科学计算为 0，量化引擎启动为 0，未运行付费 LLM 科学裁判校准。已完成源 PDF/SI 实质段落及选定图表核对、已有结果复核、分子图/化学计量检查、公开观测转录及软件契约测试。合成提交只在临时目录用于格式回归，均标记为非科学数据。

## 实施与评估契约

每篇 AR/PR 从相应现行 final 包复制；旧文件逐字节保存为私有 `evaluation/legacy_final_snapshot/*.snapshot`，来源、文件哈希、源指导文档和所读 PDF 页码写入 `upgrade_audit.json`。旧 PASS 与旧狭窄标量未作为新版本完成声明。

AR/PR 的科学目标、可用对象、公开数据、submission_schema/guide 和五份科学 evaluator 保持一致；task.md 仅 PR 多出作者假设、源路线/方法与本次新增干预的区别。AR 移除会泄露待判终态的作者产品/中间体答案坐标，保留足够的映射连接与独立构建输入。

所有任务要求 `report/results.json` 和 `report/report.md`；新增研究矩阵包含具体行/列、数值、能量零点、电子/热校正/Gibbs 分项、路径模式/双向端点与原始产物路径。评分共 100 分：身份/基准 10，逐篇三个科学面板 30/25/15，稳健性 10，结论 10。五份 evaluator 的规则直接绑定对应结果字段与原始证据。

支持、反驳及证据充分的不可区分结果等价对待。实证坍缩/无独立极小点有专门分支，不强制虚构不存在的能垒。核心对照缺失、错误对象/态/零点、仅旧标量、失败冒充完成会失去相关完成信用。顶部 optional 内容未升级为核心失败条件。新增参考和误差界限须由真实新计算校准，没有机械沿用旧 ± 范围。

已修复监督指出的两个共性问题：路径拒绝 `..` 越界并允许合法 `./`；前置输入或环境阻塞允许 `calculation_records=[]`、空实际方法与零科学资源的 `pre_engine` 诊断提交，同时要求诊断文件、原因和缺失端点。该失败分支不能携带声称完成的矩阵/科学支持结论；完整分支仍要求真实计算记录和全部核心面板。

## 检查范围及其限制

四个检查分片共执行 3870 个命名断言，去重后 2757 个，全部通过。重复项来自全批化学图检查和仓库加载；去重规则按测试名且要求结果完全一致。32 个测试时包哈希在汇总时再次与官方 `package_payload_entries`/`package_content_hash` 计算值一致。

检查使用 `.envs/researchchembench/bin/python` 和 `TaskRepository(roots=[Path('tasks/upgrade_tasks')])`，没有改变默认正式库发现机制。覆盖 JSON/JSON Schema、validate_task_package、load_runtime_evaluation、权重 100、materialize 精确公开清单且不导出 evaluator/快照、AR/PR 同科学与公开数据、源快照、完整/反驳/不可区分/坍缩/诚实失败正例及逐篇缺面板、缺端点、错误显式态、旧标量、路径越界等反例。

这些是包和提交传输/结构检查，不会因合成样例被 schema 接受就授予科学 PASS。数值范围内但物理错误的自旋、伪造日志、错误能量参考等仍须科学 evaluator 检查原始输出；本轮没有把语义规则校准伪装成执行过的数值验证。

来源完整性另核对 462 对 source/snapshot 和 513 个去重来源文件；范围限定为各包审计列出的 final、源 PDF 与指导文档，详见 [source_integrity.json](source_integrity.json)。

复跑入口为 `check_batch.py --shard 1` 至 `--shard 4`，再执行 `finalize_batch.py`。仅在本批仍由当前实施负责人持有写权时重新生成；移交后如监督已改包，旧测试哈希不匹配会使汇总失败，必须对新版本重新检查。

## 逐篇交付

### 1. paper_3235db287859287e

**范围与状态：** A→C：从两个 E/Z 终点自由能转为底物氧/外源水氧、自由基/离子局部竞争路径；纳入同位素原子追踪及 OH-Boc 保护控制。提供 1a、苯硫酚、碘物种、水和保护底物的映射图。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 PDF 5–7 页 Scheme 3 的氧标记和保护控制是公开实验约束。反应物应为 benzenethiol，而非名称混淆的 benzylthiol。SI 100 页给出 SMD-MeCN 与分元素基组；没有从缺失文字猜测泛函。

- [main.pdf](../../../../papers/paper_3235db287859287e/documents/main.pdf)：PDF 物理页 5、6、7；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_3235db287859287e/documents/supplementary_001.pdf)：PDF 物理页 94、95、96、97、98、99、100；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.paths`（30 分）；`$.results.oxygen_tests`（25 分）；`$.results.path_comparison`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧 E/Z 自由能仅能作为同约定端点核对，不能验证氧转移或动力学。

**可实施先导和未完成参考：** 先独立构建一个底物氧自由基序列和一个外源水氧/离子竞争序列，核对碘、质子、电子库存；再补 OH 保护干预和两套同位素映射，取完整多段路径的有效最大能垒。

**拒绝项、公平替代结论及限制：** 拒绝只交 E/Z 标量与同位素文字；原子守恒且满足观测约束的替代路线可以反驳作者。新路径和方法敏感性尚未计算。

**检查：** 185 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_3235db287859287e/agent_input/task.md)；[PR task](../../paper_reproduction/paper_3235db287859287e/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_3235db287859287e/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_3235db287859287e/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_3235db287859287e/evaluation/task_provenance/upgrade_audit.json)。

### 2. paper_4e9774f4128551d3

**范围与状态：** A→C：删除公开产品坐标，保留独立构建所需的映射连接；C6/C47/O52 定义 O-TMS 烯醇前体，双面质子化×两个 CSA 对映体，包含预组织代价与混合溶剂敏感性。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 Scheme 5 与 SI 20–21 页的 THF/MeOH 比例分别为 1:1 和 10:1，已明示冲突。主模型采用 THF 连续介质加一分子 MeOH，溶剂敏感性单独报告。构图检查确认 C23H38O3Si 和 CSA 对映体对。

- [main.pdf](../../../../papers/paper_4e9774f4128551d3/documents/main.pdf)：PDF 物理页 5、6；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf)：PDF 物理页 20、21、71、73、76；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.facial_paths`（30 分）；`$.results.facial_comparison`（25 分）；`$.results.racemate_control`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧 S20/50 产品自由能只能用于端点热力学，不能替代双面质子化势垒或外消旋酸加权。

**可实施先导和未完成参考：** 从映射烯醇-TMS、一个 CSA 对映体和一分子 MeOH 开始，验证两面进攻与共同零点预组织代价，再完成第二酸对映体或严格对称映射、外消旋加权和溶剂对照。

**拒绝项、公平替代结论及限制：** 拒绝以产品稳定性作面选择性、无依据省去反离子或酸对映体；完成全部路径后接近零的加权差异可接受。源混合比例冲突已公开。

**检查：** 174 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_4e9774f4128551d3/agent_input/task.md)；[PR task](../../paper_reproduction/paper_4e9774f4128551d3/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_4e9774f4128551d3/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_4e9774f4128551d3/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_4e9774f4128551d3/evaluation/task_provenance/upgrade_audit.json)。

### 3. paper_60f4c45810428116

**范围与状态：** A→B，blocked：完成有限生成/回淬/重排/捕获 ODE、独立参数区间、可辨识性和三个整条件留出契约。人工逐格核对 SI Table S2，补全 25 个位置、23 个实测点及两个堵塞点，保留 trace/n.d. 分类。 状态 `blocked`。

**正文/SI 实质依据：** SI 5–7 页确认两段流量、稀释、2.4 s 捕获段和副产物 3a=2-methylbenzenemethanethiol。补供对应 thiolate/thiol 图，修正重排通道。SI 6 页为 RBF 插值，并非机理速率拟合。

- [main.pdf](../../../../papers/paper_60f4c45810428116/documents/main.pdf)：PDF 物理页 2、3、5；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_60f4c45810428116/documents/supplementary_001.pdf)：PDF 物理页 3、4、5、6、7、19、22；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.network`（30 分）；`$.results.identifiability`（25 分）；`$.results.holdout`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧还原电势只约束还原热力学；SI 实测网格及其删失分类可用。RBF 曲面不能提供独立机理速率。

**可实施先导和未完成参考：** 解除阻塞需独立生成/回淬/重排/捕获速率区间或经过验证的势垒，以及回淬终态的电荷/电子账本。随后才校验 ODE 守恒、混合稀释、三个完整条件留出和共享温度参数的可辨识性。

**拒绝项、公平替代结论及限制：** 当前 blocked。已补真实观测，但没有臆造速率区间、检测下限或回淬物种。拒绝每个格点独立拟合、留出泄漏及把 trace/n.d./堵塞视为测得零；解除输入阻塞后证据充分的秩亏结论允许。

**检查：** 181 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_60f4c45810428116/agent_input/task.md)；[PR task](../../paper_reproduction/paper_60f4c45810428116/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_60f4c45810428116/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_60f4c45810428116/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_60f4c45810428116/evaluation/task_provenance/upgrade_audit.json)。

### 4. paper_db6c4e0558113873

**范围与状态：** A→C：CuIII(acac)(allyl)Cl 两种立体出口与匹配自由基的直接 Cl 原子转移比较；补齐 allenoate 6b、PhSO2Cl、acac、自由基和 CuI/II/III 库存，删除公开作者 Cu 中间体答案坐标。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 6–8 页、SI 56–65 页支持 acac 模型和作者 Cu 捕获/消除解释。新模型采用实验 40°C，旧 298.15 K 端点另列，不能混成一条能标。

- [main.pdf](../../../../papers/paper_db6c4e0558113873/documents/main.pdf)：PDF 物理页 6、7、8；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_db6c4e0558113873/documents/supplementary_001.pdf)：PDF 物理页 56、60、64、65；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.exit_paths`（30 分）；`$.results.reservoir_ledger`（25 分）；`$.results.stereochemical_control`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧 298.15 K 的 syn/anti Cu 中间体差仅为端点/低频诊断，不是 40°C 下消除或直接氯转移的参考势垒。

**可实施先导和未完成参考：** 先核对完整 allyl/acac 与 Cu 电子数，计算连接端点的一条 Cu C–Cl 出口和一条 PhSO2Cl→自由基氯转移；再补第二立体出口、自旋和构象敏感性。

**拒绝项、公平替代结论及限制：** 拒绝裸 CuCl、省 acac 或跨库存比较绝对总能；直接转移胜出或两者不可区分均可。新结合自由能与自旋参考仍缺。

**检查：** 176 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_db6c4e0558113873/agent_input/task.md)；[PR task](../../paper_reproduction/paper_db6c4e0558113873/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_db6c4e0558113873/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_db6c4e0558113873/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_db6c4e0558113873/evaluation/task_provenance/upgrade_audit.json)。

### 5. paper_e2d9397dff2a3f0f

**范围与状态：** A→C：补原包缺失的 state_definition；保留两吡啶与 +1 单重态，按 C28→S28/O49 的明确图编辑建立一个 bcs 干预。每配体比较开环、开环后 NH3 进攻和直接进攻；六个段必须连接到同组成 N–N 终点。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 9–10 页区分 ΔGox、N–O 裂解和氨进攻；SI 47 页给出 MeCN 电化学约定。旧 109.995i 模态的两侧 N–O 距离变化很小且未跑 IRC，不能单凭单虚频认证裂解。

- [main.pdf](../../../../papers/paper_e2d9397dff2a3f0f/documents/main.pdf)：PDF 物理页 8、9、10、11；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf)：PDF 物理页 25、26、47、48；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.local_paths`（30 分）；`$.results.ligand_effect`（25 分）；`$.results.mode_identity`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧约 110i 模态和 13.8434 kcal/mol 数值没有 IRC，且 N–O 位移很小，仅作为需复核的诊断。

**可实施先导和未完成参考：** 先用真实模态和双向端点验证 bda 的 N10–O5 裂解，再做单一 bcs 图干预；逐配体完成开环、开环后 NH3 进攻与直接进攻，共六个段，统一到初始配合物+NH3 及相同 N–N 终点。

**拒绝项、公平替代结论及限制：** 拒绝用氧化自由能作化学势垒、横向虚频作裂解，或将开环一步与完整进攻比较。bcs 闭合盆地实证消失时允许坍缩，不编造极小点或独立势垒。

**检查：** 172 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_e2d9397dff2a3f0f/agent_input/task.md)；[PR task](../../paper_reproduction/paper_e2d9397dff2a3f0f/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_e2d9397dff2a3f0f/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_e2d9397dff2a3f0f/evaluation/task_provenance/upgrade_audit.json)。

### 6. paper_fcc3c7f2c46a0fbe

**范围与状态：** A→B：四个真实 4b/c/h/i 结构的 HAT、SET→PT、SPLET 热化学循环，另做 4c/4h 的 DPPH 局部 HAT 路径。仅 4c/i 有 COOH，甲氧基不能被当作酚羟基。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 4 页 DPPH 实验为 EtOH、30 min、517 nm；DMSO 是 NMR 条件。SI 34 页 IC50 和 4e 不溶信息作为解释约束。已修正 DPPH 中心 N 自由基连接并核对 C18H12N5O6。

- [main.pdf](../../../../papers/paper_fcc3c7f2c46a0fbe/documents/main.pdf)：PDF 物理页 3、4、8、9；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_fcc3c7f2c46a0fbe/documents/supplementary_001.pdf)：PDF 物理页 30、31、32、34；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.thermochemical_cycles`（30 分）；`$.results.decisive_local_paths`（25 分）；`$.results.activity_boundary`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧 4b 几何/XRD 比较提示名称、SMILES 与构象限制，不验证抗氧化反应循环。

**可实施先导和未完成参考：** 校验 E 构型和真实供氢位点，先闭合 4c/4h 的同质子/电子基准热化学循环并做显式 DPPH HAT，再扩至 4b/4i，检查循环闭合、位点替代和 EtOH 敏感性。

**拒绝项、公平替代结论及限制：** 拒绝把 OMe 当酚、把 DMSO 当活性测定溶剂、把不溶当无活性或由轨道隙推精确 IC50；多个机制均可行可以成为完成结论，不能外推绝对活性。

**检查：** 182 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_fcc3c7f2c46a0fbe/agent_input/task.md)；[PR task](../../paper_reproduction/paper_fcc3c7f2c46a0fbe/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_fcc3c7f2c46a0fbe/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_fcc3c7f2c46a0fbe/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_fcc3c7f2c46a0fbe/evaluation/task_provenance/upgrade_audit.json)。

### 7. paper_0e835b370ddd37b6

**范围与状态：** A→B：1、V′ 与羰基类似物 4 的 H2 活化路径，加四个固定 H–H 进度点的形变/相互作用分解与闭合残差。为 4 提供完整内酰胺图。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 PDF 2 页 Scheme 2 直接核对 4 的取代连接，3–5 页给出 PBE0-D3BJ/def2-TZVP、SMD benzene、298 K/1 atm 与 IRC。旧自动键级把中性二配位 Si 推成电荷分离 Si=N，注册表已按源结构修正。

- [main.pdf](../../../../papers/paper_0e835b370ddd37b6/documents/main.pdf)：PDF 物理页 2、3、4、5；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf)：PDF 物理页 7、8；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.activation_paths`（30 分）；`$.results.matched_coordinate_decomposition`（25 分）；`$.results.causal_comparison`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 既有 1/V′ H2 路径和分离物参考可在同对象、同协议下复用；缺少 4 和匹配进度分解。

**可实施先导和未完成参考：** 先核对中性二配位 Si 的 4 图与 H2 路径，再为三体系在 H–H=0.80/1.00/1.20/1.40 Å 四点计算冻结片段能；用真实计算确定闭合残差与方法敏感性。

**拒绝项、公平替代结论及限制：** 拒绝省略 4、错位进度比较或给冻结片段加热修正。形变和相互作用共同控制的解释可接受；新增对照仍待计算。

**检查：** 162 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_0e835b370ddd37b6/agent_input/task.md)；[PR task](../../paper_reproduction/paper_0e835b370ddd37b6/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_0e835b370ddd37b6/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_0e835b370ddd37b6/evaluation/task_provenance/upgrade_audit.json)。

### 8. paper_9132719dbf91c978

**范围与状态：** A→B：从 H–H 形成扩至 η2-H2、分离 H2/Pd 和 DMAc 再配位；P1/P41/Pd75/H76/H77 映射、完整 XantPhos 与两套标准态账本明确。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 4 页与 SI 10–12 页给出源局部 Pd 路线和方法。已有验证包含释放扫描与分离物种，能复用同协议部分；−1.76058 与 +0.133748 的不同约定不能混用。

- [main.pdf](../../../../papers/paper_9132719dbf91c978/documents/main.pdf)：PDF 物理页 1、4；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_9132719dbf91c978/documents/supplementary_001.pdf)：PDF 物理页 10、11、12；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.HH_formation`（30 分）；`$.results.release_and_recoordination`（25 分）；`$.results.standard_state_control`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 既有 INT-G/TS6、双向端点、释放扫描及分离 Pd/H2 文件可逐条审计复用；DMAc 再配位和混合标准态对照仍是新缺口。

**可实施先导和未完成参考：** 先核验一条旧 H–H 路径和束缚/分离 H2 身份，再优化 Pd(XantPhos)(DMAc)，构建 H2 气体 1 atm/溶质 1 M 与全 1 M 两套账本及压力敏感性。

**拒绝项、公平替代结论及限制：** 拒绝把 η2-H2 改名自由气体、删 XantPhos 或混搭标准态。H–H 成键易而释放/再配位不利是有效结果；局部模型不能证明整体周转。

**检查：** 147 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_9132719dbf91c978/agent_input/task.md)；[PR task](../../paper_reproduction/paper_9132719dbf91c978/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_9132719dbf91c978/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_9132719dbf91c978/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_9132719dbf91c978/evaluation/task_provenance/upgrade_audit.json)。

### 9. paper_534ae3b6e2fb695f

**范围与状态：** B→B：TMC 从 context-only 变成真实必需反应物；三个二胺同一酰氯位点的首酰化，HCl/质子守恒、全部关键段最大能垒和匹配 N–C 进度形变/相互作用比较。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 本地 supplementary 是评审材料，已在本批目录补取出版社 117 页正式 SI 并核对 10–14、20–22、32 页。明确 SVP/TZVP 方法文字差异，局部气相 1 M 模型是本次控制，不等同真实膜界面。

- [main.pdf](../../../../papers/paper_534ae3b6e2fb695f/documents/main.pdf)：PDF 物理页 2、3；源 SHA256 见该包审计。
- [publisher_formal_SI.pdf](source_review/paper_534ae3b6e2fb695f/publisher_formal_SI.pdf)：PDF 物理页 10、11、12、13、14、20、21、22、32；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.first_acylation`（30 分）；`$.results.descriptors_vs_barriers`（25 分）；`$.results.distortion_interaction`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧三二胺 HOMO/TCE 指标仅为描述符基线；原包的 TMC 是背景对象，没有酰化势垒。

**可实施先导和未完成参考：** 先跑 ODA+TMC 映射 C1002/Cl1003 的完整首酰化及单酰胺+HCl 终点，再原样扩到 6FODA/PFMB；保留必要加成、消除、质子转移段并取最大值，做匹配 N–C 进度分解。

**拒绝项、公平替代结论及限制：** 拒绝仅交 HOMO 指数、丢 HCl 或跨胺比较不同反应段。允许势垒排序反驳亲核性指数；局部气相 1 M 控制不证明膜界面动力学或性能。

**检查：** 156 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_534ae3b6e2fb695f/agent_input/task.md)；[PR task](../../paper_reproduction/paper_534ae3b6e2fb695f/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_534ae3b6e2fb695f/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_534ae3b6e2fb695f/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_534ae3b6e2fb695f/evaluation/task_provenance/upgrade_audit.json)。

### 10. paper_6f9a36fff6964313

**范围与状态：** B→B：冻结 CO2 环加成中的 KI 促环氧开环一步；TMTFABAOTf/PTMAOTf×末端/苄位进攻，完整离子对、KI、一水和旁观 CO2 的同组成比较，配合预组织控制。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 Table 2 与 SI 7–16 页定义底物和条件。353.15 K、MeCN 模型与源水混合物/CO2 压力分列；不要求另一氧化阶段或整循环。

- [main.pdf](../../../../papers/paper_6f9a36fff6964313/documents/main.pdf)：PDF 物理页 1、3、4；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_6f9a36fff6964313/documents/supplementary_001.pdf)：PDF 物理页 7、8、12、16；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.ring_opening_paths`（30 分）；`$.results.preorganization`（25 分）；`$.results.synergy_comparison`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧孤立离子对 Mulliken 电荷只能作为分区相关描述符，不能证明协同催化。

**可实施先导和未完成参考：** 核对两催化剂的完整 OTf/KI/环氧化物/水/CO2 库存，先各完成一条末端开环，再补苄位出口和受限催化剂定位对照，计入组织代价。

**拒绝项、公平替代结论及限制：** 只冻结 CO2 环加成中的一步；拒绝省离子库存或跨催化阶段比较。修正后没有保留双功能优势也可完成；真实水混合物/压力与有限模型分列。

**检查：** 171 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_6f9a36fff6964313/agent_input/task.md)；[PR task](../../paper_reproduction/paper_6f9a36fff6964313/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_6f9a36fff6964313/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_6f9a36fff6964313/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_6f9a36fff6964313/evaluation/task_provenance/upgrade_audit.json)。

### 11. paper_c625cba3ce868eb1

**范围与状态：** B→B：按真实底物图纠正为六/七元闭环，采用源 NBS/Et3N 非酶对照构建同库存竞争路径；明确 O21、烯烃 C2/C4、过氧 O23/O24，原 row22 是 H。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 7 页明确 NBS/Et3N、DCM，避免凭空指定酶内游离 Br+ 或把 Br− 当亲电溴。原文 0.284 mmol/6 mL 应为 47.3 mM，其 473 mM 印刷值作为冲突记录。

- [main.pdf](../../../../papers/paper_c625cba3ce868eb1/documents/main.pdf)：PDF 物理页 3、5、6、7；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf)：PDF 物理页 30、31、32；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.closure_paths`（30 分）；`$.results.active_reagent_ledger`（25 分）；`$.results.regioselectivity_test`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧水相反应物电荷/偶极不含试剂、过渡态或产物，不能认证 DCM 中的区域选择性。

**可实施先导和未完成参考：** 核对 NBS 溴化和质子转移后，从可比溴化前体完成六元与七元闭环；计入面选择、构象准备以及 succinimide/Et3N 质子账本。

**拒绝项、公平替代结论及限制：** 以实际图和源非酶对照纠正方案的五/六元表述；拒绝虚构五元路径、把 row22 氢当氧或把 Br− 当亲电体。完整比较后构象主导或不可区分均可；不声称酶内 QM/MM。

**检查：** 172 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_c625cba3ce868eb1/agent_input/task.md)；[PR task](../../paper_reproduction/paper_c625cba3ce868eb1/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_c625cba3ce868eb1/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_c625cba3ce868eb1/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_c625cba3ce868eb1/evaluation/task_provenance/upgrade_audit.json)。

### 12. paper_d3b4575397179146

**范围与状态：** B→B：四 heptazine 的 SET/氧敏化必要条件、真实 N-methyl-N-(p-CF3phenyl)pivalamide、催化剂阴离子/底物阳离子以及 O2/S1-O2/O2− 态循环；先 dF/dOMe 先导再扩四个。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 Fig. 4 核对底物和 0°C/O2/456 nm，SI 19 页核对源 TD 方法。schema 对三个氧态逐一固定电荷/多重度；E00、垂直 S1 和三重态隙分开。

- [main.pdf](../../../../papers/paper_d3b4575397179146/documents/main.pdf)：PDF 物理页 3、4、5；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_d3b4575397179146/documents/supplementary_001.pdf)：PDF 物理页 19、47、48、49、50、51、52、53、54、55；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.photoredox_matrix`（30 分）；`$.results.oxygen_states`（25 分）；`$.results.mechanism_discrimination`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧四催化剂 TDA/NTO 光谱可以帮助态特征诊断，不含底物自由基阳离子、催化剂阴离子或氧再生热化学。

**可实施先导和未完成参考：** 先用 dF/dOMe 核验中性/阴离子、真实底物阳离子、弛豫三重态与 E00，并用合适方法校准三重氧/单重氧/超氧；再完成四催化剂同基准 SET、EnT 和再生循环。

**拒绝项、公平替代结论及限制：** schema 固定三种氧态电荷/多重度，但物理态正确性还须原始波函数审查。拒绝 E00=垂直 S1、换电极基准或由热力学可行性断言唯一机制、寿命/产率；双机制必要条件均满足允许。

**检查：** 160 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_d3b4575397179146/agent_input/task.md)；[PR task](../../paper_reproduction/paper_d3b4575397179146/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_d3b4575397179146/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_d3b4575397179146/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_d3b4575397179146/evaluation/task_provenance/upgrade_audit.json)。

### 13. paper_ef26687d63a37e29

**范围与状态：** B→B：提供 PA/无 PA 的明确短链图（2PO/1CO2，P+/O−），两 Et3B 库存；传播 CO2 插入/PO 开环与回咬逐段比较，保留短链共产品，做十倍 PO 稀释控制。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 9–10 页与 SI 4–12 页支持源磷鎓/氧相互作用解释。新增短链是 benchmark 构造，PA/无 PA 是复合结构干预，不宣称只改变静电。

- [main.pdf](../../../../papers/paper_ef26687d63a37e29/documents/main.pdf)：PDF 物理页 9、10；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf)：PDF 物理页 4、5、7、8、9、10、11、12；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.chain_paths`（30 分）；`$.results.chain_end_audit`（25 分）；`$.results.concentration_test`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧引发剂加合物 ADCH/ESP/接触分析可审身份，不能改名为碳酸酯增长链或替代传播/回咬势垒。

**可实施先导和未完成参考：** 验证 PA 短链及两 Et3B，完成 CO2 插入→PO 开环全序列和保留缩短链共产品的回咬；再做无 PA 匹配模型，用同一组势垒推十倍活度变化。

**拒绝项、公平替代结论及限制：** 拒绝省共产品/第二 Et3B 或只挑易传播段；PA 优势减弱、消失或被复合干预混杂均可如实解释。短链结构变化不能归因于纯静电，也不能证明体相聚合性能。

**检查：** 223 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_ef26687d63a37e29/agent_input/task.md)；[PR task](../../paper_reproduction/paper_ef26687d63a37e29/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_ef26687d63a37e29/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_ef26687d63a37e29/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_ef26687d63a37e29/evaluation/task_provenance/upgrade_audit.json)。

### 14. paper_0dc85595cab7bc0a

**范围与状态：** C→C：保留两阶段图枚举，加入临界构象、DFT 精化、H 原子/氧化层守恒及每阶段代表闭环的势面/态追踪。被实证排除或坍缩的候选可省不存在的 G，必须交搜索轨迹和映射依据。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 2–3 页和 SI 9–11 页的基态能量/LUMO 推断不等价于光态可达性。旧结果以 4.30 Å 截止排除约 4.327 Å 候选且主要用 xTB，不能直接成为新隐藏标准。

- [main.pdf](../../../../papers/paper_0dc85595cab7bc0a/documents/main.pdf)：PDF 物理页 2、3；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_0dc85595cab7bc0a/documents/supplementary_001.pdf)：PDF 物理页 9、10、11；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.candidate_layers`（30 分）；`$.results.accessibility_diagnostics`（25 分）；`$.results.supported_set`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧 xTB 候选枚举和图检查只作搜索诊断；4.30 Å 与 ±15 kJ/mol 剪枝未经校准，不能冻结成新标准。

**可实施先导和未完成参考：** 重新纳入旧距离边界附近的图异构闭环和构象，两阶段均作 DFT 精化；每阶段至少一个关键闭环提供映射 S0 路径及物理激发态追踪，并维护氢/氧化层守恒。

**拒绝项、公平替代结论及限制：** 拒绝跨氢数比较总能、只用旧截止剪枝或将最低 S0 终点指定唯一光产物。真实排除/坍缩可省不存在的能量但须搜索证据；多个候选保留允许，全动力学仍可选。

**检查：** 144 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_0dc85595cab7bc0a/agent_input/task.md)；[PR task](../../paper_reproduction/paper_0dc85595cab7bc0a/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_0dc85595cab7bc0a/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_0dc85595cab7bc0a/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_0dc85595cab7bc0a/evaluation/task_provenance/upgrade_audit.json)。

### 15. paper_a3892396b1843698

**范围与状态：** C→C：同一 C11H14 的 [3,3]/[5,5] 两路径×明确反号二面角预组织干预，含制备能、解除约束和双向端点；不把未证明的构象称为真实 double-chair 极小点。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 Fig. 5 的应变/构象解释与 SI 5 页方法限定局部问题；新控制是同图几何干预，完整轨迹与全部桥连衍生物可选。

- [main.pdf](../../../../papers/paper_a3892396b1843698/documents/main.pdf)：PDF 物理页 2、4、5、6；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_a3892396b1843698/documents/supplementary_001.pdf)：PDF 物理页 5；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.rearrangement_paths`（30 分）；`$.results.preorganization`（25 分）；`$.results.channel_response`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧 GFN2-xTB/RRHO 两路径与势垒可作准备和调试，不能替代 DFT 校准或轨迹分支。

**可实施先导和未完成参考：** 先 DFT 精化非约束 [3,3]/[5,5] 与端点映射，再施加定义的反号二面角干预，记录电子准备代价，解除约束后搜索两通道。

**拒绝项、公平替代结论及限制：** 拒绝把约束几何叫自由极小点、忽略准备能或由驻点断言精确分支；两个独立控制回到同盆地时提交完整坍缩证据，无须虚构两个自由能值。

**检查：** 154 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_a3892396b1843698/agent_input/task.md)；[PR task](../../paper_reproduction/paper_a3892396b1843698/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_a3892396b1843698/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_a3892396b1843698/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_a3892396b1843698/evaluation/task_provenance/upgrade_audit.json)。

### 16. paper_8fefc96b015c4577

**范围与状态：** C→C：短/长链×DMSO/DCE×两芳环闭合的 2×2×2 矩阵。长链仅在 13–14 之间插入 CH2，保留旧 1–53 映射并新增 54–56；提供同源映射与独立构图命名空间。 状态 `implemented_pending_expanded_reference`。

**正文/SI 实质依据：** 正文 2–4 页和 SI 34 页定义局部路径；旧验证有 C–C 模态测试而无全 IRC。实验添加剂也变，受控溶剂交叉不能代表所有实验原因；长链差距小，不强迫排序反转。

- [main.pdf](../../../../papers/paper_8fefc96b015c4577/documents/main.pdf)：PDF 物理页 2、3、4；源 SHA256 见该包审计。
- [supplementary_001.pdf](../../../../papers/paper_8fefc96b015c4577/documents/supplementary_001.pdf)：PDF 物理页 34；源 SHA256 见该包审计。

**评估改动：** 三个科学面板分别为 `$.results.crossed_paths`（30 分）；`$.results.factorial_contrasts`（25 分）；`$.results.strain_and_robustness`（15 分）。它们与身份、稳健性和结论规则共同绑定结果与原始证据；规则文件在两模式字节一致。

**旧参考可复用边界：** 旧短链 DMSO 的 B 零点势垒和 C–C 模态记录可复核，但没有全 IRC，不能填补长链、DCE 或新增端点。

**可实施先导和未完成参考：** 先核对 56 原子同系物与 radical map10，验证关键长链双路径的真实模态和双向端点，再完成两链长/两溶剂交叉，量化长链低频、构象、方法差异与匹配进度形变。

**拒绝项、公平替代结论及限制：** 拒绝复制短链行号、混用能量零点或省交叉格；证据支持的长链近简并可以完成，不强制反转。实验添加剂也变，受控溶剂结论需限定。

**检查：** 185 个去重逐篇断言通过；两个模式均通过官方包/运行时/导出检查。新科学参考未完成。

**文件入口：** [AR task](../../autonomous_research/paper_8fefc96b015c4577/agent_input/task.md)；[PR task](../../paper_reproduction/paper_8fefc96b015c4577/agent_input/task.md)；[提交 schema](../../autonomous_research/paper_8fefc96b015c4577/agent_input/submission_schema.json)；[扩展参考计划](../../autonomous_research/paper_8fefc96b015c4577/evaluation/reference_validation_plan.md)；[审计](../../autonomous_research/paper_8fefc96b015c4577/evaluation/task_provenance/upgrade_audit.json)。

## 阻塞、软件范围和移交

唯一输入阻塞为 `paper_60f4c45810428116`：SI Table S2 的 25 个网格位置已提供，其中 23 个非堵塞位置保留原观测/删失分类；还缺独立速率区间与回淬 sink 身份/电荷电子守恒。已有电势与 RBF 插值均不能填补缺口。包的网络、可辨识性、留出字段和失败诊断已实现，解除条件写在两模式参考计划和 manifest，不能因有观测网格就宣称科学就绪。

其余 15 篇输入与有限对照已经可审查，新增参考仍须按各计划计算。方法范围以已查 `chemistry_toolbox` README/config/native guides 为准：Gaussian/ORCA 用于相应分子 DFT、频率、TD/redox；路径采用可审计的 IRC/模态跟随，xTB/CREST 只作初筛准备；Python/SciPy 负责账本与 ODE。软件可调用不代表具体方法已校准。NBO/PyFrag 依可用性作为可选诊断，未引入无依据 NEGF、体相模型或新付费服务。

已完成本批开发写入，32 个包按 [HANDOFF.json](HANDOFF.json) 的 content/manifest 双哈希移交监督。`stopped_writing_paper_ids` 包含全部 16 篇及优先请求的 a389、913、60f；本实施进程不再修改这些包。监督会话 `01a0e2da-982a-7b32-bcc1-744840298ce5` 可据此独立复核和冻结可计算快照。`package_ready_for_supervisor_review` 只表示开发包可审查，不表示科学验证通过；后续科学预算或运行由监督另行管理。

交付清单：[manifest.json](manifest.json)、[validation_report.json](validation_report.json)、[STATUS.md](STATUS.md)、[HANDOFF.md](HANDOFF.md)、[HANDOFF.json](HANDOFF.json)。
