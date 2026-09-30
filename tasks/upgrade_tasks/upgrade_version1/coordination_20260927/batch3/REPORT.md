# 第3批任务包开发升级报告

日期：2026-09-27。范围：先修基线、有限模型与规模试算，共19篇、AR/PR共38包。

全部论文已有逐篇可审查开发结果；17篇状态为 `implemented_pending_expanded_reference`，2篇为 `blocked`。这是开发完成与输入阻塞的记录，不是38包科学验证通过。新量化引擎启动0次、新科学计算0次；没有运行长量化/HPC或新增付费服务。

## 实施和来源边界

仅写本批19篇的 upgrade_tasks 两模式目录及 batch3 工作区。现行 final 在目标不存在时复制，所有源文件按字节存为私有 `evaluation/legacy_final_snapshot/**/*.snapshot`，来源哈希见每包 `evaluation/task_provenance/upgrade_audit.json`。后续修订基于本进程已建开发包；源 final 文件和完整文件集合均在检查中复核。未修改公共 README、维护脚本、方案、论文原文、verification 或其他批次。

先读实施/复核指南、19份顶部首版规格及历史链接、源 AR/PR 包，并参照第一批两套完整包与 maintenance/check_batch1.py。正文/SI 的相关内容按页检查并在 evidence 中保留提取记录，关键结构图也查看渲染图。36个历史 JSON 结果的读取与哈希见 `evidence/legacy_run_review.json`；历史 PASS、源终态及旧数值均不构成扩展参考。

科学文本使用原有 Scientific objective / Public inputs and scientific boundaries / Required scientific validation/investigation / Deliverables 组织。两模式的对象、公开数据、schema、完成标准和五份科学 evaluator 完全一致；只有 PR 追加 Author-provided scientific guidance，区分源方法/作者解释与新增干预。作者计算终态坐标从当前公开输入移出，真实实验 CIF、已知实验观测及明确独立生成起点按授权保留；仅需身份判别的原子图、映射和类别配位关系公开。

## 提交与科学评分

每包强制 `report/results.json` 和 `report/report.md`。结构化字段含有限对象的电荷/自旋、实际任务输入输出、逐论文研究矩阵、数字指标、状态/角度/构象全表、原子映射、两个竞争假设、实测敏感性与资源计量。完整提交必须覆盖全部核心对象和矩阵；合理失败有诊断格式但无未完成端点的科学分。受限点与自由极小点分开；构象坍缩只在物理允许的行接受，需真实映射前后证据，不准用它绕过方法/归因比较。

每篇中间与最终评分均绑定具体结果字段和原始产物：对象/守恒10分，三个论文特异矩阵20/25/20分，判别与稳健性15分，结论10分，共100分。evaluator 要打开引用文件核对对象、成功终止、态/频率/路径证据、数值与单位，重算差值；仅旧标量、缺控制、错电荷/态/零点、伪造/失败冒充完成均阻止科学完成。支持、反驳和完整证据下不可区分保持对称；optional 不进入强制失败条件。新增参考容差为待校准，未继承旧窄区间。

## 开发验证

官方验证共 **2466项通过**，详见 `validation_report.json`，脚本为 `check_batch.py`。使用 `.envs/researchchembench/bin/python`、`TaskRepository(roots=[Path("tasks/upgrade_tasks")])`，没有改默认正式任务发现机制。

- JSON/JSON Schema、validate_task_package、load_runtime_evaluation、100分权重与官方 payload/content 哈希。
- AR/PR 科学正文（排除 PR 作者指导）、公开输入、schema、五份 evaluator 一致。
- materialize 仅导出 agent_input，不导出 evaluator、源快照、私有参考或源 PDF。
- 所有源快照及原 final 字节/文件集合、指南/正文/SI 来源哈希复核。
- 分子图连通性、组成、电荷/自旋奇偶、映射、笼/配位/扭转和守恒反应的论文特异检查。
- 官方 output_contract 的完整/诊断格式正例，及旧标量、缺核心行/指标/报告、错误对象/电荷/自旋/能量零点、全失败却 complete、路径穿越等负例；blocked 包拒绝 complete。

这些是结构、输入合理性与格式检查。合成样例只放临时目录并标明非科学数据；没有运行 LLM 科学裁判，也没有用假原始文件验证科学得分。output_contract 不会自动证明被引用文件的科学真实性，实际原始产物审核由科学 evaluator 负责，完整端到端正反例仍在各包 release gate 中。

## 逐篇结果

### 1. paper_36722b90a0c12825 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_36722b90a0c12825/agent_input/task.md) · [PR](../../paper_reproduction/paper_36722b90a0c12825/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_36722b90a0c12825/evaluation/reference_validation_plan.md)。

**科学升级。** 把单一 E 主体 open/close 差升级为 E/Z × 游离/Cl⁻ 结合的构象集合和闭合结合循环，加入冻结主体畸变与介质/离子对控制。公开 100 原子主体连接和 E/Z 定义，Cl⁻ 及复合物电荷明确；不公开旧优化终态坐标。

**正文/SI与基线核查。** 核对正文 Figs3–5、两份 SI 与历史输出。旧约 +0.999 eV 是 G(open)−G(close)，约 +1.516 eV 是电子能差；两者都不是 E/Z 结合开关。已将此区别写入私有基线门控；没有声称重算纠正了旧结果。PSS 不作为热平衡布居。 来源定位：Main PDF pp3-4 Figs3-5; coordinate SI1 pp2-8; SI2 pp6-7,15-16, Table S2 and DFT section.

**评估改动。** 核心矩阵为 `species_ensembles`（5行）；`binding_cycle`（3行）；`intervention`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 140 项。

**可行性、参考缺口和限制。** Gaussian/ORCA、CREST 与热化学后处理可支撑有限分子研究。仍缺四组集合、标准态一致的结合差和畸变/环境先导；第二主体及完整滴定/PSS 不是首版硬性项。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 2. paper_9455a82229de2427 — C → 加强C

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_9455a82229de2427/agent_input/task.md) · [PR](../../paper_reproduction/paper_9455a82229de2427/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_9455a82229de2427/evaluation/reference_validation_plan.md)。

**科学升级。** 保留开放候选发现，明确 Si/N 从异戊二烯两个末端的四个进攻类别；新契约要求主路径和最重要竞争路径的端点、TS/IRC 或连续无垒证据，以及热力学排序与碰撞可达性的分开判断。

**正文/SI与基线核查。** 正文反应 PES、Fig3 与 SI CBS-QB3 数据支持 SiN 双重态、异戊二烯单重态、SiNC₅H₇ 单重态和 H 双重态的守恒定义。公开的是实验碰撞/放热观测和反应物身份；候选产物图由参试者提交，不给作者赢家。统一 0 K E+ZPE 的分离反应物零点。 来源定位：Main PDF pp3-8 computational details, Fig3 energy distribution and reaction PES; SI p2 Table S1 and pp3-15 CBS-QB3 coordinates/energies.

**评估改动。** 核心矩阵为 `candidate_space`（4行）；`connected_routes`（2行）；`accessibility`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 124 项。

**可行性、参考缺口和限制。** 复合能量/ORCA 加路径软件具备方法基础；没有新路径先导，也不冻结可达性数值阈值。须先验证一条守恒连通路径再开展竞争路线；不要求全 RRKM、全散射或精确分支比。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 3. paper_9a58a1fa6ed7d780 — B → 加强B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_9a58a1fa6ed7d780/agent_input/task.md) · [PR](../../paper_reproduction/paper_9a58a1fa6ed7d780/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_9a58a1fa6ed7d780/evaluation/reference_validation_plan.md)。

**科学升级。** 新增真实 BN 5a/全碳 5b 的松弛与交叉冻结骨架对照，以匹配态的 E、f、D、Sr 和 NTO 分解化学与几何作用。给出两个 40 原子图以及经图同构检查的完整原子映射。

**正文/SI与基线核查。** SI S21/S22 支持 BN 为 C₂₂H₁₄B₂N₂、全碳为 C₂₆H₁₄，修正旧说明 H 数错误。历史 S1–S4 指标已经存在，真正需修复的是 S1 能量、S4 Sr 偏差和态/密度定义，不能将其写成缺少全部指标。 来源定位：Main pp2-4 Figs2-3; SI p3 methods, Tables S11/S14 and pp49-51 Tables S21-S22.

**评估改动。** 核心矩阵为 `relaxed_states`（2行）；`common_scaffold`（2行）；`attribution`（3行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 115 项。

**可行性、参考缺口和限制。** TDDFT 与 Multiwfn 可以完成有界对照；扩展前需复核归一化振幅、网格和态匹配。没有新能量或 Sr 参考，不沿用旧窄容差。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 4. paper_9f4c259696ad2f87 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_9f4c259696ad2f87/agent_input/task.md) · [PR](../../paper_reproduction/paper_9f4c259696ad2f87/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_9f4c259696ad2f87/evaluation/reference_validation_plan.md)。

**科学升级。** 新增 PXX1/PXX2 各自 0/1/2 个 B(C₆F₅)₃ 的有限计量矩阵、逐步守恒结合/解离、同几何取走酸及完全松弛对照，并要求 TD/NTO/f 与可比较滴定趋势。

**正文/SI与基线核查。** 正文 Figs6–7 和 SI 结构确认 PXX1 只有一个羰基，因此第二酸模型定义为额外供体位点/竞争配位，未虚构第二羰基。补公开实验浓度、溶剂、定性红移/等吸收点及游离吸收观测；明确 SI 图示与图注编号冲突。PR 还区分正文和 SI 的基组表述。 来源定位：Main pp8-10 Figs6-7; SI pp5-6 methods, pp144-149 coordinates, pp167-169 Lewis adduct discussion.

**评估改动。** 核心矩阵为 `stoichiometric_series`（6行）；`balanced_binding`（4行）；`geometry_and_spectrum`（3行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 142 项。

**可行性、参考缺口和限制。** 最大双酸复合物成本仍需先导测量，构象坍缩可以实证提交。相似光谱允许不可区分，不能硬判唯一计量；未要求无原始谱可支撑的全浓度拟合、FRET 或发光效率。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 5. paper_a0f6b899582cb9f7 — A → B

状态：`blocked`。包：[AR](../../autonomous_research/paper_a0f6b899582cb9f7/agent_input/task.md) · [PR](../../paper_reproduction/paper_a0f6b899582cb9f7/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_a0f6b899582cb9f7/evaluation/reference_validation_plan.md)。

**科学升级。** 已建立 M3 与 PM6/真实受体 BTP-eC9 的面/边接触、冻结/松弛、分解、增大片段与四极矩矩阵及提交/evaluator。公开可核对的 M3 图和已有独立初始构型，未用 Qzz 替代两类配对作用。

**正文/SI与基线核查。** 亲自查看正文 Fig1、相互作用段落及 SI。可以识别材料和 M3，但没有查到可直接复用的原子级封端配对模型、切键清单和增大片段映射；不能把示意结构默认为已核准有限模型。 来源定位：Main p2 Fig1 and pp3-4 interactions; SI pp3,5 molecular characterization and FigS3; no atom-resolved PM6/BTP-eC9 fragment coordinate/cap list was found in these materials.

**评估改动。** 核心矩阵为 `contact_models`（4行）；`decomposition`（2行）；`truncation_and_tensor`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 92 项。

**可行性、参考缺口和限制。** blocked_input_definition：必须补齐 PM6 与 BTP-eC9 两套准确连接、切键/封端、电荷及增大片段对应，并完成一组截短/分解先导。两包只接受 partial/bounded_failure；未声称已可执行完整科学任务。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 6. paper_b276b18215cba283 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_b276b18215cba283/agent_input/task.md) · [PR](../../paper_reproduction/paper_b276b18215cba283/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_b276b18215cba283/evaluation/reference_validation_plan.md)。

**科学升级。** 从单臂推广猜测升级为 57 原子单臂与完整 141 原子三臂的 cisoid/transoid、逐臂冻结与气相/乙醇转移比较。公开三个独立臂的重原子映射、明确切除其余臂时的封端规则和各臂扭转原子。

**正文/SI与基线核查。** SI TablesS8–S11 与正文/quatsome 讨论直接核对了完整三臂对象。公共图不含优化答案；图映射检查确保三臂不是三份任意小分子，也未用单臂计算冒充完整转移验证。 来源定位：Main pp4-5 optical/quatsome discussion; SI pp15-16 FigsS12-S13, pp45-64 Tables S8-S11.

**评估改动。** 核心矩阵为 `relaxed_models`（4行）；`arm_geometry_control`（3行）；`transfer_and_medium`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 122 项。

**可行性、参考缺口和限制。** 完整三臂 TD 的根窗口和成本尚未测量，至少一套完整三臂电子结果属于核心。膜、双光子与聚集实验机制不由这些局部分子结果证明。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 7. paper_fda8b9b53f8276db — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_fda8b9b53f8276db/agent_input/task.md) · [PR](../../paper_reproduction/paper_fda8b9b53f8276db/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_fda8b9b53f8276db/evaluation/reference_validation_plan.md)。

**科学升级。** 将晶体几何拟合升级为 cis/trans × 气相/MeCN 的能量与六键残差比较，并以 N1–C1–C2–N2 扭转干预区分构象与环境来源。公开原 CIF、六键实验定义及其标签映射。

**正文/SI与基线核查。** 采用 CCDC2433822 和当前 final 的六键 scope，已核对 SI TableS2/FigsS11–S13；没有混用历史七键集合或其他反式报告。单个 RMSE 不替代四个环境/构象端点和热力学比较。 来源定位：Main p4 computational structure discussion; SI Table S2 and FigsS11-S13; immutable CCDC2433822 and current final experimental_bonds.json define the six-bond scope.

**评估改动。** 核心矩阵为 `conformer_environment`（4行）；`six_bond_residuals`（4行）；`torsional_intervention`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 117 项。

**可行性、参考缺口和限制。** 常规优化/频率和短约束扭转可实现；新集合与介质参考尚未跑。晶体差异解释限制在有限分子模型，不能将气相最低能当作固态唯一原因。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 8. paper_0de37d01e35c27df — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_0de37d01e35c27df/agent_input/task.md) · [PR](../../paper_reproduction/paper_0de37d01e35c27df/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_0de37d01e35c27df/evaluation/reference_validation_plan.md)。

**科学升级。** 将单个 S···S 距离升级为 norDTCO/DTCO × 中性/阳离子及交叉冻结几何，联查键级、反键占据、自旋与距离，检验两中心三电子解释。

**正文/SI与基线核查。** 正文 Fig2/Table1 与 SI S3/S4/S7/S8 核对了桥连和无桥连对象。固定显式 H 原子映射，拒绝仅按近距离添加不存在的共价 S–S 边；中性 singlet、阳离子 doublet 和电子数一致。 来源定位：Main pp3-4 Fig2/Table1; SI pp10-11 TablesS3/S4, pp15-18 TablesS7/S8 and orbital/EPR sections.

**评估改动。** 核心矩阵为 `oxidation_pairs`（4行）；`vertical_geometry`（4行）；`bonding_interpretation`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 147 项。

**可行性、参考缺口和限制。** 开壳层 DFT、轨道/自旋分析有方法基础；需校准键级/占据定义和方法敏感性。仅收缩不能支持三电子键；证据充分的反驳或无可区分响应都允许。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 9. paper_43d74f8a469d9ad3 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_43d74f8a469d9ad3/agent_input/task.md) · [PR](../../paper_reproduction/paper_43d74f8a469d9ad3/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_43d74f8a469d9ad3/evaluation/reference_validation_plan.md)。

**科学升级。** 提供 CCDC2441197 对应染料1与 Scheme1 甲氧基染料2的明确连接和取代映射，要求同一芳基转动的 S0/S1 剖面、限制/释放以及态连续性和网格/方法控制。

**正文/SI与基线核查。** 实际检查 Scheme1、计算段、扭转讨论和 SI S5–S8：SI 标为1的一处组成与真实 CIF 对象不一致。以实验 CIF 的 C₂₃H₂₀BNO₃ 和结构式构建 C₂₄H₂₂BNO₄ 对照，未复制有疑问的 SI 优化几何。PR 披露扭转与一般 TD 方法差别。 来源定位：Main p2 Scheme1, pp3-4 computational section, pp8-10 torsion/photostability; CCDC2441197. SI pp32-37 Tables S5-S8 contain composition/label inconsistency.

**评估改动。** 核心矩阵为 `torsion_profiles`（4行）；`restriction_control`（2行）；`continuity_and_robustness`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 121 项。

**可行性、参考缺口和限制。** 先做短角段 S1 跟踪，再扩剖面；受限点不得声称无约束极小点。局部转动/激发结果不单独证明光稳定性或发光产率。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 10. paper_86a0b654270a8ce7 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_86a0b654270a8ce7/agent_input/task.md) · [PR](../../paper_reproduction/paper_86a0b654270a8ce7/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_86a0b654270a8ce7/evaluation/reference_validation_plan.md)。

**科学升级。** 两个完整 Ir–salen–NHC 配位异构体以同组成图、六个供体及三组 trans 配对唯一限定。新增构象集合、339 K THF 中 E/溶剂化/热/低频拆分、接触干预和方法稳健性。

**正文/SI与基线核查。** 正文 Scheme1 和 SI 几何/自由能段支持中性 Ir(III)、salen²⁻ 与环金属化 NHC⁻ 记账。保留身份所需的类别配位关系而移除作者终态坐标；历史排序翻转是待修基线，不冒充已解决。 来源定位：Main pp2-3 Scheme1 thermochemistry and contact discussion; SI pp6-7 geometry and pp11-18 Gibbs calculation details/coordinates.

**评估改动。** 核心矩阵为 `isomer_ensembles`（2行）；`stacking_intervention`（2行）；`ranking_robustness`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 121 项。

**可行性、参考缺口和限制。** 完整 130 原子对象可用量化软件处理，但新构象与低频敏感性成本未测量。只有相同定义的 ΔG₂₋₁ 才能排序，堆积接触不等于独立因果，产率不作平衡布居。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 11. paper_94e7481ded3b6a75 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_94e7481ded3b6a75/agent_input/task.md) · [PR](../../paper_reproduction/paper_94e7481ded3b6a75/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_validation_plan.md)。

**科学升级。** 以实际 PBNA 图定义两个外侧 B–phenyl 转轴，对 S0/S1 自由和受限几何做垂直/松弛响应，并加入第二扭转或方法及同溶剂控制。

**正文/SI与基线核查。** 正文 Figs3–4 与 SI S11/S12/光谱段已查。图桥检查将真正外侧转轴与骨架内部键分开，避免初始距离推断误把稠环内键当可自由转动的 phenyl 键。 来源定位：Main pp4-6 Fig3/Fig4; SI pp16-19 aggregation/optical context and p19 TablesS11-S12 ground-state methods/coordinates.

**评估改动。** 核心矩阵为 `state_geometry`（4行）；`motion_response`（2行）；`local_robustness`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 113 项。

**可行性、参考缺口和限制。** TD 激发态梯度/连续性和受限结果需要先导，当前没有新 S1 参考。科学结论限于分子运动贡献，不能声称完成聚集或 AIE 机制证明。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 12. paper_9aa6d5655edfeb52 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_9aa6d5655edfeb52/agent_input/task.md) · [PR](../../paper_reproduction/paper_9aa6d5655edfeb52/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_9aa6d5655edfeb52/evaluation/reference_validation_plan.md)。

**科学升级。** 采用真实融合2a与非融合前体1a，加入对称小幅笼 C–C 位移、态/频率检查和方法敏感性，区分融合、笼运动与其他化学变化。

**正文/SI与基线核查。** SI pp4–5 的1a实际含 Br；公开组成 C₁₈H₂₁B₁₀Br，对照2a为 C₁₈H₂₀B₁₀。图检查12个 closo 顶点各有五个笼邻居，切融合键、恢复 B–H/aryl–Br 有明确映射。±0.05 Å 是新设计干预，不是误差容差。 来源定位：Main pp2-4 Schemes1-2 and optical discussion; SI pp4-5 identity1a, p19 methods/2a coordinates, pp10-15 optical context.

**评估改动。** 核心矩阵为 `fusion_pair`（2行）；`cage_displacement`（4行）；`causal_limits`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 117 项。

**可行性、参考缺口和限制。** Br 差异是明确混杂因素，不能把二者差全部归因融合。需跑频率、态连续性与位移参考；近简并和方法依赖可构成有证据的不可区分结论。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 13. paper_a6e8c57709329bdb — A → B

状态：`blocked`。包：[AR](../../autonomous_research/paper_a6e8c57709329bdb/agent_input/task.md) · [PR](../../paper_reproduction/paper_a6e8c57709329bdb/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_a6e8c57709329bdb/evaluation/reference_validation_plan.md)。

**科学升级。** 已重构 HL/Fe(III)/Co(II) 的配位、质子化、溶液交换与暗态/CT 竞争解释矩阵，公开已能确认的 HL/DMF 图和 Fe/Co 候选自旋边界。

**正文/SI与基线核查。** 正文 pp2,5–7 与 SI S5–S8/S20 确认 DMF 和 Co(II) 竞争离子；没有确定传感盐反离子、水含量及 pH/质子库。原 MnL 是不同配位背景的异配体对象，不能替代干净竞争离子控制。 来源定位：Main pp2,5-7 Fig4 and theoretical calculation section; SI FigsS5-S8/S20. DMF is explicit; salt counterion, water activity and pH for Fe/Co sensing are not established by the accessed records.

**评估改动。** 核心矩阵为 `coordination_candidates`（5行）；`solution_cycles`（3行）；`selectivity_tests`（3行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 87 项。

**可行性、参考缺口和限制。** blocked_solution_definition：需源记录或经确认的有限溶液模型固定反离子、水/质子库、配位与质子化，再建立守恒 Fe/Co 交换和开壳层参考。未虚构盐、pH 或 Fe 终态，两包禁止 complete。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 14. paper_b1467cd61ca8022d — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_b1467cd61ca8022d/agent_input/task.md) · [PR](../../paper_reproduction/paper_b1467cd61ca8022d/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_b1467cd61ca8022d/evaluation/reference_validation_plan.md)。

**科学升级。** 定义 PM/BM/TFPM/TFBM、FSI⁻ 与 Li⁺，构建统一 1:1:1 中性有限簇的溶剂配位/阴离子竞争、冻结碎片能和畸变，并区分 ESP 与 RESP 的物理量和单位。

**正文/SI与基线核查。** 核对正文 Fig2/methods 后发现本地 supplementary_001 是审稿文件，另从出版方下载正式46页 SI，核查 pp5–8 FigsS5–S8 和 TableS1。四种醚的连接及氟代位置均显式提供。 来源定位：Main pp2-5,12 Fig2/methods; formal publisher SI pp5-8 FigsS5-S8 and p36 TableS1. Local supplementary_001 is a peer-review file, not the formal scientific SI.

**评估改动。** 核心矩阵为 `cluster_orientations`（8行）；`fragment_controls`（4行）；`descriptor_test`（3行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 161 项。

**可行性、参考缺口和限制。** 有限簇 DFT 和密度分析可实施；新构象、竞争能及分解参考待算。簇描述符不代表体相 RDF、配位数分布或电解液性能，未补造体相验证。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 15. paper_c28b0a1c549f4575 — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_c28b0a1c549f4575/agent_input/task.md) · [PR](../../paper_reproduction/paper_c28b0a1c549f4575/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_c28b0a1c549f4575/evaluation/reference_validation_plan.md)。

**科学升级。** 公开 TEA⁺、双季铵 DED²⁺、BF₄⁻ 和 PC 的完整图；以电中性盐的 PC0/1/2 配位层定义接触/分离离子对及第一、第二 PC 转移的守恒反应。

**正文/SI与基线核查。** 正文电解质身份与 SI 计算定义直接核对，DED 为双乙基化 DABCO，不是误电荷的中性胺。程序检查两条 PC 交换在元素与电荷上都严格守恒，避免不同离子数裸总能排序。 来源定位：Main pp1-3 electrolyte identity and association; SI pp5-6 computational details.

**评估改动。** 核心矩阵为 `equal_composition_clusters`（8行）；`PC_exchange`（2行）；`ion_pair_control`（3行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 159 项。

**可行性、参考缺口和限制。** 可用构象搜索后 DFT 精化有限簇；主介质/有限溶剂定义已写入控制。新交换自由能、接触稳定性和构象不确定性未校准，不能据此宣称全溶液热力学。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 16. paper_2877efc02814175d — A → B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_2877efc02814175d/agent_input/task.md) · [PR](../../paper_reproduction/paper_2877efc02814175d/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_2877efc02814175d/evaluation/reference_validation_plan.md)。

**科学升级。** 新增完整自由 DQCS、Cd/Co/Ni 复合物以及从各金属结构取出的冻结中性配体，使用同态 TD/NTO、金属/配体分区和畸变拆分电子与几何作用。

**正文/SI与基线核查。** 默认 papers/main.pdf 无可读正文，实际阅读已有 user_supplied 的10页恢复主文 pp2,7–8 及 SI。自由配体为64原子 C₃₁H₂₇N₃O₃；源金属索引64保留，配体末尾H为65，不进行错误整体重编号。Co doublet 与 Cd/Ni singlet 明确。 来源定位：Recovered user-supplied main PDF (10 pages; source_data/user_supplied_20260925/1-s2.0-S0022286025023567-main.pdf), p2 computational section and pp7-8 Figs8-10; SI pp11-13 TablesS1-S3 and p18 TableS8 directly checked. The default papers/main.pdf has no readable body and is not the evidence source. Experimental sensing is DMSO/water9:1, distinct from the bounded DMSO electronic calculation.

**评估改动。** 核心矩阵为 `relaxed_species`（4行）；`frozen_ligand`（3行）；`attribution`（4行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 137 项。

**可行性、参考缺口和限制。** 开壳层响应须先导检查自旋与态匹配。原实验 DMSO/H₂O 9:1 与本次有界 DMSO 电子计算明确区分，不将孤立金属复合物差异当作水溶液选择性证明。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 17. paper_2f2aa11ea61a32bb — B → 加强B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_2f2aa11ea61a32bb/agent_input/task.md) · [PR](../../paper_reproduction/paper_2f2aa11ea61a32bb/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_2f2aa11ea61a32bb/evaluation/reference_validation_plan.md)。

**科学升级。** 四个真实单体1a–1d各做松弛与共同局部螯合骨架控制，结合态身份和保留的实验吸收趋势分开检验化学取代/拓扑与几何作用。

**正文/SI与基线核查。** 正文 Fig2/Table1 明确吸收在 toluene，主环境已按实测定义；没有把另一介质照搬过来。四个原子图、含 B/O/N 的共同螯合顺序和 F 对称性有明确映射，作者计算坐标移入私有快照。 来源定位：Main pp2-3 Fig2/Table1 explicitly identifies toluene absorption; SI p2 methods, pp57-68 coordinate tables. Current experimental_absorption.json is retained as published input.

**评估改动。** 核心矩阵为 `relaxed_monomers`（4行）；`common_geometry`（4行）；`spectral_test`（3行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 142 项。

**可行性、参考缺口和限制。** 需要共几何变形代价、根匹配与独立趋势测试；不要求聚合物、固态白光或量子产率。旧单体谱匹配不能代替新归因对照。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 18. paper_3a22e838133b906d — B → 加强B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_3a22e838133b906d/agent_input/task.md) · [PR](../../paper_reproduction/paper_3a22e838133b906d/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_3a22e838133b906d/evaluation/reference_validation_plan.md)。

**科学升级。** 从旧截短单体扩到完整中性/阴离子、Li 配位、2MeCN 以及晶体支持的2阴离子/2Li/4MeCN二聚模型；定义 P–O···B 目标原子、桥连 O、配位类别与两条守恒反应，旧小模型只作截短控制。

**正文/SI与基线核查。** 查看正文 Scheme1/Fig1 及 Li₂O₂ 描述和 SI 晶体表。公开完整阴离子 C₂₀H₃₁BO₃P⁻ 与138原子二聚组成，使用类别连接构建独立起点，没有生成冒充来源的 CIF。脱乙基以 neutral+LiI→Li·anion+EtI 配平，二聚为2monomer→dimer。 来源定位：Main pp1-3 Scheme1/Fig1, including Li2O2 paragraph p2; SI pp62,69 crystal data and p78 computation; old public model graphs are retained only as labeled truncation controls.

**评估改动。** 核心矩阵为 `coordination_layers`（4行）；`balanced_cycles`（4行）；`truncation_and_mechanism`（2行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 192 项。

**可行性、参考缺口和限制。** 首版必须实际计算完整配位层与最小二聚，不能继续用小单体覆盖。最大规模/频率成本尚待先导；若二聚坍缩需保存真实路径和碎片记账，不假设已存在稳定极小点。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

### 19. paper_98b6f8a0352f72c2 — B → 加强B

状态：`implemented_pending_expanded_reference`。包：[AR](../../autonomous_research/paper_98b6f8a0352f72c2/agent_input/task.md) · [PR](../../paper_reproduction/paper_98b6f8a0352f72c2/agent_input/task.md) · [参考验证计划](../../autonomous_research/paper_98b6f8a0352f72c2/evaluation/reference_validation_plan.md)。

**科学升级。** 定义真实12a(NMe₂)/12d(NEt₂) × CHCl₃/EtOAc，新增统一扭转几何、吸收/发射/绝热能区分、f/跃迁偶极/CT 和辐射速率约定检验。

**正文/SI与基线核查。** 正文合成/光谱/3.1.4 节直接核对，另下载正式 DOCX SI 查看 FigsS31–S39/TableS1。12d 是源系列真实成员；SI 理论寿命不冒充实测寿命，只有 Φ 与 τ 都为实测时才允许实测速率拆分。 来源定位：Main pp3-5 optical tables/Figs and pp7-8 section3.1.4; formal publisher DOCX FigsS31-S39/TableS1 (downloaded and read in batch evidence), member12d synthesis/identity main pp6-7.

**评估改动。** 核心矩阵为 `solvent_series`（4行）；`common_torsion`（4行）；`rates_and_robustness`（3行）；数字、全表与原始任务文件绑定评分。相应对象/缺矩阵/错零点等契约检查已通过，本篇共 116 项。

**可行性、参考缺口和限制。** 源 ORCA 范围分离 TD 路线与独立态映射可实施；新溶剂/扭转/S1参考未跑。实验缺量不被伪造，理论辐射率与实验非辐射通道明确分开。 最低先导见该包 reference_validation_plan，完整参考仍须覆盖全部核心行、驻点/路径/态有效性、方法/构象误差及一次独立升级执行。

## 主进程复核入口与后续门控

逐包路径、官方 package content hash、来源 package hash、源文档哈希、逐篇参考缺口与检查摘要在 `manifest.json`。运行 `PYTHONDONTWRITEBYTECODE=1 .envs/researchchembench/bin/python tasks/upgrade_tasks/coordination_20260927/batch3/check_batch.py` 可重放开发检查。

优先复核两处阻塞：M3 配对的原子级片段/封端，HL 的溶液物种边界。其余17篇先按各自最低先导测量对象/态/路径有效性和实际成本，再计算完整扩展参考与误差边界，使用真实原始产物重放科学正反例。在此之前不将任何包标记为新版科学 PASS。
